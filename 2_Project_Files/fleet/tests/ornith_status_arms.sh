#!/bin/bash
# ornith_status_arms.sh — red-proof for fleet/ornith_status.py and its send_brief.sh wiring.
# Built 2026-09-17 (ledger w=5, the idle-on-a-verdict-turn costume) BEFORE any reliance.
# Every arm runs against a scratch night/ dir via ORNITH_NIGHT_DIR; nothing touches the real queue.
# The wiring arm calls send_brief.sh with NO arguments, so it exits at the usage check and sends nothing.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ST="$HERE/../ornith_status.py"
SB="$HERE/../send_brief.sh"
BASE="$(mktemp -d "${TMPDIR:-/tmp}/ornith_arms.XXXXXX")"
PASS=0; FAIL=0
ok()  { echo "PASS $1"; PASS=$((PASS+1)); }
bad() { echo "FAIL $1"; FAIL=$((FAIL+1)); }

mk() { # $1 = name, $2 = queue body, $3 = done verdict line id, $4 = verdict text
  local d="$BASE/$1"; mkdir -p "$d/log"
  printf '%s\n' "# header input= in a comment must not count" "$2" > "$d/queue.md"
  printf '%s\n' "KS-1 input=/x task=/y ctx=1 | done 2026-09-17 07:00 | verdict RESULT: PASS (7/7) | run /r0" \
                "$3 input=/x task=/y ctx=1 | done 2026-09-17 08:42 | verdict $4 | run /r1" > "$d/done.md"
  echo "$d"
}
run() { ORNITH_NIGHT_DIR="$1" ORNITH_NOW="2026-09-17 09:12" python3 "$ST" > "$BASE/out.txt" 2>&1; echo $? > "$BASE/rc.txt"; }
has() { /usr/bin/grep -c -- "$1" "$BASE/out.txt"; }

# ARM1 unheld PASS + idle: no READY, empty queue, no lock
D=$(mk a1 "" KS-1201 "RESULT: PASS (7/7)"); run "$D"
[ "$(cat $BASE/rc.txt)" = 0 ] && [ "$(has 'UNHELD PASS KS-1201')" = 1 ] && [ "$(has 'IDLE 30 min')" = 1 ] && [ "$(has 'queue 0')" = 1 ] \
  && ok "ARM1 unheld PASS and IDLE 30 min both printed" || { bad "ARM1"; cat "$BASE/out.txt"; }

# ARM2 held: a READY written AFTER the done time silences UNHELD
D=$(mk a2 "" KS-1201 "RESULT: PASS (7/7)"); touch "$D/READY_KS-1201_x.diff.md"; touch -t 202609170850 "$D/READY_KS-1201_x.diff.md"; run "$D"
[ "$(has 'UNHELD')" = 0 ] && [ "$(has 'ORNITH: queue')" = 1 ] && ok "ARM2 READY after done → no UNHELD (status line present)" || { bad "ARM2"; cat "$BASE/out.txt"; }

# ARM3 discriminating: a READY for the same id written BEFORE the done time does NOT count as held
D=$(mk a3 "" KS-1201 "RESULT: PASS (7/7)"); touch "$D/READY_KS-1201-F1_old.diff.md"; touch -t 202609170800 "$D/READY_KS-1201-F1_old.diff.md"; run "$D"
[ "$(has 'UNHELD PASS KS-1201')" = 1 ] && ok "ARM3 stale READY (before done) → still UNHELD" || { bad "ARM3"; cat "$BASE/out.txt"; }

# ARM4 prefix discipline: READY_KS-12010 must not satisfy KS-1201
D=$(mk a4 "" KS-1201 "RESULT: PASS (7/7)"); touch "$D/READY_KS-12010_x.diff.md"; touch -t 202609170850 "$D/READY_KS-12010_x.diff.md"; run "$D"
[ "$(has 'UNHELD PASS KS-1201')" = 1 ] && ok "ARM4 READY_KS-12010 does not hold KS-1201" || { bad "ARM4"; cat "$BASE/out.txt"; }

# ARM5 queued work: depth 1 → no IDLE; the comment line is not counted
D=$(mk a5 "KS-2 input=/a task=/b ctx=1" KS-1201 "RESULT: FAIL at A4"); run "$D"
[ "$(has 'queue 1 ')" = 1 ] && [ "$(has 'IDLE')" = 0 ] && [ "$(has 'UNHELD')" = 0 ] && ok "ARM5 queue 1 (comment not counted) → no IDLE; FAIL → no UNHELD" || { bad "ARM5"; cat "$BASE/out.txt"; }

# ARM6 runner live: a live pid in the lock → no IDLE, 'runner LIVE'
D=$(mk a6 "" KS-1201 "RESULT: FAIL at A4"); mkdir -p "$D/log/.night_run.lock"; echo $$ > "$D/log/.night_run.lock/pid"; run "$D"
[ "$(has 'runner LIVE pid')" = 1 ] && [ "$(has 'IDLE')" = 0 ] && ok "ARM6 live runner pid → no IDLE" || { bad "ARM6"; cat "$BASE/out.txt"; }

# ARM7 dead lock pid (and pid 1 is never treated as the runner) → not running → IDLE
D=$(mk a7 "" KS-1201 "RESULT: FAIL at A4"); mkdir -p "$D/log/.night_run.lock"; echo 1 > "$D/log/.night_run.lock/pid"; run "$D"
[ "$(has 'runner not running ·')" = 1 ] && [ "$(has 'IDLE 30 min')" = 1 ] && ok "ARM7 lock pid 1 → not running → IDLE" || { bad "ARM7"; cat "$BASE/out.txt"; }

# ARM8 under the idle threshold: done 5 min ago → no IDLE
D=$(mk a8 "" KS-1201 "RESULT: FAIL at A4"); ORNITH_NIGHT_DIR="$D" ORNITH_NOW="2026-09-17 08:47" python3 "$ST" > "$BASE/out.txt" 2>&1
[ "$(has 'IDLE')" = 0 ] && ok "ARM8 5 min after done → no IDLE" || { bad "ARM8"; cat "$BASE/out.txt"; }

# ARM9 broken input: no done.md → 'status unreadable', rc 0 (never blocks a send, never silent)
mkdir -p "$BASE/a9"; echo "" > "$BASE/a9/queue.md"; run "$BASE/a9"
[ "$(cat $BASE/rc.txt)" = 0 ] && [ "$(has 'status unreadable')" = 1 ] && ok "ARM9 missing done.md → unreadable line, rc 0" || { bad "ARM9"; cat "$BASE/out.txt"; }

# ARM10 wiring: send_brief.sh with no args prints the ORNITH line on stderr, then refuses usage (rc 2), sends nothing
WED_AGENT=wednesday ORNITH_NIGHT_DIR="$BASE/a1" ORNITH_NOW="2026-09-17 09:12" bash "$SB" > "$BASE/sb_out.txt" 2> "$BASE/sb_err.txt"; SBRC=$?
if [ "$SBRC" = 2 ] && [ "$(/usr/bin/grep -c 'UNHELD PASS KS-1201' "$BASE/sb_err.txt")" = 1 ] && [ "$(/usr/bin/grep -c 'ORNITH' "$BASE/sb_out.txt")" = 0 ] && [ "$(/usr/bin/grep -c 'usage' "$BASE/sb_err.txt")" = 1 ]; then
  ok "ARM10 send_brief prints ORNITH on stderr before the usage refusal (rc 2, stdout clean)"
else bad "ARM10 rc=$SBRC"; cat "$BASE/sb_err.txt"; fi

# ARM11 wiring is Wednesday-only: a tuesday seat prints no ORNITH line
WED_AGENT=tuesday ORNITH_NIGHT_DIR="$BASE/a1" bash "$SB" > "$BASE/sb_out2.txt" 2> "$BASE/sb_err2.txt"
[ "$(/usr/bin/grep -c 'ORNITH' "$BASE/sb_err2.txt")" = 0 ] && ok "ARM11 tuesday seat → no ORNITH line" || { bad "ARM11"; cat "$BASE/sb_err2.txt"; }

echo ""
echo "ornith_status_arms: $PASS passed, $FAIL failed (scratch $BASE)"
[ "$FAIL" -eq 0 ] && [ "$PASS" -eq 11 ]
