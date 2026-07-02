from __future__ import annotations

from typing import Any

from app.config import get_settings
from app.drug_library import get_context, get_drug, get_target
from app.drug_scoring import score_drug_evidence
from app.mammal_providers import MammalConfigurationError, MammalUnavailableError
from app.mammal_task_runner import MammalScriptUnavailableError, MissingStructuredDataError, run_mammal_task
from app.models import DrugComparisonRunRequest


def _has_text(value: Any) -> bool:
    return bool(str(value).strip()) if value is not None else False


def _missing_for_task(task_type: str, drug: Any, target: Any, run_options: dict[str, Any]) -> list[str]:
    settings = get_settings()
    missing: list[str] = []
    if task_type in {"cell_line_drug_response", "drug_target_interaction", "drug_carcinogenicity"} and not _has_text(drug.smiles):
        missing.append("drug_smiles")
    if task_type == "cell_line_drug_response":
        if not _has_text(settings.mammal_cell_line_drug_response_model_path):
            missing.append("model_path")
        if not (run_options.get("cell_line_names") or run_options.get("h5ad_file_refs")):
            missing.append("cell_line_name_or_cell_line_h5ad_file")
    if task_type == "drug_target_interaction":
        if target is None:
            missing.append("target")
        elif not _has_text(target.protein_sequence):
            missing.append("target_protein_sequence")
        if not _has_text(settings.mammal_dti_model_path):
            missing.append("model_path")
        if not _has_text(settings.mammal_dti_norm_y_mean):
            missing.append("norm_y_mean")
        if not _has_text(settings.mammal_dti_norm_y_std):
            missing.append("norm_y_std")
    if task_type == "drug_carcinogenicity" and not _has_text(settings.mammal_carcinogenicity_model_path):
        missing.append("model_path")
    if task_type == "protein_protein_interaction":
        if target is None:
            missing.append("target")
        elif not (_has_text(target.protein_sequence) or _has_text(target.target_name)):
            missing.append("protein_a_name_or_sequence")
    return missing


def comparison_requirements(comparison: dict[str, Any], override: DrugComparisonRunRequest | None = None) -> dict[str, Any]:
    run_options = {
        "cell_line_names": override.cell_line_names if override and override.cell_line_names is not None else comparison.get("cell_line_names", []),
        "h5ad_file_refs": override.h5ad_file_refs if override and override.h5ad_file_refs is not None else comparison.get("h5ad_file_refs", []),
    }
    task_types = override.task_types if override and override.task_types is not None else comparison.get("task_types", [])
    missing: list[dict[str, Any]] = []
    for drug_id in comparison.get("drug_ids", []):
        drug = get_drug(drug_id)
        if not drug:
            missing.append({"drug_id": drug_id, "task_type": "comparison", "missing_fields": ["drug"]})
            continue
        targets = [get_target(target_id) for target_id in comparison.get("target_ids", [])] or [None]
        for task_type in task_types:
            for target in targets:
                fields = _missing_for_task(task_type, drug, target, run_options)
                if fields:
                    missing.append({"drug_id": drug_id, "drug_name": drug.drug_name, "target_id": getattr(target, "id", None), "target_name": getattr(target, "target_name", None), "task_type": task_type, "missing_fields": fields})
    return {"missing_structured_data": missing, "ready": not missing}


def _task_payload(task_type: str, drug: Any, target: Any, run_options: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    if task_type == "cell_line_drug_response":
        payload = {"model_path": settings.mammal_cell_line_drug_response_model_path, "drug_smiles": drug.smiles, "drug_name": drug.drug_name}
        if run_options.get("h5ad_file_refs"):
            payload["cell_line_h5ad_file"] = run_options["h5ad_file_refs"][0]
        else:
            payload["cell_line_name"] = run_options["cell_line_names"][0]
        return payload
    if task_type == "drug_target_interaction":
        return {
            "model_path": settings.mammal_dti_model_path,
            "drug_smiles": drug.smiles,
            "drug_name": drug.drug_name,
            "target_protein_sequence": target.protein_sequence,
            "target_name": target.target_name,
            "norm_y_mean": float(settings.mammal_dti_norm_y_mean),
            "norm_y_std": float(settings.mammal_dti_norm_y_std),
        }
    if task_type == "drug_carcinogenicity":
        return {"model_path": settings.mammal_carcinogenicity_model_path, "drug_smiles": drug.smiles, "drug_name": drug.drug_name}
    if task_type == "protein_protein_interaction":
        return {"protein_a_name": drug.drug_name, "protein_b_sequence": target.protein_sequence, "protein_b_name": target.target_name}
    return {}


def run_comparison_batch(comparison: dict[str, Any], override: DrugComparisonRunRequest | None = None) -> dict[str, Any]:
    requirements = comparison_requirements(comparison, override)
    if not requirements["ready"]:
        comparison["status"] = "missing_structured_data"
        comparison["missing_structured_data"] = requirements["missing_structured_data"]
        return {"error": "missing_structured_data", **requirements, "comparison": comparison}

    run_options = {
        "cell_line_names": override.cell_line_names if override and override.cell_line_names is not None else comparison.get("cell_line_names", []),
        "h5ad_file_refs": override.h5ad_file_refs if override and override.h5ad_file_refs is not None else comparison.get("h5ad_file_refs", []),
    }
    task_types = override.task_types if override and override.task_types is not None else comparison.get("task_types", [])
    results: list[dict[str, Any]] = []
    for drug_id in comparison.get("drug_ids", []):
        drug = get_drug(drug_id)
        if not drug:
            continue
        targets = [get_target(target_id) for target_id in comparison.get("target_ids", [])] or [None]
        contexts = [get_context(context_id) for context_id in comparison.get("cancer_context_ids", [])] or [None]
        for target in targets:
            for context in contexts:
                row: dict[str, Any] = {
                    "drug_id": drug.id,
                    "drug_name": drug.drug_name,
                    "drug_class": drug.drug_class,
                    "drug_smiles_available": _has_text(drug.smiles),
                    "target_id": getattr(target, "id", None),
                    "target_name": getattr(target, "target_name", None),
                    "cancer_context": getattr(context, "cancer_type", None),
                    "resistance_notes": drug.resistance_notes,
                    "trial_notes": drug.trial_notes,
                    "task_types": task_types,
                    "missing_data": [],
                }
                for task_type in task_types:
                    payload = _task_payload(task_type, drug, target, run_options)
                    try:
                        row[task_type] = run_mammal_task(task_type, payload)
                    except MissingStructuredDataError as exc:
                        row["missing_data"].extend(exc.missing_fields)
                    except (MammalConfigurationError, MammalUnavailableError, MammalScriptUnavailableError) as exc:
                        return {"error": "mammal_unavailable", "message": str(exc), "comparison": comparison}
                row["evidence_score"] = score_drug_evidence(row).model_dump()
                results.append(row)
    comparison["status"] = "completed"
    comparison["results"] = results
    comparison["scores"] = [row["evidence_score"] for row in results]
    return {"status": "completed", "comparison": comparison, "results": results}
