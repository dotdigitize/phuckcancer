from __future__ import annotations

import httpx

from app.config import Settings, get_settings
from app.mammal_providers import MammalApiError, MammalConfigurationError


class MammalMcpClient:
    provider_name = "mcp_http"

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        if not self.settings.mammal_mcp_base_url:
            raise MammalConfigurationError("MAMMAL_MCP_BASE_URL is required when using mcp_http.")

    def status(self) -> dict:
        try:
            response = httpx.get(f"{self.settings.mammal_mcp_base_url.rstrip('/')}/health", timeout=self.settings.mammal_mcp_timeout_seconds)
            response.raise_for_status()
            return {"provider": "mcp_http", "available": True, "base_url": self.settings.mammal_mcp_base_url, "health": response.json()}
        except httpx.HTTPError as exc:
            raise MammalApiError("MAMMAL MCP server is unavailable.") from exc

    def run_task(self, task_type: str, payload: dict) -> dict:
        try:
            response = httpx.post(
                f"{self.settings.mammal_mcp_base_url.rstrip('/')}/tasks/{task_type}",
                json=payload,
                timeout=self.settings.mammal_mcp_timeout_seconds,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            raise MammalApiError("MAMMAL MCP task call failed.") from exc
