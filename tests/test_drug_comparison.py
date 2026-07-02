from fastapi.testclient import TestClient

from app.main import app


def test_drug_comparison_requires_at_least_one_drug():
    response = TestClient(app).post(
        "/api/drug-comparisons",
        json={"comparison_name": "empty", "drug_ids": [], "target_ids": [], "cancer_context_ids": [], "task_types": ["drug_carcinogenicity"]},
    )
    assert response.status_code == 400
    assert response.json()["error"] == "drug_required"


def test_create_comparison_returns_requirements():
    response = TestClient(app).post(
        "/api/drug-comparisons",
        json={"comparison_name": "BRAF drug comparison", "drug_ids": [1], "target_ids": [2], "cancer_context_ids": [2], "task_types": ["drug_target_interaction"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["comparison"]["comparison_name"] == "BRAF drug comparison"
    assert "requirements" in body
