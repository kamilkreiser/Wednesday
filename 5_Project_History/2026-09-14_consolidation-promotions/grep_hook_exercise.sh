#!/bin/bash
# Exercise harness for pretooluse_grep_case.sh: feeds hook JSON on stdin per fixture, prints
# expected vs observed. FIRE = non-empty stdout JSON with additionalContext; QUIET = empty.
H="$1"; pass=0; fail=0
run() { # $1 expect (FIRE|QUIET) $2 command text
  local exp="$1" cmd="$2"
  local json; json=$(python3 -c 'import json,sys; print(json.dumps({"tool_name":"Bash","tool_input":{"command":sys.argv[1]}}))' "$cmd")
  local out err rc
  out=$(printf '%s' "$json" | bash "$H" 2>/tmp/grep_hook_err.$$); rc=$?; err=$(cat /tmp/grep_hook_err.$$); rm -f /tmp/grep_hook_err.$$
  local obs="QUIET"; [ -n "$out" ] && obs="FIRE"
  local mark="PASS"; { [ "$obs" != "$exp" ] || [ "$rc" != 0 ]; } && mark="FAIL"
  [ "$mark" = PASS ] && pass=$((pass+1)) || fail=$((fail+1))
  printf '%s  expect=%-5s observed=%-5s rc=%s  cmd: %s\n' "$mark" "$exp" "$obs" "$rc" "$(printf '%s' "$cmd" | head -1 | cut -c1-90)"
  [ -n "$out" ] && printf '      stdout: %s\n' "$(printf '%s' "$out" | cut -c1-230)"
  [ -n "$err" ] && printf '      stderr: %s\n' "$(printf '%s' "$err" | cut -c1-120)"
}
run FIRE  "grep -c 'do not push' /tmp/f"
run FIRE  "/usr/bin/grep -q \"Context limit\" /tmp/f"
run QUIET "grep -ci 'do not push' /tmp/f"
run QUIET "grep -c foo /tmp/f"
run QUIET "grep -qi \"a b\" /tmp/f"
run FIRE  "grep -c 'x \$(y)' /tmp/f"
run QUIET "grep -F -i -c 'a b' /tmp/f"
run QUIET "/usr/bin/grep -iF -q \"a b\" /tmp/f"
run FIRE  "grep -n -E 'a b' /tmp/f"
run FIRE  "/usr/bin/grep -nE \"a b\" /tmp/f"
run QUIET "grep 'a b' /tmp/f"
run QUIET "grep -c \"\$VAR\" /tmp/f"
run FIRE  "cat /tmp/f | /usr/bin/grep -c 'do not push'"
run QUIET $'cat > /tmp/note.md <<\'EOF2\'\nprose: the seat ran grep -c \'do not push\' and got 0\nEOF2'
run QUIET "/usr/bin/grep --count --ignore-case 'a b' /tmp/f"
run FIRE  "/usr/bin/grep --count 'a b' /tmp/f"
run FIRE  "grep -c -e 'a b' /tmp/f"
run QUIET "git grep -c 'a b'"
run FIRE  "grep -c 'a b' /tmp/f | grep -qi 'c d'"
run QUIET "grep -c 'single' /tmp/f && grep -qi 'two words' /tmp/g"
run FIRE  "grep -q \"\$(cat /tmp/phrase)\" /tmp/f"
run QUIET "ls -la /tmp"
# malformed input must pass silently with rc 0
out=$(printf 'not json' | bash "$H" 2>/dev/null); rc=$?; if [ -z "$out" ] && [ "$rc" = 0 ]; then pass=$((pass+1)); echo "PASS  malformed stdin -> quiet, rc=0"; else fail=$((fail+1)); echo "FAIL  malformed stdin -> out='$out' rc=$rc"; fi
echo "TOTAL pass=$pass fail=$fail"
