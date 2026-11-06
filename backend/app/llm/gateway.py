
from app.core.config import (
    get_settings,
)
from app.llm.base import (
    LLMProvider,
)
from app.llm.models import (
    LLMRequest,
    LLMResult,
)
from app.llm.providers.mock_provider import (
    MockLLMProvider,
)
from app.llm.providers.ollama_provider import (
    OllamaProvider,
)

from app.services.chat_history_context import (
    active_session_context,
)
from app.services.chat_history_service import (
    ChatHistoryService,
)


class LLMGateway:

    def __init__(
        self,
        provider: LLMProvider | None = None,
    ):

        if provider is not None:

            self.provider = provider
            return

        settings = get_settings()

        provider_name = (
            settings.llm_provider
            .strip()
            .lower()
        )

        if provider_name == "mock":

            self.provider = MockLLMProvider()

        elif provider_name == "ollama":

            self.provider = OllamaProvider()

        else:

            raise ValueError(
                "Unsupported LLM provider: "
                f"{settings.llm_provider}"
            )

    @property
    def provider_name(self) -> str:

        return self.provider.provider_name

    @property
    def model_name(self) -> str:

        return self.provider.model_name

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResult:

        # ==================================
        # Phase E: Conversation memory
        # ==================================

        current = active_session_context.get()

        if current is not None:

            db, session_id = current

            request = (
                ChatHistoryService
                .add_recent_context(
                    db=db,
                    session_id=session_id,
                    request=request,
                    max_messages=12,
                )
            )

        # ==================================
        # Existing LLM provider
        # ==================================

        return self.provider.generate(request)
