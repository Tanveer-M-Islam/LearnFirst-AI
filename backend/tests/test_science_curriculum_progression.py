import pytest


AGE_EXPECTATIONS = [
    (
        7,
        "2",
        "SCI_LIFE_BASIC_01",
    ),

    (
        8,
        "3",
        "SCI_MATERIAL_BASIC_01",
    ),

    (
        9,
        "4",
        "SCI_PHY_MATTER_01",
    ),

    (
        10,
        "5",
        "SCI_BIO_FOODCHAIN_01",
    ),

    (
        11,
        "6",
        "SCI_ECO_SYSTEMS_01",
    ),

    (
        12,
        "7",
        "SCI_BIO_PHOTO_01",
    ),

    (
        13,
        "8",
        "SCI_ENERGY_TRANSFER_01",
    ),

    (
        14,
        "9",
        "SCI_CELL_SYSTEMS_01",
    ),
]


@pytest.mark.parametrize(
    (
        "age,"
        "grade,"
        "expected_concept"
    ),
    AGE_EXPECTATIONS,
)
def test_science_age_progression(
    client,
    age: int,
    grade: str,
    expected_concept: str,
):

    student_response = (
        client.post(
            "/api/v1/students",

            json={
                "display_name":
                    f"Science Age {age}",

                "age":
                    age,

                "grade":
                    grade,
            },
        )
    )


    assert (
        student_response
        .status_code
        == 201
    )


    student = (
        student_response
        .json()
    )


    response = (
        client.get(
            (
                "/api/v1/curriculum/"
                f"students/{student['id']}"
                "/path"
            ),

            params={
                "subject":
                    "SCIENCE",
            },
        )
    )


    assert (
        response.status_code
        == 200
    )


    path = (
        response.json()
    )


    assert (
        path[
            "target_concept"
        ][
            "concept_code"
        ]
        == expected_concept
    )


    assert (
        path[
            "recommended_concept"
        ][
            "concept_code"
        ]
        == expected_concept
    )


    assert (
        path[
            "prerequisite_review_concept"
        ]
        is None
    )