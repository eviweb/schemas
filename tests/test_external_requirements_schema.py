import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_DIRECTORY = Path(__file__).resolve().parents[1] / "json-schema" / "external-requirements"
SCHEMA_PATH = SCHEMA_DIRECTORY / "external-requirements.schema.json"
FORMAT_CHECKER = FormatChecker()


@pytest.fixture(scope="module")
def validator():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FORMAT_CHECKER)


@pytest.mark.parametrize(
    "fixture_path",
    sorted((SCHEMA_DIRECTORY / "examples" / "valid").glob("*.json")),
    ids=lambda fixture_path: fixture_path.stem,
)
def test_external_requirements_valid_example_is_accepted(validator, fixture_path):
    manifest = json.loads(fixture_path.read_text(encoding="utf-8"))
    assert list(validator.iter_errors(manifest)) == []


@pytest.mark.parametrize(
    "fixture_path",
    sorted((SCHEMA_DIRECTORY / "examples" / "invalid").glob("*.json")),
    ids=lambda fixture_path: fixture_path.stem,
)
def test_external_requirements_invalid_example_is_rejected(validator, fixture_path):
    manifest = json.loads(fixture_path.read_text(encoding="utf-8"))
    assert list(validator.iter_errors(manifest))


@pytest.mark.parametrize(
    "method",
    ["entire-output", "first-numeric-token", "last-numeric-token"],
)
def test_external_requirements_simple_extraction_method_is_accepted(validator, method):
    manifest = {
        "schemaVersion": 1,
        "requirements": [
            {
                "id": "example-tool",
                "executable": {"candidates": ["example-tool"]},
                "version": {
                    "arguments": [],
                    "outputStream": "stdout",
                    "extraction": {"method": method},
                },
            }
        ],
    }
    assert list(validator.iter_errors(manifest)) == []
