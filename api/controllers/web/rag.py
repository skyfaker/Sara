import asyncio
import logging
from typing import List, Optional

from flask_pydantic import validate
from flask_restx import Resource
from pydantic import BaseModel, Field

from core.rag.retriever import Retriever
from services.chat_service import ChatService


class SourceDocument(BaseModel):
    source_file: str
    relevance_score: float


class RAGQueryRequest(BaseModel):
    query: str = Field(..., description="User's question")
    top_k: int = Field(default=3, description="Maximum number of documents to retrieve")
    model: Optional[str] = None


class RAGQueryResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    status: int = 200


class RAGQuery(Resource):
    @validate()
    def post(self, body: RAGQueryRequest):
        query = body.query
        top_k = body.top_k
        model = body.model
        
        try:
            retriever = Retriever()
            
            document_chunks = asyncio.run(retriever.retrieve(query, top_k=top_k))
            
            if not document_chunks:
                return RAGQueryResponse(
                    answer="抱歉，我在知识库中没有找到相关的文档来回答这个问题。请尝试上传相关文档或换一种方式提问。",
                    sources=[],
                    status=200
                ).model_dump(), 200
            
            context = self._build_context(document_chunks)
            
            messages = [
                {
                    "role": "system",
                    "content": "你是一个专业的AI助手。请基于提供的上下文信息回答用户的问题。如果上下文中没有相关信息，请明确告知用户。回答要准确、简洁、有条理。"
                },
                {
                    "role": "user",
                    "content": f"上下文信息：\n\n{context}\n\n用户问题：{query}\n\n请基于上述上下文信息回答问题。"
                }
            ]
            
            answer = asyncio.run(ChatService.chat(messages, model=model))
            
            sources = [
                SourceDocument(
                    source_file=chunk.source_file,
                    relevance_score=chunk.relevance_score
                )
                for chunk in document_chunks
            ]
            
            return RAGQueryResponse(
                answer=answer,
                sources=sources,
                status=200
            ).model_dump(), 200
            
        except Exception as exc:
            logging.error(f"RAG query error: {exc}")
            return {"status": 500, "message": str(exc)}, 500
    
    def _build_context(self, document_chunks) -> str:
        context_parts = []
        for i, chunk in enumerate(document_chunks, 1):
            context_parts.append(
                f"【文档{i}：{chunk.source_file}】\n{chunk.content}\n"
            )
        return "\n---\n\n".join(context_parts)
