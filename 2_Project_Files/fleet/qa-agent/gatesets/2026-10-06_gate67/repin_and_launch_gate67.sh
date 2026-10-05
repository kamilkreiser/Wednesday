#!/bin/bash
# repin_and_launch_gate67.sh — the LAUNCH ACTION for gate67 (#1394, KS-723, T1). Adapted from repin_and_launch_gate65.sh. Inputs PR + HEAD
# must equal the kit's; --merge-seat names the LATER B seat that will merge (never 64th, the wrapping author, nor 63rd). It READS
# everything at launch and never trusts a pin it did not just re-read (Kam 2026-09-18: re-pin and launch are ONE action):
#   (R)  render prompt_gate67.txt -> prompt_gate67.rendered.txt with {{MERGE_SEAT}} = --merge-seat — rc 9 on a bad / forbidden seat;
#   (0)  the pane QA/Secuura-ks723-1394 is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead);
#   (1)  gh_gate67.py api + census: rc 3 on an API failure or a BLIND control, rc 15 on an OVERLAP;
#   (2)  ONE `git ls-remote` from the Secuura checkout (read verb; the checkout's own core.sshCommand) — rc 2;
#   (3)  rc 11 unless input == kit head == API head == pull/head == branch, the PR open, not merged, based on develop. A moved HEAD is NEVER
#        re-pinnable here (RE-DRAFT, README section 8);
#   (3b) develop: unmoved since drafting -> on. MOVED -> prints the advance (local objects, else a read-only GitHub compare GET) and the
#        MERGE-IN REQUIREMENT, then REFUSES rc 10 unless `--repin-develop <that exact 40-hex>`. Hard rc 10 (not re-pinnable): develop does
#        not descend from the kit develop, or the advance touches a CODE path or a hook path;
#   (3c) c1_pin_gate67.py --no-remote at the head (develop = origin develop if the checkout holds it, else the base, named) — rc 13;
#   (4)  G67_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's own --check — rc 13;
#   (7)  cockpit.sh add <pane> <launcher> — rc 14, then a pane census. Rung 5 is Wednesday's (README section 7).
# --dry-run: R, 0-3c and the launcher's --check, then stops. Output goes to launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*) beside this script.
# Controls-only overrides: G67_ROUTING (routing file stand-in), G67_LSFILE (ls-remote stand-in; DRY RUN ONLY).
# Usage: repin_and_launch_gate67.sh <PR> <HEAD 40-hex> --merge-seat <NNth> [--dry-run] [--repin-develop <40-hex>]   (under `script -q /dev/null`)
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))[sys.argv[2]]; print(" ".join(v) if isinstance(v,list) else v)' "$GS/kit.json" "$1"; }
ROUTING="${G67_ROUTING:-$(KJ routing)}"; KDEV="$(KJ develop_at_draft)"; KBASE="$(KJ base)"; KHEAD="$(KJ head)"; KBR="$(KJ branch)"; KPR="$(KJ pr)"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"
L="$GS/$(KJ launcher)"
USAGE="usage: repin_and_launch_gate67.sh <PR> <HEAD 40-hex> --merge-seat <NNth> [--dry-run] [--repin-develop <40-hex>]"
PR="${1:-}"; HEAD="${2:-}"; DRY=0; REPIN=""; SEAT=""
shift 2 2>/dev/null
while [ $# -gt 0 ]; do
  case "$1" in --dry-run) DRY=1; shift;; --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;; --merge-seat) SEAT="${2:-}"; shift 2 2>/dev/null || shift;; *) echo "$USAGE"; exit 9;; esac
done
case "$PR" in ''|*[!0-9]*) echo "$USAGE"; exit 9;; esac
printf '%s' "$HEAD" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: HEAD must be the FULL 40-hex sha, got '$HEAD'"; exit 9; }
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
printf '%s' "$SEAT" | grep -qE '^[0-9]+(st|nd|rd|th)$' || { echo "REFUSING: --merge-seat must be an ordinal like 65th, got '$SEAT'"; exit 9; }
case "$SEAT" in 64th|63rd) echo "REFUSING: --merge-seat $SEAT is forbidden (Seat B 64th is the wrapping author; 63rd is retired)"; exit 9;; esac
[ "$PR" = "$KPR" ] || { echo "REFUSING: PR #$PR is not this kit's PR (#$KPR)"; exit 9; }
[ "$HEAD" = "$KHEAD" ] || { echo "REFUSING: HEAD $HEAD is not this kit's head $KHEAD — a new head is a RE-DRAFT (README section 8)"; exit 11; }
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate67$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | PR #$PR | HEAD $HEAD | merger Seat B $SEAT | kit develop $KDEV | repin-develop ${REPIN:-none} | pane $PANE"

echo "--- R. render the prompt for Seat B $SEAT"
python3 - "$GS/prompt_gate67.txt" "$GS/prompt_gate67.rendered.txt" "$SEAT" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import sys
src, dst, seat = sys.argv[1:4]
t = open(src, encoding='utf-8').read()
n = t.count('{{MERGE_SEAT}}')
if n < 3: raise SystemExit('template carries {{MERGE_SEAT}} %d time(s), want >= 3' % n)
open(dst, 'w', encoding='utf-8').write(t.replace('{{MERGE_SEAT}}', seat))
print('  rendered %d token(s) -> %s (GO (Seat B %s): merge 1394 on gate67)' % (n, dst, seat))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; README section 4)"; else echo "REFUSING: add the routing line first (README section 4): $LINE"; exit 1; fi
fi

echo "--- 1. PULLS API + census"
python3 "$GS/gh_gate67.py" api > "$OUTP.api.out" 2> "$OUTP.api.err"; arc=$?
python3 "$GS/gh_gate67.py" census > "$OUTP.census.out" 2> "$OUTP.census.err"; rc=$?
sed 's/^/    /' "$OUTP.api.out" "$OUTP.census.out" | cut -c1-240; cat "$OUTP.api.err" "$OUTP.census.err" | sed 's/^/    stderr: /'
echo "  api rc=$arc census rc=$rc"
[ "$arc" -eq 3 ] || [ "$rc" -eq 3 ] && { echo "REFUSING: API failure or a BLIND census control"; exit 3; }
[ "$rc" -eq 1 ] && { echo "REFUSING: an OVERLAP on a kit code path (or a KS-723 title) — read it first"; exit 15; }
A_LINE="$(grep '^API #' "$OUTP.api.out")"
A_HEAD="$(printf '%s' "$A_LINE" | awk '{print $4}')"; A_BR="$(printf '%s' "$A_LINE" | awk '{print $6}')"; A_BASE="$(printf '%s' "$A_LINE" | awk '{print $8}')"
A_STATE="$(printf '%s' "$A_LINE" | awk '{print $10}')"; A_MERGED="$(printf '%s' "$A_LINE" | awk '{print $12}')"

echo "--- 2. ONE ls-remote (read verb) from the checkout"
if [ -n "${G67_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G67_LSFILE is a dry-run control only"; exit 16; }
  cp "$G67_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G67_LSFILE)"
else
  git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/heads/$KBR" "refs/pull/$PR/head" > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"; PH="$(awk -v r="refs/pull/$PR/head" '$2==r{print $1}' "$OUTP.lsremote.out")"; BH="$(awk -v r="refs/heads/$KBR" '$2==r{print $1}' "$OUTP.lsremote.out")"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV | pull/head $PH | branch $BH"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }

echo "--- 3. the head: input == kit == API == pull/head == branch; open, not merged, on develop"
echo "  input $HEAD | kit $KHEAD | API $A_HEAD ($A_STATE, merged $A_MERGED, base $A_BASE, branch $A_BR) | pull/head $PH | branch $BH"
if [ "$HEAD" = "$KHEAD" ] && [ "$A_HEAD" = "$HEAD" ] && [ "$PH" = "$HEAD" ] && [ "$BH" = "$HEAD" ] && [ "$A_STATE" = "open" ] && [ "$A_MERGED" = "False" ] && [ "$A_BASE" = "develop" ] && [ "$A_BR" = "$KBR" ]; then
  echo "  BOTH INSTRUMENTS AGREE with the input head."
else echo "REFUSING TO LAUNCH: the head is not the kit head on both instruments, or the PR is not open / is merged / is off develop. A new head is a RE-DRAFT (README section 8)"; exit 11; fi

echo "--- 3b. develop: origin $CUR_DEV | kit (at drafting) $KDEV"
if [ "$CUR_DEV" = "$KDEV" ]; then
  echo "  UNMOVED since drafting. The head's parent is $KBASE, NOT develop: the merge needs the docs-only merge-in (README section 6);"
  echo "  KEY-ANCHORED predicted tree on this develop: $(KJ merge_in_predicted_tree) (git merge-tree DIVERGES: both docs conflict — Wednesday's ruling, README D2)"
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else
  echo "  DEVELOP MOVED: $KDEV -> $CUR_DEV  (if #1385 / gate66 merged first, THIS is that move: every kit prediction is VOID)"
  python3 - "$GS" "$CHECKOUT" "$KDEV" "$CUR_DEV" > "$OUTP.advance.out" 2> "$OUTP.advance.err" <<'PYEOF'
import os, subprocess, sys
gs, co, kd, nd = sys.argv[1:5]
sys.path.insert(0, gs)
from lib_gate67 import K, gh_get
local = all(subprocess.run(['git', '-C', co, 'cat-file', '-t', x], capture_output=True).returncode == 0 for x in (kd, nd))
if local:
    anc = subprocess.run(['git', '-C', co, 'merge-base', '--is-ancestor', kd, nd]).returncode == 0
    files = [f for f in subprocess.run(['git', '-C', co, 'diff', '--name-only', kd, nd], capture_output=True, text=True).stdout.split('\n') if f]
    src = 'local objects (read verbs)'; status = 'ahead' if anc else 'NOT-A-DESCENDANT'
else:
    c = gh_get('compare/%s...%s' % (kd, nd)); status = c['status']; anc = status in ('ahead', 'identical')
    files = [f['filename'] for f in c.get('files', [])]; src = 'GitHub compare GET (ahead_by %s, behind_by %s)' % (c.get('ahead_by'), c.get('behind_by'))
hit = sorted(set(files) & (set(K['code_paths']) | set(K['hook_blobs'])))
print('SOURCE %s' % src); print('STATUS %s' % status)
print('ADVANCE %d path(s); docs among them %s' % (len(files), sorted(os.path.basename(x)[:28] for x in set(files) & {K['flow'], K['cheat']})))
print('KITHIT %s' % (hit or 'none'))
for f in files[:40]: print('  path %s' % f)
raise SystemExit(0 if anc and not hit else 10)
PYEOF
  arc=$?
  sed 's/^/    /' "$OUTP.advance.out" | cut -c1-200; [ -s "$OUTP.advance.err" ] && sed 's/^/    stderr: /' "$OUTP.advance.err" | tail -3
  if [ "$arc" -ne 0 ]; then
    echo "REFUSING TO LAUNCH (NOT re-pinnable): develop does not descend from the kit develop, the advance touches a CODE / hook path, or it could not be read (rc $arc). RE-GATE / RE-DRAFT: README section 8"; exit 10
  fi
  echo "  MERGE-IN REQUIREMENT: the head a94ec8f6a2c6 stays the gated head. Before the merge, Seat B $SEAT merges develop $CUR_DEV IN (a merge"
  echo "    commit M, never a rebase, never a force push). M is covered by gate67 ONLY if \`c4_docs_gate67.py qm --repo <own clone> --merge-in-head M"
  echo "    --develop-after $CUR_DEV\` passes M1-M8 (KEY-ANCHORED: flow 16. before develop's 18. with 14. below it; cheat KS-723 LAST)."
  echo "    The kit has NO prediction on this develop: \`c4_docs_gate67.py predict / mergetree --repo <own clone> --develop-after $CUR_DEV\`"
  echo "    (both refuse 'develop unresolvable' BY NAME until that develop is fetched into the clone)."
  if [ -z "$REPIN" ]; then
    echo "REFUSING TO LAUNCH: develop moved. To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then
    echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin) — re-read and re-run"; exit 10
  fi
  { echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $KDEV -> $CUR_DEV (told to re-pin by --repin-develop)"; cat "$OUTP.advance.out"; } > "$OUTP.repin.txt"
  echo "  RE-PINNED develop -> $CUR_DEV (recorded: $OUTP.repin.txt). The gate reads develop itself at start / mid / end and predicts on the develop it reads."
fi

echo "--- 3c. the kit's read-only C1 instrument at the head (P2-P11; origin was read in step 2)"
if git -C "$CHECKOUT" cat-file -t "$CUR_DEV" > /dev/null 2>&1; then C1DEV="$CUR_DEV"; C1NOTE="origin develop (in the checkout)"; else C1DEV="$KBASE"; C1NOTE="the BASE (origin develop $CUR_DEV is not in the checkout; P11 against develop is the gate's, in its own clone)"; fi
echo "  c1 develop = $C1DEV — $C1NOTE"
python3 "$GS/c1_pin_gate67.py" --repo "$CHECKOUT" --head "$HEAD" --develop "$C1DEV" --no-remote > "$OUTP.c1.out" 2> "$OUTP.c1.err"; rc=$?
echo "  c1 rc=$rc | $(grep '^CHECKED' "$OUTP.c1.out") | $(grep -E '^[0-9]+ FAIL' "$OUTP.c1.out")"; grep -E '^(FAIL|C1 REFUSED)' "$OUTP.c1.out" | sed 's/^/    /' | cut -c1-240; [ -s "$OUTP.c1.err" ] && sed 's/^/    stderr: /' "$OUTP.c1.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the C1 instrument FAILED at the head (or could not read it)"; exit 13; }

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — develop $CUR_DEV; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G67_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G67_* override is set"; exit 16; }
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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') PR #$PR at $HEAD; merger Seat B $SEAT; develop at launch $CUR_DEV — now verify RUNG 5 (README section 7)"
