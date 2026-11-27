#!/bin/bash
# A8 — items 2 (empty plans), 3 (sample finding and read-back), 4 (containment), on the fake NAS.
. "$(dirname "$0")/lib3.sh"; date; uptime
alter() { "$PY" -c 'import sys,os
for p in sys.argv[1:]:
    n=os.path.getsize(p); open(p,"wb").write(b"Z"*n)' "$@"; }
stale() { local n=0 f; for f in "$T/vol/WEDNESDAY"/sub/*.txt; do cmp -s "$f" "$(CURG)/WEDNESDAY/sub/$(basename "$f")" || n=$((n+1)); done; echo $n; }
say "== 2a. patterns that (nearly) empty a set without being a refused shape"
for pat in '*t' '?*.*' '[a-z]*' '*[!.]' '*.txt' 'a*' '[!x]*' '*??' '*.?*'; do
  fixture "p$(printf '%s' "$pat" | od -An -tx1 | tr -d ' \n')"; for i in 1 2 3 4 5 6 7 8; do echo "$i" > "$T/vol/WEDNESDAY/sub/n$i.txt"; done; std_conf "exclude_name=$pat"
  rc=$(run "$(at 0 1 0)" r); say "  exclude_name=$pat first run: rc=$rc GOOD=$(good r) planned=$(line r 'source in scope' 1 40 | sed 's/.*scope: //') $(line r 'matches every' 1 30)$(line r 'EMPTY SCOPE' 1 30)"; done
say "== 2b. allow_empty on a set that FILLS and then EMPTIES again; and a set that goes 9 -> 0 files WITH allow_empty"
fixture ae; mkdir -p "$T/vol/E/d"; std_conf "set=General|E|$T/vol/E" "allow_empty=E"
say "  empty, allowed: rc=$(run "$(at 0 1 0)" r0) GOOD=$(good r0)"
for i in 1 2 3 4 5 6 7 8 9; do echo "$i" > "$T/vol/E/d/f$i.txt"; done
say "  filled with 9: rc=$(run "$(at 1 1 0)" r1) GOOD=$(good r1) baseline=$(state last_good.set_counts.E)"
mkdir -p "$T/held"; mv "$T/vol/E/d"/f*.txt "$T/held/"
say "  emptied again (9 -> 0) under allow_empty: rc=$(run "$(at 2 1 0)" r2) GOOD=$(good r2) ; fall or empty problem lines: $(/usr/bin/grep -c -i -E 'SCOPE FELL|EMPTY SCOPE' "$T/o/r2.txt")"
say "== 2c. the plan is made per set: a file created in set 2 while set 1 copies; a file in set 2 deleted before set 2 is planned"
fixture late; mkdir -p "$T/vol/P2"; echo "second set file" > "$T/vol/P2/x.txt"; echo "will go" > "$T/vol/P2/gone.txt"
CONF_RSYNC="$(mk_stub late 'if [ "$N" = 1 ]; then echo "made during set 1" > "$STUBDIR/../vol/P2/new.txt"; mv "$STUBDIR/../vol/P2/gone.txt" "$STUBDIR/taken/"; fi; exec "$REAL" "$@"')"; std_conf "set=General|P2|$T/vol/P2"
rc=$(run "$(at 0 1 0)" r); say "  rc=$rc GOOD=$(good r) ; new.txt at destination: $([ -f "$(CURG)/P2/new.txt" ] && echo yes || echo no) ; gone.txt named anywhere in the output: $(/usr/bin/grep -c -F 'gone.txt' "$T/o/r.txt") (0 = it left before its set's plan, uncounted by design)"
say "== 3a. the cap passes DURING the full read-back; then the next nights"
fixture rb; for i in $(seq 1 60); do printf 'filler %05d\n' "$i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done; CONF_SAMPLE=5; std_conf
say "  night0 rc=$(run "$(at 0 1 0)" r0) rows=$(idxrows)"
alter "$(CURG)"/WEDNESDAY/sub/f*.txt "$(CURG)/WEDNESDAY/a.txt"
env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" NB_TEST_HASH_DELAY=0.25 "$LANE/nas_backup.sh" --run --now "$(at 1 1 0)" --max-seconds 6 > "$T/o/r1.txt" 2>&1; rc=$?
say "  night1 (61 altered, read-back slowed to 0.25 s a file by the lane's own test hook, cap 6 s): rc=$rc GOOD=$(good r1) rows left=$(idxrows) still-wrong=$(stale); $(line r1 'full read-back that follows' 1 170)"
say "  night2 sample OFF, no cap problem: "; CONF_SAMPLE=0; std_conf; rc=$(run "$(at 2 1 0)" r2); say "    rc=$rc GOOD=$(good r2) still-wrong=$(stale); $(line r2 'to copy:' 1 60) $(line r2 'compared by sha256' 1 90)"
say "== 3b. kill -9 during the read-back (row removal already committed?)"
fixture rbk; for i in $(seq 1 60); do printf 'filler %05d\n' "$i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done; CONF_SAMPLE=5; std_conf
x=$(run "$(at 0 1 0)" r0); alter "$(CURG)"/WEDNESDAY/sub/f*.txt "$(CURG)/WEDNESDAY/a.txt"; say "  rows before=$(idxrows)"
env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" NB_TEST_HASH_DELAY=0.25 "$LANE/nas_backup.sh" --run --now "$(at 1 1 0)" > "$T/o/r1.txt" 2>&1 & BG=$!
sleep 5; TP="$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1]))["pid"])' "$T/lane/state/wednesday.lock.d/owner.json")"; kill -KILL "$TP"; wait $BG 2>&1
say "  after kill -9 mid read-back: rows=$(idxrows) (the rows of unsent files must be gone) state=$(state last_attempt.status)"
x=$(nb --clear-stale-lock 2>&1); CONF_SAMPLE=0; std_conf; rc=$(run "$(at 2 1 0)" r2); say "  next night, sample OFF: rc=$rc GOOD=$(good r2) still-wrong=$(stale) ; $(line r2 'compared by sha256' 1 100)"
say "== 3c. a finding in ONE set: are the other set's proofs on the same NAS withdrawn?"
fixture two; mkdir -p "$T/vol/P2"; for i in 1 2 3 4 5 6; do echo "one $i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; echo "two $i" > "$T/vol/P2/g$i.txt"; done; CONF_SAMPLE=1; std_conf "set=General|P2|$T/vol/P2"
x=$(run "$(at 0 1 0)" r0); alter "$(CURG)"/WEDNESDAY/sub/f*.txt "$(CURG)/WEDNESDAY/a.txt" "$(CURG)/WEDNESDAY/sub/b.txt"
for f in "$(CURG)"/P2/g2.txt "$(CURG)"/P2/g3.txt "$(CURG)"/P2/g4.txt "$(CURG)"/P2/g5.txt "$(CURG)"/P2/g6.txt; do alter "$f"; done
# set P2: 5 of 6 altered; whether its 1-file sample hits the one good file is chance, so say what happened
rc=$(run "$(at 1 1 0)" r1); say "  rc=$rc GOOD=$(good r1) ; set 1 all altered -> full read-back lines: $(/usr/bin/grep -c -F 'FULL READ-BACK' "$T/o/r1.txt") ; set P2 files still wrong after the run: $(n=0; for i in 1 2 3 4 5 6; do cmp -s "$T/vol/P2/g$i.txt" "$(CURG)/P2/g$i.txt" || n=$((n+1)); done; echo $n) of 5 altered (P2's own sample of 1 decides)"
say "== 3d. a destination copy MISSING or of ANOTHER SIZE while the index holds its proof: is the set's trust withdrawn, is it said?"
fixture miss; for i in $(seq 1 20); do printf 'filler %05d\n' "$i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done; CONF_SAMPLE=0; std_conf; x=$(run "$(at 0 1 0)" r0)
mkdir -p "$T/held"; mv "$(CURG)/WEDNESDAY/sub/f1.txt" "$T/held/"; echo "short" > "$(CURG)/WEDNESDAY/sub/f2.txt"; alter "$(CURG)"/WEDNESDAY/sub/f1?.txt
rc=$(run "$(at 1 1 0)" r1); say "  1 destination file removed, 1 truncated, 10 altered same-size, sample off: rc=$rc GOOD=$(good r1) ; $(line r1 'to copy:' 1 70) ; read-back lines: $(/usr/bin/grep -c -F 'FULL READ-BACK' "$T/o/r1.txt") ; still wrong: $(stale)"
say "== 4. containment: a client folder THREE levels down; set= as ancestor of it; seat-named folders deeper"
fixture deep; mkdir -p "$T/vol/A/B/C/Datasec/proj" "$T/vol/A/B/C/plain" "$T/vol/A/B/tuesday-seat/x" "$T/vol/A/B/Friday"; echo "DS-MARK" > "$T/vol/A/B/C/Datasec/proj/d.txt"; echo ok > "$T/vol/A/B/C/plain/p.txt"; echo "TUE-MARK" > "$T/vol/A/B/tuesday-seat/x/t.txt"; echo "FRI-MARK" > "$T/vol/A/B/Friday/f.txt"
std_conf "set=General|A|$T/vol/A"
rc=$(run "$(at 0 1 0)" r); say "  set= the ancestor A (roots sit 3 and 4 levels down): rc=$rc GOOD=$(good r) $(line r REFUSED 1 90)"
say "    on the NAS: Datasec mark $(/usr/bin/grep -r -l -F DS-MARK "$T/nas" 2>&1 | wc -l | tr -d ' '), tuesday-seat mark $(/usr/bin/grep -r -l -F TUE-MARK "$T/nas" 2>&1 | wc -l | tr -d ' '), Friday mark $(/usr/bin/grep -r -l -F FRI-MARK "$T/nas" 2>&1 | wc -l | tr -d ' '), plain neighbour $(find "$T/nas" -name p.txt | wc -l | tr -d ' ')"
fixture deep2; mkdir -p "$T/vol/A/B/C/Datasec/proj"; echo "DS-MARK" > "$T/vol/A/B/C/Datasec/proj/d.txt"
for src in "$T/vol/A/B/C/Datasec" "$T/vol/A/B/C/Datasec/proj" "$T/vol/A/B/C/../C/Datasec/proj" "$T/vol/A/B/C/DATASEC/proj"; do std_conf "set=General|X|$src"; rc=$(run "$(at 0 1 0)" r); say "  set=$(echo "$src" | sed "s|$T/vol/||"): rc=$rc ; Datasec mark on NAS: $(/usr/bin/grep -r -l -F DS-MARK "$T/nas" 2>&1 | wc -l | tr -d ' ')"; done
date; uptime
