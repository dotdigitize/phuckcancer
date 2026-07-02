from app.config import Settings
from app.mammal_task_runner import run_official_script_task


def test_official_script_runner_builds_cell_line_command(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    script = repo / "mammal/examples/cell_line_drug_response/main_infer.py"
    script.parent.mkdir(parents=True)
    script.write_text("print('ok')")
    models = tmp_path / "models"
    models.mkdir()
    checkpoint = models / "best_epoch.ckpt"
    checkpoint.write_text("checkpoint")
    captured = {}

    def fake_run(args, shell, capture_output, text, timeout):
        captured["args"] = args
        captured["shell"] = shell

        class Completed:
            returncode = 0
            stdout = "0.42"
            stderr = ""

        return Completed()

    monkeypatch.setattr("app.mammal_task_runner.subprocess.run", fake_run)
    result = run_official_script_task(
        "cell_line_drug_response",
        {"model_path": str(checkpoint), "cell_line_name": "A375", "drug_smiles": "CCO", "drug_name": "ExampleDrug"},
        Settings(mammal_repo_path=str(repo), mammal_allowed_model_dirs=str(models)),
    )
    assert captured["shell"] is False
    assert "--cell_line_name" in captured["args"]
    assert result["predicted_ic50_or_response_signal"] == 0.42
