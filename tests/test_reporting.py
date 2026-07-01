from app.reporting import build_reports, latest_reports


def test_reporting_writes_latest_reports(tmp_path, monkeypatch):
    monkeypatch.setenv("REPORT_OUTPUT_DIR", str(tmp_path))
    from app.config import get_settings
    get_settings.cache_clear()
    bundle = build_reports({"risk_flags": ["needs_human_review"]})
    assert "doctor_report" in bundle.output_paths
    latest = latest_reports()
    assert "Patient/Family Summary" in latest["family_summary"]
    get_settings.cache_clear()
