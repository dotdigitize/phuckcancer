from fastapi.testclient import TestClient

from app.main import app


def test_drug_library_endpoint_returns_synthetic_drugs():
    response = TestClient(app).get("/api/drugs")
    assert response.status_code == 200
    drugs = response.json()["drugs"]
    assert any(drug["drug_name"] == "Vemurafenib" for drug in drugs)
    assert all("synthetic_fixture" in drug for drug in drugs)


def test_target_and_context_libraries_return_fixtures():
    client = TestClient(app)
    assert any(target["target_name"] == "EGFR" for target in client.get("/api/drug-targets").json()["targets"])
    assert any(context["cancer_type"] == "Lung adenocarcinoma" for context in client.get("/api/cancer-contexts").json()["contexts"])
