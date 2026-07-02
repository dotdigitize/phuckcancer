from __future__ import annotations

from typing import Any

from app.drug_evidence_models import COMPARISON_STORE, NEXT_IDS, fresh_contexts, fresh_drugs, fresh_targets, utc_now
from app.models import CancerContextRecord, DrugComparisonCreateRequest, DrugLibraryRecord, DrugTargetRecord

DRUGS: list[DrugLibraryRecord] = fresh_drugs()
TARGETS: list[DrugTargetRecord] = fresh_targets()
CONTEXTS: list[CancerContextRecord] = fresh_contexts()


def _matches_query(value: Any, query: str) -> bool:
    if not query:
        return True
    return query.lower() in str(value).lower()


def list_drugs(search: str = "") -> list[DrugLibraryRecord]:
    return [drug for drug in DRUGS if _matches_query(drug.model_dump(), search)]


def get_drug(drug_id: int) -> DrugLibraryRecord | None:
    return next((drug for drug in DRUGS if drug.id == drug_id), None)


def create_drug(record: DrugLibraryRecord) -> DrugLibraryRecord:
    now = utc_now()
    record.id = NEXT_IDS["drug"]
    NEXT_IDS["drug"] += 1
    record.created_at = record.created_at or now
    record.updated_at = now
    DRUGS.append(record)
    return record


def update_drug(drug_id: int, record: DrugLibraryRecord) -> DrugLibraryRecord | None:
    existing = get_drug(drug_id)
    if not existing:
        return None
    updated = record.model_copy(update={"id": drug_id, "created_at": existing.created_at, "updated_at": utc_now()})
    DRUGS[DRUGS.index(existing)] = updated
    return updated


def list_targets(search: str = "") -> list[DrugTargetRecord]:
    return [target for target in TARGETS if _matches_query(target.model_dump(), search)]


def get_target(target_id: int) -> DrugTargetRecord | None:
    return next((target for target in TARGETS if target.id == target_id), None)


def create_target(record: DrugTargetRecord) -> DrugTargetRecord:
    now = utc_now()
    record.id = NEXT_IDS["target"]
    NEXT_IDS["target"] += 1
    record.created_at = record.created_at or now
    record.updated_at = now
    TARGETS.append(record)
    return record


def list_contexts(search: str = "") -> list[CancerContextRecord]:
    return [context for context in CONTEXTS if _matches_query(context.model_dump(), search)]


def get_context(context_id: int) -> CancerContextRecord | None:
    return next((context for context in CONTEXTS if context.id == context_id), None)


def create_context(record: CancerContextRecord) -> CancerContextRecord:
    now = utc_now()
    record.id = NEXT_IDS["context"]
    NEXT_IDS["context"] += 1
    record.created_at = record.created_at or now
    record.updated_at = now
    CONTEXTS.append(record)
    return record


def create_comparison(request: DrugComparisonCreateRequest) -> dict[str, Any]:
    comparison_id = NEXT_IDS["comparison"]
    NEXT_IDS["comparison"] += 1
    now = utc_now()
    comparison = {
        "comparison_id": comparison_id,
        "comparison_name": request.comparison_name,
        "drug_ids": request.drug_ids,
        "target_ids": request.target_ids,
        "cancer_context_ids": request.cancer_context_ids,
        "task_types": request.task_types,
        "cell_line_names": request.cell_line_names,
        "h5ad_file_refs": request.h5ad_file_refs,
        "notes": request.notes,
        "status": "prepared",
        "created_at": now,
        "updated_at": now,
        "items": [],
        "results": [],
        "scores": [],
        "reports": [],
    }
    COMPARISON_STORE[comparison_id] = comparison
    return comparison


def list_comparisons() -> list[dict[str, Any]]:
    return list(COMPARISON_STORE.values())


def get_comparison(comparison_id: int) -> dict[str, Any] | None:
    return COMPARISON_STORE.get(comparison_id)
