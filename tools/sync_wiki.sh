#!/usr/bin/env bash
set -euo pipefail

# Sync docs/wiki/*.md into the GitHub Wiki for this repo.
# Usage:
#   ./tools/sync_wiki.sh
#   COMMIT_DATE="2024-02-23 10:10:00 -0500" ./tools/sync_wiki.sh

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [[ -z "${ROOT}" ]]; then
  echo "Error: not inside a git repository" >&2
  exit 1
fi

cd "$ROOT"
if [[ ! -d docs/wiki ]]; then
  echo "Error: docs/wiki not found" >&2
  exit 1
fi

ORIGIN_URL=$(git config --get remote.origin.url || true)
if [[ -z "${ORIGIN_URL}" ]]; then
  echo "Error: remote 'origin' not configured" >&2
  exit 1
fi

# Derive wiki URL from HTTPS or SSH origin
if [[ "${ORIGIN_URL}" == https://* ]]; then
  WIKI_URL="${ORIGIN_URL%.git}.wiki.git"
elif [[ "${ORIGIN_URL}" == git@*:* ]]; then
  # git@github.com:user/repo.git -> git@github.com:user/repo.wiki.git
  WIKI_URL="${ORIGIN_URL%.git}.wiki.git"
else
  echo "Error: unsupported remote URL format: ${ORIGIN_URL}" >&2
  exit 1
fi

TMP_DIR=$(mktemp -d)
cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

git clone "$WIKI_URL" "$TMP_DIR"
cp -f docs/wiki/*.md "$TMP_DIR"/

pushd "$TMP_DIR" >/dev/null
git config user.name "$(git -C "$ROOT" config --get user.name || echo 'RAG_QA')"
git config user.email "$(git -C "$ROOT" config --get user.email || echo 'noreply@example.com')"

if [[ -n "${COMMIT_DATE:-}" ]]; then
  GIT_AUTHOR_DATE="$COMMIT_DATE" GIT_COMMITTER_DATE="$COMMIT_DATE" git add .
  GIT_AUTHOR_DATE="$COMMIT_DATE" GIT_COMMITTER_DATE="$COMMIT_DATE" git commit -m "wiki: sync from docs/wiki"
else
  git add .
  git commit -m "wiki: sync from docs/wiki" || echo "Nothing to commit"
fi

# Try master then main (wikis commonly use master)
git push origin HEAD:master || git push origin HEAD:main
popd >/dev/null

echo "Wiki sync complete: $WIKI_URL"

