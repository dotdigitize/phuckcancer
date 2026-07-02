from app.mammal_official_tasks import OFFICIAL_MAMMAL_TASKS, official_tasks_payload


def test_official_tasks_include_required_biomedical_task_types():
    for task_type in [
        "cell_line_drug_response",
        "drug_target_interaction",
        "drug_carcinogenicity",
        "protein_protein_interaction",
        "protein_solubility",
        "tcr_epitope_binding",
    ]:
        assert task_type in OFFICIAL_MAMMAL_TASKS


def test_official_tasks_payload_warns_about_structured_inputs():
    payload = official_tasks_payload()
    assert "will not invent SMILES" in payload["warning"]
