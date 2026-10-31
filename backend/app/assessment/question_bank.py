from dataclasses import dataclass

from app.schemas.enums import (
    AssessmentType,
    DifficultyLevel,
)


@dataclass(frozen=True)
class AssessmentQuestion:
    question_id: str
    prompt: str
    difficulty: DifficultyLevel
    bloom_level: str


QUESTION_BANK: dict[
    tuple[str, AssessmentType],
    tuple[AssessmentQuestion, ...],
] = {

    (
        "MATH_ALG_LINEAR_01",
        AssessmentType.DIAGNOSTIC,
    ): (
        AssessmentQuestion(
            question_id="ALG-D-01",
            prompt="x + 3 = 7",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),
        AssessmentQuestion(
            question_id="ALG-D-02",
            prompt="2x = 10",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),
        AssessmentQuestion(
            question_id="ALG-D-03",
            prompt="2x + 3 = 11",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),
        AssessmentQuestion(
            question_id="ALG-D-04",
            prompt="4x - 5 = 19",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),
        AssessmentQuestion(
            question_id="ALG-D-05",
            prompt="3(x + 2) = 18",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
        ),
    ),

    (
        "MATH_ALG_LINEAR_01",
        AssessmentType.MASTERY,
    ): (
        AssessmentQuestion(
            question_id="ALG-M-01",
            prompt="x + 4 = 10",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),
        AssessmentQuestion(
            question_id="ALG-M-02",
            prompt="5x = 20",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),
        AssessmentQuestion(
            question_id="ALG-M-03",
            prompt="3x + 2 = 17",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),
        AssessmentQuestion(
            question_id="ALG-M-04",
            prompt="6x - 7 = 23",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),
        AssessmentQuestion(
            question_id="ALG-M-05",
            prompt="2(x + 3) = 14",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
        ),
    ),
}


def get_assessment_questions(
    concept_code: str,
    assessment_type: AssessmentType,
) -> tuple[AssessmentQuestion, ...]:

    return QUESTION_BANK.get(
        (
            concept_code,
            assessment_type,
        ),
        (),
    )