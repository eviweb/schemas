# External requirements schema

This [Draft 2020-12 schema](external-requirements.schema.json) validates the shared structure of `external-requirements.json`. Version 1 describes external executable requirements. It supports validation and authoring assistance in compatible IDEs. It does not execute probes or check whether an executable exists.

The schema declares the canonical identifier `https://schemas.eviweb.fr/external-requirements/1.0.0/schema.json`. This identifies schema revision 1.0.0 independently of the repository release version. The domain is not configured for schema retrieval; the identifier alone does not make the file available over HTTP. A GitHub URL containing a full commit ID must be selected and tested before release. The optional manifest `$schema` property can contain a relative URI reference during local development.

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
| `provisioning` | No | Object describing one or more installation sources. |
| `documentationUrl` | No | Non-empty absolute URI to documentation. |

`executable.candidates` is a required, non-empty, ordered array of distinct, non-empty strings. Each string indicates an executable name or absolute path. The schema does not validate path syntax or executable availability.

When present, `provisioning.sources` is a required non-empty array. Each source requires a non-empty `provider` and provider-specific `reference`. The provider list is open. Identical source objects are rejected; sources with the same provider and reference but different additional properties are not detected as duplicates.

```json
"provisioning": {
  "sources": [{"provider": "apt", "reference": "zbar-tools"}]
}
```

Sources identify installation options; they do not authorize installation or establish that a package is available. Consumers choose providers and their priority, verify references, and manage authorization, privileges, previews, failure handling and subsequent executable checks. The schema does not enforce these actions or infer a package from an executable name.

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

An implementation can validate the same manifest with its own complementary schema to check custom fields. Both validations must succeed for the manifest to satisfy both schemas. Consumers remain responsible for detecting duplicate IDs and for any stricter checks they require.

## Compatibility and schema references

Within manifest major version 1, new schema revisions aim to continue accepting manifests valid under previous published v1 revisions. Changes that reject previously valid manifests or change the meaning of shared fields require a new major version. Compare changes against representative earlier examples before publication.

Forward compatibility is not guaranteed: an older validator can reject a new enum value even if a newer v1 schema accepts it. Adding a shared property can also conflict with a custom property already used under that name. Review additions against known consumers and document their impact. Consumers choose which methods and custom properties to support.

`schemaVersion` identifies the manifest's major format, while the repository release and Git commit identify a specific schema revision. For reproducible validation, use a full commit ID and the path at that commit. The release registry will distinguish the first published version from any later recommended revision. These GitHub references depend on the repository and referenced commit remaining available.

The canonical `$id` identifies this schema revision and supplies its base URI. A future revision with different constraints should use a distinct identifier. Register a local copy under this identifier when resolving references offline. Retrieval and editor behavior must be checked before publication.

## Local validation

Install [uv](https://docs.astral.sh/uv/) and run `tests/run-tests.sh` from the repository root. The runner installs the pinned test dependencies, checks the schema against the Draft 2020-12 metaschema, and validates positive and negative examples offline. Schema files and examples are read locally; dependency installation may require network access on the first run.
