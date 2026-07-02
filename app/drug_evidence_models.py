from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from app.models import CancerContextRecord, DrugLibraryRecord, DrugTargetRecord


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


SYNTHETIC_DRUG_FIXTURES: list[DrugLibraryRecord] = [
    DrugLibraryRecord(id=1, drug_name="Vemurafenib", drug_class="BRAF inhibitor", mechanism_summary="Synthetic fixture record for BRAF pathway evidence organization.", known_targets=["BRAF"], cancer_contexts=["Melanoma"], resistance_notes="Synthetic fixture: resistance review notes must be replaced with sourced evidence before clinical use.", trial_notes="Synthetic fixture: add real clinical-trial citations before use.", evidence_notes="Synthetic research fixture; no MAMMAL output is included.", synthetic_fixture=True),
    DrugLibraryRecord(id=2, drug_name="Osimertinib", drug_class="EGFR inhibitor", mechanism_summary="Synthetic fixture record for EGFR pathway evidence organization.", known_targets=["EGFR"], cancer_contexts=["Lung adenocarcinoma"], resistance_notes="Synthetic fixture: resistance mechanisms are not enumerated here.", trial_notes="Synthetic fixture: trial evidence requires sourced review.", evidence_notes="Synthetic research fixture; no drug response score is precomputed.", synthetic_fixture=True),
    DrugLibraryRecord(id=3, drug_name="Imatinib", drug_class="Tyrosine kinase inhibitor", mechanism_summary="Synthetic fixture record for kinase target evidence organization.", known_targets=["ABL1", "KIT", "PDGFRA"], cancer_contexts=["Leukemia", "Gastrointestinal stromal tumor"], resistance_notes="Synthetic fixture: add sourced mutation-level resistance notes.", trial_notes="Synthetic fixture only.", evidence_notes="Synthetic research fixture.", synthetic_fixture=True),
    DrugLibraryRecord(id=4, drug_name="Sotorasib", drug_class="KRAS G12C inhibitor", mechanism_summary="Synthetic fixture record for KRAS pathway evidence organization.", known_targets=["KRAS"], cancer_contexts=["Lung adenocarcinoma", "Colorectal cancer"], resistance_notes="Synthetic fixture: no patient-specific resistance call.", trial_notes="Synthetic fixture only.", evidence_notes="Synthetic research fixture.", synthetic_fixture=True),
    DrugLibraryRecord(id=5, drug_name="Trastuzumab style biologic", drug_class="HER2-directed biologic", mechanism_summary="Synthetic fixture record for biologic-style evidence organization; no SMILES applies unless a valid structured representation is supplied.", known_targets=["ERBB2"], cancer_contexts=["Breast cancer"], resistance_notes="Synthetic fixture only.", trial_notes="Synthetic fixture only.", evidence_notes="Synthetic research fixture.", synthetic_fixture=True),
]

SYNTHETIC_TARGET_FIXTURES: list[DrugTargetRecord] = [
    DrugTargetRecord(id=1, target_name="EGFR", gene_symbol="EGFR", protein_name="Epidermal growth factor receptor", pathway="EGFR signaling", cancer_context="Lung adenocarcinoma", notes="Synthetic fixture. Protein sequence intentionally omitted until supplied from a trusted source."),
    DrugTargetRecord(id=2, target_name="BRAF", gene_symbol="BRAF", protein_name="B-Raf proto-oncogene serine/threonine-protein kinase", pathway="MAPK pathway", cancer_context="Melanoma", notes="Synthetic fixture. Protein sequence intentionally omitted until supplied from a trusted source."),
    DrugTargetRecord(id=3, target_name="KRAS", gene_symbol="KRAS", protein_name="KRAS proto-oncogene GTPase", pathway="MAPK pathway", cancer_context="Lung adenocarcinoma", notes="Synthetic fixture. Protein sequence intentionally omitted until supplied from a trusted source."),
    DrugTargetRecord(id=4, target_name="HER2/ERBB2", gene_symbol="ERBB2", protein_name="Receptor tyrosine-protein kinase erbB-2", pathway="ERBB signaling", cancer_context="Breast cancer", notes="Synthetic fixture. Protein sequence intentionally omitted until supplied from a trusted source."),
    DrugTargetRecord(id=5, target_name="ALK", gene_symbol="ALK", protein_name="ALK receptor tyrosine kinase", pathway="ALK signaling", cancer_context="Lung adenocarcinoma", notes="Synthetic fixture. Protein sequence intentionally omitted until supplied from a trusted source."),
]

SYNTHETIC_CONTEXT_FIXTURES: list[CancerContextRecord] = [
    CancerContextRecord(id=1, cancer_type="Lung adenocarcinoma", subtype="Synthetic LUAD fixture", biomarker="EGFR / KRAS / ALK review context", pathway="RTK / MAPK signaling", notes="Synthetic research fixture; no patient data."),
    CancerContextRecord(id=2, cancer_type="Melanoma", subtype="Synthetic melanoma fixture", biomarker="BRAF pathway review context", pathway="MAPK pathway", notes="Synthetic research fixture; no patient data."),
    CancerContextRecord(id=3, cancer_type="Breast cancer", subtype="Synthetic breast cancer fixture", biomarker="HER2/ERBB2 review context", pathway="ERBB signaling", notes="Synthetic research fixture; no patient data."),
    CancerContextRecord(id=4, cancer_type="Colorectal cancer", subtype="Synthetic colorectal fixture", biomarker="KRAS pathway review context", pathway="MAPK pathway", notes="Synthetic research fixture; no patient data."),
]


COMPARISON_STORE: dict[int, dict[str, Any]] = {}
NEXT_IDS = {"drug": 6, "target": 6, "context": 5, "comparison": 1}


def fresh_drugs() -> list[DrugLibraryRecord]:
    return deepcopy(SYNTHETIC_DRUG_FIXTURES)


def fresh_targets() -> list[DrugTargetRecord]:
    return deepcopy(SYNTHETIC_TARGET_FIXTURES)


def fresh_contexts() -> list[CancerContextRecord]:
    return deepcopy(SYNTHETIC_CONTEXT_FIXTURES)
