#!/bin/bash
# process-safety scenarios, v2, on SCRATCH clusters only (identified by data directory under $P)
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/chk
P="$S/proc-$(date +%H%M%S)"; mkdir -p "$P/q" || exit 2
TOOL=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/lanecopy/WEDNESDAY/2_Project_Files/brain-db/braindb.sh
FIX="$(cat "$S/atk/LAST")/tree"
SOCK=/tmp/qa3c; SOCK2=/tmp/qa3c-b
[ -z "$(ls -A "$SOCK")" ] && [ -z "$(ls -A "$SOCK2")" ] || { echo "PREFLIGHT FAILED: a socket directory of mine is not empty"; exit 2; }
PSQL=/opt/homebrew/opt/postgresql@15/bin/psql
X() { local pg="$1" so="$2" ro="$3"; shift 3; BRAINDB_ROOT="$ro" BRAINDB_PGDATA="$pg" BRAINDB_SOCKDIR="$so" BRAINDB_SCOPE="" WED_AGENT=wednesday /bin/bash "$TOOL" "$@"; }
procs() { local snap; snap="$(ps -axww -o pid=,command=)"; printf '%s\n' "$snap" | /usr/bin/grep -i -F -- "-D $1" ; }
nprocs() { local snap; snap="$(ps -axww -o pid=,command=)"; printf '%s\n' "$snap" | /usr/bin/grep -i -F -c -- "-D $1"; }
alive() { [ -n "$1" ] && [ -n "$(ps -p "$1" -o pid= | tr -d ' ')" ] && echo alive || echo GONE; }
sh() { awk -v n="${1:-200}" '{print substr($0,1,n)}'; }
idx() { "$PSQL" -X -At -h "$1" -d braindb -c "select count(*)||' files, built '||(select v from brain.meta where k='built_at')||', root …'||right((select v from brain.meta where k='root'),28) from brain.files" 2>&1 | sh 160; }
hr() { echo; echo "######## $1"; }
echo "proc run dir $P ; $(date '+%Y-%m-%d %H:%M:%S %Z')"

hr "P1 two starts at once (cluster exists, stopped)"
X "$P/c1" "$SOCK" "$FIX" init > "$P/c1-init.out" 2>&1; echo "init rc=$?"
X "$P/c1" "$SOCK" "$FIX" start > "$P/p1-a.out" 2>&1 & a=$!
X "$P/c1" "$SOCK" "$FIX" start > "$P/p1-b.out" 2>&1 & b=$!
wait $a; ra=$?; wait $b; rb=$?
echo "start A rc=$ra : $(tail -1 "$P/p1-a.out" | sh)"; echo "start B rc=$rb : $(tail -1 "$P/p1-b.out" | sh)"
echo "FATAL lines seen by A: $(/usr/bin/grep -i -c 'FATAL' "$P/p1-a.out")  by B: $(/usr/bin/grep -i -c 'FATAL' "$P/p1-b.out")"; /usr/bin/grep -i -h 'FATAL' "$P/p1-a.out" "$P/p1-b.out" | sort -u | sh 170
echo "server processes with -D c1: $(nprocs "$P/c1")"; X "$P/c1" "$SOCK" "$FIX" status | tail -1 | sh
X "$P/c1" "$SOCK" "$FIX" rebuild > "$P/c1-rebuild.out" 2>&1; echo "rebuild rc=$? ; $(idx "$SOCK")"

hr "P2 two self-starting searches at once on a STOPPED cluster"
X "$P/c1" "$SOCK" "$FIX" stop | sh 60; echo "processes: $(nprocs "$P/c1")"
X "$P/c1" "$SOCK" "$FIX" search xneighbour01 > "$P/p2-a.out" 2>&1 & a=$!
X "$P/c1" "$SOCK" "$FIX" search xneighbour01 > "$P/p2-b.out" 2>&1 & b=$!
wait $a; ra=$?; wait $b; rb=$?
echo "search A rc=$ra : $(tail -1 "$P/p2-a.out" | sh)"; echo "search B rc=$rb : $(tail -1 "$P/p2-b.out" | sh)"
/usr/bin/grep -i -h -E 'FATAL|did not start' "$P/p2-a.out" "$P/p2-b.out" | sort -u | sh 170
echo "server processes with -D c1: $(nprocs "$P/c1")"
X "$P/c1" "$SOCK" "$FIX" stop | sh 60; echo "after stop: $(nprocs "$P/c1") process(es)"

hr "P2b two self-starting searches at once with NO cluster at all (double init), 4 trials, socket dir $SOCK2"
for t in 1 2 3 4; do
  X "$P/n$t" "$SOCK2" "$FIX" search xneighbour01 > "$P/p2b-$t-a.out" 2>&1 & a=$!
  X "$P/n$t" "$SOCK2" "$FIX" search xneighbour01 > "$P/p2b-$t-b.out" 2>&1 & b=$!
  wait $a; ra=$?; wait $b; rb=$?
  echo "trial $t: A rc=$ra ($(tail -1 "$P/p2b-$t-a.out" | sh 100)) | B rc=$rb ($(tail -1 "$P/p2b-$t-b.out" | sh 100))"
  /usr/bin/grep -i -h -E 'initdb: (error|warning|removing)|REFUSED|FATAL|did not start' "$P/p2b-$t-a.out" "$P/p2b-$t-b.out" | sed "s|$P/||g" | sh 150 | sort | uniq -c
  echo "   data dir after the race: $(ls "$P/n$t" 2>&1 | wc -l | tr -d ' ') entries, PG_VERSION $([ -f "$P/n$t/PG_VERSION" ] && echo present || echo MISSING)"
  X "$P/n$t" "$SOCK2" "$FIX" search xneighbour01 > "$P/p2b-$t-c.out" 2>&1; echo "   a third search, alone, afterwards: rc=$? ($(tail -1 "$P/p2b-$t-c.out" | sed "s|$P/||g" | sh 150))"
  X "$P/n$t" "$SOCK2" "$FIX" stop 2>&1 | tail -1 | sh 50; echo "   processes left for n$t: $(nprocs "$P/n$t")"
done

hr "P4 stale pid file whose pid belongs to an unrelated LIVE process (a python sleeper that DIES on SIGINT or SIGTERM)"
python3 -c "import time; time.sleep(900)" & SL=$!
sleep 1
printf '%s\n%s\n' "$SL" "$P/c1" > "$P/c1/postmaster.pid"
echo "sleeper pid $SL: $(alive $SL) ; c1 processes: $(nprocs "$P/c1")"
X "$P/c1" "$SOCK" "$FIX" status | tail -1; 
X "$P/c1" "$SOCK" "$FIX" stop 2>&1 | sh 120; echo "stop rc=${PIPESTATUS[0]} ; sleeper $(alive $SL)"
X "$P/c1" "$SOCK" "$FIX" start > "$P/p4-start.out" 2>&1; echo "start rc=$? ; sleeper $(alive $SL)"; /usr/bin/grep -i -E 'braindb:|FATAL|HINT' "$P/p4-start.out" | tail -3 | sed "s|$P/||g" | sh 200
X "$P/c1" "$SOCK" "$FIX" search xneighbour01 > "$P/p4-search.out" 2>&1; echo "search rc=$? ; sleeper $(alive $SL)"
X "$P/c1" "$SOCK" "$FIX" up > "$P/p4-up.out" 2>&1; echo "up rc=$? ; sleeper $(alive $SL)"
echo "server processes with -D c1: $(nprocs "$P/c1") ; pid file line 1 still: $(sed -n 1p "$P/c1/postmaster.pid")"
echo "-- recovery by hand: move the stale pid file aside (mv -n), then start"
mv -n "$P/c1/postmaster.pid" "$P/q/stale-postmaster.pid"
X "$P/c1" "$SOCK" "$FIX" start | tail -1 | sh 120; echo "sleeper $(alive $SL) ; c1 processes: $(nprocs "$P/c1")"

hr "P5 pid file pointing at ANOTHER Postgres server (c1 RUNNING; c2 a second cluster, stopped, own socket dir)"
C1PID="$(sed -n 1p "$P/c1/postmaster.pid" | tr -d ' ')"; echo "c1 server pid $C1PID $(alive "$C1PID")"
X "$P/c2" "$SOCK2" "$FIX" init > "$P/c2-init.out" 2>&1; echo "c2 init rc=$? ; c2 processes: $(nprocs "$P/c2")"
echo "-- 5a: c2's pid file is a byte copy of c1's (c1's pid AND c1's data directory)"
cp "$P/c1/postmaster.pid" "$P/c2/postmaster.pid"
X "$P/c2" "$SOCK2" "$FIX" status | tail -1
X "$P/c2" "$SOCK2" "$FIX" stop 2>&1 | sed "s|$P/||g" | sh 200; echo "c2 stop rc=${PIPESTATUS[0]} ; c1 server $(alive $C1PID)"
X "$P/c2" "$SOCK2" "$FIX" start > "$P/p5a-start.out" 2>&1; echo "c2 start rc=$? ; c1 server $(alive $C1PID) ; c2 processes: $(nprocs "$P/c2")"; /usr/bin/grep -i -E 'braindb:|FATAL|HINT' "$P/p5a-start.out" | tail -3 | sed "s|$P/||g" | sh 200
[ "$(nprocs "$P/c2")" = "0" ] && mv -n "$P/c2/postmaster.pid" "$P/q/p5a-postmaster.pid"
echo "-- 5b: c2's pid file names c1's pid but c2's OWN data directory"
printf '%s\n%s\n' "$C1PID" "$P/c2" > "$P/c2/postmaster.pid"
X "$P/c2" "$SOCK2" "$FIX" status | tail -1
X "$P/c2" "$SOCK2" "$FIX" stop 2>&1 | sed "s|$P/||g" | sh 200; echo "c2 stop rc=${PIPESTATUS[0]} ; c1 server $(alive $C1PID)"
X "$P/c2" "$SOCK2" "$FIX" start > "$P/p5b-start.out" 2>&1; echo "c2 start rc=$? ; c1 server $(alive $C1PID) ; c2 processes: $(nprocs "$P/c2")"
[ "$(nprocs "$P/c2")" = "0" ] && mv -n "$P/c2/postmaster.pid" "$P/q/p5b-postmaster.pid"
echo "c1 still answers: $(X "$P/c1" "$SOCK" "$FIX" check | tail -1 | sh 60) ; c1 pid $(alive $C1PID)"

hr "P6 one socket directory, two data directories: can a command addressed to c2 (STOPPED) act on c1's server?"
echo "c1 index before: $(idx "$SOCK") ; c2 processes: $(nprocs "$P/c2")"
mkdir -p "$P/tiny/0_Brain/learnings"; printf -- '---\ntier: W\n---\n# tiny\n\nzp6token\n' > "$P/tiny/0_Brain/learnings/2026-01-01_tiny.md"
echo "-- 6a default (self-start on): PGDATA=c2, SOCKDIR=c1's, a different tree; rebuild"
X "$P/c2" "$SOCK" "$P/tiny" rebuild > "$P/p6a.out" 2>&1; echo "rc=$?"; /usr/bin/grep -i -E 'braindb:|FATAL|HINT|rebuild:' "$P/p6a.out" | tail -3 | sed "s|$P/||g" | sh 200
echo "c1 index after 6a: $(idx "$SOCK") ; c2 processes: $(nprocs "$P/c2")"
echo "-- 6b BRAINDB_NO_AUTOSTART=1 (the mode doctor.sh is proposed to use): same call"
BRAINDB_NO_AUTOSTART=1 X "$P/c2" "$SOCK" "$P/tiny" rebuild > "$P/p6b.out" 2>&1; echo "rc=$?"; tail -2 "$P/p6b.out" | sh 160
echo "c1 index after 6b: $(idx "$SOCK")"
echo "-- 6c BRAINDB_NO_AUTOSTART=1 check, addressed to c2 (stopped)"
BRAINDB_NO_AUTOSTART=1 X "$P/c2" "$SOCK" "$P/tiny" check | sh 160; echo "check rc=${PIPESTATUS[0]} (the proposed doctor block prints rc 0 as 'index current')"
X "$P/c2" "$SOCK" "$P/tiny" status | tail -1
X "$P/c1" "$SOCK" "$FIX" rebuild > "$P/p6-restore.out" 2>&1; echo "c1 restored rc=$? : $(idx "$SOCK")"

hr "P7 command substitution (the launcher's form) returns: out=\$(braindb.sh up 2>&1)"
X "$P/c1" "$SOCK" "$FIX" stop | tail -1 | sh 40
t0=$(date +%s); out="$(X "$P/c1" "$SOCK" "$FIX" up 2>&1)"; rc=$?; t1=$(date +%s); echo "up rc=$rc in $((t1-t0)) s ; last line: $(printf '%s\n' "$out" | tail -1 | sh 120) ; c1 processes $(nprocs "$P/c1")"

hr "P3 search during a rebuild; two rebuilds at once; stop during a rebuild (scratch cluster c3 over the REAL tree, read-only)"
R=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/realcopy/WEDNESDAY
X "$P/c3" "$SOCK2" "$R" init > "$P/c3-init.out" 2>&1; X "$P/c3" "$SOCK2" "$R" start | tail -1 | sh 100
X "$P/c3" "$SOCK2" "$R" rebuild > "$P/c3-rebuild1.out" 2>&1; echo "first full rebuild rc=$? : $(/usr/bin/grep -i -E '^ +total' "$P/c3-rebuild1.out") ; $(idx "$SOCK2")"
echo "-- 3a search DURING a rebuild"
X "$P/c3" "$SOCK2" "$R" rebuild > "$P/c3-rebuild2.out" 2>&1 & rb=$!
sleep 2
t0=$(date +%s); X "$P/c3" "$SOCK2" "$R" search "close a pane" --limit 1 > "$P/p3a-search.out" 2>&1; rs=$?; t1=$(date +%s)
wait $rb; echo "rebuild rc=$? ; search rc=$rs after $((t1-t0)) s : $(sed -n 2p "$P/p3a-search.out" | sh 120) / $(tail -1 "$P/p3a-search.out")"
echo "-- 3b two rebuilds at once"
X "$P/c3" "$SOCK2" "$R" rebuild > "$P/p3b-a.out" 2>&1 & a=$!
X "$P/c3" "$SOCK2" "$R" rebuild > "$P/p3b-b.out" 2>&1 & b=$!
wait $a; ra=$?; wait $b; rb2=$?
echo "rebuild A rc=$ra ($(tail -1 "$P/p3b-a.out" | sh 90)) | rebuild B rc=$rb2 ($(tail -1 "$P/p3b-b.out" | sh 90))"
/usr/bin/grep -i -h -E 'ERROR|deadlock|FAILED' "$P/p3b-a.out" "$P/p3b-b.out" | sh 200
X "$P/c3" "$SOCK2" "$R" check | head -1 | sh 140
echo "-- 3c stop DURING a rebuild (before: $(idx "$SOCK2"))"
X "$P/c3" "$SOCK2" "$R" rebuild > "$P/p3c-rebuild.out" 2>&1 & rb=$!
sleep 2
X "$P/c3" "$SOCK2" "$R" stop | tail -1 | sh 60; echo "stop rc=${PIPESTATUS[0]}"
wait $rb; echo "interrupted rebuild rc=$? : $(tail -3 "$P/p3c-rebuild.out" | tr '\n' ' ' | sh 300)"
echo "processes with -D c3 after stop: $(nprocs "$P/c3")"
X "$P/c3" "$SOCK2" "$R" start | tail -1 | sh 100
echo "after restart: $(idx "$SOCK2") ; chunks $("$PSQL" -X -At -h "$SOCK2" -d braindb -c "select count(*) from brain.chunks" 2>&1)"
X "$P/c3" "$SOCK2" "$R" check | head -1 | sh 160

hr "END: stop everything of mine, each with its own socket directory, and count by data directory"
kill "$SL"; wait "$SL" 2>> "$P/sleeper.err"; echo "sleeper $(alive $SL)"
X "$P/c1" "$SOCK" "$FIX" stop 2>&1 | tail -1 | sh 60
for c in c2 c3 n1 n2 n3 n4; do X "$P/$c" "$SOCK2" "$FIX" stop 2>&1 | tail -1 | sh 60; done
echo "processes with a data directory under $P: $(nprocs "$P")"; procs "$P" | sh 200
echo "socket dirs: [$(ls -A "$SOCK")] [$(ls -A "$SOCK2")]"
echo "$P" > "$S/PROC_LAST"; date '+%Y-%m-%d %H:%M:%S %Z'
