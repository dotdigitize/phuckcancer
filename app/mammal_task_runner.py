from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from app.config import Settings, get_settings
from app.mammal_checkpoint_config import validate_model_path
from app.mammal_mcp_client import MammalMcpClient
from app.mammal_official_tasks import OFFICIAL_MAMMAL_TASKS
from app.mammal_prompt_builder import build_protein_interaction_prompt
from app.mammal_providers import MammalConfigurationError, MammalInferenceError, get_mammal_provider
from app.mammal_result_parser import normalize_mammal_task_result
from app.mammal_task_router import provider_for_task


class MissingStructuredDataError(ValueError):
    def __init__(self, missing_fields: list[str]):
        super().__init__("missing_structured_data")
        self.missing_fields = missing_fields


class MammalScriptUnavailableError(MammalConfigurationError):
    pass


SCRIPT_TASKS = {
    "cell_line_drug_response": "mammal/examples/cell_line_drug_response/main_infer.py",
    "drug_target_interaction": "mammal/examples/dti_bindingdb_kd/main_infer.py",
    "drug_carcinogenicity": "mammal/examples/carcinogenicity/main_infer.py",
    "protein_solubility": "mammal/examples/protein_solubility/main_infer.py",
}


def _has_text(value: Any) -> bool:
    return bool(str(value).strip()) if value is not None else False


def _checkpoint_path(payload: dict[str, Any]) -> Any:
    return payload.get("checkpoint_path") or payload.get("model_path")


def validate_task_inputs(task_type: str, payload: dict[str, Any]) -> None:
    missing: list[str] = []
    if task_type == "cell_line_drug_response":
        for field in ("drug_smiles", "drug_name"):
            if not _has_text(payload.get(field)):
                missing.append(field)
        if not _has_text(_checkpoint_path(payload)):
            missing.append("model_path")
        if not (_has_text(payload.get("cell_line_name")) or _has_text(payload.get("cell_line_h5ad_file"))):
            missing.append("cell_line_name_or_cell_line_h5ad_file")
    elif task_type == "drug_target_interaction":
        for field in ("target_protein_sequence", "drug_smiles", "norm_y_mean", "norm_y_std"):
            if not _has_text(payload.get(field)):
                missing.append(field)
        if not _has_text(_checkpoint_path(payload)):
            missing.append("model_path")
    elif task_type == "drug_carcinogenicity":
        if not _has_text(_checkpoint_path(payload)):
            missing.append("model_path")
        if not _has_text(payload.get("drug_smiles")):
            missing.append("drug_smiles")
    elif task_type == "protein_protein_interaction":
        if not (_has_text(payload.get("protein_a_name")) or _has_text(payload.get("protein_a_sequence"))):
            missing.append("protein_a_name_or_sequence")
        if not (_has_text(payload.get("protein_b_name")) or _has_text(payload.get("protein_b_sequence"))):
            missing.append("protein_b_name_or_sequence")
    elif task_type == "protein_solubility":
        if not _has_text(_checkpoint_path(payload)):
            missing.append("model_path")
        if not (_has_text(payload.get("protein_name")) or _has_text(payload.get("protein_sequence"))):
            missing.append("protein_name_or_sequence")
    elif task_type == "tcr_epitope_binding":
        for field in ("tcr_sequence", "epitope_sequence"):
            if not _has_text(payload.get(field)):
                missing.append(field)
    else:
        missing.append("task_type")
    if missing:
        raise MissingStructuredDataError(missing)


def _script_path(task_type: str, settings: Settings) -> Path:
    relative_path = SCRIPT_TASKS.get(task_type)
    if not relative_path:
        raise MammalScriptUnavailableError("mammal_script_unavailable")
    repo_path = Path(settings.mammal_repo_path).expanduser().resolve()
    script_path = (repo_path / relative_path).resolve()
    if not script_path.is_relative_to(repo_path) or relative_path not in SCRIPT_TASKS.values():
        raise MammalScriptUnavailableError("mammal_script_unavailable")
    if not script_path.exists():
        raise MammalScriptUnavailableError("mammal_script_unavailable")
    return script_path


def _official_script_args(task_type: str, payload: dict[str, Any], settings: Settings) -> list[str]:
    script = _script_path(task_type, settings)
    if task_type in SCRIPT_TASKS:
        payload = {**payload, "model_path": validate_model_path(_checkpoint_path(payload), settings)}
    if task_type == "cell_line_drug_response":
        args = ["python", str(script), "--model_path", payload["model_path"]]
        if _has_text(payload.get("cell_line_h5ad_file")):
            args.extend(["--cell_line_h5ad_file", str(Path(payload["cell_line_h5ad_file"]).expanduser().resolve())])
        else:
            args.extend(["--cell_line_name", str(payload["cell_line_name"])])
        args.extend(["--drug_smiles", str(payload["drug_smiles"]), "--drug_name", str(payload["drug_name"])])
        return args
    if task_type == "drug_target_interaction":
        return [
            "python",
            str(script),
            str(payload["model_path"]),
            str(payload["target_protein_sequence"]),
            str(payload["drug_smiles"]),
            str(payload["norm_y_mean"]),
            str(payload["norm_y_std"]),
        ]
    if task_type == "drug_carcinogenicity":
        return ["python", str(script), str(payload["model_path"]), str(payload["drug_smiles"])]
    if task_type == "protein_solubility":
        protein = payload.get("protein_sequence") or payload.get("protein_name")
        return ["python", str(script), str(payload["model_path"]), str(protein)]
    raise MammalScriptUnavailableError("mammal_script_unavailable")


def run_official_script_task(task_type: str, payload: dict[str, Any], settings: Settings | None = None) -> dict:
    settings = settings or get_settings()
    args = _official_script_args(task_type, payload, settings)
    try:
        completed = subprocess.run(args, shell=False, capture_output=True, text=True, timeout=settings.mammal_script_timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        raise MammalInferenceError("MAMMAL official script timed out.") from exc
    if completed.returncode != 0:
        raise MammalInferenceError("MAMMAL official script failed.")
    return normalize_mammal_task_result(
        task_type,
        payload,
        {"provider": "official_script", "command": args[:2], "stdout": completed.stdout, "stderr": completed.stderr, "returncode": completed.returncode},
    )


def run_mammal_task(task_type: str, payload: dict[str, Any], provider: str | None = None) -> dict:
    settings = get_settings()
    if task_type not in OFFICIAL_MAMMAL_TASKS:
        raise MammalConfigurationError("unsupported_mammal_task")
    validate_task_inputs(task_type, payload)
    selected_provider = provider_for_task(task_type, provider, settings)
    if selected_provider == "official_script":
        return run_official_script_task(task_type, payload, settings)
    if selected_provider == "mcp_http":
        raw = MammalMcpClient(settings).run_task(task_type, payload)
        return normalize_mammal_task_result(task_type, payload, {"provider": "mcp_http", "output": raw})
    if selected_provider == "api":
        raw = get_mammal_provider(settings).interpret({"task_type": task_type, "inputs": payload})
        return normalize_mammal_task_result(task_type, payload, {"provider": "api", "output": raw})
    if selected_provider == "local" and task_type == "protein_protein_interaction":
        prompt = build_protein_interaction_prompt(payload)
        raw = get_mammal_provider(settings).interpret({"task_type": task_type, "structured_prompt": prompt, "inputs": payload})
        return normalize_mammal_task_result(task_type, payload, {"provider": "local", "structured_prompt": prompt, "output": raw})
    raise MammalConfigurationError(f"{selected_provider} is not supported for {task_type}.")
