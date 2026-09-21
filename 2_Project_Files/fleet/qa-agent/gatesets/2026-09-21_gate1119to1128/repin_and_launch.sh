#!/bin/bash
# repin_and_launch.sh — the LAUNCH ACTION for the #1119-#1128 batch gate (tier-1 floor). The re-pin and the launch are ONE action (Kam 2026-09-18:
# a stale pin costs a whole gate session). Order: (1) origin develop + the ten branches + the ten refs/pull/N/head by `git ls-remote` READ from
# the Secuura checkout; (2) the ten PR heads re-read from the GitHub PULLS API (a second, independent instrument); (3) refuse rc 10 unless
# develop is still 7be81d5c9, rc 11 unless every head equals its pin and is open; (4) usage gate; (5) the launcher's own --check; (6) cockpit.sh
# add — the fleet's own tooling, never raw tmux send-keys.
# READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed, anchored or commented.
# Derived from gatesets/2026-09-21_gate1112to1118/repin_and_launch.sh (data changed: ten PRs, ten heads, develop 7be81d5c9, the pane name
# QA/Secuura-batch1119 — registered in fleet/inbox_routing.conf as `QA/Secuura-batch1119|coagent@agentmail.to|yes` (the drafter READ that line
# present at 02:3x AEST; it did not write it); a cockpit pane that is not routed cannot be tapped). Wednesday runs this; the drafter did NOT.
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1119to1128'
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1119-1128.sh'
DEV=7be81d5c9b109959b559e03652fb092c12de58e8   # the pin: origin develop = every head's parent (Seat B 12th's final state; no move since)
ALLDEV=23d60cace7c37bc329ccc425e58659e950089a4d  # all ten over $DEV (predict_batch_scratch.out + generator tree-hash = the seat's octopus tree)
PANE='QA/Secuura-batch1119'
PRS="1119:e9e20196f2a91ca57ec6bc6d24087843e2611a08 1120:2a66cd17ec3bd5d91e2fc72c7e3f9102ce1eb839 1121:939de1ba519629cacd22031cbc42dbbb765b4040 1122:9aa5442aeef4d07a3d39e3c3e73e65ef9a42a350 1123:c346999ad3956c02e56fca61f9ad30396ceee2ff 1124:bd907c5538286ee9333e2182d7b388c1007b7163 1125:c50c0a8d402cb6fc585b889c528802fba74c0e40 1126:b23ad259a880ecb207b2ab3cf7e9a1b0b8368dad 1127:f0cc0aadc1a7856f76cbb69e925e23b94dd05a40 1128:e35b5ddc27dffca5ad1a7cea17b4433484d460ac"
echo "LAUNCH ACTION $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ')"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -F "$PANE|coagent@agentmail.to|yes" /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf > "$GS/routing_launch.out" 2>&1
rc=$?
echo "routing line present: $(cat "$GS/routing_launch.out") (grep rc=$rc; want 1 / rc 0; control: QA/Secuura-batch1112 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1112|coagent@agentmail.to|yes' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf))"
[ "$rc" -eq 0 ] || { echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (see README_FOR_WEDNESDAY.md)"; exit 1; }

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' ls-remote origin \
  refs/heads/develop refs/pull/1119/head refs/pull/1120/head refs/pull/1121/head refs/pull/1122/head refs/pull/1123/head refs/pull/1124/head refs/pull/1125/head refs/pull/1126/head refs/pull/1127/head refs/pull/1128/head \
  'refs/heads/feature/ks-753-*' 'refs/heads/feature/ks-1232-*' 'refs/heads/feature/ks-957-*' 'refs/heads/feature/ks-1273-*' 'refs/heads/feature/ks-1275-*' 'refs/heads/feature/ks-880-*' 'refs/heads/feature/ks-1223-*' 'refs/heads/feature/ks-1283-*' 'refs/heads/feature/ks-1244-*' 'refs/heads/feature/ks-1234-*' \
  > "$GS/lsremote_launch.out" 2>&1
rc=$?
echo "ls-remote rc=$rc"
cat "$GS/lsremote_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$GS/lsremote_launch.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of each head)"
python3 - > "$GS/api_heads_launch.out" 2>&1 <<'PY'
import json, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
for n in (1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1128):
    p = get('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/%d' % n)
    print('API #%d head %s base %s (base sha %s) state %s' % (n, p['head']['sha'], p['base']['ref'], p['base']['sha'], p['state']))
PY
rc=$?
echo "pulls API rc=$rc"
cat "$GS/api_heads_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the pulls API read failed"; exit 3; }

echo "--- 3. the pins, judged"
echo "  develop   ls-remote $CUR_DEV | pinned $DEV (all-ten tree over the pin $ALLDEV) | $([ "$CUR_DEV" = "$DEV" ] && echo UNMOVED || echo MOVED)"
[ "$CUR_DEV" = "$DEV" ] || { echo "REFUSING TO LAUNCH: origin develop has MOVED off $DEV to $CUR_DEV — every per-PR tree (= head tree today) and the all-ten tree $ALLDEV are unverified at the new base. Re-pin deliberately (gen_launcher_1119.py DEV + the prompt + this DEV)."; exit 10; }
bad=0
for pr in $PRS; do
  n="${pr%%:*}"; h="${pr##*:}"
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
