#!/bin/bash
# repin_and_launch.sh — the LAUNCH ACTION for the #1105 tier-1 gate. The re-pin and the launch are ONE action (Kam 2026-09-18: a stale pin costs
# a whole gate session). Order: (1) origin develop + the branch + refs/pull/1105/head by `git ls-remote` READ from the Secuura checkout; (2) the
# PR head re-read from the GitHub PULLS API (a second, independent instrument); (3) refuse unless develop is still dc061f2bb and the head equals
# the pin; (4) usage gate; (5) the launcher's own --check; (6) cockpit.sh add — the fleet's own tooling, never raw tmux send-keys.
# READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed, anchored or commented.
# Derived from gatesets/2026-09-20_gate1100to1101/repin_and_launch.sh (data changed: one PR, one head, the pane name QA/Secuura-1105 — registered in
# fleet/inbox_routing.conf 2026-09-21 00:24 AEST, backup inbox_routing.conf.pre-0920-0024-qagate1105).
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1105'
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_1105.sh'
DEV=dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa
H1105=e02d3ecb51a457b0eb490db1854f28c6b1af69ad
BR='refs/heads/feature/ks-1175-anchor-originate-lifecycle-event-schemas-accept-and-anchor'
PANE='QA/Secuura-1105'
echo "LAUNCH ACTION $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ')"

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' ls-remote origin \
  refs/heads/develop refs/pull/1105/head "$BR" > "$GS/lsremote_launch.out" 2>&1
rc=$?
echo "ls-remote rc=$rc"
cat "$GS/lsremote_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$GS/lsremote_launch.out")"
P1105="$(awk '$2=="refs/pull/1105/head"{print $1}' "$GS/lsremote_launch.out")"
B1105="$(awk -v b="$BR" '$2==b{print $1}' "$GS/lsremote_launch.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of the head)"
python3 - > "$GS/api_heads_launch.out" 2>&1 <<'PY'
import json, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
p = get('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/1105')
print('API #1105 head %s base %s (base sha %s) state %s' % (p['head']['sha'], p['base']['ref'], p['base']['sha'], p['state']))
PY
rc=$?
echo "pulls API rc=$rc"
cat "$GS/api_heads_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the pulls API read failed"; exit 3; }
A1105="$(awk '/^API #1105 head /{print $4}' "$GS/api_heads_launch.out")"
ASTATE="$(awk '/^API #1105 head /{print $NF}' "$GS/api_heads_launch.out")"

echo "--- 3. the pins, judged"
echo "  develop   ls-remote $CUR_DEV | pinned $DEV | $([ "$CUR_DEV" = "$DEV" ] && echo UNMOVED || echo MOVED)"
echo "  #1105     ls-remote pull/head $P1105 | branch $B1105 | API $A1105 (state $ASTATE) | pinned $H1105"
[ "$CUR_DEV" = "$DEV" ] || { echo "REFUSING TO LAUNCH: origin develop has MOVED off $DEV to $CUR_DEV — the fast-forward claim (merged tree = head tree 8f066a817) is unverified at the new base. Re-pin deliberately."; exit 10; }
[ "$P1105" = "$H1105" ] && [ "$B1105" = "$H1105" ] && [ "$A1105" = "$H1105" ] || { echo "REFUSING TO LAUNCH: #1105's head moved"; exit 11; }
[ "$ASTATE" = "open" ] || { echo "REFUSING TO LAUNCH: #1105 is not open ($ASTATE)"; exit 11; }
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
