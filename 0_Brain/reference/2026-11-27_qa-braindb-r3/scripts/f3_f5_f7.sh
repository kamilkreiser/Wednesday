#!/bin/bash
# f3_f5_f7.sh - NEW attacks: hard links / symlink swap (F3), locking and concurrency (F5), odd files (F7). Scratch only.
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-braindb-r3
PFC="$S/lanecopy/WEDNESDAY/2_Project_Files"; PGBIN=/opt/homebrew/opt/postgresql@15/bin; TOOL="$PFC/brain-db/braindb.sh"
W="$S/f357-$(date +%H%M%S)"; mkdir -p "$W" || exit 2
FIX="$W/fix"; python3 "$PFC/brain-db/tests/make_fixtures.py" "$FIX" > "$W/fx.out" 2>&1
SOCK=/tmp/qa3v; L="$FIX/0_Brain/learnings"
sh() { awk -v n="${1:-230}" '{print substr($0,1,n)}' | sed "s|$W/||g"; }
nprocs() { local snap; snap="$(ps -axww -o pid=,command=)"; printf '%s\n' "$snap" | /usr/bin/grep -F -c -- "-D $1"; }
X() { local pg="$1"; shift; env -u WED_AGENT BRAINDB_ROOT="${ROOT:-$FIX}" BRAINDB_PGDATA="$pg" BRAINDB_SOCKDIR="${SK:-$SOCK}" ${EXTRA:-} /bin/bash "$TOOL" "$@"; }
dumpc() { "$PGBIN/pg_dump" --data-only --schema=brain -h "${SK:-$SOCK}" -d braindb 2>/dev/null | /usr/bin/grep -c -F -- "$1"; }
hr() { echo; echo "######## $1"; }
echo "run dir $W ; $(date '+%Y-%m-%d %H:%M:%S %Z')"

hr "F3a a LEGITIMATE own file with link count 2 (a skill that someone hard-linked into a backup folder): skipped loudly?"
mkdir -p "$W/backup" "$FIX/4_Credentials"
printf '# legit skill\n\nzlegitskill words\n' > "$FIX/0_Brain/skills/legit-ritual.md"; ln "$FIX/0_Brain/skills/legit-ritual.md" "$W/backup/legit-ritual.md"
printf -- '---\ntier: W\n---\n# own lesson\n\nzlegitlesson\n' > "$L/2026-05-01_own-linked.md"; ln "$L/2026-05-01_own-linked.md" "$W/backup/own-linked.md"
X "$W/pg" rebuild > "$W/f3a.out" 2>&1; echo "rebuild rc=$?"
/usr/bin/grep -i -n -E 'hard link' "$W/f3a.out" | sh 200
echo "last line: $(tail -1 "$W/f3a.out")"
echo "in index: zlegitskill=$(dumpc zlegitskill) zlegitlesson=$(dumpc zlegitlesson) (control xneighbour01=$(dumpc xneighbour01))"
X "$W/pg" check > "$W/f3a-check.out" 2>&1; echo "check rc=$? ; does check mention the skipped hard links? lines naming 'hard link' or the files: $(/usr/bin/grep -i -c -E 'hard link|legit-ritual|own-linked' "$W/f3a-check.out")"; sh 160 < "$W/f3a-check.out"
X "$W/pg" search zlegitlesson 2>&1 | tail -2 | sh 200

hr "F3b symlink chain, and a symlink to a device"
printf '# secret\n\nzsecretchain\n' > "$FIX/4_Credentials/secret.md"
ln -s "$FIX/4_Credentials/secret.md" "$W/hop2.md"; ln -s "$W/hop2.md" "$W/hop1.md"; ln -s "$W/hop1.md" "$L/2026-05-02_chain.md"
ln -s /dev/zero "$L/2026-05-03_devzero.md"
X "$W/pg" rebuild > "$W/f3b.out" 2>&1; echo "rebuild rc=$? ; zsecretchain in index: $(dumpc zsecretchain) ; symlink lines: $(/usr/bin/grep -i -E '[0-9]+  symlink' "$W/f3b.out" | sh 160)"

hr "F3c a file swapped between a regular file and a symlink to a 4_Credentials file WHILE rebuilds run (lstat, then open by path)"
printf '# secret\n\nzsecretswap\n' > "$FIX/4_Credentials/swap-secret.md"
python3 - "$L/2026-05-05_swap.md" "$FIX/4_Credentials/swap-secret.md" "$W/swap.stop" <<'PY' &
import os, sys
target, secret, stop = sys.argv[1:4]
d = os.path.dirname(target); n = 0
while not os.path.exists(stop):
    a = os.path.join(d, ".swap-a"); b = os.path.join(d, ".swap-b")
    with open(a, "w") as f: f.write("---\ntier: W\n---\n# swap\n\nzswapregular\n")
    os.replace(a, target)
    os.symlink(secret, b); os.replace(b, target)
    n += 1
open(stop + ".n", "w").write(str(n))
PY
FLIP=$!
hits=0; reg=0; skipped=0; N=40
for i in $(seq 1 $N); do
  X "$W/pg" rebuild > "$W/f3c-$i.out" 2>&1
  s="$(dumpc zsecretswap)"; r="$(dumpc zswapregular)"
  [ "$s" != "0" ] && hits=$((hits+1)); [ "$r" != "0" ] && reg=$((reg+1))
  /usr/bin/grep -q -F '2026-05-05_swap.md' "$W/f3c-$i.out" || true
done
touch "$W/swap.stop"; wait $FLIP
echo "$N rebuilds while the file flipped $(cat "$W/swap.stop.n") times: the 4_Credentials text entered the index in $hits rebuild(s); the regular text was indexed in $reg (control: the instrument can see both states)"
last="$(ls "$W"/f3c-*.out | tail -1)"; echo "last rebuild's last line: $(tail -1 "$last")"
mv -n "$L/2026-05-05_swap.md" "$W/swap-final-state" 2>/dev/null
X "$W/pg" rebuild > /dev/null 2>&1; echo "after the file is moved away and one more rebuild: zsecretswap=$(dumpc zsecretswap)"

hr "F7 odd files"
: > "$L/2026-05-10_zero-bytes.md"
printf '\xff\xfe\xfd zinvalidutf8 \xc3\x28\n' > "$L/2026-05-11_invalid-utf8.md"
printf -- '---\ntier: W\n---\n# nul\n\nznul\x00word z\x1eq\n' > "$L/2026-05-12_nul.md"
mkdir -p "$L/2026-05-13_a-dir.md"; mkfifo "$L/2026-05-14_fifo.md"
: > "$FIX/0_Brain/people/empty.md"
python3 -c "
import sys
open(sys.argv[1],'w').write('---\ntier: W\n---\n' + ''.join('## h%d\n\nzmanyheads w%d\n\n' % (i, i) for i in range(20000)))" "$L/2026-05-15_many-headings.md"
python3 -c "
import sys
open(sys.argv[1],'w').write('---\ntier: W\n---\n# ' + 'zlongtitle ' * 30000 + '\n\nbody zlongbody\n')" "$L/2026-05-16_long-title.md"
X "$W/pg" rebuild > "$W/f7.out" 2>&1; echo "rebuild rc=$? ; tracebacks: $(/usr/bin/grep -c -i Traceback "$W/f7.out") ; last: $(tail -1 "$W/f7.out")"
/usr/bin/grep -i -E 'not a regular|TRUNCATED|truncat|unreadable|UNTAGGED' "$W/f7.out" | sh 170
echo "in index: zinvalidutf8=$(dumpc zinvalidutf8) znulword=$(dumpc znulword) zmanyheads=$(dumpc zmanyheads) zlongbody=$(dumpc zlongbody)"
X "$W/pg" check 2>&1 | head -1 | sh 120
echo "-- a file that changes DURING a rebuild (a 60 MB daily note makes the rebuild slow; a lesson is rewritten meanwhile)"
python3 -c "
import sys
open(sys.argv[1],'w').write('# d\n\n## S\n' + ''.join('- 06:%02d zslow%d %s\n' % (i % 60, i, 'lorem ipsum ' * 40) for i in range(120000)))" "$FIX/0_Brain/daily/2026-05-20.md"
printf -- '---\ntier: W\n---\n# changing\n\nzbefore\n' > "$L/2026-05-21_changing.md"
X "$W/pg" rebuild > "$W/f7-slow.out" 2>&1 & RB=$!
sleep 1.5; printf -- '---\ntier: W\n---\n# changing\n\nzafter\n' > "$L/2026-05-21_changing.md"
wait $RB; echo "slow rebuild rc=$? ($(/usr/bin/grep -i -E 'time:' "$W/f7-slow.out" | sh 90)) ; index holds zbefore=$(dumpc zbefore) zafter=$(dumpc zafter)"
X "$W/pg" check > "$W/f7-slow-check.out" 2>&1; echo "check rc=$? : $(head -2 "$W/f7-slow-check.out" | tr '\n' ' ' | sh 200)"
mv -n "$FIX/0_Brain/daily/2026-05-20.md" "$W/big-daily-moved.md"
X "$W/pg" rebuild > /dev/null 2>&1

hr "F5a lock: a holder that DIES (kill -9) while a command waits; a holder that stays (the indexer's own lock has no time limit)"
X "$W/pg" stop 2>&1 | tail -1 | sh 60
python3 -c "
import fcntl, os, sys, time
fd = os.open(sys.argv[1], os.O_RDWR | os.O_CREAT, 0o600); fcntl.flock(fd, fcntl.LOCK_EX); open(sys.argv[2], 'w').write('x'); time.sleep(600)" "$W/pg.lock" "$W/h1.flag" & H=$!
while [ ! -f "$W/h1.flag" ]; do sleep 0.1; done
t0=$(date +%s); X "$W/pg" start > "$W/f5a-start.out" 2>&1 & ST=$!
sleep 3; echo "after 3 s the start is $(ps -p $ST -o pid= > /dev/null && echo 'still waiting (correct)' || echo 'ALREADY FINISHED')"
kill -9 $H; wait $H 2>/dev/null; wait $ST; echo "holder killed with SIGKILL; start rc=$? after $(( $(date +%s) - t0 )) s : $(tail -1 "$W/f5a-start.out" | sh 100)"
echo "-- a live holder that never lets go: rebuild (indexer flock, no timeout) and stop (lock wrapper, 150 s limit)"
python3 -c "
import fcntl, os, sys, time
fd = os.open(sys.argv[1], os.O_RDWR | os.O_CREAT, 0o600); fcntl.flock(fd, fcntl.LOCK_EX); open(sys.argv[2], 'w').write('x'); time.sleep(600)" "$W/pg.lock" "$W/h2.flag" & H=$!
while [ ! -f "$W/h2.flag" ]; do sleep 0.1; done
X "$W/pg" rebuild > "$W/f5a-rebuild.out" 2>&1 & RB=$!
sleep 20; if ps -p $RB -o pid= > /dev/null; then echo "rebuild is STILL WAITING after 20 s with no message (output so far: $(wc -c < "$W/f5a-rebuild.out" | tr -d ' ') bytes); it has no time limit"; else echo "rebuild ended by itself"; fi
kill $H; wait $H 2>/dev/null; wait $RB; echo "holder ended; rebuild rc=$? : $(tail -1 "$W/f5a-rebuild.out" | sh 100)"

hr "F5b flock on the DRIVE volume (Case-sensitive APFS, owners disabled) versus /tmp: is the lock exclusive there?"
for where in "$O/scripts/locktest" "$W/locktest"; do
  mkdir -p "$where"; lf="$where/x.lock"
  t0=$(python3 -c 'import time; print(time.time())')
  python3 "$PFC/brain-db/braindb_lock.py" "$lf" 30 /bin/bash -c 'echo "A in $(date +%s.%N)"; sleep 2; echo "A out"' > "$W/lk-a.out" 2>&1 &
  python3 "$PFC/brain-db/braindb_lock.py" "$lf" 30 /bin/bash -c 'echo "B in"; sleep 2; echo "B out"' > "$W/lk-b.out" 2>&1 &
  python3 "$PFC/brain-db/braindb_lock.py" "$lf" 30 /bin/bash -c 'echo "C in"; sleep 2; echo "C out"' > "$W/lk-c.out" 2>&1 &
  wait
  el=$(python3 -c "import time,sys; print('%.1f' % (time.time() - float(sys.argv[1])))" "$t0")
  echo "$(df "$where" | tail -1 | awk '{print $NF}'): three holders of 2 s each took $el s in all (exclusive = about 6 s; not exclusive = about 2 s) ; lock file mode $(stat -f '%Lp %Su' "$lf")"
done

hr "F5c twelve trials of FOUR commands at once, mixes of search / check / rebuild / start / up / at on a cluster in a random starting state (none, stopped, running)"
tot=0; badc=0
for t in 1 2 3 4 5 6 7 8 9 10 11 12; do
  pg="$W/mix$t"; SKT="/tmp/qa3v-m"
  case $((t % 3)) in 0) state="no cluster" ;; 1) SK="$SKT" X "$pg" init > /dev/null 2>&1; state="stopped" ;; 2) SK="$SKT" X "$pg" start > /dev/null 2>&1 || { SK="$SKT" X "$pg" init > /dev/null 2>&1; SK="$SKT" X "$pg" start > /dev/null 2>&1; }; state="running, no index" ;; esac
  cmds=("search xneighbour01" "check" "rebuild" "start" "up" "at pane" "search zebraword --kind lesson" "rebuild")
  pids=""; names=""
  for k in 0 1 2 3; do
    c="${cmds[$(( (t * 3 + k * 5) % 8 ))]}"; names="$names[$c] "
    SK="$SKT" X "$pg" $c > "$W/mix$t-$k.out" 2>&1 & pids="$pids $!"
  done
  rcs=""; k=0
  for p in $pids; do wait $p; rc=$?; rcs="$rcs$rc "; tot=$((tot+1))
    c="${cmds[$(( (t * 3 + k * 5) % 8 ))]}"
    # check may honestly be rc 1 (RED: no index yet) when it runs before the first rebuild; anything else non-zero is a lost command
    if [ "$rc" -ne 0 ] && ! { [ "$c" = "check" ] && [ "$rc" -eq 1 ] && /usr/bin/grep -q -i 'check: RED' "$W/mix$t-$k.out"; }; then badc=$((badc+1)); echo "   LOST: trial $t '$c' rc=$rc : $(/usr/bin/grep -i -E 'braindb:|FATAL|ERROR' "$W/mix$t-$k.out" | tail -2 | tr '\n' ' ' | sh 260)"; fi
    k=$((k+1)); done
  SK="$SKT" X "$pg" rebuild > "$W/mix$t-final.out" 2>&1; frc=$?
  echo "trial $t ($state): $names-> rc $rcs| afterwards: rebuild rc=$frc, $(SK="$SKT" X "$pg" check 2>&1 | head -1 | sh 60), servers $(nprocs "$pg"), PG_VERSION $([ -f "$pg/PG_VERSION" ] && echo present || echo MISSING)"
  SK="$SKT" X "$pg" stop > /dev/null 2>&1
done
echo "commands run at once: $tot ; lost (non-zero other than an honest RED check): $badc"

hr "F5d stop racing a search and a rebuild (6 trials): what do the losers print?"
SK=/tmp/qa3v-m X "$W/mix1" rebuild > /dev/null 2>&1
for t in 1 2 3 4 5 6; do
  SK=/tmp/qa3v-m X "$W/mix1" search xneighbour01 > "$W/sr$t-a.out" 2>&1 & a=$!
  SK=/tmp/qa3v-m X "$W/mix1" stop > "$W/sr$t-b.out" 2>&1 & b=$!
  SK=/tmp/qa3v-m X "$W/mix1" rebuild > "$W/sr$t-c.out" 2>&1 & c=$!
  wait $a; ra=$?; wait $b; rb=$?; wait $c; rc=$?
  echo "trial $t: search rc=$ra stop rc=$rb rebuild rc=$rc ; tracebacks $(cat "$W/sr$t-a.out" "$W/sr$t-b.out" "$W/sr$t-c.out" | /usr/bin/grep -c -i Traceback) ; servers $(nprocs "$W/mix1") ; $(cat "$W/sr$t-a.out" "$W/sr$t-c.out" | /usr/bin/grep -i -E '^braindb:' | head -2 | tr '\n' ' ' | sh 220)"
done
SK=/tmp/qa3v-m X "$W/mix1" stop 2>&1 | tail -1 | sh 60

hr "END"
X "$W/pg" stop 2>&1 | tail -1 | sh 60
echo "processes with a data directory under $W: $(nprocs "$W")"; date '+%Y-%m-%d %H:%M:%S %Z'
