#!/bin/bash
# seat_f2_part2.sh - re-run of S6 and F2a after two instrument errors of mine in seat_f2.sh:
#  (1) S5 left a server on the shared socket directory (itself a finding: F4 is only half fixed), so every S6 probe failed to start (rc 1; my control caught it);
#  (2) F2a's trailing-slash init never created a cluster, so the symlink probes had nothing to address.
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3
PFC="$S/lanecopy/WEDNESDAY/2_Project_Files"; PGBIN=/opt/homebrew/opt/postgresql@15/bin
W="$S/seat2-$(date +%H%M%S)"; mkdir -p "$W" || exit 2
FIX="$W/fix"; python3 "$PFC/brain-db/tests/make_fixtures.py" "$FIX" > "$W/fx.out" 2>&1
SOCK=/tmp/qa3u; SOCK2=/tmp/qa3u-b
sh() { awk -v n="${1:-230}" '{print substr($0,1,n)}' | sed "s|$W/||g"; }
nprocs() { local snap; snap="$(ps -axww -o pid=,command=)"; printf '%s\n' "$snap" | /usr/bin/grep -F -c -- "-D $1"; }
mktree() { local t="$1/2_Project_Files"; mkdir -p "$t/fleet/cockpit" "$t/tools" "$t/brain-db/scope"
  cp "$PFC/brain-db/braindb.sh" "$PFC/brain-db/braindb_index.py" "$PFC/brain-db/braindb_lock.py" "$t/brain-db/"
  cp "$PFC/fleet/cockpit/seat_resolve.sh" "$t/fleet/cockpit/"; cp "$PFC/tools/seat_note.sh" "$t/tools/"
  cp "$PFC/brain-db/scope/wednesday.scope" "$t/brain-db/scope/"; }
hr() { echo; echo "######## $1"; }
mktree "$W/real/WEDNESDAY"; mktree "$W/real/TUESDAY"; cp "$PFC/brain-db/proposed/scope/tuesday.scope" "$W/real/TUESDAY/2_Project_Files/brain-db/scope/"
WT="$W/real/WEDNESDAY"; TT="$W/real/TUESDAY"

hr "F4 again: a scope file that EXISTS but is refused (wrong seat line; a hard-denied allow line; a typo). Is a cluster created and a server left running?"
i=0
for bad in "seat tuesday" "allow skill 4_Credentials/*.md" "alow skill 0_Brain/skills/*.md"; do
  i=$((i+1)); { /usr/bin/grep -v -E '^seat ' "$WT/2_Project_Files/brain-db/scope/wednesday.scope"; [ "$i" = 1 ] || echo "seat wednesday"; echo "$bad"; } > "$W/bad$i.scope"
  env -u WED_AGENT BRAINDB_ROOT="$FIX" BRAINDB_PGDATA="$W/pg-bad$i" BRAINDB_SOCKDIR="$SOCK2" BRAINDB_SCOPE="$W/bad$i.scope" /bin/bash "$WT/2_Project_Files/brain-db/braindb.sh" check > "$W/bad$i.out" 2>&1; rc=$?
  echo "scope with '$bad': check rc=$rc ; $(/usr/bin/grep -i -E '^braindb:' "$W/bad$i.out" | tail -1 | sh 150)"
  echo "   cluster directory created by the refused command? $([ -d "$W/pg-bad$i" ] && echo YES || echo no) ; server left running: $(nprocs "$W/pg-bad$i")"
  env -u WED_AGENT BRAINDB_ROOT="$FIX" BRAINDB_PGDATA="$W/pg-bad$i" BRAINDB_SOCKDIR="$SOCK2" /bin/bash "$WT/2_Project_Files/brain-db/braindb.sh" stop 2>&1 | tail -1 | sh 60
done

hr "S6 a TUESDAY-named tree, its proposed scope, plus allow lines a careless seat might write"
B="$TT/2_Project_Files/brain-db"
dumpt() { "$PGBIN/pg_dump" --data-only --schema=brain -h "$SOCK" -d braindb 2>&1; }
c() { printf '%s' "$D" | /usr/bin/grep -c -F -- "$1"; }
probe() { local label="$1"; shift
  { cat "$B/scope/tuesday.scope"; for l in "$@"; do echo "$l"; done; } > "$W/t.scope"
  env -u WED_AGENT BRAINDB_ROOT="$FIX" BRAINDB_PGDATA="$W/pg-tue" BRAINDB_SOCKDIR="$SOCK" BRAINDB_SCOPE="$W/t.scope" /bin/bash "$B/braindb.sh" rebuild > "$W/t-rebuild.out" 2>&1; local rc=$?
  D="$(dumpt)"
  printf '%-58s rc=%d | WED ledger xneighbour20=%s archive xneighbour21=%s daily xneighbour30=%s pickup xtasksown202=%s | FRI ledger xcanary22=%s daily xcanary38=%s | control TUE own ledger xcanary23=%s\n' \
    "$label" "$rc" "$(c xneighbour20)" "$(c xneighbour21)" "$(c xneighbour30)" "$(c xtasksown202)" "$(c xcanary22)" "$(c xcanary38)" "$(c xcanary23)"
  /usr/bin/grep -i -E "another seat|REFUSED|only by an" "$W/t-rebuild.out" | head -2 | sh 200
}
probe "T0 proposed tuesday.scope unchanged (control)"
probe "T1 + allow ledger 0_Brain/learnings/_ledger.md" "allow ledger 0_Brain/learnings/_ledger.md"
probe "T2 + allow ledger 0_Brain/learnings/_ledger*.md" "allow ledger 0_Brain/learnings/_ledger*.md"
probe "T3 + allow daily 0_Brain/daily/20*.md" "allow daily 0_Brain/daily/20*.md"
probe "T4 + allow skill 0_Brain/tasks/*.md" "allow skill 0_Brain/tasks/*.md"
probe "T5 + allow daily 0_Brain/daily_friday/20*.md" "allow daily 0_Brain/daily_friday/20*.md"
probe "T6 + allow ledger 0_Brain/learnings/_ledger_friday.md" "allow ledger 0_Brain/learnings/_ledger_friday.md"
probe "T7 + allow lesson 0_Brain/daily/20*.md" "allow lesson 0_Brain/daily/20*.md"
env -u WED_AGENT BRAINDB_ROOT="$FIX" BRAINDB_PGDATA="$W/pg-tue" BRAINDB_SOCKDIR="$SOCK" /bin/bash "$B/braindb.sh" stop 2>&1 | tail -1 | sh 60

hr "F2a data directory spelled with a trailing slash, through a symlink, and relative; the cluster exists (init by the plain path)"
X() { local pg="$1"; shift; env -u WED_AGENT BRAINDB_ROOT="$FIX" BRAINDB_PGDATA="$pg" BRAINDB_SOCKDIR="$SOCK" ${EXTRA:-} /bin/bash "$WT/2_Project_Files/brain-db/braindb.sh" "$@"; }
mkdir -p "$W/f2"; X "$W/f2/c" init > /dev/null 2>&1; echo "init (plain path) rc=$?"
ln -s "$W/f2/c" "$W/f2/link"
echo "-- started by the PLAIN path, then addressed through the symlink"
X "$W/f2/c" rebuild > "$W/a.out" 2>&1; echo "plain: rebuild rc=$? ; processes $(nprocs "$W/f2/c")"
X "$W/f2/link" status > "$W/b.out" 2>&1; echo "link: status rc=$? : $(/usr/bin/grep -i -E '^server' "$W/b.out")"
EXTRA="BRAINDB_NO_AUTOSTART=1" X "$W/f2/link" check > "$W/b2.out" 2>&1; echo "link, no self-start: check rc=$? : $(head -1 "$W/b2.out" | sh 120)"
X "$W/f2/link" search xneighbour01 > "$W/b3.out" 2>&1; echo "link, self-start ON: search rc=$? : $(tail -1 "$W/b3.out" | sh 200)"
X "$W/f2/link" stop > "$W/b4.out" 2>&1; echo "link: stop rc=$? : $(head -1 "$W/b4.out" | sh 200) ; processes $(nprocs "$W/f2/c")"
X "$W/f2/c" stop 2>&1 | tail -1 | sh 60
echo "-- started THROUGH the symlink, then addressed by the plain path"
X "$W/f2/link" start > "$W/c.out" 2>&1; echo "link: start rc=$? : $(tail -1 "$W/c.out" | sh 100)"
EXTRA="BRAINDB_NO_AUTOSTART=1" X "$W/f2/c" check > "$W/c2.out" 2>&1; echo "plain, no self-start: check rc=$? : $(head -1 "$W/c2.out" | sh 150)"
X "$W/f2/c" status > "$W/c3.out" 2>&1; echo "plain: status rc=$? : $(/usr/bin/grep -i -E '^server' "$W/c3.out")"
X "$W/f2/c" stop > "$W/c4.out" 2>&1; echo "plain: stop rc=$? : $(head -1 "$W/c4.out" | sh 200) ; processes by link spelling $(nprocs "$W/f2/link")"
X "$W/f2/link" stop 2>&1 | tail -1 | sh 60; echo "   processes: $(nprocs "$W/f2/link")"
echo "-- trailing slash on an existing cluster"
X "$W/f2/c/" start > "$W/d.out" 2>&1; echo "slash: start rc=$? : $(tail -1 "$W/d.out" | sh 160) ; processes $(nprocs "$W/f2/c")"
X "$W/f2/c/" stop > "$W/d2.out" 2>&1; echo "slash: stop rc=$? : $(head -1 "$W/d2.out" | sh 160) ; processes $(nprocs "$W/f2/c")"
X "$W/f2/c" stop 2>&1 | tail -1 | sh 60
echo "-- double slash inside the path (lock file path stays valid)"
DS="$W/f2//c"
X "$DS" start > "$W/e.out" 2>&1; echo "double slash: start rc=$? : $(tail -1 "$W/e.out" | sh 200)"
echo "   server processes for this cluster now: $(nprocs "$W/f2/c") (plain spelling) + $(nprocs "$DS") (double-slash spelling)"
X "$DS" status 2>&1 | /usr/bin/grep -i -E '^server' ; X "$DS" search xneighbour01 > "$W/e2.out" 2>&1; echo "double slash: search rc=$? : $(tail -1 "$W/e2.out" | sh 160)"
X "$DS" stop > "$W/e3.out" 2>&1; echo "double slash: stop rc=$? : $(head -1 "$W/e3.out" | sh 200)"
echo "   server processes LEFT after the tool's own stop: $(nprocs "$W/f2/c") + $(nprocs "$DS")"
X "$W/f2/c" stop 2>&1 | tail -1 | sh 80; echo "   after stop by the plain path: $(nprocs "$W/f2/c") + $(nprocs "$DS")"
"$PGBIN/pg_ctl" -D "$W/f2/c" status 2>&1 | head -1 | sh 100

hr "F2b status exit code when another cluster answers on the port given"
X "$W/f2/p1" init > /dev/null 2>&1; X "$W/f2/p2" init > /dev/null 2>&1
EXTRA="BRAINDB_PORT=5501" X "$W/f2/p1" start 2>&1 | tail -1 | sh 80; EXTRA="BRAINDB_PORT=5502" X "$W/f2/p2" start 2>&1 | tail -1 | sh 80
EXTRA="BRAINDB_PORT=5501" X "$W/f2/p2" status > "$W/st.out" 2>&1; echo "status addressed to p2 on p1's port: rc=$?"; sh 200 < "$W/st.out"
EXTRA="BRAINDB_PORT=5501" X "$W/f2/p1" stop 2>&1 | tail -1 | sh 60; EXTRA="BRAINDB_PORT=5502" X "$W/f2/p2" stop 2>&1 | tail -1 | sh 60

hr "END"; echo "processes with a data directory under $W: $(nprocs "$W")"; date '+%Y-%m-%d %H:%M:%S %Z'
