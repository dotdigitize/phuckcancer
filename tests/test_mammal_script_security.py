import inspect

from app.config import Settings
from app.mammal_checkpoint_config import validate_model_path
from app.mammal_task_runner import MammalScriptUnavailableError, _script_path, run_official_script_task


def test_official_script_runner_does_not_use_shell_true():
    source = inspect.getsource(run_official_script_task)
    assert "shell=False" in source
    assert "shell=True" not in source


def test_script_runner_only_allows_whitelisted_task_scripts(tmp_path):
    settings = Settings(mammal_repo_path=str(tmp_path))
    try:
        _script_path("not_a_task", settings)
    except MammalScriptUnavailableError:
        assert True
    else:
        assert False


def test_model_path_validation_rejects_outside_allowed_dirs(tmp_path):
    model = tmp_path / "best_epoch.ckpt"
    model.write_text("checkpoint")
    settings = Settings(mammal_allowed_model_dirs=str(tmp_path / "allowed"))
    try:
        validate_model_path(str(model), settings)
    except Exception as exc:
        assert "not_allowed" in str(exc)
    else:
        assert False


def test_model_path_validation_accepts_configured_allowed_dir(tmp_path):
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    model = allowed / "best_epoch.ckpt"
    model.write_text("checkpoint")
    settings = Settings(mammal_allowed_model_dirs=str(allowed))
    assert validate_model_path(str(model), settings) == str(model.resolve())
