import asyncio
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
        logging.info(
            f"Received chat request with {len(messages)} messages, model: {body.model}, stream: {body.stream}"
        )
        if body.stream:

            def sync_stream_wrapper():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    async_gen = ChatService.chat_stream(messages, model=body.model)
                    while True:
                        try:
                            chunk = loop.run_until_complete(async_gen.__anext__())
                            yield chunk
                        except StopAsyncIteration:
                            break
                finally:
                    loop.close()

            return Response(
                stream_with_context(sync_stream_wrapper()),
                mimetype="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                },
            )

        try:
            content = asyncio.run(ChatService.chat(messages, model=body.model))
        except Exception as exc:
            logging.error("Chat error: %s", exc)
            return {"status": 500, "message": str(exc)}, 500

        return (
            ChatResponseBody(
                content=content,
                model=body.model or "",
                status=200,
            ).model_dump(),
            200,
        )
