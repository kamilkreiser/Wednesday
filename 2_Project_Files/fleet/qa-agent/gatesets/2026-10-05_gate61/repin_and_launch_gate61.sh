#!/bin/bash
# repin_and_launch_gate61.sh — the LAUNCH ACTION for the gate61 kit (the directory this script lives in): ONE PR, #1383 (KS-1401), whose
# number and head are INPUTS that must equal the kit's (the kit is drafted for head 7eccb131f2d6 over develop 46c3e20cfbd2: any other head
# or develop is a RE-DRAFT, or — for a docs-only merge-in after #1381 lands — a Q-M judgement by c4_docs_gate61.py qm, README section 6). Re-pin and launch are ONE action (Kam 2026-09-18): it READS everything AT LAUNCH and never trusts a pin it did
# not just re-read. A NEW COPY of gate59's repin, re-keyed:
#   (0)  the pane QA/Secuura-ks1401-<PR> is routed (inbox_routing.conf) — rc 1;
#   (1)  the GitHub PULLS API: head sha, branch, base, state, merged, mergeable, changed_files (re-read up to 3x while null) — rc 3;
#   (2)  ONE `git ls-remote` READ from the Secuura checkout: develop + refs/pull/<PR>/head + the branch — rc 2;
#   (2b) the OVERLAP census over every OTHER open PR (gh_census_gate61.py): rc 15 on an overlap outside kit.json reported_overlaps, or on
#        a reported overlap whose head MOVED (#1381: Wednesday reads what moved first);
#   (3)  rc 11 unless HEAD == the API head == pull/head == the branch (WHOLE-FIELD), the PR is open, not merged, based on develop, not
#        `mergeable: false`, the branch == kit branch, and HEAD == kit head;
#   (3b) STALE BASE: rc 10 if origin develop != kit develop (a moved develop — e.g. #1381 landed — needs a docs-only merge-in of #1383 first:
#        a new head; README section 6);
#   (3c) FILL: fill_gate61.py writes the prompt, the launcher and pins_gate61.json from the values read in (1)-(3) — rc 10 on refusal;
#   (3d) RACE: develop and the head re-read by ls-remote AFTER the fill — rc 10 / 11 if either moved meanwhile;
#   (4)  G61_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the filled launcher's own --check — rc 13
#        (it also refuses a pin older than 30 min, exit 9: STALE PIN);  (7) cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3d with the fill done as a SIMULATION (`dry<HHMMSS>.SIM.*`, never the real pins), then the SIM launcher's --check; the
# routing line's absence is REPORTED, not refused; it stops before (4). READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged,
# deployed or commented. Every step's output is written beside this script as launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*).
# Controls-only overrides: G61_ROUTING (routing file), G61_REPORTED (a JSON file standing in for reported_overlaps), G61_OVERLAP_EXTRA (an
# extra kit path for the census).
# Usage: repin_and_launch_gate61.sh <PR number> <HEAD 40-hex> [--dry-run]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$GS/kit.json" "$1"; }
ROUTING="${G61_ROUTING:-$(KJ routing)}"; KDEV="$(KJ develop)"; KHEAD="$(KJ head)"; KBR="$(KJ branch)"; KPR="$(KJ pr)"
PR="${1:-}"; HEAD="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
if [ "$PR" = "--help" ] || [ "$PR" = "-h" ]; then sed -n '2,26p' "$0" | sed 's/^# \{0,1\}//'; exit 0; fi
case "$PR" in ''|*[!0-9]*) echo "usage: repin_and_launch_gate61.sh <PR number> <HEAD 40-hex> [--dry-run]   (PR must be digits)"; exit 9;; esac
printf '%s' "$HEAD" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: HEAD must be the FULL 40-hex sha, got '$HEAD'"; exit 9; }
[ "$PR" = "$KPR" ] || { echo "REFUSING: PR #$PR is not this kit's PR (#$KPR)"; exit 9; }
PANE="QA/Secuura-ks1401-$PR"; T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate61$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | PR #$PR | HEAD $HEAD | kit develop $KDEV | pane $PANE"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -x -F "$PANE|coagent@agentmail.to|yes" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"
rc=$?
echo "  routing file $ROUTING — line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0)"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here; README section 4)"; else echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README section 4; the drafter did NOT write it)"; exit 1; fi
fi

echo "--- 1. instrument A: the GitHub PULLS API (+ 2b the census, same read)"
G61_REPORTED="${G61_REPORTED:-}" python3 "$GS/gh_census_gate61.py" --pr "$PR" > "$OUTP.api.out" 2> "$OUTP.api.err"
rc=$?
echo "  gh_census rc=$rc"; sed 's/^/    /' "$OUTP.api.out" | cut -c1-260; [ -s "$OUTP.api.err" ] && sed 's/^/    stderr: /' "$OUTP.api.err"
[ "$rc" -eq 0 ] || { echo "REFUSING: the PULLS API read failed"; exit 3; }
grep -q '^CENSUS ' "$OUTP.api.out" || { echo "REFUSING: the census did not complete"; exit 3; }
AL="$(grep "^API #$PR " "$OUTP.api.out")"
A_HEAD="$(echo "$AL" | awk '{print $4}')"; A_BASE="$(echo "$AL" | awk '{print $6}')"; A_MERGE="$(echo "$AL" | awk '{print $10}')"
A_STATE="$(echo "$AL" | awk '{print $14}')"; A_MERGED="$(echo "$AL" | awk '{print $16}')"; BR="$(echo "$AL" | awk '{print $18}')"; A_NF="$(echo "$AL" | awk '{print $20}')"
[ -n "$BR" ] || { echo "REFUSING: could not read the PR's branch from the API line"; exit 3; }

echo "--- 2. instrument B: git ls-remote origin (ONE read from the Secuura checkout, READ-ONLY)"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/pull/$PR/head" "refs/heads/$BR" > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"
rc=$?
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"; [ -s "$OUTP.lsremote.err" ] && sed 's/^/    stderr: /' "$OUTP.lsremote.err"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"; PH="$(awk -v r="refs/pull/$PR/head" '$2==r{print $1}' "$OUTP.lsremote.out")"; BH="$(awk -v r="refs/heads/$BR" '$2==r{print $1}' "$OUTP.lsremote.out")"

echo "--- 2b. the census"
if grep -q '^OVERLAP ' "$OUTP.api.out"; then echo "REFUSING TO LAUNCH: another open PR touches a kit path or carries a kit key outside reported_overlaps — Wednesday sequences it; a re-draft decides"; exit 15; fi
if grep -q 'HEAD MOVED since drafting' "$OUTP.api.out"; then echo "REFUSING TO LAUNCH: a reported overlap's head MOVED since drafting (#1381 / #1382 / #1384 / #995?) — read what moved; re-draft or update reported_overlaps with Wednesday's ruling"; exit 15; fi
echo "  OVERLAP census clean ($(grep -c '^EXPECTED OVERLAP' "$OUTP.api.out") expected overlap(s) reported, $(grep -c '^MIGRATION' "$OUTP.api.out") other PR(s) adding a migration, $(grep -c '^WRITER' "$OUTP.api.out") touching a charge_events writer; control: $(grep -o 'FIRES\|BLIND' "$OUTP.api.out" | head -1))"
grep -q 'FIRES' "$OUTP.api.out" || { echo "REFUSING: the census classifier control did not fire on #$PR itself — its zero proves nothing"; exit 15; }

echo "--- 3. the head, judged (input == kit head == API == pull/head == branch, open, not merged, on develop, not mergeable:false, kit branch)"
echo "  input $HEAD | kit $KHEAD | API $A_HEAD (state $A_STATE, merged $A_MERGED, base $A_BASE, mergeable $A_MERGE, files $A_NF) | pull/head ${PH:-ABSENT} | $BR ${BH:-ABSENT}"
if [ "$HEAD" = "$KHEAD" ] && [ "$A_HEAD" = "$HEAD" ] && [ "$PH" = "$HEAD" ] && [ "$BH" = "$HEAD" ] && [ "$A_STATE" = "open" ] && [ "$A_MERGED" = "False" ] && [ "$A_BASE" = "develop" ] && [ "$A_MERGE" != "False" ] && [ "$BR" = "$KBR" ]; then
  echo "  BOTH INSTRUMENTS AGREE with the input head, 1 of 1."
  [ "$A_MERGE" = "None" ] && echo "  NOTE: GitHub has not computed mergeable after 3 reads — the gate's own C1 + C4 predict are the clean-merge proof"
else
  echo "REFUSING TO LAUNCH: the input head is not the kit head / the PR's head on both instruments, or the PR is not open / merged / not on develop / mergeable:false / off the kit branch — a stale pin is never launched (a NEW head is a RE-DRAFT: README section 6)"; exit 11
fi

echo "--- 3b. develop, read at launch: $CUR_DEV | kit develop $KDEV"
[ "$CUR_DEV" = "$KDEV" ] || { echo "REFUSING TO LAUNCH: STALE BASE — develop moved since drafting ($KDEV -> $CUR_DEV): #1383 no longer squashes to END_TREE; read WHAT moved; a merge-in (Q-M) is a NEW head judged by c4 qm (README section 6)"; exit 10; }
echo "  UNMOVED since drafting"

echo "--- 3c. FILL from the values just read"
if [ "$DRY" = 1 ]; then SIMARG="--simulate dry$T"; else SIMARG=""; fi
python3 "$GS/fill_gate61.py" --pr "$PR" --head "$HEAD" --develop "$CUR_DEV" --branch "$BR" $SIMARG > "$OUTP.fill.out" 2> "$OUTP.fill.err"
rc=$?
echo "  fill rc=$rc"; sed 's/^/    /' "$OUTP.fill.out" "$OUTP.fill.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the fill refused"; exit 10; }
if [ "$DRY" = 1 ]; then L="$GS/dry$T.SIM.launcher.sh"; else L="$GS/$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["launcher"])' "$GS/pins_gate61.json")"; fi

echo "--- 3d. RACE: re-read develop and the head AFTER the fill"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/pull/$PR/head" > "$OUTP.lsremote2.out" 2> "$OUTP.lsremote2.err"
rc=$?
D2="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote2.out")"; P2="$(awk -v r="refs/pull/$PR/head" '$2==r{print $1}' "$OUTP.lsremote2.out")"
echo "  ls-remote rc=$rc | develop $D2 | pull/head $P2"
[ "$rc" -eq 0 ] && [ "$D2" = "$KDEV" ] || { echo "REFUSING TO LAUNCH: develop moved DURING the fill — run this script again"; exit 10; }
[ "$P2" = "$HEAD" ] || { echo "REFUSING TO LAUNCH: the head moved DURING the fill — a new head is a RE-DRAFT"; exit 11; }

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the SIM launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"
  rc=$?
  echo "  SIM launcher --check rc=$rc"; sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the SIM launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — every read agrees with the input; the real run fills the REAL pins and continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi

echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G61_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G61_* test override is set"; exit 16; }

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
