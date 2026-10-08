from abc import (
    ABC,
    abstractmethod,
)

from app.llm.models import (
    LLMRequest,
    LLMResult,
)


class LLMProvider(ABC):

    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResult:
        raise NotImplementedError