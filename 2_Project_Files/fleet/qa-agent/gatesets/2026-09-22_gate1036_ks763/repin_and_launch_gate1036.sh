#!/bin/bash
# repin_and_launch_gate1036.sh — the LAUNCH ACTION for the #1036 (KS-763 PR-4, qs in range) TIER 1 gate. The re-pin and the launch are ONE action
# (Kam 2026-09-18: a stale pin costs a whole gate session). Order: (0) the pane is routed; (1) origin develop + the branch + refs/pull/1036/head by
# `git ls-remote` READ from the Secuura checkout; (2) the head re-read from the GitHub PULLS API (a second, independent instrument); (3) refuse rc 11
# unless the head equals the launcher's pin and the PR is open; develop MOVING is NOT a refusal here — the launcher judges develop by CONTENT (the 50
# PR paths at their merge-base blobs) and the prompt tells the gate to re-predict the merged tree over the tip it reads (BASE_GO) — it is PRINTED;
# (4) usage gate; (5) the launcher's own --check (exit 18/19 there is the develop refusal); (6) cockpit.sh add — the fleet's own tooling, never raw
# tmux send-keys. READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed, anchored or commented.
# The PINS below are READ from the launcher itself (HEAD_SHA default, DEVELOP_SHA, MERGED_TREE) so this file never carries a second copy that could drift.
# Derived from gatesets/2026-09-22_gate16C_seatC/repin_and_launch_gate16C.sh. Wednesday runs this; the drafter did NOT.
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate1036_ks763'
L="${1:-}"
[ -n "$L" ] && [ -x "$L" ] || { echo "usage: repin_and_launch_gate1036.sh <launcher path> — e.g. /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks763_1036.sh"; exit 9; }
PROMPT="$(sed -n 's/^PROMPT_FILE="\${QA1036_PROMPT:-\(.*\)}"$/\1/p' "$L")"
[ -s "$PROMPT" ] || { echo "REFUSING: could not read the prompt path from $L (got '$PROMPT')"; exit 9; }
/usr/bin/grep -qF 'PENDING' "$PROMPT" && { echo "REFUSING: the launcher's prompt is PARTIAL — re-fill first (README.md section 8)"; exit 8; }
/usr/bin/grep -qiF 'deadbeef' "$PROMPT" && { echo "REFUSING: the launcher's prompt carries a deadbeef literal — re-fill first"; exit 8; }
HEADPIN="$(sed -n 's/^HEAD_SHA="\${QA1036_HEAD:-\([0-9a-f]\{40\}\)}"$/\1/p' "$L")"
DEV="$(sed -n "s/^DEVELOP_SHA='\([0-9a-f]\{40\}\)'.*/\1/p" "$L")"
MERGED="$(sed -n "s/^MERGED_TREE='\([0-9a-f]\{40\}\)'.*/\1/p" "$L")"
BR="$(sed -n "s/^BRANCH='\(refs\/heads\/[^']*\)'.*/\1/p" "$L")"
PANE='QA/Secuura-1036'
[ -n "$HEADPIN" ] && [ -n "$DEV" ] && [ -n "$BR" ] || { echo "REFUSING: could not read the pins from $L"; exit 9; }
echo "LAUNCH ACTION $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | launcher $L | head pin $HEADPIN | develop at generation $DEV (merged tree $MERGED) | branch $BR"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -F "$PANE|coagent@agentmail.to|yes" /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf > "$GS/routing_launch.out" 2>&1
rc=$?
echo "routing line present: $(cat "$GS/routing_launch.out") (grep rc=$rc; want 1 / rc 0; control: QA/Secuura-batch1148 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1148|coagent@agentmail.to|yes' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf))"
[ "$rc" -eq 0 ] || { echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README.md section 3; the drafter did NOT write it)"; exit 1; }

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' ls-remote origin refs/heads/develop refs/pull/1036/head "$BR" > "$GS/lsremote_launch.out" 2>&1
rc=$?
echo "ls-remote rc=$rc"
cat "$GS/lsremote_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$GS/lsremote_launch.out")"
P="$(awk '$2=="refs/pull/1036/head"{print $1}' "$GS/lsremote_launch.out")"
B="$(awk -v b="$BR" '$2==b{print $1}' "$GS/lsremote_launch.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of the head)"
python3 - > "$GS/api_heads_launch.out" 2>&1 <<'PY'
import json, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
p = json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/1036', headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('API #1036 head %s base %s (base sha %s) state %s mergeable_state %s' % (p['head']['sha'], p['base']['ref'], p['base']['sha'], p['state'], p.get('mergeable_state')))
PY
rc=$?
echo "pulls API rc=$rc"
cat "$GS/api_heads_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the pulls API read failed"; exit 3; }
A="$(awk '$1=="API"{print $4}' "$GS/api_heads_launch.out")"
S="$(awk '$1=="API"{for(i=1;i<=NF;i++) if($i=="state") print $(i+1)}' "$GS/api_heads_launch.out")"

echo "--- 3. the pins, judged"
echo "  develop   ls-remote $CUR_DEV | at generation $DEV | $([ "$CUR_DEV" = "$DEV" ] && echo UNMOVED || echo "MOVED — not a refusal: the launcher judges develop by CONTENT and the gate re-predicts the merged tree over $CUR_DEV (BASE_GO); the prompt's merged tree $MERGED is then a prediction over an older tip, which the prompt itself says")"
echo "  #1036     ls-remote pull/head $P | branch $B | API $A (state $S) | pinned $HEADPIN"
[ "$P" = "$HEADPIN" ] && [ "$B" = "$HEADPIN" ] && [ "$A" = "$HEADPIN" ] && [ "$S" = "open" ] || { echo "REFUSING TO LAUNCH: the head moved or the PR is not open — re-draft (a verdict is valid ONLY at its head)"; exit 11; }
echo "  BOTH INSTRUMENTS AGREE with the head pin."

echo "--- 4. usage gate"
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check > "$GS/usage_gate_launch.out" 2>&1
rc=$?
echo "usage_gate rc=$rc"
cat "$GS/usage_gate_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused"; exit 12; }

echo "--- 5. the launcher's own --check (read it before launching; exit 18/19 here = develop moved ON the PR's paths: re-pin, README section 0)"
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
