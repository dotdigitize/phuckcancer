import httpx
from app.config import get_settings
from app.sample_data import load_json


class CbioPortalConnector:
    def __init__(self, base_url: str | None = None):
        self.settings = get_settings()
        self.base_url = (base_url or self.settings.cbioportal_base_url).rstrip("/")
        self.headers = {}
        if self.settings.cbioportal_auth_token:
            self.headers["Authorization"] = f"Bearer {self.settings.cbioportal_auth_token}"

    def status(self) -> dict:
        if not self.settings.enable_cbioportal_connector:
            return {
                "enabled": False,
                "available": False,
                "base_url": self.base_url,
                "status": "disabled",
                "message": "cBioPortal connector is disabled; local sample fixtures are used.",
            }
        return {"enabled": True, "available": True, "base_url": self.base_url, "status": "configured"}

    async def _get(self, path: str) -> dict | list:
        if not self.settings.enable_cbioportal_connector:
            raise RuntimeError("cBioPortal connector is disabled")
        try:
            async with httpx.AsyncClient(timeout=self.settings.cbioportal_timeout_seconds, headers=self.headers) as client:
                response = await client.get(f"{self.base_url}{path}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in {401, 403}:
                raise PermissionError("cBioPortal authentication failed or access is forbidden") from exc
            if exc.response.status_code == 404:
                raise LookupError("Requested cBioPortal resource was not found") from exc
            raise ValueError("cBioPortal returned an unexpected response") from exc
        except httpx.RequestError as exc:
            raise ConnectionError("cBioPortal API is unavailable") from exc

    async def studies(self):
        if not self.settings.enable_cbioportal_connector:
            return load_json("cbioportal_studies_fixture.json")
        return await self._get("/studies")

    async def cancer_types(self):
        if not self.settings.enable_cbioportal_connector:
            return [{"cancerTypeId": "luad", "name": "Lung Adenocarcinoma"}, {"cancerTypeId": "brca", "name": "Breast Cancer"}]
        return await self._get("/cancer-types")

    async def study(self, study_id: str):
        if not self.settings.enable_cbioportal_connector:
            studies = await self.studies()
            return next((item for item in studies if item.get("studyId") == study_id), {"studyId": study_id, "status": "fixture_not_found"})
        return await self._get(f"/studies/{study_id}")

    async def sample_lists(self, study_id: str):
        if not self.settings.enable_cbioportal_connector:
            return [{"sampleListId": f"{study_id}_all", "name": "All fixture samples"}]
        return await self._get(f"/studies/{study_id}/sample-lists")

    async def molecular_profiles(self, study_id: str):
        if not self.settings.enable_cbioportal_connector:
            return [{"molecularProfileId": f"{study_id}_mutations", "molecularAlterationType": "MUTATION_EXTENDED"}]
        return await self._get(f"/studies/{study_id}/molecular-profiles")

    async def mutations(self, study_id: str, molecular_profile_id: str, sample_list_id: str, genes: list[str]):
        if not self.settings.enable_cbioportal_connector:
            records = load_json("cbioportal_mutations_fixture.json")
            return [item for item in records if (item.get("gene", {}).get("hugoGeneSymbol") in genes)]
        payload = {"sampleListId": sample_list_id, "entrezGeneIds": [], "projection": "DETAILED"}
        return await self._get(f"/molecular-profiles/{molecular_profile_id}/mutations/fetch?sampleListId={sample_list_id}")
