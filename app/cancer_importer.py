from app.genomics_parser import parse_cancer_records


def import_cancer_records(payload: list[dict]):
    return parse_cancer_records(payload)
