from app.config import Settings
from app.mammal_providers import ApiMammalProvider, MammalConfigurationError, get_mammal_provider


def test_mammal_provider_supports_api():
    provider = get_mammal_provider(Settings(mammal_provider="api", mammal_api_base_url="http://localhost:9000"))
    assert isinstance(provider, ApiMammalProvider)


def test_mammal_provider_rejects_unknown():
    try:
        get_mammal_provider(Settings(mammal_provider="other"))
    except MammalConfigurationError:
        assert True
    else:
        assert False
