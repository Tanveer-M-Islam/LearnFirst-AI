import time

import httpx

from app.core.config import (
    get_settings,
)
from app.llm.base import LLMProvider
from app.llm.models import (
    LLMRequest,
    LLMResult,
)


class OllamaProvider(LLMProvider):

    def __init__(self):
        settings = get_settings()

        self.base_url = (
            settings.ollama_base_url
            .rstrip("/")
        )

        self.model = (
            settings.ollama_model
        )

        self.timeout = (
            settings
            .ollama_timeout_seconds
        )

    @property
    def provider_name(self) -> str:
        return "ollama"

    @property
    def model_name(self) -> str:
        return self.model

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResult:

        started = time.perf_counter()

        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {
                    "role": message.role,
                    "content": (
                        message.content
                    ),
                }
                for message
                in request.messages
            ],
            "options": {
                "temperature": (
                    request.temperature
                ),
                "num_predict": (
                    request.max_tokens
                ),
            },
        }

        try:
            with httpx.Client(
                timeout=self.timeout
            ) as client:

                response = client.post(
                    (
                        f"{self.base_url}"
                        "/api/chat"
                    ),
                    json=payload,
                )

                response.raise_for_status()

                data = response.json()

        except httpx.ConnectError as exc:

            raise RuntimeError(
                "Could not connect to Ollama. "
                "Make sure Ollama is running."
            ) from exc

        except httpx.HTTPStatusError as exc:

            raise RuntimeError(
                "Ollama returned an HTTP "
                f"error: {exc.response.status_code}"
            ) from exc

        content = (
            data
            .get(
                "message",
                {},
            )
            .get(
                "content",
                "",
            )
            .strip()
        )

        if not content:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        elapsed = (
            time.perf_counter()
            - started
        ) * 1000

        return LLMResult(
            content=content,
            provider=self.provider_name,
            model=self.model_name,
            latency_ms=elapsed,
        )