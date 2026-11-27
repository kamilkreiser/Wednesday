#!/bin/bash
# N3/N4/N5 — the index, the shrink guard, the conf END marker. Fresh checker, 2026-11-27. Fake NAS only.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib2.sh"
W() { echo "$T/vol/WEDNESDAY"; }
many() { for i in $(seq 1 "$1"); do printf 'filler %05d\n' "$i" > "$(W)/sub/f$i.txt"; done; }

say "### N3a a destination file DELETED behind the tool's back (index still says proven). Expected: noticed the next night, re-sent."
fixture N3a; many 20; rc=$(run "$(at 0 1 0)" r0); mkdir -p "$T/held"; mv "$(CUR)/sub/f7.txt" "$T/held/"
rc=$(run "$(at 1 1 0)" r1); say "night 1 rc=$rc GOOD=$(good r1) | $(line r1 'to copy:' 1 60 | sed 's/^ *//') | f7 back at destination: $([ -f "$(CUR)/sub/f7.txt" ] && echo yes || echo NO)"

say; say "### N3b a destination file's CONTENT altered behind the tool's back, same size (bit rot, another writer). 400 unsent files, hash_sample=40 (the shipped default). How many nights until it is noticed?"
fixture N3b; many 400; sed -i '' 's/^hash_sample=10/hash_sample=40/' "$T/lane/seats/wednesday.conf"; rc=$(run "$(at 0 1 0)" r0)
printf 'FILLER 00123\n' > "$(CUR)/sub/f123.txt"
first=""; goodn=0; for n in $(seq 1 12); do rc=$(run "$(at $n 1 0)" r$n); if [ "$rc" = 0 ]; then goodn=$((goodn+1)); else [ -z "$first" ] && first=$n; fi; done
say "12 nights with nothing changed at the source: recorded GOOD on $goodn nights while the destination copy differed; first night it was caught: ${first:-never in 12} (expected chance per night 40/402 = 10%)"
say "   the catching night said: $( [ -n "$first" ] && line r$first 'sha256 sample' 1 200 | sed 's/^ *//')"

say; say "### N3c the index file is damaged (garbage bytes). Expected: one plain line, not a traceback; the lock not left behind."
fixture N3c; rc=$(run "$(at 0 1 0)" r0); for k in 1 2 3 4 5 6 7 8 9 10 11 12; do echo 'this is not a sqlite database at all, just bytes'; done > "$T/lane/state/wednesday.index.sqlite"
rc=$(run "$(at 1 1 0)" r1); say "night 1 rc=$rc GOOD=$(good r1) | traceback lines: $(/usr/bin/grep -c -F 'Traceback' "$T/out/r1.txt") | last line: $(tail -1 "$T/out/r1.txt" | cut -c1-160)"
say "   lock left behind: $([ -d "$T/lane/state/wednesday.lock.d" ] && echo YES || echo no) | state last_attempt=$(state last_attempt.status)"
rc=$(run "$(at 1 2 0)" r1b); say "   the next attempt: rc=$rc | $(/usr/bin/grep -F -e 'STALE' -e 'Traceback' "$T/out/r1b.txt" | head -1 | cut -c1-120)"
rc=$(watch --check --now "$(at 1 3 0)" > "$T/out/w.txt" 2>&1; echo $?); say "   watch: rc=$rc $(head -1 "$T/out/w.txt" | cut -c1-200)"
nb --dry > "$T/out/dry.txt" 2>&1; say "   a DRY run with the damaged index: rc=$? traceback lines: $(/usr/bin/grep -c -F 'Traceback' "$T/out/dry.txt")"

say; say "### N3d an index from ANOTHER destination: the whole destination is replaced by same-size different content; the index is kept."
fixture N3d; many 30; rc=$(run "$(at 0 1 0)" r0)
find "$(CUR)" -type f -name 'f*.txt' | while IFS= read -r f; do n=$(basename "$f" .txt); printf 'FILLER %05d\n' "${n#f}" > "$f"; done
rc=$(run "$(at 1 1 0)" r1); say "night 1 rc=$rc GOOD=$(good r1) | $(line r1 'sha256 sample' 1 200 | sed 's/^ *//') | NOT DELIVERED lines: $(/usr/bin/grep -c -F 'NOT DELIVERED: ' "$T/out/r1.txt") of 30 altered"
rc=$(run "$(at 2 1 0)" r2); say "night 2 rc=$rc GOOD=$(good r2) | still-altered destination files: $(/usr/bin/grep -r -l -F 'FILLER' "$(CUR)" | wc -l | tr -d ' ')"
for n in 3 4 5 6; do rc=$(run "$(at $n 1 0)" r$n); done; say "night 6 rc=$rc | still-altered destination files after 6 nights: $(/usr/bin/grep -r -l -F 'FILLER' "$(CUR)" | wc -l | tr -d ' ')"

say; say "### N4a the shrink guard and the nightly job: can the nightly job accept a shrink? can a shrink be accepted twice?"
fixture N4a; many 40; rc=$(nightly --now "$(at 0 0 31)" > "$T/out/n0.txt" 2>&1; echo $?); say "night 0 (nightly) rc=$rc"
mkdir -p "$T/held"; for i in $(seq 1 35); do mv "$(W)/sub/f$i.txt" "$T/held/"; done
rc=$(nightly --now "$(at 1 0 31)" > "$T/out/n1.txt" 2>&1; echo $?); say "night 1 (nightly) after 42 -> 7 files: rc=$rc | $(/usr/bin/grep -F 'SCOPE FELL' "$T/out/n1.txt" | head -1 | cut -c1-170 | sed 's/^ *//')"
rc=$(nightly --now "$(at 2 0 31)" > "$T/out/n2.txt" 2>&1; echo $?); say "night 2 (nightly) unchanged: rc=$rc (still failing: the nightly job has no way to accept)"
say "   accept-shrink in the nightly script or the plist template: $(/usr/bin/grep -c -i 'accept' "$LANE/nas_backup_nightly.sh") / $(/usr/bin/grep -c -i 'accept' "$LANE/jobs/nasbackup.plist.template") (control: 'decide-only' in the nightly script: $(/usr/bin/grep -c -i 'decide-only' "$LANE/nas_backup_nightly.sh"))"
rc=$(nb --run --now "$(at 2 1 0)" --accept-shrink card-shrink-0001 > "$T/out/a1.txt" 2>&1; echo $?); say "by hand with --accept-shrink: rc=$rc GOOD=$(good a1) ; new baseline: $(state last_good.set_counts)"
for i in 36 37 38 39; do mv "$(W)/sub/f$i.txt" "$T/held/"; done
rc=$(run "$(at 3 1 0)" a2); say "a FURTHER sharp fall the next night, no flag: rc=$rc ($(/usr/bin/grep -c -F 'SCOPE FELL' "$T/out/a2.txt") SCOPE FELL line: the acceptance was not sticky)"

say; say "### N4b a SLOW shrink, 45% of what is left each night (below the 50% trigger)."
fixture N4b; many 1000; rc=$(run "$(at 0 1 0)" r0); mkdir -p "$T/held"; left=1000; n=0; allgood=1
while [ "$left" -gt 3 ] && [ "$n" -lt 14 ]; do n=$((n+1)); take=$((left*45/100)); [ "$take" -lt 1 ] && take=1
  ls "$(W)/sub" | /usr/bin/grep '^f' | head -"$take" | while IFS= read -r f; do mv "$(W)/sub/$f" "$T/held/"; done; left=$((left-take))
  rc=$(run "$(at $n 1 0)" r$n); [ "$rc" = 0 ] || allgood=0; printf '   night %s: %s filler files left, rc=%s GOOD=%s\n' "$n" "$left" "$rc" "$(good r$n)"; done
say "1000 -> $left files in $n nights, every night GOOD: $([ $allgood = 1 ] && echo YES || echo no)"

say; say "### N4c FIRST run of a set that holds folders but ZERO files (ruling 4: 'a set whose in-scope count is zero FAILS')."
fixture N4c; mkdir -p "$T/held"; mv "$(W)/a.txt" "$(W)/sub/b.txt" "$T/held/"; mkdir -p "$(W)/sub/deeper"
rc=$(run "$(at 0 1 0)" r0); say "rc=$rc GOOD=$(good r0) | $(line r0 'source in scope' 1 80 | sed 's/^ *//') | EMPTY SCOPE lines: $(/usr/bin/grep -c -F 'EMPTY SCOPE' "$T/out/r0.txt")"
say "CONTROL the same with no folders either: $(fixture N4c2; mv "$(W)/a.txt" "$T/"; mv "$(W)/sub" "$T/subaside"; rc=$(run "$(at 0 1 0)" r0); echo "rc=$rc EMPTY SCOPE lines: $(/usr/bin/grep -c -F 'EMPTY SCOPE' "$T/out/r0.txt")")"

say; say "### N4d exclusion patterns that are not literally '*' but match (nearly) every name, on a FIRST run and after a good run."
for pat in '*.*' '[!~]*' '*[a-z0-9]*' '?*' '**'; do fixture "N4d_$RANDOM"; many 20; write_conf "exclude_name=$pat"
  rc=$(run "$(at 0 1 0)" r0); printf '   first run, exclude_name=%-12s rc=%s GOOD=%s | %s\n' "$pat" "$rc" "$(good r0)" "$( { line r0 'source in scope' 1 60; line r0 'REFUSED' 1 90; } | sed 's/^ *//' | head -1)"; done
fixture N4d2; many 20; rc=$(run "$(at 0 1 0)" r0); write_conf 'exclude_name=*.*'; rc=$(run "$(at 1 1 0)" r1); say "   after a good 22-file night, exclude_name=*.* : rc=$rc GOOD=$(good r1) | $(/usr/bin/grep -F -e 'SCOPE FELL' -e 'EMPTY SCOPE' "$T/out/r1.txt" | head -1 | cut -c1-120 | sed 's/^ *//')"
fixture N4d3; many 20; rc=$(run "$(at 0 1 0)" r0); write_conf 'exclude_name=*.*' 'max_drop_fraction=1'; rc=$(run "$(at 1 1 0)" r1); say "   the same with max_drop_fraction=1 in the conf: rc=$rc GOOD=$(good r1) (the conf can switch the fall guard off; the zero rule remains)"
fixture N4d4; many 20; rc=$(run "$(at 0 1 0)" r0); write_conf 'exclude_name=f*'; echo '{"truncated' > "$T/lane/state/wednesday.json"; rc=$(run "$(at 1 1 0)" r1); say "   state file damaged AND 20 of 22 files newly excluded the same night: rc=$rc GOOD=$(good r1) (the baseline went with the damaged state) | $(line r1 'STATE FILE DAMAGED' 1 60)"

say; say "### N4e a set that GROWS by pulling in an unintended tree (5,000 files appear under the seat tree overnight)."
fixture N4e; many 20; rc=$(run "$(at 0 1 0)" r0); mkdir -p "$(W)/2_Project_Files/someone-elses-clone"; for i in $(seq 1 5000); do echo "$i" > "$(W)/2_Project_Files/someone-elses-clone/c$i.txt"; done
rc=$(run "$(at 1 1 0)" r1); say "rc=$rc GOOD=$(good r1) | $(line r1 'to copy:' 1 60 | sed 's/^ *//') | lines warning about growth: $(/usr/bin/grep -c -i -E 'grew|growth|rose' "$T/out/r1.txt")"

say; say "### N5a the END marker counts lines, it does not seal them: one exclude line REPLACED by another valid line, count unchanged."
fixture N5a; mkdir -p "$(W)/cache/huge"; printf 'BULK-MARK-5a\n' > "$(W)/cache/huge/blob.bin"; write_conf "exclude_path=WEDNESDAY|cache/huge"
rc=$(run "$(at 0 1 0)" r0); say "intact: rc=$rc bulk marker on NAS=$(onnas 'BULK-MARK-5a')"
fixture N5a2; mkdir -p "$(W)/cache/huge"; printf 'BULK-MARK-5a\n' > "$(W)/cache/huge/blob.bin"; write_conf "exclude_path=WEDNESDAY|cache/huge"
sed -i '' 's#^exclude_path=WEDNESDAY|cache/huge#io_timeout=1800#' "$T/lane/seats/wednesday.conf"
rc=$(run "$(at 0 1 0)" r0); say "exclude line replaced by 'io_timeout=1800' (END count untouched): rc=$rc GOOD=$(good r0) bulk marker on NAS=$(onnas 'BULK-MARK-5a')"
say; say "### N5b duplicate keys: which wins, and is it said?"
fixture N5b; { /usr/bin/grep -v '^END ' "$T/lane/seats/wednesday.conf"; echo "status=unconfirmed"; } > "$T/c.tmp"; mv "$T/c.tmp" "$T/lane/seats/wednesday.conf"; seal_conf "$T/lane/seats/wednesday.conf"
rc=$(run "$(at 0 1 0)" r0); say "status=confirmed then status=unconfirmed: rc=$rc ($(line r0 'not confirmed' 1 70))"
fixture N5b2; { echo "status=unconfirmed"; /usr/bin/grep -v '^END ' "$T/lane/seats/wednesday.conf"; } > "$T/c.tmp"; mv "$T/c.tmp" "$T/lane/seats/wednesday.conf"; seal_conf "$T/lane/seats/wednesday.conf"
rc=$(run "$(at 0 1 0)" r0); say "status=unconfirmed then status=confirmed: rc=$rc GOOD=$(good r0) | duplicate-key warnings: $(/usr/bin/grep -c -i 'duplicate\|twice\|more than once' "$T/out/r0.txt")"
say; say "### N5c an exclude_path that exists but is the WRONG folder (sub instead of cache/huge)."
fixture N5c; mkdir -p "$(W)/cache/huge"; printf 'BULK-MARK-5c\n' > "$(W)/cache/huge/blob.bin"; write_conf "exclude_path=WEDNESDAY|sub"
rc=$(run "$(at 0 1 0)" r0); say "rc=$rc GOOD=$(good r0) bulk marker on NAS=$(onnas 'BULK-MARK-5c') ; sub/b.txt at destination: $([ -f "$(CUR)/sub/b.txt" ] && echo yes || echo NO) (accepted by nature: the tool cannot know intent)"
say; say "### N5d text after the END marker, and an END marker in the middle"
fixture N5d; echo "exclude_name=zzz" >> "$T/lane/seats/wednesday.conf"; rc=$(run "$(at 0 1 0)" r0); say "a line appended after END: rc=$rc ($(line r0 'REFUSED' 1 110))"
say; say "### N5e the state file: valid JSON with a last_good in the FUTURE (a wrong clock during one good run)"
fixture N5e; rc=$(run "$(at 0 1 0)" r0); /opt/homebrew/bin/python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["last_good"]["time"]+=86400*400; json.dump(d,open(p,"w"))' "$T/lane/state/wednesday.json"
rc=$(nightly --now "$(at 5 0 31)" --decide-only > "$T/out/n.txt" 2>&1; echo $?); say "nightly 5 days later: $(head -1 "$T/out/n.txt" | cut -c1-150)"
rc=$(watch --check --now "$(at 9 9 0)" > "$T/out/w.txt" 2>&1; echo $?); say "watch 9 days later: rc=$rc $(head -1 "$T/out/w.txt" | cut -c1-120)"
say; say "### N5f the state file: valid JSON, right seat, but last_good without its fields"
fixture N5f; rc=$(run "$(at 0 1 0)" r0); echo '{"seat": "wednesday", "last_good": {}, "recent_attempts": [{}]}' > "$T/lane/state/wednesday.json"
rc=$(watch --check --now "$(at 1 9 0)" > "$T/out/w.txt" 2>&1; echo $?); say "watch: rc=$rc traceback lines=$(/usr/bin/grep -c -F Traceback "$T/out/w.txt") | $(tail -1 "$T/out/w.txt" | cut -c1-100)"
echo '{"seat": "wednesday", "last_good": {"note": "x"}, "recent_attempts": []}' > "$T/lane/state/wednesday.json"
rc=$(nightly --now "$(at 1 0 31)" > "$T/out/n.txt" 2>&1; echo $?); say "nightly with last_good lacking 'time': rc=$rc traceback lines=$(/usr/bin/grep -c -F Traceback "$T/out/n.txt") | $(tail -1 "$T/out/n.txt" | cut -c1-100)"
rc=$(watch --check --now "$(at 1 9 0)" > "$T/out/w2.txt" 2>&1; echo $?); say "watch on it: rc=$rc traceback lines=$(/usr/bin/grep -c -F Traceback "$T/out/w2.txt") | $(tail -1 "$T/out/w2.txt" | cut -c1-100)"
