from app.mammal_claim_extractor import extract_claims
from app.mammal_providers import MammalInvalidOutputError


def parse_mammal_output(payload: dict | str) -> dict:
    if not isinstance(payload, dict):
        raise MammalInvalidOutputError("MAMMAL output must be a structured object.")
    required = [
        "biological_interpretation",
        "molecular_signal",
        "pathway_context",
        "evidence_strength",
        "uncertainty",
        "review_questions",
    ]
    missing = [field for field in required if field not in payload]
    if missing:
        raise MammalInvalidOutputError(f"MAMMAL output missing required fields: {', '.join(missing)}")
    review_questions = payload["review_questions"]
    if not isinstance(review_questions, list):
        raise MammalInvalidOutputError("MAMMAL review_questions must be a list.")
    text = "\n".join(
        [
            str(payload["biological_interpretation"]),
            str(payload["molecular_signal"]),
            str(payload["pathway_context"]),
            str(payload["evidence_strength"]),
            str(payload["uncertainty"]),
            " ".join(str(question) for question in review_questions),
        ]
    )
    claims = extract_claims(text)
    return {
        "biological_interpretation": str(payload["biological_interpretation"]),
        "molecular_signal": str(payload["molecular_signal"]),
        "pathway_context": str(payload["pathway_context"]),
        "evidence_strength": str(payload["evidence_strength"]),
        "uncertainty": str(payload["uncertainty"]),
        "review_questions": [str(question) for question in review_questions],
        "provider": str(payload.get("provider", "local")),
        "model_name": str(payload.get("model_name", "")),
        "raw_mammal_output": payload,
        "interpretation": text,
        "claims": [c.model_dump() for c in claims],
    }
