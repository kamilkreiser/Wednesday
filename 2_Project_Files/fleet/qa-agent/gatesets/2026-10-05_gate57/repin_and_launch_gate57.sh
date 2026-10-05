#!/bin/bash
# repin_and_launch_gate57.sh — the LAUNCH ACTION for the gate57 kit (the directory this script lives in). TWO PRs (Seat B 60th's #1380
# KS-1333 and #1381 KS-1345, ONE READY), whose numbers and heads are INPUTS from that READY. Re-pin and launch are ONE action (Kam
# 2026-09-18): it READS everything AT LAUNCH and never trusts a pin it did not just re-read. A NEW COPY of repin_and_launch_gate56a.sh
# (two PRs) with gate58's guards, re-keyed for #1380 + #1381, plus a DEVELOP-ADVANCE rule:
#   (0)  the pane QA/Secuura-ks1333-1345-<PR1> is routed (inbox_routing.conf) — rc 1;
#   (1)  the GitHub PULLS API for EACH PR: head sha, branch, base, state, merged, mergeable — rc 3; each body saved beside this script as
#        <log>.body_pr<n>.md (C6 reads it with --body-file);
#   (2)  ONE `git ls-remote` READ from the Secuura checkout: develop + both refs/pull/<n>/head + both branches — rc 2;
#   (2b) the OVERLAP census over every OTHER open PR (a kit path or ANY Projects Documents file, outside kit reported_overlaps) — rc 15;
#   (3)  rc 11 unless, for EACH PR, input head == API head == pull/head == branch (WHOLE-FIELD), open, not merged, base develop, not
#        `mergeable: false`, the branch matches its own branch_rx and not the sibling's; and the two PRs / heads differ;
#   (3b) DEVELOP: == kit cut_base, or an ADVANCE read by the compare API (cut_base...develop) whose moved paths touch NO kit path and NOTHING
#        under Projects Documents/ (e.g. gate58's #1379: lockfiles + audit-baseline.json) — else rc 10 (a re-draft: README section 7);
#   (3c) FILL: fill_gate57.py writes the prompt, the launcher and pins_gate57.json — rc 10 on refusal;
#   (3d) RACE: develop and both heads re-read by ls-remote AFTER the fill — rc 10 / 11 if any moved meanwhile;
#   (4)  G57_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the filled launcher's own --check — rc 13
#        (it refuses a pin older than 30 min, exit 9);  (7) cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3d with the fill done as a SIMULATION (`dry<HHMMSS>.SIM.*`, never the real pins), then the SIM launcher's --check; the
# routing line's absence is REPORTED, not refused; it stops before (4). READ-ONLY in the Secuura checkout (ls-remote only). Nothing is merged,
# deployed or commented. Every step's output is written beside this script as launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*).
# Controls-only overrides (any one set makes a real launch refuse at step 4): G57_ROUTING (routing file), G57_CENSUS_OFFLINE (a SIM fixture
# dir for the API + census), G57_LSREMOTE_FILE (an ls-remote replay for steps 2 / 3d and the SIM launcher), G57_COMPARE_FILE (the SIM
# launcher's compare lines), G57_PREV_REPORT / G57_PREV_REPORT_2 (the fill's previous-round stand-ins).
# Usage: repin_and_launch_gate57.sh <PR1 number> <HEAD1 40-hex> <PR2 number> <HEAD2 40-hex> [--dry-run]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): v=v[k]
print("" if v is None else v)' "$GS/kit.json" "$1"; }
ROUTING="${G57_ROUTING:-$(KJ routing)}"; CUT="$(KJ cut_base)"; RX1="$(KJ prs.pr1.branch_rx)"; RX2="$(KJ prs.pr2.branch_rx)"
PR1="${1:-}"; HEAD1="${2:-}"; PR2="${3:-}"; HEAD2="${4:-}"; DRY=0; [ "${5:-}" = "--dry-run" ] && DRY=1
if [ "$PR1" = "--help" ] || [ "$PR1" = "-h" ]; then sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 0; fi
for _n in "$PR1" "$PR2"; do case "$_n" in ''|*[!0-9]*) echo "usage: repin_and_launch_gate57.sh <PR1> <HEAD1 40-hex> <PR2> <HEAD2 40-hex> [--dry-run]   (PR numbers must be digits)"; exit 9;; esac; done
for _h in "$HEAD1" "$HEAD2"; do printf '%s' "$_h" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: each HEAD must be the FULL 40-hex sha, got '$_h'"; exit 9; }; done
[ "$PR1" != "$PR2" ] && [ "$HEAD1" != "$HEAD2" ] || { echo "REFUSING: the two PRs (and heads) must differ"; exit 9; }
[ "$PR1" = "$(KJ prs.pr1.number)" ] && [ "$PR2" = "$(KJ prs.pr2.number)" ] || { echo "REFUSING: this kit was drafted for #$(KJ prs.pr1.number) then #$(KJ prs.pr2.number), in that order"; exit 9; }
PANE="QA/Secuura-ks1333-1345-$PR1"; T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
OFFARG=""; [ -n "${G57_CENSUS_OFFLINE:-}" ] && OFFARG="--offline-dir $G57_CENSUS_OFFLINE"
echo "LAUNCH ACTION gate57$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | #$PR1 $HEAD1 + #$PR2 $HEAD2 | cut_base $CUT | pane $PANE"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -x -F "$PANE|coagent@agentmail.to|yes" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"
rc=$?
echo "  routing file $ROUTING — line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0)"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here; README section 4)"; else echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README section 4; the drafter did NOT write it)"; exit 1; fi
fi

echo "--- 1. instrument A: the GitHub PULLS API, per PR (+ 2b the census, same read)$([ -n "$OFFARG" ] && echo '  [SIM REPLAY: G57_CENSUS_OFFLINE]')"
python3 "$GS/gh_census_gate57.py" --pr "$PR1" --body-out "$OUTP.body_pr$PR1.md" --exclude "$PR1,$PR2" $OFFARG > "$OUTP.api1.out" 2> "$OUTP.api1.err"; rc1=$?
python3 "$GS/gh_census_gate57.py" --pr "$PR2" --body-out "$OUTP.body_pr$PR2.md" --exclude "$PR1,$PR2" $OFFARG > "$OUTP.api2.out" 2> "$OUTP.api2.err"; rc2=$?
echo "  gh_census rc=$rc1 / $rc2"; sed 's/^/    /' "$OUTP.api1.out" "$OUTP.api2.out" | cut -c1-260; cat "$OUTP.api1.err" "$OUTP.api2.err" | sed 's/^/    stderr: /'
[ "$rc1" -eq 0 ] && [ "$rc2" -eq 0 ] || { echo "REFUSING: a PULLS API read failed"; exit 3; }
grep -q '^CENSUS ' "$OUTP.api1.out" || { echo "REFUSING: the census did not complete"; exit 3; }
apiline() { grep "^API #$1 head " "$2"; }
AL1="$(apiline "$PR1" "$OUTP.api1.out")"; AL2="$(apiline "$PR2" "$OUTP.api2.out")"
f() { echo "$1" | awk -v i="$2" '{print $i}'; }
BR1="$(f "$AL1" 18)"; BR2="$(f "$AL2" 18)"
[ -n "$BR1" ] && [ -n "$BR2" ] || { echo "REFUSING: could not read a PR's branch from the API line"; exit 3; }

echo "--- 2. instrument B: git ls-remote origin (ONE read from the Secuura checkout, READ-ONLY)$([ -n "${G57_LSREMOTE_FILE:-}" ] && echo '  [REPLAY: G57_LSREMOTE_FILE]')"
if [ -n "${G57_LSREMOTE_FILE:-}" ]; then cp "$G57_LSREMOTE_FILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; else
git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/pull/$PR1/head" "refs/heads/$BR1" "refs/pull/$PR2/head" "refs/heads/$BR2" > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"
rc=$?; fi
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"; [ -s "$OUTP.lsremote.err" ] && sed 's/^/    stderr: /' "$OUTP.lsremote.err"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
ref() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(ref refs/heads/develop)"

echo "--- 2b. the census"
if grep -q '^OVERLAP ' "$OUTP.api1.out"; then echo "REFUSING TO LAUNCH: another open PR touches a kit path or a Projects Documents file outside kit reported_overlaps — Wednesday sequences it; a re-draft decides"; exit 15; fi
echo "  OVERLAP census clean ($(grep -c '^EXPECTED OVERLAP' "$OUTP.api1.out") expected overlap(s) reported, $(grep -c '^SAME-KEY' "$OUTP.api1.out") SAME-KEY)"

echo "--- 3. each head, judged (input == API == pull/head == branch, open, not merged, on develop, not mergeable:false, branch rule)"
judge() {   # $1 label $2 PR $3 HEAD $4 BRANCH $5 api file $6 own rx $7 sibling rx
  local al; al="$(apiline "$2" "$5")"
  local A_HEAD A_BASE A_MERGE A_STATE A_MERGED PH BH
  A_HEAD="$(f "$al" 4)"; A_BASE="$(f "$al" 6)"; A_MERGE="$(f "$al" 10)"; A_STATE="$(f "$al" 14)"; A_MERGED="$(f "$al" 16)"
  PH="$(ref "refs/pull/$2/head")"; BH="$(ref "refs/heads/$4")"
  echo "  $1 #$2: input $3 | API $A_HEAD (state $A_STATE, merged $A_MERGED, base $A_BASE, mergeable $A_MERGE) | pull/head ${PH:-ABSENT} | $4 ${BH:-ABSENT}"
  if [ "$A_HEAD" = "$3" ] && [ "$PH" = "$3" ] && [ "$BH" = "$3" ] && [ "$A_STATE" = "open" ] && [ "$A_MERGED" = "False" ] && [ "$A_BASE" = "develop" ] && [ "$A_MERGE" != "False" ] && printf '%s' "$4" | grep -qE "$6" && ! printf '%s' "$4" | grep -qE "$7"; then
    echo "    BOTH INSTRUMENTS AGREE with the input head."
  else
    echo "REFUSING TO LAUNCH: $1 #$2 — the input head is not the PR's head on both instruments, or the PR is not open / merged / not on develop / mergeable:false / off its branch rule — a stale pin is never launched"; exit 11
  fi
}
judge "PR 1" "$PR1" "$HEAD1" "$BR1" "$OUTP.api1.out" "$RX1" "$RX2"
judge "PR 2" "$PR2" "$HEAD2" "$BR2" "$OUTP.api2.out" "$RX2" "$RX1"

echo "--- 3b. develop, read at launch: $CUR_DEV | cut_base $CUT"
BEHIND=0
if [ "$CUR_DEV" != "$CUT" ]; then
  python3 "$GS/gh_census_gate57.py" --advance "$CUR_DEV" --exclude "$PR1,$PR2" $OFFARG > "$OUTP.advance.out" 2> "$OUTP.advance.err"; rc=$?
  sed 's/^/    /' "$OUTP.advance.out" | grep -E '^    (ADVANCE|ADVANCE-PATH) ' | cut -c1-200
  AV="$(grep '^ADVANCE ' "$OUTP.advance.out")"
  [ "$rc" -eq 0 ] && [ -n "$AV" ] || { echo "REFUSING TO LAUNCH: the develop-advance compare failed (rc $rc)"; exit 10; }
  BEHIND="$(echo "$AV" | sed -E 's/.*behind=([0-9]+).*/\1/')"; OVL="$(echo "$AV" | sed -E 's/.*overlap=([^ ]*).*/\1/')"; MB="$(echo "$AV" | sed -E 's/.*merge_base=([0-9a-f]+).*/\1/')"
  [ "$OVL" = "NONE" ] && [ "$MB" = "$CUT" ] && [ "$BEHIND" -gt 0 ] || { echo "REFUSING TO LAUNCH: develop moved ($CUT -> $CUR_DEV) and the advance touches a kit path / Projects Documents ($OVL) or does not descend from cut_base (merge_base $MB): RE-DRAFT (README section 7)"; exit 10; }
  echo "  ADVANCED by $BEHIND commit(s), DISJOINT from every kit path and Projects Documents/ — accepted (README section 7); T2 must be re-derived on this develop by C4-PREDICT (--develop)"
else
  echo "  UNMOVED since drafting"
fi

echo "--- 3c. FILL from the values just read"
if [ "$DRY" = 1 ]; then SIMARG="--simulate dry$T"; else SIMARG=""; fi
python3 "$GS/fill_gate57.py" --pr1 "$PR1" --head1 "$HEAD1" --branch1 "$BR1" --pr2 "$PR2" --head2 "$HEAD2" --branch2 "$BR2" --develop "$CUR_DEV" --behind "$BEHIND" $SIMARG > "$OUTP.fill.out" 2> "$OUTP.fill.err"
rc=$?
echo "  fill rc=$rc"; sed 's/^/    /' "$OUTP.fill.out" "$OUTP.fill.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the fill refused"; exit 10; }
if [ "$DRY" = 1 ]; then L="$GS/dry$T.SIM.launcher.sh"; else L="$GS/$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["launcher"])' "$GS/pins_gate57.json")"; fi

echo "--- 3d. RACE: re-read develop and both heads AFTER the fill"
if [ -n "${G57_LSREMOTE_FILE:-}" ]; then cp "$G57_LSREMOTE_FILE" "$OUTP.lsremote2.out"; : > "$OUTP.lsremote2.err"; rc=0; else
git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/pull/$PR1/head" "refs/pull/$PR2/head" > "$OUTP.lsremote2.out" 2> "$OUTP.lsremote2.err"
rc=$?; fi
D2="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote2.out")"; Q1="$(awk -v r="refs/pull/$PR1/head" '$2==r{print $1}' "$OUTP.lsremote2.out")"; Q2="$(awk -v r="refs/pull/$PR2/head" '$2==r{print $1}' "$OUTP.lsremote2.out")"
echo "  ls-remote rc=$rc | develop $D2 | pull/$PR1 $Q1 | pull/$PR2 $Q2"
[ "$rc" -eq 0 ] && [ "$D2" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: develop moved DURING the fill — run this script again"; exit 10; }
[ "$Q1" = "$HEAD1" ] && [ "$Q2" = "$HEAD2" ] || { echo "REFUSING TO LAUNCH: a head moved DURING the fill — run this script again with the new head"; exit 11; }

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the SIM launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"
  rc=$?
  echo "  SIM launcher --check rc=$rc"; sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the SIM launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — every read agrees with the input; the real run fills the REAL pins and continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi

echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G57_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G57_* test override is set"; exit 16; }

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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') #$PR1 at $HEAD1 + #$PR2 at $HEAD2 over develop $CUR_DEV"
