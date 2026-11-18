#!/bin/bash
# clock_guard_arms.sh — red-proof arms for tuesday/hooks/pretooluse_clock_guard.sh. Each arm feeds a hook input and
# checks the exit code. Run: bash 2_Project_Files/tuesday/tests/clock_guard_arms.sh   (prints PASS/FAIL per arm, rc 0 iff all pass)
H="$(dirname "$0")/../hooks/pretooluse_clock_guard.sh"
T="$(mktemp -d)"; mkdir -p "$T/TUESDAY/0_Brain/tasks" "$T/TUESDAY/0_Brain/daily_tuesday" "$T/WEDNESDAY/0_Brain/tasks"
printf 'old line ~14:3x history\n' > "$T/TUESDAY/0_Brain/tasks/P.md"
FAILS=0
arm() { # name expected_rc tree json
  local got; got=$(printf '%s' "$4" | CLAUDE_PROJECT_DIR="$T/$3" bash "$H" 2>/dev/null; echo $?)
  if [ "$got" = "$2" ]; then echo "PASS $1 (rc $got)"; else echo "FAIL $1 (want $2, got $got)"; FAILS=$((FAILS+1)); fi
}
P="$T/TUESDAY/0_Brain/tasks/P.md"; D="$T/TUESDAY/0_Brain/daily_tuesday/2026-11-18.md"; L="$T/TUESDAY/0_Brain/learnings/_ledger_laptop_datasec.md"
arm "edit pickup with new 12:5x refuses"        2 TUESDAY "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$P\",\"old_string\":\"a\",\"new_string\":\"- 12:5x: gate read\"}}"
arm "edit pickup upper-case X refuses"          2 TUESDAY "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$P\",\"old_string\":\"a\",\"new_string\":\"at 9:1X\"}}"
arm "edit ledger refuses"                       2 TUESDAY "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$L\",\"old_string\":\"a\",\"new_string\":\"s290 at 13:1x\"}}"
arm "write daily note with new token refuses"   2 TUESDAY "{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$D\",\"content\":\"- 08:2x done\"}}"
arm "multiedit with one new token refuses"      2 TUESDAY "{\"tool_name\":\"MultiEdit\",\"tool_input\":{\"file_path\":\"$P\",\"edits\":[{\"old_string\":\"x\",\"new_string\":\"y\"},{\"old_string\":\"a\",\"new_string\":\"at 10:4x\"}]}}"
arm "exact clock passes"                        0 TUESDAY "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$P\",\"old_string\":\"a\",\"new_string\":\"before 12:41:41 (date)\"}}"
arm "token already in old_string passes"        0 TUESDAY "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$P\",\"old_string\":\"DELIVERED ~14:3x\",\"new_string\":\"DELIVERED ~14:3x (done)\"}}"
arm "write keeping an existing old token passes" 0 TUESDAY "{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$P\",\"content\":\"old line ~14:3x history\\nnew line at 12:41:41\"}}"
arm "write adding a SECOND copy refuses"        2 TUESDAY "{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$P\",\"content\":\"old line ~14:3x history\\nagain 14:3x\"}}"
arm "[quoted clock] line passes"                0 TUESDAY "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$P\",\"old_string\":\"a\",\"new_string\":\"the seat wrote 07:5x [quoted clock]\"}}"
arm "non-target file passes"                    0 TUESDAY "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$T/TUESDAY/2_Project_Files/x.md\",\"old_string\":\"a\",\"new_string\":\"12:5x\"}}"
arm "other seat tree passes"                    0 WEDNESDAY "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$T/WEDNESDAY/0_Brain/tasks/P.md\",\"old_string\":\"a\",\"new_string\":\"12:5x\"}}"
arm "Bash tool ignored"                         0 TUESDAY "{\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"echo 12:5x\"}}"
arm "unparseable input fails open"              0 TUESDAY "not json"
mv "$T" "$T.done" 2>/dev/null
echo "FAILS=$FAILS"; [ "$FAILS" = 0 ]
