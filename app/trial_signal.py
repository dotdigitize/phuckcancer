def review_trial_signal(payload: dict) -> dict:
    missing = payload.get("missing_required_information") or ["confirmed biomarker status", "trial protocol criteria", "oncologist/research coordinator review"]
    return {
        "title": payload.get("title", "Clinical-trial signal"),
        "status": "Possible signal for review" if not missing else "Missing information",
        "missing_required_information": missing,
        "human_review_status": "Needs oncologist/research coordinator review",
    }
