from app.evidence_matcher import match_claims_to_evidence
from app.mammal_claim_extractor import extract_claims
from app.config import get_settings
from app.mammal_output_parser import parse_mammal_output
from app.mammal_providers import get_mammal_provider
from app.models import AuditResult, MolecularEvidence
from app.risk_flagger import flag_risks
from app.review_workflow import review_status_for_flags


TASK_INSTRUCTION = (
    "Interpret this cancer molecular evidence using MAMMAL as a biomedical reasoning engine. "
    "Identify biological signal, pathway context, molecular relationships, uncertainty, evidence gaps, "
    "and questions for qualified human review. Do not diagnose, prescribe, predict individual outcomes, "
    "determine clinical-trial eligibility, or recommend treatment."
)

ACCEPTED_INPUT_FIELDS = {
    "gene",
    "variant",
    "cancer_type",
    "pathway",
    "evidence_note",
    "molecular_profile",
    "expression_signal",
    "resistance_signal",
    "trial_signal",
    "cbioportal_record",
    "external_source",
}


def build_mammal_task_payload(evidence: list[MolecularEvidence | dict]) -> dict:
    records: list[dict] = []
    for item in evidence:
        data = item.model_dump() if hasattr(item, "model_dump") else dict(item)
        normalized = {field: data.get(field) for field in ACCEPTED_INPUT_FIELDS if data.get(field) is not None}
        if "evidence_note" not in normalized and data.get("summary"):
            normalized["evidence_note"] = data["summary"]
        if "external_source" not in normalized and data.get("source"):
            normalized["external_source"] = data["source"]
        records.append(normalized)
    return {
        "task": "cancer_molecular_evidence_interpretation",
        "instruction": TASK_INSTRUCTION,
        "records": records,
        "required_output_fields": [
            "biological_interpretation",
            "molecular_signal",
            "pathway_context",
            "evidence_strength",
            "uncertainty",
            "review_questions",
        ],
        "safety_constraints": [
            "research_and_evidence_support_only",
            "qualified_human_review_required",
            "no_diagnosis",
            "no_prescription",
            "no_treatment_recommendation",
            "no_outcome_prediction",
            "no_trial_eligibility_decision",
        ],
    }


def run_mammal_pipeline(evidence: list[MolecularEvidence | dict]) -> dict:
    settings = get_settings()
    provider = get_mammal_provider(settings)
    payload = build_mammal_task_payload(evidence)
    parsed = parse_mammal_output(provider.interpret(payload))
    from app.models import MammalInterpretation

    interpretation = MammalInterpretation(
        interpretation_id="mammal-live-001",
        model_name=parsed["model_name"] or settings.mammal_model_name,
        provider=parsed["provider"],
        biological_interpretation=parsed["biological_interpretation"],
        molecular_signal=parsed["molecular_signal"],
        pathway_context=parsed["pathway_context"],
        evidence_strength=parsed["evidence_strength"],
        uncertainty=parsed["uncertainty"],
        review_questions=parsed["review_questions"],
        raw_mammal_output=parsed["raw_mammal_output"],
        interpretation=parsed["interpretation"],
        claims=[claim["text"] for claim in parsed["claims"]],
    )
    claims = extract_claims(interpretation.interpretation)
    model_evidence = [item for item in evidence if isinstance(item, MolecularEvidence)]
    matches = match_claims_to_evidence(claims, model_evidence)
    all_text = " ".join(claim.text for claim in claims)
    flags = flag_risks(all_text, has_evidence=all(match.matched_evidence for match in matches))
    audit = AuditResult(audit_id="audit-mammal-001", matches=matches, risk_flags=flags, review_status=review_status_for_flags(flags))
    return {"interpretation": interpretation, "claims": claims, "audit": audit}
