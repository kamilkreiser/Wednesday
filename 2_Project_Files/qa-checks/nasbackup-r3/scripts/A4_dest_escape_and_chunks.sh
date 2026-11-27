#!/bin/bash
# A4 — writes outside the seat's destination folder through a symlink planted at the destination; A6 — the chunked engine:
# odd names, versions/ collisions within a run and across two runs, SIGKILL / SIGTERM mid-chunk, what the resume trusts.
. "$(dirname "$0")/lib3.sh"; date; uptime
snap() { find "$1" -type f -exec shasum -a 256 {} + 2>&1 | sort | shasum -a 256 | cut -c1-16; }
say "== A4a current/<set> is a SYMLINK to a folder outside the seat's destination"
fixture e1; mkdir -p "$T/nas/General/Wednesday/nightly-backup/current" "$T/nas/General/SomeoneElse"; echo "theirs" > "$T/nas/General/SomeoneElse/keep.txt"
ln -s "$T/nas/General/SomeoneElse" "$T/nas/General/Wednesday/nightly-backup/current/WEDNESDAY"
say "  rc=$(run "$(at 0 1 0)" r) GOOD=$(good r) refused: $(line r REFUSED 1 160)"
say "  files now in the OUTSIDE folder: $(ls "$T/nas/General/SomeoneElse" | tr '\n' ' ')"
say "== A4b the seat folder itself (<NAS>/General/Wednesday) is a symlink to another client's folder"
fixture e2; mkdir -p "$T/nas/Datasec/x"; ln -s "$T/nas/Datasec/x" "$T/nas/General/Wednesday"
say "  rc=$(run "$(at 0 1 0)" r) GOOD=$(good r) refused: $(line r REFUSED 1 160)"
say "  entries now under nas/Datasec/x: $(find "$T/nas/Datasec/x" | wc -l | tr -d ' ') (1 = only itself)"
say "== A4c a symlinked SUBFOLDER inside current/<set> (sub -> outside), source has sub/b.txt changed"
fixture e3; say "  night1 rc=$(run "$(at 0 1 0)" r0)"; mkdir -p "$T/nas/outside" "$T/held"; echo "theirs" > "$T/nas/outside/b.txt"
mv "$(CURG)/WEDNESDAY/sub" "$T/held/sub"; ln -s "$T/nas/outside" "$(CURG)/WEDNESDAY/sub"; echo "b changed, longer" > "$T/vol/WEDNESDAY/sub/b.txt"
say "  night2 rc=$(run "$(at 1 1 0)" r1) GOOD=$(good r1); outside/b.txt now: $(cat "$T/nas/outside/b.txt"); sub is: $(stat -f '%HT' "$(CURG)/WEDNESDAY/sub")"
say "    problems: $(line r1 '  - ' 2 200)"
say "== A4d versions/ is a symlink to outside; a changed file's old copy would be written through it"
fixture e4; say "  night1 rc=$(run "$(at 0 1 0)" r0)"; mkdir -p "$T/nas/outside2" "$T/held"; mv "$(VERG)" "$T/held/versions"; ln -s "$T/nas/outside2" "$(VERG)"; echo "a changed, longer" > "$T/vol/WEDNESDAY/a.txt"
say "  night2 rc=$(run "$(at 1 1 0)" r1) GOOD=$(good r1); files now under outside2: $(find "$T/nas/outside2" -type f | wc -l | tr -d ' ')"

say "== A6a odd names in one chunk list: newline, leading dash, glob characters, trailing space, backslash, leading #, ;"
fixture n1; W="$T/vol/WEDNESDAY/odd"; mkdir -p "$W" "$W/-dashdir" "$W/sp end "
"$PY" -c 'import os,sys
d=sys.argv[1]
names=["line1\nline2.txt","-leading-dash","--delete","--remove-source-files","*","[a-z]*.txt","?","trailing space ","back\\slash","#hash",";semi","tab\there","\r.txt","-dashdir/--inplace","sp end /x ","a\x7fb","emoji-\U0001F600.txt","é-nfd.txt"]
for n in names: open(os.path.join(d,n),"w").write("ODD "+repr(n))
print(len(names))' "$W" > "$T/o/planted.txt" 2>&1
CONF_CHUNK=4; std_conf
rc=$(run "$(at 0 1 0)" r); say "  planted $(cat "$T/o/planted.txt") odd names; rc=$rc GOOD=$(good r); chunks: $(/usr/bin/grep -c -F 'engine pass' "$T/o/r.txt"); deleting lines>0: $(/usr/bin/grep -F 'engine pass' "$T/o/r.txt" | /usr/bin/grep -c -v -F 'deleting lines: 0')"
say "  source files $(find "$T/vol/WEDNESDAY" -type f | wc -l | tr -d ' ') ; destination files $(find "$(CURG)/WEDNESDAY" -type f | wc -l | tr -d ' ') ; content diff: $(diff -r "$T/vol/WEDNESDAY" "$(CURG)/WEDNESDAY" 2>&1 | wc -l | tr -d ' ') lines"
say "  first problem (if any): $(line r '  - ' 1 220)"
say "  engine argument lists the tool built (distinct option words over all calls): $(/usr/bin/grep -h -F 'engine:' "$T/o/r.txt" | tr ' ' '\n' | /usr/bin/grep -E '^-' | sed -E 's/=.*//' | sort -u | tr '\n' ' ')"

say "== A6b versions/: the same file replaced by chunk passes and by TWO runs in one night: is any earlier copy overwritten?"
fixture v1; for i in 1 2 3 4 5 6 7 8 9 10 11 12; do echo "v0 file $i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done; CONF_CHUNK=3; std_conf
say "  run0 rc=$(run "$(at 0 1 0)" r0)"
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do echo "v1 file $i longer" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
CONF_RSYNC="$(mk_stub moves 'if [ "$N" -le 6 ]; then "$REAL" "$@"; rc=$?; echo "v-during pass $N" >> "$V/sub/f1.txt"; exit $rc; fi; exec "$REAL" "$@"')"; std_conf
say "  run1 (f1 changes after each of the first engine calls) rc=$(run "$(at 0 1 10)" r1) GOOD=$(good r1) resent: $(line r1 're-sent because' 1 200 | sed 's/.*tonight, //;s/ because.*//')"
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do echo "v2 file $i longer still" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done; CONF_RSYNC=""; std_conf
say "  run2 the same night rc=$(run "$(at 0 1 20)" r2) GOOD=$(good r2)"
say "  version folders: $(ls "$(VERG)" | tr '\n' ' ')"
for want in "v0 file 1" "v1 file 1 longer" "v0 file 7" "v1 file 7 longer"; do say "    copies whose first line is exactly '$want' kept under versions/: $(/usr/bin/grep -r -l -x -F "$want" "$(VERG)" 2>&1 | wc -l | tr -d ' ')"; done
say "    distinct contents of sub/f1.txt kept under versions/: $(find "$(VERG)" -name f1.txt -exec shasum -a 256 {} + | cut -c1-64 | sort -u | wc -l | tr -d ' ') in $(find "$(VERG)" -name f1.txt | wc -l | tr -d ' ') files"

say "== A6c SIGKILL of the tool in chunk 3 of 5 (the engine hangs); then what the next run trusts"
fixture k9; for i in $(seq 1 23); do echo "payload $i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
CONF_RSYNC="$(mk_stub hang3 'if [ "$N" -ge 3 ]; then sleep 8; fi; exec "$REAL" "$@"')"; CONF_CHUNK=5; std_conf
nb --run --now "$(at 0 1 0)" > "$T/o/bg.txt" 2>&1 & BG=$!
i=0; while [ "$i" -lt 100 ]; do [ -f "$T/stub/calls" ] && [ "$(cat "$T/stub/calls")" -ge 3 ] && break; sleep 0.2; i=$((i+1)); done; sleep 1
TP="$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1]))["pid"])' "$T/lane/state/wednesday.lock.d/owner.json")"; kill -KILL "$TP"; wait "$BG" 2>&1
say "  after SIGKILL: index rows=$(idxrows) state.last_attempt=$(state last_attempt.status) last_good=$(state last_good) COMPLETE=$(completed) lock left=$([ -d "$T/lane/state/wednesday.lock.d" ] && echo yes || echo no) files at destination=$(find "$(CURG)" -type f | wc -l | tr -d ' ')"
CONF_RSYNC=""; std_conf
say "  a new run while the orphan engine lives: rc=$(run "$(at 0 1 5)" r1) $(line r1 REFUSED 1 110)"
sleep 9
say "  orphan ended; files at destination now=$(find "$(CURG)" -type f | wc -l | tr -d ' ') index rows=$(idxrows); clear-stale-lock rc=$(nb --clear-stale-lock > "$T/o/c.txt" 2>&1; echo $?)"
# corrupt ONE file the orphan delivered (same size) to see whether the resume re-proves or trusts
ORPH="$(CURG)/WEDNESDAY/sub/f18.txt"; [ -f "$ORPH" ] || ORPH="$(ls "$(CURG)"/WEDNESDAY/sub/f*.txt | tail -1)"
"$PY" -c 'import sys,os; p=sys.argv[1]; n=os.path.getsize(p); open(p,"wb").write(b"Z"*n)' "$ORPH"
say "  altered behind the tool (delivered by the orphan, no index row): $(basename "$ORPH")"
say "  resume rc=$(run "$(at 0 1 30)" r2) GOOD=$(good r2); $(line r2 'to copy:' 1 80); $(line r2 'compared by sha256' 1 110)"
say "  after the resume: source and destination differ in $(diff -r "$T/vol/WEDNESDAY" "$(CURG)/WEDNESDAY" 2>&1 | wc -l | tr -d ' ') lines; the altered content is kept in versions/: $(/usr/bin/grep -r -l -F ZZZZ "$(VERG)" 2>&1 | wc -l | tr -d ' ') file"
date; uptime
