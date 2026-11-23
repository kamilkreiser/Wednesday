#!/bin/bash
# QA-W-GATE-TEST: can the test fail? w1.py run-set (head 3838bd5) with a fault-injecting copy of the Mac stand-in. 0 model runs.
Q=/private/tmp/claude-501/qwg; S=$Q/clone/spikes/W1-windows-exec-hook; SI=$Q/t/standin/qa_stand_in.py
export TMPDIR=$Q/tmp HOME=$Q/fakehome
mkdir -p $HOME/.claude; [ -f $HOME/.claude/settings.json ] || echo '{}' > $HOME/.claude/settings.json
H=$Q/target/debug/coagent-hook; ST=$Q/target/debug/w1-stub
n=0
run() { # name setup cases extra-args... ; env from caller
  n=$((n+1)); name=$1; setup=$2; cases=$3; shift 3
  W=$Q/r/$name; mkdir -p $Q/r
  echo "=== RUN $name (set-up $setup, cases ${cases:-all}, QA_FAULT=${QA_FAULT:-none} $*)"
  python3 -I $S/w1.py run-set --setup $setup --model stand-in-no-model --claude $SI --hook $H --stub $ST --work $W --out $W/out ${cases:+--cases $cases} "$@" 2>&1 | grep -E "^(CASE|REPEAT|PROBE|W1 SET-UP|CLAUDE INVOCATIONS|SETTINGS|w1.py)"
  echo "exit=${PIPESTATUS[0]}"
}
BL=W3,W6,P3,P6,F3d,F4d,F5d,F7d,F9d,F3b,F4b,F5b,F7b,F9b
run green-A A ""
run green-B B ""
QA_FAULT=madefile run file-made A $BL
QA_FAULT=noerr run no-error-result A $BL
QA_FAULT=wrongmode run wrong-mode A W1,W3,P3,F3d,F5d
QA_FAULT=nohook run hook-never-called A ""
QA_FAULT=bashlist run bash-in-lookalike B ""
QA_FAULT=monitorlist run monitor-in-lookalike B ""
QA_FAULT=bashlater QA_MARK=$Q/r/mark1 run bash-after-probe B W1,W3,F3b
W1_STANDIN_IGNORE_TOOLS=1 W1_STANDIN_TOOLS=Read,Write run no-powershell-B B W1,P3
W1_STANDIN_TOOLS=Bash,Read,Write run no-powershell-A A W1,P1,P3
run ceiling-case A W1,W2,W3 --max-runs 2
W1_STANDIN_VOID_ONCE=$Q/r/void1 run ceiling-repeat A W3,W6 --max-runs 2 --max-repeats 3
W1_STANDIN_VOID_ONCE=$Q/r/void2 run void-repeat-ok A W3,W6 --max-runs 3 --max-repeats 3
W1_STANDIN_VOID_ONCE=$Q/r/void3 run void-no-repeat A W3,W6 --max-runs 3
QA_FAULT=chsettings run settings-changed A W1,W3
