import os
import shutil
import sys
from unittest.mock import AsyncMock, patch, MagicMock

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from core.rag.file_loader.docling_loader import DoclingLoader
from core.rag.file_indexer import FileIndexer
from core.rag.retriever import Retriever
from langchain_core.documents import Document


@pytest.fixture
def temp_dirs(tmp_path):
    index_dir = str(tmp_path / "index_files")
    os.makedirs(index_dir)
    yield index_dir
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)


@pytest.fixture
def mock_documents():
    return [
        Document(
            page_content="第一章 总则\n第一条 为维护社会治安秩序，保障公共安全，制定本法。",
            metadata={"reference": "doc1.docx"}
        ),
        Document(
            page_content="第二条 扰乱公共秩序，妨害公共安全的行为，依照本法给予治安管理处罚。",
            metadata={"reference": "doc1.docx"}
        ),
    ]


@pytest.mark.asyncio
async def test_full_rag_pipeline(temp_dirs, mock_documents):
    index_dir = temp_dirs
    
    mock_description = "这是一份关于治安管理处罚法的文档，涉及维护社会秩序、公共安全等内容。"
    mock_content = """# 治安管理处罚法

## 第一章 总则

### 第一条
为维护社会治安秩序，保障公共安全，制定本法。

### 第二条
扰乱公共秩序，妨害公共安全的行为，依照本法给予治安管理处罚。
"""
    
    with patch('core.rag.file_indexer.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = [mock_description, mock_content]
        
        indexer = FileIndexer(index_dir=index_dir)
        index_path = await indexer.index_documents(
            documents=mock_documents,
            source_file="test_doc.docx",
            file_id="test-uuid-123"
        )
    
    assert os.path.exists(index_path)
    
    retriever = Retriever(index_dir=index_dir, relevance_threshold=0.7)
    
    query = "治安管理的法律规定是什么？"
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = "0.95"
        
        results = await retriever.retrieve(query, top_k=5)
    
    assert len(results) == 1
    assert results[0].source_file == "test_doc.docx"
    assert results[0].relevance_score == 0.95
    assert "治安管理处罚法" in results[0].content


@pytest.mark.asyncio
async def test_multiple_documents_retrieval(temp_dirs):
    index_dir = temp_dirs
    
    doc1 = [Document(page_content="治安管理相关法律条文", metadata={"reference": "doc1.docx"})]
    doc2 = [Document(page_content="劳动合同相关法律条文", metadata={"reference": "doc2.docx"})]
    doc3 = [Document(page_content="Python编程基础教程", metadata={"reference": "doc3.md"})]
    
    indexer = FileIndexer(index_dir=index_dir)
    
    with patch('core.rag.file_indexer.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = [
            "治安管理法律文档", "# 治安管理\n内容1",
            "劳动合同法律文档", "# 劳动合同\n内容2",
            "Python编程文档", "# Python\n内容3"
        ]
        
        await indexer.index_documents(doc1, "doc1.docx", "uuid-1")
        await indexer.index_documents(doc2, "doc2.docx", "uuid-2")
        await indexer.index_documents(doc3, "doc3.md", "uuid-3")
    
    retriever = Retriever(index_dir=index_dir, relevance_threshold=0.6)
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = ["0.9", "0.7", "0.2"]
        
        results = await retriever.retrieve("法律相关的问题", top_k=3)
    
    assert len(results) == 2
    assert results[0].relevance_score == 0.9
    assert results[1].relevance_score == 0.7
    assert results[0].relevance_score >= results[1].relevance_score


@pytest.mark.asyncio
async def test_rag_query_with_no_relevant_documents(temp_dirs):
    index_dir = temp_dirs
    
    doc = [Document(page_content="Python编程基础", metadata={"reference": "python.md"})]
    
    indexer = FileIndexer(index_dir=index_dir)
    
    with patch('core.rag.file_indexer.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = ["Python编程文档", "# Python\nPython基础"]
        await indexer.index_documents(doc, "python.md", "uuid-python")
    
    retriever = Retriever(index_dir=index_dir, relevance_threshold=0.7)
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = "0.1"
        
        results = await retriever.retrieve("法律相关问题", top_k=5)
    
    assert len(results) == 0


def test_rag_sync_workflow(temp_dirs, mock_documents):
    index_dir = temp_dirs
    
    mock_description = "同步测试文档"
    mock_content = "# 同步内容"
    
    with patch('core.rag.file_indexer.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = [mock_description, mock_content]
        
        indexer = FileIndexer(index_dir=index_dir)
        index_path = indexer.index_documents_sync(
            documents=mock_documents,
            source_file="sync_test.docx",
            file_id="sync-uuid"
        )
    
    assert os.path.exists(index_path)
    
    retriever = Retriever(index_dir=index_dir)
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = "0.8"
        
        results = retriever.retrieve_sync("测试查询", top_k=3)
    
    assert len(results) == 1


@pytest.mark.asyncio
async def test_context_building(temp_dirs):
    index_dir = temp_dirs
    
    doc = [Document(page_content="测试内容", metadata={"reference": "test.docx"})]
    
    indexer = FileIndexer(index_dir=index_dir)
    
    with patch('core.rag.file_indexer.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = ["测试描述", "# 测试\n详细内容在这里"]
        await indexer.index_documents(doc, "test.docx", "uuid-test")
    
    retriever = Retriever(index_dir=index_dir)
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = "0.9"
        
        results = await retriever.retrieve("测试", top_k=1)
    
    assert len(results) == 1
    assert "详细内容在这里" in results[0].content
    assert results[0].source_file == "test.docx"


@pytest.mark.asyncio
async def test_top_k_limiting(temp_dirs):
    index_dir = temp_dirs
    
    indexer = FileIndexer(index_dir=index_dir)
    
    for i in range(5):
        doc = [Document(page_content=f"文档{i}内容", metadata={"reference": f"doc{i}.txt"})]
        
        with patch('core.rag.file_indexer.ChatService.chat', new_callable=AsyncMock) as mock_chat:
            mock_chat.side_effect = [f"描述{i}", f"# 文档{i}\n内容{i}"]
            await indexer.index_documents(doc, f"doc{i}.txt", f"uuid-{i}")
    
    retriever = Retriever(index_dir=index_dir, relevance_threshold=0.5)
    
    with patch('core.rag.retriever.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = ["0.9", "0.8", "0.7", "0.6", "0.55"]
        
        results = await retriever.retrieve("查询", top_k=3)
    
    assert len(results) == 3
    assert results[0].relevance_score >= results[1].relevance_score >= results[2].relevance_score
