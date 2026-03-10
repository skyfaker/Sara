import asyncio
import json
import logging
from collections.abc import Generator
from typing import Any

from litellm import acompletion

from configs import app_config
from core.providers.litellm_provider import LiteLLMProvider


class ChatService:
    @staticmethod
    def _build_provider() -> LiteLLMProvider:
        return LiteLLMProvider(
            api_key=app_config.LLM_API_KEY,
            api_base=app_config.LLM_API_BASE,
            default_model=app_config.LLM_DEFAULT_MODEL,
        )

    @staticmethod
    def chat(messages: list[dict[str, Any]], model: str | None = None) -> str:
        provider = ChatService._build_provider()
        response = asyncio.run(
            provider.chat(
                messages=messages,
                model=model or app_config.LLM_DEFAULT_MODEL,
                max_tokens=app_config.LLM_MAX_TOKENS,
                temperature=app_config.LLM_TEMPERATURE,
            )
        )
        return response.content or ""

    @staticmethod
    def chat_stream(
        messages: list[dict[str, Any]],
        model: str | None = None,
    ) -> Generator[str, None, None]:
        provider = ChatService._build_provider()
        resolved_model = provider._resolve_model(model or app_config.LLM_DEFAULT_MODEL)

        kwargs: dict[str, Any] = {
            "model": resolved_model,
            "messages": messages,
            "max_tokens": app_config.LLM_MAX_TOKENS,
            "temperature": app_config.LLM_TEMPERATURE,
            "stream": True,
        }
        if provider.api_base:
            kwargs["api_base"] = provider.api_base
        if provider.extra_headers:
            kwargs["extra_headers"] = provider.extra_headers

        async def _collect_chunks() -> list[str]:
            chunks: list[str] = []
            try:
                stream = await acompletion(**kwargs)
                async for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta:
                        delta = chunk.choices[0].delta
                        if delta.content:
                            chunks.append(delta.content)
            except Exception as exc:
                logging.error("LLM stream error: %s", exc)
                chunks.append(f"[ERROR] {exc}")
            return chunks

        for text_chunk in asyncio.run(_collect_chunks()):
            data = json.dumps({"content": text_chunk, "done": False})
            yield f"data: {data}\n\n"

        yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
