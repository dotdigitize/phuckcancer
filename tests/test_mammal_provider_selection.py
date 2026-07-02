from app.config import Settings
from app.mammal_providers import ApiMammalProvider, OfficialScriptMammalProvider, MammalConfigurationError, get_mammal_provider


def test_mammal_provider_supports_api():
    provider = get_mammal_provider(Settings(mammal_provider="api", mammal_api_base_url="http://localhost:9000"))
    assert isinstance(provider, ApiMammalProvider)


def test_mammal_provider_supports_official_script():
    provider = get_mammal_provider(Settings(mammal_provider="official_script", mammal_repo_path="/opt/biomed-multi-alignment"))
    assert isinstance(provider, OfficialScriptMammalProvider)


def test_mammal_provider_rejects_unknown():
    try:
        get_mammal_provider(Settings(mammal_provider="other"))
    except MammalConfigurationError:
        assert True
    else:
        assert False
