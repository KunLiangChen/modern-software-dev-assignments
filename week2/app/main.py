from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .routers import action_items, notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Responsibilities:
    - Initialize the database schema once at startup.
    - Provide a single, well-defined place to extend app lifecycle behaviour
      (e.g. background task shutdown, connection pool cleanup) in the future.
    """
    from .db import init_db  # Local import to avoid side effects on module import.

    init_db()
    yield

# Create
app = FastAPI(title="Action Item Extractor", lifespan=lifespan)

#Return html file to browser(application layer)
@app.get("/", response_class=HTMLResponse)
def index() -> str:
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    return html_path.read_text(encoding="utf-8")


app.include_router(notes.router)
app.include_router(action_items.router)


static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")