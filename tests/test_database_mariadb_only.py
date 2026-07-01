from pathlib import Path

from app.database import database_status


def test_database_status_reports_mariadb():
    status = database_status()
    assert status["provider"] == "mariadb"
    assert "MariaDB" in status["engine"]


def test_mariadb_demo_files_exist():
    for name in ["schema.sql", "seed_cancer_demo.sql", "reset_demo_database.sql", "README.md"]:
        assert (Path("db") / name).exists()
