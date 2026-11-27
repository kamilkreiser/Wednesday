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
sleeper() { "$PY" -c 'import time; time.sleep(600)' & SLEEPER=$!; sleep 1; }

echo "brain-db tests: run directory $RUN"
echo "started $(date '+%Y-%m-%d %H:%M:%S %Z')"

section "0. fixtures, and the tool copied into a tree named WEDNESDAY"
"$PY" "$TESTS/make_fixtures.py" "$TREE" || { echo "fixture build failed" >&2; exit 2; }
mksim WEDNESDAY with-scope || { echo "could not copy the tool" >&2; exit 2; }
[ -f "$EXP/absent.txt" ] && [ -f "$EXP/present.txt" ] && [ -f "$EXP/paths.txt" ] && ok "expectation tables written by the fixture builder ($(wc -l < "$EXP/absent.txt" | tr -d ' ') absent, $(wc -l < "$EXP/present.txt" | tr -d ' ') present, $(wc -l < "$EXP/paths.txt" | tr -d ' ') paths)" || bad "expectation tables missing"

section "1. guards before any cluster exists"
env -u WED_AGENT BRAINDB_ROOT="$TREE" /bin/bash "$TOOL" check > "$RUN/guard-root.out" 2>&1; RC=$?
rc_not0 "BRAINDB_ROOT without BRAINDB_PGDATA is refused (a fixture tree can never reach the drive cluster)"
t_has "  and says why" "may never be loaded into the drive cluster" "$RUN/guard-root.out"
run status0 status; rc_is "status on a cluster that does not exist reports STOPPED" 3 status0
run start0 start;   rc_not0 "start with no cluster is refused"
WED_AGENT=tuesday BRAINDB_ROOT="$TREE" BRAINDB_PGDATA="$PGD" BRAINDB_SOCKDIR="$SOCK" /bin/bash "$TOOL" status > "$RUN/seat-mismatch.out" 2>&1; RC=$?
rc_not0 "WED_AGENT=tuesday on a tree named WEDNESDAY is refused (the tree decides the seat; the variable may only agree)"
t_has "  and says REFUSED" "REFUSED" "$RUN/seat-mismatch.out"
WED_AGENT=wednesday BRAINDB_ROOT="$TREE" BRAINDB_PGDATA="$PGD" BRAINDB_SOCKDIR="$SOCK" /bin/bash "$TOOL" status > "$RUN/seat-match.out" 2>&1; RC=$?
rc_is "(can fail) WED_AGENT=wednesday on the same tree is accepted" 3 seat-match
mksim elsewhere with-scope
env -u WED_AGENT BRAINDB_ROOT="$TREE" BRAINDB_PGDATA="$PGD" BRAINDB_SOCKDIR="$SOCK" /bin/bash "$RUN/sim/elsewhere/2_Project_Files/brain-db/braindb.sh" status > "$RUN/seat-unknown.out" 2>&1; RC=$?
rc_not0 "a tree whose folder is not WEDNESDAY, TUESDAY or FRIDAY is refused, never defaulted to a seat"
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
t_has_re "a lesson, a skill and an architecture file with another seat's word in the NAME are indexed (ANSWER-1 item 2)" "tuesday-sweeps|tuesday-ritual|tuesday-vs-wednesday|laptop_datasec-habit" "$RUN/paths-A.txt"

section "6. every exclusion: the planted file is absent, its neighbour is present (whole-index dump)"
dump A
while IFS='|' read -r tok why; do
  [ -n "$tok" ] || continue
  t_hasnt "absent  $tok  $why" "$tok" "$RUN/dump-A.sql"
done <<'EOF'
xcanary03|lesson whose only rules-index row is scoped to another seat (friday)
xcanary03rule|its rules-index line
xcanary17|lesson whose only rules-index row is scoped to another seat (tuesday)
xcanary17rule|its rules-index line
xcanary05|lesson, a (conflict_on_ copy
xcanary06|lesson, .pre- inside a name that still ends .md
xcanary07|lesson backup ending .md.pre-0101
xcanary08|lesson, tier P-Datasec/HPSM-POC
xcanary08rule|its rules-index line
xcanary09|lesson, tier P (Datasec/OXPd)
xcanary13|lesson, project tier naming no client of this seat
xcanary14|section marked tier P-Datasec inside a MIXED lesson
xcanary15|4_Credentials file, reached through a symlink in learnings/
xcanary22|the friday ledger and its archive
xcanary23|the laptop_datasec ledger and its archive
xcanary24|ledger (conflict_on_ copy
xcanary25|ledger .pre- backup
xcanary26|_ledger_fleet_insights.md (not on the allow-list)
xcanary33|daily/_template.md
xcanary34|daily/.spoken.log
xcanary35|daily (conflict_on_ copy
xcanary36|daily .pre- backup
xcanary37|daily_tuesday/
xcanary38|daily_friday/
xcanary41|skill .pre- backup
xcanary76|a CLAUDE.md that is not one of the two allowed
xcanary77|2_Project_Files/tuesday/ (another seat's folder, not on the allow-list)
xcanary78|a (conflict_on_ copy of the root rules file
xcanary47|chat store under 0_Brain/dashboard/
xcanary48|markdown under 0_Brain/dashboard/
xcanary49|0_Brain/reference/
xcanary50|3_Access_Keys/
xcanary51|0_Brain/tasks/ (not on the allow-list)
xcanary52|learnings/families/ (no recursion)
xcanary53rule|rules-index row whose lesson file does not exist
EOF
while IFS='|' read -r tok why; do
  [ -n "$tok" ] || continue
  t_hasnt "absent  $tok  $why" "$tok" "$RUN/dump-A.sql"
done < "$EXP/absent.txt"
t_hasnt "absent  xcanary  ANY canary token at all" "xcanary" "$RUN/dump-A.sql"
while IFS='|' read -r tok why; do
  [ -n "$tok" ] || continue
  t_has "present $tok  $why" "$tok" "$RUN/dump-A.sql"
done <<'EOF'
xneighbour01|lesson, tier W
xneighbour02|lesson with 'tuesday' in its NAME whose rules-index row is scoped all
xneighbour02rule|its rules-index line
xneighbour04|lesson with 'laptop_datasec' in its NAME, no rules-index row, tier W
xneighbour19|lesson with one row for another seat and one row naming this seat
xneighbour19ruleb|the row that names this seat
xneighbour42|skill with 'tuesday' in its name
xneighbour46|architecture file with 'tuesday' in its name
xneighbour70|rules file at the tree root: text before the first heading
xneighbour70b|a section's own text before its numbered rules
xneighbour71|numbered rule 0
xneighbour71b|its continuation line
xneighbour72|numbered rule 0a
xneighbour73|numbered rule 3b-i
xneighbour74|a numbered rule under a second heading
xneighbour75|0_Brain/CLAUDE.md
xneighbour01apply|its second section
xneighbour01rule|its rules-index line
xneighbour01ruletwo|its #2 rules-index line
xneighbour10|lesson, tier P-Secuura/Blockchain
xneighbour11|lesson, tier M
xneighbour12|lesson with no tier
xneighbour14|MIXED lesson, unmarked text
xneighbour14b|section marked tier P-Secuura inside it
xneighbour14c|the section after the dropped one
xneighbour16|superseded lesson
xneighbour20|this seat's ledger
xneighbour20rule|a ledger row's rule sentence
xneighbour21|this seat's ledger archive
xneighbour30|daily bullet
xneighbour30b|its continuation line
xneighbour30c|daily bullet with no time
xneighbour30d|daily plain paragraph
xneighbour40|skill
xneighbour43|identity
xneighbour44|people
xneighbour45|architecture
EOF
while IFS='|' read -r tok why; do
  [ -n "$tok" ] || continue
  t_has "present $tok  $why" "$tok" "$RUN/dump-A.sql"
done < "$EXP/present.txt"
can_fail "absence assertion: pointed at a neighbour token it is red" hasnt "xneighbour01" "$RUN/dump-A.sql"
can_fail "presence assertion: pointed at a canary token it is red" has "xcanary03" "$RUN/dump-A.sql"
sql "select heading from brain.chunks where kind = 'rules' order by id" > "$RUN/rules-headings.txt" || bad "rules headings"
[ "$(wc -l < "$RUN/rules-headings.txt" | tr -d ' ')" = "7" ] && ok "the two rules files give 7 rows (1 intro, 1 section text, 3 numbered rules, 1 rule under a second heading, 1 section of the brain file)" || { bad "rules rows: $(wc -l < "$RUN/rules-headings.txt")"; sed 's/^/        /' "$RUN/rules-headings.txt"; }
for h in "CLAUDE.md > Rules > rule 0" "CLAUDE.md > Rules > rule 0a" "CLAUDE.md > Rules > rule 3b-i" "CLAUDE.md > Session end > rule 1" "0_Brain/CLAUDE.md > Folders"; do
  [ "$(/usr/bin/grep -i -x -F -c -- "$h" "$RUN/rules-headings.txt")" = "1" ] && ok "one row headed: $h" || bad "no single row headed: $h"
done
[ -z "$(find "$RUN" -iname 'PWNED*' -not -path '*/pgdata-*' | head -1)$(find "$PWD" -maxdepth 1 -iname 'PWNED*' | head -1)" ] && ok "no injection string in a file name, heading, body or rules-index field created a file (find PWNED*: nothing)" || bad "a PWNED file exists: $(find "$RUN" -iname 'PWNED*' | head -3)"
[ -n "$(find "$RUN" -name 'paths.txt' | head -1)" ] && ok "(control) the same find does find a file that exists" || bad "find control failed"

section "6b. the rebuild report names what failed closed (ANSWER-3 F1, F3)"
t_has "UNTAGGED lessons are listed by name" "UNTAGGED lessons indexed" "$RUN/rebuild1.out"
t_has "  including the fixture's untagged lesson" "$L/2026-01-12_untagged.md" "$RUN/rebuild1.out"
t_has "damaged rules-index rows are counted" "DAMAGED row(s) ignored" "$RUN/rebuild1.out"
t_has "a lesson excluded for a damaged row is named with the row's line" "2026-07-20_r-six-fields.md  [a damaged rules-index row names it (rules index line" "$RUN/rebuild1.out"
t_has "a lesson whose tier cannot be read safely is named with the reason" "2026-06-05_fm-dup-ds-w.md  [tier cannot be read safely: tier is given more than once" "$RUN/rebuild1.out"
t_has "the hard link is named as a hard link" "2026-07-27_hardlink.md  [hard link (link count 2)" "$RUN/rebuild1.out"
t_has "a daily note whose name is not a plain date is skipped with that reason" "not a daily-note file name" "$RUN/rebuild1.out"
t_hasnt "no Python traceback anywhere in the rebuild output" "Traceback" "$RUN/rebuild1.out"

section "7. the exclusions are load-bearing"
# 7a. Widen the ALLOW-LIST onto other seats' records, under several KINDS, and keep the deny lines:
#     the seat words must still stop them whatever kind the allow line declares (ANSWER-3 F11).
{ cat "$LANE/scope/wednesday.scope"
  echo "allow daily 0_Brain/daily_tuesday/20*.md"; echo "allow daily 0_Brain/daily_friday/20*.md"
  echo "allow skill 0_Brain/daily_tuesday/*.md"
  echo "allow ledger 0_Brain/learnings/_ledger_friday.md"; echo "allow ledger 0_Brain/learnings/_ledger_laptop_datasec.md"
  echo "allow lesson 0_Brain/learnings/*.md"; echo "allow skill 0_Brain/learnings/_ledger_*.md"
  echo "allow skill 0_Brain/tasks/*.md"; echo "allow skill 0_Brain/tasks/NEXT-PICKUP-TUESDAY.md"
  echo "allow skill 2_Project_Files/tuesday/*.md"; } > "$RUN/widened.scope"
T_SCOPE="$RUN/widened.scope" run rebuildW rebuild; rc_is "rebuild with the allow-list widened onto other seats' records under five kinds" 0 rebuildW
dump W
for tok in xcanary37 xcanary38 xcanary22 xcanary23 xcanary77 xcanary700 xcanary701; do
  t_hasnt "seat words still exclude $tok" "$tok" "$RUN/dump-W.sql"
done
t_has "  the rebuild output says why" "another seat's records" "$RUN/rebuildW.out"
t_has "(control) this seat's OWN pickup file does enter under the same widened line, so the line is live" "xtasksown202" "$RUN/dump-W.sql"
t_has "(control) a lesson named for another seat is still indexed under the same scope" "xneighbour02" "$RUN/dump-W.sql"
# 7b. Now remove the deny lines too: the planted files enter.
sed -e '/^deny_path /d' -e '/^deny_seat_word /d' -e '/^deny_clients /d' -e 's/^own_clients .*/& datasec acme/' "$RUN/widened.scope" > "$RUN/permissive.scope"
T_SCOPE="$RUN/permissive.scope" run rebuildP rebuild; rc_is "rebuild under the permissive scope" 0 rebuildP
dump P
for tok in xcanary05 xcanary06 xcanary08 xcanary09 xcanary13 xcanary14 xcanary22 xcanary23 xcanary37 xcanary38 xcanary77 xcanary700 xcanary701; do
  t_has "(can fail) without the deny lines $tok DOES enter the index" "$tok" "$RUN/dump-P.sql"
done
t_hasnt_re "even then: a lesson whose every rules-index row names another seat stays out (the seats column is not a scope-file setting)" "xcanary03|xcanary17" "$RUN/dump-P.sql"
t_hasnt_re "even then: backups ending .md.pre-*, the symlinks, the hard link, credentials, keys, dashboard, reference stay out" \
  "xcanary07|xcanary15|xcanary25|xcanary36|xcanary41|xcanary47|xcanary48|xcanary49|xcanary50|xcanary680|xcanary681" "$RUN/dump-P.sql"
t_hasnt_re "even then: every lesson whose tier or rules-index row cannot be read safely stays out (fail closed is not a scope-file setting)" \
  "xcanary60[45678]|xcanary61[02345]|xcanary618|xcanary62[0123]|xcanary66[0-9]|xcanary67[015]" "$RUN/dump-P.sql"
for tok in xcanary601 xcanary602 xcanary609 xcanary611; do
  t_has "(can fail) a lesson of the other client whose tier IS read correctly ($tok) enters once that client is allowed, so its absence above is the tier rule at work" "$tok" "$RUN/dump-P.sql"
done
run checkP check; rc_is "check under the real scope is red after a permissive rebuild (scope hash differs)" 1 checkP
run rebuild2 rebuild; rc_is "rebuild under the real scope" 0 rebuild2
dump C
t_hasnt "and every canary is gone again" "xcanary" "$RUN/dump-C.sql"

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
deny_seat_word two words
EOF
run check2 check; rc_is "the index is unchanged by the refused rebuilds (check green)" 0 check2
{ cat "$LANE/scope/wednesday.scope"; echo "allow skill 0_Brain/skills_link/*.md"; } > "$RUN/symdir.scope"
T_SCOPE="$RUN/symdir.scope" run rebuildS rebuild; rc_is "a scope naming a SYMLINKED directory still rebuilds" 0 rebuildS
dump S
t_hasnt "  but nothing behind the symlink is indexed" "xcanary" "$RUN/dump-S.sql"
t_has "  and the rebuild output names the skipped directory" "symlink" "$RUN/rebuildS.out"
run rebuild3 rebuild; rc_is "back to the real scope" 0 rebuild3

section "8b. no usable rules index: the rebuild is REFUSED, not run with every lesson let in (ANSWER-3 F1 iii)"
NF0="$(sql "select count(*) from brain.files")"
mv -n "$TREE/$L/_rules_index.tsv" "$GONE/_rules_index.tsv"
run noidx rebuild; rc_not0 "rebuild with the rules index missing is refused"
t_has "  and says why" "REFUSED: lessons are on the allow-list but no readable rules index" "$RUN/noidx.out"
[ "$(sql "select count(*) from brain.files")" = "$NF0" ] && ok "  the index still holds its $NF0 files" || bad "the index changed: $(sql "select count(*) from brain.files") files"
dump N; t_hasnt_re "  neither other-seat lesson entered" "xcanary03|xcanary17" "$RUN/dump-N.sql"
printf '# a rules index with a header and no rows\n' > "$TREE/$L/_rules_index.tsv"
run noidx2 rebuild; rc_not0 "rebuild with a rules index that has no well-formed row is refused"
mv -n "$TREE/$L/_rules_index.tsv" "$GONE/_rules_index.header-only.tsv"; mv -n "$GONE/_rules_index.tsv" "$TREE/$L/_rules_index.tsv"
run check2b check; rc_is "(can fail) with the rules index back, check is green again" 0 check2b

section "9. check: red on a changed, added or removed fixture; green after rebuild"
run check3 check; rc_is "(control) green before any change" 0 check3
echo "an appended line" >> "$TREE/$L/2026-01-01_alpha-keeps-panes-open.md"
echo "an appended line" >> "$TREE/$L/2026-01-03_what-friday-does.md"
run check4 check; rc_is "red after one indexed file and one excluded file changed" 1 check4
t_has "  and names the changed path" "changed since the last rebuild: $L/2026-01-01_alpha-keeps-panes-open.md" "$RUN/check4.out"
t_hasnt "  the changed EXCLUDED file is not named" "what-friday-does" "$RUN/check4.out"
t_has "  and exactly one path differs" "RED, 1 path(s) differ" "$RUN/check4.out"
run rebuild4 rebuild; run check5 check; rc_is "green after rebuild" 0 check5
printf -- '---\ndate: 2026-01-18\ntier: W\n---\n\n# A new lesson\n\nxneighbour60\n' > "$TREE/$L/2026-01-18_new.md"
run check6 check; rc_is "red after a file was added" 1 check6
t_has "  and names it" "on disk, not in the index: $L/2026-01-18_new.md" "$RUN/check6.out"
mv -n "$TREE/0_Brain/skills/ritual.md" "$GONE/ritual.md"
run check7 check; rc_is "red after a file was removed" 1 check7
t_has "  and names it" "gone from disk or now out of scope: 0_Brain/skills/ritual.md" "$RUN/check7.out"
mv -n "$GONE/ritual.md" "$TREE/0_Brain/skills/ritual.md"
i=0; while [ "$i" -lt 25 ]; do i=$((i+1)); printf -- '---\ndate: 2026-02-01\ntier: W\n---\n\n# Bulk %s\n\ntext\n' "$i" > "$TREE/$L/2026-02-01_bulk-$i.md"; done
run check8 check; rc_is "red with 26 differing paths" 1 check8
[ "$(count_in 'on disk, not in the index' "$RUN/check8.out")" = "20" ] && ok "  names exactly 20 paths" || bad "named $(count_in 'on disk, not in the index' "$RUN/check8.out") paths, wanted 20"
t_has "  and counts the rest" "(+6 more)" "$RUN/check8.out"
run rebuild5 rebuild; run check9 check; rc_is "green after rebuild" 0 check9

section "9b. one bad file does not lose the rebuild (ANSWER-3 F7)"
printf -- '---\ntier: W\n---\n# locked\n\nxlocked300\n' > "$TREE/$L/2026-09-01_locked.md"; chmod 000 "$TREE/$L/2026-09-01_locked.md"
"$PY" -c "
import sys
open(sys.argv[1], 'w').write('---\ntier: W\n---\n# big\n\nxbigrow301 ' + ' '.join('w%07dx' % i for i in range(300000)) + '\n')" "$TREE/$L/2026-09-02_big.md"
run rebuildF rebuild; rc_is "rebuild with one unreadable lesson and one 3 MB section still succeeds" 0 rebuildF
t_hasnt "  with no Python traceback" "Traceback" "$RUN/rebuildF.out"
t_has "  the unreadable file is listed" "2026-09-01_locked.md  [unreadable: PermissionError]" "$RUN/rebuildF.out"
t_has "  the truncated row is listed" "2026-09-02_big.md" "$RUN/rebuildF.out"
t_has "  and the LAST line says so" "DONE WITH FAULTS: 1 unreadable file(s) skipped, 1 row(s) truncated" "$RUN/rebuildF.out"
[ "$(tail -1 "$RUN/rebuildF.out" | count_in 'DONE WITH FAULTS' /dev/stdin)" = "1" ] && ok "  (it is the last line)" || bad "the fault line is not last: $(tail -1 "$RUN/rebuildF.out")"
can_fail "fault line: the clean rebuild before it did not print it" has "DONE WITH FAULTS" "$RUN/rebuild5.out"
run checkF check; rc_is "check is green on what could be read" 0 checkF
t_has "  and reports the skipped counts" "skipped for a fault: 1 file(s) unreadable on disk now; at the last rebuild 1 unreadable, 1 row(s) truncated" "$RUN/checkF.out"
t_hasnt "  with no Python traceback" "Traceback" "$RUN/checkF.out"
run sF search xbigrow301; t_has "the truncated row is still found by a word before the cut" "2026-09-02_big.md" "$RUN/sF.out"
run sF2 search xlocked300; t_has "the unreadable file's word is not in the index" "NO MATCH" "$RUN/sF2.out"
chmod 644 "$TREE/$L/2026-09-01_locked.md"; mv -n "$TREE/$L/2026-09-01_locked.md" "$GONE/"; mv -n "$TREE/$L/2026-09-02_big.md" "$GONE/"
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
run s8 search xneighbour910; t_has "a row holding the separator bytes 0x1F and 0x1E is FOUND by search (ANSWER-3 F8)" "2026-07-28_separator-bytes.md" "$RUN/s8.out"
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
B at $'pane\n' > "$RUN/a3.out" 2>&1; RC=$?; rc_not0 "a trigger with a trailing newline is refused"
B at "$(printf 'pane\nq')" > "$RUN/a4.out" 2>&1; RC=$?; rc_not0 "a trigger holding a newline is refused"
run check10 check; rc_is "  and the index is intact" 0 check10

section "12. other seats: each from its OWN tree (a copy of the tool in a tree named TUESDAY, then FRIDAY)"
mksim TUESDAY; mksim FRIDAY
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
for tok in xcanary23 xcanary37 xcanary08 xcanary14 xcanary17 xneighbour02 xneighbour01 xneighbour19 xneighbour46 xneighbour71; do t_has "tuesday scope: present $tok" "$tok" "$RUN/dump-T.sql"; done
for tok in xneighbour20 xneighbour30 xneighbour10 xneighbour14b xcanary38 xcanary22 xcanary03 xcanary15 xcanary47 xcanary77 xcanary680; do t_hasnt "tuesday scope: absent  $tok" "$tok" "$RUN/dump-T.sql"; done
runs t3 TUESDAY stop; rc_is "tuesday's server stopped" 0 t3
cp -n "$LANE/proposed/scope/friday.scope" "$RUN/sim/FRIDAY/2_Project_Files/brain-db/scope/friday.scope"
runs f2 FRIDAY rebuild; rc_is "the friday tree builds on the fixtures with its proposed scope" 0 f2
dump2 F
for tok in xcanary22 xcanary38 xcanary03 xcanary08 xneighbour10 xneighbour01 xneighbour02 xneighbour04 xneighbour19; do t_has "friday scope: present $tok" "$tok" "$RUN/dump-F.sql"; done
for tok in xneighbour20 xneighbour30 xcanary37 xcanary23 xcanary17 xcanary15 xcanary47 xcanary77 xcanary680; do t_hasnt "friday scope: absent  $tok" "$tok" "$RUN/dump-F.sql"; done
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
kill "$SLEEPER"; wait "$SLEEPER" 2>> "$RUN/sleeper.err"
alive "$SLEEPER" && bad "the sleeper survived SIGTERM, so 'still alive' above proved nothing" || ok "(can fail) the same sleeper DIES on a signal, so 'still alive' above could have failed"
printf '%s\n%s\n' "$SLEEPER" "$PGD" > "$PGD/postmaster.pid"
run stop5 stop; rc_is "a stale pid file (dead pid) is a clean no-op" 0 stop5
run start7 start; rc_is "  and start clears it by itself (dead pid: nothing to protect)" 0 start7
run stop5b stop; rc_is "stopped again" 0 stop5b

section "15. socket directory guards"
LONG="/tmp/wed-bdb-t$$-a-very-long-name-that-pushes-the-socket-path-past-the-limit-of-one-hundred-and-three-bytes"
T_SOCK="$LONG" run sock1 start
rc_not0 "a socket path over the macOS limit is refused"; t_has "  and says why" "macOS allows 103" "$RUN/sock1.out"
mkdir -m 755 "$RUN/sock755"
T_SOCK="$RUN/sock755" run sock2 start; rc_not0 "a socket directory that is not mode 700 is refused"
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
