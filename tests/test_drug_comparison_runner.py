from app.drug_comparison_runner import comparison_requirements
from app.drug_library import create_comparison
from app.models import DrugComparisonCreateRequest


def test_drug_target_comparison_requires_smiles_sequence_model_and_norms():
    comparison = create_comparison(
        DrugComparisonCreateRequest(comparison_name="DTI missing inputs", drug_ids=[1], target_ids=[1], cancer_context_ids=[1], task_types=["drug_target_interaction"])
    )
    requirements = comparison_requirements(comparison)
    missing = requirements["missing_structured_data"][0]["missing_fields"]
    assert "drug_smiles" in missing
    assert "target_protein_sequence" in missing
    assert "model_path" in missing
    assert "norm_y_mean" in missing
    assert "norm_y_std" in missing
