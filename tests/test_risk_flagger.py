from app.risk_flagger import flag_risks


def test_risk_flagger_detects_unsafe_claim():
    flags = flag_risks("This will respond and you should take therapy.", has_evidence=False)
    assert "unsupported_treatment_claim" in flags
    assert "patient_specific_recommendation" in flags
    assert "missing_source_evidence" in flags
