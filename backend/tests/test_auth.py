def create_account(
    client,
):

    response = client.post(
        "/api/v1/students",

        json={
            "display_name":
                "Login Student",

            "username":
                "loginstudent",

            "password":
                "secret123",

            "age":
                10,

            "grade":
                "5",

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


    return response.json()


def test_create_student_with_login(
    client,
):

    student = create_account(
        client
    )


    assert (
        student["username"]
        == "loginstudent"
    )


    assert (
        "password"
        not in student
    )


    assert (
        "password_hash"
        not in student
    )


def test_login_success(
    client,
):

    student = create_account(
        client
    )


    response = client.post(
        "/api/v1/auth/login",

        json={
            "username":
                "loginstudent",

            "password":
                "secret123",
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["id"]
        == student["id"]
    )


    assert (
        data["username"]
        == "loginstudent"
    )


def test_login_wrong_password(
    client,
):

    create_account(
        client
    )


    response = client.post(
        "/api/v1/auth/login",

        json={
            "username":
                "loginstudent",

            "password":
                "wrongpassword",
        },
    )


    assert (
        response.status_code
        == 401
    )


def test_login_unknown_username(
    client,
):

    response = client.post(
        "/api/v1/auth/login",

        json={
            "username":
                "missinguser",

            "password":
                "secret123",
        },
    )


    assert (
        response.status_code
        == 401
    )


def test_duplicate_username_rejected(
    client,
):

    create_account(
        client
    )


    response = client.post(
        "/api/v1/students",

        json={
            "display_name":
                "Second Student",

            "username":
                "loginstudent",

            "password":
                "another123",

            "age":
                11,

            "grade":
                "6",
        },
    )


    assert (
        response.status_code
        == 400
    )