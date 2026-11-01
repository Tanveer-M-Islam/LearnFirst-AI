from app.rag.models import (
    RAGContext,
    RetrievedChunk,
)
from app.schemas.enums import (
    AgeGroup,
    LearningMode,
    MasteryState,
    Subject,
    TutorAction,
    TutorIntent,
)
from app.tutor.decision_models import (
    TutorDecisionResult,
)
from app.tutor.prompt_builder import (
    TutorPromptBuilder,
)
from app.tutor.session_state import (
    TutorSessionState,
)


def test_rag_context_is_added_to_prompt():

    state = TutorSessionState(
        session_id="session-1",

        student_id="student-1",

        age_group=(
            AgeGroup.DEVELOPING
        ),

        mode=(
            LearningMode.LEARN
        ),

        subject=(
            Subject.SCIENCE
        ),

        topic="Photosynthesis",

        concept_code=(
            "SCI_BIO_PHOTO_01"
        ),

        current_problem=None,

        attempt_count=0,

        hint_level=0,

        direct_answer_requests=0,

        current_misconception=None,

        mastery_state=(
            MasteryState.LEARNING
        ),
    )

    decision = (
        TutorDecisionResult(
            session_id="session-1",

            student_id="student-1",

            subject=(
                Subject.SCIENCE
            ),

            mode=(
                LearningMode.LEARN
            ),

            age_group=(
                AgeGroup.DEVELOPING
            ),

            intent=(
                TutorIntent
                .EXPLANATION_REQUEST
            ),

            next_action=(
                TutorAction
                .GIVE_FEEDBACK
            ),

            hint_level=0,

            allow_final_answer=False,

            requires_rag=True,

            requires_validation=False,

            requires_mastery_check=False,

            policy_bypass_detected=False,

            reason=(
                "Science explanation "
                "requires grounding."
            ),
        )
    )

    rag_context = RAGContext(
        query=(
            "Explain photosynthesis."
        ),

        chunks=[
            RetrievedChunk(
                chunk_id="chunk-1",

                source_id=(
                    "BD_SCI_01"
                ),

                title=(
                    "Photosynthesis"
                ),

                subject="SCIENCE",

                concept_code=(
                    "SCI_BIO_PHOTO_01"
                ),

                text=(
                    "Plants use light "
                    "energy to make "
                    "glucose from water "
                    "and carbon dioxide."
                ),

                score=0.9,
            )
        ],
    )

    request = (
        TutorPromptBuilder.build(
            student_message=(
                "Explain "
                "photosynthesis."
            ),

            state=state,

            decision=decision,

            rag_context=(
                rag_context
            ),
        )
    )

    system_prompt = (
        request.messages[0]
        .content
    )

    assert (
        "TRUSTED CURRICULUM CONTEXT"
        in system_prompt
    )

    assert (
        "Plants use light energy"
        in system_prompt
    )

    assert (
        "do not have enough verified"
        in system_prompt
    )