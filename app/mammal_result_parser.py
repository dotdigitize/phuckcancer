from __future__ import annotations

import re
from typing import Any


NUMBER_RE = re.compile(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?")


def _first_number(text: str) -> float | None:
    match = NUMBER_RE.search(text)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def normalize_mammal_task_result(task_type: str, inputs: dict[str, Any], raw_output: dict[str, Any]) -> dict[str, Any]:
    stdout = str(raw_output.get("stdout") or raw_output.get("output") or raw_output)
    value = _first_number(stdout)
    base = {
        "task_type": task_type,
        "raw_mammal_output": raw_output,
        "uncertainty": "Review raw MAMMAL output and checkpoint provenance before using this research signal.",
        "review_questions": [
            "Was the correct official MAMMAL task/checkpoint used?",
            "Are the biological inputs complete, sourced, and appropriate for this model?",
            "Does a qualified biomedical reviewer agree with the interpretation of this signal?",
        ],
    }
    if task_type == "cell_line_drug_response":
        return {
            **base,
            "drug_name": inputs.get("drug_name"),
            "drug_smiles": inputs.get("drug_smiles"),
            "cell_line_name": inputs.get("cell_line_name"),
            "cell_line_h5ad_file": inputs.get("cell_line_h5ad_file"),
            "predicted_ic50_or_response_signal": value if value is not None else stdout.strip(),
        }
    if task_type == "drug_target_interaction":
        return {
            **base,
            "target_name": inputs.get("target_name"),
            "drug_name": inputs.get("drug_name"),
            "predicted_pkd_or_binding_affinity": value if value is not None else stdout.strip(),
            "binding_signal": stdout.strip(),
        }
    if task_type == "drug_carcinogenicity":
        return {
            **base,
            "drug_name": inputs.get("drug_name"),
            "drug_smiles": inputs.get("drug_smiles"),
            "carcinogenicity_signal": stdout.strip(),
            "classification_score": value,
        }
    if task_type == "protein_protein_interaction":
        return {**base, "interaction_signal": stdout.strip()}
    if task_type == "protein_solubility":
        return {**base, "solubility_signal": stdout.strip()}
    if task_type == "tcr_epitope_binding":
        return {**base, "binding_signal": stdout.strip()}
    return base
