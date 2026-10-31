from sqlalchemy.orm import Session

from app.database.models.mastery import (
    MasteryRecord,
)


class MasteryRepository:

    @staticmethod
    def get_by_student_concept(
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> MasteryRecord | None:

        return (
            db.query(MasteryRecord)
            .filter(
                MasteryRecord.student_id
                == student_id,
                MasteryRecord.concept_code
                == concept_code,
            )
            .first()
        )

    @staticmethod
    def save(
        db: Session,
        record: MasteryRecord,
    ) -> MasteryRecord:

        db.add(record)

        db.commit()

        db.refresh(record)

        return record