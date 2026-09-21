#!/bin/bash
# repin_and_launch_gate15.sh — the LAUNCH ACTION for the Seat B 15th ten-PR batch gate (tier-2 floor). The re-pin and the launch are ONE action
# (Kam 2026-09-18: a stale pin costs a whole gate session). Order: (0) the pane is routed; (1) origin develop + every branch + every
# refs/pull/N/head by `git ls-remote` READ from the Secuura checkout; (2) every PR head re-read from the GitHub PULLS API (a second, independent
# instrument); (3) refuse rc 10 unless develop is still the launcher's pin (the post-#1138 tip b192ffd4a — a FURTHER move means every merged tree
# must be re-predicted: re-run predict_batch_scratch_gate15.py + gen_launcher_gate15.py), rc 11 unless every head equals its pin and is open;
# (4) usage gate; (5) the launcher's own --check; (6) cockpit.sh add — the fleet's own tooling, never raw tmux send-keys.
# READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed, anchored or commented.
# The PINS below are READ from the launcher itself (its PRS array and DEVELOP_SHA) so this file never carries a second copy that could drift.
# Derived from gatesets/2026-09-21_gate1130to1135/repin_and_launch_1130.sh. Wednesday runs this; the drafter did NOT.
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate15_docs_comments'
L="${1:-}"
[ -n "$L" ] && [ -x "$L" ] || { echo "usage: repin_and_launch_gate15.sh <launcher path> — e.g. /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1136-<last>.sh"; exit 9; }
grep -qF 'PENDING-PR-' "$(sed -n 's/^PROMPT_FILE="\${QAB1136_PROMPT:-\(.*\)}"$/\1/p' "$L")" 2>/dev/null && { echo "REFUSING: the launcher's prompt is PARTIAL — re-fill first (README.md section 8)"; exit 8; }
DEV="$(sed -n "s/^DEVELOP_SHA='\([0-9a-f]\{40\}\)'.*/\1/p" "$L")"
ALLDEV="$(sed -n "s/^ALL_OVER_DEV='\([0-9a-f]\{40\}\)'.*/\1/p" "$L")"
PANE='QA/Secuura-batch1136'
PRS="$(sed -n 's/^  "\([0-9]*\)|[^|]*|\([^|]*\)|\${QAB1136_HEAD_[0-9]*:-\([0-9a-f]\{40\}\)}|.*/\1:\3:\2/p; s/^  "\([0-9]*\)|[^|]*|\([^|]*\)|\([0-9a-f]\{40\}\)|.*/\1:\3:\2/p' "$L")"
[ -n "$DEV" ] && [ -n "$PRS" ] || { echo "REFUSING: could not read the pins from $L"; exit 9; }
echo "LAUNCH ACTION $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | launcher $L | develop pin $DEV | PRs: $(printf '%s\n' "$PRS" | cut -d: -f1 | tr '\n' ' ')"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -F "$PANE|coagent@agentmail.to|yes" /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf > "$GS/routing_launch.out" 2>&1
rc=$?
echo "routing line present: $(cat "$GS/routing_launch.out") (grep rc=$rc; want 1 / rc 0; control: QA/Secuura-batch1130 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1130|coagent@agentmail.to|yes' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf))"
[ "$rc" -eq 0 ] || { echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README.md section 3; the drafter did NOT write it)"; exit 1; }

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
refs="refs/heads/develop"
for pr in $PRS; do n="${pr%%:*}"; rest="${pr#*:}"; br="${rest#*:}"; refs="$refs refs/pull/$n/head $br"; done
# shellcheck disable=SC2086
git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' ls-remote origin $refs > "$GS/lsremote_launch.out" 2>&1
rc=$?
echo "ls-remote rc=$rc"
cat "$GS/lsremote_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$GS/lsremote_launch.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of each head)"
PRS_ENV="$PRS" python3 - > "$GS/api_heads_launch.out" 2>&1 <<'PY'
import json, os, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
for pr in os.environ['PRS_ENV'].split():
    n = int(pr.split(':')[0])
    p = get('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/%d' % n)
    print('API #%d head %s base %s (base sha %s) state %s' % (n, p['head']['sha'], p['base']['ref'], p['base']['sha'], p['state']))
PY
rc=$?
echo "pulls API rc=$rc"
cat "$GS/api_heads_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the pulls API read failed"; exit 3; }

echo "--- 3. the pins, judged"
echo "  develop   ls-remote $CUR_DEV | pinned $DEV (all-ten tree over the pin $ALLDEV) | $([ "$CUR_DEV" = "$DEV" ] && echo UNMOVED || echo MOVED)"
[ "$CUR_DEV" = "$DEV" ] || { echo "REFUSING TO LAUNCH: origin develop has MOVED off $DEV to $CUR_DEV — every per-PR merged tree and the all-ten tree $ALLDEV are unverified at the new base. Re-pin deliberately: python3 $GS/predict_batch_scratch_gate15.py <scratchpad> ; python3 $GS/gen_launcher_gate15.py <launcher> <that scratch clone> ; the prompt's THE SHAPE section."; exit 10; }
bad=0
for pr in $PRS; do
  n="${pr%%:*}"; rest="${pr#*:}"; h="${rest%%:*}"
  P="$(awk -v r="refs/pull/$n/head" '$2==r{print $1}' "$GS/lsremote_launch.out")"
  B="$(awk -v h="$h" '$1==h && $2 ~ /^refs\/heads\/feature\//{print $1}' "$GS/lsremote_launch.out" | head -1)"
  A="$(awk -v n="$n" '$1=="API" && $2=="#"n{print $4}' "$GS/api_heads_launch.out")"
  S="$(awk -v n="$n" '$1=="API" && $2=="#"n{print $NF}' "$GS/api_heads_launch.out")"
  echo "  #$n      ls-remote pull/head $P | branch $B | API $A (state $S) | pinned $h"
  [ "$P" = "$h" ] && [ "$B" = "$h" ] && [ "$A" = "$h" ] && [ "$S" = "open" ] || bad=1
done
[ "$bad" -eq 0 ] || { echo "REFUSING TO LAUNCH: a head moved or a PR is not open"; exit 11; }
echo "  BOTH INSTRUMENTS AGREE with the pins."

echo "--- 4. usage gate"
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check > "$GS/usage_gate_launch.out" 2>&1
rc=$?
echo "usage_gate rc=$rc"
cat "$GS/usage_gate_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused"; exit 12; }

echo "--- 5. the launcher's own --check (read it before launching)"
"$L" --check > "$GS/launcher_check_launch.out" 2>&1
rc=$?
echo "launcher --check rc=$rc"
cat "$GS/launcher_check_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the launcher refused under --check"; exit 13; }

echo "--- 6. launch through the fleet's own tooling (cockpit.sh add), never raw tmux send-keys"
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add "$PANE" "$L" > "$GS/cockpit_add.out" 2>&1
rc=$?
echo "cockpit.sh add rc=$rc"
cat "$GS/cockpit_add.out"
[ "$rc" -eq 0 ] || { echo "LAUNCH FAILED at cockpit.sh add"; exit 14; }
echo "--- pane census"
/opt/homebrew/bin/tmux list-panes -a -F '#{pane_id} | #{@cockpit_name} | #{pane_current_command} | #{session_name}:#{window_index}.#{pane_index}'
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
