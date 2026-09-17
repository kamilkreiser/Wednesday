#!/bin/bash
# prepare_clone.sh <input.json> <clone-dir> — comment_patch task type (2026-09-17)
#
# The checker runs no suite and no tsc; its one dependency is the TypeScript PARSER for C4. So the clone gets exactly
# one entry: <clone>/<repo_subdir>/node_modules/typescript -> the SOURCE checkout's installed package (a symlink INTO the
# source, never a write into it — the code_patch "farm from it, never into it" practice, narrowed to the one package).
# An existing node_modules in the clone (a code_patch farm of the same clone) is left as it is.
# The clone must already exist at the pinned tip (night_run.sh makes it). Never runs npm. Idempotent. rc 0 ready · 1 not.
set -uo pipefail
INPUT="${1:-}"; CLONE="${2:-}"
[ -f "$INPUT" ] && [ -d "$CLONE/.git" ] || { echo "usage: prepare_clone.sh <input.json> <clone-dir>   (clone must exist)" >&2; exit 1; }
read_json() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(eval(sys.argv[2], {}, {"d": d}))' "$INPUT" "$1"; }
SOURCE="$(read_json 'd["repo"]["source_checkout"]')"
TIP="$(read_json 'd.get("tip") or d["repo"]["tip"]')"
SUBDIR="$(read_json 'd.get("repo_subdir","Blockchain/Dev")')"
HEAD_SHA="$(git -C "$CLONE" rev-parse HEAD)"
[ "$HEAD_SHA" = "$TIP" ] || { echo "prepare_clone: clone HEAD $HEAD_SHA != pinned tip $TIP" >&2; exit 1; }
SRC_TS="$SOURCE/$SUBDIR/node_modules/typescript"
DST_NM="$CLONE/$SUBDIR/node_modules"
[ -f "$SRC_TS/package.json" ] || { echo "prepare_clone: no typescript package at $SRC_TS" >&2; exit 1; }
mkdir -p "$DST_NM"
if [ -e "$DST_NM/typescript" ] || [ -L "$DST_NM/typescript" ]; then echo "typescript already present in the clone: $(readlink "$DST_NM/typescript" 2>/dev/null || echo 'a real directory')"
else ln -s "$SRC_TS" "$DST_NM/typescript" && echo "linked $DST_NM/typescript -> $SRC_TS"; fi
V="$(/opt/homebrew/bin/node -e 'process.stdout.write(require(process.argv[1]).version)' "$DST_NM/typescript" 2>&1)" || { echo "prepare_clone: typescript does not load from the clone: $V" >&2; exit 1; }
echo "clone at $TIP; typescript $V loads from $DST_NM/typescript"
exit 0
