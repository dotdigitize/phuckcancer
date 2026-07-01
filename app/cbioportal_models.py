from pydantic import BaseModel, Field


class CbioPortalImportRequest(BaseModel):
    base_url: str = "https://www.cbioportal.org/api"
    study_id: str
    sample_list_id: str
    molecular_profile_id: str
    genes: list[str] = Field(default_factory=lambda: ["TP53", "KRAS", "EGFR", "BRCA1", "BRCA2"])


class CbioPortalStudy(BaseModel):
    studyId: str
    name: str
    cancerTypeId: str | None = None
    description: str | None = None


class CbioPortalMutation(BaseModel):
    gene: dict | None = None
    entrezGeneId: int | None = None
    sampleId: str
    studyId: str | None = None
    proteinChange: str | None = None
    mutationType: str | None = None
    keyword: str | None = None
