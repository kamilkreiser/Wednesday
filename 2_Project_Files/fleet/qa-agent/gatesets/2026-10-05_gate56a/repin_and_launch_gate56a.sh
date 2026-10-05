#!/bin/bash
# repin_and_launch_gate56a.sh — the LAUNCH ACTION for the gate56a kit (the directory this script lives in). TWO PRs (Seat B 59th's PR 3
# KS-528 and PR 4 KS-769, ONE READY), whose numbers and heads are INPUTS from that READY. Re-pin and launch are ONE action (Kam
# 2026-09-18): it READS everything AT LAUNCH and never trusts a pin it did not just re-read. A NEW COPY of repin_and_launch_gate55.sh,
# re-keyed for two PRs:
#   (0)  the pane QA/Secuura-ks528-769-<n3> is routed (inbox_routing.conf) — rc 1;
#   (1)  the GitHub PULLS API for EACH PR: head sha, branch, base, state, merged, mergeable — rc 3; each body saved beside this script as
#        <log>.body_pr<n>.md (C1 / C5 read it);
#   (2)  ONE `git ls-remote` READ from the Secuura checkout: develop + both refs/pull/<n>/head + both branches — rc 2;
#   (2b) the OVERLAP census over every OTHER open PR: rc 15 on an OVERLAP (another PR touches either kit path); SAME-KEY reported only;
#   (3)  rc 11 unless, for EACH PR, input head == API head == pull/head == branch (WHOLE-FIELD), open, not merged, base develop, not
#        `mergeable: false`, the branch carries its own key and not the sibling's; and the two PRs differ;
#   (3b) STALE BASE: rc 10 if origin develop != kit base (14d40d4455c7);
#   (3c) FILL: fill_gate56a.py writes the prompt, the launcher and pins_gate56a.json — rc 10 on refusal;
#   (3d) RACE: develop and both heads re-read by ls-remote AFTER the fill — rc 10 / 11 if any moved meanwhile;
#   (4)  G56A_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the filled launcher's own --check — rc 13;
#   (7)  cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3d with the fill done as a SIMULATION (`dry<HHMMSS>.SIM.*`, never the real pins), then the SIM launcher's --check; the
# routing line's absence is REPORTED, not refused; it stops before (4). READ-ONLY in the Secuura checkout (ls-remote only). Nothing is merged,
# deployed or commented. Every step's output is written beside this script as launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*).
# Controls-only overrides (any one set makes a real launch refuse at step 4): G56A_ROUTING (routing file), G56A_CENSUS_OFFLINE (a SIM fixture
# dir for the API + census), G56A_LSREMOTE_FILE (an ls-remote replay for steps 2 / 3d and the SIM launcher), G56A_PREV_REPORT (the fill's
# previous-round stand-in), G56A_COMPARE_FILE (the SIM launcher's compare lines).
# Usage: repin_and_launch_gate56a.sh <PR3 number> <HEAD3 40-hex> <PR4 number> <HEAD4 40-hex> [--dry-run]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): v=v[k]
print("" if v is None else v)' "$GS/kit.json" "$1"; }
ROUTING="${G56A_ROUTING:-$(KJ routing)}"; BASE="$(KJ base)"; RX3="$(KJ prs.pr3.branch_rx | sed 's/(?i)//')"; RX4="$(KJ prs.pr4.branch_rx | sed 's/(?i)//')"
PR3="${1:-}"; HEAD3="${2:-}"; PR4="${3:-}"; HEAD4="${4:-}"; DRY=0; [ "${5:-}" = "--dry-run" ] && DRY=1
if [ "$PR3" = "--help" ] || [ "$PR3" = "-h" ]; then sed -n '2,28p' "$0" | sed 's/^# \{0,1\}//'; exit 0; fi
for _n in "$PR3" "$PR4"; do case "$_n" in ''|*[!0-9]*) echo "usage: repin_and_launch_gate56a.sh <PR3> <HEAD3 40-hex> <PR4> <HEAD4 40-hex> [--dry-run]   (PR numbers must be digits)"; exit 9;; esac; done
for _h in "$HEAD3" "$HEAD4"; do printf '%s' "$_h" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: each HEAD must be the FULL 40-hex sha, got '$_h'"; exit 9; }; done
[ "$PR3" != "$PR4" ] && [ "$HEAD3" != "$HEAD4" ] || { echo "REFUSING: the two PRs (and heads) must differ"; exit 9; }
PANE="QA/Secuura-ks528-769-$PR3"; T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
OFFARG=""; [ -n "${G56A_CENSUS_OFFLINE:-}" ] && OFFARG="--offline-dir $G56A_CENSUS_OFFLINE"
echo "LAUNCH ACTION gate56a$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | #$PR3 $HEAD3 + #$PR4 $HEAD4 | kit base $BASE | pane $PANE"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -x -F "$PANE|coagent@agentmail.to|yes" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"
rc=$?
echo "  routing file $ROUTING — line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0)"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here; README section 4)"; else echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README section 4; the drafter did NOT write it)"; exit 1; fi
fi

echo "--- 1. instrument A: the GitHub PULLS API, per PR (+ 2b the census, same read)$([ -n "$OFFARG" ] && echo '  [SIM REPLAY: G56A_CENSUS_OFFLINE]')"
python3 "$GS/gh_census_gate56a.py" --pr "$PR3" --body-out "$OUTP.body_pr$PR3.md" --exclude "$PR3,$PR4" $OFFARG > "$OUTP.api3.out" 2> "$OUTP.api3.err"; rc3=$?
python3 "$GS/gh_census_gate56a.py" --pr "$PR4" --body-out "$OUTP.body_pr$PR4.md" --exclude "$PR3,$PR4" $OFFARG > "$OUTP.api4.out" 2> "$OUTP.api4.err"; rc4=$?
echo "  gh_census rc=$rc3 / $rc4"; sed 's/^/    /' "$OUTP.api3.out" "$OUTP.api4.out" | cut -c1-260; cat "$OUTP.api3.err" "$OUTP.api4.err" | sed 's/^/    stderr: /'
[ "$rc3" -eq 0 ] && [ "$rc4" -eq 0 ] || { echo "REFUSING: a PULLS API read failed"; exit 3; }
grep -q '^CENSUS ' "$OUTP.api3.out" || { echo "REFUSING: the census did not complete"; exit 3; }
apiline() { grep "^API #$1 head " "$2"; }
AL3="$(apiline "$PR3" "$OUTP.api3.out")"; AL4="$(apiline "$PR4" "$OUTP.api4.out")"
f() { echo "$1" | awk -v i="$2" '{print $i}'; }
BR3="$(f "$AL3" 18)"; BR4="$(f "$AL4" 18)"
[ -n "$BR3" ] && [ -n "$BR4" ] || { echo "REFUSING: could not read a PR's branch from the API line"; exit 3; }

echo "--- 2. instrument B: git ls-remote origin (ONE read from the Secuura checkout, READ-ONLY)$([ -n "${G56A_LSREMOTE_FILE:-}" ] && echo '  [REPLAY: G56A_LSREMOTE_FILE]')"
if [ -n "${G56A_LSREMOTE_FILE:-}" ]; then cp "$G56A_LSREMOTE_FILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; else
git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' ls-remote origin refs/heads/develop "refs/pull/$PR3/head" "refs/heads/$BR3" "refs/pull/$PR4/head" "refs/heads/$BR4" > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"
rc=$?; fi
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"; [ -s "$OUTP.lsremote.err" ] && sed 's/^/    stderr: /' "$OUTP.lsremote.err"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
ref() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(ref refs/heads/develop)"

echo "--- 2b. the census"
if grep -q '^OVERLAP ' "$OUTP.api3.out"; then echo "REFUSING TO LAUNCH: another open PR touches audit-baseline.json or lock-discovery.mjs — Wednesday sequences it; a re-draft decides"; exit 15; fi
echo "  OVERLAP census clean ($(grep -c '^SAME-KEY' "$OUTP.api3.out") SAME-KEY PR(s) reported)"

echo "--- 3. each head, judged (input == API == pull/head == branch, open, not merged, on develop, not mergeable:false, branch keys)"
for _x in "3 $PR3 $HEAD3 $BR3 $RX3 $RX4" "4 $PR4 $HEAD4 $BR4 $RX4 $RX3"; do
  set -- $_x; _al="$(apiline "$2" "$OUTP.api$1.out")"
  A_HEAD="$(f "$_al" 4)"; A_BASE="$(f "$_al" 6)"; A_MERGE="$(f "$_al" 10)"; A_STATE="$(f "$_al" 14)"; A_MERGED="$(f "$_al" 16)"
  PH="$(ref "refs/pull/$2/head")"; BH="$(ref "refs/heads/$4")"
  echo "  PR $1 #$2: input $3 | API $A_HEAD (state $A_STATE, merged $A_MERGED, base $A_BASE, mergeable $A_MERGE) | pull/head ${PH:-ABSENT} | $4 ${BH:-ABSENT}"
  if [ "$A_HEAD" = "$3" ] && [ "$PH" = "$3" ] && [ "$BH" = "$3" ] && [ "$A_STATE" = "open" ] && [ "$A_MERGED" = "False" ] && [ "$A_BASE" = "develop" ] && [ "$A_MERGE" != "False" ] && printf '%s' "$4" | grep -qiE "$5" && ! printf '%s' "$4" | grep -qiE "$6"; then
    echo "    BOTH INSTRUMENTS AGREE with the input head."
  else
    echo "REFUSING TO LAUNCH: PR $1 #$2 — the input head is not the PR's head on both instruments, or the PR is not open / merged / not on develop / mergeable:false / its branch does not carry $5 alone — a stale pin is never launched"; exit 11
  fi
done
set --

echo "--- 3b. develop, read at launch: $CUR_DEV | kit base $BASE"
[ "$CUR_DEV" = "$BASE" ] || { echo "REFUSING TO LAUNCH: STALE BASE — develop moved since drafting ($BASE -> $CUR_DEV); RE-DRAFT (README section 7)"; exit 10; }
echo "  UNMOVED since drafting"

echo "--- 3c. FILL from the values just read"
if [ "$DRY" = 1 ]; then SIMARG="--simulate dry$T"; else SIMARG=""; fi
python3 "$GS/fill_gate56a.py" --pr3 "$PR3" --head3 "$HEAD3" --branch3 "$BR3" --pr4 "$PR4" --head4 "$HEAD4" --branch4 "$BR4" --develop "$CUR_DEV" $SIMARG > "$OUTP.fill.out" 2> "$OUTP.fill.err"
rc=$?
echo "  fill rc=$rc"; sed 's/^/    /' "$OUTP.fill.out" "$OUTP.fill.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the fill refused"; exit 10; }
if [ "$DRY" = 1 ]; then L="$GS/dry$T.SIM.launcher.sh"; else L="$GS/$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["launcher"])' "$GS/pins_gate56a.json")"; fi

echo "--- 3d. RACE: re-read develop and both heads AFTER the fill"
if [ -n "${G56A_LSREMOTE_FILE:-}" ]; then cp "$G56A_LSREMOTE_FILE" "$OUTP.lsremote2.out"; : > "$OUTP.lsremote2.err"; rc=0; else
git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' ls-remote origin refs/heads/develop "refs/pull/$PR3/head" "refs/pull/$PR4/head" > "$OUTP.lsremote2.out" 2> "$OUTP.lsremote2.err"
rc=$?; fi
D2="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote2.out")"; P3="$(awk -v r="refs/pull/$PR3/head" '$2==r{print $1}' "$OUTP.lsremote2.out")"; P4="$(awk -v r="refs/pull/$PR4/head" '$2==r{print $1}' "$OUTP.lsremote2.out")"
echo "  ls-remote rc=$rc | develop $D2 | pull/$PR3 $P3 | pull/$PR4 $P4"
[ "$rc" -eq 0 ] && [ "$D2" = "$BASE" ] || { echo "REFUSING TO LAUNCH: develop moved DURING the fill — run this script again"; exit 10; }
[ "$P3" = "$HEAD3" ] && [ "$P4" = "$HEAD4" ] || { echo "REFUSING TO LAUNCH: a head moved DURING the fill — run this script again with the new head"; exit 11; }

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the SIM launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"
  rc=$?
  echo "  SIM launcher --check rc=$rc"; sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the SIM launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — every read agrees with the input; the real run fills the REAL pins and continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi

echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G56A_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G56A_* test override is set"; exit 16; }

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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') #$PR3 at $HEAD3 + #$PR4 at $HEAD4 over develop $CUR_DEV"
