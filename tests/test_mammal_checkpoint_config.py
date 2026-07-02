from app.mammal_checkpoint_config import task_requires_fine_tuned_checkpoint, task_requires_normalization
from app.models import MammalModelRegistryEntry


def test_downstream_tasks_can_require_fine_tuned_checkpoint():
    assert task_requires_fine_tuned_checkpoint("drug_target_interaction") is True
    assert task_requires_fine_tuned_checkpoint("cell_line_drug_response") is True
    assert task_requires_fine_tuned_checkpoint("protein_protein_interaction") is False


def test_dti_requires_normalization_values():
    assert task_requires_normalization("drug_target_interaction") is True
    assert task_requires_normalization("drug_carcinogenicity") is False


def test_model_registry_entry_supports_checkpoint_model_id_and_path():
    entry = MammalModelRegistryEntry(
        task_type="drug_target_interaction",
        provider="official_script",
        checkpoint_model_id="example/dti-checkpoint",
        checkpoint_path="/opt/mammal-models/dti",
    )
    assert entry.checkpoint_model_id == "example/dti-checkpoint"
    assert entry.checkpoint_path == "/opt/mammal-models/dti"
