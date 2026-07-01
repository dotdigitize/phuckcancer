def review_resistance_signal(payload: dict) -> dict:
    return {
        "cancer_type": payload.get("cancer_type", "unspecified cancer type"),
        "treatment_category": payload.get("treatment_category", "unspecified treatment category"),
        "gene_pathway": payload.get("gene_pathway", "unspecified gene/pathway"),
        "support_status": "needs_human_review",
        "mammal_driven_interpretation": "Resistance-associated signal requires source evidence auditing and qualified human review.",
        "human_review_recommendation": "Do not use as a treatment decision without oncology review.",
    }
