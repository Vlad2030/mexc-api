import humps


def to_snake_case(json: dict | list[dict]) -> str:
    if isinstance(json, dict):
        return humps.decamelize(json.items().mapping)
    if isinstance(json, list):
        return humps.decamelize(json)
