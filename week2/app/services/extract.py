from __future__ import annotations

import logging
import os
import re
from typing import List

from ollama import chat
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

logger = logging.getLogger(__name__)

# Default to a small model for lower resource usage; override with OLLAMA_MODEL env.
OLLAMA_EXTRACT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")


class ActionItemsResponse(BaseModel):
    """Schema for LLM action-item extraction: JSON object with an array of strings."""

    items: List[str]

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def extract_action_items_llm(text: str) -> List[str]:
    """
    Extract action items from text using an LLM via Ollama with structured output
    (JSON array of strings). Requires Ollama to be running with a compatible model
    (e.g. ollama run llama3.2:1b).
    """
    text = (text or "").strip()
    if not text:
        return []

    prompt = (
        "Extract all action items, to-dos, tasks, and follow-up items from the following text. "
        "Return each item as a clear, concise phrase. "
        "Return as JSON with a single key \"items\" whose value is an array of strings. "
        "If there are no action items, return an empty array for \"items\".\n\n"
        "Text:\n"
        f"{text}"
    )

    try:
        response = chat(
            model=OLLAMA_EXTRACT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            format=ActionItemsResponse.model_json_schema(),
            options={"temperature": 0},
        )
        raw = (response.message.content or "").strip()
        if not raw:
            return []
        parsed = ActionItemsResponse.model_validate_json(raw)
        return list(parsed.items) if parsed.items else []
    except Exception as e:
        logger.warning("Ollama action-item extraction failed: %s", e)
        return []


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
