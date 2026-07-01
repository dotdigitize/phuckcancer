from app.config import get_settings
from app.plain_english import explain_plain_english


def assistant_explain(text: str, mode: str) -> dict:
    settings = get_settings()
    return {
        "enabled": settings.enable_local_llm,
        "model": settings.local_llm_model,
        "fallback_used": not settings.enable_local_llm,
        "response": explain_plain_english(text, mode),
    }
