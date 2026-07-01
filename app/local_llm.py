import httpx

from app.assistant_prompts import system_prompt_for_role
from app.config import get_settings
from app.models import AssistantRequest
from app.plain_english import explain_plain_english


SECRET_KEYS = {"token", "password", "secret", "authorization", "api_key"}


def _redact_secrets(value):
    if isinstance(value, dict):
        return {key: ("[redacted]" if any(secret in key.lower() for secret in SECRET_KEYS) else _redact_secrets(item)) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_secrets(item) for item in value]
    return value


def _request_text(request: AssistantRequest) -> str:
    if request.source_text:
        return request.source_text
    if request.report_text:
        return request.report_text
    if request.mammal_interpretation:
        return str(_redact_secrets(request.mammal_interpretation))
    if request.audit_id:
        return f"Evidence audit id: {request.audit_id}"
    return ""


def assistant_explain(request: AssistantRequest) -> dict:
    settings = get_settings()
    assert request.user_role is not None
    text = _request_text(request)
    system_prompt = system_prompt_for_role(request.user_role)
    context = {
        "user_role": request.user_role,
        "mammal_structured_output": _redact_secrets(request.mammal_interpretation or {}),
        "evidence_audit_output": _redact_secrets(request.evidence_audit or {}),
        "risk_flags": request.risk_flags,
        "source_evidence_notes": request.source_notes,
        "safety_constraints": request.safety_constraints
        or [
            "MAMMAL-powered interpretation is research and evidence support only.",
            "Qualified human medical review is required.",
            "Do not diagnose, prescribe, recommend treatment, predict survival, or determine trial eligibility.",
        ],
    }
    if settings.enable_local_llm:
        try:
            response = httpx.post(
                f"{settings.ollama_base_url.rstrip('/')}/api/chat",
                json={
                    "model": settings.local_llm_model,
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Context:\n{context}\n\nText to explain:\n{text}"},
                    ],
                },
                timeout=60,
            )
            response.raise_for_status()
            body = response.json()
            content = body.get("message", {}).get("content") or body.get("response")
            if content:
                return {"enabled": True, "model": settings.local_llm_model, "user_role": request.user_role, "system_prompt": system_prompt, "response": content}
        except httpx.HTTPError:
            pass
    return {
        "enabled": settings.enable_local_llm,
        "model": settings.local_llm_model,
        "user_role": request.user_role,
        "system_prompt": system_prompt,
        "local_llm_unavailable": not settings.enable_local_llm,
        "response": explain_plain_english(text, request.user_role),
        "context": context,
    }
