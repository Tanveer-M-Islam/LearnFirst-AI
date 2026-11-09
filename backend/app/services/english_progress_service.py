
from sqlalchemy.orm import Session

from app.database.models.assessment import AssessmentRun
from app.database.models.mastery import MasteryRecord
from app.database.repositories.assessment_repository import (
    AssessmentRepository,
)
from app.schemas.english_progress import (
    EnglishAssessmentSummary,
    EnglishProgressResponse,
)
from app.schemas.enums import (
    AssessmentType,
    MasteryState,
    Subject,
)
from app.services.english_adaptive_learning_service import (
    EnglishAdaptiveLearningService,
)


def assessment_snapshot(
    run: AssessmentRun | None,
) -> EnglishAssessmentSummary | None:

    if run is None or run.score_percent is None:
        return None

    return EnglishAssessmentSummary(
        score_percent=run.score_percent,
        total_questions=run.total_questions,
        correct_answers=run.correct_answers,
    )


class EnglishProgressService:

    @classmethod
    def get_progress(
        cls,
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> EnglishProgressResponse:

        plan = EnglishAdaptiveLearningService.get_plan(
            db=db,
            student_id=student_id,
            concept_code=concept_code,
        )

        diagnostic = AssessmentRepository.latest_completed(
            db=db,
            student_id=student_id,
            concept_code=concept_code,
            assessment_type=AssessmentType.DIAGNOSTIC,
        )

        mastery = AssessmentRepository.latest_completed(
            db=db,
            student_id=student_id,
            concept_code=concept_code,
            assessment_type=AssessmentType.MASTERY,
        )

        mastery_record = (
            db.query(MasteryRecord)
            .filter(
                MasteryRecord.student_id == student_id,
                MasteryRecord.concept_code == concept_code,
                MasteryRecord.subject == Subject.ENGLISH.value,
            )
            .first()
        )

        mastery_state = (
            MasteryState(mastery_record.mastery_state)
            if mastery_record is not None
            else plan.mastery_state
        )

        return EnglishProgressResponse(
            student_id=student_id,
            concept_code=concept_code,
            mastery_state=mastery_state,
            understanding_score_percent=(
                plan.understanding_score_percent
            ),
            total_attempts=plan.total_attempts,
            correct_attempts=plan.correct_attempts,
            partial_attempts=plan.partial_attempts,
            independent_attempts=plan.independent_attempts,
            diagnostic=assessment_snapshot(diagnostic),
            mastery=assessment_snapshot(mastery),
        )
