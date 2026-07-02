from app.mammal_model_registry import model_registry_payload


def test_model_registry_payload_exposes_configured_tasks():
    payload = model_registry_payload()
    task_types = {model["task_type"] for model in payload["models"]}
    assert "cell_line_drug_response" in task_types
    assert "drug_target_interaction" in task_types
