from app.mammal_output_parser import parse_mammal_output


def import_saved_mammal_output(payload: dict | str) -> dict:
    return parse_mammal_output(payload)
