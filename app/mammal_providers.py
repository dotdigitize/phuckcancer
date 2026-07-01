from __future__ import annotations

from typing import Protocol

import httpx

from app.config import Settings
from app.mammal_api_client import MammalApiClient


class MammalUnavailableError(Exception):
    pass


class MammalConfigurationError(MammalUnavailableError):
    pass


class MammalModelLoadError(MammalUnavailableError):
    pass


class MammalApiError(MammalUnavailableError):
    pass


class MammalInferenceError(MammalUnavailableError):
    pass


class MammalInvalidOutputError(MammalUnavailableError):
    pass


class MammalProvider(Protocol):
    provider_name: str

    def status(self) -> dict:
        ...

    def interpret(self, payload: dict) -> dict:
        ...


class LocalMammalProvider:
    provider_name = "local"

    def __init__(self, settings: Settings):
        self.settings = settings
        self.device = self._select_device(settings.mammal_device)
        try:
            from mammal.model import Mammal
        except Exception as exc:
            raise MammalUnavailableError("Local MAMMAL package is not installed.") from exc
        try:
            self.model = Mammal.from_pretrained(settings.mammal_model_name)
            if hasattr(self.model, "to"):
                self.model.to(self.device)
            if hasattr(self.model, "eval"):
                self.model.eval()
        except Exception as exc:
            raise MammalModelLoadError("Local MAMMAL model could not be loaded.") from exc

    def _select_device(self, configured: str) -> str:
        configured = (configured or "auto").lower()
        if configured == "cpu":
            return "cpu"
        try:
            import torch
        except Exception as exc:
            if configured == "cuda":
                raise MammalConfigurationError("MAMMAL_DEVICE=cuda requires PyTorch with CUDA support.") from exc
            return "cpu"
        cuda_available = bool(torch.cuda.is_available())
        if configured == "cuda" and not cuda_available:
            raise MammalConfigurationError("MAMMAL_DEVICE=cuda was requested but CUDA is unavailable.")
        if configured == "cuda":
            return "cuda"
        if configured != "auto":
            raise MammalConfigurationError("MAMMAL_DEVICE must be auto, cuda, or cpu.")
        return "cuda" if cuda_available else "cpu"

    def status(self) -> dict:
        return {
            "provider": "local",
            "available": True,
            "configured": True,
            "model_name": self.settings.mammal_model_name,
            "device": self.device,
        }

    def interpret(self, payload: dict) -> dict:
        try:
            if hasattr(self.model, "interpret"):
                result = self.model.interpret(payload)
            elif callable(self.model):
                result = self.model(payload)
            else:
                raise MammalInferenceError("Installed MAMMAL model does not expose an interpretation method.")
        except MammalInferenceError:
            raise
        except Exception as exc:
            raise MammalInferenceError("Local MAMMAL inference failed.") from exc
        if not isinstance(result, dict):
            raise MammalInvalidOutputError("Local MAMMAL output must be a structured object.")
        result.setdefault("provider", "local")
        result.setdefault("model_name", self.settings.mammal_model_name)
        result.setdefault("device", self.device)
        return result


class ApiMammalProvider:
    provider_name = "api"

    def __init__(self, settings: Settings):
        self.settings = settings
        if not settings.mammal_api_base_url:
            raise MammalConfigurationError("MAMMAL_API_BASE_URL is required when MAMMAL_PROVIDER=api.")
        self.client = MammalApiClient(settings)

    def status(self) -> dict:
        return self.client.status()

    def interpret(self, payload: dict) -> dict:
        try:
            result = self.client.interpret(payload)
        except httpx.TimeoutException as exc:
            raise MammalApiError("MAMMAL API timed out.") from exc
        except httpx.HTTPStatusError as exc:
            raise MammalApiError(f"MAMMAL API returned HTTP {exc.response.status_code}.") from exc
        except httpx.HTTPError as exc:
            raise MammalApiError("MAMMAL API request failed.") from exc
        except ValueError as exc:
            raise MammalApiError("MAMMAL API returned invalid JSON.") from exc
        result.setdefault("provider", "api")
        result.setdefault("model_name", self.settings.mammal_model_name)
        return result


def get_mammal_provider(settings: Settings) -> MammalProvider:
    provider = (settings.mammal_provider or "").lower()
    if provider == "local":
        return LocalMammalProvider(settings)
    if provider == "api":
        return ApiMammalProvider(settings)
    raise MammalConfigurationError("MAMMAL_PROVIDER must be local or api.")
