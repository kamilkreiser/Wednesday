#!/bin/bash
# prepare_clone.sh <input.json> <clone-dir> — test_only task type (2026-09-18)
#
# The test_only input carries the same clone keys as a code_patch input (source_checkout, tip, repo_subdir, service_dir,
# shared_pkg_dir, shared_pkg_name — written by build_test_only_input.sh), and the runner needs the same farm: the source
# checkout's node_modules symlink-farmed INTO the clone ("from it, never into it") and the shared package built in the
# clone. So this is the code_patch script, called unchanged — one farm, not two copies that drift. night_run.sh runs
# `$TDIR/prepare_clone.sh` for a pinned task=…/tasks/test_only/task.md, which is this file. rc and output are its.
set -uo pipefail
exec bash "$(cd "$(dirname "$0")" && pwd)/../code_patch/prepare_clone.sh" "$@"
