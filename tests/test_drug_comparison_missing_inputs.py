from fastapi.testclient import TestClient

from app.main import app


def _create(task_type: str, target_ids: list[int] | None = None, cell_line_names: list[str] | None = None):
    return TestClient(app).post(
        "/api/drug-comparisons",
        json={
            "comparison_name": f"{task_type} missing",
            "drug_ids": [1],
            "target_ids": target_ids or [],
            "cancer_context_ids": [1],
            "task_types": [task_type],
            "cell_line_names": cell_line_names or [],
        },
    ).json()


def test_cell_line_drug_response_requires_smiles_and_cell_line_or_h5ad():
    body = _create("cell_line_drug_response")
    missing = body["requirements"]["missing_structured_data"][0]["missing_fields"]
    assert "drug_smiles" in missing
    assert "cell_line_name_or_cell_line_h5ad_file" in missing


def test_drug_carcinogenicity_requires_smiles():
    body = _create("drug_carcinogenicity")
    missing = body["requirements"]["missing_structured_data"][0]["missing_fields"]
    assert "drug_smiles" in missing


def test_run_missing_data_returns_missing_structured_data():
    client = TestClient(app)
    created = _create("drug_target_interaction", target_ids=[1])
    response = client.post(f"/api/drug-comparisons/{created['comparison']['comparison_id']}/run", json={})
    assert response.status_code == 400
    assert response.json()["error"] == "missing_structured_data"
