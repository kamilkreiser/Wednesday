#!/bin/bash
# Exercise pretooluse_grep_cut.sh: FIRE arms must print additionalContext; QUIET arms must print nothing.
H="$(dirname "${BASH_SOURCE[0]}")/.."
pass=0; fail=0
arm() { # $1 want(fire|quiet) $2 command
  out=$(python3 -c 'import json,sys;print(json.dumps({"tool_input":{"command":sys.argv[1]}}))' "$2" | bash "$H/pretooluse_grep_cut.sh" 2>>"${TMPDIR:-/tmp}/grep_cut_arms.stderr.log")
  if [ "$1" = fire ]; then case "$out" in *additionalContext*) pass=$((pass+1));; *) fail=$((fail+1)); echo "FAIL want fire: $2";; esac
  else [ -z "$out" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL want quiet: $2"; }; fi
}
arm fire  "/usr/bin/grep -n -i 'two-card' f.txt | cut -c1-330"
arm fire  "grep -i x f | head -5 | cut -c1-200"
arm fire  "a=1; /usr/bin/grep -c y f | cut -c 1-80"
arm quiet "/usr/bin/grep -o -i -c 'two-card' f.txt"
arm quiet "sed -n 1,5p f | cut -c1-200"
arm quiet "grep x f; cut -c1-10 g"
arm quiet "cat > f <<'Q'
grep a b | cut -c1-9
Q"
arm quiet "grep -i x f | cut -d, -f2"
echo "pass=$pass fail=$fail"
[ $fail -eq 0 ]
