import re
from app.models import ExtractedClaim


def extract_claims(text: str) -> list[ExtractedClaim]:
    pieces = [p.strip() for p in re.split(r"[.\n]+", text) if p.strip()]
    claims: list[ExtractedClaim] = []
    for idx, piece in enumerate(pieces, start=1):
        gene = next((g for g in ["TP53", "KRAS", "EGFR", "BRCA1", "BRCA2", "PIK3CA"] if g in piece.upper()), None)
        claims.append(ExtractedClaim(claim_id=f"claim-{idx}", text=piece, gene=gene))
    return claims
