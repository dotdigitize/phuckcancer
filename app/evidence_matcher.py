from app.models import EvidenceMatch, ExtractedClaim, MolecularEvidence


def match_claims_to_evidence(claims: list[ExtractedClaim], evidence: list[MolecularEvidence]) -> list[EvidenceMatch]:
    matches: list[EvidenceMatch] = []
    for claim in claims:
        matched = [item for item in evidence if claim.gene and item.gene.upper() == claim.gene.upper()]
        status = "supported" if matched else "missing_evidence"
        score = 0.86 if matched else 0.15
        rationale = "Matched by gene and source evidence summary." if matched else "No matching source evidence was found in local evidence records."
        matches.append(EvidenceMatch(claim=claim, matched_evidence=matched, support_status=status, support_score=score, rationale=rationale))
    return matches
