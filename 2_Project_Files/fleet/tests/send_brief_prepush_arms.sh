#!/bin/bash
# send_brief_prepush_arms.sh — red-proof for the 2026-10-19 pre-push citation advisory.
# Tests the helper fleet/prepush_cite_check.sh directly (send_brief.sh's full dry run needs every
# other gate satisfied), plus a wiring arm proving send_brief.sh actually calls the helper.
# Run: bash send_brief_prepush_arms.sh -> exits non-zero on any FAIL.
set -u
SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
CHK="${PREPUSH_CHECK:-$SELF_DIR/../prepush_cite_check.sh}"
SB="$SELF_DIR/../send_brief.sh"
T=$(mktemp -d "${TMPDIR:-/tmp}/prepush_arms.XXXXXX")
fails=0
arm() { # name want(warn|silent) body
  local name="$1" want="$2" body="$3" got rc
  printf '%s\n' "$body" > "$T/$name.body"
  if [ -f "$CHK" ]; then bash "$CHK" "$T/$name.body" > "$T/$name.out" 2> "$T/$name.err"; rc=$?; else rc=127; : > "$T/$name.err"; fi
  if grep -q '^ADVISORY (2026-10-19 w=3)' "$T/$name.err"; then got=warn; else got=silent; fi
  if [ "$rc" -eq 0 ] && [ "$got" = "$want" ]; then echo "PASS $name ($got)"; else echo "FAIL $name got=$got want=$want rc=$rc"; fails=$((fails+1)); fi
}
arm a-push-nocite      warn   'Run git push origin HEAD from the branch.'
arm b-push-cited       silent 'Run git push origin HEAD. Hook: .githooks/pre-push:352-358 allows it.'
arm c-force-notinhook  silent 'Use the merge API (a PUT), not a push, after a force-push is ruled out.'
arm d-no-push-words    silent 'Please read the ticket and report back.'
arm e-allowforce-nocite warn  'Set ALLOW_FORCE=1 and retry.'
arm f-case-insens      warn   'Then FORCE PUSH the branch.'
# wiring: send_brief.sh must call the helper (red before the change, green after)
if grep -q 'prepush_cite_check.sh' "$SB"; then echo "PASS g-wired-into-send_brief"; else echo "FAIL g-wired-into-send_brief"; fails=$((fails+1)); fi
echo "FAILS=$fails"
[ "$fails" -eq 0 ]
