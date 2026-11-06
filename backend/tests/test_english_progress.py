def create_student(
    client,
):

    response = client.post(
        "/api/v1/students",
        json={
            "display_name":
                "English Progress Learner",

            "age":
                10,

            "grade":
                "5",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_english_progress_empty(
    client,
):

    student = create_student(
        client
    )


    response = client.get(
        (
            "/api/v1/english/progress/"
            f"students/{student['id']}"
            "/concepts/"
            "ENG_GRAMMAR_TENSE_01"
        )
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["total_attempts"]
        == 0
    )


    assert (
        data["mastery_state"]
        == "NOT_STARTED"
    )