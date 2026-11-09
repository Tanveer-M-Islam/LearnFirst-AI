
from app.english.assessment_forms import (
    get_english_assessment_form,
)
from app.schemas.enums import AssessmentType


CONCEPTS = [
    "ENG_VOCAB_FOUND_01",
    "ENG_SENT_SIMPLE_01",
    "ENG_GRAMMAR_POS_01",
    "ENG_GRAMMAR_TENSE_01",
    "ENG_READ_CORE_01",
    "ENG_SENT_STRUCTURE_01",
    "ENG_GRAMMAR_ADV_01",
    "ENG_READ_INFERENCE_01",
]


def create_student(client):
    response = client.post(
        "/api/v1/students",
        json={
            "display_name": "English Learner",
            "age": 10,
            "grade": "5",
        },
    )

    assert response.status_code == 201, response.text
    return response.json()["id"]


def start_assessment(
    client,
    student_id,
    assessment_type,
    concept_code="ENG_GRAMMAR_TENSE_01",
):
    response = client.post(
        "/api/v1/english/assessments/start",
        json={
            "student_id": student_id,
            "subject": "ENGLISH",
            "concept_code": concept_code,
            "assessment_type": assessment_type,
        },
    )

    assert response.status_code == 201, response.text
    return response.json()


def submit_assessment(
    client,
    assessment_id,
    answers,
):
    return client.post(
        f"/api/v1/english/assessments/{assessment_id}/submit",
        json={"answers": answers},
    )


def diagnostic_answers():
    return [
        {
            "question_id": "TENSE-E-01",
            "response": "goes",
        },
        {
            "question_id": "TENSE-M-01",
            "response": "wrong",
        },
        {
            "question_id": "TENSE-C-01",
            "response": "wrong",
        },
    ]


def mastery_answers():
    return [
        {
            "question_id": "TENSE-MAST-01",
            "response": "walk",
        },
        {
            "question_id": "TENSE-MAST-02",
            "response": "wrote",
        },
        {
            "question_id": "TENSE-MAST-03",
            "response": "will visit",
        },
    ]


def test_all_concepts_have_distinct_forms():
    for concept in CONCEPTS:

        diagnostic = get_english_assessment_form(
            concept,
            AssessmentType.DIAGNOSTIC,
        )

        mastery = get_english_assessment_form(
            concept,
            AssessmentType.MASTERY,
        )

        assert len(diagnostic) == 3
        assert len(mastery) == 3

        diagnostic_ids = {
            question.question_id
            for question in diagnostic
        }

        mastery_ids = {
            question.question_id
            for question in mastery
        }

        assert diagnostic_ids.isdisjoint(mastery_ids)

        diagnostic_prompts = {
            question.prompt
            for question in diagnostic
        }

        mastery_prompts = {
            question.prompt
            for question in mastery
        }

        assert diagnostic_prompts.isdisjoint(
            mastery_prompts
        )


def test_diagnostic_does_not_expose_answers(client):
    student_id = create_student(client)

    assessment = start_assessment(
        client,
        student_id,
        "DIAGNOSTIC",
    )

    assert assessment["subject"] == "ENGLISH"
    assert assessment["total_questions"] == 3

    for question in assessment["questions"]:
        assert "expected_answer" not in question
        assert "accepted_answers" not in question


def test_diagnostic_then_mastery(client):
    student_id = create_student(client)

    diagnostic = start_assessment(
        client,
        student_id,
        "DIAGNOSTIC",
    )

    diagnostic_response = submit_assessment(
        client,
        diagnostic["assessment_id"],
        diagnostic_answers(),
    )

    assert diagnostic_response.status_code == 200

    diagnostic_result = diagnostic_response.json()

    assert diagnostic_result["correct_answers"] == 1
    assert diagnostic_result["score_percent"] == 33.33

    mastery = start_assessment(
        client,
        student_id,
        "MASTERY",
    )

    mastery_response = submit_assessment(
        client,
        mastery["assessment_id"],
        mastery_answers(),
    )

    assert mastery_response.status_code == 200, (
        mastery_response.text
    )

    result = mastery_response.json()

    assert result["correct_answers"] == 3
    assert result["score_percent"] == 100.0
    assert result["mastery_state"] == "STRONG"

    assert result["baseline_score_percent"] == 33.33
    assert result["score_gain_percentage_points"] == 66.67
    assert result["improved"] is True

    for answer in result["answers"]:
        assert "expected_answer" not in answer


def test_progress_contains_assessment_scores(client):
    student_id = create_student(client)

    diagnostic = start_assessment(
        client,
        student_id,
        "DIAGNOSTIC",
    )

    response = submit_assessment(
        client,
        diagnostic["assessment_id"],
        diagnostic_answers(),
    )

    assert response.status_code == 200

    progress = client.get(
        "/api/v1/english/progress/"
        f"students/{student_id}/concepts/"
        "ENG_GRAMMAR_TENSE_01"
    )

    assert progress.status_code == 200, progress.text

    result = progress.json()

    assert result["diagnostic"]["score_percent"] == 33.33
    assert result["mastery"] is None


def test_mastery_is_persisted_in_progress(client):
    student_id = create_student(client)

    mastery = start_assessment(
        client,
        student_id,
        "MASTERY",
    )

    response = submit_assessment(
        client,
        mastery["assessment_id"],
        mastery_answers(),
    )

    assert response.status_code == 200, response.text

    progress = client.get(
        "/api/v1/english/progress/"
        f"students/{student_id}/concepts/"
        "ENG_GRAMMAR_TENSE_01"
    )

    assert progress.status_code == 200, progress.text

    result = progress.json()

    assert result["mastery"]["score_percent"] == 100.0
    assert result["mastery_state"] == "STRONG"


def test_duplicate_submission_is_rejected(client):
    student_id = create_student(client)

    assessment = start_assessment(
        client,
        student_id,
        "MASTERY",
    )

    first = submit_assessment(
        client,
        assessment["assessment_id"],
        mastery_answers(),
    )

    second = submit_assessment(
        client,
        assessment["assessment_id"],
        mastery_answers(),
    )

    assert first.status_code == 200
    assert second.status_code == 400


def test_incomplete_answers_are_rejected(client):
    student_id = create_student(client)

    assessment = start_assessment(
        client,
        student_id,
        "DIAGNOSTIC",
    )

    response = submit_assessment(
        client,
        assessment["assessment_id"],
        [
            {
                "question_id": "TENSE-E-01",
                "response": "goes",
            }
        ],
    )

    assert response.status_code == 400


def test_math_cannot_use_english_endpoint(client):
    student_id = create_student(client)

    response = client.post(
        "/api/v1/english/assessments/start",
        json={
            "student_id": student_id,
            "subject": "MATH",
            "concept_code": "ENG_GRAMMAR_TENSE_01",
            "assessment_type": "DIAGNOSTIC",
        },
    )

    assert response.status_code == 400
