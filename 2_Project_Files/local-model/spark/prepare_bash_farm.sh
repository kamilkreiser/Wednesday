#!/bin/bash
# prepare_bash_farm.sh <clone-dir> <tip> [service_dir]  — OPT-IN node farm + packages/shared build for the BASH tiers (2026-11-10, o128).
# WHY: round.sh runs tasks/code_patch/prepare_clone.sh (node_modules farm + `tsc` build of packages/shared in the clone) only for
# code_patch, code_patch2, test_only and test_only_input. The bash tiers (bash_patch2, test_only_bash) got a BARE clone: no
# packages/shared/dist, no node_modules. A bash suite that drives node (KS-1145 item 2, scripts/__tests__/ks949_main_seed_idempotence.test.sh:
# `die "packages/shared is not built"`, then `tsx not installed`) therefore failed on EVERY round for a reason that is the
# harness's, never the model's. MEASURED 2026-11-10 07:3x on a bare clone at d0b4825cc244: rc 1, "0 passed, 1 failed (of 27 cells) — aborted".
# It reuses prepare_clone.sh unchanged (symlink farm FROM the cache's node_modules — themselves links into spark/cache/deps — then
# `npx tsc -p .` of packages/shared inside the clone) by writing the small input.json that script reads.
# Called by round.sh ONLY when the brief dir holds a file named spark.farm (presence = opt in; optional line `service_dir=services/<x>`),
# and only for the bash tiers. No spark.farm = no call = every existing bash round is byte-for-byte what it was.
# Never writes outside <clone-dir> and its sibling prepare_clone.shared_build.out. No cd. stderr kept.
# Exit 0 ready (and dist/index.js + .bin/tsx asserted present) · 1 a precondition or the build failed.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM="$(dirname "$HERE")"
CLONE="${1:-}"; TIP="${2:-}"; SERVICE="${3:-services/auth}"
SRC="${SPARK_SRC:-$HERE/cache/src}"
SUBDIR="Blockchain/Dev"
[ -n "$CLONE" ] && [ -n "$TIP" ] && [ -d "$CLONE/.git" ] || { echo "usage: prepare_bash_farm.sh <clone-dir> <tip> [service_dir]" >&2; exit 1; }
IN="$CLONE/../prepare_bash_farm.input.json"
python3 - "$IN" "$SRC" "$TIP" "$SUBDIR" "$SERVICE" <<'PY' || exit 1
import json, sys
p, src, tip, sub, svc = sys.argv[1:6]
json.dump({"source_checkout": src, "tip": tip, "repo_subdir": sub, "service_dir": svc,
           "shared_pkg_dir": "packages/shared", "shared_pkg_name": "@secuura/shared"}, open(p, "w"))
PY
bash "$LM/tasks/code_patch/prepare_clone.sh" "$IN" "$CLONE" || { echo "prepare_bash_farm: prepare_clone.sh failed" >&2; exit 1; }
[ -f "$CLONE/$SUBDIR/packages/shared/dist/index.js" ] || { echo "prepare_bash_farm: packages/shared/dist/index.js absent after the build" >&2; exit 1; }
[ -x "$CLONE/$SUBDIR/node_modules/.bin/tsx" ] || { echo "prepare_bash_farm: node_modules/.bin/tsx absent or not executable after the farm" >&2; exit 1; }
echo "bash farm ready: shared dist + tsx present in $CLONE"
