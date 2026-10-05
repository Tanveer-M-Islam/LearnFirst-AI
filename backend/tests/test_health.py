from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "learnfirst-api"


def test_health_has_request_id():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers


def test_version_endpoint():
    response = client.get(
        "/api/v1/health/version"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "LearnFirst AI"
    assert "version" in data