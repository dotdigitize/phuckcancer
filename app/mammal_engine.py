from app.config import get_settings
from app.mammal_pipeline import run_mammal_pipeline
from app.mammal_providers import MammalUnavailableError, get_mammal_provider


class MammalEngine:
    def __init__(self):
        self.settings = get_settings()

    def status(self) -> dict:
        base = {
            "required": self.settings.mammal_required,
            "provider": self.settings.mammal_provider,
            "model_name": self.settings.mammal_model_name,
            "device": self.settings.mammal_device,
            "api_configured": bool(self.settings.mammal_api_base_url),
        }
        try:
            provider = get_mammal_provider(self.settings)
            return {**base, **provider.status(), "available": True}
        except MammalUnavailableError as exc:
            return {**base, "available": False, "message": str(exc)}

    def interpret(self, evidence: list[dict]) -> dict:
        return run_mammal_pipeline(evidence)
