from sqlalchemy.orm import Session

from app.adaptive.engine import (
    AdaptiveLearningEngine,
    AdaptiveSignals,
)
from app.adaptive.problem_bank import (
    get_adaptive_problem,
)
from app.database.repositories.student_repository import (
    StudentRepository,
)
from app.schemas.adaptive import (
    AdaptiveActivity,
    AdaptivePlanResponse,
    AdaptiveProblemView,
)
from app.schemas.enums import (
    AgeGroup,
)
from app.services.assessment_service import (
    AssessmentService,
)


class AdaptiveLearningService:

    @classmethod
    def get_plan(
        cls,
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> AdaptivePlanResponse:

        student = (
            StudentRepository
            .get_by_id(
                db=db,
                student_id=(
                    student_id
                ),
            )
        )

        if student is None:

            raise LookupError(
                "Student not found."
            )


        progress = (
            AssessmentService
            .get_concept_progress(
                db=db,

                student_id=(
                    student_id
                ),

                concept_code=(
                    concept_code
                ),
            )
        )


        diagnostic_score = (
            progress
            .diagnostic
            .score_percent

            if progress.diagnostic
            is not None

            else None
        )


        mastery_score = (
            progress
            .mastery
            .score_percent

            if progress.mastery
            is not None

            else None
        )


        metrics = (
            progress
            .learning_metrics
        )


        signals = AdaptiveSignals(
            age_group=(
                AgeGroup(
                    student.age_group
                )
            ),

            mastery_state=(
                progress
                .current_mastery_state
            ),

            recommended_difficulty=(
                progress
                .recommended_difficulty
            ),

            diagnostic_score=(
                diagnostic_score
            ),

            mastery_score=(
                mastery_score
            ),

            total_attempts=(
                metrics
                .total_attempts
            ),

            independent_attempts=(
                metrics
                .independent_attempts
            ),

            independent_attempt_rate=(
                metrics
                .independent_attempt_rate
            ),

            independent_success_rate=(
                metrics
                .independent_success_rate
            ),

            average_hint_level=(
                metrics
                .average_hint_level
            ),

            direct_answer_requests=(
                metrics
                .direct_answer_requests
            ),

            retry_success_count=(
                metrics
                .retry_success_count
            ),
        )


        decision = (
            AdaptiveLearningEngine
            .decide(
                signals
            )
        )


        latest_score = (
            mastery_score
            if mastery_score
            is not None
            else diagnostic_score
        )


        next_problem = None


        if (
            decision.next_activity
            in {
                AdaptiveActivity
                .GUIDED_PRACTICE,

                AdaptiveActivity
                .INDEPENDENT_PRACTICE,

                AdaptiveActivity
                .REVIEW_FOUNDATION,

                AdaptiveActivity
                .CHALLENGE_PRACTICE,
            }
        ):

            problem = (
                get_adaptive_problem(
                    concept_code=(
                        concept_code
                    ),

                    difficulty=(
                        decision
                        .difficulty
                    ),

                    offset=(
                        metrics
                        .total_attempts
                    ),
                )
            )

            if (
                problem
                is not None
            ):

                next_problem = (
                    AdaptiveProblemView(
                        problem_id=(
                            problem
                            .problem_id
                        ),

                        prompt=(
                            problem
                            .prompt
                        ),

                        difficulty=(
                            problem
                            .difficulty
                        ),
                    )
                )


        return AdaptivePlanResponse(
            student_id=(
                student_id
            ),

            concept_code=(
                concept_code
            ),

            age_group=(
                AgeGroup(
                    student.age_group
                )
            ),

            mastery_state=(
                progress
                .current_mastery_state
            ),

            difficulty=(
                decision
                .difficulty
            ),

            support_level=(
                decision
                .support_level
            ),

            explanation_depth=(
                decision
                .explanation_depth
            ),

            next_activity=(
                decision
                .next_activity
            ),

            latest_score_percent=(
                latest_score
            ),

            independent_attempt_rate=(
                metrics
                .independent_attempt_rate
            ),

            independent_success_rate=(
                metrics
                .independent_success_rate
            ),

            average_hint_level=(
                metrics
                .average_hint_level
            ),

            direct_answer_requests=(
                metrics
                .direct_answer_requests
            ),

            retry_success_count=(
                metrics
                .retry_success_count
            ),

            reason_codes=list(
                decision
                .reason_codes
            ),

            summary=(
                decision.summary
            ),

            next_problem=(
                next_problem
            ),
        )