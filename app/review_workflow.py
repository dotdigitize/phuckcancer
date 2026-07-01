def review_status_for_flags(flags: list[str]) -> str:
    severe = {"unsupported_treatment_claim", "clinical_action_language", "patient_specific_recommendation", "diagnostic_overreach"}
    return "escalated" if severe.intersection(flags) else "needs_human_review"
