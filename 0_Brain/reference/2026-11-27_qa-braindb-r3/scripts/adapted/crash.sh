#!/bin/bash
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/chk
C="$S/crash-$(date +%H%M%S)"; mkdir -p "$C/q"
TOOL=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/lanecopy/WEDNESDAY/2_Project_Files/brain-db/braindb.sh
python3 /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/lanecopy/WEDNESDAY/2_Project_Files/brain-db/tests/make_fixtures.py "$C/tree" > "$C/fx.out" 2>&1
X() { BRAINDB_ROOT="$C/tree" BRAINDB_PGDATA="$C/pg" BRAINDB_SOCKDIR=/tmp/qa3c WED_AGENT=wednesday /bin/bash "$TOOL" "$@"; }
sh() { awk -v n="${1:-220}" '{print substr($0,1,n)}'; }
L="$C/tree/0_Brain/learnings"
X rebuild > "$C/r0.out" 2>&1; echo "baseline rebuild rc=$? ; $(X check | sh 80)"
echo "---- K1 an indexed lesson made unreadable (mode 000)"
printf -- '---\ntier: W\n---\n# locked\n\nzk1\n' > "$L/2026-06-01_locked.md"; chmod 000 "$L/2026-06-01_locked.md"
X rebuild > "$C/k1.out" 2>&1; echo "rebuild rc=$? ; traceback lines: $(/usr/bin/grep -i -c 'Traceback' "$C/k1.out") ; last: $(tail -1 "$C/k1.out" | sh)"
X check > "$C/k1c.out" 2>&1; echo "check rc=$? ; traceback lines: $(/usr/bin/grep -i -c 'Traceback' "$C/k1c.out") ; last: $(tail -1 "$C/k1c.out" | sh)"
X search xneighbour01 > "$C/k1s.out" 2>&1; echo "search (old index) rc=$? ; $(tail -1 "$C/k1s.out" | sh 60)"
chmod 644 "$L/2026-06-01_locked.md"; mv -n "$L/2026-06-01_locked.md" "$C/q/"
echo "---- K2 one lesson section with 300,000 DIFFERENT words (a tsvector over 1 MB)"
python3 -c "
import sys
open(sys.argv[1],'w').write('---\ntier: W\n---\n# big\n\nzk2 ' + ' '.join('w%07dx' % i for i in range(300000)) + '\n')" "$L/2026-06-02_big.md"
ls -la "$L/2026-06-02_big.md" | awk '{print \$5, "bytes"}'
X rebuild > "$C/k2.out" 2>&1; echo "rebuild rc=$? ; $(/usr/bin/grep -i -E 'ERROR|FAILED' "$C/k2.out" | sh | head -3)"
X check 2>&1 | head -2 | sh 150; echo "(the whole rebuild is lost, not just the one file: every later rebuild fails the same way until the file changes)"
mv -n "$L/2026-06-02_big.md" "$C/q/"
echo "---- K3 a 30 MB daily note (one bullet)"
python3 -c "
import sys
open(sys.argv[1],'w').write('# d\n\n## S\n- 06:19 zk3 ' + ('lorem ipsum dolor ' * 1700000) + '\n')" "$C/tree/0_Brain/daily/2026-06-03.md"
X rebuild > "$C/k3.out" 2>&1; echo "rebuild rc=$? ; $(tail -1 "$C/k3.out" | sh 100) ; $(/usr/bin/grep -i -E 'ERROR|FAILED' "$C/k3.out" | sh | head -2)"
mv -n "$C/tree/0_Brain/daily/2026-06-03.md" "$C/q/"
echo "---- K4 rules index removed (missing), then a rules index that is a directory"
mv -n "$L/_rules_index.tsv" "$C/q/"
X rebuild > "$C/k4.out" 2>&1; echo "rebuild without a rules index rc=$? ; $(/usr/bin/grep -i -E 'lesson  |Traceback' "$C/k4.out" | sh 100)"
echo "   lessons scoped ONLY to other seats now indexed (no row -> tier alone): xcanary03=$(/opt/homebrew/opt/postgresql@15/bin/pg_dump --data-only --schema=brain -h /tmp/qa3c -d braindb | /usr/bin/grep -i -c xcanary03) xcanary17=$(/opt/homebrew/opt/postgresql@15/bin/pg_dump --data-only --schema=brain -h /tmp/qa3c -d braindb | /usr/bin/grep -i -c xcanary17) (control xneighbour01=$(/opt/homebrew/opt/postgresql@15/bin/pg_dump --data-only --schema=brain -h /tmp/qa3c -d braindb | /usr/bin/grep -i -c xneighbour01))"
mv -n "$C/q/_rules_index.tsv" "$L/_rules_index.tsv"
echo "---- K5 BRAINDB_WEAK not a number; search word starting with a dash; empty query"
BRAINDB_WEAK=abc X search xneighbour01 > "$C/k5.out" 2>&1; echo "rc=$? ; traceback: $(/usr/bin/grep -i -c 'Traceback' "$C/k5.out") ; $(tail -1 "$C/k5.out" | sh 100)"
X search "-what do I do" > "$C/k5b.out" 2>&1; echo "search '-what do I do' rc=$? ; $(tail -1 "$C/k5b.out" | sh 120)"
X search "" > "$C/k5c.out" 2>&1; echo "search '' rc=$? ; $(tail -1 "$C/k5c.out" | sh 120)"
X search > "$C/k5d.out" 2>&1; echo "search (no words) rc=$? ; $(tail -1 "$C/k5d.out" | sh 120)"
X rebuild > "$C/r9.out" 2>&1; X check | sh 60
X stop | tail -1 | sh 50
snap="$(ps -axww -o pid=,command=)"; echo "processes with -D under $C: $(printf '%s\n' "$snap" | /usr/bin/grep -i -F -c -- "-D $C")"
