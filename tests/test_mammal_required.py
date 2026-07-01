from app.config import Settings
from app.mammal_pipeline import build_mammal_task_payload


def test_mammal_required_default_true():
    settings = Settings()
    assert settings.mammal_required is True


def test_task_payload_has_required_fields():
    payload = build_mammal_task_payload([{"gene": "EGFR", "variant": "L858R", "ignored": "x"}])
    assert payload["records"][0]["gene"] == "EGFR"
    assert "ignored" not in payload["records"][0]
    assert "biological_interpretation" in payload["required_output_fields"]
