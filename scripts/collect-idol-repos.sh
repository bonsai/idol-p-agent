#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/data"
mkdir -p "$OUT"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

command -v gh >/dev/null || { echo "gh CLI is required" >&2; exit 1; }
command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }

strip_ansi() {
  sed -E $'s/\033\\[[0-9;]*[[:alpha:]]//g'
}

echo "Discovering bonsai/idol-* repositories..." >&2
# gh search is used instead of an organization endpoint because bonsai may be a user account.
gh search repos idol --owner bonsai --limit 100 --json name,url,description,updatedAt,isArchived,isPrivate,visibility \
  | strip_ansi \
  | jq 'map(select(.name == "idol" or (.name | startswith("idol-")))) | sort_by(.name)' > "$TMP/repos.json"

: > "$OUT/repos.jsonl"
while IFS= read -r repo; do
  name="$(jq -r '.name' <<<"$repo")"
  echo "Collecting $name" >&2
  meta="$(gh api "repos/bonsai/$name" | strip_ansi)"
  default_branch="$(jq -r '.default_branch' <<<"$meta")"
  is_private="$(jq -r '.private // false' <<<"$meta")"
  sha=""
  readme=""
  tree='[]'
  # idol-p-agent is public: retain private repo metadata for inventory, but never
  # copy private README, commit, or file-tree contents into the public snapshot.
  if [[ "$is_private" != "true" ]]; then
    sha="$(gh api "repos/bonsai/$name/commits/$default_branch" 2>/dev/null | strip_ansi | jq -r '.sha // ""' || true)"
    if readme_json="$(gh api "repos/bonsai/$name/readme" 2>/dev/null | strip_ansi)"; then
      readme="$(jq -r '.content // ""' <<<"$readme_json" | tr -d '\n' | base64 -d 2>/dev/null || true)"
    fi
    tree_payload="$(gh api "repos/bonsai/$name/git/trees/$default_branch?recursive=1" 2>/dev/null | strip_ansi || true)"
    if [[ -n "$tree_payload" ]] && jq -e . >/dev/null 2>&1 <<<"$tree_payload"; then
      tree="$(jq -c '[.tree[]? | select(.type == "blob") | .path] | .[0:200]' <<<"$tree_payload")"
    fi
  fi
  jq -nc \
    --argjson meta "$meta" \
    --arg sha "$sha" \
    --arg readme "$readme" \
    --argjson tree "$tree" \
    --arg collected_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '$meta + {commit_sha:$sha, readme:$readme, files:$tree, collected_at:$collected_at}' \
    >> "$OUT/repos.jsonl"
done < <(jq -c '.[]' "$TMP/repos.json")

echo "Wrote $(wc -l < "$OUT/repos.jsonl") repositories to $OUT/repos.jsonl" >&2
