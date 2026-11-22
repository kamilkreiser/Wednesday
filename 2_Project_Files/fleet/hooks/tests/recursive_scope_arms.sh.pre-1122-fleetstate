#!/bin/bash
# Arms for pretooluse_recursive_scope.sh: every FIRE case must exit 2, every QUIET case exit 0.
H="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/pretooluse_recursive_scope.sh"
pass=0; fail=0
run() { # expect cmd
  local exp="$1" cmd="$2" got err
  err=$(python3 -c 'import json,sys; print(json.dumps({"tool_input":{"command":sys.argv[1]}}))' "$cmd" | bash "$H" 2>&1 >/dev/null)
  got=$?
  if [ "$got" = "$exp" ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL (want $exp got $got): $cmd"; echo "  hook said: $err"; fi
}
B=/Volumes/DevMASTER/WEDNESDAY
# FIRE
run 2 "grep -rn foo $B/0_Brain/reference"
run 2 "grep -ril nas $B/0_Brain/reference"
run 2 "LC_ALL=C grep -R -l x 0_Brain/reference/"
run 2 "find /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History -name '*.md'"
run 2 "grep --recursive foo $B/2_Project_Files/local-model/spark/runs"
run 2 "echo hi; grep -rn x $B/2_Project_Files/local-model/night | head"
run 2 "rg foo $B/0_Brain/reference"
# QUIET
run 0 "grep -rn --include='*.md' foo $B/0_Brain/reference/2026-11-05_ks-lane-plan"
run 0 "grep -n foo $B/0_Brain/reference/2026-11-05_ks-lane-plan/SUMMARY.md"
run 0 "find $B/0_Brain/reference -maxdepth 1 -name '2026-11-05*'"
run 0 "grep -rn foo $B/2_Project_Files/fleet/hooks"
run 0 "ls $B/0_Brain/reference | head"
run 0 "grep -rn foo $B/0_Brain/reference # scope-ok: deliberate full census"
run 0 "git -C $B log --oneline -3"
# garbage input passes (fail-open)
gerr=$(printf 'not json' | bash "$H" 2>&1); [ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: garbage input did not pass"; }
echo "recursive_scope arms: $pass pass, $fail fail"
[ $fail = 0 ]
