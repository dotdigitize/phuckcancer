import json
from pathlib import Path
from app.models import CancerRecord, GenomicAlteration, MolecularEvidence

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "sample_data"


def load_json(name: str):
    return json.loads((SAMPLE_DIR / name).read_text())


def load_text(name: str) -> str:
    return (SAMPLE_DIR / name).read_text()


def cancer_records() -> list[CancerRecord]:
    return [CancerRecord(**item) for item in load_json("cancer_genomics_fixture.json")]


def molecular_evidence() -> list[MolecularEvidence]:
    return [MolecularEvidence(**item) for item in load_json("molecular_evidence_fixture.json")]


def genomic_alterations() -> list[GenomicAlteration]:
    return [alteration for record in cancer_records() for alteration in record.alterations]


def overview() -> dict:
    records = cancer_records()
    evidence = molecular_evidence()
    return {
        "cancer_records_loaded": len(records),
        "molecular_evidence_items": len(evidence),
        "mammal_interpretations": 1,
        "evidence_audits": 1,
        "risk_flags": 3,
        "reports_generated": 0,
        "external_connector_status": "disabled_by_default"
    }
