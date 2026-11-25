#!/bin/bash
# QA-MEASURE-2-R2 task 5 (m-1, T-c): the head's check_run.py fed the committed W1 excerpt plus ONE planted line per shape
# (each shape the first check listed, naming a made-up model or a foreign command), from memory via /dev/fd (no file written).
# usage: bash qm2r_checkrun.sh <spike folder of the clone at the head>
D="$1"; BASE="$D/raw/W1/debug.excerpt.log"; HK="$D/raw/W1/hook.stdin.jsonl"; TS="2026-11-25T21:55:50.000Z [DEBUG]"
run() { # $1 label, $2 planted line(s)
  out=$(python3 -I -B "$D/check_run.py" claude-haiku-5-5 <(cat "$BASE"; printf '%s\n' "$2") "$HK"); rc=$?
  echo "== $1 (exit $rc)"; echo "$out" | grep -v 'hook env names' | sed 's/^/   /'
}
run "unplanted" ""
run "model: dispatch line, other model"      "$TS [API:timing] dispatching to firstParty model=claude-madeup-7-7"
run "model: set_model, other model"          "$TS [engine] send set_model model=claude-madeup-7-7"
run "model: auto-mode gate, other model"     "$TS [auto-mode] verifyAutoModeGateAccess: enabledState=enabled model=claude-madeup-7-7 modelSupported=true"
run "model: advisor line, other model ALONE" "$TS [AdvisorTool] Server-side tool enabled with claude-madeup-7-7 as the advisor model"
run "model: advisor line naming the run's model" "$TS [AdvisorTool] Server-side tool enabled with claude-haiku-5-5 as the advisor model"
run "model: the seat's three planted at once" "$TS [AdvisorTool] Server-side tool enabled with claude-madeup-7-7 as the advisor model
$TS [engine] send set_model model=claude-madeup-7-7
$TS [auto-mode] verifyAutoModeGateAccess: x model=claude-madeup-7-7 y"
run "hook: Hooks: Ev:m [cmd] finished with status" "$TS Hooks: PreToolUse:Bash [/usr/local/bin/foreign-hook] finished with status 0 (5ms)"
run "hook: Hooks: Ev:m [cmd] (plugin x) finished"  "$TS Hooks: PreToolUse:Bash [/usr/local/bin/foreign-hook] (plugin foo@bar) finished with status 0 (5ms)"
run "hook: Hook Ev (cmd) returned permissionDecision" "$TS Hook PreToolUse (/usr/local/bin/foreign-hook) returned permissionDecision: allow"
run "hook: Ev:m [cmd] completed with status"   "$TS Elicitation:m2 [/usr/local/bin/foreign-hook] completed with status 0"
run "hook: Spawned hook command for Ev: cmd"   "$TS Spawned hook command for PreToolUse: /usr/local/bin/foreign-hook"
run "hook: foreign cmd whose text holds hook_stub.py" "$TS Hooks: PreToolUse:Bash [/tmp/evil --as hook_stub.py] finished with status 0 (5ms)"
