from app.models import CancerRecord, GenomicAlteration, MolecularEvidence


def _gene_symbol(record: dict) -> str:
    gene = record.get("gene") or {}
    return gene.get("hugoGeneSymbol") or record.get("hugoGeneSymbol") or record.get("gene") or "UNKNOWN"


def normalize_mutations(records: list[dict], study_id: str = "external_cbioportal_study") -> list[CancerRecord]:
    grouped: dict[str, list[dict]] = {}
    for record in records:
        grouped.setdefault(record.get("sampleId", "external-sample"), []).append(record)
    cancer_records: list[CancerRecord] = []
    for sample_id, mutations in grouped.items():
        alterations = []
        evidence = []
        for idx, mutation in enumerate(mutations, start=1):
            gene = _gene_symbol(mutation)
            pathway = "DNA repair" if gene in {"BRCA1", "BRCA2", "TP53"} else "MAPK pathway" if gene in {"KRAS", "EGFR"} else "Cancer signaling"
            alterations.append(GenomicAlteration(
                gene=gene,
                sample_id=sample_id,
                cancer_type=mutation.get("cancerType", "external cancer genomics record"),
                alteration_type="mutation",
                variant=mutation.get("proteinChange") or mutation.get("keyword"),
                mutation_class=mutation.get("mutationType", "unknown"),
                pathway=pathway,
            ))
            evidence.append(MolecularEvidence(
                evidence_id=f"cbioportal-{sample_id}-{idx}",
                gene=gene,
                cancer_type=mutation.get("cancerType", "external cancer genomics record"),
                evidence_type="external_mutation_record",
                summary=f"cBioPortal mutation record for {gene} in {sample_id}; requires PhuckCancer audit and qualified human review.",
                source=f"cBioPortal API study {study_id}",
                confidence_note="External data source normalized into PhuckCancer internal evidence model.",
            ))
        cancer_records.append(CancerRecord(
            record_id=f"cbioportal-{study_id}-{sample_id}",
            study=study_id,
            cancer_type="external cancer genomics data",
            sample_group=sample_id,
            alterations=alterations,
            evidence=evidence,
        ))
    return cancer_records


def normalize_studies(records: list[dict]) -> list[dict]:
    return [{
        "study_id": item.get("studyId"),
        "name": item.get("name"),
        "cancer_type": item.get("cancerTypeId"),
        "description": item.get("description", ""),
    } for item in records]
