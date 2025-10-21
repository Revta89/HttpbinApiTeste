import json
import os
from jsonschema import validate, ValidationError


def load_json_schema(schema: str) -> dict:
    """Load JSON schema from a file"""
    schema_dir = os.path.join(os.path.dirname(__file__), "..", "json_schemas")
    schema_path = os.path.join(schema_dir, schema)
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file '{schema}' not found in {schema_dir}")
    with open(schema_path, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_json_schema(json_data: dict, schema: str):
    """JSON validation with schema"""
    schema = load_json_schema(schema)
    try:
        validate(instance=json_data, schema=schema)
        return True
    except ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")