[English](README.md)
# SaRa - Super agent with rag

一个基于Flask + LLM的智能文档问答系统，支持DOCX文档上传、智能索引和基于检索增强生成(RAG)的问答。


## 快速开始

### 环境要求

- Python 3.11+
- uv (依赖管理工具)

### 安装依赖

```bash
cd api
uv sync
```

### 运行Web服务

```bash
cd api
uv run python app.py
```

服务将运行在 `http://localhost:5001`

## CLI工具使用指南

> 前提：已在 `api/` 目录下完成安装。
> ```bash
> cd api && uv pip install --python .venv/bin/python -e .
> ```
> 之后可直接使用 `sara` 命令（需激活 `.venv`），或通过 `.venv/bin/sara` 调用。

### 命令总览

```
sara chat        交互式LLM聊天
sara chat_once   单次LLM问答
sara upload      上传并索引DOCX文件
sara query       交互式RAG问答
sara ask         单次RAG问答
```

---

### 1. `sara chat` — 交互式聊天

```bash
sara chat [--model MODEL] [--stream/--no-stream]
```

**选项**:
- `--model, -m`: 指定LLM模型 (可选，默认使用配置中的 `LLM_DEFAULT_MODEL`)
- `--stream/--no-stream`: 启用/禁用流式输出 (默认启用)

**交互命令**:
- `exit`, `quit`: 退出会话
- `clear`: 清除对话历史

**示例**:
```bash
sara chat
sara chat --model gpt-4
sara chat --no-stream
```

---

### 2. `sara chat_once` — 单次问答

```bash
sara chat_once "你的问题" [--model MODEL] [--stream/--no-stream]
```

**选项**:
- `--model, -m`: 指定LLM模型 (可选)
- `--stream/--no-stream`: 启用/禁用流式输出 (默认禁用)

**示例**:
```bash
sara chat_once "什么是RAG?"
sara chat_once "解释一下向量数据库" --model gpt-4
sara chat_once "写一段Python代码" --stream
```

---

### 3. `sara upload` — 文件上传并索引

```bash
sara upload <docx文件路径> [--user-id USER_ID]
```

**功能**:
1. 验证文件格式 (仅支持 `.docx`)
2. 上传文件到存储
3. 自动使用 Docling 加载文档内容
4. 自动调用 LLM 重组内容并生成 markdown 索引
5. 保存索引到 `storage/index_files/{file_uuid}.md`

**选项**:
- `--user-id, -u`: 指定用户ID (默认: `cli_user`)

**示例**:
```bash
sara upload tests/test_data/doc1.docx
sara upload document.docx --user-id user123
```

**输出示例**:
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

### 4. `sara query` — 交互式RAG问答

```bash
sara query [--top-k N] [--model MODEL]
```

**选项**:
- `--top-k, -k`: 检索文档数量 (默认: 3)
- `--model, -m`: 指定LLM模型 (可选)

**交互命令**:
- `exit`, `quit`: 退出会话
- `sources`: 显示上次检索的来源文档

**示例**:
```bash
sara query
sara query --top-k 5
sara query --model gpt-4 --top-k 3
```

**交互示例**:
```
╭────────────────────────────────────╮
│ SaRa RAG Query                     │
│ Commands: exit, quit, sources      │
│ Top-K: 3                           │
╰────────────────────────────────────╯

Question: 这个文档讲的是什么？

        Retrieved Sources
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Source File ┃ Relevance Score ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ doc1.docx   │            0.90 │
└─────────────┴─────────────────┘

Answer:
这个文档是《中华人民共和国治安管理处罚法》的文本内容...

Question: exit
Goodbye!
```

---

### 5. `sara ask` — 单次RAG问答

```bash
sara ask "你的问题" [--top-k N] [--model MODEL] [--show-sources]
```

**选项**:
- `--top-k, -k`: 检索文档数量 (默认: 3)
- `--model, -m`: 指定LLM模型 (可选)
- `--show-sources, -s`: 显示来源文档

**示例**:
```bash
sara ask "这个法律规定了什么处罚原则?"
sara ask "什么是治安管理?" --show-sources
sara ask "处罚流程是怎样的?" --top-k 5 --show-sources
```

**交互示例**
```
> sara ask "治安管理工作有哪个部门负责"
>
2026-03-12 18:34:08.930 | INFO     | core.rag.retriever:retrieve:74 - Retrieving documents for query: 治安管理工作有那个部门负责...
2026-03-12 18:34:08.930 | INFO     | core.rag.retriever:retrieve:82 - Found 1 indexed documents
2026-03-12 18:34:08.931 | INFO     | core.providers.litellm_provider:chat:124 - LiteLLMProvider.chat called with model: hosted_vllm/MiniMax-M2.5
⠙ Retrieving documents...2026-03-12 18:34:13.211 | INFO     | core.rag.retriever:retrieve:91 - Found 1 relevant documents above threshold 0.6
2026-03-12 18:34:13.211 | INFO     | core.rag.retriever:retrieve:107 - Retrieved 1 document chunks
2026-03-12 18:34:13.213 | INFO     | core.providers.litellm_provider:chat:124 - LiteLLMProvider.chat called with model: hosted_vllm/MiniMax-M2.5
根据文档内容，治安管理工作的主管部门如下：
第七条　主管部门
• 全国范围：国务院公安部门负责全国的治安管理工作
 • 地方范围：县级以上地方各级人民政府公安机关负责本行政区域内的治安管理工作
 此外，治安案件的管辖由国务院公安部门规定。
```
---

## Web API接口

### 1. 聊天接口

**端点**: `POST /api/chat`

**请求体**:
```json
{
  "messages": [
    {"role": "user", "content": "你好"}
  ],
  "model": "gpt-4"
}
```

**响应**:
```json
{
  "response": "你好！我是AI助手，有什么可以帮助你的吗？",
  "status": 200
}
```

---

### 2. 文件上传接口

**端点**: `POST /api/upload_file`

**请求体**: multipart/form-data
- `file`: 上传的DOCX文件

**响应**:
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

### 3. RAG查询接口

**端点**: `POST /api/rag/query`

**请求体**:
```json
{
  "query": "这个文档讲的是什么?",
  "top_k": 3,
  "model": "gpt-4"
}
```

**响应**:
```json
{
  "answer": "这个文档是《中华人民共和国治安管理处罚法》...",
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

## RAG工作流程

### 1. 文档上传与索引

```
用户上传DOCX → FileService验证 → LocalStorage保存
                                      ↓
                                DoclingLoader加载
                                      ↓
                          FileIndexer处理 (LLM)
                          ├─ 生成description (摘要)
                          └─ 重组content (结构化)
                                      ↓
                          保存markdown索引文件
```

**索引文件格式** (`storage/index_files/{file_uuid}.md`):
```markdown
---
description: LLM生成的文档摘要 (100-200字)
source_file: doc1.docx
---

# Content

LLM重新组织的结构化内容，保留段落层级关系
```

### 2. 智能检索与问答

```
用户提问 → Retriever两阶段检索
            ├─ 阶段1: 扫描所有markdown的description
            ├─ 阶段2: LLM对description评分 (0-1)
            ├─ 阶段3: 筛选高于阈值(0.6)的文档
            └─ 阶段4: 加载完整content
                        ↓
                    构建上下文
                        ↓
                    ChatService生成答案
                        ↓
                    返回答案+来源
```

**检索策略优势**:
- **高效**: 先用轻量级description快速筛选，避免加载所有文档
- **精准**: LLM评分确保语义相关性
- **可解释**: 返回相关性评分和来源文档

---

## 测试

### 运行所有测试
```bash
cd api
uv run pytest tests/ -v
```

### 运行特定测试
```bash
# 测试RAG检索器
uv run pytest tests/test_retriever.py -v

# 测试RAG集成
uv run pytest tests/test_rag_integration.py -v

# 测试文件索引
uv run pytest tests/test_file_indexer.py -v
```

### 测试覆盖率

| 测试模块 | 测试数量 | 状态 |
|---------|---------|------|
| test_chat_service.py | 8 | ✅ |
| test_docling_loader.py | 4 | ✅ |
| test_file_indexer.py | 7 | ✅ |
| test_file_service.py | 4 | ✅ |
| test_rag_integration.py | 6 | ✅ |
| test_retriever.py | 13 | ✅ |
| **总计** | **44** | **✅** |

---

## 配置说明

### 环境变量 (`.env`)

```bash
# LLM配置
LLM_API_KEY=your-api-key
LLM_API_BASE=https://api.openai.com/v1
LLM_DEFAULT_MODEL=gpt-4
LLM_MAX_TOKENS=4096
LLM_TEMPERATURE=0.7

# 文件配置
FILE_SIZE_LIMIT=50
FILE_EXTENSIONS=txt,docx,pdf

# 存储配置
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=./storage
```

### 支持的文件格式

当前版本支持:
- ✅ `.docx` (Microsoft Word文档)

计划支持:
- 🔄 `.pdf` (PDF文档)
- 🔄 `.txt` (纯文本)

---

## 核心技术

- **Web框架**: Flask + Flask-RESTX
- **异步处理**: asyncio + async/await
- **LLM集成**: LiteLLM (支持多种模型)
- **文档解析**: Docling (IBM开源)
- **CLI框架**: Typer + Rich (精美终端UI)
- **数据验证**: Pydantic
- **测试框架**: Pytest
- **依赖管理**: uv

---

## 开发指南

### 代码规范

- 使用 `ruff` 进行代码检查和格式化
- 所有函数必须有类型注解
- 控制器层薄化，业务逻辑在服务层
- 遵循Clean Architecture原则

### 运行代码检查

```bash
cd api

# 检查代码
uv run ruff check .

# 自动修复
uv run ruff check --fix .

# 格式化代码
uv run ruff format .
```

### 数据库迁移

```bash
cd api

# 生成迁移
uv run flask db migrate -m "描述"

# 应用迁移
uv run flask db upgrade
```

---

## 项目特性

### ✨ 核心特性

1. **智能文档索引**
   - LLM自动生成文档摘要
   - 保留原文结构和层级关系
   - 支持增量索引

2. **两阶段检索**
   - 快速描述筛选 + 完整内容加载
   - LLM语义相关性评分
   - 可配置相关性阈值

3. **多种交互方式**
   - CLI交互式会话
   - CLI单次查询
   - REST API接口

4. **精美终端UI**
   - Rich库驱动的表格、面板、Markdown渲染
   - 实时进度显示
   - 彩色输出和图标

### 🔒 安全特性

- 文件类型验证
- 文件大小限制
- 文件名非法字符检查
- 存储路径隔离

---

## 许可证

MIT License

---

## 贡献

欢迎提交Issue和Pull Request！

---

## 联系方式

如有问题或建议，请提交Issue。
