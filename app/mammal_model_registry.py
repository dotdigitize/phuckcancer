from __future__ import annotations

from app.config import get_settings
from app.models import MammalModelRegistryEntry


def configured_model_registry() -> list[MammalModelRegistryEntry]:
    settings = get_settings()
    entries = [
        MammalModelRegistryEntry(
            task_type="cell_line_drug_response",
            provider="official_script",
            model_path=settings.mammal_cell_line_drug_response_model_path or None,
            notes="Configured by MAMMAL_CELL_LINE_DRUG_RESPONSE_MODEL_PATH.",
        ),
        MammalModelRegistryEntry(
            task_type="drug_target_interaction",
            provider="official_script",
            model_path=settings.mammal_dti_model_path or None,
            norm_y_mean=float(settings.mammal_dti_norm_y_mean) if settings.mammal_dti_norm_y_mean else None,
            norm_y_std=float(settings.mammal_dti_norm_y_std) if settings.mammal_dti_norm_y_std else None,
            notes="Configured by MAMMAL_DTI_MODEL_PATH and DTI normalization env vars.",
        ),
        MammalModelRegistryEntry(
            task_type="drug_carcinogenicity",
            provider="official_script",
            model_path=settings.mammal_carcinogenicity_model_path or None,
            notes="Configured by MAMMAL_CARCINOGENICITY_MODEL_PATH.",
        ),
        MammalModelRegistryEntry(
            task_type="protein_solubility",
            provider="official_script",
            model_path=settings.mammal_protein_solubility_model_path or None,
            notes="Configured by MAMMAL_PROTEIN_SOLUBILITY_MODEL_PATH.",
        ),
    ]
    return entries


def model_registry_payload() -> dict:
    return {"models": [entry.model_dump() for entry in configured_model_registry()]}
