#!/bin/bash
# probe_verdict.sh — the DRAFTER's cheap re-derivation of s214's PROOF 1 / PROOF 2 / PROOF 3 shape (the verdict line of
# preflight.sh on a closed gateway) WITHOUT running the real 15-leg gate: the fixture recipe of preflight_deps.test.sh at
# 5341b1dae (preflight_fixture_run, :283-431) copied verbatim — every delegated leg stubbed, one passing fixture suite, a
# slot stub that exports one variable, GATEWAY_URL=http://127.0.0.1:1 — applied to ANY preflight.sh version handed in.
# Prints the verdict lines, the rc and the SKIP counts. Never touches a checkout; builds under $TMPDIR (set it INSIDE the set).
# Usage: probe_verdict.sh <preflight.sh> <run-shell-suites.sh> <strict 0|1> <label>
set -u
PF="${1:?preflight.sh}"; RSS="${2:?run-shell-suites.sh}"; STRICT="${3:?strict}"; LABEL="${4:?label}"
tmp="$(mktemp -d "${TMPDIR:-/tmp}/probe-verdict.XXXXXX")"
dev="$tmp/Blockchain/Dev"
mkdir -p "$dev/scripts/preflight" "$dev/scripts/audit" "$dev/scripts/__tests__" "$tmp/systemTest"
cp "$PF" "$dev/scripts/preflight/preflight.sh"
printf '#!/usr/bin/env bash\nexit 0\n' > "$dev/scripts/preflight/deps-present.sh"
printf '#!/usr/bin/env bash\nexit 0\n' > "$dev/scripts/preflight/lockfile-cleanroom.sh"
printf '#!/usr/bin/env bash\nexit 0\n' > "$dev/scripts/preflight/no-tracked-credentials.sh"
cp "$RSS" "$dev/scripts/"
printf '#!/usr/bin/env bash\nexit 0\n' > "$dev/scripts/preflight/bare-path-scripts-executable.sh"
printf '#!/usr/bin/env bash\nexit 0\n' > "$dev/scripts/preflight/action-pins-labelled.sh"
printf '#!/usr/bin/env bash\nexit 0\n' > "$dev/scripts/check-shared-relink.sh"
printf '#!/usr/bin/env bash\necho "OK — 0 code guards (fixture stub)"\nexit 0\n' > "$dev/scripts/run-code-guards.sh"
printf '0\n' > "$dev/scripts/audit/expected-case-count"
printf 'console.log("audit-gate stub");process.exit(0);\n' > "$dev/scripts/audit/audit-gate.mjs"
printf 'console.log("audit-locks stub");process.exit(0);\n' > "$dev/scripts/audit/audit-locks.mjs"
mkdir -p "$dev/scripts/audit/node_modules/semver"
printf '{"name":"x","scripts":{"check:openapi":"true","audit:contract":"echo \\"# tests 0\\""}}\n' > "$dev/package.json"
printf '#!/usr/bin/env bash\necho "fixture stub suite"\nexit 0\n' > "$dev/scripts/__tests__/fixture_stub.test.sh"
printf '#!/usr/bin/env bash\nexport FIXTURE_SLOT_VAR=1\n' > "$tmp/systemTest/slot-target.sh"
echo "== $LABEL: preflight.sh sha256 $(shasum -a 256 "$PF" | cut -c1-16), strict=$STRICT, fixture $tmp"
out=$( cd "$dev" && GATEWAY_URL="http://127.0.0.1:1" PREFLIGHT_STRICT_LEGS="$STRICT" bash scripts/preflight/preflight.sh 2>&1 ); rc=$?
printf '%s\n' "$out" > "$tmp/run.out"
echo "rc=$rc  step banners=$(printf '%s\n' "$out" | /usr/bin/grep -c '^=== ')  SKIP-stack lines=$(printf '%s\n' "$out" | /usr/bin/grep -c '^SKIP — local stack not up')  SKIP-advisory lines=$(printf '%s\n' "$out" | /usr/bin/grep -c 'SKIP (advisory)')"
echo "verdict lines:"
printf '%s\n' "$out" | /usr/bin/grep -E 'PREFLIGHT (PASSED|INCOMPLETE|FAILED|ABORTED)|refusing to pass|^  legs|Nothing failed|This is NOT a pass' | sed 's/^/  | /'
echo "run.out kept at $tmp/run.out"
exit 0
