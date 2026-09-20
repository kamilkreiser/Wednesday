#!/bin/bash
# repin_and_launch.sh — the LAUNCH ACTION for the #1100 + #1101 batch gate. The re-pin and the launch are ONE action (Kam 2026-09-18: a stale pin
# costs a whole gate session). Order: (1) origin develop + both branches by `git ls-remote` READ from the Secuura checkout; (2) both PR heads re-read
# from the GitHub PULLS API (a second, independent instrument); (3) refuse unless develop is still e47019878 and both heads equal the pins;
# (4) usage gate; (5) the launcher's own --check; (6) cockpit.sh add — the fleet's own tooling, never raw tmux send-keys.
# READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed or commented.
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1100to1101'
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1100_1101.sh'
DEV=e470198783bcb1ef0eac94780f87579974051423
H1100=99ce89e741e6c3cad7457af7c91fb6fea86acdff
H1101=dc40087e756c598ca8b2957da7fbf1ec01945df8
PANE='QA/Secuura-1100'
echo "LAUNCH ACTION $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ')"

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' ls-remote origin \
  refs/heads/develop refs/pull/1100/head refs/pull/1101/head \
  'refs/heads/feature/ks-1230-put-apiadminsettings-stores-a-connectors-n97-1' \
  'refs/heads/feature/ks-1282-get-apiplatformtenants-the-requiresuperadmin-guard-n99-1' > "$GS/lsremote_launch.out" 2>&1
rc=$?
echo "ls-remote rc=$rc"
cat "$GS/lsremote_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$GS/lsremote_launch.out")"
P1100="$(awk '$2=="refs/pull/1100/head"{print $1}' "$GS/lsremote_launch.out")"
P1101="$(awk '$2=="refs/pull/1101/head"{print $1}' "$GS/lsremote_launch.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of both heads)"
python3 - > "$GS/api_heads_launch.out" 2>&1 <<'PY'
import json, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
for n in (1100, 1101):
    p = get('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/%d' % n)
    print('API #%d head %s base %s state %s' % (n, p['head']['sha'], p['base']['ref'], p['state']))
PY
rc=$?
echo "pulls API rc=$rc"
cat "$GS/api_heads_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the pulls API read failed"; exit 3; }
A1100="$(awk '/^API #1100 head /{print $4}' "$GS/api_heads_launch.out")"
A1101="$(awk '/^API #1101 head /{print $4}' "$GS/api_heads_launch.out")"

echo "--- 3. the pins, judged"
echo "  develop   ls-remote $CUR_DEV | pinned $DEV | $([ "$CUR_DEV" = "$DEV" ] && echo UNMOVED || echo MOVED)"
echo "  #1100     ls-remote $P1100 | API $A1100 | pinned $H1100"
echo "  #1101     ls-remote $P1101 | API $A1101 | pinned $H1101"
[ "$CUR_DEV" = "$DEV" ] || { echo "REFUSING TO LAUNCH: origin develop has MOVED off $DEV to $CUR_DEV — the batch tree claim (1ccb80e0d) is unverified at the new base. Re-pin deliberately."; exit 10; }
[ "$P1100" = "$H1100" ] && [ "$A1100" = "$H1100" ] || { echo "REFUSING TO LAUNCH: #1100's head moved"; exit 11; }
[ "$P1101" = "$H1101" ] && [ "$A1101" = "$H1101" ] || { echo "REFUSING TO LAUNCH: #1101's head moved"; exit 11; }
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
