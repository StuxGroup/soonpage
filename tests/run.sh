#!/bin/bash
# Soonpage - test suite
# Usage: bash tests/run.sh
# Plain Python unittest, no dependencies: the version, the changelog page's parser (needs
# Node.js, skipped without it), the Discord link previews and the icon set.
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY=""
for candidate in python3 python; do
    if "$candidate" -c 'import sys; sys.exit(sys.version_info < (3, 8))' >/dev/null 2>&1; then PY="$candidate"; break; fi
done
if [ -z "$PY" ]; then
    echo "Python 3.8+ is needed to run the tests." >&2
    exit 1
fi

# -B: no __pycache__ left in the site (GitHub Pages publishes the whole folder)
exec "$PY" -B -m unittest discover -s "$DIR" -p 'test_*.py' "$@"
