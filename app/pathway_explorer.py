from app.models import PathwayFinding
from app.sample_data import genomic_alterations, molecular_evidence


def pathway_findings() -> list[PathwayFinding]:
    alterations = genomic_alterations()
    evidence = molecular_evidence()
    pathways = sorted({a.pathway for a in alterations})
    findings: list[PathwayFinding] = []
    for pathway in pathways:
        genes = sorted({a.gene for a in alterations if a.pathway == pathway})
        notes = [e.summary for e in evidence if e.gene in genes]
        score = 0.74 if notes else 0.45
        flags = [] if notes else ["missing_source_evidence"]
        findings.append(PathwayFinding(
            pathway=pathway,
            altered_genes=genes,
            evidence_notes=notes or ["Synthetic research fixture requires source review."],
            mammal_interpretation=f"MAMMAL-driven biomedical interpretation identifies {pathway} as a research-level signal requiring qualified human review.",
            support_score=score,
            risk_flags=flags,
            human_review_recommendation="Needs qualified oncology or research review before any clinical use."
        ))
    return findings
