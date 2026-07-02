from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config import get_settings
from app.drug_library import get_context, get_drug, get_target
from app.drug_scoring import score_drug_evidence


def build_comparison_matrix(comparison: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    if comparison.get("results"):
        source_rows = comparison["results"]
    else:
        source_rows = []
        for drug_id in comparison.get("drug_ids", []):
            drug = get_drug(drug_id)
            if not drug:
                continue
            targets = [get_target(target_id) for target_id in comparison.get("target_ids", [])] or [None]
            contexts = [get_context(context_id) for context_id in comparison.get("cancer_context_ids", [])] or [None]
            for target in targets:
                for context in contexts:
                    row = {
                        "drug_id": drug.id,
                        "drug_name": drug.drug_name,
                        "drug_class": drug.drug_class,
                        "drug_smiles_available": bool(drug.smiles),
                        "target_name": getattr(target, "target_name", None),
                        "cancer_context": getattr(context, "cancer_type", None),
                        "resistance_notes": drug.resistance_notes,
                        "trial_notes": drug.trial_notes,
                        "task_types": comparison.get("task_types", []),
                        "missing_data": ["completed_mammal_outputs"],
                    }
                    row["evidence_score"] = score_drug_evidence(row).model_dump()
                    source_rows.append(row)

    for row in source_rows:
        score = row.get("evidence_score") or score_drug_evidence(row).model_dump()
        rows.append(
            {
                "drug_name": row.get("drug_name"),
                "drug_class": row.get("drug_class"),
                "target": row.get("target_name"),
                "cancer_context": row.get("cancer_context"),
                "drug_smiles_available": row.get("drug_smiles_available", False),
                "cell_line_response_signal": _signal(row.get("cell_line_drug_response")),
                "drug_target_binding_signal": _signal(row.get("drug_target_interaction")),
                "carcinogenicity_signal": _signal(row.get("drug_carcinogenicity")),
                "resistance_notes": row.get("resistance_notes"),
                "evidence_support_score": score.get("evidence_support_score"),
                "data_completeness_score": score.get("data_completeness_score"),
                "overall_review_priority": score.get("overall_review_priority"),
                "missing_data": row.get("missing_data", []),
                "evidence_score": score,
            }
        )
    return {"comparison_id": comparison["comparison_id"], "comparison_name": comparison["comparison_name"], "rows": rows}


def build_comparison_report(comparison: dict[str, Any]) -> dict[str, Any]:
    matrix = build_comparison_matrix(comparison)
    lines = [
        f"# Drug Evidence Comparison: {comparison['comparison_name']}",
        "",
        "This report organizes structured MAMMAL task outputs and evidence notes. It is not a medical decision, diagnosis, prescription, or treatment recommendation.",
        "",
        "| Drug | Class | Target | Cancer context | Evidence support | Data completeness | Review priority | Missing data |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in matrix["rows"]:
        missing = ", ".join(row.get("missing_data") or []) or "None"
        lines.append(f"| {row.get('drug_name') or ''} | {row.get('drug_class') or ''} | {row.get('target') or ''} | {row.get('cancer_context') or ''} | {row.get('evidence_support_score')} | {row.get('data_completeness_score')} | {row.get('overall_review_priority')} | {missing} |")
    markdown = "\n".join(lines) + "\n"
    out = Path(get_settings().report_output_dir)
    out.mkdir(exist_ok=True)
    json_path = out / f"drug_comparison_{comparison['comparison_id']}.json"
    markdown_path = out / f"drug_comparison_{comparison['comparison_id']}.md"
    json_path.write_text(json.dumps(matrix, indent=2))
    markdown_path.write_text(markdown)
    report = {"markdown": markdown, "json": matrix, "output_paths": {"json": str(json_path), "markdown": str(markdown_path)}}
    comparison.setdefault("reports", []).append(report)
    return report


def _signal(value: Any) -> str:
    if not value:
        return "not_run"
    if isinstance(value, dict) and value.get("error"):
        return value["error"]
    return "completed_mammal_output_available"
