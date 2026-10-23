#!/bin/bash
# launch_when_cool_arms.sh: four arms for tuesday/tools/launch_when_cool.sh's pane-space retry (2026-10-23 s150).
# Uses a stub cockpit (fixtures/lwc_stub_cockpit.sh); touches no real pane except selecting %0 (the coordinator).
H="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; L="${1:-$H/../tools/launch_when_cool.sh}"
W="$(mktemp -d -t lwc_arms)"; PASS=0; FAIL=0
arm() { m=$1 want_rc=$2 want_adds=$3 want_stamp=$4; d=$W/$m; mkdir -p $d; echo 0 > $d/count; echo old > $d/stamp
  STUB_DIR=$d MODE=$m LWC_COCKPIT=$H/fixtures/lwc_stub_cockpit.sh LWC_STAMP=$d/stamp LOAD_MAX=1000 GAP_MIN=0 LWC_RETRY_SLEEP=0 \
    bash "$L" Test/X "echo hi" > $d/out 2>&1; rc=$?
  s=old; [ "$(cat $d/stamp)" != old ] && s=new
  if [ $rc = $want_rc ] && [ "$(cat $d/count)" = $want_adds ] && [ $s = $want_stamp ]; then PASS=$((PASS+1)); echo "PASS $m"; else FAIL=$((FAIL+1)); echo "FAIL $m rc=$rc adds=$(cat $d/count) stamp=$s"; fi; }
arm nospace_once 0 2 new; arm nospace_always 1 4 old; arm other 3 1 old; arm ok 0 1 new
# ONE-WAITER lock arms (2026-10-23 s150): a live holder refuses rc 5 with no add; a dead or "free" holder proceeds; exit leaves "free".
lockarm() { label=$1 holder=$2 want_rc=$3 want_adds=$4; d=$W/lock_$label; mkdir -p $d; echo 0 > $d/count; echo old > $d/stamp; echo "$holder" > $d/lock
  STUB_DIR=$d MODE=ok LWC_COCKPIT=$H/fixtures/lwc_stub_cockpit.sh LWC_STAMP=$d/stamp LWC_LOCK=$d/lock LOAD_MAX=1000 GAP_MIN=0 \
    bash "$L" Test/X "echo hi" > $d/out 2>&1; rc=$?
  if [ $rc = $want_rc ] && [ "$(cat $d/count)" = $want_adds ] && { [ $rc = 5 ] || [ "$(cat $d/lock)" = free ]; }; then PASS=$((PASS+1)); echo "PASS lock_$label"; else FAIL=$((FAIL+1)); echo "FAIL lock_$label rc=$rc adds=$(cat $d/count) lock=$(cat $d/lock)"; fi; }
sleep 120 & LIVE=$!
lockarm live $LIVE 5 0; lockarm free free 0 1; lockarm dead 999999 0 1
kill $LIVE 2>/dev/null
echo "PASS=$PASS FAIL=$FAIL (scratch $W)"; [ $FAIL = 0 ]
