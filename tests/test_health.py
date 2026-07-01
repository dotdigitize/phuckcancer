from fastapi.testclient import TestClient
from app.main import app


def test_health():
    client = TestClient(app)
    assert client.get("/health").json()["status"] == "ok"


def test_system_status_is_local_safe():
    client = TestClient(app)
    data = client.get("/api/system/status").json()
    assert data["backend_port"] == 8717
    assert data["frontend_port"] == 5179
    assert data["database_provider"] == "mariadb"
    assert data["mammal_required"] is True
    assert "not a medical device" in data["medical_safety"]
