from __future__ import annotations

from typing import Any

from app.models import DrugEvidenceScore


def _has_output(result: dict[str, Any], task_type: str) -> bool:
    task = result.get(task_type)
    return isinstance(task, dict) and bool(task.get("raw_mammal_output") or task.get("structured_output") or task.get("result"))


def _numeric_signal(result: dict[str, Any], task_type: str) -> float | None:
    task = result.get(task_type)
    if not isinstance(task, dict):
        return None
    for key in ("score", "prediction", "response_score", "binding_score", "normalized_score"):
        value = task.get(key)
        if isinstance(value, (int, float)):
            return max(0.0, min(1.0, float(value)))
    return 0.5 if _has_output(result, task_type) else None


def score_drug_evidence(row: dict[str, Any]) -> DrugEvidenceScore:
    missing = row.get("missing_data") or []
    response = _numeric_signal(row, "cell_line_drug_response")
    binding = _numeric_signal(row, "drug_target_interaction")
    carcinogenicity_output = row.get("drug_carcinogenicity")
    carcinogenicity_flag = bool(isinstance(carcinogenicity_output, dict) and str(carcinogenicity_output).lower().find("carcinogenic") >= 0)
    resistance_flag = bool(str(row.get("resistance_notes") or "").strip())
    completed_tasks = sum(1 for task in ("cell_line_drug_response", "drug_target_interaction", "drug_carcinogenicity") if _has_output(row, task))
    expected_tasks = max(1, len(row.get("task_types") or []))
    data_completeness = completed_tasks / expected_tasks

    if missing or completed_tasks == 0:
        return DrugEvidenceScore(
            response_signal_score=response,
            binding_signal_score=binding,
            carcinogenicity_flag=carcinogenicity_flag,
            resistance_flag=resistance_flag,
            evidence_support_score=None,
            data_completeness_score=round(data_completeness, 3),
            uncertainty_score=1.0,
            overall_review_priority="insufficient_data",
            explanation_summary="Insufficient structured MAMMAL outputs or required inputs are available for evidence organization scoring.",
        )

    available_scores = [score for score in (response, binding) if score is not None]
    evidence_support = sum(available_scores) / len(available_scores) if available_scores else data_completeness
    uncertainty = max(0.0, 1.0 - data_completeness)
    if data_completeness >= 0.75 and evidence_support >= 0.6:
        priority = "high_review_priority"
    elif data_completeness >= 0.5:
        priority = "medium_review_priority"
    else:
        priority = "low_review_priority"
    return DrugEvidenceScore(
        response_signal_score=response,
        binding_signal_score=binding,
        carcinogenicity_flag=carcinogenicity_flag,
        resistance_flag=resistance_flag,
        evidence_support_score=round(evidence_support, 3),
        data_completeness_score=round(data_completeness, 3),
        uncertainty_score=round(uncertainty, 3),
        overall_review_priority=priority,
        explanation_summary="Evidence organization score based only on completed structured task outputs and stored evidence notes; it is not a treatment recommendation.",
    )
