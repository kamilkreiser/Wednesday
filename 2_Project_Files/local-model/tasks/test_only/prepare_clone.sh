#!/bin/bash
# prepare_clone.sh <input.json> <clone-dir> — test_only task type (2026-09-18)
#
# The test_only input carries the same clone keys as a code_patch input (source_checkout, tip, repo_subdir, service_dir,
# shared_pkg_dir, shared_pkg_name — written by build_test_only_input.sh), and the runner needs the same farm: the source
# checkout's node_modules symlink-farmed INTO the clone ("from it, never into it") and the shared package built in the
# clone. So this is the code_patch script, called unchanged — one farm, not two copies that drift. night_run.sh runs
# `$TDIR/prepare_clone.sh` for a pinned task=…/tasks/test_only/task.md, which is this file. rc and output are its.
set -uo pipefail
# 2026-09-18 18:xx (bash runner): a `runner: bash` input runs a *.test.sh suite with /bin/bash from the clone root. It
# needs no node farm and no shared build; farming the source's node_modules would make the clone NOT the tree the suite
# claims to pin (a suite that silently needs an install must go red at T5, not pass on a borrowed install). Clone check
# only, then rc 0.
# 2026-09-22 15:5x (bash FARM, opt-in; KS-1145 / the ks949 suite, feed15): a bash input whose JSON carries `farm`
# (written by the builder from the brief's `Farm: \`shared+tsx\`` header line; tokens from {shared, tsx}) is routed
# through the code_patch farm INSTEAD of the bare clone: `tsx` = the source's node_modules symlink-farmed into the clone
# (never into the source), `shared` = that farm plus packages/shared built in the clone (the builder sets shared_pkg_dir
# for it; the code_patch script builds only when shared_pkg_dir is non-empty). After the farm the suite's own
# preconditions are asserted here, one line each (`<subdir>/node_modules/.bin/tsx` executable; `<shared>/dist/index.js`
# present) — rc 1 naming the missing one. An input without `farm` takes the 2026-09-18 path unchanged; a `farm` value
# outside the token set is REFUSED (rc 1) — the builder never writes one, so it is a hand-edited input.
if [ -f "${1:-}" ] && [ "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("runner",""))' "$1")" = bash ]; then
  TIP_="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["tip"])' "$1")"
  [ -d "${2:-}/.git" ] || { echo "usage: prepare_clone.sh <input.json> <clone-dir>   (clone must exist)" >&2; exit 1; }
  HEAD_="$(git -C "$2" rev-parse HEAD)"
  [ "$HEAD_" = "$TIP_" ] || { echo "prepare_clone: clone HEAD $HEAD_ != pinned tip $TIP_" >&2; exit 1; }
  FARM_="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("farm",""))' "$1")"
  if [ -z "$FARM_" ]; then
    echo "clone HEAD == pinned tip $TIP_; runner bash — no node farm, no shared build (the suite runs on the bare clone)"
    exit 0
  fi
  case "$FARM_" in shared|tsx|shared+tsx) ;; *) echo "prepare_clone: REFUSED — farm '$FARM_' is not a farm token set (shared, tsx, shared+tsx); the builder never writes this value" >&2; exit 1 ;; esac
  SUBDIR_="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["repo_subdir"])' "$1")"
  SHARED_="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("shared_pkg_dir",""))' "$1")"
  case "$FARM_" in *shared*) [ -n "$SHARED_" ] || { echo "prepare_clone: REFUSED — farm '$FARM_' names shared but shared_pkg_dir is empty (the builder sets it; hand-edited input?)" >&2; exit 1; } ;; esac
  echo "clone HEAD == pinned tip $TIP_; runner bash — FARM '$FARM_' (opt-in by the brief's Farm: line): routing through the code_patch farm (node_modules symlink-farmed FROM the source into the clone$( [ -n "$SHARED_" ] && printf '%s' "; $SHARED_ built in the clone" ))"
  bash "$(dirname "$0")/../code_patch/prepare_clone.sh" "$@"
  frc=$?
  [ "$frc" -eq 0 ] || { echo "prepare_clone: the farm failed rc=$frc" >&2; exit 1; }
  case "$FARM_" in *tsx*) if [ -x "$2/$SUBDIR_/node_modules/.bin/tsx" ]; then echo "farm check: $SUBDIR_/node_modules/.bin/tsx executable — ok"; else echo "prepare_clone: farm '$FARM_' — $SUBDIR_/node_modules/.bin/tsx is NOT executable in the clone after the farm" >&2; exit 1; fi ;; esac
  case "$FARM_" in *shared*) if [ -f "$2/$SUBDIR_/$SHARED_/dist/index.js" ]; then echo "farm check: $SUBDIR_/$SHARED_/dist/index.js present — ok"; else echo "prepare_clone: farm '$FARM_' — $SUBDIR_/$SHARED_/dist/index.js is MISSING in the clone after the build" >&2; exit 1; fi ;; esac
  exit 0
fi
exec bash "$(cd "$(dirname "$0")" && pwd)/../code_patch/prepare_clone.sh" "$@"
