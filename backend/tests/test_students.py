def test_create_foundation_student(
    client,
):
    response = client.post(
        "/api/v1/students",
        json={
            "display_name": "Rafi",
            "age": 8,
            "grade": "3",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["display_name"] == "Rafi"

    assert data["age"] == 8

    assert (
        data["age_group"]
        == "FOUNDATION"
    )

    assert (
        data["preferred_language"]
        == "en"
    )

    assert (
        data["curriculum_profile"]
        == "bangladesh_english_v1"
    )


def test_create_developing_student(
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

    assert response.status_code == 201

    assert (
        response.json()["age_group"]
        == "DEVELOPING"
    )


def test_create_independent_student(
    client,
):
    response = client.post(
        "/api/v1/students",
        json={
            "display_name": "Arif",
            "age": 14,
            "grade": "8",
        },
    )

    assert response.status_code == 201

    assert (
        response.json()["age_group"]
        == "INDEPENDENT"
    )


def test_reject_unsupported_age(
    client,
):
    response = client.post(
        "/api/v1/students",
        json={
            "display_name": "Test",
            "age": 6,
            "grade": "1",
        },
    )

    assert response.status_code == 422