def create_student(
    client,
):

    response = client.post(
        "/api/v1/students",
        json={
            "display_name": "Rafi",
            "age": 11,
            "grade": "6",
        },
    )

    assert (
        response.status_code
        == 201
    )

    return response.json()


def create_session(
    client,
    student_id,
):

    response = client.post(
        "/api/v1/sessions",
        json={
            "student_id": student_id,
            "mode": "HOMEWORK_HELP",
            "subject": "MATH",
            "topic": (
                "Linear Equations"
            ),
            "concept_code": (
                "MATH_ALG_LINEAR_01"
            ),
            "current_problem": (
                "3x + 6 = 18"
            ),
        },
    )

    assert (
        response.status_code
        == 201
    )

    return response.json()


def test_learning_independence_metrics(
    client,
):

    student = create_student(
        client
    )

    session = create_session(
        client,
        student["id"],
    )

    endpoint = (
        "/api/v1/tutor/sessions/"
        f"{session['id']}/message"
    )

    direct = client.post(
        endpoint,
        json={
            "message": (
                "Just give me the answer."
            )
        },
    )

    assert (
        direct.status_code
        == 200
    )

    partial = client.post(
        endpoint,
        json={
            "message": (
                "3x = 12; x = 12"
            )
        },
    )

    assert (
        partial.status_code
        == 200
    )

    correct = client.post(
        endpoint,
        json={
            "message": "x = 4"
        },
    )

    assert (
        correct.status_code
        == 200
    )

    response = client.get(
        (
            "/api/v1/assessments/"
            f"students/{student['id']}"
            "/concepts/"
            "MATH_ALG_LINEAR_01"
            "/progress"
        )
    )

    assert (
        response.status_code
        == 200
    )

    metrics = (
        response.json()
        ["learning_metrics"]
    )

    assert (
        metrics["total_attempts"]
        == 2
    )

    assert (
        metrics["correct_attempts"]
        == 1
    )

    assert (
        metrics[
            "direct_answer_requests"
        ]
        == 1
    )

    assert (
        metrics[
            "retry_success_count"
        ]
        == 1
    )

    assert (
        metrics[
            "independent_attempt_rate"
        ]
        == 50.0
    )