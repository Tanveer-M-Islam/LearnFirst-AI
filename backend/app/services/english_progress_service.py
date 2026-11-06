from sqlalchemy.orm import Session

from app.services.english_adaptive_learning_service import (
    EnglishAdaptiveLearningService,
)
from app.schemas.english_progress import (
    EnglishProgressResponse,
)


class EnglishProgressService:

    @classmethod
    def get_progress(
        cls,
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> EnglishProgressResponse:

        plan = (
            EnglishAdaptiveLearningService
            .get_plan(
                db=db,
                student_id=student_id,
                concept_code=concept_code,
            )
        )


        return (
            EnglishProgressResponse(
                student_id=(
                    student_id
                ),

                concept_code=(
                    concept_code
                ),

                mastery_state=(
                    plan.mastery_state
                ),

                understanding_score_percent=(
                    plan
                    .understanding_score_percent
                ),

                total_attempts=(
                    plan.total_attempts
                ),

                correct_attempts=(
                    plan.correct_attempts
                ),

                partial_attempts=(
                    plan.partial_attempts
                ),

                independent_attempts=(
                    plan.independent_attempts
                ),

                diagnostic=None,

                mastery=None,
            )
        )