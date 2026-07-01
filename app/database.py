from app.config import get_settings


def database_status() -> dict:
    settings = get_settings()
    return {
        "enabled": settings.enable_database,
        "engine": "MariaDB",
        "mode": "configured" if settings.enable_database else "disabled_local_fixture_mode",
    }
