#!/bin/bash
# A3 — REDO of A10-KILL and A11. The first attempt (A2, kept as *.FLAWED-first-run.out) built its "big" files from
# a 5-byte pattern * 70000 = 350 KB, not the 1 MB / 2.5 MB intended, so SIGKILL arrived after the copy had finished
# and the 12 MB image never filled. Here the files are exact-size and incompressible.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
run() { nb --run --now "$1" > "$T/out/$2.txt" 2>&1; echo $?; }
tailmsg() { /usr/bin/grep -E 'GOOD:|FAILED|PROBLEM|  - |REFUSED|Traceback|Error' "$T/out/$1.txt" | head -8 | cut -c1-300; }
mkbig() { "$PY" -c 'import sys,random; r=random.Random(sys.argv[2]); n=int(sys.argv[3]); m=sys.argv[2].encode(); open(sys.argv[1],"wb").write(m+bytes(r.getrandbits(8) for _ in range(n-len(m))))' "$1" "$2" "$3"; }
slow_stub() { local f="$T/stub/rsync_slow"; { echo '#!/bin/bash'; echo "REAL=$REAL_RSYNC"
  echo 'for a in "$@"; do if [ "$a" = "--version" ]; then exec "$REAL" --version; fi; done'
  echo 'exec "$REAL" --bwlimit=250 "$@"'; } > "$f"; chmod +x "$f"; echo "$f"; }
nv() { /usr/bin/grep -l -r -a "$1" "$2" 2>/dev/null | wc -l | tr -d ' '; }

say "### A10-KILL (redo) SIGKILL of the tool mid-copy; is the engine orphaned and still writing?"
fixture A10KILLb; for i in 1 2 3 4 5; do mkbig "$T/vol/WEDNESDAY/big$i.bin" "v1-$i-" 1000000; done
ls -l "$T/vol/WEDNESDAY/big1.bin" | awk '{print "size of big1.bin:", $5}'
rc=$(run "$(at 0 1 0)" r1); verdict "first run rc" 0 "$rc"; snap a
for i in 1 2 3 4 5; do mkbig "$T/vol/WEDNESDAY/big$i.bin" "v2-$i-" 1000001; done
CONF_RSYNC="$(slow_stub)"; write_conf
nb --run --now "$(at 1 1 0)" > "$T/out/r2.txt" 2>&1 &
sleep 7
PIDS="$(pgrep -f "nb_core.py backup --seat wednesday --tree $T/")"
say "at 7 s: python pid $PIDS ; rsync procs $(pgrep -f "rsync.*$T/" | wc -l | tr -d ' ') ; current v2 files $(nv 'v2-' "$(CUR)") of 5"
kill -KILL $PIDS; sleep 2; wait 2>/dev/null
say "2 s after SIGKILL: rsync procs STILL RUNNING: $(pgrep -f "rsync.*$T/" | wc -l | tr -d ' ') ; current v2 files $(nv 'v2-' "$(CUR)") ; lock present: $([ -d "$T/lane/state/wednesday.lock.d" ] && echo yes || echo no) ; state=$(state last_attempt.status)"
rc=$(run "$(at 1 2 0)" r3); say "an immediate rerun: rc=$rc ($(tailmsg r3 | cut -c1-60))"
nb --clear-stale-lock > "$T/out/clr.txt" 2>&1; say "--clear-stale-lock WHILE the orphan engine is still running: rc=$? ; rsync procs now: $(pgrep -f "rsync.*$T/" | wc -l | tr -d ' ')"
CONF_RSYNC=""; write_conf
rc=$(run "$(at 1 3 0)" r4); say "rerun beside the orphan: rc=$rc"; tailmsg r4
sleep 22; say "22 s later: rsync procs: $(pgrep -f "rsync.*$T/" | wc -l | tr -d ' ')"
lost a | tail -2; verdict "A10-KILL nothing lost" 0 "${PIPESTATUS[0]}"
verdict "A10-KILL all 5 current are v2" 5 "$(nv 'v2-' "$(CUR)")"; verdict "A10-KILL all 5 v1 kept under versions/" 5 "$(nv 'v1-' "$(VER)")"
say "versions tree:"; find "$(VER)" -type f | sed "s|$T/nas/General/Wednesday/nightly-backup/||" | sort
say "temp leftovers: $(find "$T/nas" -path '*_tmp_incoming*' -type f | wc -l | tr -d ' ')"
rc=$(run "$(at 2 1 0)" r5); say "next night rc=$rc, to copy: $(/usr/bin/grep -m1 'to copy:' "$T/out/r5.txt" | cut -c1-40)"

say; say "### A11 (redo) a FULL destination: 12 MB HFS+ image"
T="$S/fx/IMG2"; mkdir -p "$T/vol/WEDNESDAY" "$T/vol/CODING/Secuura" "$T/nas/Secuura" "$T/nas/General" "$T/lane/seats" "$T/out" "$T/stub"
echo 5000 > "$T/free_gib.txt"; CONF_STATUS=confirmed; CONF_RSYNC=""; write_conf; write_mounts
for i in 1 2 3; do mkbig "$T/vol/WEDNESDAY/full$i.bin" "v1-$i-" 2500000; done
rc=$(run "$(at 0 1 0)" f1); verdict "A11 first run rc (7.5 MB into 12 MB)" 0 "$rc"; snap full; df -k "$T/nas" | tail -1 | awk '{print "used KB", $3, "avail KB", $4}'
for i in 1 2 3; do mkbig "$T/vol/WEDNESDAY/full$i.bin" "v2-$i-" 2500001; done
rc=$(run "$(at 1 1 0)" f2); say "A11 second run rc=$rc"; tailmsg f2; /usr/bin/grep -m2 -i 'engine stderr' "$T/out/f2.txt" | cut -c1-260; df -k "$T/nas" | tail -1 | awk '{print "used KB", $3, "avail KB", $4}'
lost full | tail -2; verdict "A11 nothing lost on a full destination" 0 "${PIPESTATUS[0]}"
say "A11 state: last_attempt=$(state last_attempt.status) last_good=$(state last_good.time_local)"
say "A11 current/: v1 $(nv 'v1-' "$(CUR)"), v2 $(nv 'v2-' "$(CUR)"); versions/: v1 $(nv 'v1-' "$(VER)"); temp leftovers $(find "$T/nas" -path '*_tmp_incoming*' -type f | wc -l | tr -d ' ') ($(find "$T/nas" -path '*_tmp_incoming*' -type f -exec stat -f %z {} + | tr '\n' ' ')bytes)"
rc=$(run "$(at 2 1 0)" f3); say "A11 the NEXT night on the still-full disk rc=$rc"; lost full | tail -1; say "temp leftovers now $(find "$T/nas" -path '*_tmp_incoming*' -type f | wc -l | tr -d ' ')"
