from app.config import get_settings
from app.models import MammalInterpretation


class MammalEngine:
    def __init__(self):
        self.settings = get_settings()

    def status(self) -> dict:
        return {
            "enabled": self.settings.enable_mammal_engine,
            "model_name": self.settings.mammal_model_name,
            "pipeline_mode": "live_mammal" if self.settings.enable_mammal_engine else "deterministic_fallback",
            "subprocess_allowed": self.settings.mammal_allow_subprocess,
        }

    def interpret(self, evidence: list[dict]) -> MammalInterpretation:
        genes = sorted({str(item.get("gene", "unknown")) for item in evidence})
        findings = [f"{gene} has molecular evidence that should be audited against source records." for gene in genes]
        return MammalInterpretation(
            interpretation_id="mammal-fallback-001",
            model_name=self.settings.mammal_model_name,
            enabled=self.settings.enable_mammal_engine,
            fallback_used=not self.settings.enable_mammal_engine,
            findings=findings,
            interpretation=" ".join(findings) + " This is research support output and needs qualified human review.",
            claims=findings,
        )
