from app.models import CancerRecord, GenomicAlteration


def parse_cancer_records(payload: list[dict]) -> list[CancerRecord]:
    return [CancerRecord(**item) for item in payload]


def build_alteration_matrix(records: list[CancerRecord]) -> dict:
    alterations: list[GenomicAlteration] = [a for record in records for a in record.alterations]
    genes = sorted({a.gene for a in alterations})
    samples = sorted({a.sample_id for a in alterations})
    cells = []
    for gene in genes:
        row = {"gene": gene, "pathway": next((a.pathway for a in alterations if a.gene == gene), ""), "samples": {}}
        for sample in samples:
            matching = [a for a in alterations if a.gene == gene and a.sample_id == sample]
            row["samples"][sample] = [a.alteration_type for a in matching] or ["none"]
        cells.append(row)
    return {
        "genes": genes,
        "samples": samples,
        "legend": {"mutation": "Mutation", "amplification": "Amplification", "deletion": "Deletion", "expression": "Expression change"},
        "rows": cells,
    }
