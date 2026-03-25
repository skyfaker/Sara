[简体中文](README.zh-cn.md)
# SaRa - Super agent with rag

An intelligent document Q&A system built on Flask + LLM, supporting DOCX document upload, smart indexing, and retrieval-augmented generation (RAG) based question answering.


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

### Run the Web Server

```bash
cd api
uv run python app.py
```

The server runs at `http://localhost:5001`.

## CLI Usage

> **Prerequisite:** Install the package from the `api/` directory:
> ```bash
> cd api && uv pip install --python .venv/bin/python -e .
> ```
> Then use `sara` directly (with `.venv` activated) or via `.venv/bin/sara`.

### Command Overview

```
sara chat        Start an interactive LLM chat session
sara chat_once   Send a single message to the LLM
sara upload      Upload and index a DOCX file
sara query       Start an interactive RAG Q&A session
sara ask         Ask a single question via RAG
```

---

### 1. `sara chat` — Interactive Chat

```bash
sara chat [--model MODEL] [--stream/--no-stream]
```

**Options:**
- `--model, -m`: LLM model to use (optional, defaults to `LLM_DEFAULT_MODEL` in config)
- `--stream/--no-stream`: Enable/disable streaming output (default: enabled)

**Session commands:**
- `exit`, `quit`: End the session
- `clear`: Clear conversation history

**Examples:**
```bash
sara chat
sara chat --model gpt-4
sara chat --no-stream
```

---

### 2. `sara chat_once` — Single-turn Chat

```bash
sara chat_once "your message" [--model MODEL] [--stream/--no-stream]
```

**Options:**
- `--model, -m`: LLM model to use (optional)
- `--stream/--no-stream`: Enable/disable streaming output (default: disabled)

**Examples:**
```bash
sara chat_once "What is RAG?"
sara chat_once "Explain vector databases" --model gpt-4
sara chat_once "Write a Python function" --stream
```

---

### 3. `sara upload` — Upload and Index a Document

```bash
sara upload <path-to-docx> [--user-id USER_ID]
```

**What it does:**
1. Validates file format (`.docx` only)
2. Uploads the file to storage
3. Loads document content via Docling
4. Calls LLM to restructure content and generate a markdown index
5. Saves the index to `storage/index_files/{file_uuid}.md`

**Options:**
- `--user-id, -u`: User ID for the upload (default: `cli_user`)

**Examples:**
```bash
sara upload tests/test_data/doc1.docx
sara upload document.docx --user-id user123
```

**Sample output:**
```
╭─────────────────╮
│ Uploading File  │
│ File: doc1.docx │
│ Size: 15.59 KB  │
│ User: cli_user  │
╰─────────────────╯
✓ File uploaded successfully
                 Upload Details
 File UUID  06faac32-5845-4416-9db2-769c27ace596
 Filename   doc1.docx
 Size       15.59 KB

Starting automatic indexing...
✓ Loaded 20 document chunks
✓ Indexed successfully
Index saved to: /path/to/storage/index_files/06faac32-...md

✓ Upload and indexing complete!
```

---

### 4. `sara query` — Interactive RAG Q&A

```bash
sara query [--top-k N] [--model MODEL]
```

**Options:**
- `--top-k, -k`: Number of documents to retrieve (default: 3)
- `--model, -m`: LLM model to use (optional)

**Session commands:**
- `exit`, `quit`: End the session
- `sources`: Show sources from the last retrieval

**Examples:**
```bash
sara query
sara query --top-k 5
sara query --model gpt-4 --top-k 3
```

**Sample session:**
```
╭────────────────────────────────────╮
│ SaRa RAG Query                     │
│ Commands: exit, quit, sources      │
│ Top-K: 3                           │
╰────────────────────────────────────╯

Question: What is this document about?

        Retrieved Sources
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Source File ┃ Relevance Score ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ doc1.docx   │            0.90 │
└─────────────┴─────────────────┘

Answer:
This document contains the text of ...

Question: exit
Goodbye!
```

---

### 5. `sara ask` — Single-turn RAG Query

```bash
sara ask "your question" [--top-k N] [--model MODEL] [--show-sources]
```

**Options:**
- `--top-k, -k`: Number of documents to retrieve (default: 3)
- `--model, -m`: LLM model to use (optional)
- `--show-sources, -s`: Display source documents

**Examples:**
```bash
sara ask "What penalties does this law define?"
sara ask "What is public order management?" --show-sources
sara ask "Describe the enforcement process" --top-k 5 --show-sources
```

**Sample output:**
```
$ sara ask "Which department is responsible for public order management?"

根据文档内容，治安管理工作的主管部门如下：
第七条　主管部门
• 全国范围：国务院公安部门负责全国的治安管理工作
• 地方范围：县级以上地方各级人民政府公安机关负责本行政区域内的治安管理工作
```

---

## Web API

### 1. Chat

**Endpoint:** `POST /api/chat`

**Request body:**
```json
{
  "messages": [
    {"role": "user", "content": "Hello"}
  ],
  "model": "gpt-4"
}
```

**Response:**
```json
{
  "response": "Hello! I'm an AI assistant. How can I help you?",
  "status": 200
}
```

---

### 2. File Upload

**Endpoint:** `POST /api/upload_file`

**Request body:** `multipart/form-data`
- `file`: The DOCX file to upload

**Response:**
```json
{
  "file_uuid": "06faac32-5845-4416-9db2-769c27ace596",
  "file_key": "upload_files/06faac32-5845-4416-9db2-769c27ace596.docx",
  "filename": "doc1.docx",
  "extension": "docx",
  "size": 15958
}
```

---

### 3. RAG Query

**Endpoint:** `POST /api/rag/query`

**Request body:**
```json
{
  "query": "What is this document about?",
  "top_k": 3,
  "model": "gpt-4"
}
```

**Response:**
```json
{
  "answer": "This document contains ...",
  "sources": [
    {
      "source_file": "doc1.docx",
      "relevance_score": 0.90
    }
  ],
  "status": 200
}
```

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

## Testing

### Run all tests
```bash
cd api
uv run pytest tests/ -v
```

### Run a specific test file
```bash
uv run pytest tests/test_retriever.py -v
uv run pytest tests/test_rag_integration.py -v
uv run pytest tests/test_file_indexer.py -v
```

### Test coverage

| Module | Tests | Status |
|--------|-------|--------|
| test_chat_service.py | 8 | ✅ |
| test_docling_loader.py | 4 | ✅ |
| test_file_indexer.py | 7 | ✅ |
| test_file_service.py | 4 | ✅ |
| test_rag_integration.py | 6 | ✅ |
| test_retriever.py | 13 | ✅ |
| **Total** | **44** | **✅** |

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
