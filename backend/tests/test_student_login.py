def test_create_student_with_login(
    client,
):

    response = client.post(
        "/api/v1/students",

        json={
            "display_name": "Rafi",
            "age": 11,
            "grade": "6",
            "username": "rafi11",
            "password": "student123",
        },
    )


    assert (
        response.status_code
        == 201
    )


    data = (
        response.json()
    )


    assert (
        data["username"]
        == "rafi11"
    )


    # Never expose password data.

    assert (
        "password"
        not in data
    )


    assert (
        "password_hash"
        not in data
    )


    assert (
        "password_salt"
        not in data
    )


def test_login_student(
    client,
):

    created = client.post(
        "/api/v1/students",

        json={
            "display_name": "Rafi",
            "age": 11,
            "grade": "6",
            "username": "rafi11",
            "password": "student123",
        },
    )


    assert (
        created.status_code
        == 201
    )


    response = client.post(
        "/api/v1/students/login",

        json={
            "username": "RAFI11",
            "password": "student123",
        },
    )


    assert (
        response.status_code
        == 200
    )


    assert (
        response.json()[
            "display_name"
        ]
        == "Rafi"
    )


    assert (
        response.json()[
            "username"
        ]
        == "rafi11"
    )


def test_reject_wrong_password(
    client,
):

    created = client.post(
        "/api/v1/students",

        json={
            "display_name": "Rafi",
            "age": 11,
            "grade": "6",
            "username": "rafi11",
            "password": "student123",
        },
    )


    assert (
        created.status_code
        == 201
    )


    response = client.post(
        "/api/v1/students/login",

        json={
            "username": "rafi11",
            "password": "wrongpass123",
        },
    )


    assert (
        response.status_code
        == 401
    )


def test_reject_duplicate_username(
    client,
):

    first = client.post(
        "/api/v1/students",

        json={
            "display_name": "Rafi",
            "age": 11,
            "grade": "6",
            "username": "student1",
            "password": "student123",
        },
    )


    assert (
        first.status_code
        == 201
    )


    second = client.post(
        "/api/v1/students",

        json={
            "display_name": "Nabila",
            "age": 12,
            "grade": "7",
            "username": "student1",
            "password": "another123",
        },
    )


    assert (
        second.status_code
        == 400
    )


def test_existing_profile_can_set_credentials(
    client,
):

    # Legacy/internal profile without
    # credentials.

    created = client.post(
        "/api/v1/students",

        json={
            "display_name":
                "Old Student",

            "age":
                10,

            "grade":
                "5",
        },
    )


    assert (
        created.status_code
        == 201
    )


    student_id = (
        created.json()[
            "id"
        ]
    )


    response = client.patch(
        (
            "/api/v1/students/"
            + student_id
            + "/credentials"
        ),

        json={
            "username":
                "oldstudent",

            "password":
                "oldstudent123",
        },
    )


    assert (
        response.status_code
        == 200
    )


    assert (
        response.json()[
            "username"
        ]
        == "oldstudent"
    )


    login = client.post(
        "/api/v1/students/login",

        json={
            "username":
                "oldstudent",

            "password":
                "oldstudent123",
        },
    )


    assert (
        login.status_code
        == 200
    )


def test_existing_credentials_require_current_password(
    client,
):

    created = client.post(
        "/api/v1/students",

        json={
            "display_name":
                "Rafi",

            "age":
                11,

            "grade":
                "6",

            "username":
                "rafi11",

            "password":
                "student123",
        },
    )


    assert (
        created.status_code
        == 201
    )


    student_id = (
        created.json()[
            "id"
        ]
    )


    response = client.patch(
        (
            "/api/v1/students/"
            + student_id
            + "/credentials"
        ),

        json={
            "username":
                "rafi_new",

            "password":
                "newpassword123",

            "current_password":
                "student123",
        },
    )


    assert (
        response.status_code
        == 200
    )


    assert (
        response.json()[
            "username"
        ]
        == "rafi_new"
    )


def test_reject_credential_change_with_wrong_current_password(
    client,
):

    created = client.post(
        "/api/v1/students",

        json={
            "display_name":
                "Rafi",

            "age":
                11,

            "grade":
                "6",

            "username":
                "rafi11",

            "password":
                "student123",
        },
    )


    assert (
        created.status_code
        == 201
    )


    student_id = (
        created.json()[
            "id"
        ]
    )


    response = client.patch(
        (
            "/api/v1/students/"
            + student_id
            + "/credentials"
        ),

        json={
            "username":
                "rafi_new",

            "password":
                "newpassword123",

            "current_password":
                "wrongpassword",
        },
    )


    assert (
        response.status_code
        == 400
    )