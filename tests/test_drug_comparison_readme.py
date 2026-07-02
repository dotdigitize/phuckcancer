from pathlib import Path


def test_readme_contains_drug_comparison_and_official_mammal_sections():
    readme = Path("README.md").read_text()
    assert "## Powerful Cancer Drug Evidence Comparison" in readme
    assert "## Official MAMMAL Task Integration" in readme
