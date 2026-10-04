#!/bin/bash
# repin_and_launch_gate55.sh — the LAUNCH ACTION for the gate55 kit (the directory this script lives in). ONE PR, whose number and head are
# INPUTS taken from Seat B 58th's READY. Re-pin and launch are ONE action (Kam 2026-09-18): it READS everything AT LAUNCH and never trusts a
# pin it did not just re-read. A NEW COPY of repin_and_launch_gate54a.sh, re-keyed for gate55 (pane QA/Secuura-ks1015-<PR>, 5 paths, the
# KS-1404 co-tenant), plus step (3e) MOVED HEAD:
#   (0)  the pane QA/Secuura-ks1015-<PR> is routed (inbox_routing.conf) — rc 1;
#   (1)  the GitHub PULLS API: head sha, branch, base, state, merged, mergeable — rc 3; the PR body is saved beside this script (C4 / C6 read it);
#   (2)  ONE `git ls-remote` READ from the Secuura checkout: develop + refs/pull/<PR>/head + the branch — rc 2;
#   (2b) the OVERLAP census over every OTHER open PR: rc 15 on an OVERLAP; Seat D 4th's KS-1404 docs PR is REPORTED, never refused;
#   (3)  rc 11 unless HEAD == the API head == pull/head == the branch (WHOLE-FIELD), open, not merged, on develop, not `mergeable: false`,
#        and the branch matches kit branch_rx;
#   (3b) STALE BASE: rc 10 if origin develop != kit base (2d85b84e1012: a move is a RE-DRAFT);
#   (3e) MOVED HEAD: rc 18 if HEAD != kit expected_head (16784d620080: the blobs, numstat and doc-block lines are drafted there; a re-draft);
#   (3c) FILL: fill_gate55.py writes the prompt, the launcher and pins_gate55.json — rc 10 on refusal;
#   (3d) RACE: develop and the head re-read by ls-remote AFTER the fill — rc 10 / 11 if either moved meanwhile;
#   (4)  G55_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the filled launcher's own --check — rc 13 (it also
#        refuses a pin older than 30 min, exit 9);  (7) cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3d with the fill done as a SIMULATION (`dry<HHMMSS>.SIM.*`, never the real pins), then the SIM launcher's --check; the
# routing line's absence is REPORTED, not refused; it stops before (4). READ-ONLY in the Secuura checkout (ls-remote only). Nothing is merged,
# deployed or commented. Every step's output is written beside this script as launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*).
# Controls-only overrides (any one set makes a real launch refuse at step 4): G55_ROUTING (routing file), G55_CENSUS_OFFLINE (a SIM fixture dir
# for the API + census), G55_EXPECTED_HEAD (stands in for kit expected_head), G55_PREV_REPORT / G55_PREV_SHA (the fill's previous-round
# report), G55_COMPARE_FILE (the SIM launcher's compare line).
# Usage: repin_and_launch_gate55.sh <PR number> <HEAD 40-hex> [--dry-run]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))[sys.argv[2]]; print("" if v is None else v)' "$GS/kit.json" "$1"; }
ROUTING="${G55_ROUTING:-$(KJ routing)}"; BASE="$(KJ base)"; RX="$(KJ branch_rx)"; EXPH="${G55_EXPECTED_HEAD:-$(KJ expected_head)}"
PR="${1:-}"; HEAD="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
if [ "$PR" = "--help" ] || [ "$PR" = "-h" ]; then sed -n '2,27p' "$0" | sed 's/^# \{0,1\}//'; exit 0; fi
case "$PR" in ''|*[!0-9]*) echo "usage: repin_and_launch_gate55.sh <PR number> <HEAD 40-hex> [--dry-run]   (PR must be digits)"; exit 9;; esac
printf '%s' "$HEAD" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: HEAD must be the FULL 40-hex sha, got '$HEAD'"; exit 9; }
PANE="QA/Secuura-ks1015-$PR"; T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
OFFARG=""; [ -n "${G55_CENSUS_OFFLINE:-}" ] && OFFARG="--offline-dir $G55_CENSUS_OFFLINE"
echo "LAUNCH ACTION gate55$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | PR #$PR | HEAD $HEAD | kit base $BASE | pane $PANE"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -x -F "$PANE|coagent@agentmail.to|yes" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"
rc=$?
echo "  routing file $ROUTING — line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0)"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here; README section 4)"; else echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README section 4; the drafter did NOT write it)"; exit 1; fi
fi

echo "--- 1. instrument A: the GitHub PULLS API (+ 2b the census, same read)$([ -n "$OFFARG" ] && echo '  [SIM REPLAY: G55_CENSUS_OFFLINE]')"
python3 "$GS/gh_census_gate55.py" --pr "$PR" --body-out "$OUTP.body.md" $OFFARG > "$OUTP.api.out" 2> "$OUTP.api.err"
rc=$?
echo "  gh_census rc=$rc"; sed 's/^/    /' "$OUTP.api.out" | cut -c1-260; [ -s "$OUTP.api.err" ] && sed 's/^/    stderr: /' "$OUTP.api.err"
[ "$rc" -eq 0 ] || { echo "REFUSING: the PULLS API read failed"; exit 3; }
grep -q '^CENSUS ' "$OUTP.api.out" || { echo "REFUSING: the census did not complete"; exit 3; }
AL="$(grep "^API #$PR head " "$OUTP.api.out")"
A_HEAD="$(echo "$AL" | awk '{print $4}')"; A_BASE="$(echo "$AL" | awk '{print $6}')"; A_MERGE="$(echo "$AL" | awk '{print $10}')"
A_STATE="$(echo "$AL" | awk '{print $14}')"; A_MERGED="$(echo "$AL" | awk '{print $16}')"; BR="$(echo "$AL" | awk '{print $18}')"
[ -n "$BR" ] || { echo "REFUSING: could not read the PR's branch from the API line"; exit 3; }

echo "--- 2. instrument B: git ls-remote origin (ONE read from the Secuura checkout, READ-ONLY)"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/pull/$PR/head" "refs/heads/$BR" > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"
rc=$?
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"; [ -s "$OUTP.lsremote.err" ] && sed 's/^/    stderr: /' "$OUTP.lsremote.err"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"; PH="$(awk -v r="refs/pull/$PR/head" '$2==r{print $1}' "$OUTP.lsremote.out")"; BH="$(awk -v r="refs/heads/$BR" '$2==r{print $1}' "$OUTP.lsremote.out")"

echo "--- 2b. the census"
if grep -q '^OVERLAP ' "$OUTP.api.out"; then echo "REFUSING TO LAUNCH: another open PR touches a kit path or carries KS-1015 outside the co-tenant allowance — Wednesday sequences it; a re-draft decides"; exit 15; fi
echo "  OVERLAP census clean ($(grep -c '^EXPECTED CO-TENANT' "$OUTP.api.out") expected co-tenant(s) reported)"

echo "--- 3. the head, judged (input == API == pull/head == branch, open, not merged, on develop, not mergeable:false, branch rule)"
echo "  input $HEAD | API $A_HEAD (state $A_STATE, merged $A_MERGED, base $A_BASE, mergeable $A_MERGE) | pull/head ${PH:-ABSENT} | $BR ${BH:-ABSENT}"
if [ "$A_HEAD" = "$HEAD" ] && [ "$PH" = "$HEAD" ] && [ "$BH" = "$HEAD" ] && [ "$A_STATE" = "open" ] && [ "$A_MERGED" = "False" ] && [ "$A_BASE" = "develop" ] && [ "$A_MERGE" != "False" ] && printf '%s' "$BR" | grep -qE "$RX"; then
  echo "  BOTH INSTRUMENTS AGREE with the input head, 1 of 1."
  [ "$A_MERGE" = "None" ] && echo "  NOTE: GitHub has not computed mergeable after 3 reads — the gate's own C1 (ahead 1 / behind 0) is the clean-merge proof"
else
  echo "REFUSING TO LAUNCH: the input head is not the PR's head on both instruments, or the PR is not open / merged / not on develop / mergeable:false / off the branch rule — a stale pin is never launched"; exit 11
fi

echo "--- 3b. develop, read at launch: $CUR_DEV | kit base $BASE"
[ "$CUR_DEV" = "$BASE" ] || { echo "REFUSING TO LAUNCH: STALE BASE — develop moved since drafting ($BASE -> $CUR_DEV); the C1-C6 expectations are base-specific: RE-DRAFT (README section 7)"; exit 10; }
echo "  UNMOVED since drafting"
echo "--- 3e. the head vs the drafted head: $HEAD | kit expected_head $EXPH$([ -n "${G55_EXPECTED_HEAD:-}" ] && echo '  [CONTROL OVERRIDE G55_EXPECTED_HEAD]')"
[ "$HEAD" = "$EXPH" ] || { echo "REFUSING TO LAUNCH: MOVED HEAD — the PR's head is not the head the kit was drafted at (blobs, numstat, doc-block lines): RE-DRAFT (README section 7)"; exit 18; }
echo "  == the drafted head"

echo "--- 3c. FILL from the values just read"
if [ "$DRY" = 1 ]; then SIMARG="--simulate dry$T"; else SIMARG=""; fi
python3 "$GS/fill_gate55.py" --pr "$PR" --head "$HEAD" --develop "$CUR_DEV" --branch "$BR" $SIMARG > "$OUTP.fill.out" 2> "$OUTP.fill.err"
rc=$?
echo "  fill rc=$rc"; sed 's/^/    /' "$OUTP.fill.out" "$OUTP.fill.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the fill refused"; exit 10; }
if [ "$DRY" = 1 ]; then L="$GS/dry$T.SIM.launcher.sh"; else L="$GS/$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["launcher"])' "$GS/pins_gate55.json")"; fi

echo "--- 3d. RACE: re-read develop and the head AFTER the fill"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/pull/$PR/head" > "$OUTP.lsremote2.out" 2> "$OUTP.lsremote2.err"
rc=$?
D2="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote2.out")"; P2="$(awk -v r="refs/pull/$PR/head" '$2==r{print $1}' "$OUTP.lsremote2.out")"
echo "  ls-remote rc=$rc | develop $D2 | pull/head $P2"
[ "$rc" -eq 0 ] && [ "$D2" = "$BASE" ] || { echo "REFUSING TO LAUNCH: develop moved DURING the fill — run this script again"; exit 10; }
[ "$P2" = "$HEAD" ] || { echo "REFUSING TO LAUNCH: the head moved DURING the fill — run this script again with the new head"; exit 11; }

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the SIM launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"
  rc=$?
  echo "  SIM launcher --check rc=$rc"; sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the SIM launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — every read agrees with the input; the real run fills the REAL pins and continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi

echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G55_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G55_* test override is set"; exit 16; }

echo "--- 5. usage gate"
"$(KJ usage_gate)" --check > "$OUTP.usage_gate.out" 2> "$OUTP.usage_gate.err"
rc=$?
echo "  usage_gate rc=$rc (WED_USAGE_STOP=${WED_USAGE_STOP:-unset})"; sed 's/^/    /' "$OUTP.usage_gate.out" "$OUTP.usage_gate.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused (pass WED_USAGE_STOP only with Kam's recorded authority for this lane)"; exit 12; }

echo "--- 6. the launcher's own --check"
"$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"
rc=$?
echo "  launcher --check rc=$rc"; sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the launcher refused under --check"; exit 13; }

echo "--- 7. launch through the fleet's own tooling (cockpit.sh add), never raw tmux send-keys"
"$(KJ cockpit)" add "$PANE" "$L" > "$OUTP.cockpit_add.out" 2> "$OUTP.cockpit_add.err"
rc=$?
echo "  cockpit.sh add rc=$rc"; sed 's/^/    /' "$OUTP.cockpit_add.out" "$OUTP.cockpit_add.err"
[ "$rc" -eq 0 ] || { echo "LAUNCH FAILED at cockpit.sh add"; exit 14; }
echo "--- pane census"
/opt/homebrew/bin/tmux list-panes -a -F '#{pane_id} | #{@cockpit_name} | #{pane_current_command} | #{session_name}:#{window_index}.#{pane_index}'
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') PR #$PR at $HEAD over develop $CUR_DEV"
