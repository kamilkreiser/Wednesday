#!/usr/bin/env bash
# =============================================================================
# KS-1054 / N-1332-5 — the deploy step reads /health's startupMigrations flag
# =============================================================================
# Kam ruled option (a) on `secuura-ks1054-f9282-migration-failure-visibility`:
#   "Keep serving, flag it on /health — The migration run returns its failed count.
#    /health reports it, so the deploy scripts' existing /health checks see it and the
#    deploy reads as failed. The running service is not stopped."
#
# So /health STAYS 200 and the service keeps serving; it is the DEPLOY STEP that fails.
# This script is the predicate both deploy scripts call, so the rule lives in ONE place
# and each caller can be tested for actually calling it.
#
# KEYED ON `failed`, NEVER ON `error`. gate39's N-G39-2 measured a CORE statement failure
# served as `failed: 3` with NO `error` field at all, so a check keyed on `error` would
# have read that as a clean run. The count is the signal; the message is not.
#
# ABSENT FIELD: an older gateway image serves no `startupMigrations` at all. This still PASSES the
# deploy and WARNS LOUDLY, rather than failing. Two reasons, and the second is the one that decides it:
#   1. absence of the field is not evidence of failure, it is absence of evidence; and
#   2. failing closed here would block a ROLLBACK to an older image — exactly the operation
#      you need when a deploy has gone wrong. A check that cannot be rolled back past is a
#      check that makes an outage longer.
# It is deliberately NOT silent: a check that quietly stops checking is how a gate rots.
#
# === THREE STATES, NOT TWO (KS-1054, gate44 N-1346-2/-3/-4) ===
# This script used to return a BOOLEAN while its own OUTPUT already distinguished three cases: a
# clean tick, a named skip, and a failure. rc 0 covered both "ran clean" and "never ran", so neither
# caller could tell them apart and both printed a passing line for a check that did not run. The
# information existed and was thrown away at the boundary. Hence a third exit code.
#
# Exit 0 = the check RAN and was CLEAN; the deploy step may proceed.
# Exit 1 = the deploy step FAILS (migrations failed, `failed` malformed, or no parser — see below).
# Exit 2 = PASS-WITH-SKIP: the check did NOT run. The deploy step still PASSES — that is the
#          rollback rule above — but the caller must NOT report a clean run. Both callers render
#          this as a named warning and count it separately; neither treats it as a pass or a failure.
# ⚠ rc 2 is NOT backwards-compatible with an `if predicate; then pass; else fail; fi` caller: under
#   `if !`, rc 2 is a truthy failure. The predicate and BOTH callers therefore change together, in
#   one commit. Shipping this alone would flip ABSENT from pass to FAIL and break the rollback rule.
#
# Usage:  check-startup-migrations.sh '<health json>'
#     or: curl -s .../health | check-startup-migrations.sh
# =============================================================================
set -uo pipefail

# ⚠ "no argument" and "an EMPTY argument" are DIFFERENT. `BODY="${1-}"` followed by an
# emptiness test conflated them: `check-startup-migrations.sh ""` fell through to `cat` and
# BLOCKED ON STDIN FOREVER. In a deploy that is a hung deploy, not a failed one — the worse
# outcome, because nothing reports it. Caught by this ticket's own P7 cell.
# Argument count decides; stdin is read only when there is genuinely no argument, and never
# from a terminal, so an interactive run cannot hang either.
if [[ $# -ge 1 ]]; then
  BODY="$1"
elif [[ -t 0 ]]; then
  echo "  ! startupMigrations: no body given and stdin is a terminal — nothing to check" >&2
  exit 2
else
  BODY="$(cat)"
fi

if [[ -z "${BODY//[[:space:]]/}" ]]; then
  echo "  ! startupMigrations: /health returned an EMPTY body — migration check SKIPPED (not a pass)"
  echo "    The migration check did NOT run. Passing the deploy step, but this is not a clean run."
  exit 2
fi

# gate44 N-1346-4 — THE PARSER IS A DEPENDENCY AND ITS ABSENCE IS NOT A SKIP.
# #1346 introduced the only `python3` use in deploy.sh's whole path, through this script. When
# python3 was missing, the `|| echo UNPARSEABLE` below reported a body that said `failed: 2` as
# "not JSON" and exited 0: it failed OPEN, and it misattributed the cause. Wednesday ruled FAIL
# CLOSED (rc 1) rather than pass-with-skip, and the reasoning is that a missing parser is a HOST
# defect, not an image property — so the rollback argument that protects the ABSENT case does not
# reach it, and deploy-all.sh ALREADY fails a deploy without python3 at its login-token parse, so
# this makes the two scripts consistent instead of inventing a new failure mode. Kam's option (a) is
# explicit that the deploy reads as FAILED.
# Checked EXPLICITLY, before the pipeline, so the message can name the real cause.
# N-1350-1 (gate47): a python3 that is PRESENT but BROKEN (on PATH, exits non-zero) is the same host
# defect. It is probed here, or the pipeline's `|| echo UNPARSEABLE` reads it as "not JSON" (rc 2).
if ! command -v python3 > /dev/null 2>&1 || ! python3 -c 'import json' > /dev/null 2>&1 < /dev/null; then
  echo "  ✗ startupMigrations: python3 is NOT on PATH or does not run, so /health's body cannot be parsed."
  echo "    A missing parser is not evidence of a clean run; the DEPLOY fails (Kam's option (a))."
  exit 1
fi

FAILED="$(printf '%s' "$BODY" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    print("UNPARSEABLE"); raise SystemExit(0)
sm = d.get("startupMigrations")
if not isinstance(sm, dict):
    print("ABSENT"); raise SystemExit(0)
# `ran` is read BEFORE `failed`, and that ordering IS the fix for N-1346-2. A {ran:false, failed:0}
# body used to print a clean "0 failed" tick, which is the most misleading of the four skip shapes
# because it names the field and reports a number. The gateway module says ran:false "is NOT the
# same as a clean run"; gate44 measured it reachable at boot three ways. Treated exactly like ABSENT.
if sm.get("ran") is False:
    print("NOTRUN"); raise SystemExit(0)
f = sm.get("failed")
# A present-but-non-numeric `failed` is not a zero. Say so rather than coercing it.
print(f if isinstance(f, int) else ("MALFORMED" if f is not None else "ABSENT"))
' 2>/dev/null || echo "UNPARSEABLE")"

case "$FAILED" in
  UNPARSEABLE)
    echo "  ! startupMigrations: /health body is not JSON — migration check SKIPPED (not a pass)"
    echo "    The migration check did NOT run. Passing the deploy step, but this is not a clean run."
    exit 2 ;;
  NOTRUN)
    echo "  ! startupMigrations: /health reports ran:false — the migration check did NOT run."
    echo "    That is NOT the same as a clean run (the gateway's own module says so). Reachable when"
    echo "    the DB is late at boot, DATABASE_URL is unset, or the run threw. Treated as ABSENT."
    exit 2 ;;
  ABSENT)
    echo "  ! startupMigrations: field ABSENT from /health — this gateway image predates KS-1054."
    echo "    The migration check did NOT run. Passing so a rollback to an older image is not blocked."
    exit 2 ;;
  MALFORMED)
    echo "  ✗ startupMigrations: 'failed' is present but not an integer — refusing to read it as zero"
    exit 1 ;;
  0)
    echo "  ✓ startupMigrations: 0 failed"
    exit 0 ;;
  *)
    echo "  ✗ startupMigrations: $FAILED migration(s) FAILED at gateway startup."
    echo "    /health stays 200 and the service keeps serving (Kam's option (a)); the DEPLOY fails."
    exit 1 ;;
esac
