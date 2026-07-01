from app.mammal_pipeline import build_mammal_task_payload
from app.sample_data import molecular_evidence


def test_build_mammal_task_payload_instructs_mammal():
    payload = build_mammal_task_payload(molecular_evidence())
    assert payload["task"] == "cancer_molecular_evidence_interpretation"
    assert "MAMMAL as a biomedical reasoning engine" in payload["instruction"]
    assert "no_treatment_recommendation" in payload["safety_constraints"]
