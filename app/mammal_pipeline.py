from app.evidence_matcher import match_claims_to_evidence
from app.mammal_claim_extractor import extract_claims
from app.mammal_engine import MammalEngine
from app.models import AuditResult, MolecularEvidence
from app.risk_flagger import flag_risks
from app.review_workflow import review_status_for_flags


def run_mammal_pipeline(evidence: list[MolecularEvidence]) -> dict:
    engine = MammalEngine()
    interpretation = engine.interpret([item.model_dump() for item in evidence])
    claims = extract_claims(interpretation.interpretation)
    matches = match_claims_to_evidence(claims, evidence)
    all_text = " ".join(claim.text for claim in claims)
    flags = flag_risks(all_text, has_evidence=all(match.matched_evidence for match in matches))
    audit = AuditResult(audit_id="audit-mammal-001", matches=matches, risk_flags=flags, review_status=review_status_for_flags(flags))
    return {"interpretation": interpretation, "claims": claims, "audit": audit}
