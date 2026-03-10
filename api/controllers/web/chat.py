import logging
from typing import Optional

from flask import Response, stream_with_context
from flask_pydantic import validate
from flask_restx import Resource
from pydantic import BaseModel

from services.chat_service import ChatService


class MessageItem(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[MessageItem]
    model: Optional[str] = None
    stream: bool = False


class ChatResponseBody(BaseModel):
    content: str
    model: str
    status: int = 200


class Chat(Resource):
    @validate()
    def post(self, body: ChatRequest):
        messages = [m.model_dump() for m in body.messages]

        if body.stream:
            generator = ChatService.chat_stream(messages, model=body.model)
            return Response(
                stream_with_context(generator),
                mimetype="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                },
            )

        try:
            content = ChatService.chat(messages, model=body.model)
        except Exception as exc:
            logging.error("Chat error: %s", exc)
            return {"status": 500, "message": str(exc)}, 500

        return ChatResponseBody(
            content=content,
            model=body.model or "",
            status=200,
        ).model_dump(), 200
