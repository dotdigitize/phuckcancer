from __future__ import annotations

from app.config import Settings, get_settings
from app.mammal_official_tasks import OFFICIAL_MAMMAL_TASKS
from app.mammal_providers import MammalConfigurationError


VALID_PROVIDER_MODES = {"local", "api", "mcp_http", "official_script"}


def provider_for_task(task_type: str, requested_provider: str | None = None, settings: Settings | None = None) -> str:
    settings = settings or get_settings()
    provider = (requested_provider or settings.mammal_provider or "").lower()
    if provider not in VALID_PROVIDER_MODES:
        raise MammalConfigurationError("MAMMAL_PROVIDER must be local, api, mcp_http, or official_script.")
    task = OFFICIAL_MAMMAL_TASKS.get(task_type)
    if not task:
        raise MammalConfigurationError("unsupported_mammal_task")
    if provider not in task.provider_modes:
        raise MammalConfigurationError(f"{provider} is not supported for {task_type}.")
    return provider
