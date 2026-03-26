[简体中文](README.zh-cn.md)
# SaRa - Super agent with rag

An intelligent document Q&A system built on Flask + LLM, supporting DOCX document upload, smart indexing, and retrieval-augmented generation (RAG) based question answering.
![](./doc/desktop.png)

## Quick Start

### Requirements

- Python 3.11+
- uv (dependency manager)

### Install Dependencies

```bash
git clone https://github.com/skyfaker/Sara/tree/master
cd api
uv sync
```

### Run the Server

```bash
cd api
uv run python app.py
```

The server runs at `http://localhost:5001`.


---

## RAG Pipeline

### 1. Document Upload and Indexing

```
User uploads DOCX → FileService validates → LocalStorage saves
                                                  ↓
                                           DoclingLoader loads
                                                  ↓
                                        FileIndexer processes (LLM)
                                        ├─ Generates description (summary)
                                        └─ Restructures content
                                                  ↓
                                        Saves markdown index file
```

**Index file format** (`storage/index_files/{file_uuid}.md`):
```markdown
---
description: LLM-generated document summary (100–200 words)
source_file: doc1.docx
---

# Content

LLM-restructured content preserving section hierarchy
```

### 2. Retrieval and Answer Generation

```
User question → Retriever two-stage retrieval
                ├─ Stage 1: Scan descriptions of all indexed markdown files
                ├─ Stage 2: LLM scores each description (0–1)
                ├─ Stage 3: Filter documents above threshold (0.6)
                └─ Stage 4: Load full content of selected documents
                                  ↓
                           Build context
                                  ↓
                           ChatService generates answer
                                  ↓
                           Return answer + sources
```

**Why this works well:**
- **Efficient**: Lightweight description scanning avoids loading all documents upfront
- **Accurate**: LLM scoring ensures semantic relevance
- **Explainable**: Relevance scores and source files are returned with every answer



---

## Configuration

### Environment Variables (`.env`)

```bash
# LLM
LLM_API_KEY=your-api-key
LLM_API_BASE=https://api.openai.com/v1
LLM_DEFAULT_MODEL=gpt-4
LLM_MAX_TOKENS=4096
LLM_TEMPERATURE=0.7

# File upload
FILE_SIZE_LIMIT=50
FILE_EXTENSIONS=txt,docx,pdf

# Storage
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=./storage
```

### Supported File Formats

Currently supported:
- ✅ `.docx` (Microsoft Word)

Planned:
- 🔄 `.pdf`
- 🔄 `.txt`

---

## Tech Stack

- **Web framework**: Flask + Flask-RESTX
- **Async**: asyncio + async/await
- **LLM integration**: LiteLLM (multi-model support)
- **Document parsing**: Docling (IBM open source)
- **CLI**: Typer + Rich
- **Validation**: Pydantic
- **Testing**: Pytest
- **Dependency management**: uv

---

## Development

### Code Style

- `ruff` for linting and formatting
- Type hints required on all functions
- Thin controllers — business logic belongs in services
- Clean Architecture principles

### Linting

```bash
cd api
uv run ruff check .
uv run ruff check --fix .
uv run ruff format .
```

### Database Migrations

```bash
cd api
uv run flask db migrate -m "description"
uv run flask db upgrade
```

---

## Features

### ✨ Core

1. **Smart document indexing** — LLM-generated summaries with preserved document structure
2. **Two-stage retrieval** — Fast description filtering + full content loading with LLM relevance scoring
3. **Multiple interfaces** — Interactive CLI sessions, single-shot CLI commands, REST API
4. **Rich terminal UI** — Tables, panels, Markdown rendering, and live progress via Rich

### 🔒 Security

- File type validation
- File size limits
- Filename sanitization
- Isolated storage paths

---

## License

MIT License

---

## Contributing

Issues and pull requests are welcome.
