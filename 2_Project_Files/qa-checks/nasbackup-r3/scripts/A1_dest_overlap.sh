#!/bin/bash
# A1 — item 6/4: two sets of ONE client whose destination names NEST (X and X/sub). Does one set overwrite the other's
# proven files while the run says GOOD?   A2 — two sets, two clients, the SAME destination name: allow_empty and the baseline.
. "$(dirname "$0")/lib3.sh"; date; uptime
say "== A1 nested destination names, same client"
fixture a1; mkdir -p "$T/vol/WEDNESDAY/docs" "$T/vol/Other"
echo "OUTER-SET-CONTENT of docs/readme (from the seat tree)" > "$T/vol/WEDNESDAY/docs/readme.txt"
echo "INNER-SET-CONTENT (another folder, same file name)!!" > "$T/vol/Other/readme.txt"
std_conf "set=General|WEDNESDAY/docs|$T/vol/Other"
say "night1 rc=$(run "$(at 0 1 0)" n1) GOOD lines=$(good n1) COMPLETE markers=$(completed)"
say "  refused? $(line n1 REFUSED)"
D="$(CURG)/WEDNESDAY/docs/readme.txt"
say "  destination current/WEDNESDAY/docs/readme.txt holds: $(cat "$D" 2>&1)"
say "  source of set WEDNESDAY for that path holds:       $(cat "$T/vol/WEDNESDAY/docs/readme.txt")"
say "  cmp outer source vs destination: $(cmp -s "$T/vol/WEDNESDAY/docs/readme.txt" "$D" && echo SAME || echo DIFFERENT)"
say "  state last_attempt.status=$(state last_attempt.status)  undelivered=$(state last_attempt.undelivered_count)"
say "  copies of the outer content anywhere on the fake NAS: $(/usr/bin/grep -r -l -F OUTER-SET-CONTENT "$T/nas" 2>&1 | sed "s|$T/nas/||")"
say "night2 rc=$(run "$(at 1 1 0)" n2) GOOD lines=$(good n2); to-copy lines: $(/usr/bin/grep -F 'to copy:' "$T/o/n2.txt" | cut -c1-60 | tr '\n' '|')"
say "  after night 2 destination holds: $(cat "$D" 2>&1); sample line: $(line n2 SAMPLE 1 160)"
say "night3 rc=$(run "$(at 2 1 0)" n3) GOOD lines=$(good n3); destination holds: $(cat "$D" 2>&1)"
say "CONTROL (same two sets, the inner one named apart: General|Docs2): "
fixture a1c; mkdir -p "$T/vol/WEDNESDAY/docs" "$T/vol/Other"; echo "OUTER-SET-CONTENT of docs/readme (from the seat tree)" > "$T/vol/WEDNESDAY/docs/readme.txt"; echo "INNER-SET-CONTENT (another folder, same file name)!!" > "$T/vol/Other/readme.txt"
std_conf "set=General|Docs2|$T/vol/Other"
say "  rc=$(run "$(at 0 1 0)" n1) GOOD=$(good n1) outer cmp: $(cmp -s "$T/vol/WEDNESDAY/docs/readme.txt" "$(CURG)/WEDNESDAY/docs/readme.txt" && echo SAME || echo DIFFERENT)"

say "== A2 same destination name under two clients: allow_empty and the fall baseline are keyed by the name alone"
fixture a2; mkdir -p "$T/vol/P1" "$T/vol/P2/d"; for i in 1 2 3 4 5 6 7 8 9 10 11 12; do echo "p1 $i" > "$T/vol/P1/f$i.txt"; done; echo one > "$T/vol/P2/d/x.txt"
std_conf "set=General|Proj|$T/vol/P1" "set=Secuura|Proj|$T/vol/P2"
say "night1 rc=$(run "$(at 0 1 0)" n1) GOOD=$(good n1)  refused: $(line n1 REFUSED 1 200)"
say "  baseline recorded: $(state last_good.set_counts)"
mkdir -p "$T/held"; for i in 3 4 5 6 7 8 9 10 11 12; do mv -n "$T/vol/P1/f$i.txt" "$T/held/"; done
say "night2 (General/Proj fell 12 -> 2) rc=$(run "$(at 1 1 0)" n2) GOOD=$(good n2)  fell-line: $(line n2 'SCOPE FELL' 1 120)"
std_conf "set=General|Proj|$T/vol/P1" "set=Secuura|Proj|$T/vol/P2" "allow_empty=Proj"
mv -n "$T/vol/P1/f1.txt" "$T/vol/P1/f2.txt" "$T/held/"
say "night3 (allow_empty=Proj meant for one; General/Proj now EMPTY) rc=$(run "$(at 2 1 0)" n3) GOOD=$(good n3) empty-lines: $(/usr/bin/grep -c -F 'allows it to be empty' "$T/o/n3.txt")"
date; uptime
