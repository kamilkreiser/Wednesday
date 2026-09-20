#!/bin/bash
# repin_and_launch.sh — the LAUNCH ACTION for the #1106-#1111 batch gate (tier-1 floor). The re-pin and the launch are ONE action (Kam 2026-09-18:
# a stale pin costs a whole gate session). Order: (1) origin develop + the six branches + the six refs/pull/N/head by `git ls-remote` READ from the
# Secuura checkout; (2) the six PR heads re-read from the GitHub PULLS API (a second, independent instrument); (3) refuse rc 10 unless develop is
# still cbae988db, rc 11 unless every head equals its pin and is open; (4) usage gate; (5) the launcher's own --check; (6) cockpit.sh add — the
# fleet's own tooling, never raw tmux send-keys.
# READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed, anchored or commented.
# Derived from gatesets/2026-09-20_gate1105/repin_and_launch.sh (data changed: six PRs, six heads, the pane name QA/Secuura-batch1106 — registered
# in fleet/inbox_routing.conf 2026-09-21 02:42 AEST, backup inbox_routing.conf.pre-0921-0242-qagate1106). NOT RUN by the drafter.
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1106to1111'
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1106-1111.sh'
DEV=cbae988dbe90ebe556459ada2cb437eaf80e2402   # the pin: 778e6cfe2 + the #1105 squash (Seat A 15th on Wednesday's GO, 15:2xZ)
BASE=778e6cfe2b6061d60ffcf3a57a951c84dc152b67  # the six heads' parent = merge-base
ALLDEV=2e981e7779dc9bcabecd099c6e93da21345a8ed0  # all six over $DEV (predict_batch_scratch.out + generator tree-hash)
PANE='QA/Secuura-batch1106'
PRS="1106:2abc82d11014f00567b75a6b8fab5ec5e78f9df2 1107:7e7da2f88f9ef8dcf571a5720bb7bffcd700aa30 1108:4904c081c4f9be776acef78349bc10384f10de35 1109:f592268af36b282029e50ff2fa1ebe2614304b81 1110:a2a7d7845e75dac2df5c6ad0c4109d5f63394d4c 1111:3d1ea289a0c367af5cd0d060322e46fc900a1c76"
echo "LAUNCH ACTION $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ')"

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' ls-remote origin \
  refs/heads/develop refs/pull/1106/head refs/pull/1107/head refs/pull/1108/head refs/pull/1109/head refs/pull/1110/head refs/pull/1111/head \
  'refs/heads/feature/ks-1232-*' 'refs/heads/feature/ks-753-*' 'refs/heads/feature/ks-1234-*' 'refs/heads/feature/ks-1279-*' 'refs/heads/feature/ks-880-*' 'refs/heads/feature/ks-1223-*' \
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
for n in (1106, 1107, 1108, 1109, 1110, 1111):
    p = get('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/%d' % n)
    print('API #%d head %s base %s (base sha %s) state %s' % (n, p['head']['sha'], p['base']['ref'], p['base']['sha'], p['state']))
PY
rc=$?
echo "pulls API rc=$rc"
cat "$GS/api_heads_launch.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the pulls API read failed"; exit 3; }

echo "--- 3. the pins, judged"
echo "  develop   ls-remote $CUR_DEV | pinned $DEV (base $BASE, all-six tree over the pin $ALLDEV) | $([ "$CUR_DEV" = "$DEV" ] && echo UNMOVED || echo MOVED)"
[ "$CUR_DEV" = "$DEV" ] || { echo "REFUSING TO LAUNCH: origin develop has MOVED off $DEV to $CUR_DEV — every per-PR tree over develop and the all-six tree $ALLDEV are unverified at the new base. Re-pin deliberately (gen_launcher_1106.py DEV + the prompt + this DEV)."; exit 10; }
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
