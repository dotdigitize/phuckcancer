RISK_KEYWORDS = {
    "unsupported_treatment_claim": ["will respond", "cures", "guaranteed"],
    "diagnostic_overreach": ["diagnoses", "definitive diagnosis"],
    "clinical_action_language": ["start therapy", "stop therapy", "prescribe"],
    "overconfident_language": ["certainly", "always", "never"],
    "missing_uncertainty": ["conclude"],
    "individual_outcome_prediction": ["survival will", "outcome will"],
    "trial_eligibility_overclaim": ["eligible for trial"],
    "drug_response_overclaim": ["will benefit"],
    "patient_specific_recommendation": ["you should take"],
}


def flag_risks(text: str, has_evidence: bool = True) -> list[str]:
    lowered = text.lower()
    flags = [flag for flag, words in RISK_KEYWORDS.items() if any(word in lowered for word in words)]
    if not has_evidence:
        flags.append("missing_source_evidence")
    if "because" in lowered and not has_evidence:
        flags.append("unsupported_causal_claim")
    return sorted(set(flags)) or ["needs_human_review"]
