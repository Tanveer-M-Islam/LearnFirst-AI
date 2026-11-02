from app.schemas.enums import (
    AgeGroup,
    AttemptStatus,
    LearningMode,
    MasteryState,
    Subject,
    TutorAction,
    TutorIntent,
)
from app.tutor.decision_models import (
    TutorDecisionInput,
)
from app.tutor.policy_engine import (
    TutorPolicyEngine,
)
from app.tutor.session_state import (
    TutorSessionState,
)


engine = (
    TutorPolicyEngine()
)


def make_state(
    mode: LearningMode,
    current_problem: (
        str | None
    ) = "2x + 5 = 17",
    attempt_count: int = 0,
) -> TutorSessionState:

    return (
        TutorSessionState(
            session_id=(
                "session-1"
            ),

            student_id=(
                "student-1"
            ),

            age_group=(
                AgeGroup
                .DEVELOPING
            ),

            mode=mode,

            subject=(
                Subject.MATH
            ),

            topic=(
                "Linear Equations"
            ),

            concept_code=(
                "MATH_ALG_LINEAR_01"
            ),

            current_problem=(
                current_problem
            ),

            attempt_count=(
                attempt_count
            ),

            hint_level=0,

            direct_answer_requests=0,

            current_misconception=None,

            mastery_state=(
                MasteryState
                .LEARNING
            ),
        )
    )


# ======================================================
# HOMEWORK HELP
# ======================================================

def test_homework_mode_requires_attempt():

    state = (
        make_state(
            LearningMode
            .HOMEWORK_HELP
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .EXPLANATION_REQUEST
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == TutorAction
        .ASK_ATTEMPT
    )


    assert (
        result.allow_final_answer
        is False
    )


def test_homework_mode_allows_guidance_after_attempt():

    state = (
        make_state(
            mode=(
                LearningMode
                .HOMEWORK_HELP
            ),

            attempt_count=1,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .EXPLANATION_REQUEST
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == (
            TutorAction
            .ASK_GUIDING_QUESTION
        )
    )


    assert (
        result.allow_final_answer
        is False
    )


def test_homework_hint_uses_hint_ladder():

    state = (
        make_state(
            mode=(
                LearningMode
                .HOMEWORK_HELP
            ),

            attempt_count=1,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .HINT_REQUEST
                    )
                )
            ),
        )
    )


    assert (
        result.hint_level
        >= 1
    )


    assert (
        result.allow_final_answer
        is False
    )


# ======================================================
# PRACTICE
# ======================================================

def test_practice_mode_expects_attempt():

    state = (
        make_state(
            LearningMode.PRACTICE
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .LEARN_CONCEPT
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == TutorAction
        .ASK_ATTEMPT
    )


def test_practice_mode_can_request_new_problem():

    state = (
        make_state(
            LearningMode.PRACTICE
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .PRACTICE_REQUEST
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == (
            TutorAction
            .GENERATE_PRACTICE_QUESTION
        )
    )


    assert (
        result.allow_final_answer
        is False
    )


def test_practice_correct_attempt_triggers_fresh_problem():

    state = (
        make_state(
            mode=(
                LearningMode
                .PRACTICE
            ),

            attempt_count=1,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .STUDENT_ATTEMPT
                    ),

                    attempt_status=(
                        AttemptStatus
                        .CORRECT
                    ),
                )
            ),
        )
    )


    assert (
        result.next_action
        == (
            TutorAction
            .GIVE_MASTERY_QUESTION
        )
    )


    assert (
        result.requires_mastery_check
        is True
    )


def test_practice_incorrect_attempt_gets_support():

    state = (
        make_state(
            mode=(
                LearningMode
                .PRACTICE
            ),

            attempt_count=1,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .STUDENT_ATTEMPT
                    ),

                    attempt_status=(
                        AttemptStatus
                        .INCORRECT
                    ),
                )
            ),
        )
    )


    assert (
        result.allow_final_answer
        is False
    )


    assert (
        result.hint_level
        >= 1
    )


# ======================================================
# LEARN MODE
# ======================================================

def test_learn_mode_teaches_without_problem():

    state = (
        make_state(
            mode=(
                LearningMode.LEARN
            ),

            current_problem=None,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .LEARN_CONCEPT
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == (
            TutorAction
            .GIVE_FULL_TEACHING_EXPLANATION
        )
    )


    assert (
        result.allow_final_answer
        is True
    )


def test_learn_mode_explanation_teaches_concept():

    state = (
        make_state(
            mode=(
                LearningMode.LEARN
            ),

            current_problem=None,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .EXPLANATION_REQUEST
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == (
            TutorAction
            .GIVE_FULL_TEACHING_EXPLANATION
        )
    )


def test_learn_mode_i_dont_know_teaches():

    state = (
        make_state(
            mode=(
                LearningMode.LEARN
            ),

            current_problem=None,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .I_DONT_KNOW
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == (
            TutorAction
            .GIVE_FULL_TEACHING_EXPLANATION
        )
    )


def test_learn_mode_can_generate_practice():

    state = (
        make_state(
            mode=(
                LearningMode.LEARN
            ),

            current_problem=None,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .PRACTICE_REQUEST
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == (
            TutorAction
            .GENERATE_PRACTICE_QUESTION
        )
    )


    assert (
        result.allow_final_answer
        is False
    )


def test_learn_mode_validates_attempt_after_problem():

    state = (
        make_state(
            mode=(
                LearningMode.LEARN
            ),

            current_problem=(
                "2x + 5 = 17"
            ),

            attempt_count=1,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .STUDENT_ATTEMPT
                    ),

                    attempt_status=(
                        AttemptStatus
                        .CORRECT
                    ),
                )
            ),
        )
    )


    assert (
        result.next_action
        == (
            TutorAction
            .GIVE_MASTERY_QUESTION
        )
    )


# ======================================================
# ANSWER-RESISTANCE
# ======================================================

def test_homework_direct_answer_is_blocked():

    state = (
        make_state(
            mode=(
                LearningMode
                .HOMEWORK_HELP
            ),

            attempt_count=0,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .DIRECT_ANSWER_REQUEST
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == TutorAction
        .ASK_ATTEMPT
    )


    assert (
        result.allow_final_answer
        is False
    )


def test_practice_direct_answer_is_blocked():

    state = (
        make_state(
            mode=(
                LearningMode.PRACTICE
            ),

            attempt_count=0,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .DIRECT_ANSWER_REQUEST
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == TutorAction
        .ASK_ATTEMPT
    )


    assert (
        result.allow_final_answer
        is False
    )


def test_learn_mode_does_not_reveal_problem_answer():

    state = (
        make_state(
            mode=(
                LearningMode.LEARN
            ),

            current_problem=(
                "2x + 5 = 17"
            ),

            attempt_count=0,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .DIRECT_ANSWER_REQUEST
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == TutorAction
        .ASK_ATTEMPT
    )


    assert (
        result.allow_final_answer
        is False
    )


def test_learn_without_problem_redirects_answer_request_to_learning():

    state = (
        make_state(
            mode=(
                LearningMode.LEARN
            ),

            current_problem=None,

            attempt_count=0,
        )
    )


    result = (
        engine.decide(
            state=state,

            decision_input=(
                TutorDecisionInput(
                    intent=(
                        TutorIntent
                        .DIRECT_ANSWER_REQUEST
                    )
                )
            ),
        )
    )


    assert (
        result.next_action
        == (
            TutorAction
            .ASK_PRIOR_KNOWLEDGE
        )
    )


    assert (
        result.allow_final_answer
        is False
    )