from sqlalchemy.orm import Session

from app.database.models.tutor_decision import (
    TutorDecision,
)


class TutorDecisionRepository:

    @staticmethod
    def create(
        db: Session,
        decision: TutorDecision,
    ) -> TutorDecision:

        db.add(decision)

        db.commit()

        db.refresh(decision)

        return decision