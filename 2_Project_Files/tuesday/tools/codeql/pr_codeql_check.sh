#!/bin/bash
# pr_codeql_check.sh - local approximation of the hosted CodeQL PR check. See README.md.
# rc 0 pass | rc 1 would block (KEPT high+ or NEW high+) | rc 2 tool error. macOS bash 3.2 compatible.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
CQ="${CQ_CLI:-$ROOT/tools/codeql/codeql/codeql}"
LIB="$HERE/pr_codeql_lib.py"

usage() { echo "usage: $0 --repo <owner/name> --checkout <local clone, READ ONLY> --base <sha> --head <sha> --lang <javascript|python|csharp|java|go|ruby|cpp|swift> --work <scratch dir> [--allow-empty] [--fresh] [--threads N]" >&2; }
err() { echo "TOOL ERROR: $*" >&2; exit 2; }

REPO=""; CHECKOUT=""; BASE=""; HEAD=""; LANGN=""; WORK=""; ALLOW=""; FRESH=""; THREADS=4
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --checkout) CHECKOUT="$2"; shift 2 ;;
    --base) BASE="$2"; shift 2 ;;
    --head) HEAD="$2"; shift 2 ;;
    --lang) LANGN="$2"; shift 2 ;;
    --work) WORK="$2"; shift 2 ;;
    --threads) THREADS="$2"; shift 2 ;;
    --allow-empty) ALLOW="--allow-empty"; shift ;;
    --fresh) FRESH=1; shift ;;
    *) usage; err "unknown argument: $1" ;;
  esac
done
[ -n "$REPO" ] || { usage; err "missing --repo"; }
[ -n "$CHECKOUT" ] || { usage; err "missing --checkout"; }
[ -n "$BASE" ] || { usage; err "missing --base"; }
[ -n "$HEAD" ] || { usage; err "missing --head"; }
[ -n "$LANGN" ] || { usage; err "missing --lang"; }
[ -n "$WORK" ] || { usage; err "missing --work"; }
[ -x "$CQ" ] || err "CodeQL CLI not found at $CQ (set CQ_CLI)"
command -v python3 >/dev/null || err "python3 not found"
[ -d "$CHECKOUT" ] || err "checkout not a directory: $CHECKOUT"

EXTRA=""
case "$LANGN" in
  javascript) SUITE="codeql/javascript-queries:codeql-suites/javascript-security-extended.qls" ;;
  python|ruby|go|swift|cpp) SUITE="codeql/$LANGN-queries:codeql-suites/$LANGN-security-extended.qls" ;;
  csharp|java) SUITE="codeql/$LANGN-queries:codeql-suites/$LANGN-security-extended.qls"; EXTRA="--build-mode=none" ;;
  *) err "unsupported --lang $LANGN" ;;
esac

# Read-only git against the checkout. Resolve both shas to commits; git's own error is printed.
G() { git --no-optional-locks -C "$CHECKOUT" "$@"; }
BASE_FULL="$(G rev-parse --verify "$BASE^{commit}")" || err "base sha not resolvable in $CHECKOUT: $BASE (a scratch clone that holds the PR objects is the normal path)"
HEAD_FULL="$(G rev-parse --verify "$HEAD^{commit}")" || err "head sha not resolvable in $CHECKOUT: $HEAD (a scratch clone that holds the PR objects is the normal path)"

mkdir -p "$WORK/trees" "$WORK/db" "$WORK/sarif" "$WORK/logs" "$WORK/diff" || err "cannot create work dir $WORK"
echo "pr_codeql_check: repo=$REPO lang=$LANGN base=$BASE_FULL head=$HEAD_FULL cli=$("$CQ" version --format=terse 2>&1)"

export_tree() { # <sha>; nothing is deleted: a half-extracted tree of the same sha is simply overwritten
  local sha="$1" t="$WORK/trees/$1"
  [ -f "$t/.export_ok" ] && return 0
  mkdir -p "$t" || return 2
  G archive --format=tar -o "$WORK/trees/$sha.tar" "$sha" || { echo "git archive failed for $sha" >&2; return 2; }
  tar -xf "$WORK/trees/$sha.tar" -C "$t" || { echo "tar extract failed for $sha" >&2; return 2; }
  : > "$WORK/trees/$sha.tar"
  touch "$t/.export_ok"
}

build_db() { # <sha>
  local sha="$1" db="$WORK/db/$1-$LANGN" rc
  if [ -z "$FRESH" ] && [ -f "$db/.pr_codeql_ok" ] && [ "$(cat "$db/.pr_codeql_ok")" = "$sha $LANGN" ]; then
    echo "db $sha: reused ($db)"; return 0
  fi
  export_tree "$sha" || return 2
  echo "db $sha: building"
  "$CQ" database create "$db" --language="$LANGN" $EXTRA --source-root="$WORK/trees/$sha" --threads="$THREADS" --overwrite \
    > "$WORK/logs/dbcreate_$sha.log" 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "database create failed rc $rc, see $WORK/logs/dbcreate_$sha.log" >&2; tail -5 "$WORK/logs/dbcreate_$sha.log" >&2; return 2
  fi
  echo "$sha $LANGN" > "$db/.pr_codeql_ok"
}

analyze() { # <sha>
  local sha="$1" db="$WORK/db/$1-$LANGN" out="$WORK/sarif/$1-$LANGN.sarif" rc
  if [ -z "$FRESH" ] && [ -s "$out" ] && [ "$out" -nt "$db/.pr_codeql_ok" ]; then
    echo "sarif $sha: reused ($out)"; return 0
  fi
  echo "analyze $sha: $SUITE"
  "$CQ" database analyze "$db" "$SUITE" --format=sarif-latest --output="$out" --threads="$THREADS" --rerun \
    > "$WORK/logs/analyze_$sha.log" 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "database analyze failed rc $rc, see $WORK/logs/analyze_$sha.log" >&2; tail -5 "$WORK/logs/analyze_$sha.log" >&2; return 2
  fi
}

# One CodeQL process at a time: strictly sequential.
build_db "$BASE_FULL" || exit 2
analyze "$BASE_FULL" || exit 2
if [ "$HEAD_FULL" != "$BASE_FULL" ]; then
  build_db "$HEAD_FULL" || exit 2
  analyze "$HEAD_FULL" || exit 2
fi

# Diff pack: added-line ranges of head vs base (no rename detection: a moved file counts as added).
DIFF="$WORK/diff/$BASE_FULL..$HEAD_FULL.diff"
G diff --no-renames --no-color --no-ext-diff -U0 "$BASE_FULL" "$HEAD_FULL" > "$DIFF" || err "git diff failed"
python3 -I "$LIB" diffranges "$DIFF" "$WORK/diff/added_ranges.json" || exit 2

python3 -I "$LIB" verdict "$WORK/sarif/$HEAD_FULL-$LANGN.sarif" "$WORK/sarif/$BASE_FULL-$LANGN.sarif" \
  "$WORK/diff/added_ranges.json" "$WORK/verdict_$HEAD_FULL.json" $ALLOW
exit $?
