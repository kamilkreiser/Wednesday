#!/bin/bash
# repin_and_launch_gate64.sh — the LAUNCH ACTION for gate64 (#1389, KS-1330, T2). Inputs PR + HEAD must equal the kit's. It READS
# everything at launch and never trusts a pin it did not just re-read (Kam 2026-09-18: re-pin and launch are ONE action):
#   (0)  the pane QA/Secuura-ks1330-1389 is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead);
#   (1)  the census + PULLS API (gh_census_gate64.py): rc 3 on an API failure or a BLIND control, rc 15 on an OVERLAP (incl. a MOVED #1250);
#   (2)  ONE `git ls-remote` from the Secuura checkout (read verb only; the checkout's own core.sshCommand) — rc 2;
#   (3)  rc 11 unless input == kit head == API head == pull/head == branch, the PR open, not merged, based on develop; rc 15 if #1250's
#        pull/head or branch left the kit's 2b8dcb824dd2. A moved HEAD is NEVER re-pinnable here: every kit figure (END_TREE, blobs,
#        +/-, the C3 evidence) is about a7f5965a7b3f, so a new head is a RE-DRAFT (README section 8);
#   (3b) develop: unmoved -> on. MOVED -> prints the new sha, the advance (local objects if the checkout has them, else a read-only
#        GitHub compare GET), and the MERGE-IN REQUIREMENT (Seat G 2nd merges develop in; judged by the KEY-ANCHORED target tree,
#        c4_docs_gate64.py predict/qm — never a div-anchored one). Then REFUSES rc 10 unless re-pinned with
#        `--repin-develop <that exact 40-hex>` (a stale or different sha is rc 10 too). NOT re-pinnable (hard rc 10): develop does not
#        descend from the kit develop, or the advance touches a kit path or a hook path;
#   (3c) the kit's read-only C1 instrument at the head (c1_pin_gate64.py --no-remote at the kit develop; origin was read in step 2) — rc 13;
#   (4)  G64_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's own --check — rc 13;
#   (7)  cockpit.sh add <pane> <launcher> — rc 14, then a pane census. Rung 5 is Wednesday's, after this (README section 7).
# --dry-run: steps 0-3c and the launcher's --check, then stops (no usage gate, no cockpit). Every step's output goes to launch_<HHMMSS>.*
# (dry: dry_<HHMMSS>.*) beside this script. Controls-only overrides: G64_ROUTING (a routing file stand-in), G64_LSFILE (a file standing in
# for the ls-remote output; DRY RUN ONLY — a real run refuses it at step 4 like every G64_*).
# Usage: repin_and_launch_gate64.sh <PR> <HEAD 40-hex> [--dry-run] [--repin-develop <40-hex>]   (under `script -q /dev/null` — README 7)
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))[sys.argv[2]]; print(" ".join(v) if isinstance(v,list) else v)' "$GS/kit.json" "$1"; }
ROUTING="${G64_ROUTING:-$(KJ routing)}"; KDEV="$(KJ develop_at_draft)"; KHEAD="$(KJ head)"; KBR="$(KJ branch)"; KPR="$(KJ pr)"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"
K1250="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["pr1250"]["head"])' "$GS/kit.json")"
B1250="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["pr1250"]["branch"])' "$GS/kit.json")"
L="$GS/$(KJ launcher)"
PR="${1:-}"; HEAD="${2:-}"; DRY=0; REPIN=""
shift 2 2>/dev/null
while [ $# -gt 0 ]; do
  case "$1" in --dry-run) DRY=1; shift;; --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;; *) echo "usage: repin_and_launch_gate64.sh <PR> <HEAD 40-hex> [--dry-run] [--repin-develop <40-hex>]"; exit 9;; esac
done
case "$PR" in ''|*[!0-9]*) echo "usage: repin_and_launch_gate64.sh <PR> <HEAD 40-hex> [--dry-run] [--repin-develop <40-hex>]"; exit 9;; esac
printf '%s' "$HEAD" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: HEAD must be the FULL 40-hex sha, got '$HEAD'"; exit 9; }
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
[ "$PR" = "$KPR" ] || { echo "REFUSING: PR #$PR is not this kit's PR (#$KPR)"; exit 9; }
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate64$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | PR #$PR | HEAD $HEAD | kit develop $KDEV | repin-develop ${REPIN:-none} | pane $PANE"

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; README section 4)"; else echo "REFUSING: add the routing line first (README section 4): $LINE"; exit 1; fi
fi

echo "--- 1. census + PULLS API"
python3 "$GS/gh_census_gate64.py" --json "$OUTP.census.json" > "$OUTP.census.out" 2> "$OUTP.census.err"; rc=$?
sed 's/^/    /' "$OUTP.census.out" | cut -c1-240; [ -s "$OUTP.census.err" ] && sed 's/^/    stderr: /' "$OUTP.census.err"
echo "  census rc=$rc"
[ "$rc" -eq 3 ] && { echo "REFUSING: API failure or a BLIND census control"; exit 3; }
[ "$rc" -eq 15 ] && { echo "REFUSING: an OVERLAP on a kit path (or #1250 moved) — read it first"; exit 15; }
[ "$rc" -eq 0 ] || { echo "REFUSING: census rc $rc"; exit 3; }
A_LINE="$(grep '^API #' "$OUTP.census.out")"
A_HEAD="$(printf '%s' "$A_LINE" | awk '{print $4}')"; A_BR="$(printf '%s' "$A_LINE" | awk '{print $6}')"; A_BASE="$(printf '%s' "$A_LINE" | awk '{print $8}')"
A_STATE="$(printf '%s' "$A_LINE" | awk '{print $10}')"; A_MERGED="$(printf '%s' "$A_LINE" | awk '{print $12}')"

echo "--- 2. ONE ls-remote (read verb) from the checkout"
if [ -n "${G64_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G64_LSFILE is a dry-run control only"; exit 16; }
  cp "$G64_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G64_LSFILE)"
else
  git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/heads/$KBR" "refs/pull/$PR/head" "refs/heads/$B1250" "refs/pull/1250/head" > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"; PH="$(awk -v r="refs/pull/$PR/head" '$2==r{print $1}' "$OUTP.lsremote.out")"; BH="$(awk -v r="refs/heads/$KBR" '$2==r{print $1}' "$OUTP.lsremote.out")"
P50="$(awk '$2=="refs/pull/1250/head"{print $1}' "$OUTP.lsremote.out")"; B50="$(awk -v r="refs/heads/$B1250" '$2==r{print $1}' "$OUTP.lsremote.out")"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV | pull/head $PH | branch $BH | #1250 pull $P50 branch $B50"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }

echo "--- 3. the head: input == kit == API == pull/head == branch; open, not merged, on develop"
echo "  input $HEAD | kit $KHEAD | API $A_HEAD ($A_STATE, merged $A_MERGED, base $A_BASE, branch $A_BR) | pull/head $PH | branch $BH"
if [ "$HEAD" = "$KHEAD" ] && [ "$A_HEAD" = "$HEAD" ] && [ "$PH" = "$HEAD" ] && [ "$BH" = "$HEAD" ] && [ "$A_STATE" = "open" ] && [ "$A_MERGED" = "False" ] && [ "$A_BASE" = "develop" ] && [ "$A_BR" = "$KBR" ]; then
  echo "  BOTH INSTRUMENTS AGREE with the input head."
else echo "REFUSING TO LAUNCH: the head is not the kit head on both instruments, or the PR is not open / merged / off develop. A new head is a RE-DRAFT (README section 8); --repin-develop does not cover a head"; exit 11; fi
[ "$P50" = "$K1250" ] && [ "$B50" = "$K1250" ] || { echo "REFUSING TO LAUNCH: #1250 moved (pull $P50 / branch $B50 != kit $K1250) — Q-1250 says it must not; read it first"; exit 15; }
echo "  #1250 UNTOUCHED at ${K1250:0:12} (pull/head AND branch)"

echo "--- 3b. develop: origin $CUR_DEV | kit (at READY / drafting) $KDEV"
if [ "$CUR_DEV" = "$KDEV" ]; then
  echo "  UNMOVED since drafting. The head's parent is 0f2422925317, NOT develop: the merge still needs Seat G 2nd's merge-in (README section 6); predicted tree $(KJ merge_in_predicted_tree)"
else
  echo "  DEVELOP MOVED: $KDEV -> $CUR_DEV"
  python3 - "$GS" "$CHECKOUT" "$KDEV" "$CUR_DEV" > "$OUTP.advance.out" 2> "$OUTP.advance.err" <<'PYEOF'
import json, os, subprocess, sys
gs, co, kd, nd = sys.argv[1:5]
sys.path.insert(0, gs)
from lib_gate64 import K, gh_get
local = subprocess.run(['git', '-C', co, 'cat-file', '-t', nd], capture_output=True).returncode == 0
if local:
    anc = subprocess.run(['git', '-C', co, 'merge-base', '--is-ancestor', kd, nd]).returncode == 0
    files = subprocess.run(['git', '-C', co, 'diff', '--name-only', kd, nd], capture_output=True, text=True).stdout.split()
    src = 'local objects (read verbs)'; status = 'ahead' if anc else 'NOT-A-DESCENDANT'
else:
    c = gh_get('compare/%s...%s' % (kd, nd)); status = c['status']; anc = status in ('ahead', 'identical')
    files = [f['filename'] for f in c.get('files', [])]; src = 'GitHub compare GET (objects not in the checkout; ahead_by %s, behind_by %s)' % (c.get('ahead_by'), c.get('behind_by'))
code = set(K['files']); hooks = set(K['hook_blobs']); docs = {K['flow'], K['cheat']}
hit = sorted(set(files) & (code | hooks))
suites = sorted(p for p in files if p.endswith('.test.sh') and any(p.startswith(r + '/') and '/' not in p[len(r) + 1:] for r in K['roots']))
print('SOURCE %s' % src)
print('STATUS %s' % status)
print('ADVANCE %d path(s); docs among them %s' % (len(files), sorted(os.path.basename(x)[:28] for x in set(files) & docs)))
print('KITHIT %s' % (hit or 'none'))
print('SUITES %s' % (suites or 'none'))
for f in files[:40]: print('  path %s' % f)
raise SystemExit(0 if anc and not hit else 10)
PYEOF
  arc=$?
  sed 's/^/    /' "$OUTP.advance.out" | cut -c1-200; [ -s "$OUTP.advance.err" ] && sed 's/^/    stderr: /' "$OUTP.advance.err" | tail -3
  if [ "$arc" -ne 0 ]; then
    echo "REFUSING TO LAUNCH (NOT re-pinnable): develop does not descend from the kit develop, the advance touches a kit / hook path, or it could not be read (rc $arc). That is a RE-GATE / RE-DRAFT, not a merge-in: README section 8"; exit 10
  fi
  grep -q '^SUITES none' "$OUTP.advance.out" || echo "  COUPLING NOTE: the advance changes runner-globbed suites — the gate re-runs c3_census_gate64.py at the predicted merge-in tree"
  echo "  MERGE-IN REQUIREMENT: the head a7f5965a7b3f is unaffected and stays the gated head. Before the merge, Seat G 2nd merges develop"
  echo "    $CUR_DEV IN (a merge commit M, never a rebase, never a force push). #1389 carries NO doc hunk, so every doc at M must equal develop's"
  echo "    byte for byte. M is covered by gate64 ONLY if \`c4_docs_gate64.py qm --repo <own clone> --merge-in-head M --develop-after $CUR_DEV\`"
  echo "    passes M1-M8: tree(M) == the KEY-ANCHORED predicted tree on THAT develop (sections found by their h2 KS key, never by"
  echo "    \`<div class=\"section\">\` or tail position: the cheat sheet has no readable ordering invariant). Anything else re-gates."
  if [ -z "$REPIN" ]; then
    echo "REFUSING TO LAUNCH: develop moved. To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then
    echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin) — re-read and re-run"; exit 10
  fi
  { echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $KDEV -> $CUR_DEV (told to re-pin by --repin-develop)"; cat "$OUTP.advance.out"; } > "$OUTP.repin.txt"
  echo "  RE-PINNED develop -> $CUR_DEV (recorded: $OUTP.repin.txt). The gate reads develop itself at start / mid / end and predicts on the develop it reads."
fi

echo "--- 3c. the kit's read-only C1 instrument at the head (P2-P11; origin was read in step 2)"
python3 "$GS/c1_pin_gate64.py" --repo "$CHECKOUT" --head "$HEAD" --develop "$KDEV" --no-remote > "$OUTP.c1.out" 2> "$OUTP.c1.err"; rc=$?
echo "  c1 rc=$rc | $(grep '^CHECKED' "$OUTP.c1.out") | $(grep -E '^[0-9]+ FAIL' "$OUTP.c1.out")"; grep '^FAIL' "$OUTP.c1.out" | sed 's/^/    /' | cut -c1-240; [ -s "$OUTP.c1.err" ] && sed 's/^/    stderr: /' "$OUTP.c1.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the C1 instrument FAILED at the head (or could not read it)"; exit 13; }

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — develop $CUR_DEV; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G64_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G64_* override is set"; exit 16; }
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
