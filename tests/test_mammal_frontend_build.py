import subprocess


def test_frontend_builds():
    completed = subprocess.run(["npm", "run", "build"], capture_output=True, text=True, timeout=120)
    assert completed.returncode == 0, completed.stdout + completed.stderr
