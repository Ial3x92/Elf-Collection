#!/usr/bin/env bash
set -euo pipefail

# Ensure .venv is activated (unless SKIP_VENV): python3 must resolve to mkpfs/.venv/bin/python3
# Set SKIP_VENV=1 to skip activating the venv
if [ -z "${SKIP_VENV:-}" ]; then
  pybin=$(which python3 2>/dev/null)
  if [[ ! "$pybin" =~ mkpfs/.venv/bin/python3$ ]]; then
    source .venv/bin/activate || { echo '[run-tests] ERROR: Could not activate .venv'; exit 1; }
  fi
fi

uv sync

# Install pre-commit hooks
git config --unset-all core.hooksPath || true
uv run pre-commit install --overwrite

# Run formatting and linting (automatically runs on commit)
uv run ruff format .

# Auto Fix
uv run ruff check . --fix

uv run --frozen pytest
