import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


SCHEMA_DIRECTORY = Path(__file__).resolve().parents[1] / "json-schema" / "external-requirements"
SCHEMA_PATH = SCHEMA_DIRECTORY / "external-requirements.schema.json"
FORMAT_CHECKER = FormatChecker()


def test_schema_canonical_identity_resolves_registered_local_schema():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    schema_id = "https://schemas.eviweb.fr/external-requirements/1.0.0/schema.json"
    assert schema.get("$id") == schema_id
    registry = Registry().with_resource(schema_id, Resource.from_contents(schema))
    validator = Draft202012Validator({"$ref": schema_id}, registry=registry)
    assert validator.is_valid({"schemaVersion": 1, "requirements": []})
    assert not validator.is_valid({"schemaVersion": 2, "requirements": []})


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


@pytest.mark.parametrize("custom_value, is_valid", [("enabled", True), (42, False)])
def test_complementary_schema_custom_field_validates_independently(validator, custom_value, is_valid):
    manifest = {
        "schemaVersion": 1,
        "requirements": [{"id": "tool", "executable": {"candidates": ["tool"]}, "clientMode": custom_value}],
    }
    client_schema = {
        "properties": {
            "requirements": {"items": {"properties": {"clientMode": {"type": "string"}}}}
        }
    }
    assert validator.is_valid(manifest)
    assert Draft202012Validator(client_schema).is_valid(manifest) is is_valid


def test_optional_property_typo_is_accepted_as_custom_field(validator):
    manifest = {
        "schemaVersion": 1,
        "requirements": [{"id": "tool", "executable": {"candidates": ["tool"]}, "descripton": "Typo"}],
    }
    assert validator.is_valid(manifest)


@pytest.mark.parametrize("field,value", [("name", 42), ("description", ""), ("documentationUrl", "not a uri")])
def test_optional_shared_property_invalid_value_is_rejected(validator, field, value):
    manifest = {
        "schemaVersion": 1,
        "requirements": [{"id": "tool", "executable": {"candidates": ["tool"]}, field: value}],
    }
    assert not validator.is_valid(manifest)


@pytest.mark.parametrize(
    "version",
    [
        {"outputStream": "stdout", "extraction": {"method": "entire-output"}},
        {"arguments": [], "extraction": {"method": "entire-output"}},
        {"arguments": [12], "outputStream": "stdout", "extraction": {"method": "entire-output"}},
        {"arguments": [], "outputStream": "both", "extraction": {"method": "entire-output"}},
        {"arguments": [], "outputStream": "stdout", "extraction": {"method": "json-property"}},
        {"arguments": [], "outputStream": "stdout", "extraction": {"method": "after-prefix", "prefix": ""}},
        {"arguments": [], "outputStream": "stdout", "extraction": {"method": "entire-output"}, "comparison": "unknown"},
        {"arguments": [], "outputStream": "stdout", "extraction": {"method": "entire-output"}, "minimum": "", "comparison": "semver"},
    ],
)
def test_version_invalid_declaration_is_rejected(validator, version):
    manifest = {"schemaVersion": 1, "requirements": [{"id": "tool", "executable": {"candidates": ["tool"]}, "version": version}]}
    assert not validator.is_valid(manifest)


@pytest.mark.parametrize("comparison", ["numeric-segments", "semver"])
def test_version_minimum_with_supported_comparison_is_accepted(validator, comparison):
    manifest = {"schemaVersion": 1, "requirements": [{"id": "tool", "executable": {"candidates": ["tool"]}, "version": {"arguments": [], "outputStream": "stderr", "extraction": {"method": "entire-output"}, "minimum": "1.0", "comparison": comparison}}]}
    assert validator.is_valid(manifest)


@pytest.mark.parametrize("candidates", [[""], [42], "tool"])
def test_executable_invalid_candidates_are_rejected(validator, candidates):
    manifest = {"schemaVersion": 1, "requirements": [{"id": "tool", "executable": {"candidates": candidates}}]}
    assert not validator.is_valid(manifest)


@pytest.mark.parametrize("provisioning", [None, {}, {"sources": []}, {"sources": [{}]}, {"sources": [{"provider": "apt"}]}, {"sources": [{"reference": "tool"}]}, {"sources": [{"provider": "", "reference": "tool"}]}, {"sources": [{"provider": "apt", "reference": ""}]}, {"sources": [{"provider": "apt", "reference": "tool"}, {"provider": "apt", "reference": "tool"}]}])
def test_provisioning_invalid_sources_are_rejected(validator, provisioning):
    manifest = {"schemaVersion": 1, "requirements": [{"id": "tool", "executable": {"candidates": ["tool"]}, "provisioning": provisioning}]}
    assert not validator.is_valid(manifest)


def test_provisioning_multiple_sources_and_custom_fields_are_accepted(validator):
    manifest = {"schemaVersion": 1, "requirements": [{"id": "tool", "executable": {"candidates": ["tool"]}, "provisioning": {"sources": [{"provider": "apt", "reference": "tool", "clientField": 1}, {"provider": "custom", "reference": "registry/tool"}]}}]}
    assert validator.is_valid(manifest)
