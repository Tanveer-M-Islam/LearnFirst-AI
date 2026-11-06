from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.enums import (
    AssessmentStatus,
    AssessmentType,
    DifficultyLevel,
    MasteryState,
)


class ScienceAssessmentStartRequest(
    BaseModel
):
    student_id: str

    session_id: (
        str | None
    ) = None

    concept_code: str = Field(
        min_length=1,
        max_length=100,
    )

    assessment_type: (
        AssessmentType
    )


class ScienceAssessmentQuestionView(
    BaseModel
):
    question_id: str

    prompt: str

    difficulty: (
        DifficultyLevel
    )


class ScienceAssessmentStartResponse(
    BaseModel
):
    assessment_id: str

    student_id: str

    session_id: (
        str | None
    )

    concept_code: str

    assessment_type: (
        AssessmentType
    )

    status: (
        AssessmentStatus
    )

    total_questions: int

    questions: list[
        ScienceAssessmentQuestionView
    ]


class ScienceAssessmentAnswerInput(
    BaseModel
):
    question_id: str

    response: str = Field(
        min_length=1,
        max_length=2000,
    )


class ScienceAssessmentSubmitRequest(
    BaseModel
):
    answers: list[
        ScienceAssessmentAnswerInput
    ] = Field(
        min_length=1
    )


class ScienceAssessmentAnswerResult(
    BaseModel
):
    question_id: str

    status: str

    is_correct: bool

    coverage_score: float

    misconception_code: (
        str | None
    ) = None


class ScienceAssessmentResult(
    BaseModel
):
    assessment_id: str

    assessment_type: (
        AssessmentType
    )

    concept_code: str

    correct_answers: int

    partial_answers: int

    total_questions: int

    score_percent: float

    mastery_state: (
        MasteryState
    )

    recommended_difficulty: (
        DifficultyLevel
    )

    baseline_score_percent: (
        float | None
    ) = None

    score_gain_percentage_points: (
        float | None
    ) = None

    improved: (
        bool | None
    ) = None

    answers: list[
        ScienceAssessmentAnswerResult
    ]


class ScienceAssessmentSnapshot(
    BaseModel
):
    assessment_id: str

    score_percent: float

    correct_answers: int

    total_questions: int


class ScienceAssessmentProgress(
    BaseModel
):
    student_id: str

    concept_code: str

    diagnostic: (
        ScienceAssessmentSnapshot
        | None
    )

    mastery: (
        ScienceAssessmentSnapshot
        | None
    )

    score_gain_percentage_points: (
        float | None
    )

    assessment_mastery_state: (
        MasteryState
    )