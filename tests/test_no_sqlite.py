from pathlib import Path


def test_no_sqlite_runtime_import_or_files():
    text = "\n".join(path.read_text(errors="ignore") for path in list(Path("app").glob("**/*.py")) + list(Path("requirements.txt").parent.glob("*.md")))
    assert f"import {'sqlite'}3" not in text
    assert f".{'db'} files" not in text
    assert f"{'SQLite'} database option" not in text
