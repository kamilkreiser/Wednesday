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
if [ -f "${1:-}" ] && [ "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("runner",""))' "$1")" = bash ]; then
  TIP_="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["tip"])' "$1")"
  [ -d "${2:-}/.git" ] || { echo "usage: prepare_clone.sh <input.json> <clone-dir>   (clone must exist)" >&2; exit 1; }
  HEAD_="$(git -C "$2" rev-parse HEAD)"
  [ "$HEAD_" = "$TIP_" ] || { echo "prepare_clone: clone HEAD $HEAD_ != pinned tip $TIP_" >&2; exit 1; }
  echo "clone HEAD == pinned tip $TIP_; runner bash — no node farm, no shared build (the suite runs on the bare clone)"
  exit 0
fi
exec bash "$(cd "$(dirname "$0")" && pwd)/../code_patch/prepare_clone.sh" "$@"
