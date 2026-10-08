from app.llm.gateway import (
    LLMGateway,
)
from app.llm.models import (
    LLMMessage,
    LLMRequest,
)
from app.llm.providers.mock_provider import (
    MockLLMProvider,
)


def test_mock_gateway_returns_response():

    gateway = LLMGateway(
        provider=MockLLMProvider()
    )

    request = LLMRequest(
        messages=[
            LLMMessage(
                role="system",
                content="Tutor.",
            ),
            LLMMessage(
                role="user",
                content="Help me.",
            ),
        ],
        metadata={
            "action": "ASK_ATTEMPT",
        },
    )

    result = gateway.generate(
        request
    )

    assert result.provider == "mock"

    assert (
        result.model
        == "learnfirst-mock-v1"
    )

    assert len(result.content) > 0

    assert result.latency_ms >= 0