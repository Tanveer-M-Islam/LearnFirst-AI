def create_student(
    client,
    age=10,
    grade="5",
):

    response = client.post(
        "/api/v1/students",

        json={
            "display_name":
                "English Tutor Learner",

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


def create_english_session(
    client,
    student_id,
    concept_code=(
        "ENG_GRAMMAR_TENSE_01"
    ),
    topic="Core Tenses",
    problem=(
        "Complete the sentence: "
        "'She ___ to school every day.' "
        "Use the correct form of 'go'."
    ),
    mode="PRACTICE",
):

    response = client.post(
        "/api/v1/sessions",

        json={
            "student_id":
                student_id,

            "mode":
                mode,

            "subject":
                "ENGLISH",

            "topic":
                topic,

            "concept_code":
                concept_code,

            "current_problem":
                problem,
        },
    )


    assert (
        response.status_code
        == 201
    )


    return response.json()


# ======================================================
# Correct exact-answer English attempt
# ======================================================

def test_bare_english_answer_is_attempt(
    client,
):

    student = create_student(
        client
    )


    session = create_english_session(
        client,
        student["id"],
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "goes"
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "detected_intent"
        ]
        == "STUDENT_ATTEMPT"
    )


    assert (
        data[
            "english_validation"
        ]
        is not None
    )


    assert (
        data[
            "english_validation"
        ][
            "status"
        ]
        == "CORRECT"
    )


    assert (
        data[
            "english_validation"
        ][
            "supported"
        ]
        is True
    )


# ======================================================
# Wrong exact-answer English attempt
# ======================================================

def test_wrong_english_answer(
    client,
):

    student = create_student(
        client
    )


    session = create_english_session(
        client,
        student["id"],
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "go"
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "english_validation"
        ]
        is not None
    )


    assert (
        data[
            "english_validation"
        ][
            "status"
        ]
        == "INCORRECT"
    )


    assert (
        data[
            "decision"
        ][
            "allow_final_answer"
        ]
        is False
    )


# ======================================================
# Sentence-rule evaluation
# ======================================================

def test_sentence_partial_feedback(
    client,
):

    student = create_student(
        client,
        age=8,
        grade="3",
    )


    session = create_english_session(
        client,
        student["id"],

        concept_code=(
            "ENG_SENT_SIMPLE_01"
        ),

        topic=(
            "Simple Sentences"
        ),

        problem=(
            "Write a complete sentence "
            "using the word 'cat'."
        ),
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "the cat is sleeping."
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "english_validation"
        ]
        is not None
    )


    assert (
        data[
            "english_validation"
        ][
            "status"
        ]
        == "PARTIALLY_CORRECT"
    )


    feedback = (
        data[
            "english_validation"
        ][
            "rule_feedback"
        ]
    )


    assert any(
        (
            "capital"
            in item.lower()
        )

        for item
        in feedback
    )


# ======================================================
# Complete sentence is correct
# ======================================================

def test_complete_sentence_is_correct(
    client,
):

    student = create_student(
        client,
        age=8,
        grade="3",
    )


    session = create_english_session(
        client,
        student["id"],

        concept_code=(
            "ENG_SENT_SIMPLE_01"
        ),

        topic=(
            "Simple Sentences"
        ),

        problem=(
            "Write a complete sentence "
            "using the word 'cat'."
        ),
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "The cat is sleeping."
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "english_validation"
        ][
            "status"
        ]
        == "CORRECT"
    )


# ======================================================
# Direct-answer protection
# ======================================================

def test_direct_answer_request_is_protected(
    client,
):

    student = create_student(
        client
    )


    session = create_english_session(
        client,
        student["id"],
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "Just give me the answer."
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "detected_intent"
        ]
        == "DIRECT_ANSWER_REQUEST"
    )


    assert (
        data[
            "english_validation"
        ]
        is None
    )


    assert (
        data[
            "decision"
        ][
            "allow_final_answer"
        ]
        is False
    )


# ======================================================
# Correct attempt is actually recorded
#
# Important:
# session.attempt_count may return to 0 after a
# correct response because LearnFirst immediately
# assigns the next question.
#
# Therefore we verify the persisted adaptive history.
# ======================================================

def test_english_attempt_is_recorded(
    client,
):

    student = create_student(
        client
    )


    session = create_english_session(
        client,
        student["id"],
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "goes"
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "english_validation"
        ]
        is not None
    )


    assert (
        data[
            "english_validation"
        ][
            "status"
        ]
        == "CORRECT"
    )


    adaptive_response = client.get(
        (
            "/api/v1/english/adaptive/"
            f"students/{student['id']}"
            "/concepts/"
            "ENG_GRAMMAR_TENSE_01"
            "/plan"
        )
    )


    assert (
        adaptive_response.status_code
        == 200
    )


    adaptive_data = (
        adaptive_response.json()
    )


    assert (
        adaptive_data[
            "total_attempts"
        ]
        == 1
    )


    assert (
        adaptive_data[
            "correct_attempts"
        ]
        == 1
    )


    assert (
        adaptive_data[
            "understanding_score_percent"
        ]
        == 100.0
    )


# ======================================================
# Incorrect attempt is also recorded
# ======================================================

def test_incorrect_english_attempt_is_recorded(
    client,
):

    student = create_student(
        client
    )


    session = create_english_session(
        client,
        student["id"],
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "go"
        },
    )


    assert (
        response.status_code
        == 200
    )


    adaptive_response = client.get(
        (
            "/api/v1/english/adaptive/"
            f"students/{student['id']}"
            "/concepts/"
            "ENG_GRAMMAR_TENSE_01"
            "/plan"
        )
    )


    assert (
        adaptive_response.status_code
        == 200
    )


    adaptive_data = (
        adaptive_response.json()
    )


    assert (
        adaptive_data[
            "total_attempts"
        ]
        == 1
    )


    assert (
        adaptive_data[
            "correct_attempts"
        ]
        == 0
    )


    assert (
        adaptive_data[
            "understanding_score_percent"
        ]
        == 0.0
    )


# ======================================================
# Reading comprehension
# ======================================================

def test_reading_answer_is_evaluated(
    client,
):

    student = create_student(
        client,
        age=11,
        grade="6",
    )


    session = create_english_session(
        client,
        student["id"],

        concept_code=(
            "ENG_READ_CORE_01"
        ),

        topic=(
            "Reading Comprehension"
        ),

        problem=(
            "Read: 'Rina woke up early "
            "and watered the plants "
            "before school.' "
            "What did Rina do before "
            "school?"
        ),
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "She watered the plants."
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "english_validation"
        ]
        is not None
    )


    assert (
        data[
            "english_validation"
        ][
            "status"
        ]
        == "CORRECT"
    )


# ======================================================
# Reading inference
# ======================================================

def test_reading_inference_answer(
    client,
):

    student = create_student(
        client,
        age=14,
        grade="9",
    )


    session = create_english_session(
        client,
        student["id"],

        concept_code=(
            "ENG_READ_INFERENCE_01"
        ),

        topic=(
            "Reading and Inference"
        ),

        problem=(
            "Read: 'Nadia looked at "
            "the dark clouds and quickly "
            "closed all the windows.' "
            "What did Nadia probably "
            "expect?"
        ),
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "She probably expected rain."
        },
    )


    assert (
        response.status_code
        == 200
    )


    assert (
        response.json()[
            "english_validation"
        ][
            "status"
        ]
        == "CORRECT"
    )


# ======================================================
# Parts of speech
# ======================================================

def test_parts_of_speech_answer(
    client,
):

    student = create_student(
        client,
        age=9,
        grade="4",
    )


    session = create_english_session(
        client,
        student["id"],

        concept_code=(
            "ENG_GRAMMAR_POS_01"
        ),

        topic=(
            "Parts of Speech"
        ),

        problem=(
            "In the sentence "
            "'The dog runs fast', "
            "which word is the noun?"
        ),
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "dog"
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "detected_intent"
        ]
        == "STUDENT_ATTEMPT"
    )


    assert (
        data[
            "english_validation"
        ][
            "status"
        ]
        == "CORRECT"
    )


# ======================================================
# Intermediate grammar
# ======================================================

def test_intermediate_grammar_answer(
    client,
):

    student = create_student(
        client,
        age=13,
        grade="8",
    )


    session = create_english_session(
        client,
        student["id"],

        concept_code=(
            "ENG_GRAMMAR_ADV_01"
        ),

        topic=(
            "Intermediate Grammar"
        ),

        problem=(
            "Correct the sentence: "
            "'He have finished "
            "his work.'"
        ),
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "He has finished his work."
        },
    )


    assert (
        response.status_code
        == 200
    )


    assert (
        response.json()[
            "english_validation"
        ][
            "status"
        ]
        == "CORRECT"
    )


# ======================================================
# English practice request
# ======================================================

def test_english_practice_request(
    client,
):

    student = create_student(
        client
    )


    session = create_english_session(
        client,
        student["id"],

        problem=None,
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "Give me a practice question."
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "detected_intent"
        ]
        == "PRACTICE_REQUEST"
    )


    assert (
        data[
            "decision"
        ][
            "next_action"
        ]
        == "GENERATE_PRACTICE_QUESTION"
    )


    assert (
        "English question"
        in data[
            "reply"
        ]
    )


# ======================================================
# English response schema should not expose
# internal missing ideas.
# ======================================================

def test_english_public_validation_hides_missing_ideas(
    client,
):

    student = create_student(
        client,
        age=8,
        grade="3",
    )


    session = create_english_session(
        client,
        student["id"],

        concept_code=(
            "ENG_SENT_SIMPLE_01"
        ),

        topic=(
            "Simple Sentences"
        ),

        problem=(
            "Write a sentence using "
            "'boy' and 'runs'."
        ),
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "The boy sleeps."
        },
    )


    assert (
        response.status_code
        == 200
    )


    validation = (
        response.json()[
            "english_validation"
        ]
    )


    assert (
        validation is not None
    )


    assert (
        "missing_ideas"
        not in validation
    )


# ======================================================
# Math / Science fields remain empty
# during English evaluation.
# ======================================================

def test_english_response_does_not_use_other_validators(
    client,
):

    student = create_student(
        client
    )


    session = create_english_session(
        client,
        student["id"],
    )


    response = client.post(
        (
            "/api/v1/tutor/sessions/"
            f"{session['id']}/message"
        ),

        json={
            "message":
                "goes"
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert (
        data[
            "math_validation"
        ]
        is None
    )


    assert (
        data[
            "science_validation"
        ]
        is None
    )


    assert (
        data[
            "english_validation"
        ]
        is not None
    )