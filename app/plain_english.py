from app.assistant_prompts import ROLE_LABELS
from app.models import UserRole


SAFETY = "This is for education, research support, evidence organization, and qualified human review, not medical decision-making."


def explain_plain_english(text: str, user_role: UserRole) -> str:
    if user_role == "patient_family":
        return (
            "Family-friendly summary: this information describes research-level cancer evidence. "
            "Ask your oncologist about the genes, biomarkers, missing information, and whether any finding matters for your care. "
            f"{SAFETY}"
        )
    if user_role == "data_engineer":
        return (
            "System/data summary: review the data source status, MariaDB configuration, cBioPortal connector settings, "
            "MAMMAL provider availability, and API behavior before interpreting biomedical output. "
            f"{SAFETY}"
        )
    if user_role == "cancer_researcher":
        return (
            "Research summary: organize molecular mechanisms, pathway signals, resistance notes, evidence gaps, and reproducible source notes. "
            f"{SAFETY}"
        )
    return (
        f"{ROLE_LABELS[user_role]} summary: the submitted text should be reviewed as molecular evidence, mapped to source records, "
        "checked for unsupported claims, and discussed in qualified clinical or research review. "
        f"{SAFETY}"
    )
