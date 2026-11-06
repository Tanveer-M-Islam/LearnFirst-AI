# ============================================================
# LearnFirst AI
# Curriculum Progression Tests
# ============================================================


def create_student(
    client,
    *,
    name="Curriculum Learner",
    age=10,
    grade="5",
):

    response = client.post(
        "/api/v1/students",
        json={
            "display_name":
                name,

            "age":
                age,

            "grade":
                grade,
        },
    )


    assert (
        response.status_code
        == 201
    )


    return response.json()


def get_curriculum_path(
    client,
    student_id,
    subject,
):

    return client.get(
        (
            "/api/v1/curriculum/"
            f"students/{student_id}"
            f"/path?subject={subject}"
        )
    )


# ============================================================
# Basic path response
# ============================================================


def test_math_curriculum_path_returns_success(
    client,
):

    student = create_student(
        client,
        age=10,
        grade="5",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["student_id"]
        == student["id"]
    )


    assert (
        data["subject"]
        == "MATH"
    )


    assert (
        data["learner_age"]
        == 10
    )


    assert (
        data["selection_policy"]
        == "AGE_PRIMARY_GRADE_CONTEXT"
    )


# ============================================================
# Math age progression
# ============================================================


def test_age_7_math_targets_basic_arithmetic(
    client,
):

    student = create_student(
        client,
        age=7,
        grade="2",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"]
        is not None
    )


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "MATH_ARITH_BASIC_01"
    )


    assert (
        data["recommended_concept"]
        is not None
    )


    assert (
        data["recommended_concept"][
            "concept_code"
        ]
        == "MATH_ARITH_BASIC_01"
    )


def test_age_8_math_targets_multiplication_division(
    client,
):

    student = create_student(
        client,
        age=8,
        grade="3",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "MATH_ARITH_MULTDIV_01"
    )


def test_age_9_math_targets_fractions(
    client,
):

    student = create_student(
        client,
        age=9,
        grade="4",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "MATH_ARITH_FRAC_01"
    )


def test_age_10_math_targets_integers(
    client,
):

    student = create_student(
        client,
        age=10,
        grade="5",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "MATH_ARITH_INT_01"
    )


def test_age_11_math_targets_order_of_operations(
    client,
):

    student = create_student(
        client,
        age=11,
        grade="6",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "MATH_ARITH_ORDER_01"
    )


def test_age_12_math_targets_pre_algebra(
    client,
):

    student = create_student(
        client,
        age=12,
        grade="7",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "MATH_PREALG_EXPR_01"
    )


def test_age_13_math_targets_linear_equations(
    client,
):

    student = create_student(
        client,
        age=13,
        grade="8",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "MATH_ALG_LINEAR_01"
    )


def test_age_14_math_targets_linear_graphs(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "MATH_GRAPH_LINEAR_01"
    )


# ============================================================
# New learner behavior
#
# Missing mastery evidence must NOT be treated as failure.
# ============================================================


def test_new_age_14_math_learner_is_not_forced_to_age_7(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "MATH_GRAPH_LINEAR_01"
    )


    assert (
        data["recommended_concept"][
            "concept_code"
        ]
        == "MATH_GRAPH_LINEAR_01"
    )


    assert (
        data["prerequisite_review_concept"]
        is None
    )


def test_missing_mastery_is_not_weak_mastery(
    client,
):

    student = create_student(
        client,
        age=13,
        grade="8",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["recommended_concept"][
            "concept_code"
        ]
        == "MATH_ALG_LINEAR_01"
    )


    assert (
        data["prerequisite_review_concept"]
        is None
    )


# ============================================================
# Science age progression
# ============================================================


def test_age_7_science_targets_living_things(
    client,
):

    student = create_student(
        client,
        age=7,
        grade="2",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "SCI_LIFE_BASIC_01"
    )


def test_age_8_science_targets_materials(
    client,
):

    student = create_student(
        client,
        age=8,
        grade="3",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "SCI_MATERIAL_BASIC_01"
    )


def test_age_9_science_targets_matter(
    client,
):

    student = create_student(
        client,
        age=9,
        grade="4",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "SCI_PHY_MATTER_01"
    )


def test_age_10_science_targets_food_chains(
    client,
):

    student = create_student(
        client,
        age=10,
        grade="5",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "SCI_BIO_FOODCHAIN_01"
    )


def test_age_11_science_targets_ecosystems(
    client,
):

    student = create_student(
        client,
        age=11,
        grade="6",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "SCI_ECO_SYSTEMS_01"
    )


    assert (
        data["recommended_concept"][
            "concept_code"
        ]
        == "SCI_ECO_SYSTEMS_01"
    )


def test_new_science_learner_does_not_fallback_without_evidence(
    client,
):

    student = create_student(
        client,
        age=11,
        grade="6",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["recommended_concept"][
            "concept_code"
        ]
        == "SCI_ECO_SYSTEMS_01"
    )


    assert (
        data["prerequisite_review_concept"]
        is None
    )


def test_age_12_science_targets_photosynthesis(
    client,
):

    student = create_student(
        client,
        age=12,
        grade="7",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "SCI_BIO_PHOTO_01"
    )


def test_age_13_science_targets_energy_transfer(
    client,
):

    student = create_student(
        client,
        age=13,
        grade="8",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "SCI_ENERGY_TRANSFER_01"
    )


def test_age_14_science_targets_cells(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "SCI_CELL_SYSTEMS_01"
    )


# ============================================================
# English curriculum
#
# Phase 21.4:
# English is now IMPLEMENTED and ACTIVE.
# ============================================================


def test_english_path_is_active(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["subject"]
        == "ENGLISH"
    )


    assert (
        data["target_concept"]
        is not None
    )


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "ENG_READ_INFERENCE_01"
    )


    assert (
        data["recommended_concept"]
        is not None
    )


    assert (
        data["recommended_concept"][
            "concept_code"
        ]
        == "ENG_READ_INFERENCE_01"
    )


    assert (
        data["recommended_concept"][
            "implemented"
        ]
        is True
    )


def test_age_7_english_targets_vocabulary(
    client,
):

    student = create_student(
        client,
        age=7,
        grade="2",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "ENG_VOCAB_FOUND_01"
    )


    assert (
        data["recommended_concept"][
            "concept_code"
        ]
        == "ENG_VOCAB_FOUND_01"
    )


def test_age_8_english_targets_simple_sentences(
    client,
):

    student = create_student(
        client,
        age=8,
        grade="3",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "ENG_SENT_SIMPLE_01"
    )


def test_age_9_english_targets_parts_of_speech(
    client,
):

    student = create_student(
        client,
        age=9,
        grade="4",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "ENG_GRAMMAR_POS_01"
    )


def test_age_10_english_targets_core_tenses(
    client,
):

    student = create_student(
        client,
        age=10,
        grade="5",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "ENG_GRAMMAR_TENSE_01"
    )


def test_age_11_english_targets_reading_comprehension(
    client,
):

    student = create_student(
        client,
        age=11,
        grade="6",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "ENG_READ_CORE_01"
    )


def test_age_12_english_targets_sentence_structure(
    client,
):

    student = create_student(
        client,
        age=12,
        grade="7",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "ENG_SENT_STRUCTURE_01"
    )


def test_age_13_english_targets_advanced_grammar(
    client,
):

    student = create_student(
        client,
        age=13,
        grade="8",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "ENG_GRAMMAR_ADV_01"
    )


def test_age_14_english_targets_reading_inference(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["target_concept"][
            "concept_code"
        ]
        == "ENG_READ_INFERENCE_01"
    )


    assert (
        data["recommended_concept"][
            "concept_code"
        ]
        == "ENG_READ_INFERENCE_01"
    )


def test_new_english_learner_does_not_fallback_without_evidence(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data["recommended_concept"][
            "concept_code"
        ]
        == "ENG_READ_INFERENCE_01"
    )


    assert (
        data["prerequisite_review_concept"]
        is None
    )


# ============================================================
# English implementation state
# ============================================================


def test_all_english_path_concepts_are_implemented(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    english_concepts = (
        data["concepts"]
    )


    assert (
        len(
            english_concepts
        )
        >= 8
    )


    expected_codes = {
        "ENG_VOCAB_FOUND_01",
        "ENG_SENT_SIMPLE_01",
        "ENG_GRAMMAR_POS_01",
        "ENG_GRAMMAR_TENSE_01",
        "ENG_READ_CORE_01",
        "ENG_SENT_STRUCTURE_01",
        "ENG_GRAMMAR_ADV_01",
        "ENG_READ_INFERENCE_01",
    }


    returned_codes = {
        concept[
            "concept_code"
        ]
        for concept
        in english_concepts
    }


    assert (
        expected_codes
        .issubset(
            returned_codes
        )
    )


    for concept in english_concepts:

        if (
            concept[
                "concept_code"
            ]
            in expected_codes
        ):

            assert (
                concept[
                    "implemented"
                ]
                is True
            )


# ============================================================
# Subject isolation
# ============================================================


def test_math_path_contains_only_math(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    for concept in data["concepts"]:

        assert (
            concept["subject"]
            == "MATH"
        )


def test_science_path_contains_only_science(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    for concept in data["concepts"]:

        assert (
            concept["subject"]
            == "SCIENCE"
        )


def test_english_path_contains_only_english(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    for concept in data["concepts"]:

        assert (
            concept["subject"]
            == "ENGLISH"
        )


# ============================================================
# Age groups
# ============================================================


def test_foundation_age_group(
    client,
):

    student = create_student(
        client,
        age=8,
        grade="3",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "ENGLISH",
    )


    assert (
        response.status_code
        == 200
    )


    assert (
        response.json()[
            "age_group"
        ]
        == "FOUNDATION"
    )


def test_developing_age_group(
    client,
):

    student = create_student(
        client,
        age=11,
        grade="6",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "SCIENCE",
    )


    assert (
        response.status_code
        == 200
    )


    assert (
        response.json()[
            "age_group"
        ]
        == "DEVELOPING"
    )


def test_independent_age_group(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    response = get_curriculum_path(
        client,
        student["id"],
        "MATH",
    )


    assert (
        response.status_code
        == 200
    )


    assert (
        response.json()[
            "age_group"
        ]
        == "INDEPENDENT"
    )