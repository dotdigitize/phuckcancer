SAFETY = "This is for education, research support, evidence organization, and qualified human review, not medical decision-making."


def explain_plain_english(text: str, mode: str) -> str:
    if mode == "patient_family":
        return (
            "Family-friendly summary: this information describes research-level cancer evidence. "
            "Ask your oncologist about the genes, biomarkers, missing information, and whether any finding matters for your care. "
            f"{SAFETY}"
        )
    return (
        "Doctor/research summary: the submitted text should be reviewed as molecular evidence, mapped to source records, "
        "checked for unsupported claims, and discussed in qualified clinical or research review. "
        f"{SAFETY}"
    )
