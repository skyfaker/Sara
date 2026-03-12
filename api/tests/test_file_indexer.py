import os
import shutil
import sys
from unittest.mock import AsyncMock, patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from core.rag.file_indexer import FileIndexer
from langchain_core.documents import Document


@pytest.fixture
def temp_index_dir(tmp_path):
    """Fixture to create a temporary index directory."""
    index_dir = str(tmp_path / "index_files")
    yield index_dir
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)


@pytest.fixture
def sample_documents():
    """Fixture providing sample documents."""
    return [
        Document(
            page_content="第一章 总则\n第一条 为维护社会治安秩序，保障公共安全，保护公民、法人和其他组织的合法权益，规范和保障公安机关及其人民警察依法履行治安管理职责，制定本法。",
            metadata={"reference": "doc1.docx"}
        ),
        Document(
            page_content="第二条 扰乱公共秩序，妨害公共安全，侵犯人身权利、财产权利，妨害社会管理，具有社会危害性，依照《中华人民共和国刑法》的规定构成犯罪的，依法追究刑事责任；尚不够刑事处罚的，由公安机关依照本法给予治安管理处罚。",
            metadata={"reference": "doc1.docx"}
        ),
    ]


@pytest.mark.asyncio
async def test_index_documents(temp_index_dir, sample_documents):
    """Test indexing documents with mocked LLM calls."""
    indexer = FileIndexer(index_dir=temp_index_dir)
    
    mock_description = "这是一份关于治安管理处罚法的文档，主要包含总则部分的内容。"
    mock_content = """# 治安管理处罚法

## 第一章 总则

### 第一条
为维护社会治安秩序，保障公共安全，保护公民、法人和其他组织的合法权益，规范和保障公安机关及其人民警察依法履行治安管理职责，制定本法。

### 第二条
扰乱公共秩序，妨害公共安全，侵犯人身权利、财产权利，妨害社会管理，具有社会危害性，依照《中华人民共和国刑法》的规定构成犯罪的，依法追究刑事责任；尚不够刑事处罚的，由公安机关依照本法给予治安管理处罚。
"""
    
    with patch('core.rag.file_indexer.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = [mock_description, mock_content]
        
        result_path = await indexer.index_documents(
            documents=sample_documents,
            source_file="doc1.docx",
            file_id="test-uuid-123"
        )
    
    # Verify file was created
    assert os.path.exists(result_path)
    assert result_path.endswith("test-uuid-123.md")
    
    # Verify file content
    with open(result_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "description:" in content
    assert "source_file: doc1.docx" in content
    assert "# Content" in content
    assert mock_description in content
    assert "治安管理处罚法" in content


def test_index_documents_sync(temp_index_dir, sample_documents):
    """Test synchronous wrapper for index_documents."""
    indexer = FileIndexer(index_dir=temp_index_dir)
    
    mock_description = "同步测试文档摘要"
    mock_content = "# 同步测试内容"
    
    with patch('core.rag.file_indexer.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = [mock_description, mock_content]
        
        result_path = indexer.index_documents_sync(
            documents=sample_documents,
            source_file="sync_test.docx",
            file_id="sync-uuid-456"
        )
    
    assert os.path.exists(result_path)
    assert result_path.endswith("sync-uuid-456.md")


@pytest.mark.asyncio
async def test_generate_description_fallback(temp_index_dir, sample_documents):
    """Test fallback when LLM fails to generate description."""
    indexer = FileIndexer(index_dir=temp_index_dir)
    
    with patch('core.rag.file_indexer.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        # First call fails (description), second succeeds (content)
        mock_chat.side_effect = [
            Exception("LLM API error"),
            "# Fallback content"
        ]
        
        result_path = await indexer.index_documents(
            documents=sample_documents,
            source_file="fallback_test.docx",
            file_id="fallback-uuid-789"
        )
    
    assert os.path.exists(result_path)
    
    # Verify fallback description was used (first 200 chars + ...)
    with open(result_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "description:" in content
    assert "..." in content


@pytest.mark.asyncio
async def test_reorganize_content_fallback(temp_index_dir, sample_documents):
    """Test fallback when LLM fails to reorganize content."""
    indexer = FileIndexer(index_dir=temp_index_dir)
    
    with patch('core.rag.file_indexer.ChatService.chat', new_callable=AsyncMock) as mock_chat:
        # First call succeeds (description), second fails (content)
        mock_chat.side_effect = [
            "正常的描述",
            Exception("LLM API error")
        ]
        
        result_path = await indexer.index_documents(
            documents=sample_documents,
            source_file="fallback_content.docx",
            file_id="fallback-content-uuid"
        )
    
    assert os.path.exists(result_path)
    
    # Verify fallback content was used (simple concatenation)
    with open(result_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "第一章 总则" in content
    assert "第二条" in content


def test_create_markdown_format(temp_index_dir):
    """Test markdown file format."""
    indexer = FileIndexer(index_dir=temp_index_dir)
    
    markdown = indexer._create_markdown(
        description="测试描述",
        source_file="test.docx",
        content="# 测试内容"
    )
    
    assert markdown.startswith("---")
    assert "description: 测试描述" in markdown
    assert "source_file: test.docx" in markdown
    assert "# Content" in markdown
    assert "# 测试内容" in markdown
