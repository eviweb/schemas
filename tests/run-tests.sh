#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

command -v uv >/dev/null 2>&1 || {
  echo "Error: uv is required to run the schema tests" >&2
  exit 127
}

cd "$PROJECT_DIR"
uv run --no-project --with-requirements requirements-test.txt pytest -q tests/
