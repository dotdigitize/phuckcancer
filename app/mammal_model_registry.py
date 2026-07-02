from __future__ import annotations

from app.config import get_settings
from app.mammal_official_tasks import OFFICIAL_MAMMAL_TASKS
from app.models import MammalModelRegistryEntry


def _hf_task_url(task_type: str, settings) -> str:
    return f"{settings.mammal_hf_finetuned_models_url}&search={task_type}"


def _entry(
    *,
    task_type: str,
    provider: str,
    checkpoint_path: str | None = None,
    checkpoint_model_id: str | None = None,
    norm_y_mean: float | None = None,
    norm_y_std: float | None = None,
    notes: str | None = None,
) -> MammalModelRegistryEntry:
    settings = get_settings()
    task = OFFICIAL_MAMMAL_TASKS[task_type]
    checkpoint_source = "huggingface_or_local_path" if task.requires_fine_tuned_checkpoint else "base_model_or_provider"
    return MammalModelRegistryEntry(
        task_type=task_type,
        provider=provider,
        base_model_id=settings.mammal_base_model_id,
        tokenizer_id=settings.mammal_base_tokenizer_id,
        checkpoint_source=checkpoint_source,
        checkpoint_model_id=checkpoint_model_id,
        checkpoint_path=checkpoint_path,
        model_path=checkpoint_path,
        norm_y_mean=norm_y_mean,
        norm_y_std=norm_y_std,
        official_example_script=task.script_relative_path,
        hf_model_url=_hf_task_url(task_type, settings) if task.requires_fine_tuned_checkpoint else f"https://huggingface.co/{settings.mammal_base_model_id}",
        enabled=bool(not task.requires_fine_tuned_checkpoint or checkpoint_path or checkpoint_model_id or provider in {"api", "mcp_http"}),
        notes=notes,
    )


def configured_model_registry() -> list[MammalModelRegistryEntry]:
    settings = get_settings()
    entries = [
        _entry(
            task_type="cell_line_drug_response",
            provider="official_script",
            checkpoint_path=settings.mammal_cell_line_drug_response_model_path or None,
            notes="Requires a fine-tuned cell-line drug-response checkpoint and matching tokenizer. Configure MAMMAL_CELL_LINE_DRUG_RESPONSE_MODEL_PATH or use a provider-hosted checkpoint.",
        ),
        _entry(
            task_type="drug_target_interaction",
            provider="official_script",
            checkpoint_path=settings.mammal_dti_model_path or None,
            norm_y_mean=float(settings.mammal_dti_norm_y_mean) if settings.mammal_dti_norm_y_mean else None,
            norm_y_std=float(settings.mammal_dti_norm_y_std) if settings.mammal_dti_norm_y_std else None,
            notes="Requires a fine-tuned DTI checkpoint, matching tokenizer, and norm_y_mean/norm_y_std. Configure MAMMAL_DTI_MODEL_PATH and DTI normalization env vars.",
        ),
        _entry(
            task_type="drug_carcinogenicity",
            provider="official_script",
            checkpoint_path=settings.mammal_carcinogenicity_model_path or None,
            notes="Requires a fine-tuned carcinogenicity checkpoint and matching tokenizer. Configure MAMMAL_CARCINOGENICITY_MODEL_PATH or use a provider-hosted checkpoint.",
        ),
        _entry(
            task_type="protein_solubility",
            provider="official_script",
            checkpoint_path=settings.mammal_protein_solubility_model_path or None,
            notes="Requires a fine-tuned protein-solubility checkpoint and matching tokenizer. Configure MAMMAL_PROTEIN_SOLUBILITY_MODEL_PATH or use a provider-hosted checkpoint.",
        ),
        _entry(
            task_type="protein_protein_interaction",
            provider="local",
            notes="Can use the base model/tokenizer through local/API/MCP provider behavior when no task-specific checkpoint is configured.",
        ),
        _entry(
            task_type="tcr_epitope_binding",
            provider="mcp_http",
            notes="Usually provider-hosted through a MAMMAL MCP or API task runner.",
        ),
    ]
    return entries


def model_registry_payload() -> dict:
    settings = get_settings()
    return {
        "base_model_id": settings.mammal_base_model_id,
        "base_tokenizer_id": settings.mammal_base_tokenizer_id,
        "official_repo_url": settings.mammal_official_repo_url,
        "hf_finetuned_models_url": settings.mammal_hf_finetuned_models_url,
        "hf_space_url": settings.mammal_hf_space_url,
        "warning": "Some MAMMAL downstream tasks require fine-tuned checkpoints and matching tokenizers. The base MAMMAL model alone may not be sufficient for every task.",
        "models": [entry.model_dump() for entry in configured_model_registry()],
    }
