import asyncio
import os
from typing import List

from langchain_core.documents import Document
from loguru import logger as log

from configs import app_config
from services.chat_service import ChatService


class FileIndexer:
    """
    Converts document chunks into structured Markdown with LLM enhancement.
    
    Output format:
    ---
    description: <LLM-generated summary>
    source_file: <original file path>
    ---
    
    # Content
    <LLM-reorganized content with preserved structure>
    """
    
    def __init__(self, index_dir: str = None):
        """
        Initialize the FileIndexer.
        
        Args:
            index_dir: Directory to save indexed markdown files. 
                      Defaults to api/storage/index_files/
        """
        if index_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            api_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
            index_dir = os.path.join(api_dir, 'storage', 'index_files')
        
        self.index_dir = index_dir
        os.makedirs(self.index_dir, exist_ok=True)
    
    async def index_documents(
        self, 
        documents: List[Document], 
        source_file: str,
        file_id: str
    ) -> str:
        """
        Index documents by converting them to structured Markdown.
        
        Args:
            documents: List of Document objects from docling_loader
            source_file: Original file path/name
            file_id: Unique identifier for the file (e.g., UUID)
        
        Returns:
            Path to the generated markdown file
        """
        log.info(f"Indexing {len(documents)} document chunks from {source_file}")
        
        # Combine all chunks
        full_text = "\n\n".join(doc.page_content for doc in documents)
        
        # Generate description (summary) using LLM
        description = await self._generate_description(full_text)
        
        # Reorganize content with structure using LLM
        structured_content = await self._reorganize_content(documents)
        
        # Create markdown file
        markdown_path = os.path.join(self.index_dir, f"{file_id}.md")
        markdown_content = self._create_markdown(
            description=description,
            source_file=source_file,
            content=structured_content
        )
        
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        log.info(f"Indexed file saved to {markdown_path}")
        return markdown_path
    
    async def _generate_description(self, full_text: str) -> str:
        """
        Generate a concise description/summary of the document.
        
        Args:
            full_text: Complete document text
        
        Returns:
            LLM-generated summary
        """
        # Truncate if too long (to fit in context)
        max_chars = 8000
        truncated_text = full_text[:max_chars]
        if len(full_text) > max_chars:
            truncated_text += "\n...(truncated)"
        
        prompt = f"""请为以下文档生成一个简洁的描述摘要（100-200字）。
摘要应该：
1. 概括文档的主要主题和内容
2. 提取关键信息点
3. 帮助快速判断文档是否与特定问题相关

文档内容：
{truncated_text}

请直接输出摘要，不要包含"摘要："等前缀。"""
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            description = await ChatService.chat(
                messages=messages,
                model=app_config.LLM_DEFAULT_MODEL
            )
            return description.strip()
        except Exception as e:
            log.error(f"Failed to generate description: {e}")
            # Fallback: use first 200 characters
            return full_text[:200] + "..."
    
    async def _reorganize_content(self, documents: List[Document]) -> str:
        """
        Reorganize document chunks into structured Markdown with hierarchy.
        
        Args:
            documents: List of Document chunks
        
        Returns:
            Structured markdown content
        """
        # Combine chunks with separators
        chunks_text = "\n\n---CHUNK---\n\n".join(
            doc.page_content for doc in documents
        )
        
        # Truncate if necessary
        max_chars = 15000
        if len(chunks_text) > max_chars:
            chunks_text = chunks_text[:max_chars] + "\n...(内容已截断)"
        
        prompt = f"""请将以下文档片段重新组织为结构化的Markdown格式。

要求：
1. 保留原文的段落结构和层级关系
2. 使用Markdown标题（#, ##, ###）标注章节
3. 保持内容完整性，不要遗漏重要信息
4. 使用合适的Markdown格式（列表、加粗等）提升可读性
5. 如果内容是法律条文、技术文档等，保持原有编号和格式

文档内容（用---CHUNK---分隔）：
{chunks_text}

请直接输出重新组织后的Markdown内容。"""
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            structured_content = await ChatService.chat(
                messages=messages,
                model=app_config.LLM_DEFAULT_MODEL
            )
            return structured_content.strip()
        except Exception as e:
            log.error(f"Failed to reorganize content: {e}")
            # Fallback: simple concatenation
            return "\n\n".join(doc.page_content for doc in documents)
    
    def _create_markdown(
        self, 
        description: str, 
        source_file: str, 
        content: str
    ) -> str:
        """
        Create final markdown file with frontmatter.
        
        Args:
            description: Document summary
            source_file: Original file path
            content: Structured content
        
        Returns:
            Complete markdown string
        """
        markdown = f"""---
description: {description}
source_file: {source_file}
---

# Content

{content}
"""
        return markdown
    
    def index_documents_sync(
        self, 
        documents: List[Document], 
        source_file: str,
        file_id: str
    ) -> str:
        """
        Synchronous wrapper for index_documents.
        
        Args:
            documents: List of Document objects
            source_file: Original file path
            file_id: Unique file identifier
        
        Returns:
            Path to generated markdown file
        """
        return asyncio.run(self.index_documents(documents, source_file, file_id))
