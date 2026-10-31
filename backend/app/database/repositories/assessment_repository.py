from sqlalchemy.orm import Session

from app.database.models.assessment import (
    AssessmentAnswer,
    AssessmentRun,
)
from app.schemas.enums import (
    AssessmentStatus,
    AssessmentType,
)


class AssessmentRepository:

    @staticmethod
    def create_run(
        db: Session,
        run: AssessmentRun,
    ) -> AssessmentRun:

        db.add(run)

        db.commit()

        db.refresh(run)

        return run

    @staticmethod
    def get_run(
        db: Session,
        assessment_id: str,
    ) -> AssessmentRun | None:

        return (
            db.query(AssessmentRun)
            .filter(
                AssessmentRun.id
                == assessment_id
            )
            .first()
        )

    @staticmethod
    def save_run(
        db: Session,
        run: AssessmentRun,
    ) -> AssessmentRun:

        db.add(run)

        db.commit()

        db.refresh(run)

        return run

    @staticmethod
    def create_answer(
        db: Session,
        answer: AssessmentAnswer,
    ) -> AssessmentAnswer:

        db.add(answer)

        db.commit()

        db.refresh(answer)

        return answer

    @staticmethod
    def list_answers(
        db: Session,
        assessment_id: str,
    ) -> list[AssessmentAnswer]:

        return (
            db.query(AssessmentAnswer)
            .filter(
                AssessmentAnswer
                .assessment_id
                == assessment_id
            )
            .all()
        )

    @staticmethod
    def latest_completed(
        db: Session,
        student_id: str,
        concept_code: str,
        assessment_type: (
            AssessmentType
        ),
    ) -> AssessmentRun | None:

        return (
            db.query(AssessmentRun)
            .filter(
                AssessmentRun.student_id
                == student_id,
                AssessmentRun.concept_code
                == concept_code,
                AssessmentRun.assessment_type
                == assessment_type.value,
                AssessmentRun.status
                == (
                    AssessmentStatus
                    .COMPLETED
                    .value
                ),
            )
            .order_by(
                AssessmentRun
                .completed_at
                .desc()
            )
            .first()
        )