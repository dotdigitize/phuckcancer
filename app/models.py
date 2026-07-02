from typing import Any, Literal
from pydantic import BaseModel, Field

SupportStatus = Literal["supported", "partially_supported", "unsupported", "contradicted", "missing_evidence", "needs_human_review"]
ReviewStatus = Literal["pending", "needs_human_review", "reviewed", "escalated"]


class GenomicAlteration(BaseModel):
    gene: str
    sample_id: str
    cancer_type: str
    alteration_type: str
    variant: str | None = None
    mutation_class: str | None = None
    copy_number_alteration: str | None = None
    expression_signal: str | None = None
    pathway: str


class MolecularEvidence(BaseModel):
    evidence_id: str
    gene: str
    cancer_type: str
    evidence_type: str
    summary: str
    source: str
    confidence_note: str
    support_status: SupportStatus = "needs_human_review"


class CancerRecord(BaseModel):
    record_id: str
    study: str
    cancer_type: str
    sample_group: str
    alterations: list[GenomicAlteration] = Field(default_factory=list)
    evidence: list[MolecularEvidence] = Field(default_factory=list)
    human_review_status: ReviewStatus = "needs_human_review"


class PathwayFinding(BaseModel):
    pathway: str
    altered_genes: list[str]
    evidence_notes: list[str]
    mammal_interpretation: str
    support_score: float
    risk_flags: list[str]
    human_review_recommendation: str


MammalProviderMode = Literal["local", "api", "mcp_http", "official_script"]
MammalOfficialTaskType = Literal[
    "cell_line_drug_response",
    "drug_target_interaction",
    "drug_carcinogenicity",
    "protein_protein_interaction",
    "protein_solubility",
    "tcr_epitope_binding",
]


class MammalInterpretation(BaseModel):
    interpretation_id: str
    engine: str = "MAMMAL biomedical reasoning layer"
    model_name: str
    provider: MammalProviderMode
    biological_interpretation: str
    molecular_signal: str
    pathway_context: str
    evidence_strength: str
    uncertainty: str
    review_questions: list[str]
    raw_mammal_output: dict[str, Any]
    interpretation: str
    claims: list[str] = Field(default_factory=list)


class ExtractedClaim(BaseModel):
    claim_id: str
    text: str
    gene: str | None = None
    pathway: str | None = None
    source: str = "mammal_output"


class EvidenceMatch(BaseModel):
    claim: ExtractedClaim
    matched_evidence: list[MolecularEvidence]
    support_status: SupportStatus
    support_score: float
    rationale: str


class AuditResult(BaseModel):
    audit_id: str
    matches: list[EvidenceMatch]
    risk_flags: list[str]
    review_status: ReviewStatus


UserRole = Literal["patient_family", "doctor_tumor_board", "cancer_researcher", "data_engineer"]


class AssistantRequest(BaseModel):
    user_role: UserRole | None = None
    source_text: str | None = None
    report_text: str | None = None
    audit_id: str | None = None
    mammal_interpretation: dict[str, Any] | None = None
    evidence_audit: dict[str, Any] | None = None
    risk_flags: list[str] = Field(default_factory=list)
    source_notes: list[str] = Field(default_factory=list)
    safety_constraints: list[str] = Field(default_factory=list)


class MammalModelRegistryEntry(BaseModel):
    id: int | None = None
    task_type: MammalOfficialTaskType
    provider: MammalProviderMode = "official_script"
    model_path: str | None = None
    norm_y_mean: float | None = None
    norm_y_std: float | None = None
    enabled: bool = True
    notes: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class CellLineDrugResponseRequest(BaseModel):
    model_path: str | None = None
    cell_line_name: str | None = None
    cell_line_h5ad_file: str | None = None
    drug_smiles: str | None = None
    drug_name: str | None = None


class DrugTargetInteractionRequest(BaseModel):
    model_path: str | None = None
    target_protein_sequence: str | None = None
    drug_smiles: str | None = None
    norm_y_mean: float | None = None
    norm_y_std: float | None = None
    target_name: str | None = None
    drug_name: str | None = None
    cancer_context: str | None = None


class DrugCarcinogenicityRequest(BaseModel):
    model_path: str | None = None
    drug_smiles: str | None = None
    drug_name: str | None = None


class ProteinProteinInteractionRequest(BaseModel):
    protein_a_sequence: str | None = None
    protein_a_name: str | None = None
    protein_b_sequence: str | None = None
    protein_b_name: str | None = None


class ProteinSolubilityRequest(BaseModel):
    model_path: str | None = None
    protein_sequence: str | None = None
    protein_name: str | None = None


class TcrEpitopeBindingRequest(BaseModel):
    tcr_sequence: str | None = None
    epitope_sequence: str | None = None
    cancer_context: str | None = None


class MammalTaskExplainRequest(BaseModel):
    user_role: UserRole | None = None
    task_result: dict[str, Any] | None = None


class UserRoleRequest(BaseModel):
    user_role: UserRole | None = None


class ReportBundle(BaseModel):
    doctor_report_markdown: str
    family_summary_markdown: str
    audit_json: dict[str, Any]
    output_paths: dict[str, str]
