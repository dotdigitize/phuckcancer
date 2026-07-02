from app.mammal_model_registry import model_registry_payload


def test_model_registry_payload_exposes_configured_tasks():
    payload = model_registry_payload()
    task_types = {model["task_type"] for model in payload["models"]}
    assert "cell_line_drug_response" in task_types
    assert "drug_target_interaction" in task_types


def test_model_registry_exposes_base_tokenizer_and_checkpoint_fields():
    payload = model_registry_payload()
    assert payload["base_model_id"] == "ibm/biomed.omics.bl.sm.ma-ted-458m"
    assert payload["base_tokenizer_id"] == "ibm/biomed.omics.bl.sm.ma-ted-458m"
    assert payload["official_repo_url"] == "https://github.com/BiomedSciAI/biomed-multi-alignment"
    first_model = payload["models"][0]
    assert "checkpoint_model_id" in first_model
    assert "checkpoint_path" in first_model
    assert "tokenizer_id" in first_model
    assert "base_model_id" in first_model
