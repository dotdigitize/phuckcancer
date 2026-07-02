from app.config import get_settings


MAMMAL_TABLES = [
    "mammal_model_registry",
    "mammal_task_runs",
    "mammal_task_inputs",
    "mammal_task_outputs",
    "mammal_task_errors",
    "mammal_uploaded_files",
]


def database_status() -> dict:
    settings = get_settings()
    base = {
        "enabled": settings.enable_database,
        "provider": "mariadb",
        "engine": "MariaDB/MySQL",
        "host": settings.database_host,
        "port": settings.database_port,
        "database": settings.database_name,
        "mammal_tables": MAMMAL_TABLES,
    }
    if not settings.enable_database:
        return {**base, "available": False, "mode": "disabled_local_fixture_mode"}
    try:
        import mysql.connector
        from mysql.connector import Error
    except Exception as exc:
        return {**base, "available": False, "message": f"mysql-connector-python unavailable: {type(exc).__name__}"}
    try:
        conn = mysql.connector.connect(
            host=settings.database_host,
            port=settings.database_port,
            database=settings.database_name,
            user=settings.database_user,
            password=settings.database_password,
            connection_timeout=3,
        )
        conn.close()
        return {**base, "available": True, "mode": "configured"}
    except Error as exc:
        return {**base, "available": False, "mode": "configured_unavailable", "message": exc.__class__.__name__}
