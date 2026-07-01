from app.models import EvidenceMatch


def aggregate_support_score(matches: list[EvidenceMatch]) -> float:
    if not matches:
        return 0.0
    return round(sum(match.support_score for match in matches) / len(matches), 2)
