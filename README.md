# Schemas

Schemas maintains and distributes reusable schemas that validate structured documents and help developers create them in compatible IDEs.

The first schema describes an [external requirements manifest](json-schema/external-requirements/README.md) for executable requirements, including optional provisioning sources. It is under development and has not been published.

Its canonical identifier uses `schemas.eviweb.fr`; schema retrieval from that domain is not configured. The schema documentation explains how identity differs from a Git commit reference.

Run `tests/run-tests.sh` to validate the schema and its examples. This requires [uv](https://docs.astral.sh/uv/) and downloads pinned Python test dependencies on the first run.

GitHub Actions runs the same validation on pushes, pull requests and manual requests.

## Schema revisions

| Schema | Revision | Git reference |
| --- | --- | --- |
| External requirements | 1.0.0 | [Schema at commit `19740cd145dec6eb45a587484efbbfb0199e6a84`](https://raw.githubusercontent.com/eviweb/schemas/19740cd145dec6eb45a587484efbbfb0199e6a84/json-schema/external-requirements/external-requirements.schema.json) |

The GitHub URL requires repository access while the repository is private. The schema revision is independent of the repository release version.

## Project profile

This project uses the strict Git workflow: changes go through pull requests, with required checks and reviews before merging.

## License

This project is licensed under the [MIT License](LICENSE.md).
