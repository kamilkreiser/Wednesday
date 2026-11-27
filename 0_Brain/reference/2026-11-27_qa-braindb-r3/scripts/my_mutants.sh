#!/bin/bash
# my_mutants.sh: run each of my mutants through the COPY's own suite, 4 at a time; verdict = number of FAIL lines
S="/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3"; O="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-braindb-r3"; PFC="$S/lanecopy/WEDNESDAY/2_Project_Files"
OUT="$S/mymut-$(date +%H%M%S)"; mkdir -p "$OUT"
NAMES="${*:-$(python3 $O/scripts/my_mutate.py --list)}"
one() { local n="$1" d="$OUT/$1"; mkdir -p "$d/scr"
  if ! python3 "$O/scripts/my_mutate.py" "$n" "$PFC" "$d" > "$d/mutate.out" 2>&1; then echo "SETUP-ERROR $(tail -1 "$d/mutate.out")" > "$d/verdict"; return 0; fi
  /bin/bash "$d/WEDNESDAY/2_Project_Files/brain-db/tests/run.sh" "$d/scr" > "$d/suite.log" 2>&1; local rc=$?
  local nf np; nf="$(/usr/bin/grep -i -F -c '  FAIL  ' "$d/suite.log")"; np="$(/usr/bin/grep -i -F -c '  PASS  ' "$d/suite.log")"
  if [ "$nf" = "0" ] && [ "$rc" -eq 0 ]; then echo "SURVIVED ($np passed, 0 failed, rc 0)" > "$d/verdict"; else echo "CAUGHT $nf FAIL line(s), $np passed, rc $rc: $(/usr/bin/grep -i -F '  FAIL  ' "$d/suite.log" | head -1 | cut -c9-170)" > "$d/verdict"; fi
}
r=0
for n in $NAMES; do one "$n" & r=$((r+1)); if [ "$r" -ge 4 ]; then wait; r=0; fi; done; wait
for n in $NAMES; do printf '%-40s %s\n' "$n" "$(cat "$OUT/$n/verdict")"; done
echo "output dir $OUT"; date '+%Y-%m-%d %H:%M:%S %Z'
