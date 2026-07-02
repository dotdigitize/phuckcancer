from fastapi.testclient import TestClient

from app.main import app
from app.mammal_task_runner import MissingStructuredDataError, validate_task_inputs


def test_cell_line_drug_response_requires_structured_fields():
    try:
        validate_task_inputs("cell_line_drug_response", {"model_path": "/m.ckpt", "drug_smiles": "CCO", "drug_name": "drug"})
    except MissingStructuredDataError as exc:
        assert "cell_line_name_or_cell_line_h5ad_file" in exc.missing_fields
    else:
        assert False


def test_drug_target_interaction_requires_normalization_values():
    try:
        validate_task_inputs("drug_target_interaction", {"model_path": "/m", "target_protein_sequence": "MEEP", "drug_smiles": "CCO"})
    except MissingStructuredDataError as exc:
        assert "norm_y_mean" in exc.missing_fields
        assert "norm_y_std" in exc.missing_fields
    else:
        assert False


def test_drug_carcinogenicity_requires_model_and_smiles():
    try:
        validate_task_inputs("drug_carcinogenicity", {"drug_name": "unknown"})
    except MissingStructuredDataError as exc:
        assert set(exc.missing_fields) == {"model_path", "drug_smiles"}
    else:
        assert False


def test_missing_structured_inputs_return_400():
    client = TestClient(app)
    response = client.post("/api/mammal/tasks/cell_line_drug_response", json={"drug_name": "drug"})
    assert response.status_code == 400
    assert response.json()["error"] == "missing_structured_data"
