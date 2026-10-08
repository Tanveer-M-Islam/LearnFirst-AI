def create_student(
    client,
    age=11,
):

    response = client.post(
        "/api/v1/students",
        json={
            "display_name": "Nabila",
            "age": age,
            "grade": "6",
        },
    )

    assert response.status_code == 201

    return response.json()


def create_session(
    client,
    student_id,
    mode="HOMEWORK_HELP",
    subject="MATH",
):

    response = client.post(
        "/api/v1/sessions",
        json={
            "student_id": student_id,
            "mode": mode,
            "subject": subject,
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

    return response.json()


def test_homework_requires_attempt(
    client,
):

    student = create_student(
        client
    )

    session = create_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/decision"
        ),
        json={
            "intent": "HOMEWORK_REQUEST"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["next_action"]
        == "ASK_ATTEMPT"
    )

    assert (
        data["allow_final_answer"]
        is False
    )


def test_direct_answer_is_blocked(
    client,
):

    student = create_student(
        client
    )

    session = create_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/decision"
        ),
        json={
            "intent": (
                "DIRECT_ANSWER_REQUEST"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["next_action"] == "ASK_ATTEMPT"

    assert (
        data["allow_final_answer"]
        is False
    )


def test_hint_request_increases_level(
    client,
):

    student = create_student(
        client
    )

    session = create_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/decision"
        ),
        json={
            "intent": "HINT_REQUEST"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["hint_level"] == 1

    assert (
        data["next_action"]
        == "GIVE_HINT"
    )


def test_second_hint_progresses(
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
        f"{session['id']}/decision"
    )

    first = client.post(
        endpoint,
        json={
            "intent": "HINT_REQUEST"
        },
    )

    assert first.status_code == 200

    second = client.post(
        endpoint,
        json={
            "intent": "HINT_REQUEST"
        },
    )

    assert second.status_code == 200

    data = second.json()

    assert data["hint_level"] == 2

    assert (
        data["next_action"]
        == "ASK_GUIDING_QUESTION"
    )


def test_foundation_repeated_confusion(
    client,
):

    student = create_student(
        client,
        age=8,
    )

    session = create_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/decision"
        ),
        json={
            "intent": "I_DONT_KNOW",
            "repeated_confusion": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["hint_level"] == 2

    assert (
        data["next_action"]
        == "ASK_GUIDING_QUESTION"
    )


def test_correct_attempt_triggers_mastery(
    client,
):

    student = create_student(
        client
    )

    session = create_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/decision"
        ),
        json={
            "intent": "STUDENT_ATTEMPT",
            "attempt_status": "CORRECT",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["next_action"]
        == "GIVE_MASTERY_QUESTION"
    )

    assert (
        data["requires_mastery_check"]
        is True
    )


def test_math_attempt_requires_validation(
    client,
):

    student = create_student(
        client
    )

    session = create_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/decision"
        ),
        json={
            "intent": "STUDENT_ATTEMPT",
            "attempt_status": (
                "PARTIALLY_CORRECT"
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["requires_validation"]
        is True
    )


def test_science_requires_rag(
    client,
):

    student = create_student(
        client
    )

    session = create_session(
        client,
        student["id"],
        mode="LEARN",
        subject="SCIENCE",
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/decision"
        ),
        json={
            "intent": "LEARN_CONCEPT"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["requires_rag"]
        is True
    )


def test_policy_bypass_detected(
    client,
):

    student = create_student(
        client
    )

    session = create_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/decision"
        ),
        json={
            "intent": "POLICY_BYPASS"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["next_action"]
        == "REFUSE_POLICY_BYPASS"
    )

    assert (
        data["policy_bypass_detected"]
        is True
    )

    assert (
        data["allow_final_answer"]
        is False
    )


def test_mock_test_disables_hints(
    client,
):

    student = create_student(
        client
    )

    session = create_session(
        client,
        student["id"],
        mode="MOCK_TEST",
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/decision"
        ),
        json={
            "intent": "HINT_REQUEST"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["next_action"]
        == "CLARIFY_TEST_INSTRUCTION"
    )

    assert (
        data["allow_final_answer"]
        is False
    )


def test_safety_overrides_tutor_policy(
    client,
):

    student = create_student(
        client
    )

    session = create_session(
        client,
        student["id"],
    )

    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/decision"
        ),
        json={
            "intent": "SAFETY_SENSITIVE"
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["next_action"]
        == "ESCALATE_SAFETY"
    )