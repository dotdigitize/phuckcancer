import asyncio
from app.cbioportal_connector import CbioPortalConnector


def test_cbioportal_connector_uses_fixture_when_disabled():
    connector = CbioPortalConnector()
    assert connector.status()["enabled"] is False
    studies = asyncio.run(connector.studies())
    assert studies[0]["studyId"] == "synthetic_luad_cbioportal"


def test_cbioportal_mutations_fixture_filters_genes():
    connector = CbioPortalConnector()
    records = asyncio.run(connector.mutations("synthetic_luad_cbioportal", "profile", "samples", ["EGFR"]))
    assert len(records) == 1
    assert records[0]["gene"]["hugoGeneSymbol"] == "EGFR"
