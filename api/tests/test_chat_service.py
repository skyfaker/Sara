import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from configs import app_config
from services.chat_service import ChatService


@pytest.fixture
def llm_config():
    """
    Fixture to provide LLM configuration for tests.
    
    ⚠️  IMPORTANT: Fill in these values before running tests ⚠️
    
    Set environment variables or edit this fixture directly:
      - app_config.LLM_API_KEY: Your LLM provider API key
      - app_config.LLM_API_BASE: Optional custom endpoint (vLLM, AiHubMix, etc.)
      - app_config.LLM_DEFAULT_MODEL: Model identifier, e.g. "anthropic/claude-opus-4-5"
    
    Example .env:
        LLM_API_KEY=sk-ant-api03-xxx
        LLM_API_BASE=https://aihubmix.com/v1
        LLM_DEFAULT_MODEL=anthropic/claude-sonnet-4-5
    """
    original_key = app_config.LLM_API_KEY
    original_base = app_config.LLM_API_BASE
    original_model = app_config.LLM_DEFAULT_MODEL

    if not app_config.LLM_API_KEY:
        pytest.skip("LLM_API_KEY not configured. Set it in .env or environment variables.")

    yield {
        "api_key": app_config.LLM_API_KEY,
        "api_base": app_config.LLM_API_BASE,
        "model": app_config.LLM_DEFAULT_MODEL,
    }

    app_config.LLM_API_KEY = original_key
    app_config.LLM_API_BASE = original_base
    app_config.LLM_DEFAULT_MODEL = original_model


def test_chat_non_streaming(llm_config):
    """
    Test non-streaming chat completion.
    
    Sends a simple message and expects a text response.
    """
    messages = [{"role": "user", "content": "Say 'Hello, World!' and nothing else."}]

    response = ChatService.chat(messages, model=llm_config["model"])

    assert isinstance(response, str)
    assert len(response) > 0
    print(f"\n[Non-streaming response]: {response}")


def test_chat_streaming(llm_config):
    """
    Test streaming chat completion.
    
    Sends a message and collects SSE chunks from the generator.
    """
    messages = [{"role": "user", "content": "Count from 1 to 3, one number per line."}]

    chunks = list(ChatService.chat_stream(messages, model=llm_config["model"]))

    assert len(chunks) > 0
    assert all(chunk.startswith("data: ") for chunk in chunks)

    last_chunk = chunks[-1]
    assert '"done": true' in last_chunk

    print(f"\n[Streaming chunks collected]: {len(chunks)}")
    print(f"[First chunk]: {chunks[0]}")
    print(f"[Last chunk]: {last_chunk}")


def test_chat_empty_messages(llm_config):
    """
    Test behavior with empty messages list.
    
    Should not crash, but may return error or empty response.
    """
    messages = []

    try:
        response = ChatService.chat(messages, model=llm_config["model"])
        assert isinstance(response, str)
        print(f"\n[Empty messages response]: {response}")
    except Exception as exc:
        print(f"\n[Empty messages raised exception]: {exc}")
        assert "message" in str(exc).lower() or "invalid" in str(exc).lower()


def test_chat_multi_turn_conversation(llm_config):
    """
    Test multi-turn conversation handling.
    
    Sends multiple messages simulating a back-and-forth conversation.
    """
    messages = [
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "2+2 equals 4."},
        {"role": "user", "content": "What about 3+3?"},
    ]

    response = ChatService.chat(messages, model=llm_config["model"])

    assert isinstance(response, str)
    assert len(response) > 0
    print(f"\n[Multi-turn response]: {response}")
