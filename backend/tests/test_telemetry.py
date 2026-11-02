import time


def create_student(
    client,
) -> str:

    response = client.post(
        "/api/v1/students",

        json={
            "display_name":
                "Telemetry Learner",

            "age": 11,

            "grade": "6",

            "preferred_language":
                "en",

            "curriculum_profile":
                "bangladesh_english_v1",
        },
    )

    assert (
        response.status_code
        == 201
    )

    return (
        response.json()[
            "id"
        ]
    )


def create_math_session(
    client,
    student_id: str,
) -> str:

    response = client.post(
        "/api/v1/sessions",

        json={
            "student_id":
                student_id,

            "mode":
                "PRACTICE",

            "subject":
                "MATH",

            "topic":
                "Linear Equations",

            "concept_code":
                "MATH_ALG_LINEAR_01",

            "current_problem":
                "2x + 5 = 17",
        },
    )

    assert (
        response.status_code
        == 201
    )

    return (
        response.json()[
            "id"
        ]
    )


def test_telemetry_records_learning_interactions(
    client,
):

    student_id = (
        create_student(
            client
        )
    )

    session_id = (
        create_math_session(
            client,
            student_id,
        )
    )


    first = client.post(
        (
            "/api/v1/tutor/"
            f"sessions/{session_id}/"
            "message"
        ),

        json={
            "message":
                "Can you give me a hint?"
        },
    )

    assert (
        first.status_code
        == 200
    )


    # Small delay so the next
    # learner response has measurable
    # non-zero latency.

    time.sleep(
        0.01
    )


    second = client.post(
        (
            "/api/v1/tutor/"
            f"sessions/{session_id}/"
            "message"
        ),

        json={
            "message":
                "I think I subtract 5."
        },
    )

    assert (
        second.status_code
        == 200
    )


    summary = client.get(
        (
            "/api/v1/telemetry/"
            f"students/{student_id}/"
            "concepts/"
            "MATH_ALG_LINEAR_01/"
            "summary"
        )
    )


    assert (
        summary.status_code
        == 200
    )


    data = (
        summary.json()
    )


    assert (
        data[
            "student_messages"
        ]
        == 2
    )

    assert (
        data[
            "tutor_responses"
        ]
        == 2
    )

    assert (
        data[
            "measured_student_responses"
        ]
        >= 1
    )

    assert (
        data[
            "average_response_latency_ms"
        ]
        is not None
    )

    assert (
        data[
            "average_tutor_latency_ms"
        ]
        is not None
    )