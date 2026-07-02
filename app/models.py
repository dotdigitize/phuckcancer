from typing import Any, Literal
from pydantic import BaseModel, Field

SupportStatus = Literal["supported", "partially_supported", "unsupported", "contradicted", "missing_evidence", "needs_human_review"]
ReviewStatus = Literal["pending", "needs_human_review", "reviewed", "escalated"]
DrugComparisonTaskType = Literal["cell_line_drug_response", "drug_target_interaction", "drug_carcinogenicity", "protein_protein_interaction"]
ReviewPriority = Literal["high_review_priority", "medium_review_priority", "low_review_priority", "insufficient_data"]


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
    base_model_id: str | None = None
    tokenizer_id: str | None = None
    checkpoint_source: str | None = None
    checkpoint_model_id: str | None = None
    checkpoint_path: str | None = None
    model_path: str | None = None
    norm_y_mean: float | None = None
    norm_y_std: float | None = None
    official_example_script: str | None = None
    hf_model_url: str | None = None
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


class DrugLibraryRecord(BaseModel):
    id: int | None = None
    drug_name: str
    brand_names: list[str] = Field(default_factory=list)
    drug_class: str | None = None
    mechanism_summary: str | None = None
    smiles: str | None = None
    known_targets: list[str] = Field(default_factory=list)
    cancer_contexts: list[str] = Field(default_factory=list)
    resistance_notes: str | None = None
    trial_notes: str | None = None
    evidence_notes: str | None = None
    source_label: str = "Synthetic research fixture"
    source_url: str | None = None
    synthetic_fixture: bool = True
    created_at: str | None = None
    updated_at: str | None = None


class DrugTargetRecord(BaseModel):
    id: int | None = None
    target_name: str
    gene_symbol: str | None = None
    protein_name: str | None = None
    protein_sequence: str | None = None
    pathway: str | None = None
    cancer_context: str | None = None
    notes: str | None = None
    source_label: str = "Synthetic research fixture"
    synthetic_fixture: bool = True
    created_at: str | None = None
    updated_at: str | None = None


class CancerContextRecord(BaseModel):
    id: int | None = None
    cancer_type: str
    subtype: str | None = None
    biomarker: str | None = None
    pathway: str | None = None
    notes: str | None = None
    synthetic_fixture: bool = True
    created_at: str | None = None
    updated_at: str | None = None


class DrugComparisonCreateRequest(BaseModel):
    comparison_name: str
    drug_ids: list[int] = Field(default_factory=list)
    target_ids: list[int] = Field(default_factory=list)
    cancer_context_ids: list[int] = Field(default_factory=list)
    task_types: list[DrugComparisonTaskType] = Field(default_factory=list)
    cell_line_names: list[str] = Field(default_factory=list)
    h5ad_file_refs: list[str] = Field(default_factory=list)
    notes: str | None = None


class DrugComparisonRunRequest(BaseModel):
    task_types: list[DrugComparisonTaskType] | None = None
    cell_line_names: list[str] | None = None
    h5ad_file_refs: list[str] | None = None


class DrugComparisonExplainRequest(BaseModel):
    user_role: UserRole | None = None


class DrugEvidenceScore(BaseModel):
    response_signal_score: float | None = None
    binding_signal_score: float | None = None
    carcinogenicity_flag: bool = False
    resistance_flag: bool = False
    evidence_support_score: float | None = None
    data_completeness_score: float = 0.0
    uncertainty_score: float = 1.0
    overall_review_priority: ReviewPriority = "insufficient_data"
    explanation_summary: str
