from collections import defaultdict
from datetime import (
    datetime,
    timezone,
)

from sqlalchemy.orm import Session

from app.assessment.question_bank import (
    AssessmentQuestion,
    get_assessment_questions,
)
from app.database.models.assessment import (
    AssessmentAnswer,
    AssessmentRun,
)
from app.database.models.mastery import (
    MasteryRecord,
)
from app.database.repositories.assessment_repository import (
    AssessmentRepository,
)
from app.database.repositories.mastery_repository import (
    MasteryRepository,
)
from app.database.repositories.session_repository import (
    LearningSessionRepository,
)
from app.database.repositories.student_attempt_repository import (
    StudentAttemptRepository,
)
from app.database.repositories.student_repository import (
    StudentRepository,
)
from app.math.validator import (
    MathValidator,
)
from app.schemas.assessment import (
    AssessmentAnswerResult,
    AssessmentQuestionView,
    AssessmentResult,
    AssessmentScoreSnapshot,
    AssessmentStartRequest,
    AssessmentStartResponse,
    ConceptProgressResponse,
    LearningIndependenceMetrics,
)
from app.schemas.enums import (
    AssessmentStatus,
    AssessmentType,
    AttemptStatus,
    DifficultyLevel,
    MasteryState,
    Subject,
)


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    )


class AssessmentService:

    @classmethod
    def start_assessment(
        cls,
        db: Session,
        data: AssessmentStartRequest,
    ) -> AssessmentStartResponse:

        student = (
            StudentRepository.get_by_id(
                db=db,
                student_id=data.student_id,
            )
        )

        if student is None:
            raise LookupError(
                "Student not found."
            )

        if data.subject != Subject.MATH:
            raise ValueError(
                "Phase 6 assessments currently "
                "support Math only."
            )

        questions = (
            get_assessment_questions(
                concept_code=(
                    data.concept_code
                ),
                assessment_type=(
                    data.assessment_type
                ),
            )
        )

        if not questions:
            raise ValueError(
                "No assessment question bank "
                "exists for this concept."
            )

        if data.session_id is not None:

            session = (
                LearningSessionRepository
                .get_by_id(
                    db=db,
                    session_id=(
                        data.session_id
                    ),
                )
            )

            if session is None:
                raise LookupError(
                    "Learning session "
                    "not found."
                )

            if (
                session.student_id
                != data.student_id
            ):
                raise ValueError(
                    "The learning session "
                    "does not belong to this "
                    "student."
                )

            if (
                session.concept_code
                and session.concept_code
                != data.concept_code
            ):
                raise ValueError(
                    "Assessment concept does "
                    "not match the learning "
                    "session concept."
                )

        run = AssessmentRun(
            student_id=data.student_id,
            session_id=data.session_id,
            subject=data.subject.value,
            concept_code=(
                data.concept_code
            ),
            assessment_type=(
                data.assessment_type.value
            ),
            status=(
                AssessmentStatus
                .IN_PROGRESS
                .value
            ),
            total_questions=(
                len(questions)
            ),
            correct_answers=0,
        )

        run = (
            AssessmentRepository
            .create_run(
                db=db,
                run=run,
            )
        )

        return AssessmentStartResponse(
            assessment_id=run.id,
            student_id=run.student_id,
            session_id=run.session_id,
            subject=Subject(
                run.subject
            ),
            concept_code=(
                run.concept_code
            ),
            assessment_type=(
                AssessmentType(
                    run.assessment_type
                )
            ),
            status=AssessmentStatus(
                run.status
            ),
            total_questions=(
                run.total_questions
            ),
            questions=[
                AssessmentQuestionView(
                    question_id=(
                        question.question_id
                    ),
                    prompt=(
                        question.prompt
                    ),
                    difficulty=(
                        question.difficulty
                    ),
                    bloom_level=(
                        question.bloom_level
                    ),
                )
                for question in questions
            ],
        )

    @classmethod
    def submit_assessment(
        cls,
        db: Session,
        assessment_id: str,
        answers,
    ) -> AssessmentResult:

        run = (
            AssessmentRepository.get_run(
                db=db,
                assessment_id=(
                    assessment_id
                ),
            )
        )

        if run is None:
            raise LookupError(
                "Assessment not found."
            )

        if (
            run.status
            == AssessmentStatus
            .COMPLETED.value
        ):
            raise ValueError(
                "This assessment has "
                "already been completed."
            )

        assessment_type = (
            AssessmentType(
                run.assessment_type
            )
        )

        questions = (
            get_assessment_questions(
                concept_code=(
                    run.concept_code
                ),
                assessment_type=(
                    assessment_type
                ),
            )
        )

        question_map: dict[
            str,
            AssessmentQuestion,
        ] = {
            question.question_id: (
                question
            )
            for question in questions
        }

        submitted_ids = [
            answer.question_id
            for answer in answers
        ]

        if (
            len(submitted_ids)
            != len(set(submitted_ids))
        ):
            raise ValueError(
                "Duplicate question IDs "
                "were submitted."
            )

        expected_ids = set(
            question_map.keys()
        )

        if (
            set(submitted_ids)
            != expected_ids
        ):
            raise ValueError(
                "All assessment questions "
                "must be answered exactly once."
            )

        results: list[
            AssessmentAnswerResult
        ] = []

        correct_answers = 0

        for submitted in answers:

            question = question_map[
                submitted.question_id
            ]

            validation = (
                MathValidator.validate(
                    problem=(
                        question.prompt
                    ),
                    student_message=(
                        submitted.response
                    ),
                )
            )

            if validation.is_correct:
                correct_answers += 1

            answer_record = (
                AssessmentAnswer(
                    assessment_id=run.id,
                    question_id=(
                        question.question_id
                    ),
                    problem_text=(
                        question.prompt
                    ),
                    response_text=(
                        submitted.response
                    ),
                    status=(
                        validation.status.value
                    ),
                    is_correct=(
                        validation.is_correct
                    ),
                    expected_answer=(
                        validation
                        .expected_answer
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
            )

            (
                AssessmentRepository
                .create_answer(
                    db=db,
                    answer=(
                        answer_record
                    ),
                )
            )

            results.append(
                AssessmentAnswerResult(
                    question_id=(
                        question.question_id
                    ),
                    status=(
                        validation
                        .status.value
                    ),
                    is_correct=(
                        validation
                        .is_correct
                    ),
                    misconception_code=(
                        validation
                        .misconception_code
                    ),
                )
            )

        score_percent = round(
            (
                correct_answers
                / run.total_questions
            )
            * 100,
            2,
        )

        mastery_state = (
            cls._mastery_state(
                score_percent
            )
        )

        difficulty = (
            cls._recommended_difficulty(
                score_percent
            )
        )

        run.correct_answers = (
            correct_answers
        )

        run.score_percent = (
            score_percent
        )

        run.difficulty_recommendation = (
            difficulty.value
        )

        run.status = (
            AssessmentStatus
            .COMPLETED
            .value
        )

        run.completed_at = utc_now()

        (
            AssessmentRepository.save_run(
                db=db,
                run=run,
            )
        )

        baseline_score = None
        score_gain = None
        improved = None

        if (
            assessment_type
            == AssessmentType.MASTERY
        ):

            diagnostic = (
                AssessmentRepository
                .latest_completed(
                    db=db,
                    student_id=(
                        run.student_id
                    ),
                    concept_code=(
                        run.concept_code
                    ),
                    assessment_type=(
                        AssessmentType
                        .DIAGNOSTIC
                    ),
                )
            )

            if (
                diagnostic is not None
                and diagnostic
                .score_percent
                is not None
            ):

                baseline_score = round(
                    diagnostic
                    .score_percent,
                    2,
                )

                score_gain = round(
                    score_percent
                    - baseline_score,
                    2,
                )

                improved = (
                    score_gain > 0
                )

            cls._update_mastery(
                db=db,
                run=run,
                score_percent=(
                    score_percent
                ),
                mastery_state=(
                    mastery_state
                ),
            )

        return AssessmentResult(
            assessment_id=run.id,
            assessment_type=(
                assessment_type
            ),
            concept_code=(
                run.concept_code
            ),
            correct_answers=(
                correct_answers
            ),
            total_questions=(
                run.total_questions
            ),
            score_percent=(
                score_percent
            ),
            mastery_state=(
                mastery_state
            ),
            recommended_difficulty=(
                difficulty
            ),
            baseline_score_percent=(
                baseline_score
            ),
            score_gain_percentage_points=(
                score_gain
            ),
            improved=improved,
            answers=results,
        )

    @classmethod
    def get_concept_progress(
        cls,
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> ConceptProgressResponse:

        student = (
            StudentRepository.get_by_id(
                db=db,
                student_id=student_id,
            )
        )

        if student is None:
            raise LookupError(
                "Student not found."
            )

        diagnostic = (
            AssessmentRepository
            .latest_completed(
                db=db,
                student_id=student_id,
                concept_code=(
                    concept_code
                ),
                assessment_type=(
                    AssessmentType
                    .DIAGNOSTIC
                ),
            )
        )

        mastery = (
            AssessmentRepository
            .latest_completed(
                db=db,
                student_id=student_id,
                concept_code=(
                    concept_code
                ),
                assessment_type=(
                    AssessmentType
                    .MASTERY
                ),
            )
        )

        mastery_record = (
            MasteryRepository
            .get_by_student_concept(
                db=db,
                student_id=student_id,
                concept_code=(
                    concept_code
                ),
            )
        )

        gain = None

        if (
            diagnostic is not None
            and mastery is not None
            and diagnostic.score_percent
            is not None
            and mastery.score_percent
            is not None
        ):

            gain = round(
                mastery.score_percent
                - diagnostic
                .score_percent,
                2,
            )

        if mastery_record is not None:

            current_mastery = (
                MasteryState(
                    mastery_record
                    .mastery_state
                )
            )

        elif (
            mastery is not None
            and mastery.score_percent
            is not None
        ):

            current_mastery = (
                cls._mastery_state(
                    mastery.score_percent
                )
            )

        else:

            current_mastery = (
                MasteryState.NOT_STARTED
            )

        latest_score = None

        if (
            mastery is not None
            and mastery.score_percent
            is not None
        ):
            latest_score = (
                mastery.score_percent
            )

        elif (
            diagnostic is not None
            and diagnostic.score_percent
            is not None
        ):
            latest_score = (
                diagnostic
                .score_percent
            )

        recommended = (
            cls._recommended_difficulty(
                latest_score or 0.0
            )
        )

        metrics = (
            cls._learning_metrics(
                db=db,
                student_id=student_id,
                concept_code=(
                    concept_code
                ),
            )
        )

        return ConceptProgressResponse(
            student_id=student_id,
            concept_code=concept_code,
            diagnostic=(
                cls._snapshot(
                    diagnostic
                )
            ),
            mastery=(
                cls._snapshot(
                    mastery
                )
            ),
            score_gain_percentage_points=(
                gain
            ),
            current_mastery_state=(
                current_mastery
            ),
            recommended_difficulty=(
                recommended
            ),
            learning_metrics=metrics,
        )

    @staticmethod
    def _mastery_state(
        score_percent: float,
    ) -> MasteryState:

        if score_percent >= 80:
            return (
                MasteryState.STRONG
            )

        if score_percent >= 60:
            return (
                MasteryState
                .DEVELOPING
            )

        return MasteryState.LEARNING

    @staticmethod
    def _recommended_difficulty(
        score_percent: float,
    ) -> DifficultyLevel:

        if score_percent >= 80:
            return (
                DifficultyLevel
                .CHALLENGING
            )

        if score_percent >= 40:
            return (
                DifficultyLevel
                .MODERATE
            )

        return DifficultyLevel.EASY

    @classmethod
    def _update_mastery(
        cls,
        db: Session,
        run: AssessmentRun,
        score_percent: float,
        mastery_state: MasteryState,
    ) -> None:

        now = utc_now()

        record = (
            MasteryRepository
            .get_by_student_concept(
                db=db,
                student_id=(
                    run.student_id
                ),
                concept_code=(
                    run.concept_code
                ),
            )
        )

        if record is None:

            record = MasteryRecord(
                student_id=(
                    run.student_id
                ),
                subject=run.subject,
                concept_code=(
                    run.concept_code
                ),
                mastery_state=(
                    mastery_state.value
                ),
                mastery_score=(
                    score_percent
                ),
                independent_successes=0,
                assisted_successes=0,
                failed_attempts=0,
                follow_up_successes=0,
                explain_back_successes=0,
                last_practiced_at=now,
                updated_at=now,
            )

        else:

            record.mastery_state = (
                mastery_state.value
            )

            record.mastery_score = (
                score_percent
            )

            record.last_practiced_at = (
                now
            )

            record.updated_at = now

        MasteryRepository.save(
            db=db,
            record=record,
        )

        if run.session_id is not None:

            session = (
                LearningSessionRepository
                .get_by_id(
                    db=db,
                    session_id=(
                        run.session_id
                    ),
                )
            )

            if session is not None:

                session.mastery_state = (
                    mastery_state.value
                )

                (
                    LearningSessionRepository
                    .save(
                        db=db,
                        learning_session=(
                            session
                        ),
                    )
                )

    @staticmethod
    def _snapshot(
        run: AssessmentRun | None,
    ) -> (
        AssessmentScoreSnapshot
        | None
    ):

        if (
            run is None
            or run.score_percent
            is None
        ):
            return None

        return AssessmentScoreSnapshot(
            assessment_id=run.id,
            score_percent=round(
                run.score_percent,
                2,
            ),
            correct_answers=(
                run.correct_answers
            ),
            total_questions=(
                run.total_questions
            ),
        )

    @classmethod
    def _learning_metrics(
        cls,
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> LearningIndependenceMetrics:

        attempts = [
            attempt
            for attempt in (
                StudentAttemptRepository
                .list_by_student(
                    db=db,
                    student_id=(
                        student_id
                    ),
                )
            )
            if (
                attempt.problem_ref
                == concept_code
            )
        ]

        sessions = [
            session
            for session in (
                LearningSessionRepository
                .list_by_student(
                    db=db,
                    student_id=(
                        student_id
                    ),
                )
            )
            if (
                session.concept_code
                == concept_code
            )
        ]

        total_attempts = len(
            attempts
        )

        correct_attempts = sum(
            1
            for attempt in attempts
            if (
                attempt.status
                == AttemptStatus
                .CORRECT.value
            )
        )

        independent_attempts = sum(
            1
            for attempt in attempts
            if attempt.is_independent
        )

        independent_correct = sum(
            1
            for attempt in attempts
            if (
                attempt.is_independent
                and attempt.status
                == AttemptStatus
                .CORRECT.value
            )
        )

        if total_attempts:

            independent_attempt_rate = (
                independent_attempts
                / total_attempts
                * 100
            )

            average_hint_level = (
                sum(
                    attempt
                    .hint_level_before
                    for attempt
                    in attempts
                )
                / total_attempts
            )

        else:

            independent_attempt_rate = 0.0
            average_hint_level = 0.0

        if independent_attempts:

            independent_success_rate = (
                independent_correct
                / independent_attempts
                * 100
            )

        else:

            independent_success_rate = 0.0

        direct_answer_requests = sum(
            session
            .direct_answer_requests
            for session in sessions
        )

        retry_success_count = (
            cls._retry_success_count(
                attempts
            )
        )

        return LearningIndependenceMetrics(
            total_attempts=(
                total_attempts
            ),
            correct_attempts=(
                correct_attempts
            ),
            independent_attempts=(
                independent_attempts
            ),
            independent_correct_attempts=(
                independent_correct
            ),
            independent_attempt_rate=round(
                independent_attempt_rate,
                2,
            ),
            independent_success_rate=round(
                independent_success_rate,
                2,
            ),
            average_hint_level=round(
                average_hint_level,
                2,
            ),
            direct_answer_requests=(
                direct_answer_requests
            ),
            retry_success_count=(
                retry_success_count
            ),
        )

    @staticmethod
    def _retry_success_count(
        attempts,
    ) -> int:

        grouped = defaultdict(list)

        for attempt in attempts:

            grouped[
                attempt.session_id
            ].append(
                attempt
            )

        recovered_sessions = 0

        failure_statuses = {
            AttemptStatus
            .INCORRECT.value,
            AttemptStatus
            .PARTIALLY_CORRECT.value,
            AttemptStatus
            .INCOMPLETE.value,
        }

        for session_attempts in (
            grouped.values()
        ):

            ordered = sorted(
                session_attempts,
                key=lambda item: (
                    item.attempt_number
                ),
            )

            failure_seen = False

            recovered = False

            for attempt in ordered:

                if (
                    attempt.status
                    in failure_statuses
                ):
                    failure_seen = True

                elif (
                    failure_seen
                    and attempt.status
                    == AttemptStatus
                    .CORRECT.value
                ):
                    recovered = True
                    break

            if recovered:
                recovered_sessions += 1

        return recovered_sessions