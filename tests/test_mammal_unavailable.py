from fastapi.testclient import TestClient

from app.main import app


def test_mammal_unavailable_returns_503():
    client = TestClient(app)
    response = client.post("/api/mammal/interpret", json={})
    assert response.status_code == 503
    body = response.json()
    detail = body.get("detail", body)
    assert detail["error"] == "mammal_unavailable"
    assert "MAMMAL is required" in detail["message"]
