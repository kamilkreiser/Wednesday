#!/bin/bash
# N1x — the coordinator's exact question (ANSWER-3): can a WHOLE source going unreadable mid-run make every file
# "gone" and the run GOOD? Three shapes, each with the stub acting BEFORE the real engine is called for that set.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib2.sh"
W() { echo "$T/vol/WEDNESDAY"; }
fill() { mkdir -p "$(W)/a" "$(W)/b"; for i in $(seq 1 20); do echo "payload-A $i" > "$(W)/a/f$i.txt"; echo "payload-B $i" > "$(W)/b/g$i.txt"; done; }
report() { say "$1: rc=$rc GOOD=$(good r0) | at destination: $(find "$(CUR)" -type f 2>/dev/null | wc -l | tr -d ' ') of 42 files | $(line r0 'engine pass 1' 1 60 | sed 's/^ *//') | $(/usr/bin/grep -o -E 'proven at the destination: [0-9]+ of [0-9]+|gone from the source during the run: [0-9]+|NOT PROVEN: [0-9]+' "$T/out/r0.txt" | head -3 | tr '\n' ';') state=$(state last_attempt.status)"; }
say "### (1) the set's ROOT folder itself becomes mode 000 (the engine cannot enter it at all)"
fixture N1x1; fill; CONF_RSYNC="$(mkstub s1 'case "$DEST" in */current/WEDNESDAY/) chmod 000 "$T2/vol/WEDNESDAY";; esac; "$REAL" "$@"; rc=$?; chmod 755 "$T2/vol/WEDNESDAY"; exit $rc')"; write_conf; rc=$(run "$(at 0 1 0)" r0); report "root 000 during the copy, readable again by the proof"
fixture N1x2; fill; CONF_RSYNC="$(mkstub s2 'case "$DEST" in */current/WEDNESDAY/) chmod 000 "$T2/vol/WEDNESDAY";; esac; exec "$REAL" "$@"')"; write_conf; rc=$(run "$(at 0 1 0)" r0); chmod 755 "$(W)"; report "root 000 from the copy to the end of the run"
say "### (2) EVERY top-level folder of the set becomes mode 000 (the root is enterable, nothing under it is readable)"
fixture N1x3; fill; CONF_RSYNC="$(mkstub s3 'case "$DEST" in */current/WEDNESDAY/) chmod 000 "$T2/vol/WEDNESDAY/a" "$T2/vol/WEDNESDAY/b" "$T2/vol/WEDNESDAY/sub"; chmod 000 "$T2/vol/WEDNESDAY/a.txt";; esac; exec "$REAL" "$@"')"; write_conf; rc=$(run "$(at 0 1 0)" r0); chmod 755 "$(W)/a" "$(W)/b" "$(W)/sub"; chmod 644 "$(W)/a.txt"; report "every folder and file under the root unreadable"
say "### (3) the same on a LATER night, after a good first night, with every file changed (so every file is to be sent)"
fixture N1x4; fill; rc=$(run "$(at 0 1 0)" r0); say "night 0: rc=$rc GOOD=$(good r0)"; sleep 1; for f in "$(W)"/a/*.txt "$(W)"/b/*.txt; do echo "changed overnight" >> "$f"; done
CONF_RSYNC="$(mkstub s4 'case "$DEST" in */current/WEDNESDAY/) chmod 000 "$T2/vol/WEDNESDAY/a" "$T2/vol/WEDNESDAY/b";; esac; exec "$REAL" "$@"')"; write_conf; rc=$(nb --run --now "$(at 1 1 0)" > "$T/out/r1.txt" 2>&1; echo $?); chmod 755 "$(W)/a" "$(W)/b"
say "night 1: rc=$rc GOOD=$(good r1) | destination files still holding LAST night's content: $(/usr/bin/grep -r -L -F 'changed overnight' "$(CUR)/a" "$(CUR)/b" | wc -l | tr -d ' ') of 40 | $(/usr/bin/grep -o -E 'gone from the source during the run: [0-9]+|NOT PROVEN: [0-9]+' "$T/out/r1.txt" | head -2 | tr '\n' ';') state=$(state last_attempt.status) recorded src_files=$(state last_good.counts.src_files) vanished=$(state last_good.counts.vanished)"
rc=$(nb --run --now "$(at 2 1 0)" > "$T/out/r2.txt" 2>&1; echo $?); say "night 2 (folders readable again, real engine via the same stub now a no-op): rc=$rc GOOD=$(good r2) | still-stale destination files: $(/usr/bin/grep -r -L -F 'changed overnight' "$(CUR)/a" "$(CUR)/b" | wc -l | tr -d ' ')"
