from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.assistant_prompts import validate_user_role
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
from app.mammal_providers import MammalUnavailableError
from app.pathway_explorer import pathway_findings
from app.reporting import build_reports, latest_reports
from app.resistance_watch import review_resistance_signal
from app.risk_flagger import flag_risks
from app.review_workflow import review_status_for_flags
from app.sample_data import cancer_records, genomic_alterations, molecular_evidence, overview
from app.trial_signal import review_trial_signal
from app.models import AssistantRequest, AuditResult, UserRoleRequest

app = FastAPI(title="PhuckCancer", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "app": "PhuckCancer"}


@app.get("/api/system/status")
def system_status():
    settings = get_settings()
    db_status = database_status()
    mammal_status = MammalEngine().status()
    return {
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "backend_port": settings.backend_port,
        "frontend_port": settings.frontend_port,
        "database_enabled": settings.enable_database,
        "database_provider": "mariadb",
        "database_available": db_status.get("available", False),
        "database": db_status,
        "mammal_required": settings.mammal_required,
        "mammal_provider": settings.mammal_provider,
        "mammal_available": mammal_status.get("available", False),
        "mammal_model_name": settings.mammal_model_name,
        "mammal_device": settings.mammal_device,
        "mammal_api_configured": bool(settings.mammal_api_base_url),
        "mammal": mammal_status,
        "local_llm_enabled": settings.enable_local_llm,
        "local_llm": {"enabled": settings.enable_local_llm, "model": settings.local_llm_model},
        "cbioportal_connector_enabled": settings.enable_cbioportal_connector,
        "medical_safety": "PhuckCancer is not a medical device, not a diagnostic system, and not a treatment recommendation engine.",
    }


@app.get("/api/sample/overview")
def sample_overview():
    return overview()


@app.get("/api/data-sources")
def data_sources():
    settings = get_settings()
    db_status = database_status()
    return {
        "sources": [
            {"name": "Local synthetic research fixtures", "enabled": True},
            {"name": "MariaDB database mode", "enabled": settings.enable_database, "available": db_status.get("available", False)},
            {"name": "cBioPortal connector", "enabled": settings.enable_cbioportal_connector, "base_url": settings.cbioportal_base_url},
        ],
        "configured_api_base_url": settings.cbioportal_base_url,
        "available_studies": [] if not settings.enable_cbioportal_connector else "Use /api/cbioportal/studies after connector setup.",
        "last_import_summary": "No external import has run in this session.",
        "warning": "External data may require permission, institutional access, authentication, data-use compliance, and qualified human review.",
    }


@app.get("/api/database/status")
def database_status_endpoint():
    return database_status()


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
    evidence = payload.get("evidence") if isinstance(payload, dict) and payload.get("evidence") else molecular_evidence()
    try:
        return run_mammal_pipeline(evidence)
    except MammalUnavailableError:
        return JSONResponse(
            status_code=503,
            content={
                "error": "mammal_unavailable",
                "message": "MAMMAL is required for biomedical interpretation. Configure local MAMMAL or a MAMMAL API provider.",
            },
        )


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


@app.post("/api/user-role/validate")
def user_role_validate(request: UserRoleRequest):
    if not validate_user_role(request.user_role):
        return JSONResponse(status_code=400, content={"error": "invalid_user_role", "message": "Unsupported user role."})
    return {"valid": True, "user_role": request.user_role}


@app.post("/api/assistant/explain")
def assistant(request: AssistantRequest):
    if not request.user_role:
        return JSONResponse(status_code=400, content={"error": "user_role_required", "message": "Choose a user type before generating an explanation."})
    if not any([request.source_text, request.report_text, request.audit_id, request.mammal_interpretation]):
        return JSONResponse(status_code=400, content={"error": "source_required", "message": "Provide source_text, report_text, audit_id, or mammal_interpretation."})
    return assistant_explain(request)


@app.post("/api/trials/review")
def trials_review(payload: dict):
    return review_trial_signal(payload)


@app.post("/api/resistance/review")
def resistance_review(payload: dict):
    return review_resistance_signal(payload)


@app.post("/api/reports/build")
def reports_build(payload: dict | None = None):
    if payload and payload.get("report_type") in {"doctor", "family"} and not validate_user_role(payload.get("user_role")):
        return JSONResponse(status_code=400, content={"error": "user_role_required", "message": "Choose a user type before building this report."})
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
    try:
        pipeline = run_mammal_pipeline([ev for record in normalized for ev in record.evidence])
    except MammalUnavailableError:
        return JSONResponse(
            status_code=503,
            content={
                "error": "mammal_unavailable",
                "message": "MAMMAL is required for biomedical interpretation. Configure local MAMMAL or a MAMMAL API provider.",
            },
        )
    return {"normalized_records": normalized, "mammal_pipeline": pipeline, "last_import_summary": f"Imported {len(normalized)} normalized records for review."}


@app.post("/api/cbioportal/import/mutations")
async def cbioportal_import_mutations(request: CbioPortalImportRequest):
    return await cbioportal_import(request)
