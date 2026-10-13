def create_student(
    client,
):

    response = client.post(
        "/api/v1/students",
        json={
            "display_name": "Nabila",
            "age": 11,
            "grade": "6",
        },
    )

    assert (
        response.status_code
        == 201
    )

    return response.json()


def create_math_session(
    client,
    student_id,
    problem="3x + 5 = 20",
):

    response = client.post(
        "/api/v1/sessions",
        json={
            "student_id": (
                student_id
            ),

            "mode": (
                "HOMEWORK_HELP"
            ),

            "subject": "MATH",

            "topic": (
                "Linear Equations"
            ),

            "concept_code": (
                "MATH_ALG_LINEAR_01"
            ),

            "current_problem": (
                problem
            ),
        },
    )

    assert (
        response.status_code
        == 201
    )

    return response.json()


def test_correct_math_attempt(
    client,
):

    student = create_student(
        client
    )

    session = create_math_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message": (
                "I think x = 5."
            )
        },
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        data["detected_intent"]
        == "STUDENT_ATTEMPT"
    )

    assert (
        data["math_validation"]
        ["status"]
        == "CORRECT"
    )

    assert (
        data["math_validation"]
        ["is_correct"]
        is True
    )

    assert (
        data["decision"]
        ["next_action"]
        == "GIVE_MASTERY_QUESTION"
    )

    assert (
        data["decision"]
        ["requires_mastery_check"]
        is True
    )

    # Critical answer leakage test.
    assert (
        "expected_answer"
        not in data["math_validation"]
    )


def test_divide_coefficient_misconception(
    client,
):

    student = create_student(
        client
    )

    session = create_math_session(
        client,
        student["id"],
        problem="3x + 6 = 18",
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message": (
                "3x = 12; x = 12"
            )
        },
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    validation = (
        data["math_validation"]
    )

    assert (
        validation["status"]
        == "PARTIALLY_CORRECT"
    )

    assert (
        "3x = 12"
        in validation[
            "correct_steps"
        ]
    )

    assert (
        validation[
            "first_error_step"
        ]
        == "x = 12"
    )

    assert (
        validation[
            "misconception_code"
        ]
        == "MATH_DIVIDE_COEFFICIENT"
    )

    assert (
        data["decision"]
        ["next_action"]
        == "ASK_GUIDING_QUESTION"
    )

    assert (
        data["decision"]
        ["allow_final_answer"]
        is False
    )


def test_incorrect_math_attempt(
    client,
):

    student = create_student(
        client
    )

    session = create_math_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message": (
                "I think x = 7."
            )
        },
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        data["math_validation"]
        ["status"]
        == "INCORRECT"
    )

    assert (
        data["decision"]
        ["allow_final_answer"]
        is False
    )


def test_attempt_count_updates(
    client,
):

    student = create_student(
        client
    )

    session = create_math_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message": (
                "I think x = 5."
            )
        },
    )

    assert (
        response.status_code
        == 200
    )

    session_response = client.get(
        (
            "/api/v1/sessions/"
            f"{session['id']}"
        )
    )

    assert (
        session_response.status_code
        == 200
    )

    assert (
        session_response
        .json()["attempt_count"]
        == 1
    )


def test_bare_number_is_attempt(
    client,
):

    student = create_student(
        client
    )

    session = create_math_session(
        client,
        student["id"],
        problem="12 + 7",
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message": "19"
        },
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        data["detected_intent"]
        == "STUDENT_ATTEMPT"
    )

    assert (
        data["math_validation"]
        ["status"]
        == "CORRECT"
    )


def test_math_validation_does_not_leak_answer(
    client,
):

    student = create_student(
        client
    )

    session = create_math_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message": (
                "I think x = 9."
            )
        },
    )

    assert (
        response.status_code
        == 200
    )

    validation = (
        response
        .json()
        ["math_validation"]
    )

    assert (
        "expected_answer"
        not in validation
    )