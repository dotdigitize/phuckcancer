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


class MammalInterpretation(BaseModel):
    interpretation_id: str
    engine: str = "MAMMAL biomedical reasoning layer"
    model_name: str
    enabled: bool
    fallback_used: bool
    findings: list[str]
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


class AssistantRequest(BaseModel):
    mode: Literal["doctor_researcher", "patient_family"]
    text: str


class ReportBundle(BaseModel):
    doctor_report_markdown: str
    family_summary_markdown: str
    audit_json: dict[str, Any]
    output_paths: dict[str, str]
