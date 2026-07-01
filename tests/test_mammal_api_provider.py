import httpx

from app.config import Settings
from app.mammal_providers import ApiMammalProvider, MammalApiError, MammalConfigurationError


def test_api_provider_requires_base_url():
    settings = Settings(mammal_provider="api", mammal_api_base_url="")
    try:
        ApiMammalProvider(settings)
    except MammalConfigurationError:
        assert True
    else:
        assert False


def test_api_provider_wraps_http_errors(monkeypatch):
    settings = Settings(mammal_provider="api", mammal_api_base_url="http://mammal.example")
    provider = ApiMammalProvider(settings)

    def raise_timeout(*args, **kwargs):
        raise httpx.TimeoutException("timeout")

    monkeypatch.setattr(provider.client, "interpret", raise_timeout)
    try:
        provider.interpret({"records": []})
    except MammalApiError:
        assert True
    else:
        assert False
