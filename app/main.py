from fastapi import FastAPI
from app.cancer_importer import import_cancer_records
from app.cbioportal_connector import CbioPortalConnector
from app.cbioportal_models import CbioPortalImportRequest
from app.cbioportal_normalizer import normalize_mutations, normalize_studies
from app.config import get_settings
from app.database import database_status
from app.evidence_matcher import match_claims_to_evidence
from app.genomics_parser import build_alteration_matrix
from app.local_llm import assistant_explain
from app.mammal_claim_extractor import extract_claims
from app.mammal_engine import MammalEngine
from app.mammal_importer import import_saved_mammal_output
from app.mammal_pipeline import run_mammal_pipeline
from app.pathway_explorer import pathway_findings
from app.reporting import build_reports, latest_reports
from app.resistance_watch import review_resistance_signal
from app.risk_flagger import flag_risks
from app.review_workflow import review_status_for_flags
from app.sample_data import cancer_records, genomic_alterations, molecular_evidence, overview
from app.trial_signal import review_trial_signal
from app.models import AssistantRequest, AuditResult

app = FastAPI(title="PhuckCancer", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "app": "PhuckCancer"}


@app.get("/api/system/status")
def system_status():
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "database": database_status(),
        "mammal": MammalEngine().status(),
        "local_llm": {"enabled": settings.enable_local_llm, "model": settings.local_llm_model},
        "medical_safety": "PhuckCancer is not a medical device, not a diagnostic system, and not a treatment recommendation engine.",
    }


@app.get("/api/sample/overview")
def sample_overview():
    return overview()


@app.get("/api/data-sources")
def data_sources():
    settings = get_settings()
    return {
        "sources": [
            {"name": "Local synthetic research fixtures", "enabled": True},
            {"name": "MariaDB database mode", "enabled": settings.enable_database},
            {"name": "cBioPortal connector", "enabled": settings.enable_cbioportal_connector, "base_url": settings.cbioportal_base_url},
        ],
        "warning": "External data may require permission, institutional access, authentication, data-use compliance, and qualified human review.",
    }


@app.get("/api/cancer-records")
def get_cancer_records():
    return cancer_records()


@app.post("/api/cancer/import")
def cancer_import(payload: list[dict]):
    return {"records": import_cancer_records(payload), "status": "imported_to_local_model"}


@app.get("/api/genomics/matrix")
def genomics_matrix():
    return build_alteration_matrix(cancer_records())


@app.get("/api/pathways")
def pathways():
    return pathway_findings()


@app.post("/api/mammal/interpret")
def mammal_interpret(payload: dict | None = None):
    evidence = molecular_evidence()
    return run_mammal_pipeline(evidence)


@app.post("/api/mammal/import")
def mammal_import(payload: dict):
    return import_saved_mammal_output(payload)


@app.post("/api/claims/extract")
def claims_extract(payload: dict):
    return extract_claims(payload.get("text", ""))


@app.post("/api/evidence/audit")
def evidence_audit(payload: dict):
    claims = extract_claims(payload.get("text", ""))
    matches = match_claims_to_evidence(claims, molecular_evidence())
    flags = flag_risks(payload.get("text", ""), has_evidence=all(m.matched_evidence for m in matches))
    return AuditResult(audit_id="audit-local-001", matches=matches, risk_flags=flags, review_status=review_status_for_flags(flags))


@app.get("/api/audits")
def audits():
    return [{"audit_id": "audit-local-001", "review_status": "needs_human_review"}]


@app.post("/api/assistant/explain")
def assistant(request: AssistantRequest):
    return assistant_explain(request.text, request.mode)


@app.post("/api/trials/review")
def trials_review(payload: dict):
    return review_trial_signal(payload)


@app.post("/api/resistance/review")
def resistance_review(payload: dict):
    return review_resistance_signal(payload)


@app.post("/api/reports/build")
def reports_build(payload: dict | None = None):
    return build_reports(payload)


@app.get("/api/reports/latest")
def reports_latest():
    return latest_reports()


@app.get("/api/cbioportal/status")
def cbioportal_status():
    return CbioPortalConnector().status()


@app.get("/api/cbioportal/studies")
async def cbioportal_studies():
    return normalize_studies(await CbioPortalConnector().studies())


@app.get("/api/cbioportal/cancer-types")
async def cbioportal_cancer_types():
    return await CbioPortalConnector().cancer_types()


@app.get("/api/cbioportal/studies/{study_id}")
async def cbioportal_study(study_id: str):
    return await CbioPortalConnector().study(study_id)


@app.get("/api/cbioportal/studies/{study_id}/sample-lists")
async def cbioportal_sample_lists(study_id: str):
    return await CbioPortalConnector().sample_lists(study_id)


@app.get("/api/cbioportal/studies/{study_id}/molecular-profiles")
async def cbioportal_molecular_profiles(study_id: str):
    return await CbioPortalConnector().molecular_profiles(study_id)


@app.post("/api/cbioportal/import")
async def cbioportal_import(request: CbioPortalImportRequest):
    connector = CbioPortalConnector(request.base_url)
    records = await connector.mutations(request.study_id, request.molecular_profile_id, request.sample_list_id, request.genes)
    normalized = normalize_mutations(records, request.study_id)
    pipeline = run_mammal_pipeline([ev for record in normalized for ev in record.evidence])
    return {"normalized_records": normalized, "mammal_pipeline": pipeline, "last_import_summary": f"Imported {len(normalized)} normalized records for review."}


@app.post("/api/cbioportal/import/mutations")
async def cbioportal_import_mutations(request: CbioPortalImportRequest):
    return await cbioportal_import(request)
