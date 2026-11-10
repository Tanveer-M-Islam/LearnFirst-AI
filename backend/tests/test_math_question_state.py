
from app.intent.router import IntentRouter
from app.math.parser import evaluate_arithmetic
from app.schemas.enums import TutorIntent
from app.services.math_question_workflow import (
    MathQuestionWorkflow,
)


def test_new_problem_request_detection():
    assert MathQuestionWorkflow.is_new_problem_request(
        "Give me another problem"
    )

    assert MathQuestionWorkflow.is_new_problem_request(
        "Can you give me another problem?"
    )


def test_natural_result_detection():
    assert MathQuestionWorkflow.is_natural_math_answer(
        "I think the result is 13"
    )

    assert MathQuestionWorkflow.is_natural_math_answer(
        "The answer maybe 14"
    )

    assert not MathQuestionWorkflow.is_natural_math_answer(
        "I think multiplication"
    )

    assert not MathQuestionWorkflow.is_natural_math_answer(
        "Give me the final answer"
    )


def test_new_math_problem_is_saved_and_graded(client):

    student_response = client.post(
        "/api/v1/students",
        json={
            "display_name": "Math State Test",
            "age": 11,
            "grade": "6",
        },
    )

    assert student_response.status_code == 201

    student_id = student_response.json()["id"]

    session_response = client.post(
        "/api/v1/sessions",
        json={
            "student_id": student_id,
            "mode": "HOMEWORK_HELP",
            "subject": "MATH",
            "topic": "Order of Operations",
            "concept_code": "MATH_ARITH_ORDER_01",
            "current_problem": "8 + 2 * 3",
        },
    )

    assert session_response.status_code == 201

    session_id = session_response.json()["id"]

    # Request a completely new problem.
    response = client.post(
        f"/api/v1/tutor/sessions/{session_id}/message",
        json={
            "message": "Give me another problem",
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["provider"] == "system"
    assert data["model"] == "adaptive-practice"

    # Confirm the problem was actually saved.
    saved_response = client.get(
        f"/api/v1/sessions/{session_id}"
    )

    assert saved_response.status_code == 200

    new_problem = saved_response.json()["current_problem"]

    assert new_problem
    assert new_problem != "8 + 2 * 3"
    assert new_problem in data["reply"]

    # Calculate the answer to the new,
    # database-backed problem.
    correct_answer = str(
        evaluate_arithmetic(new_problem)
    )

    # Submit using natural learner language.
    answer_response = client.post(
        f"/api/v1/tutor/sessions/{session_id}/message",
        json={
            "message": (
                f"I think the result is {correct_answer}"
            )
        },
    )

    assert answer_response.status_code == 200, (
        answer_response.text
    )

    result = answer_response.json()

    assert result["detected_intent"] == (
        TutorIntent.STUDENT_ATTEMPT.value
    )

    assert result["math_validation"] is not None

    assert result["math_validation"]["status"] == "CORRECT"

    assert result["math_validation"]["is_correct"] is True

    assert "correct" in result["reply"].lower()
