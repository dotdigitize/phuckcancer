from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PhuckCancer"
    app_env: str = "local"
    enable_database: bool = True
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str = "phuckcancer_demo"
    database_user: str = "phuckcancer_user"
    database_password: str = "change_this_password"
    mammal_required: bool = True
    mammal_provider: str = "local"
    mammal_model_name: str = "ibm/biomed.omics.bl.sm.ma-ted-458m"
    mammal_device: str = "auto"
    mammal_workdir: str = ""
    mammal_api_base_url: str = ""
    mammal_api_token: str = ""
    mammal_api_timeout_seconds: int = 60
    mammal_api_interpret_path: str = "/v1/interpret"
    mammal_api_health_path: str = "/health"
    enable_local_llm: bool = False
    ollama_base_url: str = "http://localhost:11434"
    local_llm_model: str = "gemma4:e4b"
    enable_cbioportal_connector: bool = False
    cbioportal_base_url: str = "https://www.cbioportal.org/api"
    cbioportal_api_docs_url: str = "https://www.cbioportal.org/api/v3/api-docs"
    cbioportal_auth_token: str = ""
    cbioportal_timeout_seconds: int = 30
    cbioportal_max_records: int = 500
    backend_host: str = "0.0.0.0"
    backend_port: int = 8717
    frontend_host: str = "0.0.0.0"
    frontend_port: int = 5179
    report_output_dir: str = "reports"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
