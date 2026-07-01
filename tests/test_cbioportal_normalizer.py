from app.cbioportal_normalizer import normalize_mutations, normalize_studies
from app.sample_data import load_json


def test_normalize_cbioportal_studies():
    studies = normalize_studies(load_json("cbioportal_studies_fixture.json"))
    assert studies[0]["study_id"] == "synthetic_luad_cbioportal"


def test_normalize_mutations_to_internal_records():
    records = normalize_mutations(load_json("cbioportal_mutations_fixture.json"), "synthetic")
    assert records
    assert records[0].alterations[0].alteration_type == "mutation"
    assert records[0].evidence[0].source.startswith("cBioPortal API study")
