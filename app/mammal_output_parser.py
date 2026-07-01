from app.mammal_claim_extractor import extract_claims


def parse_mammal_output(payload: dict | str) -> dict:
    if isinstance(payload, str):
        text = payload
        findings = [line.strip("- ") for line in text.splitlines() if line.strip()]
    else:
        findings = [str(item) for item in payload.get("findings", [])]
        text = payload.get("interpretation", "\n".join(findings))
    claims = extract_claims(text)
    return {"findings": findings, "interpretation": text, "claims": [c.model_dump() for c in claims]}
