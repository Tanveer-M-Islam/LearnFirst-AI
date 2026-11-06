from datetime import (
    datetime,
    timezone,
)

from sqlalchemy.orm import (
    Session,
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
from app.database.repositories.student_repository import (
    StudentRepository,
)
from app.science.assessment_bank import (
    get_science_assessment_questions,
)
from app.science.evaluator import (
    ScienceUnderstandingEvaluator,
)
from app.schemas.enums import (
    AssessmentStatus,
    AssessmentType,
    AttemptStatus,
    DifficultyLevel,
    MasteryState,
    Subject,
)
from app.schemas.science_assessment import (
    ScienceAssessmentAnswerResult,
    ScienceAssessmentProgress,
    ScienceAssessmentQuestionView,
    ScienceAssessmentResult,
    ScienceAssessmentSnapshot,
    ScienceAssessmentStartRequest,
    ScienceAssessmentStartResponse,
)


def utc_now() -> datetime:

    return datetime.now(
        timezone.utc
    )


class ScienceAssessmentService:

    @classmethod
    def start(
        cls,
        db: Session,
        data: ScienceAssessmentStartRequest,
    ) -> ScienceAssessmentStartResponse:

        student = (
            StudentRepository
            .get_by_id(
                db=db,

                student_id=(
                    data.student_id
                ),
            )
        )


        if (
            student
            is None
        ):

            raise LookupError(
                "Student not found."
            )


        questions = (
            get_science_assessment_questions(
                concept_code=(
                    data.concept_code
                ),

                assessment_type=(
                    data.assessment_type
                ),
            )
        )


        if (
            not questions
        ):

            raise ValueError(
                "No Science assessment "
                "exists for this concept."
            )


        if (
            data.session_id
            is not None
        ):

            session = (
                LearningSessionRepository
                .get_by_id(
                    db=db,

                    session_id=(
                        data.session_id
                    ),
                )
            )


            if (
                session
                is None
            ):

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
                    "does not belong to "
                    "this student."
                )


            if (
                session.subject
                != Subject.SCIENCE.value
            ):

                raise ValueError(
                    "This is not a "
                    "Science session."
                )


            if (
                session.concept_code

                and session.concept_code
                != data.concept_code
            ):

                raise ValueError(
                    "Assessment concept "
                    "does not match the "
                    "Science session."
                )


        run = (
            AssessmentRun(
                student_id=(
                    data.student_id
                ),

                session_id=(
                    data.session_id
                ),

                subject=(
                    Subject.SCIENCE.value
                ),

                concept_code=(
                    data.concept_code
                ),

                assessment_type=(
                    data
                    .assessment_type
                    .value
                ),

                status=(
                    AssessmentStatus
                    .IN_PROGRESS
                    .value
                ),

                total_questions=(
                    len(
                        questions
                    )
                ),

                correct_answers=0,
            )
        )


        run = (
            AssessmentRepository
            .create_run(
                db=db,

                run=(
                    run
                ),
            )
        )


        return (
            ScienceAssessmentStartResponse(
                assessment_id=(
                    run.id
                ),

                student_id=(
                    run.student_id
                ),

                session_id=(
                    run.session_id
                ),

                concept_code=(
                    run.concept_code
                ),

                assessment_type=(
                    AssessmentType(
                        run.assessment_type
                    )
                ),

                status=(
                    AssessmentStatus(
                        run.status
                    )
                ),

                total_questions=(
                    run.total_questions
                ),

                questions=[

                    ScienceAssessmentQuestionView(
                        question_id=(
                            question
                            .question_id
                        ),

                        prompt=(
                            question.prompt
                        ),

                        difficulty=(
                            question
                            .difficulty
                        ),
                    )

                    for question
                    in questions
                ],
            )
        )


    @classmethod
    def submit(
        cls,
        db: Session,
        assessment_id: str,
        answers,
    ) -> ScienceAssessmentResult:

        run = (
            AssessmentRepository
            .get_run(
                db=db,

                assessment_id=(
                    assessment_id
                ),
            )
        )


        if (
            run
            is None
        ):

            raise LookupError(
                "Assessment not found."
            )


        if (
            run.subject
            != Subject.SCIENCE.value
        ):

            raise ValueError(
                "This is not a "
                "Science assessment."
            )


        if (
            run.status
            == (
                AssessmentStatus
                .COMPLETED
                .value
            )
        ):

            raise ValueError(
                "This assessment "
                "has already been "
                "completed."
            )


        assessment_type = (
            AssessmentType(
                run.assessment_type
            )
        )


        questions = (
            get_science_assessment_questions(
                concept_code=(
                    run.concept_code
                ),

                assessment_type=(
                    assessment_type
                ),
            )
        )


        question_map = {

            question.question_id:
                question

            for question
            in questions
        }


        submitted_ids = [
            answer.question_id

            for answer
            in answers
        ]


        if (
            len(
                submitted_ids
            )
            != len(
                set(
                    submitted_ids
                )
            )
        ):

            raise ValueError(
                "Duplicate question IDs "
                "were submitted."
            )


        if (
            set(
                submitted_ids
            )
            != set(
                question_map.keys()
            )
        ):

            raise ValueError(
                "All Science assessment "
                "questions must be "
                "answered exactly once."
            )


        correct_answers = 0

        partial_answers = 0

        weighted_score = 0.0

        answer_results: list[
            ScienceAssessmentAnswerResult
        ] = []


        for submitted in answers:

            question = (
                question_map[
                    submitted.question_id
                ]
            )


            validation = (
                ScienceUnderstandingEvaluator
                .evaluate_question(
                    concept_code=(
                        run.concept_code
                    ),

                    question=(
                        question
                    ),

                    student_message=(
                        submitted.response
                    ),
                )
            )


            is_correct = (
                validation.status
                == AttemptStatus.CORRECT
            )


            if is_correct:

                correct_answers += 1

                weighted_score += 1.0


            elif (
                validation.status
                == (
                    AttemptStatus
                    .PARTIALLY_CORRECT
                )
            ):

                partial_answers += 1

                weighted_score += 0.5


            stored_answer = (
                AssessmentAnswer(
                    assessment_id=(
                        run.id
                    ),

                    question_id=(
                        question
                        .question_id
                    ),

                    problem_text=(
                        question.prompt
                    ),

                    response_text=(
                        submitted.response
                    ),

                    status=(
                        validation
                        .status
                        .value
                    ),

                    is_correct=(
                        is_correct
                    ),

                    expected_answer=None,

                    misconception_code=(
                        validation
                        .misconception_code
                    ),

                    validator_result=(
                        validation
                        .model_dump(
                            mode="json"
                        )
                    ),
                )
            )


            AssessmentRepository\
                .create_answer(
                    db=db,

                    answer=(
                        stored_answer
                    ),
                )


            answer_results.append(
                ScienceAssessmentAnswerResult(
                    question_id=(
                        question
                        .question_id
                    ),

                    status=(
                        validation
                        .status
                        .value
                    ),

                    is_correct=(
                        is_correct
                    ),

                    coverage_score=(
                        validation
                        .coverage_score
                    ),

                    misconception_code=(
                        validation
                        .misconception_code
                    ),
                )
            )


        score_percent = (
            round(
                (
                    weighted_score
                    / len(
                        questions
                    )
                    * 100
                ),

                1,
            )
        )


        mastery_state = (
            cls._mastery_state(
                score_percent
            )
        )


        recommended_difficulty = (
            cls._difficulty(
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
            recommended_difficulty
            .value
        )


        run.status = (
            AssessmentStatus
            .COMPLETED
            .value
        )


        run.completed_at = (
            utc_now()
        )


        AssessmentRepository\
            .save_run(
                db=db,

                run=(
                    run
                ),
            )


        cls._update_mastery_record(
            db=db,

            student_id=(
                run.student_id
            ),

            concept_code=(
                run.concept_code
            ),

            mastery_state=(
                mastery_state
            ),

            score_percent=(
                score_percent
            ),
        )


        baseline = None


        if (
            assessment_type
            == AssessmentType.MASTERY
        ):

            baseline = (
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


        baseline_score = (
            baseline.score_percent

            if (
                baseline
                and baseline
                .score_percent
                is not None
            )

            else None
        )


        gain = None

        improved = None


        if (
            baseline_score
            is not None

            and assessment_type
            == AssessmentType.MASTERY
        ):

            gain = (
                round(
                    score_percent
                    - baseline_score,

                    1,
                )
            )


            improved = (
                gain > 0
            )


        return (
            ScienceAssessmentResult(
                assessment_id=(
                    run.id
                ),

                assessment_type=(
                    assessment_type
                ),

                concept_code=(
                    run.concept_code
                ),

                correct_answers=(
                    correct_answers
                ),

                partial_answers=(
                    partial_answers
                ),

                total_questions=(
                    len(
                        questions
                    )
                ),

                score_percent=(
                    score_percent
                ),

                mastery_state=(
                    mastery_state
                ),

                recommended_difficulty=(
                    recommended_difficulty
                ),

                baseline_score_percent=(
                    baseline_score
                ),

                score_gain_percentage_points=(
                    gain
                ),

                improved=(
                    improved
                ),

                answers=(
                    answer_results
                ),
            )
        )


    @classmethod
    def get_progress(
        cls,
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> ScienceAssessmentProgress:

        diagnostic = (
            AssessmentRepository
            .latest_completed(
                db=db,

                student_id=(
                    student_id
                ),

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

                student_id=(
                    student_id
                ),

                concept_code=(
                    concept_code
                ),

                assessment_type=(
                    AssessmentType
                    .MASTERY
                ),
            )
        )


        diagnostic_snapshot = (
            cls._snapshot(
                diagnostic
            )
        )


        mastery_snapshot = (
            cls._snapshot(
                mastery
            )
        )


        gain = None


        if (
            diagnostic
            and mastery

            and diagnostic
            .score_percent
            is not None

            and mastery
            .score_percent
            is not None
        ):

            gain = (
                round(
                    mastery.score_percent
                    - diagnostic.score_percent,

                    1,
                )
            )


        score_for_state = None


        if (
            mastery
            and mastery
            .score_percent
            is not None
        ):

            score_for_state = (
                mastery.score_percent
            )


        elif (
            diagnostic
            and diagnostic
            .score_percent
            is not None
        ):

            score_for_state = (
                diagnostic
                .score_percent
            )


        mastery_state = (
            cls._mastery_state(
                score_for_state
            )

            if score_for_state
            is not None

            else (
                MasteryState
                .NOT_STARTED
            )
        )


        return (
            ScienceAssessmentProgress(
                student_id=(
                    student_id
                ),

                concept_code=(
                    concept_code
                ),

                diagnostic=(
                    diagnostic_snapshot
                ),

                mastery=(
                    mastery_snapshot
                ),

                score_gain_percentage_points=(
                    gain
                ),

                assessment_mastery_state=(
                    mastery_state
                ),
            )
        )


    @staticmethod
    def _snapshot(
        run: AssessmentRun | None,
    ) -> ScienceAssessmentSnapshot | None:

        if (
            run is None

            or run.score_percent
            is None
        ):

            return None


        return (
            ScienceAssessmentSnapshot(
                assessment_id=(
                    run.id
                ),

                score_percent=(
                    run.score_percent
                ),

                correct_answers=(
                    run.correct_answers
                ),

                total_questions=(
                    run.total_questions
                ),
            )
        )


    @staticmethod
    def _mastery_state(
        score_percent: float,
    ) -> MasteryState:

        if (
            score_percent
            >= 80.0
        ):

            return (
                MasteryState.STRONG
            )


        if (
            score_percent
            >= 60.0
        ):

            return (
                MasteryState.DEVELOPING
            )


        return (
            MasteryState.LEARNING
        )


    @staticmethod
    def _difficulty(
        score_percent: float,
    ) -> DifficultyLevel:

        if (
            score_percent
            >= 80.0
        ):

            return (
                DifficultyLevel
                .CHALLENGING
            )


        if (
            score_percent
            >= 50.0
        ):

            return (
                DifficultyLevel.MODERATE
            )


        return (
            DifficultyLevel.EASY
        )


    @staticmethod
    def _update_mastery_record(
        db: Session,
        student_id: str,
        concept_code: str,
        mastery_state: MasteryState,
        score_percent: float,
    ) -> None:

        record = (
            MasteryRepository
            .get_by_student_concept(
                db=db,

                student_id=(
                    student_id
                ),

                concept_code=(
                    concept_code
                ),
            )
        )


        if (
            record is None
        ):

            record = (
                MasteryRecord(
                    student_id=(
                        student_id
                    ),

                    subject=(
                        Subject.SCIENCE
                        .value
                    ),

                    concept_code=(
                        concept_code
                    ),
                )
            )


        record.mastery_state = (
            mastery_state.value
        )


        record.mastery_score = (
            score_percent
        )


        record.last_practiced_at = (
            utc_now()
        )


        MasteryRepository.save(
            db=db,

            record=(
                record
            ),
        )