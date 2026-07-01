from fastapi.testclient import TestClient

from app.main import app


def test_assistant_explain_requires_user_role():
    client = TestClient(app)
    response = client.post("/api/assistant/explain", json={"source_text": "EGFR"})
    assert response.status_code == 400
    assert response.json()["error"] == "user_role_required"


def test_assistant_explain_accepts_role():
    client = TestClient(app)
    response = client.post("/api/assistant/explain", json={"user_role": "patient_family", "source_text": "EGFR"})
    assert response.status_code == 200
    assert response.json()["user_role"] == "patient_family"
