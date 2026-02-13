import pytest
from unittest.mock import MagicMock, patch

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# ---------------------------------------------------------------------------
# TODO 2: Unit tests for extract_action_items_llm()
# ---------------------------------------------------------------------------
# We mock the Ollama chat() call so tests run without a running Ollama server
# and are fast and deterministic. This satisfies the assignment requirement to
# "write unit tests for extract_action_items_llm() covering multiple inputs".
# We patch the chat function where it is used ('week2.app.services.extract.chat')
# so the LLM is never invoked. Run tests from project root: pytest week2/tests/


def test_extract_action_items_llm_empty_input():
    """
    Empty or whitespace-only input must return [] without calling the LLM.
    Assignment: cover "empty input" for extract_action_items_llm().
    """
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   ") == []
    assert extract_action_items_llm("\n\t\n") == []


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_bullet_list_input(mock_chat):
    """
    Input that looks like bullet lists should be sent to the LLM and the
    structured response (items array) returned. Assignment: cover "bullet lists".
    """
    # Simulate LLM returning a JSON object with an "items" array of strings.
    mock_chat.return_value = MagicMock(
        message=MagicMock(content='{"items": ["Set up database", "Write tests"]}')
    )
    text = """
    Notes from meeting:
    - Set up database
    * Write tests
    """
    items = extract_action_items_llm(text)
    assert items == ["Set up database", "Write tests"]
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_keyword_prefixed_lines(mock_chat):
    """
    Input with keyword-prefixed lines (todo:, action:, etc.) should be
    extracted via the LLM. Assignment: cover "keyword-prefixed lines".
    """
    mock_chat.return_value = MagicMock(
        message=MagicMock(
            content='{"items": ["Review pull request", "Deploy to staging"]}'
        )
    )
    text = """
    todo: Review pull request
    action: Deploy to staging
    """
    items = extract_action_items_llm(text)
    assert items == ["Review pull request", "Deploy to staging"]
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_no_action_items(mock_chat):
    """
    When the LLM returns an empty items array, we must return [].
    Covers the "no action items" branch and ensures we don't crash on empty JSON array.
    """
    mock_chat.return_value = MagicMock(message=MagicMock(content='{"items": []}'))
    text = "Just some narrative. No tasks here."
    items = extract_action_items_llm(text)
    assert items == []
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_returns_empty_on_failure(mock_chat):
    """
    On Ollama/network failure, extract_action_items_llm() must return []
    (per implementation) so callers get a safe, predictable result.
    """
    mock_chat.side_effect = Exception("Connection refused")
    text = "- Do something"
    items = extract_action_items_llm(text)
    assert items == []
