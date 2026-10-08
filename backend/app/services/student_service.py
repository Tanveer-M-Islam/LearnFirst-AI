from sqlalchemy.orm import Session

from app.database.models.student import StudentProfile
from app.database.repositories.student_repository import (
    StudentRepository,
)
from app.schemas.enums import AgeGroup
from app.schemas.student import StudentCreate


def determine_age_group(
    age: int,
) -> AgeGroup:

    if 7 <= age <= 9:
        return AgeGroup.FOUNDATION

    if 10 <= age <= 12:
        return AgeGroup.DEVELOPING

    if 13 <= age <= 14:
        return AgeGroup.INDEPENDENT

    raise ValueError(
        "LearnFirst AI currently supports ages 7–14."
    )


class StudentService:

    @staticmethod
    def create_student(
        db: Session,
        data: StudentCreate,
    ) -> StudentProfile:

        age_group = determine_age_group(
            data.age
        )

        student = StudentProfile(
            parent_id=data.parent_id,
            display_name=data.display_name,
            age=data.age,
            grade=data.grade,
            age_group=age_group.value,
            preferred_language=(
                data.preferred_language
            ),
            curriculum_profile=(
                data.curriculum_profile
            ),
        )

        return StudentRepository.create(
            db=db,
            student=student,
        )

    @staticmethod
    def get_student(
        db: Session,
        student_id: str,
    ) -> StudentProfile | None:

        return StudentRepository.get_by_id(
            db=db,
            student_id=student_id,
        )