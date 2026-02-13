from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .. import db


router = APIRouter(prefix="/notes", tags=["notes"])


class NoteCreateRequest(BaseModel):
    """Request body for creating a note."""

    content: str


class NoteResponse(BaseModel):
    """Canonical API representation of a note."""

    id: int
    content: str
    created_at: str


@router.post("", response_model=NoteResponse, status_code=201)
def create_note(payload: NoteCreateRequest) -> NoteResponse:
    """
    Create a new note from raw text content.

    Using a Pydantic request model gives us:
    - Automatic validation and a well-defined schema in OpenAPI docs.
    - A single place to extend the payload in the future (e.g. title, tags).
    """
    content = payload.content.strip()
    if not content:
        # Explicit 400 makes the contract clear to API consumers.
        raise HTTPException(status_code=400, detail="content is required")

    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    if note is None:
        # This should not normally happen, but it makes failure behaviour explicit.
        raise HTTPException(status_code=500, detail="failed to load created note")

    return NoteResponse(
        id=note["id"],
        content=note["content"],
        created_at=note["created_at"],
    )


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteResponse(
        id=row["id"],
        content=row["content"],
        created_at=row["created_at"],
    )


@router.get("", response_model=List[NoteResponse])
def list_all_notes() -> List[NoteResponse]:
    """
    Retrieve all notes from the database.
    """
    rows = db.list_notes()
    return [
        NoteResponse(
            id=r["id"],
            content=r["content"],
            created_at=r["created_at"],
        )
        for r in rows
    ]


