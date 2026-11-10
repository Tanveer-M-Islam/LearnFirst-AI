
import pytest

from app.services.math_question_workflow import (
    MathQuestionWorkflow,
)


@pytest.mark.parametrize(
    "message",
    [
        "4",
        "The answer is maybe 4",
        "The answer is 4",
        "The answer maybe 4",
        "The answer may be 4",
        "I think the result is 13",
        "I think it's 14",
        "Maybe 4",
        "I guess 4",
        "I don't know, maybe 4",
        "My answer: 4",
        "Is it 4?",
    ],
)
def test_recognizes_natural_math_answers(message):
    assert MathQuestionWorkflow.is_natural_math_answer(
        message
    )


@pytest.mark.parametrize(
    "message",
    [
        "Give me the answer",
        "I think multiplication",
        "Give me another problem",
        "Explain the multiplication rule",
    ],
)
def test_does_not_confuse_requests_with_answers(message):
    assert not MathQuestionWorkflow.is_natural_math_answer(
        message
    )


def test_new_problem_request_still_works():
    assert MathQuestionWorkflow.is_new_problem_request(
        "Give me another problem"
    )


def test_correct_answer_reaches_math_validator(client):
    student = client.post(
        "/api/v1/students",
        json={
            "display_name": "Math Workflow Test",
            "age": 11,
            "grade": "6",
        },
    )

    assert student.status_code == 201, student.text
    student_id = student.json()["id"]

    session = client.post(
        "/api/v1/sessions",
        json={
            "student_id": student_id,
            "subject": "MATH",
            "mode": "HOMEWORK_HELP",
            "topic": "Order of Operations",
            "concept_code": "MATH_ARITH_ORDER_01",
            "current_problem": "(8 + 4) / 3",
        },
    )

    assert session.status_code == 201, session.text
    session_id = session.json()["id"]

    response = client.post(
        f"/api/v1/tutor/sessions/{session_id}/message",
        json={
            "message": "The answer is maybe 4",
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["detected_intent"] == "STUDENT_ATTEMPT"

    assert data["math_validation"] is not None

    assert data["math_validation"]["supported"] is True

    assert data["math_validation"]["status"] == "CORRECT"

    assert data["math_validation"]["is_correct"] is True

    updated = client.get(
        f"/api/v1/sessions/{session_id}"
    )

    assert updated.status_code == 200

    assert updated.json()["attempt_count"] == 1


def test_wrong_natural_answer_is_validated(client):
    student = client.post(
        "/api/v1/students",
        json={
            "display_name": "Math Wrong Answer Test",
            "age": 11,
            "grade": "6",
        },
    )

    assert student.status_code == 201
    student_id = student.json()["id"]

    session = client.post(
        "/api/v1/sessions",
        json={
            "student_id": student_id,
            "subject": "MATH",
            "mode": "HOMEWORK_HELP",
            "topic": "Order of Operations",
            "concept_code": "MATH_ARITH_ORDER_01",
            "current_problem": "(8 + 4) / 3",
        },
    )

    assert session.status_code == 201
    session_id = session.json()["id"]

    response = client.post(
        f"/api/v1/tutor/sessions/{session_id}/message",
        json={
            "message": "The answer is maybe 5",
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["detected_intent"] == "STUDENT_ATTEMPT"

    assert data["math_validation"]["status"] == "INCORRECT"

    assert data["decision"]["allow_final_answer"] is False
