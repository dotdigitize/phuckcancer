from __future__ import annotations

from dataclasses import dataclass


OFFICIAL_TASK_TYPES = (
    "cell_line_drug_response",
    "drug_target_interaction",
    "drug_carcinogenicity",
    "protein_protein_interaction",
    "protein_solubility",
    "tcr_epitope_binding",
)


@dataclass(frozen=True)
class OfficialMammalTask:
    task_type: str
    purpose: str
    provider_modes: tuple[str, ...]
    required_inputs: tuple[str, ...]
    optional_inputs: tuple[str, ...]
    script_relative_path: str | None = None
    requires_fine_tuned_checkpoint: bool = False
    requires_normalization: bool = False


OFFICIAL_MAMMAL_TASKS: dict[str, OfficialMammalTask] = {
    "cell_line_drug_response": OfficialMammalTask(
        task_type="cell_line_drug_response",
        purpose="Predict cancer cell-line drug response / IC50-style signal using MAMMAL.",
        provider_modes=("official_script", "api", "mcp_http"),
        required_inputs=("model_path", "drug_smiles", "drug_name", "cell_line_name_or_cell_line_h5ad_file"),
        optional_inputs=("cell_line_name", "cell_line_h5ad_file"),
        script_relative_path="mammal/examples/cell_line_drug_response/main_infer.py",
        requires_fine_tuned_checkpoint=True,
    ),
    "drug_target_interaction": OfficialMammalTask(
        task_type="drug_target_interaction",
        purpose="Predict drug-target binding affinity using target amino acid sequence and drug SMILES.",
        provider_modes=("official_script", "api", "mcp_http"),
        required_inputs=("model_path", "target_protein_sequence", "drug_smiles", "norm_y_mean", "norm_y_std"),
        optional_inputs=("target_name", "drug_name", "cancer_context"),
        script_relative_path="mammal/examples/dti_bindingdb_kd/main_infer.py",
        requires_fine_tuned_checkpoint=True,
        requires_normalization=True,
    ),
    "drug_carcinogenicity": OfficialMammalTask(
        task_type="drug_carcinogenicity",
        purpose="Predict whether a drug SMILES has carcinogenicity signal.",
        provider_modes=("official_script", "api", "mcp_http"),
        required_inputs=("model_path", "drug_smiles"),
        optional_inputs=("drug_name",),
        script_relative_path="mammal/examples/carcinogenicity/main_infer.py",
        requires_fine_tuned_checkpoint=True,
    ),
    "protein_protein_interaction": OfficialMammalTask(
        task_type="protein_protein_interaction",
        purpose="Predict whether two proteins interact with official MAMMAL structured prompt syntax or MCP.",
        provider_modes=("local", "mcp_http", "api"),
        required_inputs=("protein_a_name_or_sequence", "protein_b_name_or_sequence"),
        optional_inputs=("protein_a_name", "protein_a_sequence", "protein_b_name", "protein_b_sequence"),
    ),
    "protein_solubility": OfficialMammalTask(
        task_type="protein_solubility",
        purpose="Predict protein solubility.",
        provider_modes=("official_script", "api", "mcp_http"),
        required_inputs=("model_path", "protein_name_or_sequence"),
        optional_inputs=("protein_name", "protein_sequence"),
        script_relative_path="mammal/examples/protein_solubility/main_infer.py",
        requires_fine_tuned_checkpoint=True,
    ),
    "tcr_epitope_binding": OfficialMammalTask(
        task_type="tcr_epitope_binding",
        purpose="Predict binding between T-cell receptor sequence and epitope sequence through MAMMAL MCP if available.",
        provider_modes=("mcp_http", "api"),
        required_inputs=("tcr_sequence", "epitope_sequence"),
        optional_inputs=("cancer_context",),
    ),
}


def official_tasks_payload() -> dict:
    return {
        "tasks": [
            {
                "task_type": task.task_type,
                "purpose": task.purpose,
                "provider_modes": list(task.provider_modes),
                "required_inputs": list(task.required_inputs),
                "optional_inputs": list(task.optional_inputs),
                "script_relative_path": task.script_relative_path,
                "requires_fine_tuned_checkpoint": task.requires_fine_tuned_checkpoint,
                "requires_normalization": task.requires_normalization,
            }
            for task in OFFICIAL_MAMMAL_TASKS.values()
        ],
        "warning": (
            "MAMMAL needs structured biological inputs. PhuckCancer will not invent SMILES strings, "
            "protein sequences, gene-expression profiles, h5ad files, model checkpoints, or normalization values. "
            "Some MAMMAL downstream tasks require fine-tuned checkpoints and matching tokenizers. "
            "The base MAMMAL model alone may not be sufficient for every task."
        ),
    }
