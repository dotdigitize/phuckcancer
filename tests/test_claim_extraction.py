from app.mammal_claim_extractor import extract_claims


def test_extract_claims_detects_gene():
    claims = extract_claims("EGFR alteration suggests a pathway signal. This needs review.")
    assert claims[0].gene == "EGFR"
    assert len(claims) == 2
