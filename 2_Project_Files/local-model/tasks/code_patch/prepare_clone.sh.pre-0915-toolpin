#!/bin/bash
# prepare_clone.sh <input.json> <clone-dir> — code_patch task type
#
# Symlink-farm the SOURCE checkout's installed node_modules into a scratch
# clone pinned at the input's `tip`, then build the shared package in the
# clone (its dist is gitignored and the source's copy may be stale). This is
# the established gate practice ("node_modules symlink-farmed FROM the
# builder's worktree — from it, never into it"): every entry is a symlink
# INTO the source's node_modules except the write-prone ones (`.vite`,
# `.package-lock.json`) which become real, clone-local directories, so
# vitest's cache and any install bookkeeping never land in the source.
#
# The clone must already exist at the pinned tip (the caller made it with
# `git clone --shared --no-checkout <source> <clone>` +
# `git -C <clone> checkout --detach <tip>` — both in the scratchpad).
# Never runs npm install. Never writes into the source. Idempotent.
#
# exit 0 = ready, 1 = a precondition failed. stderr never discarded.
set -uo pipefail

INPUT="${1:-}"
CLONE="${2:-}"
if [ -z "$INPUT" ] || [ -z "$CLONE" ] || [ ! -f "$INPUT" ] || [ ! -d "$CLONE/.git" ]; then
  echo "usage: prepare_clone.sh <input.json> <clone-dir>   (clone must exist)" >&2
  exit 1
fi

field() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$INPUT" "$1"; }
SOURCE="$(field source_checkout)"
TIP="$(field tip)"
SUBDIR="$(field repo_subdir)"        # e.g. Blockchain/Dev
SERVICE="$(field service_dir)"       # e.g. services/auth   (relative to SUBDIR)
SHARED="$(field shared_pkg_dir)"     # e.g. packages/shared (relative to SUBDIR)
SHARED_NAME="$(field shared_pkg_name)"  # e.g. @secuura/shared

HEAD_SHA="$(git -C "$CLONE" rev-parse HEAD)"
if [ "$HEAD_SHA" != "$TIP" ]; then
  echo "prepare_clone: clone HEAD $HEAD_SHA != pinned tip $TIP" >&2
  exit 1
fi
echo "clone HEAD == pinned tip $TIP"

farm() {
  # farm <source node_modules dir> <clone node_modules dir> [skip-name ...]
  local src="$1" dst="$2"; shift 2
  if [ ! -d "$src" ]; then echo "prepare_clone: no source node_modules at $src" >&2; return 1; fi
  mkdir -p "$dst"
  local n_link=0 n_skip=0 name
  while IFS= read -r name; do
    [ -z "$name" ] && continue
    local skip=0 s
    for s in "$@"; do [ "$name" = "$s" ] && skip=1; done
    if [ "$skip" -eq 1 ]; then n_skip=$((n_skip+1)); continue; fi
    if [ ! -e "$dst/$name" ] && [ ! -L "$dst/$name" ]; then
      ln -s "$src/$name" "$dst/$name"
    fi
    n_link=$((n_link+1))
  done < <(ls -A "$src")
  echo "farmed $dst: $n_link linked, $n_skip skipped (real clone-local dirs instead)"
  return 0
}

ROOT_SRC="$SOURCE/$SUBDIR/node_modules"
ROOT_DST="$CLONE/$SUBDIR/node_modules"
# @secuura (the workspace scope) is rebuilt as a REAL dir so the shared package
# resolves to the CLONE's copy (built below at the tip), not the source's.
SCOPE="${SHARED_NAME%%/*}"
farm "$ROOT_SRC" "$ROOT_DST" .vite .package-lock.json "$SCOPE" || exit 1
mkdir -p "$ROOT_DST/.vite" "$ROOT_DST/$SCOPE"
farm "$ROOT_SRC/$SCOPE" "$ROOT_DST/$SCOPE" "${SHARED_NAME#*/}" || exit 1
if [ ! -L "$ROOT_DST/$SHARED_NAME" ]; then
  ln -s "../../$SHARED" "$ROOT_DST/$SHARED_NAME"
fi
echo "$SHARED_NAME -> $(readlink "$ROOT_DST/$SHARED_NAME") (clone-local)"

for ws in "$SERVICE" "$SHARED"; do
  if [ -d "$SOURCE/$SUBDIR/$ws/node_modules" ]; then
    farm "$SOURCE/$SUBDIR/$ws/node_modules" "$CLONE/$SUBDIR/$ws/node_modules" .vite .package-lock.json || exit 1
    mkdir -p "$CLONE/$SUBDIR/$ws/node_modules/.vite"
  fi
done

# Build the shared package in the clone (tsc from the farmed node_modules).
BUILD_OUT="$CLONE/../prepare_clone.shared_build.out"
(cd "$CLONE/$SUBDIR/$SHARED" && npx tsc -p . ) > "$BUILD_OUT" 2>&1
rc=$?
if [ "$rc" -ne 0 ]; then
  echo "prepare_clone: shared build FAILED rc=$rc — see $BUILD_OUT" >&2
  tail -20 "$BUILD_OUT" >&2
  exit 1
fi
echo "shared built in clone: $(ls "$CLONE/$SUBDIR/$SHARED/dist" | wc -l | tr -d ' ') dist entries"

# Guard: nothing landed in the source. `git status` there is a READ verb.
SRC_DIRTY="$(git -C "$SOURCE" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
echo "source checkout tracked-modified count after prepare: $SRC_DIRTY (must equal what it was before — the caller compares)"
exit 0
