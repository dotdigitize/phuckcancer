from app.assistant_prompts import ROLE_SYSTEM_PROMPTS, system_prompt_for_role


def test_assistant_prompt_changes_by_role():
    assert "patient or family member" in system_prompt_for_role("patient_family")
    assert "qualified medical reviewer" in system_prompt_for_role("doctor_tumor_board")
    assert "cancer research evidence review" in system_prompt_for_role("cancer_researcher")
    assert "system operation" in system_prompt_for_role("data_engineer")
    assert len(set(ROLE_SYSTEM_PROMPTS.values())) == 4
