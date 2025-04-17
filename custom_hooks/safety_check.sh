#!/bin/bash
set -e

# Install poetry if not installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing..."
    curl -sSL https://install.python-poetry.org | python -
fi

# Install pip-audit if not installed
if ! command -v pip-audit &> /dev/null; then
    echo "Pip-audit is not installed. Installing..."
    pip install pip-audit
fi

# Export requirements and run pip-audit
poetry export --format requirements.txt > requirements-temp.txt && pip-audit --requirement requirements-temp.txt && rm requirements-temp.txt
