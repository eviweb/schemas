# External requirements schema

This [Draft 2020-12 schema](external-requirements.schema.json) validates the shared structure of `external-requirements.json`. Version 1 describes external executable requirements. It supports validation and authoring assistance in compatible IDEs. It does not execute probes or check whether an executable exists.

The schema has no published `$id` yet. The repository is private during initial development. A published identifier and an immutable URL containing a full Git commit ID must be selected and tested before release. The optional manifest `$schema` property can contain a relative URI reference during local development.

## Manifest properties

| Property | Required | Accepted value |
| --- | --- | --- |
| `schemaVersion` | Yes | Integer `1`; this is the major manifest format version. |
| `requirements` | Yes | Array of requirements; may be empty. |
| `$schema` | No | Non-empty URI reference for compatible editors and validators. |

Each requirement has the following shared properties:

| Property | Required | Accepted value |
| --- | --- | --- |
| `id` | Yes | Non-empty lowercase kebab-case identifier, for example `ghostscript`. |
| `executable` | Yes | Object containing `candidates`. |
| `name` | No | Non-empty display name. `id` can be used as a label when it is absent. |
| `description` | No | Non-empty description of the executable's purpose in the project. |
| `version` | No | Version detection information described below. |
| `documentationUrl` | No | Non-empty absolute URI to documentation. |

`executable.candidates` is a required, non-empty, ordered array of distinct, non-empty strings. Each string indicates an executable name or absolute path. The schema does not validate path syntax or executable availability.

When `version` is present, `arguments` is a required array of strings and may be empty. `outputStream` is required and accepts `stdout` or `stderr`. `extraction` is required. `minimum` is an optional non-empty string. When `minimum` is present, `comparison` is required. When present, `comparison` accepts `numeric-segments` or `semver`. These values indicate version formats; the schema does not compare actual versions or parse command output.

`extraction.method` is required and accepts:

| Method | Indicated output | Required additional property |
| --- | --- | --- |
| `entire-output` | The output contains the complete version. | None |
| `first-numeric-token` | The first numeric token indicates the version. | None |
| `last-numeric-token` | The last numeric token indicates the version. | None |
| `after-prefix` | The version follows a prefix. | Non-empty `prefix`. |
| `json-property` | A JSON property indicates the version. | Non-empty `property`. |

For a value such as `2.4.1-rc.1`, the numeric token methods can indicate `2.4.1` and `1` respectively. `entire-output` can indicate the complete string when the output contains only the version. The schema does not prescribe a path notation for `json-property` or how a consumer extracts, compares or reports versions. Each consumer documents the methods and notations it supports.

See [valid examples](examples/valid/) and [invalid examples](examples/invalid/). These examples use synthetic tools and values; they do not establish minimum supported versions for real software.

## Validation boundary

The schema validates all shared properties when present, including optional ones. It permits additional properties so an implementation can add its own fields and validate the same document with a complementary schema. Consequently, a misspelled optional property can be accepted as an additional property. The implementation author is responsible for spelling shared properties correctly and validating custom fields. Passing this schema alone does not validate the entire implementation-specific document.

The schema does not enforce uniqueness of `id` across requirement objects, authorize execution or installation, or verify that a documentation URI resolves. `format` checks for URI syntax depend on validator configuration; the test suite enables them explicitly.

## Local validation

Install [uv](https://docs.astral.sh/uv/) and run `tests/run-tests.sh` from the repository root. The runner installs the pinned test dependencies, checks the schema against the Draft 2020-12 metaschema, and validates positive and negative examples offline. Schema files and examples are read locally; dependency installation may require network access on the first run.
