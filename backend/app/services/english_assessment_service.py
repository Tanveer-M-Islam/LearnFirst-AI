
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models.assessment import (
    AssessmentAnswer,
    AssessmentRun,
)
from app.database.models.learning_session import LearningSession
from app.database.models.mastery import MasteryRecord
from app.database.models.student import StudentProfile

from app.database.repositories.assessment_repository import (
    AssessmentRepository,
)
from app.english.assessment_forms import (
    get_english_assessment_form,
)
from app.english.evaluator import EnglishEvaluator
from app.english.models import EnglishEvaluationMode

from app.schemas.assessment import (
    AssessmentAnswerInput,
    AssessmentAnswerResult,
    AssessmentQuestionView,
    AssessmentResult,
    AssessmentStartRequest,
    AssessmentStartResponse,
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
    return datetime.now(timezone.utc)


def mastery_from_score(score: float) -> MasteryState:
    if score >= 80:
        return MasteryState.STRONG
    if score >= 60:
        return MasteryState.DEVELOPING
    return MasteryState.LEARNING


def difficulty_from_score(
    score: float,
) -> DifficultyLevel:
    if score >= 80:
        return DifficultyLevel.CHALLENGING
    if score >= 40:
        return DifficultyLevel.MODERATE
    return DifficultyLevel.EASY


def evaluate_english_question(
    concept_code: str,
    question,
    response: str,
):
    """
    Use existing deterministic English evaluator
    on an assessment question.

    The normal evaluate() method looks up tutoring
    questions in the main bank. Assessment mastery
    questions are separate, so we reuse its
    underlying evaluation rules directly.
    """

    if question.evaluation_mode == EnglishEvaluationMode.EXACT:
        return EnglishEvaluator._evaluate_exact(
            concept_code=concept_code,
            question=question,
            student_message=response,
        )

    if question.evaluation_mode == EnglishEvaluationMode.KEY_IDEAS:
        return EnglishEvaluator._evaluate_key_ideas(
            concept_code=concept_code,
            question=question,
            student_message=response,
        )

    if question.evaluation_mode == EnglishEvaluationMode.SENTENCE_RULES:
        return EnglishEvaluator._evaluate_sentence(
            concept_code=concept_code,
            question=question,
            student_message=response,
        )

    raise ValueError("Unsupported English question type.")


class EnglishAssessmentService:

    @staticmethod
    def start(
        db: Session,
        data: AssessmentStartRequest,
    ) -> AssessmentStartResponse:

        if data.subject != Subject.ENGLISH:
            raise ValueError(
                "This endpoint only supports English."
            )

        student = db.get(
            StudentProfile,
            data.student_id,
        )

        if student is None:
            raise LookupError("Student not found.")

        questions = get_english_assessment_form(
            concept_code=data.concept_code,
            assessment_type=data.assessment_type,
        )

        if not questions:
            raise ValueError(
                "No English assessment form exists "
                "for this concept."
            )

        if data.session_id is not None:
            session = db.get(
                LearningSession,
                data.session_id,
            )

            if session is None:
                raise LookupError(
                    "Learning session not found."
                )

            if session.student_id != data.student_id:
                raise ValueError(
                    "The session belongs to another student."
                )

            if session.subject != Subject.ENGLISH.value:
                raise ValueError(
                    "An English assessment requires "
                    "an English learning session."
                )

            if (
                session.concept_code is not None
                and session.concept_code != data.concept_code
            ):
                raise ValueError(
                    "The assessment and session concepts "
                    "must match."
                )

        run = AssessmentRun(
            student_id=data.student_id,
            session_id=data.session_id,
            subject=Subject.ENGLISH.value,
            concept_code=data.concept_code,
            assessment_type=data.assessment_type.value,
            status=AssessmentStatus.IN_PROGRESS.value,
            total_questions=len(questions),
            correct_answers=0,
        )

        db.add(run)
        db.commit()
        db.refresh(run)

        return AssessmentStartResponse(
            assessment_id=run.id,
            student_id=run.student_id,
            session_id=run.session_id,
            subject=Subject.ENGLISH,
            concept_code=run.concept_code,
            assessment_type=data.assessment_type,
            status=AssessmentStatus.IN_PROGRESS,
            total_questions=len(questions),
            questions=[
                AssessmentQuestionView(
                    question_id=question.question_id,
                    prompt=question.prompt,
                    difficulty=question.difficulty,
                    bloom_level=(
                        "Understand"
                        if question.evaluation_mode
                        == EnglishEvaluationMode.KEY_IDEAS
                        else "Apply"
                    ),
                )
                for question in questions
            ],
        )

    @staticmethod
    def submit(
        db: Session,
        assessment_id: str,
        answers: list[AssessmentAnswerInput],
    ) -> AssessmentResult:

        run = db.get(
            AssessmentRun,
            assessment_id,
        )

        if (
            run is None
            or run.subject != Subject.ENGLISH.value
        ):
            raise LookupError(
                "English assessment not found."
            )

        if run.status != AssessmentStatus.IN_PROGRESS.value:
            raise ValueError(
                "This assessment was already submitted."
            )

        kind = AssessmentType(run.assessment_type)

        questions = get_english_assessment_form(
            concept_code=run.concept_code,
            assessment_type=kind,
        )

        question_map = {
            question.question_id: question
            for question in questions
        }

        submitted_ids = [
            answer.question_id
            for answer in answers
        ]

        if (
            len(submitted_ids) != len(question_map)
            or set(submitted_ids) != set(question_map)
        ):
            raise ValueError(
                "Answer every assessment question "
                "exactly once."
            )

        correct_answers = 0
        results = []

        for submitted in answers:
            question = question_map[
                submitted.question_id
            ]

            validation = evaluate_english_question(
                concept_code=run.concept_code,
                question=question,
                response=submitted.response,
            )

            if not validation.supported:
                raise ValueError(
                    "Question evaluation is unsupported."
                )

            is_correct = (
                validation.status == AttemptStatus.CORRECT
            )

            if is_correct:
                correct_answers += 1

            db.add(
                AssessmentAnswer(
                    assessment_id=run.id,
                    question_id=question.question_id,
                    problem_text=question.prompt,
                    response_text=submitted.response,
                    status=validation.status.value,
                    is_correct=is_correct,
                    expected_answer=None,
                    misconception_code=None,
                    validator_result=validation.model_dump(
                        mode="json"
                    ),
                )
            )

            results.append(
                AssessmentAnswerResult(
                    question_id=question.question_id,
                    status=validation.status.value,
                    is_correct=is_correct,
                    misconception_code=None,
                )
            )

        score_percent = round(
            correct_answers / run.total_questions * 100,
            2,
        )

        mastery_state = mastery_from_score(
            score_percent
        )

        difficulty = difficulty_from_score(
            score_percent
        )

        baseline_score = None
        score_gain = None
        improved = None

        # Update mastery only after a Mastery check.
        if kind == AssessmentType.MASTERY:

            diagnostic = (
                AssessmentRepository.latest_completed(
                    db=db,
                    student_id=run.student_id,
                    concept_code=run.concept_code,
                    assessment_type=AssessmentType.DIAGNOSTIC,
                )
            )

            if (
                diagnostic is not None
                and diagnostic.score_percent is not None
            ):
                baseline_score = round(
                    diagnostic.score_percent,
                    2,
                )

                score_gain = round(
                    score_percent - baseline_score,
                    2,
                )

                improved = score_gain > 0

            mastery_record = (
                db.query(MasteryRecord)
                .filter(
                    MasteryRecord.student_id == run.student_id,
                    MasteryRecord.concept_code == run.concept_code,
                )
                .first()
            )

            if mastery_record is None:
                mastery_record = MasteryRecord(
                    student_id=run.student_id,
                    subject=Subject.ENGLISH.value,
                    concept_code=run.concept_code,
                )

            mastery_record.mastery_state = (
                mastery_state.value
            )

            mastery_record.mastery_score = score_percent
            mastery_record.last_practiced_at = utc_now()

            db.add(mastery_record)

            if run.session_id is not None:
                session = db.get(
                    LearningSession,
                    run.session_id,
                )

                if session is not None:
                    session.mastery_state = (
                        mastery_state.value
                    )
                    db.add(session)

        run.correct_answers = correct_answers
        run.score_percent = score_percent
        run.difficulty_recommendation = difficulty.value
        run.status = AssessmentStatus.COMPLETED.value
        run.completed_at = utc_now()

        db.add(run)

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        return AssessmentResult(
            assessment_id=run.id,
            assessment_type=kind,
            concept_code=run.concept_code,
            correct_answers=correct_answers,
            total_questions=run.total_questions,
            score_percent=score_percent,
            mastery_state=mastery_state,
            recommended_difficulty=difficulty,
            baseline_score_percent=baseline_score,
            score_gain_percentage_points=score_gain,
            improved=improved,
            answers=results,
        )
