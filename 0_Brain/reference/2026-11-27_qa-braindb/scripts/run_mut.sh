#!/bin/bash
# run_mut.sh <mutation name> : copy the tool, mutate the COPY, run the copy's suite, list FAIL lines
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/qa-braindb
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-braindb
n="$1"; dst="$S/mut/$n-$(date +%H%M%S)"
python3 "$S/mut/mutate.py" "$n" "$dst/copy" || exit 2
mkdir -p "$dst/scr"
/bin/bash "$dst/copy/2_Project_Files/brain-db/tests/run.sh" "$dst/scr" > "$O/02_mut_$n.log" 2>&1
echo "== $n: suite rc=$? ; $(tail -1 "$O/02_mut_$n.log" | cut -c1-40)"
/usr/bin/grep -i '  FAIL  ' "$O/02_mut_$n.log" | cut -c1-230 | head -14
echo "   (FAIL lines: $(/usr/bin/grep -i -c '  FAIL  ' "$O/02_mut_$n.log"), PASS lines: $(/usr/bin/grep -i -c '  PASS  ' "$O/02_mut_$n.log"))"
snap="$(ps -axww -o pid=,command=)"
left="$(printf '%s\n' "$snap" | /usr/bin/grep -i -F -- "-D $dst" )"
if [ -n "$left" ]; then echo "   LEFT RUNNING: $left"; fi
