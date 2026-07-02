from __future__ import annotations

from pathlib import Path

from app.config import Settings, get_settings
from app.mammal_official_tasks import OFFICIAL_MAMMAL_TASKS
from app.mammal_providers import MammalConfigurationError


def configured_allowed_model_dirs(settings: Settings | None = None) -> list[Path]:
    settings = settings or get_settings()
    return [Path(item).expanduser().resolve() for item in settings.mammal_allowed_model_dirs.split(",") if item.strip()]


def validate_model_path(model_path: str | None, settings: Settings | None = None) -> str:
    if not model_path or not str(model_path).strip():
        raise MammalConfigurationError("mammal_model_path_required")
    path = Path(str(model_path)).expanduser().resolve()
    allowed_dirs = configured_allowed_model_dirs(settings)
    if allowed_dirs and not any(path == allowed or path.is_relative_to(allowed) for allowed in allowed_dirs):
        raise MammalConfigurationError("mammal_model_path_not_allowed")
    if not path.exists():
        raise MammalConfigurationError("mammal_model_path_required")
    return str(path)


def task_requires_fine_tuned_checkpoint(task_type: str) -> bool:
    task = OFFICIAL_MAMMAL_TASKS.get(task_type)
    return bool(task and task.requires_fine_tuned_checkpoint)


def task_requires_normalization(task_type: str) -> bool:
    task = OFFICIAL_MAMMAL_TASKS.get(task_type)
    return bool(task and task.requires_normalization)


def configured_checkpoint_path_for_task(task_type: str, settings: Settings | None = None) -> str:
    settings = settings or get_settings()
    paths = {
        "cell_line_drug_response": settings.mammal_cell_line_drug_response_model_path,
        "drug_target_interaction": settings.mammal_dti_model_path,
        "drug_carcinogenicity": settings.mammal_carcinogenicity_model_path,
        "protein_solubility": settings.mammal_protein_solubility_model_path,
    }
    return paths.get(task_type, "")
