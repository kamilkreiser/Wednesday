#!/bin/bash
# seat_f2.sh - NEW attacks on the round-3 seat rule and on F2 (server identity). Scratch only.
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3
PFC="$S/lanecopy/WEDNESDAY/2_Project_Files"
PGBIN=/opt/homebrew/opt/postgresql@15/bin
W="$S/seat-$(date +%H%M%S)"; mkdir -p "$W" || exit 2
FIX="$W/fix"; python3 "$PFC/brain-db/tests/make_fixtures.py" "$FIX" > "$W/fx.out" 2>&1
SOCK=/tmp/qa3s; SOCK2=/tmp/qa3s-b
sh() { awk -v n="${1:-230}" '{print substr($0,1,n)}' | sed "s|$W/||g"; }
nprocs() { local snap; snap="$(ps -axww -o pid=,command=)"; printf '%s\n' "$snap" | /usr/bin/grep -F -c -- "-D $1"; }
mktree() { # mktree <dir path whose basename is the tree name> [scope file to install as scope/<seat>.scope] [seat]
  local t="$1/2_Project_Files"; mkdir -p "$t/fleet/cockpit" "$t/tools" "$t/brain-db/scope"
  cp "$PFC/brain-db/braindb.sh" "$PFC/brain-db/braindb_index.py" "$PFC/brain-db/braindb_lock.py" "$t/brain-db/"
  cp "$PFC/fleet/cockpit/seat_resolve.sh" "$t/fleet/cockpit/"; cp "$PFC/tools/seat_note.sh" "$t/tools/"
  cp "$PFC/brain-db/scope/wednesday.scope" "$t/brain-db/scope/"
  cp "$PFC/brain-db/proposed/scope/tuesday.scope" "$PFC/brain-db/proposed/scope/friday.scope" "$t/brain-db/scope/"
}
T() { # T <tree dir> <args...> : that tree's tool, fixture root, own scratch cluster under $W/pg-<basename>
  local tree="$1"; shift
  env -u WED_AGENT BRAINDB_ROOT="$FIX" BRAINDB_PGDATA="$W/pg-$(basename "$tree" | tr -d ' ')" BRAINDB_SOCKDIR="$SOCK" ${EXTRA:-} /bin/bash "$tree/2_Project_Files/brain-db/braindb.sh" "$@"
}
hr() { echo; echo "######## $1"; }
echo "run dir $W ; $(date '+%Y-%m-%d %H:%M:%S %Z')"

hr "S1 tree names: which seat does each resolve to? (status line 1; rc 2 = refused)"
for name in "WEDNESDAY" "wednesday" "Wednesday" "WEDNESDAY " " WEDNESDAY" "WEDNESDAY.bak" "wEDNESDAY" "TUESDAY" "tuesday" "TuEsday" "FRIDAY" "WEDNESDAY-copy" "WEDNESDAY
x"; do
  d="$W/names/n$(printf '%s' "$name" | cksum | cut -d' ' -f1)/$name"; mktree "$d"
  out="$(T "$d" status 2>&1 | head -1 | sh 150)"; rc=${PIPESTATUS[0]}
  printf 'tree %-18s -> %s\n' "'$(printf '%s' "$name" | tr '\n' '~')'" "$out"
done

hr "S2 symlinked trees: the link's name versus the real folder's name"
mktree "$W/real/WEDNESDAY"; mktree "$W/real/TUESDAY"
mkdir -p "$W/links"; ln -s "$W/real/WEDNESDAY" "$W/links/TUESDAY"; ln -s "$W/real/TUESDAY" "$W/links/WEDNESDAY"
echo "run through link named TUESDAY -> real WEDNESDAY : $(T "$W/links/TUESDAY" status 2>&1 | head -1 | sh 120)"
echo "run through link named WEDNESDAY -> real TUESDAY : $(T "$W/links/WEDNESDAY" status 2>&1 | head -1 | sh 120)"
ln -s "$W/real/WEDNESDAY/2_Project_Files/brain-db/braindb.sh" "$W/links/bdb"
echo "run through a symlink to braindb.sh itself        : $(env -u WED_AGENT BRAINDB_ROOT="$FIX" BRAINDB_PGDATA="$W/pg-x" BRAINDB_SOCKDIR="$SOCK" /bin/bash "$W/links/bdb" status 2>&1 | head -1 | sh 120)"

hr "S3 nested trees"
mktree "$W/nest/TUESDAY/WEDNESDAY"; mktree "$W/nest2/WEDNESDAY/TUESDAY"
echo "TUESDAY/WEDNESDAY/2_Project_Files : $(T "$W/nest/TUESDAY/WEDNESDAY" status 2>&1 | head -1 | sh 120)"
echo "WEDNESDAY/TUESDAY/2_Project_Files : $(T "$W/nest2/WEDNESDAY/TUESDAY" status 2>&1 | head -1 | sh 120)"

hr "S4 WED_AGENT forms on a tree named WEDNESDAY"
for v in tuesday friday Wednesday "wednesday " "" all; do
  out="$(WED_AGENT="$v" BRAINDB_ROOT="$FIX" BRAINDB_PGDATA="$W/pg-x" BRAINDB_SOCKDIR="$SOCK" /bin/bash "$W/real/WEDNESDAY/2_Project_Files/brain-db/braindb.sh" status 2>&1 | head -1 | sh 140)"
  printf "WED_AGENT=%-12s -> %s\n" "'$v'" "$out"
done

hr "S5 BRAINDB_SEAT / BRAINDB_SCOPE given from outside on a WEDNESDAY tree (can an env var re-seat the indexer?)"
echo "BRAINDB_SEAT=tuesday exported by the caller: $(BRAINDB_SEAT=tuesday T "$W/real/WEDNESDAY" status 2>&1 | head -1 | sh 120)"
EXTRA="BRAINDB_SCOPE=$W/real/WEDNESDAY/2_Project_Files/brain-db/scope/tuesday.scope" T "$W/real/WEDNESDAY" rebuild 2>&1 | tail -1 | sh 200
echo "cluster created by that refused call? $([ -d "$W/pg-WEDNESDAY" ] && echo YES || echo no) ; processes: $(nprocs "$W/pg-WEDNESDAY")"

hr "S6 a TUESDAY-named tree, its proposed scope, plus allow lines a careless seat might write for the WEDNESDAY seat's records"
TT="$W/real/TUESDAY"; B="$TT/2_Project_Files/brain-db"
dumpt() { "$PGBIN/pg_dump" --data-only --schema=brain -h "$SOCK" -d braindb 2>&1; }
probe() { # probe <label> <extra scope lines...>
  local label="$1"; shift
  { cat "$B/scope/tuesday.scope"; for l in "$@"; do echo "$l"; done; } > "$W/t.scope"
  EXTRA="BRAINDB_SCOPE=$W/t.scope" T "$TT" rebuild > "$W/t-rebuild.out" 2>&1; local rc=$?
  local d; d="$(dumpt)"
  local own; own="$(printf '%s' "$d" | /usr/bin/grep -c -F xcanary23)"       # tuesday's own ledger token (control: must be present)
  printf '%-64s rc=%d | wed ledger xneighbour20=%s wed archive xneighbour21=%s wed daily xneighbour30=%s wed pickup xtasksown202=%s friday ledger xcanary22=%s friday daily xcanary38=%s | control tuesday own ledger=%s\n' \
    "$label" "$rc" "$(printf '%s' "$d" | /usr/bin/grep -c -F xneighbour20)" "$(printf '%s' "$d" | /usr/bin/grep -c -F xneighbour21)" "$(printf '%s' "$d" | /usr/bin/grep -c -F xneighbour30)" \
    "$(printf '%s' "$d" | /usr/bin/grep -c -F xtasksown202)" "$(printf '%s' "$d" | /usr/bin/grep -c -F xcanary22)" "$(printf '%s' "$d" | /usr/bin/grep -c -F xcanary38)" "$own"
  /usr/bin/grep -i -E "another seat|REFUSED|only by an" "$W/t-rebuild.out" | head -3 | sh 200
}
probe "T0 proposed tuesday.scope unchanged (control)"
probe "T1 + allow ledger 0_Brain/learnings/_ledger.md" "allow ledger 0_Brain/learnings/_ledger.md"
probe "T2 + allow ledger 0_Brain/learnings/_ledger*.md" "allow ledger 0_Brain/learnings/_ledger*.md"
probe "T3 + allow daily 0_Brain/daily/20*.md" "allow daily 0_Brain/daily/20*.md"
probe "T4 + allow skill 0_Brain/tasks/*.md" "allow skill 0_Brain/tasks/*.md"
probe "T5 + allow daily 0_Brain/daily_friday/20*.md" "allow daily 0_Brain/daily_friday/20*.md"
probe "T6 + allow ledger 0_Brain/learnings/_ledger_friday.md" "allow ledger 0_Brain/learnings/_ledger_friday.md"
echo "-- the reverse: a WEDNESDAY tree whose scope lost its deny_seat_word lines and gained Tuesday's records"
WT="$W/real/WEDNESDAY"
{ /usr/bin/grep -v -E '^deny_seat_word' "$WT/2_Project_Files/brain-db/scope/wednesday.scope"; echo "allow ledger 0_Brain/learnings/_ledger_laptop_datasec.md"; echo "allow daily 0_Brain/daily_tuesday/20*.md"; } > "$W/w.scope"
EXTRA="BRAINDB_SCOPE=$W/t.scope" T "$TT" stop > /dev/null 2>&1
EXTRA="BRAINDB_SCOPE=$W/w.scope" T "$WT" rebuild > "$W/w-rebuild.out" 2>&1; echo "rc=$? ; tuesday ledger xcanary23=$(dumpt | /usr/bin/grep -c -F xcanary23) tuesday daily xcanary37=$(dumpt | /usr/bin/grep -c -F xcanary37) (control own ledger xneighbour20=$(dumpt | /usr/bin/grep -c -F xneighbour20))"
T "$WT" stop 2>&1 | tail -1 | sh 60

hr "F2a data directory given with a trailing slash, as a relative path, through a symlink (does the identity test fail SAFE, and is anything left running?)"
X() { local pg="$1" so="$2"; shift 2; env -u WED_AGENT BRAINDB_ROOT="$FIX" BRAINDB_PGDATA="$pg" BRAINDB_SOCKDIR="$so" ${EXTRA:-} /bin/bash "$WT/2_Project_Files/brain-db/braindb.sh" "$@"; }
mkdir -p "$W/f2"
X "$W/f2/slash/" "$SOCK" init > "$W/f2-slash-init.out" 2>&1; echo "trailing slash: init rc=$?"
X "$W/f2/slash/" "$SOCK" start > "$W/f2-slash-start.out" 2>&1; echo "trailing slash: start rc=$? : $(tail -1 "$W/f2-slash-start.out" | sh 200)"
echo "   server processes with -D .../f2/slash : $(nprocs "$W/f2/slash")"
X "$W/f2/slash/" "$SOCK" status 2>&1 | tail -1 | sh 100
X "$W/f2/slash/" "$SOCK" search xneighbour01 > "$W/f2-slash-search.out" 2>&1; echo "trailing slash: search rc=$? : $(tail -1 "$W/f2-slash-search.out" | sh 200)"
X "$W/f2/slash/" "$SOCK" stop > "$W/f2-slash-stop.out" 2>&1; echo "trailing slash: stop rc=$? : $(head -1 "$W/f2-slash-stop.out" | sh 200)"
echo "   server processes STILL running after the tool's own stop: $(nprocs "$W/f2/slash")"
X "$W/f2/slash" "$SOCK" stop 2>&1 | tail -1 | sh 80; echo "   after stop with the plain spelling: $(nprocs "$W/f2/slash")"
ln -s "$W/f2/slash" "$W/f2/link"
X "$W/f2/link" "$SOCK" start > "$W/f2-link-start.out" 2>&1; echo "symlinked data dir: start rc=$? : $(tail -1 "$W/f2-link-start.out" | sh 160)"
X "$W/f2/link" "$SOCK" rebuild > "$W/f2-link-rebuild.out" 2>&1; echo "symlinked data dir: rebuild rc=$? : $(tail -1 "$W/f2-link-rebuild.out" | sh 120)"
echo "-- the SAME server addressed by its real path while it was started through the link (same cluster: accepted or refused?)"
X "$W/f2/slash" "$SOCK" status 2>&1 | tail -3 | sh 160
EXTRA="BRAINDB_NO_AUTOSTART=1" X "$W/f2/slash" "$SOCK" check 2>&1 | head -1 | sh 200;
X "$W/f2/slash" "$SOCK" stop 2>&1 | head -2 | sh 200; echo "   processes after stop by real path: $(nprocs "$W/f2/link")"
X "$W/f2/link" "$SOCK" stop 2>&1 | tail -1 | sh 100; echo "   processes after stop by link path: $(nprocs "$W/f2/link") / $(nprocs "$W/f2/slash")"

hr "F2b two clusters in ONE socket directory on different BRAINDB_PORT values; a command addressed to c2 but carrying c1's port"
X "$W/f2/c1" "$SOCK2" init > /dev/null 2>&1; X "$W/f2/c2" "$SOCK2" init > /dev/null 2>&1
EXTRA="BRAINDB_PORT=5501" X "$W/f2/c1" "$SOCK2" rebuild > "$W/f2b-c1.out" 2>&1; echo "c1 (port 5501) rebuild rc=$?"
EXTRA="BRAINDB_PORT=5502" X "$W/f2/c2" "$SOCK2" start 2>&1 | tail -1 | sh 120
ls -A "$SOCK2" | tr '\n' ' '; echo
EXTRA="BRAINDB_PORT=5501" X "$W/f2/c2" "$SOCK2" rebuild > "$W/f2b-x.out" 2>&1; echo "addressed to c2, port of c1: rebuild rc=$? : $(tail -1 "$W/f2b-x.out" | sh 150)"
for c in check "search xneighbour01" "at pane" status; do EXTRA="BRAINDB_PORT=5501" X "$W/f2/c2" "$SOCK2" $c > "$W/f2b-y.out" 2>&1; echo "addressed to c2, port of c1: $c rc=$? : $(/usr/bin/grep -i -c -E 'GREEN|result' "$W/f2b-y.out") GREEN/result lines"; done
EXTRA="BRAINDB_PORT=5501" X "$W/f2/c2" "$SOCK2" stop 2>&1 | tail -1 | sh 120; echo "   c1 processes: $(nprocs "$W/f2/c1") c2 processes: $(nprocs "$W/f2/c2")  (stop addressed to c2 must stop c2, never c1)"
EXTRA="BRAINDB_PORT=5501" X "$W/f2/c1" "$SOCK2" stop 2>&1 | tail -1 | sh 80
EXTRA="BRAINDB_PORT=5502" X "$W/f2/c2" "$SOCK2" stop 2>&1 | tail -1 | sh 80

hr "F2c TIME-OF-CHECK: the server is swapped AFTER the identity check and BEFORE the write (rebuild waits for the cluster lock in between)"
# c1 and c2 share one socket directory and port (as two trees of ONE seat on one Mac do by default: /tmp/wed-braindb-<uid>-<seat>).
# 1. c1 is up. A holder takes c1's lock (stands for any other rebuild of c1 in progress).
# 2. `rebuild` addressed to c1 passes need_server(), parses, then waits for the lock.
# 3. c1's server goes away (pg_ctl stop: stands for a crash, a kill, or another seat's stop) and c2's comes up on the same socket.
# 4. the holder lets go. Where does c1's rebuild write, and what does it print?
mkdir -p "$W/tiny/0_Brain/learnings"; printf -- '---\ntier: W\n---\n# tiny\n\nzp6token\n' > "$W/tiny/0_Brain/learnings/2026-01-01_tiny.md"
printf '# h\n2026-01-01_tiny.md\tlive\tall\tfam\tpane\t-\tA rule.\n' > "$W/tiny/0_Brain/learnings/_rules_index.tsv"; printf '# R\n\n1. rule\n' > "$W/tiny/CLAUDE.md"
SOCK3=/tmp/qa3s-c
X "$W/f2/t1" "$SOCK3" rebuild > "$W/toc-c1-first.out" 2>&1; echo "c1 built from the fixture tree: rc=$? ; files in c1: $("$PGBIN/psql" -X -At -h "$SOCK3" -d braindb -c 'select count(*) from brain.files')"
X "$W/f2/t2" "$SOCK3" init > /dev/null 2>&1
python3 -c "
import fcntl, os, sys, time
fd = os.open(sys.argv[1], os.O_RDWR | os.O_CREAT, 0o600); fcntl.flock(fd, fcntl.LOCK_EX); open(sys.argv[2], 'w').write('held'); time.sleep(12)" "$W/f2/t1.lock" "$W/holder.flag" & HOLD=$!
while [ ! -f "$W/holder.flag" ]; do sleep 0.2; done
env -u WED_AGENT BRAINDB_ROOT="$W/tiny" BRAINDB_PGDATA="$W/f2/t1" BRAINDB_SOCKDIR="$SOCK3" /bin/bash "$WT/2_Project_Files/brain-db/braindb.sh" rebuild > "$W/toc-rebuild.out" 2>&1 & RB=$!
sleep 3
"$PGBIN/pg_ctl" -D "$W/f2/t1" -m fast -w stop > "$W/toc-pgctl.out" 2>&1; echo "c1's server stopped behind the tool's back: rc=$? ; c1 processes $(nprocs "$W/f2/t1")"
X "$W/f2/t2" "$SOCK3" start 2>&1 | tail -1 | sh 120
wait $HOLD; wait $RB; echo "the rebuild ADDRESSED TO c1 finished: rc=$?"
/usr/bin/grep -i -E 'data directory|REFUSED|rebuild: |FAILED' "$W/toc-rebuild.out" | sh 200
echo "c2 (never addressed) now holds: $("$PGBIN/psql" -X -At -h "$SOCK3" -d postgres -c "select count(*) from pg_database where datname='braindb'" 2>&1) braindb database(s); files: $("$PGBIN/psql" -X -At -h "$SOCK3" -d braindb -c "select count(*)||' file(s), root '||(select right(v,12) from brain.meta where k='root') from brain.files" 2>&1 | sh 120)"
echo "which data directory does the answering server serve: $("$PGBIN/psql" -X -At -h "$SOCK3" -d postgres -c 'show data_directory' | sh 200)"
X "$W/f2/t2" "$SOCK3" check 2>&1 | head -2 | sh 200
X "$W/f2/t2" "$SOCK3" stop 2>&1 | tail -1 | sh 80; X "$W/f2/t1" "$SOCK3" stop 2>&1 | tail -1 | sh 80

hr "END"
for d in "$W"/pg-* "$W"/f2/*; do [ -f "$d/postmaster.pid" ] && echo "pid file still present: $d"; done
echo "processes with a data directory under $W: $(nprocs "$W")"
date '+%Y-%m-%d %H:%M:%S %Z'
