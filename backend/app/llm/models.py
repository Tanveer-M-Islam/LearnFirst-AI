from typing import Any, Literal

from pydantic import (
    BaseModel,
    Field,
)


class LLMMessage(BaseModel):
    role: Literal[
        "system",
        "user",
        "assistant",
    ]

    content: str


class LLMRequest(BaseModel):
    messages: list[LLMMessage]

    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
    )

    max_tokens: int = Field(
        default=300,
        ge=1,
        le=2000,
    )

    metadata: dict[str, Any] = (
        Field(
            default_factory=dict
        )
    )


class LLMResult(BaseModel):
    content: str

    provider: str

    model: str

    latency_ms: float