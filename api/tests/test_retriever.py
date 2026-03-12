import os
import shutil
import sys
from unittest.mock import AsyncMock, patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from core.rag.retriever import Retriever, DocumentChunk


@pytest.fixture
def temp_index_dir(tmp_path):
    index_dir = str(tmp_path / "index_files")
    os.makedirs(index_dir)
    yield index_dir
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)


@pytest.fixture
def sample_indexed_files(temp_index_dir):
    doc1_content = """---
description: 这是一份关于治安管理处罚法的文档，主要包含总则部分的内容，涉及立法目的、适用范围等。
source_file: doc1.docx
---

# Content

# 治安管理处罚法

## 第一章 总则

### 第一条
为维护社会治安秩序，保障公共安全，保护公民、法人和其他组织的合法权益，规范和保障公安机关及其人民警察依法履行治安管理职责，制定本法。
"""
    
    doc2_content = """---
description: 这是一份关于劳动合同法的文档，主要介绍劳动合同的签订、履行、解除等内容。
source_file: doc2.docx
---

# Content

# 劳动合同法

## 第一章 总则

### 第一条
为了完善劳动合同制度，明确劳动合同双方当事人的权利和义务，保护劳动者的合法权益，构建和发展和谐稳定的劳动关系，制定本法。
"""
    
    doc3_content = """---
description: 这是一份关于Python编程的技术文档，包含函数、类、模块等概念的介绍。
source_file: python_guide.md
---

# Content

# Python Programming Guide

## Functions

Functions are reusable blocks of code that perform specific tasks.
"""
    
    with open(os.path.join(temp_index_dir, "uuid-doc1.md"), 'w', encoding='utf-8') as f:
        f.write(doc1_content)
    
    with open(os.path.join(temp_index_dir, "uuid-doc2.md"), 'w', encoding='utf-8') as f:
        f.write(doc2_content)
    
    with open(os.path.join(temp_index_dir, "uuid-doc3.md"), 'w', encoding='utf-8') as f:
        f.write(doc3_content)
    
    return temp_index_dir


def test_scan_index_directory(temp_index_dir, sample_indexed_files):
    retriever = Retriever(index_dir=temp_index_dir)
    documents = retriever._scan_index_directory()
    
    assert len(documents) == 3
    assert all('file_id' in doc for doc in documents)
    assert all('description' in doc for doc in documents)
    assert all('source_file' in doc for doc in documents)


def test_parse_frontmatter(temp_index_dir, sample_indexed_files):
    retriever = Retriever(index_dir=temp_index_dir)
    file_path = os.path.join(temp_index_dir, "uuid-doc1.md")
    
    metadata = retriever._parse_frontmatter(file_path)
    
    assert 'description' in metadata
    assert 'source_file' in metadata
    assert metadata['source_file'] == "doc1.docx"
    assert "治安管理处罚法" in metadata['description']


def test_parse_frontmatter_missing(temp_index_dir):
    retriever = Retriever(index_dir=temp_index_dir)
    
    invalid_file = os.path.join(temp_index_dir, "invalid.md")
    with open(invalid_file, 'w', encoding='utf-8') as f:
        f.write("# No frontmatter here")
    
    with pytest.raises(ValueError, match="Missing frontmatter"):
        retriever._parse_frontmatter(invalid_file)


def test_load_full_content(temp_index_dir, sample_indexed_files):
    retriever = Retriever(index_dir=temp_index_dir)
    file_path = os.path.join(temp_index_dir, "uuid-doc1.md")
    
    content = retriever._load_full_content(file_path)
    
    assert "# 治安管理处罚法" in content
    assert "## 第一章 总则" in content
    assert "description:" not in content


@pytest.mark.asyncio
async def test_score_single_document(temp_index_dir):
    retriever = Retriever(index_dir=temp_index_dir)
    
    doc = {
        'file_id': 'test-id',
        'description': '这是一份关于治安管理处罚法的文档'
    }
    
    query = "治安管理的法律规定是什么？"
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = "0.9"
        
        score = await retriever._score_single_document(query, doc)
    
    assert 0.0 <= score <= 1.0
    assert score == 0.9


@pytest.mark.asyncio
async def test_score_single_document_invalid_response(temp_index_dir):
    retriever = Retriever(index_dir=temp_index_dir)
    
    doc = {
        'file_id': 'test-id',
        'description': '测试文档'
    }
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = "not a number"
        
        score = await retriever._score_single_document("test query", doc)
    
    assert score == 0.0


@pytest.mark.asyncio
async def test_score_single_document_clamping(temp_index_dir):
    retriever = Retriever(index_dir=temp_index_dir)
    
    doc = {'file_id': 'test', 'description': 'test'}
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = "1.5"
        score = await retriever._score_single_document("query", doc)
        assert score == 1.0
        
        mock_chat.return_value = "-0.5"
        score = await retriever._score_single_document("query", doc)
        assert score == 0.0


@pytest.mark.asyncio
async def test_retrieve(temp_index_dir, sample_indexed_files):
    retriever = Retriever(index_dir=temp_index_dir, relevance_threshold=0.7)
    
    query = "治安管理的相关法律规定"
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = ["0.95", "0.3", "0.1"]
        
        results = await retriever.retrieve(query, top_k=5)
    
    assert len(results) == 1
    assert isinstance(results[0], DocumentChunk)
    assert results[0].source_file == "doc1.docx"
    assert results[0].relevance_score == 0.95
    assert "治安管理处罚法" in results[0].content


@pytest.mark.asyncio
async def test_retrieve_top_k_limit(temp_index_dir, sample_indexed_files):
    retriever = Retriever(index_dir=temp_index_dir, relevance_threshold=0.5)
    
    query = "法律相关内容"
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = ["0.9", "0.8", "0.7"]
        
        results = await retriever.retrieve(query, top_k=2)
    
    assert len(results) == 2
    assert results[0].relevance_score >= results[1].relevance_score


@pytest.mark.asyncio
async def test_retrieve_no_results(temp_index_dir, sample_indexed_files):
    retriever = Retriever(index_dir=temp_index_dir, relevance_threshold=0.9)
    
    query = "完全不相关的问题"
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = ["0.1", "0.2", "0.05"]
        
        results = await retriever.retrieve(query, top_k=5)
    
    assert len(results) == 0


def test_retrieve_sync(temp_index_dir, sample_indexed_files):
    retriever = Retriever(index_dir=temp_index_dir, relevance_threshold=0.6)
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = ["0.85", "0.4", "0.2"]
        
        results = retriever.retrieve_sync("治安管理", top_k=3)
    
    assert len(results) == 1
    assert results[0].relevance_score == 0.85


def test_retrieve_empty_directory(temp_index_dir):
    retriever = Retriever(index_dir=temp_index_dir)
    
    results = retriever.retrieve_sync("test query")
    
    assert len(results) == 0


@pytest.mark.asyncio
async def test_score_documents_parallel(temp_index_dir, sample_indexed_files):
    retriever = Retriever(index_dir=temp_index_dir)
    
    documents = retriever._scan_index_directory()
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = ["0.9", "0.5", "0.3"]
        
        scored = await retriever._score_documents("test query", documents)
    
    assert len(scored) == 3
    assert scored[0]['score'] >= scored[1]['score'] >= scored[2]['score']
    assert mock_chat.call_count == 3
