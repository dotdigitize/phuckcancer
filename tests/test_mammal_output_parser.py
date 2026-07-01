from app.mammal_output_parser import parse_mammal_output
from app.sample_data import load_json


def test_parse_mammal_output_fixture():
    parsed = parse_mammal_output(load_json("mammal_output_fixture.json"))
    assert parsed["biological_interpretation"]
    assert any(claim["gene"] == "EGFR" for claim in parsed["claims"])
