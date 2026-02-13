# Action Item Extractor

A professional tool designed to convert free-form notes into structured, actionable items. This project demonstrates how to leverage both traditional heuristics and modern Large Language Models (LLMs) to enhance productivity.

## 🚀 Project Overview

The Action Item Extractor is a minimal but powerful FastAPI application that helps users organize their thoughts by automatically identifying tasks from meeting notes or brainstorming sessions. 

Key features include:
- **Dual Extraction Modes**:
  - **Traditional Heuristic**: Uses pattern matching and rule-based logic to quickly identify common task formats.
  - **LLM AI Driven**: Powered by Ollama, utilizing advanced natural language understanding to extract complex or context-heavy action items.
- **Persistent Storage**: Save your raw notes and extracted items in a local SQLite database.
- **Simple Web Interface**: A clean, vanilla JavaScript frontend for immediate interaction.

## 🛠 Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: [SQLite](https://www.sqlite.org/) with [Pydantic](https://docs.pydantic.dev/) for data validation.
- **AI Engine**: [Ollama](https://ollama.com/) (Local LLM execution).
- **Frontend**: Vanilla JavaScript + HTML5.
- **Dependency Management**: [Poetry](https://python-poetry.org/).

## 🏁 Getting Started

### Prerequisites

* **Python 3.12**: The core runtime required for this project.
* **Conda**: For environment isolation and Python version management.
* **Ollama**: Required for LLM-powered features. [Download here](https://ollama.com/).

### Setup & Installation

1. **Create and Activate Environment**:
Initialize a new Conda environment with Python 3.12:
```bash
conda create -n cs146s python=3.12 -y
conda activate cs146s

```


2. **Install Poetry**:
If you don't have Poetry installed, run the official installer:
```bash
curl -sSL https://install.python-poetry.org | python -

```


3. **Install Dependencies**:
Install all project requirements using Poetry (ensure you are in the project root):
```bash
poetry install --no-interaction

```


4. **Launch Ollama**:
Ensure the Ollama application is running on your machine and pull the required model:
```bash
ollama pull llama3.2:1b
ollama run llama3.2:1b

```
### Running the Application

Start the FastAPI server from the project root:

```bash
poetry run uvicorn week2.app.main:app --reload

```

Open your browser and navigate to `http://127.0.0.1:8000/`.

## 🔌 API Reference

### Action Items

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/action-items/extract` | `POST` | Extract items using traditional heuristics. |
| `/action-items/extract-llm` | `POST` | Extract items using the LLM (Ollama). |
| `/action-items` | `GET` | List all action items (supports filtering by `note_id`). |
| `/action-items/{id}/done` | `POST` | Mark a specific item as completed. |

### Notes

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/notes` | `POST` | Create a new note. |
| `/notes` | `GET` | Retrieve a list of all saved notes. |
| `/notes/{id}` | `GET` | Retrieve a single note by its ID. |

## 🧪 Testing

The project includes a suite of unit tests for the extraction logic, including mocked LLM responses to ensure reliable CI/CD.

Run tests using `pytest`:

```bash
# Run all tests in the week2 directory
python -m pytest week2/tests/
```

## 📁 Project Structure

```text
week2/
├── app/
│   ├── db.py            # SQLite database initialization and operations.
│   ├── main.py          # FastAPI app entry point and configuration.
│   ├── routers/         # API endpoint definitions (Action Items & Notes).
│   └── services/        # Core logic, including heuristic and LLM extraction.
├── frontend/            # Web assets (HTML/JS).
├── tests/               # Unit tests for backend services.
└── data/                # Local SQLite database storage (generated at runtime).
```

---
*Developed as part of the Modern Software Development series.*
