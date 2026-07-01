from app.plain_english import explain_plain_english


def test_plain_english_patient_safety():
    response = explain_plain_english("EGFR L858R", "patient_family")
    assert "Ask your oncologist" in response
    assert "not medical decision-making" in response
