#!/bin/bash
# launch_r2_gate61r2.sh — the LAUNCH ACTION for gate61 ROUND 2 (#1383, KS-1401, narrowed to ONE commit). Re-read and launch are ONE action: it
# reads everything AT LAUNCH and trusts no pin it did not just re-read. Shape: gate61's repin_and_launch, reduced (no fill: the prompt is
# drafted for exactly ONE head; a different head is a RE-DRAFT).
#   (0) the pane QA/Secuura-ks1401-1383r2 is routed (inbox_routing.conf) — rc 1 (a dry run REPORTS it);
#   (1) the GitHub PULLS API (GH_TOKEN read BY NAME in a subshell, never printed): head, branch, base, state, merged — rc 3;
#   (2) ONE `git ls-remote` READ from the Secuura checkout: develop + refs/pull/1383/head + the exact branch — rc 2;
#   (3) rc 11 unless INPUT == kit head == API head == pull/head == branch, open, not merged, base develop, kit branch;
#   (3b) develop is RECORDED, never refused (Kam's merge order moves it first);
#   (3c) the kit's own read-only scope instrument at the head (r2_check_gate61r2.py scope, S1-S9) — rc 13 on any FAIL;
#   (4) G61R2_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's own --check — rc 13;
#   (7) cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3c and the launcher's --check; stops before (4). Every step's output is written beside this script as launch_<HHMMSS>.*
# (dry: dry_<HHMMSS>.*). READ-ONLY in the Secuura checkout. Controls-only override: G61R2_ROUTING (a routing file standing in).
# Usage: launch_r2_gate61r2.sh <PR number> <HEAD 40-hex> [--dry-run]
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$GS/kit.json" "$1"; }
ROUTING="${G61R2_ROUTING:-$(KJ routing)}"; KHEAD="$(KJ head)"; KBR="$(KJ branch)"; KPR="$(KJ pr)"; PANE="$(KJ pane)"; RLINE="$(KJ routing_line)"
L="$GS/$(KJ launcher)"; ENVF="$(KJ secuura_env)"
PR="${1:-}"; HEAD="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
if [ "$PR" = "--help" ] || [ "$PR" = "-h" ]; then sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'; exit 0; fi
case "$PR" in ''|*[!0-9]*) echo "usage: launch_r2_gate61r2.sh <PR number> <HEAD 40-hex> [--dry-run]"; exit 9;; esac
printf '%s' "$HEAD" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: HEAD must be the FULL 40-hex sha, got '$HEAD'"; exit 9; }
[ "$PR" = "$KPR" ] || { echo "REFUSING: PR #$PR is not this kit's PR (#$KPR)"; exit 9; }
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate61 ROUND 2$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | PR #$PR | HEAD $HEAD | pane $PANE"

echo "--- 0. the pane must be routed"
/usr/bin/grep -c -x -F "$RLINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"
rc=$?
echo "  routing file $ROUTING — line '$RLINE' present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0)"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here; README section 4)"; else echo "REFUSING: $PANE is not registered — add the line first (README section 4)"; exit 1; fi
fi

echo "--- 1. instrument A: the GitHub PULLS API"
( set -a; . "$ENVF"; set +a; PRN="$PR" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
try:
    p = json.load(urllib.request.urlopen(urllib.request.Request("https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/" + os.environ["PRN"], headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
    print("API %s head %s base %s state %s merged %s branch %s mergeable_state %s updated_at %s" % (p["number"], p["head"]["sha"], p["base"]["ref"], p["state"], p["merged"], p["head"]["ref"], p.get("mergeable_state"), p.get("updated_at")))
except Exception as e:
    print("ERROR %s" % e)
PY
) > "$OUTP.api.out" 2> "$OUTP.api.err"
rc=$?
echo "  api rc=$rc"; sed 's/^/    /' "$OUTP.api.out"; [ -s "$OUTP.api.err" ] && sed 's/^/    stderr: /' "$OUTP.api.err"
grep -q '^API ' "$OUTP.api.out" || { echo "REFUSING: the PULLS API read failed"; exit 3; }
AL="$(grep '^API ' "$OUTP.api.out")"
A_HEAD="$(echo "$AL" | awk '{print $4}')"; A_BASE="$(echo "$AL" | awk '{print $6}')"; A_STATE="$(echo "$AL" | awk '{print $8}')"; A_MERGED="$(echo "$AL" | awk '{print $10}')"; BR="$(echo "$AL" | awk '{print $12}')"

echo "--- 2. instrument B: git ls-remote origin (ONE read, READ-ONLY)"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/pull/$PR/head" "refs/heads/$KBR" > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"
rc=$?
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"; [ -s "$OUTP.lsremote.err" ] && sed 's/^/    stderr: /' "$OUTP.lsremote.err"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"; PH="$(awk -v r="refs/pull/$PR/head" '$2==r{print $1}' "$OUTP.lsremote.out")"; BH="$(awk -v r="refs/heads/$KBR" '$2==r{print $1}' "$OUTP.lsremote.out")"

echo "--- 3. the head, judged (input == kit head == API == pull/head == branch, open, not merged, on develop, kit branch)"
echo "  input $HEAD | kit $KHEAD | API $A_HEAD (state $A_STATE, merged $A_MERGED, base $A_BASE) | pull/head ${PH:-ABSENT} | branch ${BH:-ABSENT} ($BR)"
if [ "$HEAD" = "$KHEAD" ] && [ "$A_HEAD" = "$HEAD" ] && [ "$PH" = "$HEAD" ] && [ "$BH" = "$HEAD" ] && [ "$A_STATE" = "open" ] && [ "$A_MERGED" = "False" ] && [ "$A_BASE" = "develop" ] && [ "$BR" = "$KBR" ]; then
  echo "  BOTH INSTRUMENTS AGREE with the input head, 1 of 1."
else
  echo "REFUSING TO LAUNCH: the input head is not the kit head / the PR's head on both instruments, or the PR is not open / is merged / is off develop or the kit branch — a new head is a RE-DRAFT"; exit 11
fi

echo "--- 3b. develop, read at launch: $CUR_DEV (RECORDED, not refused: the KS-1404 anchor-wiring PR merges before #1383)"

echo "--- 3c. the kit's read-only scope instrument at the head (S1-S9)"
python3 "$GS/r2_check_gate61r2.py" scope --repo "$CHECKOUT" --head "$HEAD" > "$OUTP.scope.out" 2> "$OUTP.scope.err"
rc=$?
echo "  scope rc=$rc | $(grep '^CHECKED' "$OUTP.scope.out")"; grep '^FAIL' "$OUTP.scope.out" | sed 's/^/    /'; [ -s "$OUTP.scope.err" ] && sed 's/^/    stderr: /' "$OUTP.scope.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the scope instrument FAILED at the head (or could not read it)"; exit 13; }

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"
  rc=$?
  echo "  launcher --check rc=$rc"; sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — every read agrees with the input; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi

echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G61R2_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G61R2_* test override is set"; exit 16; }

echo "--- 5. usage gate"
"$(KJ usage_gate)" --check > "$OUTP.usage_gate.out" 2> "$OUTP.usage_gate.err"
rc=$?
echo "  usage_gate rc=$rc (WED_USAGE_STOP=${WED_USAGE_STOP:-unset})"; sed 's/^/    /' "$OUTP.usage_gate.out" "$OUTP.usage_gate.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused (pass WED_USAGE_STOP only with Kam's recorded authority)"; exit 12; }

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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') PR #$PR at $HEAD; develop at launch $CUR_DEV"
