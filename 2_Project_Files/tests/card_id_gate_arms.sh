#!/bin/bash
# card_id_gate_arms.sh — arms for fleet/card_id_gate.sh (widened 2026-10-18: dated ids for every
# store prefix + quoted card titles). Usage: card_id_gate_arms.sh [gate path]  (default: the live gate)
# Each arm writes a body file into a fresh mktemp dir (left for the OS to reap; never-delete rule),
# runs the gate, and compares the rc with the expected one.
set -uo pipefail
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GATE="${1:-$SELF_DIR/../fleet/card_id_gate.sh}"
TMP="$(mktemp -d)"; PASS=0; FAIL=0
arm() { # name expected_rc text [env]
  local name="$1" want="$2" text="$3"; shift 3
  printf '%s\n' "$text" > "$TMP/body"
  env "$@" bash "$GATE" "$TMP/body" > "$TMP/out" 2>&1; local rc=$?
  if [ "$rc" = "$want" ]; then PASS=$((PASS+1)); echo "PASS  $name (rc $rc)"; else FAIL=$((FAIL+1)); echo "FAIL  $name (rc $rc, wanted $want)"; sed 's/^/      /' "$TMP/out"; fi
}
# RED: the 2026-10-18 19:14 message shape, with a title no card carries (the add was refused)
arm "title absent -> refuse" 1 "Please tap a, b or c on the new card, 'approve three imaginary fixes nobody filed'. My recommendation is a."
# PASS: the real 19:14 and 19:19 messages (their cards exist)
arm "real 19:14 title -> pass" 0 "Please tap a, b or c on the new card, 'approve two one-line fixes the live check found'. My recommendation is a."
arm "real 19:19 title -> pass" 0 "All five are listed on the card 'QuickQuote 2.39: approve five more sentences'. My recommendation is a."
# RED: a Datasec dated id that is not in the store (the prefix the old pattern never knew)
arm "datasec dated id absent -> refuse" 1 "Carded as mpscalc-no-such-card-9999 for Kam."
# PASS: a Datasec dated id that is in the store
arm "datasec dated id present -> pass" 0 "Kam ruled card mpscalc-hosted-deploy-e6f92a5-1017 = a."
# RED: the original pattern still fires
arm "old prefix absent -> refuse" 1 "card nexusai-no-such-card-ever"
# PASS: a dated id on a line with no card word is not a claim
arm "no card word -> pass" 0 "branch b109/mpscalc-157-proposals-x-1013 was rebuilt."
# PASS: a short quote after 'card' (< 8 chars) is not a title
arm "short quote -> pass" 0 "tap 'a' on the card 'a'."
# RED: store unreadable -> fail closed
arm "store unreadable -> refuse" 1 "on the card 'approve two one-line fixes the live check found'" DQ_FILE=/nonexistent/decisions.json
echo "card_id_gate arms: $PASS pass, $FAIL fail"
[ "$FAIL" = 0 ]
