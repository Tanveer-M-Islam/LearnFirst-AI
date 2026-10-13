from sqlalchemy.orm import Session

from app.database.models.attempt import (
    StudentAttempt,
)
from app.database.models.learning_session import (
    LearningSession,
)
from app.database.repositories.student_attempt_repository import (
    StudentAttemptRepository,
)
from app.math.models import (
    MathValidationResult,
)
from app.math.validator import (
    MathValidator,
)
from app.schemas.enums import (
    AttemptStatus,
)


class MathAttemptService:

    @staticmethod
    def analyze(
        problem: str,
        student_message: str,
    ) -> MathValidationResult:

        return MathValidator.validate(
            problem=problem,
            student_message=student_message,
        )

    @staticmethod
    def record(
        db: Session,
        learning_session: LearningSession,
        student_message: str,
        validation: MathValidationResult,
        hint_level_before: int,
    ) -> StudentAttempt:

        # TutorService increments attempt_count
        # before this method is called.
        attempt_number = (
            learning_session.attempt_count
        )

        # MVP definition only.
        # This is an engineering metric,
        # not a validated psychological measure.
        is_independent = (
            hint_level_before <= 1
        )

        if (
            validation.misconception_code
            is not None
        ):

            learning_session.current_misconception = (
                validation
                .misconception_code
            )

        elif (
            validation.status
            == AttemptStatus.CORRECT
        ):

            learning_session.current_misconception = (
                None
            )

        attempt = StudentAttempt(
            session_id=(
                learning_session.id
            ),

            student_id=(
                learning_session.student_id
            ),

            problem_ref=(
                learning_session.concept_code
            ),

            response_text=(
                student_message
            ),

            attempt_number=(
                attempt_number
            ),

            status=(
                validation.status.value
            ),

            is_independent=(
                is_independent
            ),

            hint_level_before=(
                hint_level_before
            ),

            misconception_code=(
                validation
                .misconception_code
            ),

            validator_result=(
                validation.model_dump(
                    mode="json"
                )
            ),
        )

        return (
            StudentAttemptRepository
            .create(
                db=db,
                attempt=attempt,
            )
        )