#!/bin/bash
# repin_and_launch_1130.sh — the LAUNCH ACTION for the #1130-#1135 batch gate (tier-1 floor). The re-pin and the launch are ONE action (Kam 2026-09-18:
# a stale pin costs a whole gate session). Order: (1) origin develop + the six branches + the six refs/pull/N/head by `git ls-remote` READ from
# the Secuura checkout; (2) the six PR heads re-read from the GitHub PULLS API (a second, independent instrument); (3) refuse rc 10 unless
# develop is still 9f0265eb0, rc 11 unless every head equals its pin and is open; (4) usage gate; (5) the launcher's own --check; (6) cockpit.sh
# add — the fleet's own tooling, never raw tmux send-keys.
# READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed, anchored or commented.
# Derived from gatesets/2026-09-21_gate1119to1128/repin_and_launch.sh (data changed: six PRs, six heads, develop 9f0265eb0, the pane name
# QA/Secuura-batch1130 — registered in fleet/inbox_routing.conf as `QA/Secuura-batch1130|coagent@agentmail.to|yes` by the drafter at 09:45:10Z with
# the backup inbox_routing.conf.pre-batch1130-094510 beside it; a cockpit pane that is not routed cannot be tapped). Wednesday runs this; the drafter did NOT.
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135'
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1130-1135.sh'
DEV=9f0265eb06ecf24d4de18149ce862ad2330a61ee   # the pin: origin develop = every head's parent (Seat B 13th's final state; no move since)
ALLDEV=60bd96e7078c41bbd71b3e0d7e15f815f70b0b1b  # all six over $DEV (predict_batch_scratch_2.out six orders + generator tree-hash = the seat's octopus tree)
PANE='QA/Secuura-batch1130'
PRS="1130:7c3cc821f2fdd63d96e30689cc9477472a843ce0 1131:d897f531876b33c9b4f2e118e3aea08b23e5344d 1132:39bbf29a564fcc6b68ffe50607e29df251b8b180 1133:0fd2a7f0d3990329567e2ae6532babab0f0d250a 1134:d7439346d1c489162584c64937ea91d66cb28984 1135:1c7c01afe589f1ba07e70106dc1cf019dba14a00"
echo "LAUNCH ACTION $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ')"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -F "$PANE|coagent@agentmail.to|yes" /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf > "$GS/routing_launch.out" 2>&1
rc=$?
echo "routing line present: $(cat "$GS/routing_launch.out") (grep rc=$rc; want 1 / rc 0; control: QA/Secuura-batch1119 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1119|coagent@agentmail.to|yes' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf))"
[ "$rc" -eq 0 ] || { echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (see README_FOR_WEDNESDAY.md)"; exit 1; }

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' ls-remote origin \
  refs/heads/develop refs/pull/1130/head refs/pull/1131/head refs/pull/1132/head refs/pull/1133/head refs/pull/1134/head refs/pull/1135/head \
  'refs/heads/feature/ks-1273-*' 'refs/heads/feature/ks-1135-*' 'refs/heads/feature/ks-958-*' 'refs/heads/feature/ks-880-*' 'refs/heads/feature/ks-887-*' 'refs/heads/feature/ks-1236-*' \
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
for n in (1130, 1131, 1132, 1133, 1134, 1135):
    p = get('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/%d' % n)
    print('API #%d head %s base %s (base sha %s) state %s' % (n, p['head']['sha'], p['base']['ref'], p['base']['sha'], p['state']))
PY
rc=$?
echo "pulls API rc=$rc"
cat "$GS/api_heads_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the pulls API read failed"; exit 3; }

echo "--- 3. the pins, judged"
echo "  develop   ls-remote $CUR_DEV | pinned $DEV (all-six tree over the pin $ALLDEV) | $([ "$CUR_DEV" = "$DEV" ] && echo UNMOVED || echo MOVED)"
[ "$CUR_DEV" = "$DEV" ] || { echo "REFUSING TO LAUNCH: origin develop has MOVED off $DEV to $CUR_DEV — every per-PR tree (= head tree today), the pair tree and the all-six tree $ALLDEV are unverified at the new base. Re-pin deliberately (gen_launcher_1130.py DEV + the prompt + this DEV)."; exit 10; }
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
