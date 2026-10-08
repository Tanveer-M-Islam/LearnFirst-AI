import time

from app.llm.base import LLMProvider
from app.llm.models import (
    LLMRequest,
    LLMResult,
)


class MockLLMProvider(LLMProvider):

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def model_name(self) -> str:
        return "learnfirst-mock-v1"

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResult:

        started = time.perf_counter()

        action = (
            request.metadata.get(
                "action"
            )
        )

        topic = (
            request.metadata.get(
                "topic"
            )
            or "this topic"
        )

        responses = {

            "ASK_ATTEMPT": (
                "Show me what you have tried "
                "so far, even if you are not "
                "sure yet."
            ),

            "ASK_PRIOR_KNOWLEDGE": (
                f"Before we begin {topic}, "
                "what do you already know "
                "about it?"
            ),

            "ASK_GUIDING_QUESTION": (
                "What do you think would be "
                "a useful first step?"
            ),

            "GIVE_HINT": (
                "Think about the key concept "
                "you need here. What operation "
                "or rule might help?"
            ),

            "GIVE_SIMILAR_EXAMPLE": (
                "Let's first look at a similar "
                "example with different values, "
                "then you can return to your "
                "original problem."
            ),

            "BREAK_INTO_STEPS": (
                "Let's make the task smaller. "
                "Focus only on the first step "
                "for now."
            ),

            "GIVE_STRONG_GUIDANCE": (
                "I will guide you closely. "
                "Start with the first operation, "
                "then tell me what you get."
            ),

            "GIVE_FULL_TEACHING_EXPLANATION": (
                "Let's work through the concept "
                "carefully and connect each step "
                "to the rule behind it."
            ),

            "GIVE_MASTERY_QUESTION": (
                "Good work. Now try a fresh "
                "similar question without a hint "
                "to check whether the idea is "
                "clear."
            ),

            "GENERATE_PRACTICE_QUESTION": (
                "Let's try a new practice "
                "question at your current level."
            ),

            "SWITCH_TO_PREREQUISITE": (
                "Before continuing, let's review "
                "one smaller idea that this topic "
                "depends on."
            ),

            "REDIRECT_TO_LEARNING": (
                "Let's bring this back to what "
                "you are learning. What part "
                "would you like help with?"
            ),

            "REFUSE_POLICY_BYPASS": (
                "I can help you work it out, "
                "but I will not skip the learning "
                "steps just to reveal the answer."
            ),

            "CLARIFY_TEST_INSTRUCTION": (
                "This is Mock Test Mode, so I "
                "cannot give hints or solutions "
                "during the test."
            ),

            "RECORD_TEST_RESPONSE": (
                "Your answer has been recorded. "
                "Continue to the next question."
            ),

            "ESCALATE_SAFETY": (
                "I cannot handle this as a normal "
                "learning question. Please involve "
                "a trusted adult who can help."
            ),
        }

        content = responses.get(
            action,
            (
                "Let's work through this "
                "carefully together."
            ),
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