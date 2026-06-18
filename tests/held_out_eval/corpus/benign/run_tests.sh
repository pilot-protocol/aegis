#!/bin/sh
# Run the full test suite with coverage. POSIX sh so it works in CI containers.
set -e

echo "Linting..."
ruff check src/

echo "Type checking..."
mypy src/

echo "Running unit tests..."
pytest --cov=src --cov-report=term-missing --maxfail=1 -q

echo "All checks passed."
