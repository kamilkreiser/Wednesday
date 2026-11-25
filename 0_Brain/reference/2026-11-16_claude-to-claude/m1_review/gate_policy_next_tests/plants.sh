#!/bin/bash
# QA-POLICY-NEXT by-hand plants (the check's own re-making). Each: a detached worktree of MY clone under qpx/pl/<name>,
# its own empty target dir qpx/pl/tt_<name>/target and test tmp qpx/pl/tt_<name>/testtmp. Patches kept in qpx/pl/patches.
set -u
W=/private/tmp/claude-501/qpx; PL=$W/pl; . $W/h/envx.sh
H=7677162edf6a2fac91156da3e54309f0bfdf5fd9; B=7fc61882b6eed3245428d0e120714bd3b06e0c18
QPN=/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_policy_notes_tests/plants
BLD="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools/tmp/pnx/5f455b/plants"
mkdir -p $PL/patches $PL/logs
mk() { git -C $W/clone worktree add --quiet --detach $PL/$1 $2 || { echo "MKFAIL $1"; exit 1; }; mkdir -p $PL/tt_$1/target $PL/tt_$1/testtmp; }
run() { # name logname args...
  local n=$1 l=$2; shift 2
  local s=$(date +%s)
  CARGO_TARGET_DIR=$PL/tt_$n/target COAGENT_TEST_TMP=$PL/tt_$n/testtmp python3 -B $W/h/inroot.py $PL/$n cargo test -p coagent-policy --locked --offline "$@" > $PL/logs/$l.log 2>&1
  local rc=$?
  echo "== $l tree $n at $(git -C $PL/$n rev-parse --short HEAD) rc=$rc secs=$(( $(date +%s)-s )) compiled_crate=$(grep -c 'Compiling coagent-policy' $PL/logs/$l.log) :: $(grep -m1 -E 'test result' $PL/logs/$l.log)"
  grep -m1 -A1 'panicked at' $PL/logs/$l.log | tail -1 | cut -c1-600
}
py() { python3 -B -c "$1"; }
case "$1" in
p1a) mk p1a $H; git -C $PL/p1a show b6af26c -- crates/coagent-policy/src/engine.rs crates/coagent-policy/Cargo.toml > $PL/patches/p1a_item1.patch; git -C $PL/p1a apply -R $PL/patches/p1a_item1.patch && git -C $PL/p1a diff > $PL/patches/p1a.diff; run p1a p1a --test t25_owner_allow switch_screen ;;
p1b)
  for k in 1 2 3; do n=p1b$k; mk $n $H
    case $k in
      1) O='It can also read, change, delete or send'; N='It can also read';;
      2) O='in the same way read, change, delete or send files'; N='in the same way read files';;
      3) O="a terminal command can read, change, delete or send files on the owner's"; N="a terminal command can read files on the owner's";;
    esac
    O="$O" N="$N" python3 -B -c "
import os; p='$PL/$n/docs/POLICY.md'; s=open(p).read(); o=os.environ['O']; assert s.count(o)==1, s.count(o); open(p,'w').write(s.replace(o,os.environ['N']))"
    git -C $PL/$n diff > $PL/patches/$n.diff; run $n $n --test t25_owner_allow docs_name
  done ;;
p2) mk p2 $H; run p2 p2 --features red_owner_spellings_off --test t25_owner_allow agent_word_mentions ;;
p3) mk p3 $H; git -C $PL/p3 checkout $B -- crates/coagent-policy/tests/owner_common/mod.rs; git -C $PL/p3 diff HEAD > $PL/patches/p3.diff; run p3 p3 --test t25_owner_allow fixture_facts_refuses ;;
pT26a|pT26b) mk $1 $H; git -C $PL/$1 apply $QPN/$1.patch && git -C $PL/$1 diff > $PL/patches/$1.diff; run $1 $1 --test t26_owner_property ;;
p4c|p4s)
  for c in base:$B head:$H; do n=${1}_${c%%:*}; mk $n ${c#*:}
    if [ $1 = p4c ]; then
      python3 -B -c "
p='$PL/$n/crates/coagent-policy/src/owner_mode.rs'; s=open(p).read(); o='cwd_not_absolute: !std::path::Path::new(&input.cwd).is_absolute(),'; assert s.count(o)==1; open(p,'w').write(s.replace(o,'cwd_not_absolute: false, // QPX PLANT (i)'))"
    else
      python3 -B -c "
p='$PL/$n/crates/coagent-policy/src/owner_mode.rs'; s=open(p).read()
o='''sandbox_flag_not_false: input
            .tool_input
            .get(\"dangerouslyDisableSandbox\")
            .is_some_and(|v| v.as_bool() != Some(false)),'''
assert s.count(o)==1; open(p,'w').write(s.replace(o,'sandbox_flag_not_false: false, // QPX PLANT (ii)'))"
    fi
    git -C $PL/$n diff > $PL/patches/$n.diff; run $n ${n}_t26 --test t26_owner_property; run $n ${n}_t25 --test t25_owner_allow
  done ;;
p5) mk p5 $H; git -C $PL/p5 apply "$BLD/p5.diff" && git -C $PL/p5 diff > $PL/patches/p5.diff; run p5 p5 --test t27_owner_dark ;;
p4i) mk p4i $H; python3 -B $W/h/mk_p4i.py $PL/p4i/crates/coagent-policy/tests/t26_owner_property.rs && git -C $PL/p4i diff > $PL/patches/p4i.diff; run p4i p4i --test t26_owner_property -- --nocapture; grep -E '^QPX|^REACH' $PL/logs/p4i.log ;;
*) echo usage; exit 2;;
esac
