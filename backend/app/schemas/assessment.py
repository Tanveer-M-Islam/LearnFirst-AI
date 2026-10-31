from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.enums import (
    AssessmentStatus,
    AssessmentType,
    DifficultyLevel,
    MasteryState,
    Subject,
)


class AssessmentStartRequest(
    BaseModel
):
    student_id: str

    session_id: str | None = None

    subject: Subject = Subject.MATH

    concept_code: str = Field(
        min_length=1,
        max_length=100,
    )

    assessment_type: AssessmentType


class AssessmentQuestionView(
    BaseModel
):
    question_id: str

    prompt: str

    difficulty: DifficultyLevel

    bloom_level: str


class AssessmentStartResponse(
    BaseModel
):
    assessment_id: str

    student_id: str

    session_id: str | None

    subject: Subject

    concept_code: str

    assessment_type: AssessmentType

    status: AssessmentStatus

    total_questions: int

    questions: list[
        AssessmentQuestionView
    ]


class AssessmentAnswerInput(
    BaseModel
):
    question_id: str

    response: str = Field(
        min_length=1,
        max_length=1000,
    )


class AssessmentSubmitRequest(
    BaseModel
):
    answers: list[
        AssessmentAnswerInput
    ] = Field(
        min_length=1
    )


class AssessmentAnswerResult(
    BaseModel
):
    question_id: str

    status: str

    is_correct: bool

    misconception_code: (
        str | None
    ) = None


class AssessmentResult(
    BaseModel
):
    assessment_id: str

    assessment_type: AssessmentType

    concept_code: str

    correct_answers: int

    total_questions: int

    score_percent: float

    mastery_state: MasteryState

    recommended_difficulty: (
        DifficultyLevel
    )

    baseline_score_percent: (
        float | None
    ) = None

    score_gain_percentage_points: (
        float | None
    ) = None

    improved: bool | None = None

    answers: list[
        AssessmentAnswerResult
    ]


class AssessmentScoreSnapshot(
    BaseModel
):
    assessment_id: str

    score_percent: float

    correct_answers: int

    total_questions: int


class LearningIndependenceMetrics(
    BaseModel
):
    total_attempts: int

    correct_attempts: int

    independent_attempts: int

    independent_correct_attempts: int

    independent_attempt_rate: float

    independent_success_rate: float

    average_hint_level: float

    direct_answer_requests: int

    retry_success_count: int


class ConceptProgressResponse(
    BaseModel
):
    student_id: str

    concept_code: str

    diagnostic: (
        AssessmentScoreSnapshot | None
    )

    mastery: (
        AssessmentScoreSnapshot | None
    )

    score_gain_percentage_points: (
        float | None
    )

    current_mastery_state: (
        MasteryState
    )

    recommended_difficulty: (
        DifficultyLevel
    )

    learning_metrics: (
        LearningIndependenceMetrics
    )