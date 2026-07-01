from app.genomics_parser import build_alteration_matrix
from app.sample_data import cancer_records


def test_build_alteration_matrix():
    matrix = build_alteration_matrix(cancer_records())
    assert "EGFR" in matrix["genes"]
    assert matrix["legend"]["mutation"] == "Mutation"
    assert matrix["rows"]
