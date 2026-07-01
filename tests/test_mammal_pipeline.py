from app.mammal_pipeline import run_mammal_pipeline
from app.sample_data import molecular_evidence


def test_mammal_pipeline_uses_fallback():
    result = run_mammal_pipeline(molecular_evidence())
    assert result["interpretation"].fallback_used is True
    assert result["audit"].matches
