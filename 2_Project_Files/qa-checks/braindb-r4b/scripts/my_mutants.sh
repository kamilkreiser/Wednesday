#!/bin/bash
# my_mutants.sh [names...]: each of my mutants through the scratch copy's own suite, 3 at a time.
# verdict = SURVIVED (suite rc 0, 0 FAIL lines) or CAUGHT (with the first failing line); beside it what I predicted.
S="/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/063b86e1-bf25-4ab6-9e57-b16c1f229efa/scratchpad/r4b"
Q="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/qa-checks/braindb-r4b"
PFC="$S/lanecopy/WEDNESDAY/2_Project_Files"
OUT="$S/mymut-$(date +%H%M%S)"; mkdir -p "$OUT"
NAMES="${*:-$(python3 "$Q/scripts/my_mutate.py" --list)}"
echo "start $(date '+%Y-%m-%d %H:%M:%S %Z') ; $(uptime)"
one() { local n="$1" d="$OUT/$1"; mkdir -p "$d/scr"
  if ! python3 "$Q/scripts/my_mutate.py" "$n" "$PFC/brain-db" "$PFC" "$d" > "$d/mutate.out" 2>&1; then echo "SETUP-ERROR $(tail -1 "$d/mutate.out")" > "$d/verdict"; return 0; fi
  /bin/bash "$d/WEDNESDAY/2_Project_Files/brain-db/tests/run.sh" "$d/scr" > "$d/suite.log" 2>&1; local rc=$?
  local nf np; nf="$(/usr/bin/grep -i -F -c '  FAIL  ' "$d/suite.log")"; np="$(/usr/bin/grep -i -F -c '  PASS  ' "$d/suite.log")"
  if [ "$nf" = "0" ] && [ "$rc" -eq 0 ]; then echo "SURVIVED ($np passed, 0 failed, rc 0)" > "$d/verdict"
  else echo "CAUGHT $nf FAIL line(s), $np passed, rc $rc: $(/usr/bin/grep -i -F '  FAIL  ' "$d/suite.log" | head -1 | cut -c9-150)" > "$d/verdict"; fi
}
r=0
for n in $NAMES; do one "$n" & r=$((r+1)); if [ "$r" -ge 3 ]; then wait; r=0; fi; done; wait
for n in $NAMES; do printf '%-36s predicted %-8s %s\n    broke: %s\n' "$n" "$(python3 "$Q/scripts/my_mutate.py" --expect "$n")" "$(cat "$OUT/$n/verdict")" "$(python3 "$Q/scripts/my_mutate.py" --what "$n")"; done
snap="$(ps -axww -o pid=,command=)"; echo "server processes left under $OUT: $(printf '%s\n' "$snap" | /usr/bin/grep -F -c -- "-D $OUT")"
echo "output dir $OUT ; end $(date '+%Y-%m-%d %H:%M:%S %Z') ; $(uptime)"
