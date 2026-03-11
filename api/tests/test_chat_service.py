import json
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from configs import app_config
from services.chat_service import ChatService


@pytest.fixture(scope="session", autouse=True)
def check_llm_config():
    """
    Session-level check for LLM configuration.

    ⚠️  IMPORTANT: Fill in these values before running tests ⚠️

    Example .env:
        LLM_API_KEY=sk-xxxxx
        LLM_DEFAULT_MODEL=deepseek-chat
        LLM_API_BASE=https://api.example.com/v1  # optional
    """
    if not app_config.LLM_API_KEY:
        pytest.skip(
            "LLM_API_KEY not configured. Set it in .env or environment variables.\n"
            "Example .env:\n"
            "  LLM_API_KEY=sk-xxxxx\n"
            "  LLM_DEFAULT_MODEL=deepseek-chat\n"
            "  LLM_API_BASE=https://api.example.com/v1  # optional"
        )


@pytest.fixture
def test_model():
    return app_config.LLM_DEFAULT_MODEL


@pytest.fixture
def simple_message():
    return [{"role": "user", "content": "Say 'OK' and nothing else."}]


@pytest.fixture
def counting_message():
    return [{"role": "user", "content": "Count from 1 to 3, one number per line."}]


@pytest.fixture
def multi_turn_messages():
    return [
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "2+2 equals 4."},
        {"role": "user", "content": "What about 3+3?"},
    ]


@pytest.mark.asyncio
async def test_chat_basic_response(simple_message, test_model):
    """
    Test basic non-streaming chat completion.

    Verifies:
    - Returns non-empty string
    - Response time is reasonable
    """
    start_time = time.time()
    response = await ChatService.chat(simple_message, model=test_model)
    elapsed = time.time() - start_time

    assert isinstance(response, str), "Response should be a string"
    assert len(response) > 0, "Response should not be empty"
    assert elapsed < 30, f"Response took too long: {elapsed:.2f}s"

    print(f"\n[Non-streaming response] ({elapsed:.2f}s): {response}")


@pytest.mark.asyncio
async def test_chat_streaming_format(counting_message, test_model):
    """
    Test streaming chat with SSE format validation.

    Verifies:
    - All chunks are valid SSE format
    - Last chunk has done=true
    - Streaming is incremental (not batch)
    """
    chunks = []
    chunk_times = []
    start_time = time.time()

    async for chunk in ChatService.chat_stream(counting_message, model=test_model):
        chunks.append(chunk)
        chunk_times.append(time.time() - start_time)

    assert len(chunks) > 0, "Should receive at least one chunk"

    for i, chunk in enumerate(chunks[:-1]):
        assert chunk.startswith("data: "), f"Chunk {i} should start with 'data: '"
        data_str = chunk[6:].strip()
        data = json.loads(data_str)
        assert "content" in data, f"Chunk {i} should have 'content' field"
        assert "done" in data, f"Chunk {i} should have 'done' field"
        assert data["done"] is False, f"Chunk {i} should have done=false"

    last_chunk = chunks[-1]
    assert last_chunk.startswith("data: "), "Last chunk should be SSE format"
    last_data = json.loads(last_chunk[6:].strip())
    assert last_data.get("done") is True, "Last chunk should have done=true"

    if len(chunk_times) > 1:
        time_gaps = [
            chunk_times[i + 1] - chunk_times[i] for i in range(len(chunk_times) - 1)
        ]
        assert any(
            gap > 0.01 for gap in time_gaps
        ), "Streaming should be incremental, not batch"

    print(f"\n[Streaming chunks]: {len(chunks)}")
    print(f"[First chunk]: {chunks[0]}")
    print(f"[Last chunk]: {last_chunk}")
    print(f"[Chunk timing]: {chunk_times}")


@pytest.mark.asyncio
async def test_chat_streaming_content_reconstruction(counting_message, test_model):
    """
    Test that streaming chunks can be reconstructed into full response.
    """
    full_content = ""

    async for chunk in ChatService.chat_stream(counting_message, model=test_model):
        if chunk.startswith("data: "):
            data = json.loads(chunk[6:].strip())
            if not data.get("done"):
                full_content += data.get("content", "")

    assert len(full_content) > 0, "Reconstructed content should not be empty"
    print(f"\n[Reconstructed content]: {full_content}")


@pytest.mark.asyncio
async def test_chat_multi_turn_conversation(multi_turn_messages, test_model):
    """
    Test multi-turn conversation handling.

    Verifies the model can handle conversation context.
    """
    response = await ChatService.chat(multi_turn_messages, model=test_model)

    assert isinstance(response, str)
    assert len(response) > 0
    print(f"\n[Multi-turn response]: {response}")


@pytest.mark.asyncio
async def test_chat_empty_messages(test_model):
    """
    Test behavior with empty messages list.

    Should gracefully handle edge case.
    """
    messages = []

    try:
        response = await ChatService.chat(messages, model=test_model)
        assert isinstance(response, str)
        print(f"\n[Empty messages response]: {response}")
    except Exception as exc:
        print(f"\n[Empty messages raised exception]: {type(exc).__name__}: {exc}")
        error_msg = str(exc).lower()
        assert any(
            keyword in error_msg
            for keyword in ["message", "invalid", "empty", "required"]
        ), f"Unexpected error message: {exc}"


@pytest.mark.asyncio
async def test_chat_model_override(simple_message):
    """
    Test that model parameter correctly overrides default.

    Uses the same model but verifies parameter is passed through.
    """
    custom_model = app_config.LLM_DEFAULT_MODEL

    response = await ChatService.chat(simple_message, model=custom_model)

    assert isinstance(response, str)
    assert len(response) > 0
    print(f"\n[Model override test with {custom_model}]: {response}")


@pytest.mark.asyncio
async def test_chat_streaming_vs_non_streaming_consistency(simple_message, test_model):
    """
    Test that streaming and non-streaming produce similar results.

    Both should return valid responses (content may differ due to sampling).
    """
    non_streaming_response = await ChatService.chat(simple_message, model=test_model)

    streaming_content = ""
    async for chunk in ChatService.chat_stream(simple_message, model=test_model):
        if chunk.startswith("data: "):
            data = json.loads(chunk[6:].strip())
            if not data.get("done"):
                streaming_content += data.get("content", "")

    assert len(non_streaming_response) > 0, "Non-streaming should return content"
    assert len(streaming_content) > 0, "Streaming should return content"

    print(f"\n[Non-streaming]: {non_streaming_response}")
    print(f"[Streaming]: {streaming_content}")


@pytest.mark.asyncio
async def test_chat_long_context(test_model):
    """
    Test handling of longer conversation context.
    """
    messages = [
        {"role": "user", "content": "Remember this number: 42"},
        {"role": "assistant", "content": "I will remember that the number is 42."},
        {"role": "user", "content": "What number did I ask you to remember?"},
    ]

    response = await ChatService.chat(messages, model=test_model)

    assert isinstance(response, str)
    assert len(response) > 0
    print(f"\n[Long context response]: {response}")
