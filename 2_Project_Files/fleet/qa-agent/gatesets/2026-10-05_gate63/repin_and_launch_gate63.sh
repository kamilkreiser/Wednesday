#!/bin/bash
# repin_and_launch_gate63.sh — the LAUNCH ACTION for gate63 (#1388, KS-1404 wiring, T1). Inputs PR + HEAD must equal the kit's. It READS
# everything at launch and never trusts a pin it did not just re-read (Kam 2026-09-18: re-pin and launch are ONE action):
#   (0)  the pane QA/Secuura-ks1404-1388 is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead);
#   (1)  the census + PULLS API (gh_census_gate63.py): rc 3 on an API failure or a BLIND control, rc 15 on an OVERLAP (NEAR is reported);
#   (2)  ONE `git ls-remote` from the Secuura checkout (read verb only) — rc 2;
#   (3)  rc 11 unless input == kit head == API head == pull/head == branch, the PR open, not merged, based on develop;
#   (3b) develop is RECORDED, never refused (it moved twice while this kit was drafted); rc 10 only if it does NOT descend from the base;
#   (3c) the kit's own read-only C1 instrument at the head (c1_pin_gate63.py, P1-P13) — rc 13 on any FAIL;
#   (3d) the Docker daemon state, RECORDED (down = the gate's image proof will be NOT RUN; README section 6, W2) — never refused;
#   (4)  G63_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's own --check — rc 13;
#   (7)  cockpit.sh add <pane> <launcher> — rc 14, then a pane census. Rung 5 is Wednesday's, after this (README section 7).
# --dry-run: steps 0-3d and the launcher's --check, then stops (no usage gate, no cockpit). Every step's output goes to launch_<HHMMSS>.*
# (dry: dry_<HHMMSS>.*) beside this script. Controls-only override: G63_ROUTING (a routing file stand-in).
# Usage: repin_and_launch_gate63.sh <PR> <HEAD 40-hex> [--dry-run]     (Wednesday runs it under `script -q /dev/null` — README section 7)
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$GS/kit.json" "$1"; }
ROUTING="${G63_ROUTING:-$(KJ routing)}"; KHEAD="$(KJ head)"; KBASE="$(KJ base)"; KBR="$(KJ branch)"; KPR="$(KJ pr)"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"
L="$GS/$(KJ launcher)"
PR="${1:-}"; HEAD="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
case "$PR" in ''|*[!0-9]*) echo "usage: repin_and_launch_gate63.sh <PR> <HEAD 40-hex> [--dry-run]"; exit 9;; esac
printf '%s' "$HEAD" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: HEAD must be the FULL 40-hex sha, got '$HEAD'"; exit 9; }
[ "$PR" = "$KPR" ] || { echo "REFUSING: PR #$PR is not this kit's PR (#$KPR)"; exit 9; }
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate63$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | PR #$PR | HEAD $HEAD | pane $PANE"

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; README section 4)"; else echo "REFUSING: add the routing line first (README section 4): $LINE"; exit 1; fi
fi

echo "--- 1. census + PULLS API"
python3 "$GS/gh_census_gate63.py" --json "$OUTP.census.json" > "$OUTP.census.out" 2> "$OUTP.census.err"; rc=$?
sed 's/^/    /' "$OUTP.census.out" | cut -c1-240; [ -s "$OUTP.census.err" ] && sed 's/^/    stderr: /' "$OUTP.census.err"
echo "  census rc=$rc"
[ "$rc" -eq 3 ] && { echo "REFUSING: API failure or a BLIND census control"; exit 3; }
[ "$rc" -eq 15 ] && { echo "REFUSING: an OVERLAP on a non-doc kit path — read it first"; exit 15; }
[ "$rc" -eq 0 ] || { echo "REFUSING: census rc $rc"; exit 3; }
A_LINE="$(grep '^API #' "$OUTP.census.out")"
A_HEAD="$(printf '%s' "$A_LINE" | awk '{print $4}')"; A_BR="$(printf '%s' "$A_LINE" | awk '{print $6}')"; A_BASE="$(printf '%s' "$A_LINE" | awk '{print $8}')"
A_STATE="$(printf '%s' "$A_LINE" | awk '{print $10}')"; A_MERGED="$(printf '%s' "$A_LINE" | awk '{print $12}')"

echo "--- 2. ONE ls-remote (read verb) from the checkout"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/heads/$KBR" "refs/pull/$PR/head" > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"; PH="$(awk -v r="refs/pull/$PR/head" '$2==r{print $1}' "$OUTP.lsremote.out")"; BH="$(awk -v r="refs/heads/$KBR" '$2==r{print $1}' "$OUTP.lsremote.out")"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV | pull/head $PH | branch $BH"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }

echo "--- 3. the head: input == kit == API == pull/head == branch; open, not merged, on develop"
echo "  input $HEAD | kit $KHEAD | API $A_HEAD ($A_STATE, merged $A_MERGED, base $A_BASE, branch $A_BR) | pull/head $PH | branch $BH"
if [ "$HEAD" = "$KHEAD" ] && [ "$A_HEAD" = "$HEAD" ] && [ "$PH" = "$HEAD" ] && [ "$BH" = "$HEAD" ] && [ "$A_STATE" = "open" ] && [ "$A_MERGED" = "False" ] && [ "$A_BASE" = "develop" ] && [ "$A_BR" = "$KBR" ]; then
  echo "  BOTH INSTRUMENTS AGREE with the input head."
else echo "REFUSING TO LAUNCH: the head is not the kit head on both instruments, or the PR is not open / merged / off develop (a new head is a RE-DRAFT)"; exit 11; fi

echo "--- 3b. develop RECORDED: $CUR_DEV (kit base $KBASE; at READY 0f2422925317; at drafting 32e058975d4e)"
if git -C "$CHECKOUT" cat-file -t "$CUR_DEV" > /dev/null 2>&1; then
  git -C "$CHECKOUT" merge-base --is-ancestor "$KBASE" "$CUR_DEV" || { echo "REFUSING TO LAUNCH: develop $CUR_DEV does not descend from the base (history rewritten?)"; exit 10; }
  echo "  descends from the base; first-parent advance since the base: $(git -C "$CHECKOUT" rev-list --first-parent --count "$KBASE..$CUR_DEV") commit(s)"
else echo "  NOT in the local store — the gate fetches it into its OWN clone (X7); recorded, not refused"; fi

echo "--- 3c. the kit's read-only C1 instrument at the head (P1-P13)"
python3 "$GS/c1_pin_gate63.py" --repo "$CHECKOUT" --head "$HEAD" > "$OUTP.c1.out" 2> "$OUTP.c1.err"; rc=$?
echo "  c1 rc=$rc | $(grep '^CHECKED' "$OUTP.c1.out")"; grep '^FAIL' "$OUTP.c1.out" | sed 's/^/    /' | cut -c1-240; [ -s "$OUTP.c1.err" ] && sed 's/^/    stderr: /' "$OUTP.c1.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the C1 instrument FAILED at the head (or could not read it)"; exit 13; }

echo "--- 3d. Docker daemon (RECORDED, never refused: down means C6 IMAGE PROOF = NOT RUN)"
/usr/local/bin/docker info --format '{{.ServerVersion}} {{.Architecture}}' > "$OUTP.docker.out" 2> "$OUTP.docker.err"; rc=$?
if [ "$rc" -eq 0 ]; then echo "  daemon UP: $(cat "$OUTP.docker.out")"; else echo "  daemon DOWN (rc $rc): the gate will record C6 NOT RUN unless the daemon is up when it gets there (README W2)"; fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G63_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G63_* override is set"; exit 16; }
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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') PR #$PR at $HEAD; develop at launch $CUR_DEV — now verify RUNG 5 (README section 7)"
