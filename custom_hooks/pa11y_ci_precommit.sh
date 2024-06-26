#!/bin/bash
set +e

if [ "$CI" = "true" ]; then exit 0; fi

export $(grep -v '^#' .env.e2e_tests | xargs)
OUTPUT=$(npx pa11y-ci --config configs/pa11y_ci_precommit.js)
echo "${OUTPUT}"

set -e
