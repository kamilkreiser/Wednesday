#!/usr/bin/env bash
# Usage: bash leg16.sh <Blockchain/Dev dir>
# Runs leg 16 exactly as preflight.sh does: cwd = Dev, `run_delegated bash scripts/preflight/test-types-ratchet.sh`,
# with run_delegated and _note_skip extracted VERBATIM from that tree's own preflight.sh (asserted present).
set -u
DEV="$1"; PF="$DEV/scripts/preflight/preflight.sh"
fn() { awk -v n="$1" '$0 ~ "^"n"\\(\\) *\\{" {p=1} p {print} p && /^}/ {exit}' "$PF"; }
RD="$(fn run_delegated)"; NS="$(fn _note_skip)"
[ -n "$RD" ] && [ -n "$NS" ] || { echo "HARNESS: could not extract run_delegated/_note_skip"; exit 99; }
grep -q '^if ! run_delegated bash scripts/preflight/test-types-ratchet.sh; then' "$PF" || { echo "HARNESS: leg-16 call line not found verbatim"; exit 98; }
eval "$RD"; eval "$NS"
CURRENT_LEG=16; SKIPPED_ADVISORY=""; fail=0
cd "$DEV" || exit 97
if ! run_delegated bash scripts/preflight/test-types-ratchet.sh; then fail=1; fi
echo "HARNESS: leg16 fail=$fail skipped_advisory='${SKIPPED_ADVISORY}'"
exit $fail
