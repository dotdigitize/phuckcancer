from app.config import Settings
from app.mammal_model_registry import model_registry_payload


def test_mammal_availability_urls_exist_in_settings():
    settings = Settings()
    assert settings.mammal_base_model_id == "ibm/biomed.omics.bl.sm.ma-ted-458m"
    assert settings.mammal_base_tokenizer_id == "ibm/biomed.omics.bl.sm.ma-ted-458m"
    assert settings.mammal_official_repo_url == "https://github.com/BiomedSciAI/biomed-multi-alignment"
    assert settings.mammal_hf_finetuned_models_url.startswith("https://huggingface.co/models")
    assert settings.mammal_hf_space_url == "https://huggingface.co/spaces/ibm/biomed-multi-alignment"


def test_model_registry_payload_exposes_huggingface_links():
    payload = model_registry_payload()
    assert payload["hf_finetuned_models_url"] == "https://huggingface.co/models?other=base_model:finetune:ibm-research/biomed.omics.bl.sm.ma-ted-458m"
    assert payload["hf_space_url"] == "https://huggingface.co/spaces/ibm/biomed-multi-alignment"
    assert any(model["hf_model_url"] for model in payload["models"])
