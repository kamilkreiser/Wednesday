#!/bin/bash
# tests/run.sh <scratch directory> - the brain-db test suite.
# Copies the tool into <scratch>/.../sim/WEDNESDAY (a tree named for the seat, as the tool requires) and
# runs THAT copy against a FIXTURE tree and SCRATCH clusters. It never touches the drive cluster: every
# call sets BRAINDB_ROOT, BRAINDB_PGDATA and BRAINDB_SOCKDIR. Nothing is deleted: every run makes a new
# directory, and its two socket directories are moved into it at the end.
# Each group of assertions carries a "(can fail)" line: the same assertion, pointed at a case that must
# be red. tests/mutants.sh goes further: it breaks the tool on purpose and shows this suite going red.
# macOS bash 3.2. No `cd`. stderr is kept (it lands in the run's log files or the terminal).
set -u

SCR="${1:-}"
[ -n "$SCR" ] || { echo "usage: run.sh <scratch directory outside the brain-db lane>" >&2; exit 2; }
PY="${BRAINDB_PYTHON:-python3}"
SELF="${BASH_SOURCE[0]}"; case "$SELF" in /*) ;; *) SELF="$PWD/$SELF" ;; esac
TESTS="$("$PY" -c 'import os,sys; print(os.path.dirname(os.path.realpath(sys.argv[1])))' "$SELF")"
LANE="$(dirname "$TESTS")"
PF="$(dirname "$LANE")"                      # the 2_Project_Files folder the lane sits in
[ -d "$SCR" ] || { echo "run.sh: scratch directory does not exist: $SCR" >&2; exit 2; }
SCR="$("$PY" -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$SCR")"
case "$SCR/" in "$LANE"/*) echo "run.sh: REFUSED, the scratch directory is inside the lane" >&2; exit 2 ;; esac

RUN="$SCR/braindb-test-$(date +%Y%m%d-%H%M%S)-$$"
TREE="$RUN/tree"; EXP="$RUN/expect-tree"; PGD="$RUN/pgdata-test"; GONE="$RUN/moved-aside"
SOCK="/tmp/wed-bdb-t$$"; SOCK2="/tmp/wed-bdb-t$$b"      # unique per run: two seats may run the suite at once
mkdir -p "$RUN" "$GONE" || exit 2
PGBIN=""
for d in "${BRAINDB_PGBIN:-}" /opt/homebrew/opt/postgresql@15/bin /usr/local/opt/postgresql@15/bin "$(dirname "$(command -v postgres || echo /nonexistent/postgres)")"; do
  if [ -n "$d" ] && [ -x "$d/pg_dump" ] && [ -x "$d/psql" ] && [ -x "$d/pg_ctl" ]; then PGBIN="$d"; break; fi
done
[ -n "$PGBIN" ] || { echo "run.sh: Postgres binaries not found" >&2; exit 2; }
L="0_Brain/learnings"

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  PASS  $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL  $1"; }
section() { echo; echo "== $1"; }

# mksim <NAME> [with-scope]: a tree folder of that name holding a copy of the tool, the seat resolver and
# (where this tree has it) tools/seat_note.sh. "with-scope" also copies scope/wednesday.scope.
mksim() {
  local t="$RUN/sim/$1/2_Project_Files"
  mkdir -p "$t/brain-db/scope" "$t/fleet/cockpit" "$t/tools" || return 1
  cp "$LANE/braindb.sh" "$LANE/braindb_index.py" "$LANE/braindb_lock.py" "$t/brain-db/" || return 1
  cp "$PF/fleet/cockpit/seat_resolve.sh" "$t/fleet/cockpit/" || return 1
  if [ -f "$PF/tools/seat_note.sh" ]; then cp "$PF/tools/seat_note.sh" "$t/tools/" || return 1; fi
  if [ "${2:-}" = "with-scope" ]; then cp "$LANE/scope/wednesday.scope" "$t/brain-db/scope/" || return 1; fi
}
TOOL="$RUN/sim/WEDNESDAY/2_Project_Files/brain-db/braindb.sh"
# B <args>: the WEDNESDAY copy on the fixture tree and the scratch cluster. T_SCOPE / T_SOCK / T_PGD / T_ROOT override per call.
B() {
  env -u WED_AGENT BRAINDB_ROOT="${T_ROOT:-$TREE}" BRAINDB_PGDATA="${T_PGD:-$PGD}" BRAINDB_SOCKDIR="${T_SOCK:-$SOCK}" \
    BRAINDB_SCOPE="${T_SCOPE:-}" /bin/bash "$TOOL" "$@"
}
# S <NAME> <args>: another seat's own copy (tree named TUESDAY or FRIDAY), its own scratch cluster, socket 2
S() {
  local nm="$1"; shift
  env -u WED_AGENT BRAINDB_ROOT="$TREE" BRAINDB_PGDATA="$RUN/pgdata-$nm" BRAINDB_SOCKDIR="$SOCK2" \
    /bin/bash "$RUN/sim/$nm/2_Project_Files/brain-db/braindb.sh" "$@"
}
# run <name> <args>: B with stdout+stderr to $RUN/<name>.out; sets RC.   runs <name> <SEAT> <args>: the same for S
run()  { local name="$1"; shift; B "$@" > "$RUN/$name.out" 2>&1; RC=$?; }
runs() { local name="$1"; shift; S "$@" > "$RUN/$name.out" 2>&1; RC=$?; }
rc_is()  { if [ "$RC" -eq "$2" ]; then ok "$1 (rc $RC)"; else bad "$1 (rc $RC, wanted $2)"; echo "        output: $(tail -3 "$RUN/$3.out")"; fi; }
rc_not0() { if [ "$RC" -ne 0 ]; then ok "$1 (rc $RC)"; else bad "$1 (rc 0, wanted non-zero)"; fi; }
count_in() { /usr/bin/grep -i -F -c -- "$1" "$2"; }            # fixed string; prints the count (0 with rc 1)
count_re() { /usr/bin/grep -i -E -c -- "$1" "$2"; }            # extended regex
has()    { [ "$(count_in "$1" "$2")" != "0" ]; }                # token present in file
hasnt()  { [ "$(count_in "$1" "$2")" = "0" ]; }
has_re()   { [ "$(count_re "$1" "$2")" != "0" ]; }
hasnt_re() { [ "$(count_re "$1" "$2")" = "0" ]; }
t_has()   { if has "$2" "$3"; then ok "$1"; else bad "$1 (no '$2' in $(basename "$3"))"; fi; }
t_hasnt() { if hasnt "$2" "$3"; then ok "$1"; else bad "$1 ('$2' found $(count_in "$2" "$3") time(s) in $(basename "$3"))"; fi; }
t_has_re()   { if has_re "$2" "$3"; then ok "$1"; else bad "$1 (no match for /$2/ in $(basename "$3"))"; fi; }
t_hasnt_re() { if hasnt_re "$2" "$3"; then ok "$1"; else bad "$1 (/$2/ matched $(count_re "$2" "$3") time(s) in $(basename "$3"))"; fi; }
# can_fail <description> <command...>: the command is an assertion that MUST be false here
can_fail() { local d="$1"; shift; if "$@"; then bad "(can fail) $d: the assertion passed where it must fail"; else ok "(can fail) $d"; fi; }
dump()  { "$PGBIN/pg_dump" --data-only --schema=brain -h "$SOCK" -d braindb > "$RUN/dump-$1.sql" || bad "pg_dump $1"; }
dump2() { "$PGBIN/pg_dump" --data-only --schema=brain -h "$SOCK2" -d braindb > "$RUN/dump-$1.sql" || bad "pg_dump $1"; }
sql()   { "$PGBIN/psql" -X -At -h "$SOCK" -d braindb -c "$1"; }
paths() { sql "select path from brain.files order by path" > "$RUN/paths-$1.txt" || bad "path list $1"; }
# ps is captured BEFORE grep starts, so the grep can never count itself
server_procs() { local snap; snap="$(ps -axww -o pid=,command=)"; printf '%s\n' "$snap" | /usr/bin/grep -F -c -- "-D ${1:-$PGD}"; }
alive() { [ -n "$(ps -p "$1" -o pid= | tr -d ' ')" ]; }
line_of() { sed -n "${1}p" "$2"; }                              # line N of a file
# a foreign process that DIES on the signals a stop would send (SIGINT, SIGTERM), so "still alive" can fail
# (a background child of a non-interactive bash starts with SIGINT IGNORED, and Python then leaves it ignored,
#  so the sleeper sets SIGINT back to its default itself: pg_ctl's fast stop sends SIGINT)
sleeper() { "$PY" -c 'import signal, time; signal.signal(signal.SIGINT, signal.SIG_DFL); time.sleep(600)' & SLEEPER=$!; sleep 1; }

echo "brain-db tests: run directory $RUN"
echo "started $(date '+%Y-%m-%d %H:%M:%S %Z')"

section "0. fixtures, and the tool copied into a tree named WEDNESDAY"
"$PY" "$TESTS/make_fixtures.py" "$TREE" || { echo "fixture build failed" >&2; exit 2; }
mksim WEDNESDAY with-scope || { echo "could not copy the tool" >&2; exit 2; }
[ -f "$EXP/absent.txt" ] && [ -f "$EXP/present.txt" ] && [ -f "$EXP/paths.txt" ] && [ -f "$EXP/clauses.txt" ] && ok "expectation tables written by the fixture builder ($(wc -l < "$EXP/absent.txt" | tr -d ' ') absent, $(wc -l < "$EXP/present.txt" | tr -d ' ') present, $(wc -l < "$EXP/paths.txt" | tr -d ' ') paths, $(wc -l < "$EXP/clauses.txt" | tr -d ' ') lessons to be left out)" || bad "expectation tables missing"

section "1. guards before any cluster exists"
env -u WED_AGENT BRAINDB_ROOT="$TREE" /bin/bash "$TOOL" check > "$RUN/guard-root.out" 2>&1; RC=$?
rc_not0 "BRAINDB_ROOT without BRAINDB_PGDATA is refused (a fixture tree can never reach the drive cluster)"
t_has "  and says why" "may never be loaded into the drive cluster" "$RUN/guard-root.out"
run status0 status; rc_is "status on a cluster that does not exist reports STOPPED" 3 status0
run start0 start;   rc_not0 "start with no cluster is refused"
WED_AGENT=tuesday BRAINDB_ROOT="$TREE" BRAINDB_PGDATA="$PGD" BRAINDB_SOCKDIR="$SOCK" /bin/bash "$TOOL" status > "$RUN/seat-mismatch.out" 2>&1; RC=$?
cp "$RUN/seat-mismatch.out" "$RUN/seatmm.out"; rc_is "WED_AGENT=tuesday on a tree named WEDNESDAY is refused with rc 2 (the tree decides the seat; the variable may only agree)" 2 seatmm
t_has "  and says REFUSED" "REFUSED" "$RUN/seat-mismatch.out"
WED_AGENT=wednesday BRAINDB_ROOT="$TREE" BRAINDB_PGDATA="$PGD" BRAINDB_SOCKDIR="$SOCK" /bin/bash "$TOOL" status > "$RUN/seat-match.out" 2>&1; RC=$?
rc_is "(can fail) WED_AGENT=wednesday on the same tree is accepted" 3 seat-match
mksim elsewhere with-scope
env -u WED_AGENT BRAINDB_ROOT="$TREE" BRAINDB_PGDATA="$PGD" BRAINDB_SOCKDIR="$SOCK" /bin/bash "$RUN/sim/elsewhere/2_Project_Files/brain-db/braindb.sh" status > "$RUN/seat-unknown.out" 2>&1; RC=$?
cp "$RUN/seat-unknown.out" "$RUN/seatun.out"; rc_is "a tree whose folder is not WEDNESDAY, TUESDAY or FRIDAY is refused with rc 2, never defaulted to a seat" 2 seatun
t_has "  and says REFUSED" "REFUSED" "$RUN/seat-unknown.out"
[ ! -e "$PGD" ] && ok "none of the refused commands created a cluster" || bad "a refused command created $PGD"

section "2. init"
run init1 init; rc_is "init creates the cluster" 0 init1
[ "$(stat -f '%Lp' "$PGD")" = "700" ] && ok "data directory is mode 700" || bad "data directory mode is $(stat -f '%Lp' "$PGD")"
t_has_re "postgresql.conf carries listen_addresses = ''" "^listen_addresses = ''" "$PGD/postgresql.conf"
run init2 init; rc_not0 "a second init is refused"
t_has "  and says REFUSED" "REFUSED" "$RUN/init2.out"
can_fail "init refusal: the first init did not report REFUSED" has "REFUSED" "$RUN/init1.out"
run stop0 stop; rc_is "stop on a never-started cluster is a clean no-op" 0 stop0

section "3. start, socket only"
run start1 start; rc_is "start" 0 start1
PID="$(sed -n 1p "$PGD/postmaster.pid" | tr -d ' ')"
[ "$(server_procs)" = "1" ] && ok "exactly one process runs with -D <scratch data directory> (pid $PID)" || bad "server process count is $(server_procs)"
/usr/sbin/lsof -nP -a -p "$PID" -i > "$RUN/lsof.out" 2>&1; LRC=$?
if [ "$LRC" -ne 0 ] && [ ! -s "$RUN/lsof.out" ]; then ok "the server holds no network socket (lsof -i: nothing, rc $LRC)"; else bad "the server holds a network socket: $(cat "$RUN/lsof.out")"; fi
/usr/sbin/lsof -nP -a -p "$PID" -U > "$RUN/lsof-unix.out" 2>&1
t_has "(control) the same lsof does see the Unix socket" ".s.PGSQL" "$RUN/lsof-unix.out"
run start2 start; rc_is "a second start is a no-op" 0 start2
t_has "  and says already running" "already running" "$RUN/start2.out"
run status1 status; rc_is "status reports RUNNING" 0 status1
t_has "  and names the data directory the answering server serves" "the server answering is this data directory's: $PGD" "$RUN/status1.out"

section "4. check before any rebuild is RED, rebuild makes it GREEN"
run check0 check; rc_is "check with no index is red" 1 check0
run rebuild1 rebuild; rc_is "rebuild" 0 rebuild1
sed 's/^/        /' "$RUN/rebuild1.out"
run check1 check; rc_is "check after rebuild is green" 0 check1
t_has "check prints the data directory it reports on" "data directory: $PGD" "$RUN/check1.out"
t_has "rebuild's last line says nothing was skipped for a fault" "rebuild: done; no file was unreadable and no row was truncated" "$RUN/rebuild1.out"

section "5. the indexed path set is exactly the expected set"
paths A
N_EXP="$(wc -l < "$EXP/paths.txt" | tr -d ' ')"
if diff "$EXP/paths.txt" "$RUN/paths-A.txt" > "$RUN/paths.diff" 2>&1; then ok "$N_EXP paths, exactly the expected ones"; else bad "path set differs"; sed 's/^/        /' "$RUN/paths.diff"; fi
SEATREC="daily_tuesday|daily_friday|_ledger_friday|_ledger_laptop_datasec|2_Project_Files/tuesday|0_Brain/tasks|conflict_on_|\.pre-|4_Credentials|3_Access_Keys|dashboard|reference"
t_hasnt_re "no indexed path is another seat's record, a sync leftover or a hard-excluded folder" "$SEATREC" "$RUN/paths-A.txt"
can_fail "that path assertion: with 'learnings' added to the same pattern it is red" hasnt_re "$SEATREC|learnings" "$RUN/paths-A.txt"
t_has_re "a lesson, a skill and an architecture file with another seat's word in the NAME are indexed (ANSWER-1 item 2)" "tuesday-sweeps|tuesday-ritual|tuesday-vs-wednesday" "$RUN/paths-A.txt"

section "6. QUALIFY OR STAY OUT: every planted file is absent, every neighbour is present (whole-index dump)"
dump A
while IFS='|' read -r tok why; do
  [ -n "$tok" ] || continue
  t_hasnt "absent  $tok  $why" "$tok" "$RUN/dump-A.sql"
done < "$EXP/absent.txt"
t_hasnt "absent  xcanary  ANY canary token at all" "xcanary" "$RUN/dump-A.sql"
while IFS='|' read -r tok why; do
  [ -n "$tok" ] || continue
  t_has "present $tok  $why" "$tok" "$RUN/dump-A.sql"
done < "$EXP/present.txt"
can_fail "absence assertion: pointed at a neighbour token it is red" hasnt "xneighbour01" "$RUN/dump-A.sql"
can_fail "presence assertion: pointed at a canary token it is red" has "xcanary03" "$RUN/dump-A.sql"
sql "select heading from brain.chunks where kind = 'rules' order by id" > "$RUN/rules-headings.txt" || bad "rules headings"
[ "$(wc -l < "$RUN/rules-headings.txt" | tr -d ' ')" = "8" ] && ok "the two rules files give 8 rows (1 intro, 1 section text, 3 numbered rules, 2 rules under later headings, 1 section of the brain file)" || { bad "rules rows: $(wc -l < "$RUN/rules-headings.txt")"; sed 's/^/        /' "$RUN/rules-headings.txt"; }
for h in "CLAUDE.md > Rules > rule 0" "CLAUDE.md > Rules > rule 0a" "CLAUDE.md > Rules > rule 3b-i" "CLAUDE.md > Session end > rule 1" "0_Brain/CLAUDE.md > Folders"; do
  [ "$(/usr/bin/grep -i -x -F -c -- "$h" "$RUN/rules-headings.txt")" = "1" ] && ok "one row headed: $h" || bad "no single row headed: $h"
done
[ -z "$(find "$RUN" -iname 'PWNED*' -not -path '*/pgdata-*' | head -1)$(find "$PWD" -maxdepth 1 -iname 'PWNED*' | head -1)" ] && ok "no injection string in a file name, heading, body or rules-index field created a file (find PWNED*: nothing)" || bad "a PWNED file exists: $(find "$RUN" -iname 'PWNED*' | head -3)"
[ -n "$(find "$RUN" -name 'paths.txt' | head -1)" ] && ok "(control) the same find does find a file that exists" || bad "find control failed"

section "6b. every left-out lesson is NAMED, under the clause it was planted for (N8)"
# the rebuild report -> "file name|clause", compared with the fixture builder's own table
"$PY" - "$RUN/rebuild1.out" > "$RUN/clauses-got.txt" <<'PYEOF'
import re, sys
cl = None
out = []
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"\s+clause \((\w)\) ", line)
    if m:
        cl = m.group(1); continue
    m = re.match(r"\s{11}(.+?)  \[", line)
    if m and cl:
        out.append("%s|%s" % (m.group(1), cl)); continue
    if not line.startswith("     "):
        cl = None
print("\n".join(sorted(out)))
PYEOF
N_CL="$(wc -l < "$EXP/clauses.txt" | tr -d ' ')"
if diff "$EXP/clauses.txt" "$RUN/clauses-got.txt" > "$RUN/clauses.diff" 2>&1; then ok "all $N_CL left-out lessons are named in the rebuild report, each under the clause it was planted for"; else bad "left-out lessons or their clauses differ from the plan"; sed 's/^/        /' "$RUN/clauses.diff" | head -30; fi
for c in a b c d t f; do
  n="$(/usr/bin/grep -i -c -- "|$c\$" "$EXP/clauses.txt")"
  t_has "the report counts clause ($c): $n" "clause ($c) " "$RUN/rebuild1.out"
  [ "$(/usr/bin/grep -i -E -c -- "clause \($c\) .*: $n\$" "$RUN/rebuild1.out")" = "1" ] && ok "  and the count printed for clause ($c) is $n" || bad "clause ($c) count is not $n: $(/usr/bin/grep -i -F -- "clause ($c) " "$RUN/rebuild1.out")"
done
t_has_re "the rebuild's LAST line gives the count left out by each clause" "^rebuild: done; .*; $N_CL lesson file\(s\) LEFT OUT by the qualify rule: a=[0-9]+, b=[0-9]+, c=[0-9]+, d=[0-9]+, t=[0-9]+, f=[0-9]+\$" "$RUN/rebuild1.out"
[ "$(tail -1 "$RUN/rebuild1.out" | count_in 'LEFT OUT by the qualify rule' /dev/stdin)" = "1" ] && ok "  (it is the last line)" || bad "the left-out line is not last: $(tail -1 "$RUN/rebuild1.out")"
t_has "check prints the same count" "left out: $N_CL lesson file(s) LEFT OUT by the qualify rule" "$RUN/check1.out"
t_has "  and names lessons under each clause, up to its limit" "(+" "$RUN/check1.out"
t_has "  for example the hard link, by name" "2026-09-02_f-hardlink.md  [hard link (link count 2)" "$RUN/check1.out"
t_has "the report says which rules-index lines could not be read" "could NOT be read as a row" "$RUN/rebuild1.out"
t_has "  and names a row whose lesson file does not exist" "2026-01-99_missing-lesson.md" "$RUN/rebuild1.out"
t_has "a daily note whose name is not a plain date is skipped with that reason" "not a daily-note file name" "$RUN/rebuild1.out"
t_hasnt "no Python traceback anywhere in the rebuild output" "Traceback" "$RUN/rebuild1.out"
run sLO search xcanary03; t_has "search for a left-out lesson's word says NO MATCH" "NO MATCH" "$RUN/sLO.out"
t_has "  and says that $N_CL lesson files are left out and not searched" "NOTE: $N_CL lesson file(s) are LEFT OUT" "$RUN/sLO.out"
run docLO doctor; t_has "doctor's one line carries the left-out count" "$N_CL lesson file(s) LEFT OUT" "$RUN/docLO.out"

section "6c. ROUND 4b: a lesson that merely NAMES another client is indexed (ANSWER-7, must succeed)"
for tok in xneighbour741 xneighbour742 xneighbour743 xneighbour744 xneighbour745 xneighbour746 xneighbour747 xneighbour748 xneighbour749 xneighbour749rule xneighbour750 xneighbour751; do
  t_has "present $tok  a tier W or own-project lesson naming the other client in its text, name, rule line or frontmatter" "$tok" "$RUN/dump-A.sql"
done
run sNM search xneighbour741; t_has "  and search finds one by its word" "d-ok-name-plain.md" "$RUN/sNM.out"
t_hasnt_re "  while every marker and tier-like case stays out (red-capable: the six marker forms, two comments, six tier-like lines, the numeric reference)" "xcanary7[0-9][0-9]" "$RUN/dump-A.sql"
{ cat "$LANE/scope/wednesday.scope"; echo "deny_clients datasec"; } > "$RUN/denyline.scope"
T_SCOPE="$RUN/denyline.scope" run denyline check; rc_is "a scope file that still carries a deny_clients line is refused (rc 2): the line would promise a protection that no longer exists" 2 denyline

section "7. what a scope file may ask for is a closed table in the code (N5): anything else is REFUSED at load"
NF7="$(sql "select count(*) from brain.files")"
n=0
while IFS= read -r line; do
  [ -n "$line" ] || continue
  n=$((n+1))
  { cat "$LANE/scope/wednesday.scope"; echo "$line"; } > "$RUN/wide$n.scope"
  T_SCOPE="$RUN/wide$n.scope" run wide$n rebuild
  if [ "$RC" -eq 2 ] && has "REFUSED" "$RUN/wide$n.out"; then ok "refused (rc 2): $line"; else bad "NOT refused: $line (rc $RC): $(tail -1 "$RUN/wide$n.out")"; fi
done <<'EOF'
allow daily 0_Brain/daily_tuesday/20*.md
allow daily 0_Brain/daily_friday/20*.md
allow skill 0_Brain/daily_tuesday/*.md
allow lesson 0_Brain/daily/20*.md
allow ledger 0_Brain/learnings/_ledger_friday.md
allow ledger 0_Brain/learnings/_ledger_laptop_datasec.md
allow ledger 0_Brain/learnings/_ledger*.md
allow ledger 0_Brain/learnings/_ledger_fleet_insights.md
allow skill 0_Brain/learnings/_ledger_*.md
allow skill 0_Brain/tasks/*.md
allow pickup 0_Brain/tasks/*.md
allow pickup 0_Brain/tasks/NEXT-PICKUP-TUESDAY.md
allow pickup 0_Brain/tasks/WEEK-INSTRUCTION-FRIDAY.md
allow skill 2_Project_Files/tuesday/*.md
allow rules 2_Project_Files/CLAUDE.md
allow rules_index 0_Brain/learnings/_other_index.tsv
allow architecture 1_Project_Definition/Discovery/*.md
EOF
[ "$(sql "select count(*) from brain.files")" = "$NF7" ] && ok "the index is unchanged by the $n refused scopes ($NF7 files)" || bad "the index changed"
{ cat "$LANE/scope/wednesday.scope"; echo "allow pickup 0_Brain/tasks/NEXT-PICKUP.md"; echo "allow lesson 0_Brain/learnings/*.md"; echo "allow skill 0_Brain/skills/_*.md"; } > "$RUN/own.scope"
T_SCOPE="$RUN/own.scope" run rebuildW rebuild; rc_is "(can fail) a line for this seat's OWN pickup file, and wider patterns inside the table's folders, are accepted" 0 rebuildW
dump W
t_has "  the seat's own pickup file enters, so the table is live in both directions" "xtasksown202" "$RUN/dump-W.sql"
t_hasnt_re "  and no other seat's record, ledger-named skill or planted lesson came with the wider patterns" "xcanary" "$RUN/dump-W.sql"
t_has "  a file whose name starts with '_' is never a skill or a lesson" "is a ledger, digest or index, never a" "$RUN/rebuildW.out"
# 7a. the other two seats' tables, on trees named for them: Wednesday's records are refused whatever line asks
mksim TUESDAY; mksim FRIDAY
for seatname in TUESDAY FRIDAY; do
  low="$(echo "$seatname" | tr '[:upper:]' '[:lower:]')"
  for line in "allow ledger 0_Brain/learnings/_ledger.md" "allow ledger 0_Brain/learnings/_ledger_archive.md" "allow ledger 0_Brain/learnings/_ledger*.md" "allow daily 0_Brain/daily/20*.md" "allow skill 0_Brain/tasks/*.md" "allow pickup 0_Brain/tasks/NEXT-PICKUP.md"; do
    { cat "$LANE/proposed/scope/$low.scope"; echo "$line"; } > "$RUN/sim/$seatname/2_Project_Files/brain-db/scope/$low.scope"
    runs n5$low $seatname rebuild
    if [ "$RC" -eq 2 ] && has "REFUSED" "$RUN/n5$low.out" && [ ! -e "$RUN/pgdata-$seatname" ]; then ok "a $seatname tree: '$line' is refused (rc 2) and no cluster is created"; else bad "a $seatname tree: '$line' rc $RC, cluster dir $([ -e "$RUN/pgdata-$seatname" ] && echo created || echo absent)"; fi
  done
  mv -n "$RUN/sim/$seatname/2_Project_Files/brain-db/scope/$low.scope" "$GONE/$low.scope.n5"
done
# 7b. the clauses that read the scope file are load-bearing: name this seat for the other client and its lessons enter
sed -e '/^deny_path /d' -e 's/^own_clients .*/& datasec/' "$LANE/scope/wednesday.scope" > "$RUN/permissive.scope"
T_SCOPE="$RUN/permissive.scope" run rebuildP rebuild; rc_is "rebuild under a scope that calls the other client its own" 0 rebuildP
dump P
for tok in xcanary08; do
  t_has "(can fail) under that scope $tok DOES enter, so its absence above is clause (c)'s client test at work" "$tok" "$RUN/dump-P.sql"
done
t_hasnt_re "even then: every lesson left out under (a), (b), (t) or (f), and every structural (c) and (d) case, stays out" \
  "xcanary03|xcanary17|xcanary3[0-9][0-9]|xcanary40[12]|xcanary50[1-79]|xcanary5[1-4][0-9]|xcanary7[0-9][0-9]|xcanary8[0-9][0-9]|xcanary15|xcanary680" "$RUN/dump-P.sql"
t_hasnt_re "even then: sync copies and backups stay out although the scope's deny_path lines are not what holds them" "xcanary05|xcanary06|xcanary07|xcanary24|xcanary25" "$RUN/dump-P.sql"
run checkP check; rc_is "check under the real scope is red after that rebuild" 1 checkP
run rebuild2 rebuild; rc_is "rebuild under the real scope" 0 rebuild2
dump C
t_hasnt "and every canary is gone again" "xcanary" "$RUN/dump-C.sql"
{ cat "$LANE/scope/wednesday.scope"; echo "# one more comment line"; } > "$RUN/comment.scope"
T_SCOPE="$RUN/comment.scope" run checkC check; rc_is "a scope file that differs only by a comment line makes check red (N24)" 1 checkC
t_has "  with 0 paths differing" "RED, 0 path(s) differ" "$RUN/checkC.out"
t_has "  and the reason given" "the scope file has changed since the last rebuild" "$RUN/checkC.out"

section "8. hard exclusions: a scope file that names them is refused, and the index is untouched"
n=0
while IFS= read -r line; do
  [ -n "$line" ] || continue
  n=$((n+1))
  { cat "$LANE/scope/wednesday.scope"; echo "$line"; } > "$RUN/bad$n.scope"
  T_SCOPE="$RUN/bad$n.scope" run bad$n rebuild
  if [ "$RC" -ne 0 ] && has "braindb:" "$RUN/bad$n.out"; then ok "refused: $line"; else bad "NOT refused: $line (rc $RC)"; fi
done <<'EOF'
allow skill 4_Credentials/*.md
allow skill 3_Access_Keys/*.md
allow skill 0_Brain/dashboard/*.md
allow skill 0_Brain/dashboard/data/chat_*.json
allow skill 0_Brain/reference/2026-01-01_x/*.md
allow skill 0_Brain/../4_Credentials/*.md
allow skill /etc/*.md
allow skill 0_Brain/*/notes.md
allow skill 0_Brain/skills/*
allow nonsense 0_Brain/skills/*.md
allow rules ../CLAUDE.md
allow rules *.md
allow lesson CLAUDE.md
allow skill 0_Brain/skills/4_Credentials/*.md
allow skill 0_Brain/skills_link/*.md
deny_seat_word two words
own_clients secuura general d-s
deny_clients ds
seat tuesday
alow skill 0_Brain/skills/*.md
EOF
run check2 check; rc_is "the index is unchanged by the refused rebuilds (check green)" 0 check2
mv -n "$TREE/0_Brain/people" "$GONE/people.real"; ln -s "../4_Credentials" "$TREE/0_Brain/people"
run rebuildS rebuild; rc_is "a table folder that is itself a SYMLINK (people -> 4_Credentials) still rebuilds" 0 rebuildS
dump S
t_hasnt "  but nothing behind the symlink is indexed" "xcanary" "$RUN/dump-S.sql"
t_has "  and the rebuild output names the skipped directory" "0_Brain/people/  [directory is or sits under a symlink]" "$RUN/rebuildS.out"
mv -n "$TREE/0_Brain/people" "$GONE/people.symlink"; mv -n "$GONE/people.real" "$TREE/0_Brain/people"
run rebuild3 rebuild; rc_is "back to the real scope" 0 rebuild3

section "8b. no usable rules index: the rebuild is REFUSED, not run with every lesson let in (ANSWER-3 F1 iii)"
NF0="$(sql "select count(*) from brain.files")"
mv -n "$TREE/$L/_rules_index.tsv" "$GONE/_rules_index.tsv"
run noidx rebuild; rc_not0 "rebuild with the rules index missing is refused"
t_has "  and says why" "REFUSED: lessons are on the allow-list but the rules index" "$RUN/noidx.out"
[ "$(sql "select count(*) from brain.files")" = "$NF0" ] && ok "  the index still holds its $NF0 files" || bad "the index changed: $(sql "select count(*) from brain.files") files"
dump N; t_hasnt_re "  neither other-seat lesson entered" "xcanary03|xcanary17" "$RUN/dump-N.sql"
printf '# a rules index with a header and no rows\n' > "$TREE/$L/_rules_index.tsv"
run noidx2 rebuild; rc_not0 "rebuild with a rules index that has no row is refused"
ln -s "$GONE/_rules_index.tsv" "$TREE/$L/_rules_index.tsv.tmp"; mv -n "$TREE/$L/_rules_index.tsv" "$GONE/_rules_index.header-only.tsv"; mv -n "$TREE/$L/_rules_index.tsv.tmp" "$TREE/$L/_rules_index.tsv"
run noidx3 rebuild; rc_not0 "rebuild with a rules index that is a SYMLINK is refused"
t_has "  and says it is not a plain regular file" "not a plain regular file (symlink)" "$RUN/noidx3.out"
[ "$(sql "select count(*) from brain.files")" = "$NF0" ] && ok "  the index still holds its $NF0 files" || bad "the index changed"
mv -n "$TREE/$L/_rules_index.tsv" "$GONE/_rules_index.symlink"
mv -n "$GONE/_rules_index.tsv" "$TREE/$L/_rules_index.tsv"
run check2b check; rc_is "(can fail) with the rules index back, check is green again" 0 check2b

section "9. check: red on a changed, added or removed fixture; green after rebuild"
run check3 check; rc_is "(control) green before any change" 0 check3
echo "an appended line" >> "$TREE/$L/2026-01-01_alpha-keeps-panes-open.md"
echo "an appended line" >> "$TREE/$L/2026-01-03_what-friday-does.md"
run check4 check; rc_is "red after one indexed file and one excluded file changed" 1 check4
t_has "  and names the changed path" "changed since the last rebuild: $L/2026-01-01_alpha-keeps-panes-open.md" "$RUN/check4.out"
t_hasnt "  the changed LEFT-OUT file is not named as changed (it is not in the index)" "changed since the last rebuild: $L/2026-01-03_what-friday-does.md" "$RUN/check4.out"
t_has "  and exactly one path differs" "RED, 1 path(s) differ" "$RUN/check4.out"
run rebuild4 rebuild; run check5 check; rc_is "green after rebuild" 0 check5
printf -- '---\ndate: 2026-01-18\ntier: W\n---\n\n# A new lesson\n\nxnewnorow60\n' > "$TREE/$L/2026-01-18_new.md"
run check6a check; rc_is "a NEW lesson with no rules-index row does not make check red: it does not qualify, so it is not owed to the index" 0 check6a
t_has "  but check names it as left out under clause (a)" "2026-01-18_new.md  [it has no rules-index row whose key is exactly its file name]" "$RUN/check6a.out"
printf '# A new skill\n\nxneighbour60\n' > "$TREE/0_Brain/skills/new-skill.md"
run check6 check; rc_is "red after a file was added" 1 check6
t_has "  and names it" "on disk, not in the index: 0_Brain/skills/new-skill.md" "$RUN/check6.out"
mv -n "$TREE/0_Brain/skills/ritual.md" "$GONE/ritual.md"
run check7 check; rc_is "red after a file was removed" 1 check7
t_has "  and names it" "gone from disk or now out of scope: 0_Brain/skills/ritual.md" "$RUN/check7.out"
mv -n "$GONE/ritual.md" "$TREE/0_Brain/skills/ritual.md"
i=0; while [ "$i" -lt 25 ]; do i=$((i+1)); printf '# Bulk %s\n\ntext\n' "$i" > "$TREE/0_Brain/skills/bulk-$i.md"; done
run check8 check; rc_is "red with 26 differing paths" 1 check8
[ "$(count_in 'on disk, not in the index' "$RUN/check8.out")" = "20" ] && ok "  names exactly 20 paths" || bad "named $(count_in 'on disk, not in the index' "$RUN/check8.out") paths, wanted 20"
t_has "  and counts the rest" "(+6 more)" "$RUN/check8.out"
run rebuild5 rebuild; run check9 check; rc_is "green after rebuild" 0 check9

section "9b. one bad file does not lose the rebuild (ANSWER-3 F7)"
printf -- '---\ntier: W\n---\n# locked\n\nxlocked300\n' > "$TREE/$L/2026-09-01_locked.md"; chmod 000 "$TREE/$L/2026-09-01_locked.md"
"$PY" -c "
import sys
open(sys.argv[1], 'w').write('# big\n\nxbigrow301 ' + ' '.join('w%07dx' % i for i in range(300000)) + '\n')" "$TREE/0_Brain/skills/big-row.md"
run rebuildF rebuild; rc_is "rebuild with one unreadable lesson and one 3 MB section still succeeds" 0 rebuildF
t_hasnt "  with no Python traceback" "Traceback" "$RUN/rebuildF.out"
t_has "  the unreadable file is listed" "2026-09-01_locked.md  [unreadable: PermissionError]" "$RUN/rebuildF.out"
t_has "  the truncated row is listed" "0_Brain/skills/big-row.md" "$RUN/rebuildF.out"
t_has "  and the LAST line says so" "DONE WITH FAULTS: 1 unreadable file(s) skipped, 1 row(s) truncated; they are listed above; " "$RUN/rebuildF.out"
[ "$(tail -1 "$RUN/rebuildF.out" | count_in 'DONE WITH FAULTS' /dev/stdin)" = "1" ] && ok "  (it is the last line)" || bad "the fault line is not last: $(tail -1 "$RUN/rebuildF.out")"
can_fail "fault line: the clean rebuild before it did not print it" has "DONE WITH FAULTS" "$RUN/rebuild5.out"
run checkF check; rc_is "check is green on what could be read" 0 checkF
t_has "  and reports the skipped counts" "skipped for a fault: 1 file(s) unreadable on disk now; at the last rebuild 1 unreadable, 1 row(s) truncated" "$RUN/checkF.out"
t_hasnt "  with no Python traceback" "Traceback" "$RUN/checkF.out"
run sF search xbigrow301; t_has "the truncated row is still found by a word before the cut" "0_Brain/skills/big-row.md" "$RUN/sF.out"
run sF2 search xlocked300; t_has "the unreadable file's word is not in the index" "NO MATCH" "$RUN/sF2.out"
chmod 644 "$TREE/$L/2026-09-01_locked.md"; mv -n "$TREE/$L/2026-09-01_locked.md" "$GONE/"; mv -n "$TREE/0_Brain/skills/big-row.md" "$GONE/"
run rebuild5b rebuild; run check9b check; rc_is "green and clean after the two files are moved away" 0 check9b
t_has "  the fault counts are back to zero" "0 file(s) unreadable on disk now; at the last rebuild 0 unreadable, 0 row(s) truncated" "$RUN/check9b.out"

section "10. rebuild is idempotent"
dump I1; run rebuild6 rebuild; dump I2
# pg_dump 15.19 writes a random \restrict token into every dump; it and built_at are the only lines allowed to differ
/usr/bin/grep -v -i -E 'built_at|^.(un)?restrict ' "$RUN/dump-I1.sql" > "$RUN/dump-I1.cmp"; /usr/bin/grep -v -i -E 'built_at|^.(un)?restrict ' "$RUN/dump-I2.sql" > "$RUN/dump-I2.cmp"
if cmp -s "$RUN/dump-I1.cmp" "$RUN/dump-I2.cmp"; then ok "two rebuilds give byte-identical data (built_at aside), $(wc -l < "$RUN/dump-I2.cmp" | tr -d ' ') dump lines"; else bad "two rebuilds differ"; fi
/usr/bin/grep -v -i -E 'built_at|^.(un)?restrict ' "$RUN/dump-P.sql" > "$RUN/dump-P.cmp"
can_fail "idempotence comparison: the permissive dump, filtered the same way, does differ" cmp -s "$RUN/dump-P.cmp" "$RUN/dump-I2.cmp"

section "11. search and at"
run s1 search xneighbour01; rc_is "search" 0 s1
t_has "search finds the lesson by a body word" "$L/2026-01-01_alpha-keeps-panes-open.md" "$RUN/s1.out"
t_has "  and prints its rule line" "xneighbour01rule" "$RUN/s1.out"
run s2 search "launch xneighbour30" --kind daily; t_has "search --kind daily finds the bullet with its time stamp" "2026-01-20 06:19" "$RUN/s2.out"
run s3 search xneighbour30 --kind ledger; t_has "--kind filters (the daily word is not a ledger row)" "(0 results" "$RUN/s3.out"
run s4 search xcanary03; t_has "search for an excluded file's word finds nothing" "(0 results" "$RUN/s4.out"
t_has "  and says NO MATCH, pointing at the trigger form" "NO MATCH" "$RUN/s4.out"
can_fail "NO MATCH line: a search that finds something does not print it" has "NO MATCH" "$RUN/s1.out"
run s5 search "seat thing" --kind ledger --limit 2; t_has "--limit 2 gives two results" "(2 results" "$RUN/s5.out"
run s6 search word --kind bogus; rc_not0 "an unknown --kind is refused"
run s7 search "the of and"; t_has "a query of stop words gives zero results, not an error" "(0 results" "$RUN/s7.out"
run s8 search xneighbour910; t_has "a row holding the separator bytes 0x1F and 0x1E is FOUND by search (ANSWER-3 F8)" "0_Brain/skills/separator-bytes.md" "$RUN/s8.out"
[ "$(sql "select count(*) from brain.chunks where body like '%xneighbour910%'")" = "1" ] && ok "  (control) and the database holds that row once" || bad "the row count is not 1"

echo "  -- what a result is, lessons first, rules files, weak matches"
run k1 search yakword --limit 3; rc_is "search yakword (in five ledger headlines and one lesson body)" 0 k1
sed 's/^/        /' "$RUN/k1.out"
t_has "default order says so in its header" "rules and lessons first" "$RUN/k1.out"
[ "$(line_of 2 "$RUN/k1.out" | count_re '^ 1\. .*\[lesson' /dev/stdin)" = "1" ] && ok "default: the lesson is result 1 although ledger rows score higher" || bad "default: result 1 is not the lesson: $(line_of 2 "$RUN/k1.out")"
t_has "default: incident rows follow under their own heading" "also, incident rows from the ledger and daily notes" "$RUN/k1.out"
run k2 search yakword --all --limit 3
[ "$(line_of 2 "$RUN/k2.out" | count_re '^ 1\. .*\[ledger' /dev/stdin)" = "1" ] && ok "(can fail) --all: the same search puts a ledger row first (the old mixed order)" || bad "--all: result 1 is not a ledger row: $(line_of 2 "$RUN/k2.out")"
run k3 search yakword --kind ledger --all; rc_not0 "--kind with --all is refused"
NRES="$(count_re '^ ?[0-9]+\. ' "$RUN/k2.out")"; NKIND="$(count_re '^ ?[0-9]+\. [0-9.]+  \[(rules|lesson|ledger|daily|skill|identity|people|architecture)[],]' "$RUN/k2.out")"
[ "$NRES" = "3" ] && [ "$NKIND" = "3" ] && ok "every result line carries its kind ($NKIND of $NRES)" || bad "result lines $NRES, with a kind $NKIND"
t_has_re "the last line states the first result's score and which of the question's rarest words it holds" "first result: score [0-9.]+; it holds all 1 of the question's rarest words \[yakword\]" "$RUN/k2.out"
t_hasnt "no result is called weak or strong: the line states facts only (ANSWER-3 F10)" "WEAK" "$RUN/k2.out"
run z1 search zebraword --limit 3
sed 's/^/        /' "$RUN/z1.out"
[ "$(line_of 2 "$RUN/z1.out" | count_re '^ 1\. .*\[rules\]  CLAUDE.md:' /dev/stdin)" = "1" ] && ok "a rules-file row that matches well is result 1, ahead of the lesson" || bad "result 1 is not the rules row: $(line_of 2 "$RUN/z1.out")"
t_has "  its heading names the file, section and rule" "CLAUDE.md > Rules > rule 0" "$RUN/z1.out"
t_has "  its last line says the row holds the question's one rare word" "it holds all 1 of the question's rarest words [zebraword]" "$RUN/z1.out"
run z2 search zebraword xneighbour21z --limit 3
[ "$(line_of 2 "$RUN/z2.out" | count_re '^ 1\. .*\[lesson' /dev/stdin)" = "1" ] && ok "(can fail) a rules row that holds only ONE of the question's two rare words is not put first: the lesson holding both is result 1" || bad "result 1 is not the lesson: $(line_of 2 "$RUN/z2.out")"
run z5 search "everything that lives on the drive, zebraword"
[ "$(line_of 2 "$RUN/z5.out" | count_re '^ 1\. .*\[rules\]  CLAUDE.md:' /dev/stdin)" = "1" ] && ok "a longer question whose rare words are ALL in the rule still puts the rules row first" || bad "result 1 is not the rules row: $(line_of 2 "$RUN/z5.out")"
run z3 search zebraword qqqnotaword qqqalsonot qqqnorthis
t_has "when the first result lacks most of the question's rare words, the last line says how many it holds and lacks" "of the question's 4 rarest words it holds 1 [zebraword] and lacks 3 [" "$RUN/z3.out"
t_has "  and names the words it lacks" "qqqnotaword" "$RUN/z3.out"
t_hasnt "  it gives no verdict (no WEAK MATCH line: no threshold separated right from wrong on 34 questions)" "WEAK" "$RUN/z3.out"
can_fail "that statement: a result holding every rare word does not print 'lacks'" has "and lacks" "$RUN/z1.out"
run z4 search xneighbour72 --kind rules; t_has "--kind rules finds numbered rule 0a" "CLAUDE.md > Rules > rule 0a" "$RUN/z4.out"
BRAINDB_TOPK=abc run z6 search zebraword; rc_not0 "BRAINDB_TOPK that is not 1 to 6 is refused"
t_hasnt "  with a plain message, not a traceback" "Traceback" "$RUN/z6.out"
run a1 at pane; rc_is "at pane" 0 a1
sed 's/^/        /' "$RUN/a1.out"
t_has "at pane lists three rules (the lesson named for tuesday but scoped all is among them)" "Rules for: pane (3)" "$RUN/a1.out"
[ "$(line_of 4 "$RUN/a1.out" | count_in 'xneighbour02rule' /dev/stdin)" = "1" ] && ok "third: the never-cited rule of the lesson with 'tuesday' in its name" || bad "third line is not the tuesday-named lesson's rule"
[ "$(sed -n 2p "$RUN/a1.out" | /usr/bin/grep -i -E -c '×3\].*xneighbour01rule')" = "1" ] && ok "most reinforced first: the lesson cited 3 times in this seat's ledgers" || bad "first line is not the x3 rule"
[ "$(sed -n 3p "$RUN/a1.out" | /usr/bin/grep -i -E -c '×2\].*xneighbour11rule')" = "1" ] && ok "second: cited once plus one passed on by the superseded lesson (the laptop_datasec ledger's 3 citations are NOT counted)" || bad "second line is not the x2 rule"
t_hasnt_re "another seat's rule, a superseded rule and excluded lessons' rules are not listed" "xneighbour19rulea|old wording|xcanary" "$RUN/a1.out"
run a2 at 'pane; drop schema brain cascade'; rc_not0 "a trigger that is not one plain word is refused"
run a2b at pane --top -5; rc_not0 "at --top with a negative number is refused"
echo "  -- N9: whether a rules row leads does not depend on --limit"
run q1 search quillwort marshwort; run q2 search quillwort marshwort --limit 20; run q3 search quillwort marshwort --limit 1
for q in q1 q2 q3; do
  [ "$(line_of 2 "$RUN/$q.out" | count_re '^ 1\. .*\[rules\]  CLAUDE.md:' /dev/stdin)" = "1" ] && ok "the rules row holding both rare words is result 1 ($q: default limit, --limit 20, --limit 1)" || bad "$q: result 1 is not the rules row: $(line_of 2 "$RUN/$q.out")"
done
[ "$(sql "select count(*) from brain.chunks where kind = 'lesson' and slug like 'quillwort%'")" = "8" ] && ok "(control) eight lessons outscore that row on those words, so before the cut it was not in the first five" || bad "the N9 filler lessons are not indexed"
B at $'pane\n' > "$RUN/a3.out" 2>&1; RC=$?; rc_not0 "a trigger with a trailing newline is refused"
B at "$(printf 'pane\nq')" > "$RUN/a4.out" 2>&1; RC=$?; rc_not0 "a trigger holding a newline is refused"
run check10 check; rc_is "  and the index is intact" 0 check10

section "12. other seats: each from its OWN tree (a copy of the tool in a tree named TUESDAY, then FRIDAY)"
runs t0 TUESDAY check; rc_not0 "a seat with no scope file is refused"
t_has "  and says why" "no scope file for seat 'tuesday'" "$RUN/t0.out"
[ ! -e "$RUN/pgdata-TUESDAY" ] && ok "  and NOTHING was created: no cluster directory (ANSWER-3 F4)" || bad "the refused command created a cluster directory"
[ "$(server_procs "$RUN/pgdata-TUESDAY")" = "0" ] && ok "  and no server was started" || bad "the refused command left a server running"
for c in rebuild search at up; do
  runs t0$c TUESDAY $c pane
  if [ "$RC" -ne 0 ] && [ ! -e "$RUN/pgdata-TUESDAY" ]; then ok "  the same for '$c': refused, nothing created"; else bad "'$c' with no scope file: rc $RC, cluster dir $([ -e "$RUN/pgdata-TUESDAY" ] && echo created || echo absent)"; fi
done
runs t0d TUESDAY doctor; rc_is "  doctor on a seat with no scope file says 'not adopted' and is rc 0" 0 t0d
T_SCOPE="$LANE/proposed/scope/tuesday.scope" run t1 rebuild; rc_not0 "the wednesday seat cannot use the tuesday scope file"
cp -n "$LANE/proposed/scope/tuesday.scope" "$RUN/sim/TUESDAY/2_Project_Files/brain-db/scope/tuesday.scope"
runs t2 TUESDAY rebuild; rc_is "(can fail) once its scope file is in place the tuesday tree builds on the fixtures" 0 t2
dump2 T
for tok in xcanary23 xcanary37 xcanary08 xcanary17 xcanary401 xcanary402 xneighbour741 xneighbour748 xneighbour730 xneighbour02 xneighbour01 xneighbour46 xneighbour71; do t_has "tuesday scope: present $tok" "$tok" "$RUN/dump-T.sql"; done
for tok in xneighbour20 xneighbour30 xneighbour10 xneighbour403 xcanary38 xcanary22 xcanary03 xcanary15 xcanary47 xcanary77 xcanary680 xcanary301 xcanary501 xcanary701 xcanary801 xtasksown202; do t_hasnt "tuesday scope: absent  $tok" "$tok" "$RUN/dump-T.sql"; done
runs t3 TUESDAY stop; rc_is "tuesday's server stopped" 0 t3
cp -n "$LANE/proposed/scope/friday.scope" "$RUN/sim/FRIDAY/2_Project_Files/brain-db/scope/friday.scope"
runs f2 FRIDAY rebuild; rc_is "the friday tree builds on the fixtures with its proposed scope" 0 f2
dump2 F
for tok in xcanary22 xcanary38 xcanary03 xcanary08 xcanary401 xneighbour741 xneighbour10 xneighbour01 xneighbour02 xneighbour404 xneighbour730; do t_has "friday scope: present $tok" "$tok" "$RUN/dump-F.sql"; done
for tok in xneighbour20 xneighbour30 xneighbour403 xcanary37 xcanary23 xcanary17 xcanary15 xcanary47 xcanary77 xcanary680 xcanary301 xcanary501 xcanary701 xcanary801; do t_hasnt "friday scope: absent  $tok" "$tok" "$RUN/dump-F.sql"; done
runs f3 FRIDAY stop; rc_is "friday's server stopped" 0 f3
[ "$(server_procs "$RUN/pgdata-TUESDAY")$(server_procs "$RUN/pgdata-FRIDAY")" = "00" ] && ok "no other-seat test server is left" || bad "an other-seat test server is still running"

section "12b. a command can only act on the cluster it is addressed to (ANSWER-3 F2, the checker's P6)"
T_PGD="$RUN/pgdata-c2" run c2init init; rc_is "a second cluster c2 is created and left STOPPED" 0 c2init
NF1="$(sql "select count(*) from brain.files")"; ROOT1="$(sql "select v from brain.meta where k='root'")"
mkdir -p "$RUN/tiny/0_Brain/learnings"; printf -- '---\ntier: W\n---\n# tiny\n\nztinytoken\n' > "$RUN/tiny/0_Brain/learnings/2026-01-01_tiny.md"
printf '# idx\n2026-01-01_tiny.md\tlive\tall\tlearning-loop\tpane\t-\tWhen tiny: do it.\n' > "$RUN/tiny/0_Brain/learnings/_rules_index.tsv"
BRAINDB_NO_AUTOSTART=1 T_PGD="$RUN/pgdata-c2" T_ROOT="$RUN/tiny" run p6b rebuild
rc_is "with self-start OFF, a rebuild addressed to c2 while the main cluster answers on the same socket directory is REFUSED" 4 p6b
t_has "  and says which data directory answered and which was addressed" "serves data directory '$PGD', but this command is addressed to '$RUN/pgdata-c2'" "$RUN/p6b.out"
[ "$(sql "select count(*) from brain.files")" = "$NF1" ] && [ "$(sql "select v from brain.meta where k='root'")" = "$ROOT1" ] && ok "  the main cluster's index is untouched ($NF1 files, same tree)" || bad "the main cluster's index was overwritten: $(sql "select count(*) from brain.files") files, root $(sql "select v from brain.meta where k='root'")"
BRAINDB_NO_AUTOSTART=1 T_PGD="$RUN/pgdata-c2" T_ROOT="$RUN/tiny" run p6c check
rc_is "  a check addressed to c2 is refused the same way; it does NOT read GREEN off the other cluster" 4 p6c
t_hasnt "  (no GREEN line was printed)" "GREEN" "$RUN/p6c.out"
BRAINDB_NO_AUTOSTART=1 T_PGD="$RUN/pgdata-c2" T_ROOT="$RUN/tiny" run p6s search ztinytoken; rc_is "  search likewise" 4 p6s
BRAINDB_NO_AUTOSTART=1 T_PGD="$RUN/pgdata-c2" T_ROOT="$RUN/tiny" run p6a at pane; rc_is "  at likewise" 4 p6a
T_PGD="$RUN/pgdata-c2" T_ROOT="$RUN/tiny" run p6d doctor; rc_is "  doctor for c2 warns" 1 p6d
t_has "    that ANOTHER cluster is answering, not 'index current'" "ANOTHER cluster is answering" "$RUN/p6d.out"
T_PGD="$RUN/pgdata-c2" T_ROOT="$RUN/tiny" run p6e rebuild; rc_not0 "with self-start ON the same rebuild also fails safely"
[ "$(sql "select count(*) from brain.files")" = "$NF1" ] && ok "  and the main index is still untouched" || bad "the main index changed"
run p6ok check; rc_is "(can fail) the same check addressed to the main cluster is accepted and green" 0 p6ok
run doc1 doctor; rc_is "doctor for the main cluster: rc 0" 0 doc1
t_has "  it says index current and names the data directory" "OK brain-db: index current, $PGD" "$RUN/doc1.out"
[ "$(server_procs "$RUN/pgdata-c2")" = "0" ] && ok "c2 was never started" || bad "c2 is running"

section "12c. the right database INSIDE the same session (N3; the second checker's F2c, lifted)"
X() { local pg="$1"; shift; env -u WED_AGENT BRAINDB_ROOT="${X_ROOT:-$RUN/tiny}" BRAINDB_PGDATA="$pg" BRAINDB_SOCKDIR="$SOCK2" /bin/bash "$TOOL" "$@"; }
psql2() { "$PGBIN/psql" -X -At -h "$SOCK2" -d "${2:-braindb}" -c "$1"; }
holder() { # holder <lock file> <flag written once held> <file whose appearance releases it>
  "$PY" -c "
import fcntl, os, sys, time
fd = os.open(sys.argv[1], os.O_RDWR | os.O_CREAT, 0o600); fcntl.flock(fd, fcntl.LOCK_EX); open(sys.argv[2], 'w').write('held')
t = time.time()
while not os.path.exists(sys.argv[3]) and time.time() - t < 90: time.sleep(0.1)" "$1" "$2" "$3" & HOLD=$!
  while [ ! -f "$2" ]; do sleep 0.1; done
}
waitfor() { local i=0; while [ ! -e "$1" ] && [ "$i" -lt 300 ]; do sleep 0.1; i=$((i+1)); done; [ -e "$1" ]; }
mkdir -p "$RUN/tiny2/0_Brain/learnings"; printf -- '---\ntier: W\n---\n# tiny two\n\nztwotoken\n' > "$RUN/tiny2/0_Brain/learnings/2026-01-02_tiny.md"
printf '# idx\n2026-01-02_tiny.md\tlive\tall\tlearning-loop\tpane\t-\tWhen tiny: do it.\n' > "$RUN/tiny2/0_Brain/learnings/_rules_index.tsv"
X_ROOT="$RUN/tiny2" X "$RUN/f2c-t2" rebuild > "$RUN/f2c-t2-build.out" 2>&1; RC=$?; rc_is "cluster t2 is built from its own tree (one file, token ztwotoken)" 0 f2c-t2-build
X_ROOT="$RUN/tiny2" X "$RUN/f2c-t2" stop > "$RUN/f2c-t2-stop.out" 2>&1
X "$RUN/f2c-t1" rebuild > "$RUN/f2c-t1-build.out" 2>&1; RC=$?; rc_is "cluster t1 is built from the other tree, on the SAME socket directory, and is the one answering" 0 f2c-t1-build
# -- control: a rebuild that waits for the lock and is NOT swapped succeeds
holder "$RUN/f2c-t1.lock" "$RUN/f2c-h0.flag" "$RUN/f2c-h0.release"
X "$RUN/f2c-t1" rebuild > "$RUN/f2c-control.out" 2>&1 & RB=$!
sleep 2; alive "$RB" && ok "(control) a rebuild behind a lock holder waits" || bad "the rebuild did not wait for the lock"
touch "$RUN/f2c-h0.release"; wait "$HOLD"; wait "$RB"; RC=$?; rc_is "(can fail) and, with no swap, ends rc 0 once the holder lets go" 0 f2c-control
# -- A. the checker's F2c: the server is swapped while the rebuild waits for the lock
holder "$RUN/f2c-t1.lock" "$RUN/f2c-h1.flag" "$RUN/f2c-h1.release"
X "$RUN/f2c-t1" rebuild > "$RUN/f2c-a.out" 2>&1 & RB=$!
sleep 2
"$PGBIN/pg_ctl" -D "$RUN/f2c-t1" -m fast -w stop > "$RUN/f2c-a-pgctl.out" 2>&1 || bad "could not stop t1 behind the tool's back"
X_ROOT="$RUN/tiny2" X "$RUN/f2c-t2" start > "$RUN/f2c-a-t2start.out" 2>&1 || bad "could not start t2"
touch "$RUN/f2c-h1.release"; wait "$HOLD"; wait "$RB"; RC=$?
rc_is "A. swapped during the lock wait: the rebuild addressed to t1 is REFUSED with rc 4" 4 f2c-a
t_has "  it names the directory that answered and the one addressed" "serves data directory '$RUN/f2c-t2', but this command is addressed to '$RUN/f2c-t1'" "$RUN/f2c-a.out"
t_hasnt "  it does not print 'rebuild: done'" "rebuild: done" "$RUN/f2c-a.out"
[ "$(psql2 "select count(*) from brain.chunks where body like '%ztwotoken%'")" = "1" ] && [ "$(psql2 "select count(*) from brain.chunks where body like '%ztinytoken%'")" = "0" ] && [ "$(psql2 "select count(*) from brain.files")" = "2" ] \
  && ok "  t2, never addressed, still holds its own index and nothing of t1's tree" || bad "t2 was written to: $(psql2 "select count(*) from brain.files") files, ztinytoken $(psql2 "select count(*) from brain.chunks where body like '%ztinytoken%'")"
# -- B. the narrowest window: swapped AFTER the tool's last separate session and BEFORE the load session opens
X_ROOT="$RUN/tiny2" X "$RUN/f2c-t2" stop > "$RUN/f2c-b-t2stop.out" 2>&1; X "$RUN/f2c-t1" start > "$RUN/f2c-b-t1start.out" 2>&1 || bad "could not restart t1"
BRAINDB_TEST_HOLD="$RUN/f2c-hold" X "$RUN/f2c-t1" rebuild > "$RUN/f2c-b.out" 2>&1 & RB=$!
waitfor "$RUN/f2c-hold.waiting" && ok "B. the rebuild has passed every separate check and is about to open its load session" || bad "the rebuild never reached the hold point"
"$PGBIN/pg_ctl" -D "$RUN/f2c-t1" -m fast -w stop > "$RUN/f2c-b-pgctl.out" 2>&1 || bad "could not stop t1"
X_ROOT="$RUN/tiny2" X "$RUN/f2c-t2" start > "$RUN/f2c-b-t2start.out" 2>&1 || bad "could not start t2"
touch "$RUN/f2c-hold"; wait "$RB"; RC=$?
rc_is "  swapped at that point: REFUSED with rc 4 by the assertion INSIDE the load transaction" 4 f2c-b
t_has "  the refusal is the data-directory one" "serves data directory '$RUN/f2c-t2'" "$RUN/f2c-b.out"
[ "$(psql2 "select count(*) from brain.chunks where body like '%ztwotoken%'")" = "1" ] && [ "$(psql2 "select count(*) from brain.chunks where body like '%ztinytoken%'")" = "0" ] \
  && ok "  and t2's index is untouched (the transaction never dropped or loaded anything)" || bad "t2 was written to by a rebuild addressed to t1"
for c in "check" "search ztwotoken" "at pane"; do
  BRAINDB_NO_AUTOSTART=1 X "$RUN/f2c-t1" $c > "$RUN/f2c-read.out" 2>&1; RC=$?
  rc_is "  a '$c' addressed to t1 while t2 answers is refused in its own session" 4 f2c-read
  t_hasnt_re "    and printed no result or GREEN line off the other cluster" "GREEN|ztwotoken|Rules for" "$RUN/f2c-read.out"
done
X_ROOT="$RUN/tiny2" X "$RUN/f2c-t2" stop > "$RUN/f2c-t2-stop2.out" 2>&1; RC=$?; rc_is "t2 stopped" 0 f2c-t2-stop2
[ "$(server_procs "$RUN/f2c-")" = "0" ] && ok "no F2c server is left" || bad "an F2c server is still running"

section "12d. spellings of the data directory, exit codes, the lock wait (N10, N11, N13)"
T_PGD="$PGD/" run n10a status; rc_is "the data directory spelled with a trailing slash is the same running cluster" 0 n10a
t_has "  status prints the one real spelling" "data directory: $PGD" "$RUN/n10a.out"
T_PGD="$RUN//pgdata-test" run n10b start; rc_is "spelled with a doubled slash: start says already running" 0 n10b
t_has "  (already running)" "already running" "$RUN/n10b.out"
ln -s "$PGD" "$RUN/pglink"
T_PGD="$RUN/pglink" BRAINDB_NO_AUTOSTART=1 run n10c check; rc_is "addressed through a symlink to the data directory: check is green for the same cluster" 0 n10c
[ "$(server_procs)" = "1" ] && ok "  still exactly one server for it" || bad "server count is $(server_procs)"
BRAINDB_PORT=5502 T_PGD="$RUN/pgdata-c2" run n11a start; rc_is "c2 is started on its own socket name in the SAME socket directory" 0 n11a
BRAINDB_PORT=5432 T_PGD="$RUN/pgdata-c2" T_ROOT="$RUN/tiny" run n11b status
rc_is "status addressed to c2 on the main cluster's socket prints REFUSED and exits 4, not 0 (N11)" 4 n11b
t_has "  (it printed REFUSED)" "REFUSED: the server answering" "$RUN/n11b.out"
BRAINDB_PORT=5502 T_PGD="$RUN/pgdata-c2" T_ROOT="$RUN/tiny" run n11c status; rc_is "(can fail) on its own socket the same status is rc 0" 0 n11c
BRAINDB_PORT=5502 T_PGD="$RUN/pgdata-c2" run n11d stop; rc_is "c2 stopped" 0 n11d
BRAINDB_PORT=5999 BRAINDB_NO_AUTOSTART=1 run n11e check; rc_is "no server on the socket named: rc 3" 3 n11e
t_has "  it says 'not answering'" "is not answering" "$RUN/n11e.out"
t_hasnt_re "  and never claims another cluster answered" "REFUSED|unknown" "$RUN/n11e.out"
holder "$PGD.lock" "$RUN/n13.flag" "$RUN/n13.release"
BRAINDB_LOCK_WAIT=2 run n13a rebuild; rc_is "a rebuild behind a holder that never lets go gives up at its limit: rc 75 (N13)" 75 n13a
t_has "  with the same words as the lock wrapper" "another braindb command has held $PGD.lock for more than 2 s; nothing was done" "$RUN/n13a.out"
BRAINDB_LOCK_WAIT=2 run n13b stop; rc_is "  stop behind the same holder gives up the same way" 75 n13b
t_has "  with the same words" "another braindb command has held $PGD.lock for more than 2 s; nothing was done" "$RUN/n13b.out"
touch "$RUN/n13.release"; wait "$HOLD"
run n13c check; rc_is "(can fail) with the holder gone the index is intact and green" 0 n13c

section "12e. a scope file that EXISTS but is refused creates nothing (N7)"
i=0
for badline in "seat tuesday" "allow skill 4_Credentials/*.md" "alow skill 0_Brain/skills/*.md" "allow ledger 0_Brain/learnings/_ledger_friday.md"; do
  i=$((i+1))
  { if [ "$i" = 1 ]; then /usr/bin/grep -v -i -E '^seat ' "$LANE/scope/wednesday.scope"; else cat "$LANE/scope/wednesday.scope"; fi; echo "$badline"; } > "$RUN/n7-$i.scope"
  for c in check rebuild "search x" up; do
    T_SCOPE="$RUN/n7-$i.scope" T_PGD="$RUN/pgdata-n7" T_SOCK="$SOCK2" run n7 $c
    if [ "$RC" -eq 2 ] && [ ! -e "$RUN/pgdata-n7" ] && [ ! -e "$RUN/pgdata-n7.lock" ] && [ "$(server_procs "$RUN/pgdata-n7")" = "0" ]; then ok "scope with '$badline': '$c' is rc 2 and created no cluster, no lock file and no server"; else bad "scope with '$badline': '$c' rc $RC, cluster dir $([ -e "$RUN/pgdata-n7" ] && echo CREATED || echo absent), servers $(server_procs "$RUN/pgdata-n7")"; fi
  done
done
T_PGD="$RUN/pgdata-n7" T_SOCK="$SOCK2" run n7stop stop     # a no-op, unless a broken guard let a server start
T_PGD="$RUN/pgdata-n7" T_SOCK="$SOCK2" T_SCOPE="$RUN/n7-2.scope" run n7doc doctor; t_hasnt "doctor on a seat with a refused scope does not print OK" "OK brain-db" "$RUN/n7doc.out"

section "12f. a file swapped for a symlink while rebuilds run never gets read (N6)"
printf '# secret\n\nzsecretswap\n' > "$TREE/4_Credentials/swap-secret.md"
"$PY" - "$TREE/0_Brain/skills/swap.md" "$TREE/4_Credentials/swap-secret.md" "$RUN/swap.stop" <<'PYEOF' &
import os, sys
target, secret, stop = sys.argv[1:4]
d = os.path.dirname(target); n = 0
while not os.path.exists(stop):
    a = os.path.join(d, ".swap-a"); b = os.path.join(d, ".swap-b")
    with open(a, "w") as f: f.write("# swap\n\nzswapregular\n")
    os.replace(a, target)
    os.symlink(secret, b); os.replace(b, target)
    n += 1
open(stop + ".n", "w").write(str(n))
PYEOF
FLIP=$!
hits=0; reg=0; sym=0; i=0
while [ "$i" -lt 14 ]; do
  i=$((i+1)); run swap$i rebuild; dump X
  hasnt "zsecretswap" "$RUN/dump-X.sql" || hits=$((hits+1))
  hasnt "zswapregular" "$RUN/dump-X.sql" || reg=$((reg+1))
  hasnt "0_Brain/skills/swap.md  [symlink]" "$RUN/swap$i.out" || sym=$((sym+1))
done
touch "$RUN/swap.stop"; wait "$FLIP"
[ "$hits" = "0" ] && ok "14 rebuilds while the file flipped $(cat "$RUN/swap.stop.n") times: the 4_Credentials text entered the index in 0 of them" || bad "the 4_Credentials text entered the index in $hits of 14 rebuilds"
[ "$reg" -gt 0 ] && [ "$sym" -gt 0 ] && ok "(control) the instrument saw both states: indexed as a regular file $reg time(s), skipped as a symlink $sym time(s)" || bad "the flip was not seen in both states (regular $reg, symlink $sym): the test proved nothing"
mv -n "$TREE/0_Brain/skills/swap.md" "$GONE/swap-final-state"; mv -n "$TREE/4_Credentials/swap-secret.md" "$GONE/"
run rebuildX rebuild; run checkX check; rc_is "green again with the swapped file moved away" 0 checkX

section "13. stop, and on-demand start"
[ "$(server_procs)" = "1" ] && ok "(control) one server process before stop" || bad "server process count before stop is $(server_procs)"
run stop1 stop; rc_is "stop" 0 stop1
[ "$(server_procs)" = "0" ] && ok "no process is left with -D <scratch data directory>" || bad "a server process is still alive"
alive "$PID" && bad "pid $PID is alive" || ok "pid $PID is gone"
run stop2 stop; rc_is "a second stop is a clean no-op" 0 stop2
t_has "  and says not running" "not running" "$RUN/stop2.out"
run status2 status; rc_is "status reports STOPPED" 3 status2
BRAINDB_NO_AUTOSTART=1 run check13 check; rc_is "with BRAINDB_NO_AUTOSTART=1 check on a stopped server is rc 3, and starts nothing" 3 check13
[ "$(server_procs)" = "0" ] && ok "  nothing was started" || bad "a server was started"
run doc2 doctor; rc_is "doctor on a stopped server: rc 0" 0 doc2
t_has "  it says the server is stopped (on demand)" "OK brain-db: server stopped" "$RUN/doc2.out"
[ "$(server_procs)" = "0" ] && ok "  and doctor started nothing" || bad "doctor started a server"
run auto1 search xneighbour01; rc_is "search on a stopped server brings it up itself" 0 auto1
t_has "  and answers" "$L/2026-01-01_alpha-keeps-panes-open.md" "$RUN/auto1.out"
[ "$(server_procs)" = "1" ] && ok "  one server is now running" || bad "server process count is $(server_procs)"
run stop1b stop; rc_is "stop again" 0 stop1b
run auto2 check; rc_is "check on a stopped server brings it up itself and is green" 0 auto2
run stop1c stop
run auto3 at pane; rc_is "at on a stopped server brings it up itself" 0 auto3
run stop1d stop; rc_is "stop again" 0 stop1d
[ "$(server_procs)" = "0" ] && ok "no server is left" || bad "a server is still alive"

section "13b. two commands at once (ANSWER-3 F5)"
B search xneighbour01 > "$RUN/race-a.out" 2>&1 & RA=$!
B search xneighbour01 > "$RUN/race-b.out" 2>&1 & RB=$!
wait $RA; RCA=$?; wait $RB; RCB=$?
[ "$RCA" = "0" ] && [ "$RCB" = "0" ] && ok "two self-starting searches on a STOPPED cluster both succeed (rc $RCA, rc $RCB)" || bad "racing searches: rc $RCA and rc $RCB: $(tail -1 "$RUN/race-a.out") / $(tail -1 "$RUN/race-b.out")"
[ "$(server_procs)" = "1" ] && ok "  exactly one server is running" || bad "server process count is $(server_procs)"
run stop1e stop
B start > "$RUN/race-c.out" 2>&1 & RA=$!
B start > "$RUN/race-d.out" 2>&1 & RB=$!
wait $RA; RCA=$?; wait $RB; RCB=$?
[ "$RCA" = "0" ] && [ "$RCB" = "0" ] && ok "two starts at once both succeed (rc $RCA, rc $RCB)" || bad "racing starts: rc $RCA and rc $RCB"
run stop1f stop
t=0; RACE_OK=1
while [ "$t" -lt 3 ]; do
  t=$((t+1))
  T_PGD="$RUN/pgdata-race$t" T_SOCK="$SOCK2" B search xneighbour01 > "$RUN/race$t-a.out" 2>&1 & RA=$!
  T_PGD="$RUN/pgdata-race$t" T_SOCK="$SOCK2" B search xneighbour01 > "$RUN/race$t-b.out" 2>&1 & RB=$!
  wait $RA; RCA=$?; wait $RB; RCB=$?
  if [ "$RCA" != "0" ] || [ "$RCB" != "0" ] || [ ! -f "$RUN/pgdata-race$t/PG_VERSION" ]; then RACE_OK=0; echo "        trial $t: rc $RCA, rc $RCB, PG_VERSION $([ -f "$RUN/pgdata-race$t/PG_VERSION" ] && echo present || echo MISSING): $(tail -1 "$RUN/race$t-a.out") / $(tail -1 "$RUN/race$t-b.out")"; fi
  T_PGD="$RUN/pgdata-race$t" T_SOCK="$SOCK2" run race$t-stop stop
done
[ "$RACE_OK" = "1" ] && ok "two self-starting searches with NO cluster at all: both succeed and the new cluster survives, 3 trials of 3" || bad "a double init lost a command or the cluster (see the trial lines above)"
[ "$(server_procs "$RUN/pgdata-race")" = "0" ] && ok "  no race server is left" || bad "a race server is still running"

section "14. stop and start never touch a process that is not this cluster's server (ANSWER-3 F6, F9)"
sleeper
printf '%s\n%s\n' "$SLEEPER" "$PGD" > "$PGD/postmaster.pid"
alive "$SLEEPER" && ok "(control) the foreign process (a sleeper that dies on SIGINT or SIGTERM) is alive: pid $SLEEPER" || bad "the sleeper did not start"
run stop3 stop; rc_not0 "stop with a pid file naming a live foreign process is refused"
t_has "  and says REFUSED" "REFUSED" "$RUN/stop3.out"
alive "$SLEEPER" && ok "  and the foreign process is still alive" || bad "the foreign process was killed by stop"
run start4 start; rc_not0 "start with that stale pid file is refused"
t_has "  it says STALE PID FILE in one line" "STALE PID FILE: $PGD/postmaster.pid names pid $SLEEPER" "$RUN/start4.out"
t_has "  it prints the exact recovery command (mv -n)" "mv -n \"$PGD/postmaster.pid\"" "$RUN/start4.out"
[ -f "$PGD/postmaster.pid" ] && [ "$(sed -n 1p "$PGD/postmaster.pid")" = "$SLEEPER" ] && ok "  it did NOT move the file itself" || bad "the tool moved or changed the pid file"
run start5 search xneighbour01; rc_not0 "search (which would start the server) is refused the same way"
t_has "  with the same recovery line" "STALE PID FILE" "$RUN/start5.out"
run start6 up; rc_not0 "up likewise"
alive "$SLEEPER" && ok "  and the foreign process is still alive after start, search and up" || bad "the foreign process was killed"
[ "$(server_procs)" = "0" ] && ok "  and no server was started" || bad "a server was started"
printf '%s\n%s\n' "$SLEEPER" "/some/other/datadir" > "$PGD/postmaster.pid"
run stop4 stop; rc_not0 "a pid file naming another data directory is refused"
alive "$SLEEPER" && ok "  and the foreign process is still alive" || bad "the foreign process was killed"
kill -INT "$SLEEPER"; wait "$SLEEPER" 2>> "$RUN/sleeper.err"
alive "$SLEEPER" && bad "the sleeper survived SIGINT, so 'still alive' above proved nothing" || ok "(can fail) the same sleeper DIES on SIGINT, the signal a fast stop sends, so 'still alive' above could have failed"
printf '%s\n%s\n' "$SLEEPER" "$PGD" > "$PGD/postmaster.pid"
run stop5 stop; rc_is "a stale pid file (dead pid) is a clean no-op" 0 stop5
run start7 start; rc_is "  and start clears it by itself (dead pid: nothing to protect)" 0 start7
run stop5b stop; rc_is "stopped again" 0 stop5b

section "15. socket directory guards"
LONG="/tmp/wed-bdb-t$$-a-very-long-name-that-pushes-the-socket-path-past-the-limit-of-one-hundred-and-three-bytes"
T_SOCK="$LONG" run sock1 start
rc_not0 "a socket path over the macOS limit is refused"; t_has "  and says why" "macOS allows 103" "$RUN/sock1.out"
mkdir -m 755 "$SOCK-m"
T_SOCK="$SOCK-m" run sock2 start; rc_not0 "a socket directory that is not mode 700 is refused"
t_has "  for its MODE (the path is short enough to reach that test)" "is not mode 700 (it is 755)" "$RUN/sock2.out"
mkdir -m 700 "$SOCK-real"; ln -s "$SOCK-real" "$SOCK-l"
T_SOCK="$SOCK-l" run sock3 start; rc_not0 "a socket directory that is a symlink is refused"
t_has "  and says so" "is a symlink" "$RUN/sock3.out"
T_SOCK="$SOCK-m" run sock2stop stop; T_SOCK="$SOCK-l" run sock3stop stop     # no-ops, unless a broken guard let a server start there
mv -n "$SOCK-m" "$GONE/"; mv -n "$SOCK-l" "$GONE/sock-symlink"; mv -n "$SOCK-real" "$GONE/"
[ "$(server_procs)" = "0" ] && ok "  and nothing was started" || bad "a server started"
[ ! -e "$LONG" ] && ok "  and the over-long directory was never created" || bad "the over-long socket directory was created"

section "16. version marker"
mv -n "$PGD/PG_VERSION" "$GONE/PG_VERSION.real"; echo 14 > "$PGD/PG_VERSION"
run ver1 start; rc_not0 "start on a mismatched version marker is refused"
t_has "  and says rebuild" "rebuild" "$RUN/ver1.out"
run ver1b search xneighbour01; rc_not0 "search (which would start the server itself) is refused the same way"
t_has "  and says rebuild" "the binaries here are" "$RUN/ver1b.out"
[ "$(server_procs)" = "0" ] && ok "  and nothing was started" || bad "a server started"
mv -n "$PGD/PG_VERSION" "$GONE/PG_VERSION.fake"; mv -n "$GONE/PG_VERSION.real" "$PGD/PG_VERSION"
run ver2 start; rc_is "(can fail) with the real marker back, the same start succeeds" 0 ver2
run check14 check; rc_is "the index survived a clean stop and start (green)" 0 check14

section "17. an unclean stop empties the index; check says so; search rebuilds it"
"$PGBIN/pg_ctl" -D "$PGD" -m immediate -w stop > "$RUN/immediate.out" 2>&1 || bad "immediate stop"
run start3 start; rc_is "start after an unclean stop" 0 start3
run check15 check; rc_is "check is red" 1 check15
t_has "  and says the index is empty" "index is empty" "$RUN/check15.out"
run auto4 search xneighbour01; rc_is "search on the emptied index rebuilds it itself" 0 auto4
t_has "  says it is building" "no index yet" "$RUN/auto4.out"
t_has "  and answers" "$L/2026-01-01_alpha-keeps-panes-open.md" "$RUN/auto4.out"
run check16 check; rc_is "green afterwards" 0 check16

section "18. up, a first run with no cluster, and leave everything stopped"
run stop6 stop
run up1 up; rc_is "up starts a stopped cluster and ends green" 0 up1
run stop7 stop; rc_is "stop" 0 stop7
T_PGD="$RUN/pgdata-auto" run auto5 search xneighbour01; rc_is "search with NO cluster at all creates one, starts it, builds the index and answers" 0 auto5
t_has "  the answer" "$L/2026-01-01_alpha-keeps-panes-open.md" "$RUN/auto5.out"
[ -f "$RUN/pgdata-auto/PG_VERSION" ] && ok "  the new cluster exists" || bad "no new cluster"
T_PGD="$RUN/pgdata-auto" run stop8 stop; rc_is "final stop of that cluster" 0 stop8
[ "$(server_procs "$RUN/")" = "0" ] && ok "no test server process is left (any cluster of this run)" || bad "a test server is still running"
for s in "$SOCK" "$SOCK2"; do
  if [ -d "$s" ]; then
    [ -z "$(ls -A "$s")" ] && ok "socket directory $s is empty" || bad "socket directory $s is not empty: $(ls -A "$s")"
    mv -n "$s" "$GONE/$(basename "$s")" && ok "  and was moved into the run directory (nothing is left in /tmp)" || bad "could not move $s"
  fi
done

echo
echo "finished $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "RESULT: $PASS passed, $FAIL failed  (run directory $RUN)"
[ "$FAIL" -eq 0 ]
