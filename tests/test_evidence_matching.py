from app.evidence_matcher import match_claims_to_evidence
from app.mammal_claim_extractor import extract_claims
from app.sample_data import molecular_evidence


def test_match_claims_to_evidence():
    matches = match_claims_to_evidence(extract_claims("BRCA1 loss needs review."), molecular_evidence())
    assert matches[0].support_status == "supported"
    assert matches[0].matched_evidence
