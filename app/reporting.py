import json
from pathlib import Path
from app.config import get_settings
from app.models import ReportBundle


def build_reports(audit: dict | None = None) -> ReportBundle:
    settings = get_settings()
    out = Path(settings.report_output_dir)
    out.mkdir(exist_ok=True)
    doctor = "# Doctor/Research Evidence Report\n\nMAMMAL-powered biomedical interpretation and evidence audit results require qualified human review.\n"
    family = "# Patient/Family Summary\n\nThis summary helps prepare questions for the oncology care team and does not provide diagnosis or treatment instructions.\n"
    audit_json = audit or {"review_status": "needs_human_review", "risk_flags": ["needs_human_review"]}
    paths = {
        "doctor_report": str(out / "latest_doctor_report.md"),
        "family_summary": str(out / "latest_family_summary.md"),
        "audit_report": str(out / "latest_audit_report.json"),
    }
    Path(paths["doctor_report"]).write_text(doctor)
    Path(paths["family_summary"]).write_text(family)
    Path(paths["audit_report"]).write_text(json.dumps(audit_json, indent=2))
    return ReportBundle(doctor_report_markdown=doctor, family_summary_markdown=family, audit_json=audit_json, output_paths=paths)


def latest_reports() -> dict:
    settings = get_settings()
    out = Path(settings.report_output_dir)
    return {
        "doctor_report": (out / "latest_doctor_report.md").read_text() if (out / "latest_doctor_report.md").exists() else "",
        "family_summary": (out / "latest_family_summary.md").read_text() if (out / "latest_family_summary.md").exists() else "",
        "audit_report": json.loads((out / "latest_audit_report.json").read_text()) if (out / "latest_audit_report.json").exists() else {},
    }
