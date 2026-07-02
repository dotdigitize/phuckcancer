from app.drug_scoring import score_drug_evidence


def test_evidence_scoring_returns_insufficient_data_when_outputs_missing():
    score = score_drug_evidence({"task_types": ["drug_target_interaction"], "missing_data": ["drug_smiles"]})
    assert score.overall_review_priority == "insufficient_data"
    assert score.evidence_support_score is None
