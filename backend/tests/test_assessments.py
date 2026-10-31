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


def start_assessment(
    client,
    student_id,
    assessment_type,
    session_id=None,
):

    body = {
        "student_id": student_id,
        "subject": "MATH",
        "concept_code": (
            "MATH_ALG_LINEAR_01"
        ),
        "assessment_type": (
            assessment_type
        ),
    }

    if session_id is not None:
        body["session_id"] = (
            session_id
        )

    response = client.post(
        "/api/v1/assessments/start",
        json=body,
    )

    assert (
        response.status_code
        == 201
    )

    return response.json()


def diagnostic_answers():

    return [
        {
            "question_id": "ALG-D-01",
            "response": "x = 4",
        },
        {
            "question_id": "ALG-D-02",
            "response": "x = 5",
        },
        {
            "question_id": "ALG-D-03",
            "response": "x = 5",
        },
        {
            "question_id": "ALG-D-04",
            "response": "x = 7",
        },
        {
            "question_id": "ALG-D-05",
            "response": "x = 5",
        },
    ]


def mastery_answers():

    return [
        {
            "question_id": "ALG-M-01",
            "response": "x = 6",
        },
        {
            "question_id": "ALG-M-02",
            "response": "x = 4",
        },
        {
            "question_id": "ALG-M-03",
            "response": "x = 5",
        },
        {
            "question_id": "ALG-M-04",
            "response": "x = 5",
        },
        {
            "question_id": "ALG-M-05",
            "response": "x = 5",
        },
    ]


def test_start_diagnostic_hides_answers(
    client,
):

    student = create_student(
        client
    )

    assessment = start_assessment(
        client,
        student["id"],
        "DIAGNOSTIC",
    )

    assert (
        assessment[
            "assessment_type"
        ]
        == "DIAGNOSTIC"
    )

    assert (
        assessment[
            "total_questions"
        ]
        == 5
    )

    assert (
        len(
            assessment["questions"]
        )
        == 5
    )

    for question in (
        assessment["questions"]
    ):

        assert (
            "expected_answer"
            not in question
        )


def test_diagnostic_score_is_40(
    client,
):

    student = create_student(
        client
    )

    assessment = start_assessment(
        client,
        student["id"],
        "DIAGNOSTIC",
    )

    response = client.post(
        (
            "/api/v1/assessments/"
            f"{assessment['assessment_id']}"
            "/submit"
        ),
        json={
            "answers": (
                diagnostic_answers()
            )
        },
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        data["correct_answers"]
        == 2
    )

    assert (
        data["score_percent"]
        == 40.0
    )

    assert (
        data[
            "recommended_difficulty"
        ]
        == "MODERATE"
    )


def test_mastery_measures_improvement(
    client,
):

    student = create_student(
        client
    )

    diagnostic = start_assessment(
        client,
        student["id"],
        "DIAGNOSTIC",
    )

    response = client.post(
        (
            "/api/v1/assessments/"
            f"{diagnostic['assessment_id']}"
            "/submit"
        ),
        json={
            "answers": (
                diagnostic_answers()
            )
        },
    )

    assert (
        response.status_code
        == 200
    )

    mastery = start_assessment(
        client,
        student["id"],
        "MASTERY",
    )

    response = client.post(
        (
            "/api/v1/assessments/"
            f"{mastery['assessment_id']}"
            "/submit"
        ),
        json={
            "answers": (
                mastery_answers()
            )
        },
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        data["correct_answers"]
        == 4
    )

    assert (
        data["score_percent"]
        == 80.0
    )

    assert (
        data[
            "baseline_score_percent"
        ]
        == 40.0
    )

    assert (
        data[
            "score_gain_percentage_points"
        ]
        == 40.0
    )

    assert (
        data["improved"]
        is True
    )

    assert (
        data["mastery_state"]
        == "STRONG"
    )

    assert (
        data[
            "recommended_difficulty"
        ]
        == "CHALLENGING"
    )


def test_public_result_does_not_leak_answers(
    client,
):

    student = create_student(
        client
    )

    assessment = start_assessment(
        client,
        student["id"],
        "DIAGNOSTIC",
    )

    response = client.post(
        (
            "/api/v1/assessments/"
            f"{assessment['assessment_id']}"
            "/submit"
        ),
        json={
            "answers": (
                diagnostic_answers()
            )
        },
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    for answer in data["answers"]:

        assert (
            "expected_answer"
            not in answer
        )


def test_progress_endpoint(
    client,
):

    student = create_student(
        client
    )

    diagnostic = start_assessment(
        client,
        student["id"],
        "DIAGNOSTIC",
    )

    client.post(
        (
            "/api/v1/assessments/"
            f"{diagnostic['assessment_id']}"
            "/submit"
        ),
        json={
            "answers": (
                diagnostic_answers()
            )
        },
    )

    mastery = start_assessment(
        client,
        student["id"],
        "MASTERY",
    )

    client.post(
        (
            "/api/v1/assessments/"
            f"{mastery['assessment_id']}"
            "/submit"
        ),
        json={
            "answers": (
                mastery_answers()
            )
        },
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

    data = response.json()

    assert (
        data["diagnostic"]
        ["score_percent"]
        == 40.0
    )

    assert (
        data["mastery"]
        ["score_percent"]
        == 80.0
    )

    assert (
        data[
            "score_gain_percentage_points"
        ]
        == 40.0
    )

    assert (
        data[
            "current_mastery_state"
        ]
        == "STRONG"
    )