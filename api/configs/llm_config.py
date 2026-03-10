from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class LlmConfig(BaseSettings):
    """Configuration for LLM providers."""

    LLM_API_KEY: Optional[str] = Field(
        description="API key for the LLM provider (Anthropic, OpenAI, OpenRouter, etc.).",
        default=None,
    )

    LLM_API_BASE: Optional[str] = Field(
        description="Custom API base URL (for local deployments, vLLM, AiHubMix, etc.).",
        default=None,
    )

    LLM_DEFAULT_MODEL: str = Field(
        description="Default LLM model identifier, e.g. 'anthropic/claude-opus-4-5'.",
        default="anthropic/claude-opus-4-5",
    )

    LLM_MAX_TOKENS: int = Field(
        description="Maximum number of tokens in a single LLM response.",
        default=4096,
    )

    LLM_TEMPERATURE: float = Field(
        description="Sampling temperature for LLM responses (0.0 – 2.0).",
        default=0.7,
    )
