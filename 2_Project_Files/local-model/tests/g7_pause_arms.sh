#!/bin/bash
# g7_pause_arms.sh — arms for the G7 BUSY-leg deliberate-pause predicate (2026-09-20, Wednesday).
# Exercises BOTH directions plus the malformed shape that broke ALLOW_SEATS on 2026-09-17.
# Never touches the real fleet: it sources ONLY the predicate, with SELF_DIR pointed at a scratch dir.
set -u
PASS=0; FAIL=0
ok(){ echo "ARM PASS  $1"; PASS=$((PASS+1)); }
no(){ echo "ARM FAIL  $1"; FAIL=$((FAIL+1)); }
RUN="$(mktemp -d)"; trap 'rm -rf "$RUN"' EXIT
SRC="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/night_run.sh"
OLD="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/night_run.sh.pre-0920-pausequeue"

# extract the predicate alone (no side effects) and run it against a scratch PAUSE_QUEUE
probe(){ # $1 = script, $2 = file contents or empty for none
  local sc="$1" body="$2" d="$RUN/d$$RANDOM"; mkdir -p "$d"
  [ -n "$body" ] && printf '%s\n' "$body" > "$d/PAUSE_QUEUE"
  SELF_DIR="$d" bash -c '
    SELF_DIR="'"$d"'"
    '"$(awk "/^_g7_pause_live\(\) \{/,/^\}/" "$sc")"'
    if _g7_pause_live; then echo LIVE; else echo NOTLIVE; fi
  ' 2>/dev/null
}
FUT=$(( $(date +%s) + 3600 ))
PAST=$(( $(date +%s) - 3600 ))

# 1 no file -> the leg must tap (unchanged behaviour). NEGATIVE CONTROL for the whole feature.
[ "$(probe "$SRC" "")" = "NOTLIVE" ] && ok "1 no PAUSE_QUEUE -> NOT live (leg taps, behaviour unchanged)" || no "1 no PAUSE_QUEUE"
# 2 future epoch -> pause live, tap suppressed
[ "$(probe "$SRC" "$FUT
reserving the allowance for the running QA gate")" = "LIVE" ] && ok "2 future epoch -> LIVE (tap suppressed)" || no "2 future epoch"
# 3 past epoch -> expired, leg taps again. THE EXPIRY ACTUALLY FIRES.
[ "$(probe "$SRC" "$PAST
stale reason")" = "NOTLIVE" ] && ok "3 expired epoch -> NOT live (the pause ENDS on its own)" || no "3 expired epoch"
# 4 the 2026-09-17 defect: a human date must NOT become a permanent pause
[ "$(probe "$SRC" "2026-09-20 23:00
a human date, not an epoch")" = "NOTLIVE" ] && ok "4 human date on line 1 -> REFUSED as malformed (not a permanent pause)" || no "4 human date -> permanent pause (the ALLOW_SEATS defect)"
# 5 garbage line 1 -> not live
[ "$(probe "$SRC" "not-a-number
x")" = "NOTLIVE" ] && ok "5 non-numeric line 1 -> NOT live" || no "5 non-numeric line 1"
# 6 NEGATIVE CONTROL on the ARM ITSELF: the pre-fix script has no predicate at all, so the
#   extraction is empty and the probe cannot return LIVE. Proves arm 2 discriminates the FIX.
[ "$(probe "$OLD" "$FUT
x")" != "LIVE" ] && ok "6 NEGATIVE CONTROL: pre-fix script never reports LIVE (arm 2 tests the fix, not the harness)" || no "6 negative control"

echo "================  $PASS passed, $FAIL failed  ================"
[ "$FAIL" -eq 0 ]
