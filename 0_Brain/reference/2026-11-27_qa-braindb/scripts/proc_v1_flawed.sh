#!/bin/bash
# process-safety scenarios on SCRATCH clusters only (identified by data directory under $P)
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/qa-braindb
P="$S/proc-$(date +%H%M%S)"; mkdir -p "$P/q" || exit 2
TOOL=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db/braindb.sh
FIX="$(cat "$S/atk/LAST")/tree"
SOCK=/tmp/qa-bdb-501; SOCK2=/tmp/qa-bdb-501-b
[ -d "$SOCK2" ] || mkdir -m 700 "$SOCK2"
# X <pgdata> <sockdir> <root> args...
X() { local pg="$1" so="$2" ro="$3"; shift 3; BRAINDB_ROOT="$ro" BRAINDB_PGDATA="$pg" BRAINDB_SOCKDIR="$so" BRAINDB_SCOPE="" WED_AGENT=wednesday /bin/bash "$TOOL" "$@"; }
procs() { local snap; snap="$(ps -axww -o pid=,command=)"; printf '%s\n' "$snap" | /usr/bin/grep -i -F -- "-D $1" ; }
nprocs() { local snap; snap="$(ps -axww -o pid=,command=)"; printf '%s\n' "$snap" | /usr/bin/grep -i -F -c -- "-D $1"; }
alive() { [ -n "$(ps -p "$1" -o pid= | tr -d ' ')" ] && echo alive || echo GONE; }
hr() { echo; echo "######## $1"; }
echo "proc run dir $P ; $(date '+%Y-%m-%d %H:%M:%S %Z')"

hr "P1 two starts at once (cluster exists, stopped)"
X "$P/c1" "$SOCK" "$FIX" init > "$P/c1-init.out" 2>&1; echo "init rc=$?"
X "$P/c1" "$SOCK" "$FIX" start > "$P/p1-a.out" 2>&1 & a=$!
X "$P/c1" "$SOCK" "$FIX" start > "$P/p1-b.out" 2>&1 & b=$!
wait $a; ra=$?; wait $b; rb=$?
echo "start A rc=$ra : $(tail -1 "$P/p1-a.out" | cut -c1-200)"; echo "start B rc=$rb : $(tail -1 "$P/p1-b.out" | cut -c1-200)"
/usr/bin/grep -i -E 'FATAL|lock file|another server' "$P/p1-a.out" "$P/p1-b.out" | cut -c1-220
echo "server processes with -D c1: $(nprocs "$P/c1")"; X "$P/c1" "$SOCK" "$FIX" status | tail -3
X "$P/c1" "$SOCK" "$FIX" rebuild > "$P/c1-rebuild.out" 2>&1; echo "rebuild rc=$?"

hr "P2 two self-starting searches at once on a STOPPED cluster"
X "$P/c1" "$SOCK" "$FIX" stop
X "$P/c1" "$SOCK" "$FIX" search xneighbour01 > "$P/p2-a.out" 2>&1 & a=$!
X "$P/c1" "$SOCK" "$FIX" search xneighbour01 > "$P/p2-b.out" 2>&1 & b=$!
wait $a; ra=$?; wait $b; rb=$?
echo "search A rc=$ra : $(tail -1 "$P/p2-a.out" | cut -c1-200)"; echo "search B rc=$rb : $(tail -1 "$P/p2-b.out" | cut -c1-200)"
/usr/bin/grep -i -E 'FATAL|lock file|another server|did not start' "$P/p2-a.out" "$P/p2-b.out" | cut -c1-220
echo "server processes with -D c1: $(nprocs "$P/c1")"
X "$P/c1" "$SOCK" "$FIX" stop; echo "after stop: $(nprocs "$P/c1") process(es)"

hr "P2b two self-starting searches at once with NO cluster at all (double init), 3 trials"
for t in 1 2 3; do
  X "$P/n$t" "$SOCK" "$FIX" search xneighbour01 > "$P/p2b-$t-a.out" 2>&1 & a=$!
  X "$P/n$t" "$SOCK" "$FIX" search xneighbour01 > "$P/p2b-$t-b.out" 2>&1 & b=$!
  wait $a; ra=$?; wait $b; rb=$?
  echo "trial $t: A rc=$ra ($(tail -1 "$P/p2b-$t-a.out" | cut -c1-110)) | B rc=$rb ($(tail -1 "$P/p2b-$t-b.out" | cut -c1-110))"
  /usr/bin/grep -i -h -E 'initdb:|REFUSED|FATAL|exists but is not empty|did not start' "$P/p2b-$t-a.out" "$P/p2b-$t-b.out" | cut -c1-200 | sort | uniq -c
  X "$P/n$t" "$SOCK" "$FIX" search xneighbour01 > "$P/p2b-$t-c.out" 2>&1; echo "   third, alone, afterwards: rc=$? ($(tail -1 "$P/p2b-$t-c.out" | cut -c1-110))"
  X "$P/n$t" "$SOCK" "$FIX" check 2>&1 | tail -1 | cut -c1-160
  X "$P/n$t" "$SOCK" "$FIX" stop 2>&1 | tail -1; echo "   processes left for n$t: $(nprocs "$P/n$t")"
done

hr "P4 stale pid file whose pid belongs to an unrelated LIVE process (a python sleeper that dies on SIGINT/SIGTERM)"
python3 -c "import time; time.sleep(900)" & SL=$!
sleep 1
printf '%s\n%s\n' "$SL" "$P/c1" > "$P/c1/postmaster.pid"
echo "sleeper pid $SL: $(alive $SL)"
X "$P/c1" "$SOCK" "$FIX" status; echo "status rc=$?"
X "$P/c1" "$SOCK" "$FIX" stop; echo "stop rc=$? ; sleeper $(alive $SL)"
X "$P/c1" "$SOCK" "$FIX" start > "$P/p4-start.out" 2>&1; echo "start rc=$? ; sleeper $(alive $SL)"; tail -6 "$P/p4-start.out" | cut -c1-220
X "$P/c1" "$SOCK" "$FIX" search xneighbour01 > "$P/p4-search.out" 2>&1; echo "search rc=$? ; sleeper $(alive $SL)"; tail -2 "$P/p4-search.out" | cut -c1-220
echo "server processes with -D c1: $(nprocs "$P/c1") ; pid file now: $(tr '\n' ' ' < "$P/c1/postmaster.pid" 2>&1 | cut -c1-120)"
echo "-- recovery: move the stale pid file aside (mv -n), then start"
mv -n "$P/c1/postmaster.pid" "$P/q/stale-postmaster.pid"
X "$P/c1" "$SOCK" "$FIX" start | tail -1; echo "start rc=$? ; sleeper $(alive $SL)"

hr "P5 pid file pointing at ANOTHER Postgres server (c1 is running; c2 is a second cluster, stopped)"
X "$P/c2" "$SOCK2" "$FIX" init > "$P/c2-init.out" 2>&1; echo "c2 init rc=$?"
C1PID="$(sed -n 1p "$P/c1/postmaster.pid" | tr -d ' ')"; echo "c1 server pid $C1PID"
echo "-- 5a: c2's pid file is a byte copy of c1's (names c1's pid AND c1's data directory)"
cp "$P/c1/postmaster.pid" "$P/c2/postmaster.pid"
X "$P/c2" "$SOCK2" "$FIX" status | tail -1; X "$P/c2" "$SOCK2" "$FIX" stop; echo "c2 stop rc=$? ; c1 server $(alive $C1PID)"
X "$P/c2" "$SOCK2" "$FIX" start > "$P/p5a-start.out" 2>&1; echo "c2 start rc=$? ; c1 server $(alive $C1PID)"; tail -4 "$P/p5a-start.out" | cut -c1-200
mv -n "$P/c2/postmaster.pid" "$P/q/p5a-postmaster.pid" 2>&1
echo "-- 5b: c2's pid file names c1's pid but c2's own data directory"
X "$P/c2" "$SOCK2" "$FIX" stop > "$P/p5b-pre.out" 2>&1
[ -f "$P/c2/postmaster.pid" ] && mv -n "$P/c2/postmaster.pid" "$P/q/p5b-pre-postmaster.pid"
printf '%s\n%s\n' "$C1PID" "$P/c2" > "$P/c2/postmaster.pid"
X "$P/c2" "$SOCK2" "$FIX" stop; echo "c2 stop rc=$? ; c1 server $(alive $C1PID)"
X "$P/c2" "$SOCK2" "$FIX" status | tail -1
mv -n "$P/c2/postmaster.pid" "$P/q/p5b-postmaster.pid"
echo "c1 still answers: $(X "$P/c1" "$SOCK" "$FIX" check | tail -1 | cut -c1-80)"
echo "c2 processes: $(nprocs "$P/c2")"; procs "$P/c2" | cut -c1-200

hr "P6 one socket directory, two data directories: does a command for c2 write into c1's server?"
echo "c1 files before: $(/opt/homebrew/opt/postgresql@15/bin/psql -X -At -h "$SOCK" -d braindb -c "select count(*)||' files, root='||(select v from brain.meta where k='root') from brain.files" | cut -c1-200)"
mkdir -p "$P/tiny/0_Brain/learnings"; printf -- '---\ntier: W\n---\n# tiny\n\nzp6token\n' > "$P/tiny/0_Brain/learnings/2026-01-01_tiny.md"
echo "-- 6a default (self-start on): c2 + c1's socket directory, rebuild of a different tree"
X "$P/c2" "$SOCK" "$P/tiny" rebuild > "$P/p6a.out" 2>&1; echo "rc=$?"; tail -3 "$P/p6a.out" | cut -c1-220
echo "c1 files after 6a: $(/opt/homebrew/opt/postgresql@15/bin/psql -X -At -h "$SOCK" -d braindb -c "select count(*)||' files, root='||(select v from brain.meta where k='root') from brain.files" | cut -c1-200)"
echo "c2 processes: $(nprocs "$P/c2")"
echo "-- 6b BRAINDB_NO_AUTOSTART=1 (doctor's mode): c2 + c1's socket directory, rebuild of a different tree"
BRAINDB_NO_AUTOSTART=1 X "$P/c2" "$SOCK" "$P/tiny" rebuild > "$P/p6b.out" 2>&1; echo "rc=$?"; tail -3 "$P/p6b.out" | cut -c1-220
echo "c1 files after 6b: $(/opt/homebrew/opt/postgresql@15/bin/psql -X -At -h "$SOCK" -d braindb -c "select count(*)||' files, root='||(select v from brain.meta where k='root') from brain.files" | cut -c1-200)"
echo "-- 6c the same for check, as doctor would call it for c2 (which is STOPPED)"
BRAINDB_NO_AUTOSTART=1 X "$P/c2" "$SOCK" "$P/tiny" check; echo "check rc=$? (doctor reads 0 as 'index current', 3 as 'server stopped')"
X "$P/c1" "$SOCK" "$FIX" rebuild > "$P/p6-restore.out" 2>&1; echo "c1 restored rc=$?"

hr "P7 command substitution (the launcher's form) does not hang: out=\$(braindb.sh up 2>&1)"
X "$P/c1" "$SOCK" "$FIX" stop | tail -1
t0=$(date +%s); out="$(X "$P/c1" "$SOCK" "$FIX" up 2>&1)"; rc=$?; t1=$(date +%s); echo "up rc=$rc in $((t1-t0)) s ; last line: $(printf '%s\n' "$out" | tail -1 | cut -c1-120)"

hr "P3 stop during a rebuild; search during a rebuild; two rebuilds at once (scratch cluster c3 over the REAL tree, read-only, ~5 s per rebuild)"
R=/Volumes/DevMASTER/WEDNESDAY
X "$P/c3" "$SOCK2" "$R" init > "$P/c3-init.out" 2>&1; X "$P/c3" "$SOCK2" "$R" start | tail -1
X "$P/c3" "$SOCK2" "$R" rebuild > "$P/c3-rebuild1.out" 2>&1; echo "first full rebuild rc=$? : $(/usr/bin/grep -i 'total' "$P/c3-rebuild1.out")"
BUILT1="$(/opt/homebrew/opt/postgresql@15/bin/psql -X -At -h "$SOCK2" -d braindb -c "select v from brain.meta where k='built_at'")"; echo "built_at $BUILT1"
echo "-- 3a search DURING a rebuild"
X "$P/c3" "$SOCK2" "$R" rebuild > "$P/c3-rebuild2.out" 2>&1 & rb=$!
sleep 2
t0=$(date +%s); X "$P/c3" "$SOCK2" "$R" search "close a pane" --limit 1 > "$P/p3a-search.out" 2>&1; rs=$?; t1=$(date +%s)
wait $rb; echo "rebuild rc=$? ; search rc=$rs after $((t1-t0)) s : $(sed -n 2p "$P/p3a-search.out" | cut -c1-140) / $(tail -1 "$P/p3a-search.out")"
echo "-- 3b two rebuilds at once"
X "$P/c3" "$SOCK2" "$R" rebuild > "$P/p3b-a.out" 2>&1 & a=$!
X "$P/c3" "$SOCK2" "$R" rebuild > "$P/p3b-b.out" 2>&1 & b=$!
wait $a; ra=$?; wait $b; rb2=$?
echo "rebuild A rc=$ra ($(tail -1 "$P/p3b-a.out" | cut -c1-90)) | rebuild B rc=$rb2 ($(tail -1 "$P/p3b-b.out" | cut -c1-90))"
/usr/bin/grep -i -h -E 'ERROR|deadlock|FAILED' "$P/p3b-a.out" "$P/p3b-b.out" | cut -c1-200
X "$P/c3" "$SOCK2" "$R" check | head -1 | cut -c1-140
BUILT2="$(/opt/homebrew/opt/postgresql@15/bin/psql -X -At -h "$SOCK2" -d braindb -c "select v from brain.meta where k='built_at'")"
echo "-- 3c stop DURING a rebuild (index built_at before: $BUILT2)"
X "$P/c3" "$SOCK2" "$R" rebuild > "$P/p3c-rebuild.out" 2>&1 & rb=$!
sleep 2
X "$P/c3" "$SOCK2" "$R" stop; echo "stop rc=$?"
wait $rb; echo "interrupted rebuild rc=$? : $(tail -2 "$P/p3c-rebuild.out" | tr '\n' ' ' | cut -c1-260)"
echo "processes with -D c3 after stop: $(nprocs "$P/c3")"
X "$P/c3" "$SOCK2" "$R" start | tail -1
echo "after restart: built_at $(/opt/homebrew/opt/postgresql@15/bin/psql -X -At -h "$SOCK2" -d braindb -c "select v from brain.meta where k='built_at'") ; files $(/opt/homebrew/opt/postgresql@15/bin/psql -X -At -h "$SOCK2" -d braindb -c "select count(*) from brain.files") ; chunks $(/opt/homebrew/opt/postgresql@15/bin/psql -X -At -h "$SOCK2" -d braindb -c "select count(*) from brain.chunks")"
X "$P/c3" "$SOCK2" "$R" check | head -1 | cut -c1-160

hr "END: stop everything of mine, by data directory"
kill "$SL"; wait "$SL" 2>> "$P/sleeper.err"; echo "sleeper $(alive $SL)"
for c in c1 c2 c3 n1 n2 n3; do X "$P/$c" "$SOCK" "$FIX" stop 2>&1 | tail -1 | cut -c1-160; done
echo "processes with a data directory under $P: $(nprocs "$P")"; procs "$P" | cut -c1-200
echo "$P" > "$S/PROC_LAST"; date '+%Y-%m-%d %H:%M:%S %Z'
