#!/bin/bash
# repin_and_launch_gate62.sh — the LAUNCH ACTION for gate62 (#1387, KS-1388 s1, T2). Inputs PR + HEAD must equal the kit's. It READS
# everything at launch and never trusts a pin it did not just re-read (Kam 2026-09-18: re-pin and launch are ONE action):
#   (0)  the pane QA/Secuura-ks1388-1387 is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead);
#   (1)  the census + PULLS API (gh_census_gate62.py): rc 3 on an API failure or a BLIND control, rc 15 on an OVERLAP;
#   (2)  ONE `git ls-remote` from the Secuura checkout (read verb only);
#   (3)  rc 11 unless input == kit head == API head == pull/head == branch, the PR open, not merged, based on develop;
#   (3b) rc 10 if origin develop != kit develop (a docs PR landed: #1387 needs a docs-only merge-in = a new head = a RE-DRAFT, README §6);
#   (4)  G62_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's own --check — rc 13;
#   (7)  cockpit.sh add <pane> <launcher> — rc 14, then a pane census. Rung 5 is Wednesday's, after this (README §7).
# --dry-run: steps 0-3b and the launcher's --check, then stops (no usage gate, no cockpit). Every step's output goes to launch_<HHMMSS>.*
# (dry: dry_<HHMMSS>.*) beside this script. Controls-only override: G62_ROUTING (a routing file stand-in).
# Usage: repin_and_launch_gate62.sh <PR> <HEAD 40-hex> [--dry-run]     (Wednesday runs it under `script -q /dev/null` — README §7)
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$GS/kit.json" "$1"; }
ROUTING="${G62_ROUTING:-$(KJ routing)}"; KDEV="$(KJ develop)"; KHEAD="$(KJ head)"; KBR="$(KJ branch)"; KPR="$(KJ pr)"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"
L="$GS/$(KJ launcher)"
PR="${1:-}"; HEAD="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
case "$PR" in ''|*[!0-9]*) echo "usage: repin_and_launch_gate62.sh <PR> <HEAD 40-hex> [--dry-run]"; exit 9;; esac
printf '%s' "$HEAD" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: HEAD must be the FULL 40-hex sha, got '$HEAD'"; exit 9; }
[ "$PR" = "$KPR" ] || { echo "REFUSING: PR #$PR is not this kit's PR (#$KPR)"; exit 9; }
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate62$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | PR #$PR | HEAD $HEAD | kit develop $KDEV | pane $PANE"

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; README §4)"; else echo "REFUSING: add the routing line first (README §4): $LINE"; exit 1; fi
fi

echo "--- 1. census + PULLS API"
python3 "$GS/gh_census_gate62.py" --json "$OUTP.census.json" > "$OUTP.census.out" 2> "$OUTP.census.err"; rc=$?
sed 's/^/    /' "$OUTP.census.out" | cut -c1-240; [ -s "$OUTP.census.err" ] && sed 's/^/    stderr: /' "$OUTP.census.err"
echo "  census rc=$rc"
[ "$rc" -eq 3 ] && { echo "REFUSING: API failure or a BLIND census control"; exit 3; }
[ "$rc" -eq 15 ] && { echo "REFUSING: an OVERLAP outside the expected doc-only set — read it first"; exit 15; }
[ "$rc" -eq 0 ] || { echo "REFUSING: census rc $rc"; exit 3; }
A_LINE="$(grep '^API #' "$OUTP.census.out")"
A_HEAD="$(printf '%s' "$A_LINE" | awk '{print $4}')"; A_BR="$(printf '%s' "$A_LINE" | awk '{print $6}')"; A_BASE="$(printf '%s' "$A_LINE" | awk '{print $8}')"
A_STATE="$(printf '%s' "$A_LINE" | awk '{print $10}')"; A_MERGED="$(printf '%s' "$A_LINE" | awk '{print $12}')"

echo "--- 2. ONE ls-remote (read verb) from the checkout"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/heads/$KBR" "refs/pull/$PR/head" > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"; PH="$(awk -v r="refs/pull/$PR/head" '$2==r{print $1}' "$OUTP.lsremote.out")"; BH="$(awk -v r="refs/heads/$KBR" '$2==r{print $1}' "$OUTP.lsremote.out")"
echo "  ls-remote rc=$rc | develop $CUR_DEV | pull/head $PH | branch $BH"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }

echo "--- 3. the head: input == kit == API == pull/head == branch; open, not merged, on develop"
echo "  input $HEAD | kit $KHEAD | API $A_HEAD ($A_STATE, merged $A_MERGED, base $A_BASE, branch $A_BR) | pull/head $PH | branch $BH"
if [ "$HEAD" = "$KHEAD" ] && [ "$A_HEAD" = "$HEAD" ] && [ "$PH" = "$HEAD" ] && [ "$BH" = "$HEAD" ] && [ "$A_STATE" = "open" ] && [ "$A_MERGED" = "False" ] && [ "$A_BASE" = "develop" ] && [ "$A_BR" = "$KBR" ]; then
  echo "  BOTH INSTRUMENTS AGREE with the input head."
else echo "REFUSING TO LAUNCH: the head is not the kit head on both instruments, or the PR is not open / merged / off develop (a new head is a RE-DRAFT)"; exit 11; fi
echo "--- 3b. develop: $CUR_DEV | kit $KDEV"
[ "$CUR_DEV" = "$KDEV" ] || { echo "REFUSING TO LAUNCH: develop moved ($KDEV -> $CUR_DEV): #1387 needs a docs-only merge-in (a new head) before a gate; README §6"; exit 10; }
echo "  UNMOVED since drafting"

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G62_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G62_* override is set"; exit 16; }
echo "--- 5. usage gate"
"$(KJ usage_gate)" --check > "$OUTP.usage_gate.out" 2> "$OUTP.usage_gate.err"; rc=$?
sed 's/^/    /' "$OUTP.usage_gate.out" "$OUTP.usage_gate.err"; echo "  usage_gate rc=$rc (WED_USAGE_STOP=${WED_USAGE_STOP:-unset})"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused (WED_USAGE_STOP only with Kam's recorded authority)"; exit 12; }
echo "--- 6. the launcher's own --check"
"$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the launcher refused under --check"; exit 13; }
echo "--- 7. cockpit.sh add (the fleet's own tooling, never raw send-keys)"
"$(KJ cockpit)" add "$PANE" "$L" > "$OUTP.cockpit_add.out" 2> "$OUTP.cockpit_add.err"; rc=$?
sed 's/^/    /' "$OUTP.cockpit_add.out" "$OUTP.cockpit_add.err"; echo "  cockpit.sh add rc=$rc"
[ "$rc" -eq 0 ] || { echo "LAUNCH FAILED at cockpit.sh add"; exit 14; }
echo "--- pane census"
/opt/homebrew/bin/tmux list-panes -a -F '#{pane_id} | #{@cockpit_name} | #{pane_current_command} | #{session_name}:#{window_index}.#{pane_index}'
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') PR #$PR at $HEAD over develop $CUR_DEV — now verify RUNG 5 (README §7)"
