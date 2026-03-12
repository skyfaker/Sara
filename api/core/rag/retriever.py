import asyncio
import os
from typing import List

from loguru import logger as log

from configs import app_config
from services.chat_service import ChatService


class DocumentChunk:
    def __init__(
        self,
        file_id: str,
        source_file: str,
        description: str,
        content: str,
        relevance_score: float
    ):
        self.file_id = file_id
        self.source_file = source_file
        self.description = description
        self.content = content
        self.relevance_score = relevance_score
    
    def __repr__(self):
        return f"DocumentChunk(source={self.source_file}, score={self.relevance_score:.2f})"


class Retriever:
    """
    Retrieves relevant documents from indexed markdown files.
    
    Two-stage retrieval process:
    1. Scan all markdown files and read description from frontmatter
    2. Use LLM to score relevance of each description to the query
    3. For high-scoring documents, load full content
    4. Return ranked list of relevant document chunks
    """
    
    def __init__(self, index_dir: str = None, relevance_threshold: float = 0.6):
        """
        Initialize the Retriever.
        
        Args:
            index_dir: Directory containing indexed markdown files.
                      Defaults to api/storage/index_files/
            relevance_threshold: Minimum relevance score (0-1) to include document.
                               Default 0.6 means 60% relevance.
        """
        if index_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            api_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
            index_dir = os.path.join(api_dir, 'storage', 'index_files')
        
        self.index_dir = index_dir
        self.relevance_threshold = relevance_threshold
    
    async def retrieve(
        self, 
        query: str, 
        top_k: int = 5
    ) -> List[DocumentChunk]:
        """
        Retrieve relevant documents for a given query.
        
        Args:
            query: User's question or search query
            top_k: Maximum number of documents to return
        
        Returns:
            List of DocumentChunk objects, sorted by relevance (highest first)
        """
        log.info(f"Retrieving documents for query: {query[:100]}...")
        
        documents_metadata = self._scan_index_directory()
        
        if not documents_metadata:
            log.warning("No indexed documents found")
            return []
        
        log.info(f"Found {len(documents_metadata)} indexed documents")
        
        scored_docs = await self._score_documents(query, documents_metadata)
        
        relevant_docs = [
            doc for doc in scored_docs 
            if doc['score'] >= self.relevance_threshold
        ]
        
        log.info(f"Found {len(relevant_docs)} relevant documents above threshold {self.relevance_threshold}")
        
        top_docs = relevant_docs[:top_k]
        document_chunks = []
        
        for doc_meta in top_docs:
            content = self._load_full_content(doc_meta['file_path'])
            chunk = DocumentChunk(
                file_id=doc_meta['file_id'],
                source_file=doc_meta['source_file'],
                description=doc_meta['description'],
                content=content,
                relevance_score=doc_meta['score']
            )
            document_chunks.append(chunk)
        
        log.info(f"Retrieved {len(document_chunks)} document chunks")
        return document_chunks
    
    def _scan_index_directory(self) -> List[dict]:
        if not os.path.exists(self.index_dir):
            log.warning(f"Index directory does not exist: {self.index_dir}")
            return []
        
        documents = []
        
        for filename in os.listdir(self.index_dir):
            if not filename.endswith('.md'):
                continue
            
            file_path = os.path.join(self.index_dir, filename)
            file_id = filename.replace('.md', '')
            
            try:
                metadata = self._parse_frontmatter(file_path)
                documents.append({
                    'file_id': file_id,
                    'file_path': file_path,
                    'source_file': metadata['source_file'],
                    'description': metadata['description']
                })
            except Exception as e:
                log.error(f"Failed to parse {filename}: {e}")
                continue
        
        return documents
    
    def _parse_frontmatter(self, file_path: str) -> dict:
        """
        Parse frontmatter from markdown file to extract description and source_file.
        
        Args:
            file_path: Path to the markdown file
        
        Returns:
            Dictionary with 'description' and 'source_file' keys
        
        Raises:
            ValueError: If frontmatter is missing or malformed
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            raise ValueError("Missing frontmatter")
        
        end_marker = content.find('---', 3)
        if end_marker == -1:
            raise ValueError("Malformed frontmatter")
        
        frontmatter = content[3:end_marker].strip()
        
        metadata = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        if 'description' not in metadata or 'source_file' not in metadata:
            raise ValueError("Missing required frontmatter fields")
        
        return metadata
    
    async def _score_documents(
        self, 
        query: str, 
        documents: List[dict]
    ) -> List[dict]:
        scored_docs = []
        
        tasks = [
            self._score_single_document(query, doc)
            for doc in documents
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for doc, result in zip(documents, results):
            if isinstance(result, Exception):
                log.error(f"Failed to score document {doc['file_id']}: {result}")
                score = 0.0
            else:
                score = result
            
            scored_docs.append({
                **doc,
                'score': score
            })
        
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_docs
    
    async def _score_single_document(self, query: str, doc: dict) -> float:
        prompt = f"""请评估以下文档描述与用户问题的相关性。

用户问题：{query}

文档描述：{doc['description']}

请给出一个0到1之间的相关性分数：
- 1.0 = 非常相关，文档很可能包含问题的答案
- 0.7-0.9 = 相关，文档可能包含有用信息
- 0.4-0.6 = 部分相关，文档可能有间接关系
- 0.1-0.3 = 弱相关，文档与问题关系较远
- 0.0 = 不相关，文档与问题无关

请只输出一个0到1之间的数字，不要包含任何其他文字。"""
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            response = await ChatService.chat(
                messages=messages,
                model=app_config.LLM_DEFAULT_MODEL
            )
            
            score_str = response.strip()
            score = float(score_str)
            
            score = max(0.0, min(1.0, score))
            
            return score
            
        except ValueError as e:
            log.error(f"Failed to parse score from LLM response: {response}. Error: {e}")
            return 0.0
        except Exception as e:
            log.error(f"LLM scoring failed: {e}")
            return 0.0
    
    def _load_full_content(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content_marker = "# Content"
        content_start = content.find(content_marker)
        
        if content_start == -1:
            log.warning(f"No content section found in {file_path}")
            return content
        
        return content[content_start + len(content_marker):].strip()
    
    def retrieve_sync(self, query: str, top_k: int = 5) -> List[DocumentChunk]:
        return asyncio.run(self.retrieve(query, top_k))
