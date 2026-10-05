#!/bin/bash
# repin_and_launch_gate68.sh — the LAUNCH ACTION for gate68 (#1393 ROUND 2, KS-1278, T1). Adapted from repin_and_launch_gate67.sh.
# THE HEAD IS A PARAMETER. It READS everything at launch and never trusts a pin it did not just re-read (Kam 2026-09-18):
#   (A)  --addendum <file> must exist and name <HEAD> in full (the author's "READY ADDENDUM … new head" mail)            — rc 18
#        <HEAD> must equal kit.json head_expected (b5adaba751d8) unless --accept-unexpected-head (then every drafter figure is VOID) — rc 11
#   (R)  render prompt_gate68.txt -> prompt_gate68.rendered.txt ({{MERGE_SEAT}}, {{HEAD}}) + head_at_launch.txt              — rc 9
#        --merge-seat must be an ordinal and never 63rd / 64th / 65th (65th is the author, wrapping cold)
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead)
#   (1)  gh_gate68.py api (at <HEAD>) + census: rc 3 API failure / blind control, rc 15 OVERLAP
#   (2)  ONE `git ls-remote` from the Secuura checkout (read verb) — rc 2
#   (3)  rc 11 unless input == addendum == API head == pull/head == branch, open, not merged, base develop
#   (3b) develop: == kit develop_at_draft (3f9ff4e1e1b9) -> on; MOVED -> printed advance + MERGE-IN REQUIREMENT, rc 10 unless
#        `--repin-develop <that exact 40-hex>`; hard rc 10 if it does not descend from the kit develop or touches a code / hook path
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, `clone --shared` of the checkout, origin + core.sshCommand copied, NEVER an exported
#        GIT_SSH_COMMAND): fetch <HEAD> and develop BY SHA if absent; c1 at <HEAD> (rc 13); c4 predict (both cheat-anchor rules) +
#        mergetree on (<HEAD>, develop) — the merge-in prediction RECOMPUTED for the head actually launched (printed, never refused)
#   (4)  G68_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's --check — rc 13;  (7) cockpit add — rc 14
# --dry-run: A, R, 0-3c and the launcher's --check, then stops. Output goes to launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*) beside this script.
# Controls-only overrides: G68_ROUTING (routing stand-in), G68_LSFILE (ls-remote stand-in; DRY RUN ONLY).
# Usage: repin_and_launch_gate68.sh <PR> <HEAD 40-hex> --merge-seat <NNth> --addendum <file> [--dry-run] [--repin-develop <40-hex>]
#        [--accept-unexpected-head]      (run under `script -q /dev/null`)
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))[sys.argv[2]]; print(" ".join(v) if isinstance(v,list) else v)' "$GS/kit.json" "$1"; }
ROUTING="${G68_ROUTING:-$(KJ routing)}"; KDEV="$(KJ develop_at_draft)"; KBASE="$(KJ branch_base)"; KEXP="$(KJ head_expected)"; KBR="$(KJ branch)"; KPR="$(KJ pr)"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"
L="$GS/$(KJ launcher)"; CL="$GS/_scratch/clone"
USAGE="usage: repin_and_launch_gate68.sh <PR> <HEAD 40-hex> --merge-seat <NNth> --addendum <file> [--dry-run] [--repin-develop <40-hex>] [--accept-unexpected-head]"
PR="${1:-}"; HEAD="${2:-}"; DRY=0; REPIN=""; SEAT=""; ADD=""; ACCEPT=0
shift 2 2>/dev/null
while [ $# -gt 0 ]; do
  case "$1" in --dry-run) DRY=1; shift;; --accept-unexpected-head) ACCEPT=1; shift;; --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;;
    --merge-seat) SEAT="${2:-}"; shift 2 2>/dev/null || shift;; --addendum) ADD="${2:-}"; shift 2 2>/dev/null || shift;; *) echo "$USAGE"; exit 9;; esac
done
case "$PR" in ''|*[!0-9]*) echo "$USAGE"; exit 9;; esac
[ "$PR" = "$KPR" ] || { echo "REFUSING: PR #$PR is not this kit's PR (#$KPR)"; exit 9; }
printf '%s' "$HEAD" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: HEAD must be the FULL 40-hex sha, got '$HEAD'"; exit 9; }
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
printf '%s' "$SEAT" | grep -qE '^[0-9]+(st|nd|rd|th)$' || { echo "REFUSING: --merge-seat must be an ordinal like 66th, got '$SEAT'"; exit 9; }
case "$SEAT" in 63rd|64th|65th) echo "REFUSING: --merge-seat $SEAT is forbidden (63rd / 64th retired; 65th is the author, wrapping cold)"; exit 9;; esac
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate68$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | PR #$PR | HEAD $HEAD | merger Seat B $SEAT | kit expected head $KEXP | kit develop $KDEV | repin-develop ${REPIN:-none} | pane $PANE"

echo "--- A. the head must be the one the author's addendum names"
[ -n "$ADD" ] && [ -s "$ADD" ] || { echo "REFUSING: --addendum <file> missing or empty ('$ADD')"; exit 18; }
_n="$(/usr/bin/grep -c -F "$HEAD" "$ADD")"; _ctl="$(/usr/bin/grep -c -i 'ADDENDUM' "$ADD")"
echo "  $ADD (sha256/16 $(shasum -a 256 "$ADD" | cut -c1-16)): lines naming $HEAD in full = $_n | CONTROL lines naming 'ADDENDUM' = $_ctl"
[ "$_n" -ge 1 ] || { echo "REFUSING: the addendum does not name $HEAD in full"; exit 18; }
if [ "$HEAD" != "$KEXP" ]; then
  if [ "$ACCEPT" = 1 ]; then echo "  WARNING: HEAD != kit head_expected $KEXP — accepted by --accept-unexpected-head: EVERY drafter figure is VOID; the gate re-derives all"
  else echo "REFUSING: HEAD $HEAD != kit head_expected $KEXP (the drafter's figures are for $KEXP). Re-draft, or pass --accept-unexpected-head"; exit 11; fi
fi

echo "--- R. render the prompt (Seat B $SEAT, head $HEAD)"
python3 - "$GS/prompt_gate68.txt" "$GS/prompt_gate68.rendered.txt" "$SEAT" "$HEAD" "$GS/head_at_launch.txt" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import sys
src, dst, seat, head, hf = sys.argv[1:6]
t = open(src, encoding='utf-8').read()
n, h = t.count('{{MERGE_SEAT}}'), t.count('{{HEAD}}')
if n < 3 or h < 10: raise SystemExit('template carries {{MERGE_SEAT}} x%d (want >= 3), {{HEAD}} x%d (want >= 10)' % (n, h))
open(dst, 'w', encoding='utf-8').write(t.replace('{{MERGE_SEAT}}', seat).replace('{{HEAD}}', head))
open(hf, 'w').write(head + '\n')
print('  rendered {{MERGE_SEAT}} x%d, {{HEAD}} x%d -> %s ; head file %s (GO (Seat B %s): merge 1393 on gate68)' % (n, h, dst, hf, seat))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_LINE.txt)"; else echo "REFUSING: add the routing line first (ROUTING_LINE.txt): $LINE"; exit 1; fi
fi

echo "--- 1. PULLS API (at the head) + census"
G68_HEAD="$HEAD" python3 "$GS/gh_gate68.py" api --head "$HEAD" > "$OUTP.api.out" 2> "$OUTP.api.err"; arc=$?
python3 "$GS/gh_gate68.py" census > "$OUTP.census.out" 2> "$OUTP.census.err"; rc=$?
sed 's/^/    /' "$OUTP.api.out" "$OUTP.census.out" | cut -c1-240; cat "$OUTP.api.err" "$OUTP.census.err" | sed 's/^/    stderr: /'
echo "  api rc=$arc census rc=$rc"
[ "$arc" -eq 3 ] || [ "$rc" -eq 3 ] && { echo "REFUSING: API failure or a BLIND census control"; exit 3; }
[ "$rc" -eq 1 ] && { echo "REFUSING: an OVERLAP on a kit code path (or a KS-1278 title) — read it first"; exit 15; }
A_LINE="$(grep '^API #' "$OUTP.api.out")"
A_HEAD="$(printf '%s' "$A_LINE" | awk '{print $4}')"; A_BR="$(printf '%s' "$A_LINE" | awk '{print $6}')"; A_BASE="$(printf '%s' "$A_LINE" | awk '{print $8}')"
A_STATE="$(printf '%s' "$A_LINE" | awk '{print $10}')"; A_MERGED="$(printf '%s' "$A_LINE" | awk '{print $12}')"

echo "--- 2. ONE ls-remote (read verb) from the checkout"
if [ -n "${G68_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G68_LSFILE is a dry-run control only"; exit 16; }
  cp "$G68_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G68_LSFILE)"
else
  git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/heads/$KBR" "refs/pull/$PR/head" > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"; PH="$(awk -v r="refs/pull/$PR/head" '$2==r{print $1}' "$OUTP.lsremote.out")"; BH="$(awk -v r="refs/heads/$KBR" '$2==r{print $1}' "$OUTP.lsremote.out")"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV | pull/head $PH | branch $BH"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }

echo "--- 3. the head: input == addendum == API == pull/head == branch; open, not merged, on develop"
echo "  input $HEAD | API $A_HEAD ($A_STATE, merged $A_MERGED, base $A_BASE, branch $A_BR) | pull/head $PH | branch $BH"
if [ "$A_HEAD" = "$HEAD" ] && [ "$PH" = "$HEAD" ] && [ "$BH" = "$HEAD" ] && [ "$A_STATE" = "open" ] && [ "$A_MERGED" = "False" ] && [ "$A_BASE" = "develop" ] && [ "$A_BR" = "$KBR" ]; then
  echo "  ALL INSTRUMENTS AGREE with the input head (named by the addendum)."
else echo "REFUSING TO LAUNCH: the head is not the input head on every instrument, or the PR is not open / is merged / is off develop"; exit 11; fi

echo "--- 3b. develop: origin $CUR_DEV | kit (at drafting) $KDEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$KDEV" ]; then
  echo "  UNMOVED since drafting. The head's chain starts at $KBASE, NOT develop: the merge needs the docs-only merge-in (Q-M)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else
  DEV_MOVED=1; echo "  DEVELOP MOVED: $KDEV -> $CUR_DEV  (every kit prediction is VOID; step 3c recomputes)"
fi

echo "--- 3c. the kit's own clone: fetch by sha, C1 at the head, the merge-in prediction RECOMPUTED for (head, develop)"
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
  git -C "$CL" config remote.origin.url "$(git -C "$CHECKOUT" config --get remote.origin.url)"
  git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
fi
[ -z "${GIT_SSH_COMMAND:-}" ] || { echo "REFUSING: GIT_SSH_COMMAND is exported in this shell (never export it; the clone carries core.sshCommand)"; exit 16; }
for s in "$HEAD" "$CUR_DEV" "$KDEV"; do
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || git -C "$CL" fetch --quiet origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err" || { echo "REFUSING: fetch by sha $s into the kit clone failed"; sed 's/^/    /' "$OUTP.fetch.err" | tail -3; exit 13; }
done
echo "  kit clone $CL holds head $(git -C "$CL" cat-file -t "$HEAD") / develop $(git -C "$CL" cat-file -t "$CUR_DEV")"
if [ "$DEV_MOVED" = 1 ]; then
  python3 - "$GS" "$CL" "$KDEV" "$CUR_DEV" > "$OUTP.advance.out" 2> "$OUTP.advance.err" <<'PYEOF'
import os, subprocess, sys
gs, cl, kd, nd = sys.argv[1:5]
sys.path.insert(0, gs)
from lib_gate68 import K
anc = subprocess.run(['git', '-C', cl, 'merge-base', '--is-ancestor', kd, nd]).returncode == 0
files = [f for f in subprocess.run(['git', '-C', cl, 'diff', '--name-only', kd, nd], capture_output=True, text=True).stdout.split('\n') if f]
hit = sorted(set(files) & (set(K['code_paths']) | set(K['hook_blobs'])))
print('STATUS %s' % ('ahead' if anc else 'NOT-A-DESCENDANT')); print('ADVANCE %d path(s); docs among them %s' % (len(files), sorted(os.path.basename(x)[:28] for x in set(files) & {K['flow'], K['cheat']})))
print('KITHIT %s' % (hit or 'none'))
for f in files[:40]: print('  path %s' % f)
raise SystemExit(0 if anc and not hit else 10)
PYEOF
  arc=$?; sed 's/^/    /' "$OUTP.advance.out" | cut -c1-200; [ -s "$OUTP.advance.err" ] && sed 's/^/    stderr: /' "$OUTP.advance.err" | tail -3
  [ "$arc" -eq 0 ] || { echo "REFUSING TO LAUNCH (NOT re-pinnable): develop does not descend from the kit develop or touches a CODE / hook path (rc $arc)"; exit 10; }
fi
G68_HEAD="$HEAD" python3 "$GS/c1_pin_gate68.py" --repo "$CL" --head "$HEAD" --develop "$CUR_DEV" --no-remote > "$OUTP.c1.out" 2> "$OUTP.c1.err"; rc=$?
echo "  c1 rc=$rc | $(grep '^CHECKED' "$OUTP.c1.out") | $(grep -E '^[0-9]+ FAIL' "$OUTP.c1.out")"; grep -E '^(FAIL|C1 REFUSED)' "$OUTP.c1.out" | sed 's/^/    /' | cut -c1-240; [ -s "$OUTP.c1.err" ] && sed 's/^/    stderr: /' "$OUTP.c1.err"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the C1 instrument FAILED at the head (or could not read it)"; exit 13; }
for anc in last after-pred; do
  G68_SCRATCH="$GS/_scratch/kitout" python3 "$GS/c4_docs_gate68.py" predict --repo "$CL" --head "$HEAD" --develop-after "$CUR_DEV" --cheat-anchor "$anc" > "$OUTP.predict_$anc.out" 2> "$OUTP.predict_$anc.err"; prc=$?
  echo "  PREDICTED (cheat anchor $anc) $(awk '/^PREDICTED/{print $2}' "$OUTP.predict_$anc.out") rc=$prc"; grep -E 'READ-BACK' "$OUTP.predict_$anc.out" | sed 's/^/    /' | cut -c1-200
done
G68_SCRATCH="$GS/_scratch/kitout" python3 "$GS/c4_docs_gate68.py" mergetree --repo "$CL" --head "$HEAD" --develop-after "$CUR_DEV" > "$OUTP.mergetree.out" 2> "$OUTP.mergetree.err"
echo "  $(grep -E '^(AGREE|DIVERGENCE)' "$OUTP.mergetree.out" | cut -c1-200)"; grep -E 'conflicted paths|merge-tree flow blob' "$OUTP.mergetree.out" | sed 's/^/    /' | cut -c1-200
if [ "$DEV_MOVED" = 1 ]; then
  echo "  MERGE-IN REQUIREMENT: the merger merges develop $CUR_DEV IN (a merge commit M, never a rebase / force push); covered by gate68 ONLY if"
  echo "    \`c4_docs_gate68.py qm --repo <own clone> --head $HEAD --merge-in-head M --develop-after $CUR_DEV\` passes M1-M8."
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved. To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  { echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $KDEV -> $CUR_DEV"; cat "$OUTP.advance.out"; } > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — head $HEAD, develop $CUR_DEV; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G68_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G68_* override is set"; exit 16; }
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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') PR #$PR at $HEAD; merger Seat B $SEAT; develop at launch $CUR_DEV — now verify RUNG 5 (README §7)"
