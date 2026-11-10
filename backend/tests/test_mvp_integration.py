
import pytest


# ======================================
# Test helper
# ======================================

def create_student(
    client,
    age: int = 11,
) -> str:

    response = client.post(
        "/api/v1/students",
        json={
            "display_name": "MVP Test Learner",
            "age": age,
            "grade": str(max(1, age - 5)),
        },
    )

    assert response.status_code == 201, response.text

    return response.json()["id"]


# ======================================
# Health and database
# ======================================

def test_health_and_readiness(client):

    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    readiness = client.get(
        "/api/v1/health/ready"
    )

    assert readiness.status_code == 200, readiness.text
    assert readiness.json()["database"] == "ok"


# ======================================
# Curriculum — Math, Science, English
# ======================================

@pytest.mark.parametrize(
    "subject",
    ["MATH", "SCIENCE", "ENGLISH"],
)
def test_curriculum_available(
    client,
    subject,
):

    student_id = create_student(client)

    response = client.get(
        f"/api/v1/curriculum/students/{student_id}/path",
        params={
            "subject": subject,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["student_id"] == student_id
    assert data["subject"] == subject


# ======================================
# Conversation history persistence
# ======================================

def test_tutor_messages_are_persisted(client):

    student_id = create_student(
        client,
        age=14,
    )

    session_response = client.post(
        "/api/v1/sessions",
        json={
            "student_id": student_id,
            "subject": "MATH",
            "mode": "HOMEWORK_HELP",
            "topic": "Linear Equations",
            "concept_code": "MATH_ALG_LINEAR_01",
            "current_problem": "3x + 5 = 20",
        },
    )

    assert session_response.status_code == 201, (
        session_response.text
    )

    session_id = session_response.json()["id"]

    student_messages = [
        "Can I get a hint?",
        "I think x = 5.",
    ]

    tutor_replies = []

    for message in student_messages:

        response = client.post(
            f"/api/v1/tutor/sessions/{session_id}/message",
            json={
                "message": message,
            },
        )

        assert response.status_code == 200, response.text

        data = response.json()

        assert data["session_id"] == session_id

        tutor_replies.append(
            data["reply"]
        )

    # Verify saved messages.

    history = client.get(
        f"/api/v1/history/sessions/{session_id}/messages",
        params={
            "student_id": student_id,
        },
    )

    assert history.status_code == 200, history.text

    saved = history.json()

    assert len(saved) == 4

    assert [
        item["role"]
        for item in saved
    ] == [
        "user",
        "assistant",
        "user",
        "assistant",
    ]

    assert saved[0]["content"] == student_messages[0]
    assert saved[1]["content"] == tutor_replies[0]

    assert saved[2]["content"] == student_messages[1]
    assert saved[3]["content"] == tutor_replies[1]

    assert saved[1]["response_payload"] is not None
    assert saved[3]["response_payload"] is not None

    # Verify the session appears in History.

    sessions = client.get(
        f"/api/v1/history/students/{student_id}/sessions"
    )

    assert sessions.status_code == 200, sessions.text

    matching = [
        item
        for item in sessions.json()
        if item["session_id"] == session_id
    ]

    assert len(matching) == 1
    assert matching[0]["message_count"] == 4


# ======================================
# History ownership check
# ======================================

def test_history_rejects_mismatched_student(client):

    owner_id = create_student(
        client,
        age=14,
    )

    session = client.post(
        "/api/v1/sessions",
        json={
            "student_id": owner_id,
            "subject": "MATH",
            "mode": "LEARN",
            "concept_code": "MATH_ALG_LINEAR_01",
        },
    )

    assert session.status_code == 201, session.text

    session_id = session.json()["id"]

    other_student_id = create_student(
        client,
        age=11,
    )

    response = client.get(
        f"/api/v1/history/sessions/{session_id}/messages",
        params={
            "student_id": other_student_id,
        },
    )

    assert response.status_code == 403


# ======================================
# English assessment persistence
# ======================================

def test_english_diagnostic_persists(client):

    student_id = create_student(
        client,
        age=10,
    )

    started = client.post(
        "/api/v1/english/assessments/start",
        json={
            "student_id": student_id,
            "subject": "ENGLISH",
            "concept_code": "ENG_GRAMMAR_TENSE_01",
            "assessment_type": "DIAGNOSTIC",
        },
    )

    assert started.status_code == 201, started.text

    assessment = started.json()

    assert assessment["total_questions"] == 3

    # Use the question IDs returned by the API.

    answers = [
        {
            "question_id": question["question_id"],
            "response": (
                "goes"
                if question["question_id"] == "TENSE-E-01"
                else "wrong"
            ),
        }
        for question in assessment["questions"]
    ]

    submitted = client.post(
        "/api/v1/english/assessments/"
        f"{assessment['assessment_id']}/submit",
        json={
            "answers": answers,
        },
    )

    assert submitted.status_code == 200, submitted.text

    saved_progress = client.get(
        "/api/v1/english/progress/"
        f"students/{student_id}/concepts/"
        "ENG_GRAMMAR_TENSE_01"
    )

    assert saved_progress.status_code == 200, (
        saved_progress.text
    )

    progress = saved_progress.json()

    assert progress["diagnostic"] is not None

    assert (
        progress["diagnostic"]["score_percent"]
        == submitted.json()["score_percent"]
    )


# ======================================
# English Mastery persistence
# ======================================

def test_english_mastery_persists(client):

    student_id = create_student(
        client,
        age=10,
    )

    started = client.post(
        "/api/v1/english/assessments/start",
        json={
            "student_id": student_id,
            "subject": "ENGLISH",
            "concept_code": "ENG_GRAMMAR_TENSE_01",
            "assessment_type": "MASTERY",
        },
    )

    assert started.status_code == 201, started.text

    assessment = started.json()

    correct = {
        "TENSE-MAST-01": "walk",
        "TENSE-MAST-02": "wrote",
        "TENSE-MAST-03": "will visit",
    }

    answers = [
        {
            "question_id": question["question_id"],
            "response": correct[question["question_id"]],
        }
        for question in assessment["questions"]
    ]

    submitted = client.post(
        "/api/v1/english/assessments/"
        f"{assessment['assessment_id']}/submit",
        json={
            "answers": answers,
        },
    )

    assert submitted.status_code == 200, submitted.text

    result = submitted.json()

    assert result["score_percent"] == 100.0
    assert result["mastery_state"] == "STRONG"

    progress_response = client.get(
        "/api/v1/english/progress/"
        f"students/{student_id}/concepts/"
        "ENG_GRAMMAR_TENSE_01"
    )

    assert progress_response.status_code == 200, (
        progress_response.text
    )

    progress = progress_response.json()

    assert progress["mastery"] is not None
    assert progress["mastery"]["score_percent"] == 100.0
    assert progress["mastery_state"] == "STRONG"
