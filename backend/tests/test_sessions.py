def create_student(client):

    response = client.post(
        "/api/v1/students",
        json={
            "display_name": "Nabila",
            "age": 11,
            "grade": "6",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_math_homework_session(
    client,
):
    student = create_student(
        client
    )

    response = client.post(
        "/api/v1/sessions",
        json={
            "student_id": student["id"],
            "mode": "HOMEWORK_HELP",
            "subject": "MATH",
            "topic": "Linear Equations",
            "concept_code": (
                "MATH_ALG_LINEAR_01"
            ),
            "current_problem": (
                "3x + 5 = 20"
            ),
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["subject"] == "MATH"

    assert (
        data["mode"]
        == "HOMEWORK_HELP"
    )

    assert (
        data["current_hint_level"]
        == 0
    )

    assert data["attempt_count"] == 0

    assert (
        data["direct_answer_requests"]
        == 0
    )

    assert (
        data["mastery_state"]
        == "LEARNING"
    )

    assert data["status"] == "ACTIVE"


def test_session_requires_valid_student(
    client,
):
    response = client.post(
        "/api/v1/sessions",
        json={
            "student_id": "not-real",
            "mode": "LEARN",
            "subject": "SCIENCE",
            "topic": "Photosynthesis",
        },
    )

    assert response.status_code == 404