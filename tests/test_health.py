from fastapi.testclient import TestClient
from app.main import app


def test_health():
    client = TestClient(app)
    assert client.get("/health").json()["status"] == "ok"


def test_system_status_is_local_safe():
    client = TestClient(app)
    data = client.get("/api/system/status").json()
    assert data["database"]["enabled"] is False
    assert "not a medical device" in data["medical_safety"]
