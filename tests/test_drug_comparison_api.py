from fastapi.testclient import TestClient

from app.main import app


def test_comparison_matrix_returns_rows_with_scores_and_missing_data():
    client = TestClient(app)
    created = client.post(
        "/api/drug-comparisons",
        json={"comparison_name": "Matrix test", "drug_ids": [1], "target_ids": [2], "cancer_context_ids": [2], "task_types": ["drug_target_interaction"]},
    ).json()
    comparison_id = created["comparison"]["comparison_id"]
    matrix = client.get(f"/api/drug-comparisons/{comparison_id}/matrix").json()
    assert matrix["rows"][0]["drug_name"] == "Vemurafenib"
    assert "drug_target_binding_signal" in matrix["rows"][0]
    assert "evidence_support_score" in matrix["rows"][0]
    assert "overall_review_priority" in matrix["rows"][0]
    assert "missing_data" in matrix["rows"][0]
