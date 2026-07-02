from __future__ import annotations


def build_protein_interaction_prompt(payload: dict) -> str:
    protein_a = payload.get("protein_a_sequence") or payload.get("protein_a_name")
    protein_b = payload.get("protein_b_sequence") or payload.get("protein_b_name")
    return (
        "<@TOKENIZER-TYPE=AA>\n"
        "<BINDING_AFFINITY_CLASS>\n"
        "<SENTINEL_ID_0>\n"
        "<MOLECULAR_ENTITY>\n"
        "<MOLECULAR_ENTITY_GENERAL_PROTEIN>\n"
        f"<SEQUENCE_NATURAL_START>{protein_a}</SEQUENCE_NATURAL_END>\n"
        "<MOLECULAR_ENTITY>\n"
        "<MOLECULAR_ENTITY_GENERAL_PROTEIN>\n"
        f"<SEQUENCE_NATURAL_START>{protein_b}</SEQUENCE_NATURAL_END>\n"
        "<EOS>"
    )
