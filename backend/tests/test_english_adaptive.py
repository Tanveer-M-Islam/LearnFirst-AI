from app.english.adaptive_engine import (
    EnglishAdaptiveEngine,
    EnglishAdaptiveSignals,
)
from app.schemas.adaptive import (
    AdaptiveSupport,
)
from app.schemas.english_adaptive import (
    EnglishAdaptiveActivity,
)
from app.schemas.enums import (
    AgeGroup,
    DifficultyLevel,
    MasteryState,
)


def create_student(
    client,
    age: int = 10,
    grade: str = "5",
):

    response = client.post(
        "/api/v1/students",

        json={
            "display_name":
                "English Learner",

            "age":
                age,

            "grade":
                grade,
        },
    )


    assert (
        response.status_code
        == 201
    )


    return response.json()


def test_new_english_learner_starts_learning(
    client,
):

    student = (
        create_student(
            client=client,
            age=10,
            grade="5",
        )
    )


    response = client.get(
        (
            "/api/v1/english/adaptive/"
            f"students/{student['id']}"
            "/concepts/"
            "ENG_GRAMMAR_TENSE_01"
            "/plan"
        )
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "mastery_state"
        ]
        == "NOT_STARTED"
    )


    assert (
        data[
            "difficulty"
        ]
        == "EASY"
    )


    assert (
        data[
            "next_activity"
        ]
        == "START_LEARNING"
    )


    assert (
        data[
            "next_question"
        ]
        is not None
    )


    assert (
        data[
            "next_question"
        ][
            "difficulty"
        ]
        == "EASY"
    )


def test_unknown_english_concept_returns_404(
    client,
):

    student = (
        create_student(
            client=client
        )
    )


    response = client.get(
        (
            "/api/v1/english/adaptive/"
            f"students/{student['id']}"
            "/concepts/"
            "ENG_UNKNOWN_01"
            "/plan"
        )
    )


    assert (
        response.status_code
        == 404
    )


def test_no_attempts_produces_not_started():

    signals = (
        EnglishAdaptiveSignals(
            age_group=(
                AgeGroup.DEVELOPING
            ),

            total_attempts=0,

            correct_attempts=0,

            partial_attempts=0,

            understanding_score_percent=0.0,

            independent_attempt_rate=0.0,

            independent_success_rate=0.0,

            average_hint_level=0.0,

            direct_answer_requests=0,
        )
    )


    decision = (
        EnglishAdaptiveEngine
        .decide(
            signals
        )
    )


    assert (
        decision.mastery_state
        == MasteryState.NOT_STARTED
    )


    assert (
        decision.difficulty
        == DifficultyLevel.EASY
    )


    assert (
        decision.next_activity
        == (
            EnglishAdaptiveActivity
            .START_LEARNING
        )
    )


def test_low_understanding_triggers_review():

    signals = (
        EnglishAdaptiveSignals(
            age_group=(
                AgeGroup.DEVELOPING
            ),

            total_attempts=4,

            correct_attempts=1,

            partial_attempts=0,

            understanding_score_percent=25.0,

            independent_attempt_rate=75.0,

            independent_success_rate=33.3,

            average_hint_level=3.0,

            direct_answer_requests=1,
        )
    )


    decision = (
        EnglishAdaptiveEngine
        .decide(
            signals
        )
    )


    assert (
        decision.mastery_state
        == MasteryState.LEARNING
    )


    assert (
        decision.difficulty
        == DifficultyLevel.EASY
    )


    assert (
        decision.next_activity
        == (
            EnglishAdaptiveActivity
            .REVIEW_CONCEPT
        )
    )


def test_high_hint_use_gives_strong_support():

    signals = (
        EnglishAdaptiveSignals(
            age_group=(
                AgeGroup.FOUNDATION
            ),

            total_attempts=4,

            correct_attempts=1,

            partial_attempts=1,

            understanding_score_percent=37.5,

            independent_attempt_rate=50.0,

            independent_success_rate=50.0,

            average_hint_level=5.0,

            direct_answer_requests=0,
        )
    )


    decision = (
        EnglishAdaptiveEngine
        .decide(
            signals
        )
    )


    assert (
        decision.support_level
        == AdaptiveSupport.STRONG
    )


def test_strong_english_performance():

    signals = (
        EnglishAdaptiveSignals(
            age_group=(
                AgeGroup.INDEPENDENT
            ),

            total_attempts=6,

            correct_attempts=5,

            partial_attempts=1,

            understanding_score_percent=91.7,

            independent_attempt_rate=83.3,

            independent_success_rate=80.0,

            average_hint_level=1.0,

            direct_answer_requests=0,
        )
    )


    decision = (
        EnglishAdaptiveEngine
        .decide(
            signals
        )
    )


    assert (
        decision.mastery_state
        == MasteryState.STRONG
    )


    assert (
        decision.difficulty
        == DifficultyLevel.CHALLENGING
    )


    assert (
        decision.support_level
        == AdaptiveSupport.GENTLE
    )


    assert (
        decision.next_activity
        == (
            EnglishAdaptiveActivity
            .CHALLENGE_QUESTION
        )
    )


def test_fast_response_alone_does_not_raise_difficulty():

    signals = (
        EnglishAdaptiveSignals(
            age_group=(
                AgeGroup.DEVELOPING
            ),

            total_attempts=3,

            correct_attempts=1,

            partial_attempts=0,

            understanding_score_percent=33.3,

            independent_attempt_rate=100.0,

            independent_success_rate=33.3,

            average_hint_level=0.0,

            direct_answer_requests=0,

            measured_response_count=3,

            average_response_latency_ms=5000.0,
        )
    )


    decision = (
        EnglishAdaptiveEngine
        .decide(
            signals
        )
    )


    assert (
        decision.difficulty
        == DifficultyLevel.EASY
    )


    assert (
        decision.next_activity
        == (
            EnglishAdaptiveActivity
            .REVIEW_CONCEPT
        )
    )