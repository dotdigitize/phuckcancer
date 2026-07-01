from __future__ import annotations

import httpx

from app.config import Settings


class MammalApiClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = settings.mammal_api_base_url.rstrip("/")
        self.timeout = settings.mammal_api_timeout_seconds

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.settings.mammal_api_token:
            headers["Authorization"] = f"Bearer {self.settings.mammal_api_token}"
        return headers

    def status(self) -> dict:
        configured = bool(self.base_url)
        if not configured:
            return {"provider": "api", "configured": False, "available": False, "message": "MAMMAL_API_BASE_URL is not configured."}
        try:
            response = httpx.get(f"{self.base_url}{self.settings.mammal_api_health_path}", headers=self._headers(), timeout=self.timeout)
            response.raise_for_status()
            body = response.json() if response.content else {}
            return {"provider": "api", "configured": True, "available": True, "health": body}
        except httpx.HTTPError as exc:
            return {"provider": "api", "configured": True, "available": False, "message": type(exc).__name__}
        except ValueError:
            return {"provider": "api", "configured": True, "available": False, "message": "Invalid MAMMAL API health response."}

    def interpret(self, payload: dict) -> dict:
        response = httpx.post(
            f"{self.base_url}{self.settings.mammal_api_interpret_path}",
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        body = response.json()
        if not isinstance(body, dict):
            raise ValueError("MAMMAL API response must be a JSON object.")
        return body
