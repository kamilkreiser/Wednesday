#!/usr/bin/env bash
# =============================================================================
# CHECK: the gated services' TEST files still type-check against their baseline (KS-1487 / KS-1000)
# =============================================================================
# Why this exists.
#
# A gated service's tsconfig.json excludes src/__tests__ (every gated service's does), so
# `tsc -p tsconfig.json` ("npm run build") has never examined a test file:
# a "tsc: 0 errors" line over a test-only change is a green that could not fail. KS-1000 added
# scripts/typecheck-tests/check.cjs, which runs the same compiler over the service's
# tsconfig.test.json and compares the result to a recorded baseline that can only shrink: a new error
# fails, and so does a baseline entry that no longer reproduces.
#
# Until this leg, nothing at the gate ran it. The auth and api-gateway vitest suites do (each has a cell
# that shells out to the checker), so it was enforced by convention - "run the suite as the final
# check" - and not at push time. A push that added a test-file type error went through and was found
# later. A ratchet nothing runs at the gate is decoration; this is the run.
#
# What it does: runs `node scripts/typecheck-tests/check.cjs <service>` for each service given (default: each
# gated service, the list below; auth and api-gateway about 2.6 to 3.2 s each, measured) and fails if ANY of them
# exits non-zero. It does not stop at the first failure, so one push shows every service that is red.
# The checker's exit codes are 0 pass, 1 a new error or a stale baseline entry, 2 it could not run,
# examined nothing (KS-676's shape: a clean report over an empty file set) or has no baseline to read. All three non-zero outcomes
# fail this leg: a ratchet that did not run is not a pass.
#
# One precondition is NOT a failure of this leg: no workspace install. The checker resolves `tsc` from the
# install, and without one it can only say "run npm ci". That is an environment condition, and leg 1 already
# refuses it (deps-present.sh), so this leg prints SKIP (advisory) and exits 0 rather than add a second red
# for the same cause. preflight.sh runs this leg through run_delegated(), so the verdict counts that as a
# SKIPPED leg, not a run one. The skip lets nothing through: leg 1 has already refused the push.
#
# To gate another service, give it a tsconfig.test.json and a baseline (`check.cjs <svc> --init`), then
# add it to the default below. Services come in as ARGUMENTS and no environment variable is read, so
# nothing a caller exported can quietly point the gate at a clean directory (the KS-1261 class).
#
# bash 3.2 compatible on purpose: macOS ships 3.2 (KS-676).
#
# Usage:  bash scripts/preflight/test-types-ratchet.sh [<service-dir> ...]      (default: services/auth services/api-gateway services/vc-issuer services/security services/m365-integration)
# =============================================================================

set -uo pipefail

DEV_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$DEV_ROOT" || { echo "FAIL — cannot enter $DEV_ROOT"; exit 1; }

if [ "$#" -eq 0 ]; then
    set -- services/auth services/api-gateway services/vc-issuer services/security services/m365-integration
fi

# The same precondition leg 1 establishes (and the same variable it honours, so a fixture can aim it).
if ! bash scripts/preflight/deps-present.sh >/dev/null 2>&1; then
    echo "SKIP (advisory) — the workspace install is absent or incomplete, so the compiler this check needs is not there."
    echo "  Leg 1 reports the install problem and refuses the push. Run 'npm ci' in Blockchain/Dev, then push again."
    exit 0
fi

failed=0
for svc in "$@"; do
    node scripts/typecheck-tests/check.cjs "$svc"
    rc=$?
    if [ "$rc" -ne 0 ]; then
        failed=$((failed + 1))
        case "$rc" in
            1) why="a NEW test-file type error, a swap, a baseline entry that no longer reproduces, a tsc diagnostic with no file, a @ts-nocheck, or a fallen examined-test-files floor" ;;
            2) why="the check could not run, examined no test file (a clean result would say nothing), or the baseline cannot be trusted (missing, count-only, unparseable, no floor line, a duplicate line)" ;;
            *) why="an unexpected exit" ;;
        esac
        echo "FAIL — $svc: the test-file type-check ratchet exited $rc: $why."
    fi
done

if [ "$failed" -ne 0 ]; then
    echo ""
    echo "  The lines above name the cause. For a type error, fix it in the file named: that can be a product file the"
    echo "  tests import, not only a test file. The baseline admits only the errors already recorded; 'check.cjs <service>"
    echo "  --update' LOWERS it (it refuses to admit anything new), so it cannot be used to silence a new error."
    echo "  (KS-1000: scripts/typecheck-tests/check.cjs)"
    exit 1
fi
echo "OK — $# service(s) type-check against their baseline."
exit 0
