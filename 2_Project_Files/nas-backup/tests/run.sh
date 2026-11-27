#!/bin/bash
# tests/run.sh — every behaviour of the nightly NAS backup against a FAKE NAS and a fake source tree.
# NEVER the real NAS: nb_core.py honours test mode only for a directory under /private/tmp, and in test mode
# refuses any nas_root or source outside it.
#
#   tests/run.sh [base dir under /private/tmp]     default: /private/tmp/nas-backup-tests
# Each run builds fresh fixtures under <base>/run_<stamp>_<pid>/ and removes nothing afterwards (no rm).
#
# HOW EACH TEST IS SHOWN ABLE TO FAIL:
#   - every refusal has a MUST-SUCCEED NEIGHBOUR: the same command with the one condition put right;
#   - the additive checks are re-run against SABOTAGED engines (an engine that keeps no previous version, an
#     engine after which a destination file has gone) and the SAME predicate must then come out false
#     ("CAN-FAIL" lines);
#   - the secret check has a neighbour file that is not secret-shaped and must arrive;
#   - clock cases come in pairs that differ only in the supplied time or the state.
# macOS bash 3.2. No cd. Never discards stderr (everything is captured into <fixture>/out/).
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANE="$(cd -P "$HERE/.." && pwd)"
BASE="${1:-/private/tmp/nas-backup-tests}"
case "$BASE" in /private/tmp/*) ;; *) echo "tests: REFUSED — the base must be under /private/tmp (got $BASE)" >&2; exit 2 ;; esac
RUN="$BASE/run_$(date +%Y%m%d-%H%M%S)_$$"
mkdir -p "$RUN" || exit 2
PY=/opt/homebrew/bin/python3; [ -x "$PY" ] || PY=/usr/bin/python3
REAL_RSYNC=/opt/homebrew/bin/rsync
PASS=0; FAIL=0; FAILED=""
T=""; RC=0

pass() { PASS=$((PASS+1)); printf '  PASS  %s\n' "$1"; }
fail() { FAIL=$((FAIL+1)); FAILED="$FAILED
    $1"; printf '  FAIL  %s\n' "$1"; }
is()    { if [ "$2" = "$3" ]; then pass "$1 (= $3)"; else fail "$1 (expected '$2', got '$3')"; fi; }
has()   { if /usr/bin/grep -i -q -F -- "$3" "$2"; then pass "$1"; else fail "$1 (no '$3' in $2)"; fi; }
hasnt() { if [ -s "$2" ] && ! /usr/bin/grep -i -q -F -- "$3" "$2"; then pass "$1"; else fail "$1 ('$3' present, or $2 empty)"; fi; }
yes()   { local d="$1"; shift; if "$@"; then pass "$d"; else fail "$d"; fi; }
no()    { local d="$1"; shift; if "$@"; then fail "$d"; else pass "$d"; fi; }
canfail() { local d="$1"; shift; if "$@"; then fail "CAN-FAIL $d (the predicate stayed TRUE under sabotage: this test cannot fail)"; else pass "CAN-FAIL $d (predicate is false under sabotage)"; fi; }

# the clock: day D of a fixed week, HH MM local -> epoch
at() { "$PY" -c 'import datetime,sys; d=datetime.datetime(2026,12,1)+datetime.timedelta(days=int(sys.argv[1])); print(int(d.replace(hour=int(sys.argv[2]),minute=int(sys.argv[3])).timestamp()))' "$1" "$2" "$3"; }

write_conf() { # [rsync] [late_fire] [extra line]
  {
    echo "status=${CONF_STATUS:-confirmed}"
    echo "source_volume=$T/vol"
    echo "nas_root=$T/nas"
    echo "fire=00:30"
    echo "window_hours=5"
    echo "late_fire=${2:-refuse}"
    echo "min_free_gib=200"
    echo "max_seconds=600"
    echo "stall_seconds=${CONF_STALL:-900}"
    echo "hash_sample=${CONF_SAMPLE:-10}"
    [ -n "${CONF_CHUNK:-}" ] && echo "chunk_files=$CONF_CHUNK"
    echo "rsync=${1:-$REAL_RSYNC}"
    echo "set=General|WEDNESDAY|$T/vol/WEDNESDAY"
    echo "set=Secuura|Secuura|$T/vol/CODING/Secuura"
    [ -n "${3:-}" ] && echo "$3"
    [ -n "${4:-}" ] && echo "$4"
    [ -n "${5:-}" ] && echo "$5"
  } > "$T/lane/seats/wednesday.conf"
  seal_conf
}
seal_conf() { # append the END marker with the right count (what a careful editor does by hand)
  local f="$T/lane/seats/wednesday.conf"
  local n; n="$(/usr/bin/grep -v -E '^[[:space:]]*(#|$)' "$f" | /usr/bin/grep -c -v -E '^END ')"
  /usr/bin/grep -v -E '^END ' "$f" > "$f.tmp"; mv "$f.tmp" "$f"; echo "END lines=$n" >> "$f"
}
owner_json() { # pid -> a lock owner record as the tool writes it (pid + the time that process started)
  printf '{"pid": %s, "pid_started": "%s", "started_local": "test"}\n' "$1" "$(ps -o lstart= -p "$1" | sed -e 's/^ *//' -e 's/ *$//')" > "$T/lane/state/wednesday.lock.d/owner.json"
}
doctor_block() { # <now epoch> : run the PROPOSED doctor block exactly as doctor.sh would source it, with doctor's own three helpers
  ( QUIET=""          # not --quiet here, so an "ok" outcome is a visible line the tests can read
    ok()   { [ "$QUIET" = "--quiet" ] || printf "  ✓ %s\n" "$1"; }
    warn() { printf "  ⚠ %-38s %s\n" "$1" "${2:-}"; }
    fail() { printf "  ✗ %-38s %s\n" "$1" "${2:-}"; }
    PROJECT_DIR="$(cd -P "$LANE/../.." && pwd)"
    unset WED_AGENT
    export NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" NB_DOCTOR_NOW="$1"
    . "$LANE/proposed/doctor_nasbackup_block.sh" )
}
write_mounts() { # [nas fs] [vol opts]
  {
    echo "/dev/disk9s1 on $T/vol (${2:-apfs, local, nodev, nosuid, journaled, noowners})"
    [ "${1:-smbfs}" = "none" ] || echo "//user@nas.example/DEV-Working on $T/nas (${1:-smbfs}, nodev, nosuid, mounted by tester)"
  } > "$T/mount.txt"
}
fixture() { # name
  T="$RUN/$1"
  mkdir -p "$T/vol/WEDNESDAY/sub" "$T/vol/WEDNESDAY/sp ace" "$T/vol/WEDNESDAY/0_Brain/learnings" "$T/vol/WEDNESDAY/emptydir" \
           "$T/vol/WEDNESDAY/2_Project_Files" "$T/vol/CODING/Secuura/Blockchain/src" \
           "$T/nas/Secuura" "$T/nas/General" "$T/nas/Datasec" "$T/lane/seats" "$T/stub" "$T/out"
  echo "old content of a" > "$T/vol/WEDNESDAY/a.txt"
  printf 'AAAA' > "$T/vol/WEDNESDAY/same.txt"
  echo "b" > "$T/vol/WEDNESDAY/sub/b.txt"
  echo "c d" > "$T/vol/WEDNESDAY/sp ace/c d.txt"
  echo "lesson" > "$T/vol/WEDNESDAY/0_Brain/learnings/é-ünï lesson.md"
  ln -s a.txt "$T/vol/WEDNESDAY/link-to-a"
  echo "console.log(1)" > "$T/vol/CODING/Secuura/Blockchain/src/app.js"
  echo 5000 > "$T/free_gib.txt"
  CONF_STATUS=confirmed; CONF_STALL=900; CONF_SAMPLE=10; CONF_CHUNK=""
  write_conf
  write_mounts
}
nb()      { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup.sh" "$@"; }
nightly() { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup_nightly.sh" "$@"; }
watch()   { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup_watch.sh" "$@"; }
to() { local o="$T/out/$1"; shift; "$@" > "$o" 2>&1; RC=$?; }
OUTF() { echo "$T/out/$1"; }
CUR() { echo "$T/nas/General/Wednesday/nightly-backup/current/WEDNESDAY"; }
VER() { echo "$T/nas/General/Wednesday/nightly-backup/versions"; }
started() { find "$T/nas" -name 'RUN_*_STARTED.txt' 2>&1 | wc -l | tr -d ' '; }
completed() { find "$T/nas" -name 'RUN_*_COMPLETE.txt' 2>&1 | wc -l | tr -d ' '; }
state() { "$PY" -c 'import json,sys
d=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."):
    d = d.get(k) if isinstance(d, dict) else None
print(d)' "$T/lane/state/wednesday.json" "$1" 2>&1; }
state_owner() { "$PY" -c 'import json,sys; print(json.load(open(sys.argv[1])).get(sys.argv[2]))' "$T/lane/state/wednesday.lock.d/owner.json" "$1" 2>&1; }
cards() { cat "$T"/out/"$1"* 2>&1 | /usr/bin/grep -c -F 'CARD-COMMAND:'; }

# predicates used both straight and under sabotage
p_prev_version_kept() { [ -n "$(/usr/bin/grep -r -l -x -F 'old content of a' "$(VER)" 2>&1 | /usr/bin/grep -F 'a.txt')" ]; }
p_same_size_version_kept() { [ -n "$(/usr/bin/grep -r -l -F 'AAAA' "$(VER)" 2>&1 | /usr/bin/grep -F 'same.txt')" ]; }
p_deleted_source_still_at_dest() { [ -f "$(CUR)/sub/b.txt" ]; }
p_no_secret_on_nas() { [ -z "$(find "$T/nas" \( -name 'secret.txt' -o -name '.env' -o -name '*.pem' -o -name 'id_rsa' -o -name 'config' -o -name 'x.js' -o -name 'q.txt' -o -name 'PG_VERSION' -o -name 'notes.md' -o -name '4_Credentials' -o -name '3_Access_Keys' \) 2>&1)" ]; }

mk_stub() { # name body  (body runs after the --version passthrough; "$@" are rsync's args)
  local f="$T/stub/$1"
  { echo '#!/bin/bash'
    echo "REAL=$REAL_RSYNC"
    echo 'STUBDIR="$(dirname "$0")"'
    echo 'for a in "$@"; do if [ "$a" = "--version" ]; then exec "$REAL" --version; fi; done'
    echo "$2"
  } > "$f"; chmod +x "$f"; echo "$f"
}

echo "=== nas-backup tests — fixtures under $RUN ==="
echo "lane: $LANE   python: $($PY --version 2>&1)   rsync: $($REAL_RSYNC --version 2>&1 | head -1)"

# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo; echo "T1  --dry is the DEFAULT and writes nothing"
fixture main
to t1.txt nb
is  "T1 no-argument run exits 0" 0 "$RC"
has "T1 it says DRY RUN" "$(OUTF t1.txt)" "DRY RUN finished"
has "T1 it reports what it would copy (5 files in the seat tree)" "$(OUTF t1.txt)" "to copy: 5 files"
no  "T1 nothing created on the fake NAS (no seat folder)" test -e "$T/nas/General/Wednesday"
no  "T1 no state file written" test -e "$T/lane/state/wednesday.json"
no  "T1 no index file created (a dry run never opens the index for writing)" test -e "$T/lane/state/wednesday.index.sqlite"
is  "T1 no run markers on the NAS" 0 "$(started)"

echo; echo "T2  a real run copies, counts both sides, records state (neighbour of T1: this one DOES write)"
to t2.txt nb --run --now "$(at 0 1 0)"
is  "T2 real run exits 0" 0 "$RC"
has "T2 says GOOD" "$(OUTF t2.txt)" "GOOD: every in-scope source file is PROVEN"
yes "T2 a.txt arrived byte-identical" cmp -s "$T/vol/WEDNESDAY/a.txt" "$(CUR)/a.txt"
yes "T2 a name with spaces arrived" cmp -s "$T/vol/WEDNESDAY/sp ace/c d.txt" "$(CUR)/sp ace/c d.txt"
yes "T2 a non-ASCII name arrived" test -f "$(CUR)/0_Brain/learnings/é-ünï lesson.md"
yes "T2 the Secuura set landed in the Secuura client folder" test -f "$T/nas/Secuura/Wednesday/nightly-backup/current/Secuura/Blockchain/src/app.js"
yes "T2 an empty folder was created at the destination" test -d "$(CUR)/emptydir"
no  "T2 the symlink was NOT created on the NAS" test -e "$(CUR)/link-to-a"
yes "T2 the symlink is recorded in the manifest folder on the NAS" /usr/bin/grep -r -q -F 'link-to-a' "$T/nas/General/Wednesday/nightly-backup/manifests"
is  "T2 one STARTED marker per client" 2 "$(started)"
is  "T2 one COMPLETE marker per client" 2 "$(completed)"
is  "T2 state: last attempt good" good "$(state last_attempt.status)"
is  "T2 state: 6 source files counted" 6 "$(state last_good.counts.src_files)"
is  "T2 state: 6 destination files counted" 6 "$(state last_good.counts.dst_files)"
is  "T2 state: source bytes = destination bytes" "$(state last_good.counts.src_bytes)" "$(state last_good.counts.dst_bytes)"
yes "T2 the lock was released (moved aside, not left)" test ! -d "$T/lane/state/wednesday.lock.d"

echo; echo "T3  ADDITIVE: a changed file keeps its previous version; a file deleted at the source stays"
echo "new longer content of a" > "$T/vol/WEDNESDAY/a.txt"
sleep 1; printf 'BBBB' > "$T/vol/WEDNESDAY/same.txt"          # same size, different content
mkdir -p "$T/held"; mv -n "$T/vol/WEDNESDAY/sub/b.txt" "$T/held/b.txt"   # "deleted at the source" (moved out of it)
to t3.txt nb --run --now "$(at 1 1 0)"
is  "T3 second run exits 0" 0 "$RC"
has "T3 says GOOD although the destination now holds a file the source lacks" "$(OUTF t3.txt)" "GOOD: every in-scope"
yes "T3 current/a.txt is the NEW content" cmp -s "$T/vol/WEDNESDAY/a.txt" "$(CUR)/a.txt"
yes "T3 the PREVIOUS a.txt is kept under versions/" p_prev_version_kept
yes "T3 same-size change detected: current/same.txt is BBBB" /usr/bin/grep -q -F BBBB "$(CUR)/same.txt"
yes "T3 same-size change: previous AAAA kept under versions/" p_same_size_version_kept
yes "T3 the file deleted at the source is STILL at the destination" p_deleted_source_still_at_dest
has "T3 the run reports previous copies kept" "$(OUTF t3.txt)" "previous copies kept: 2"
is  "T3 state: 5 source files now, 5 counted at destination" "5/5" "$(state last_good.counts.src_files)/$(state last_good.counts.dst_files)"
is  "T3 state: 1 destination-only file reported" 1 "$(state last_good.counts.dst_only_files)"
to t3b.txt nb --run --now "$(at 1 2 0)"
has "T3 a run with nothing changed copies 0 files" "$(OUTF t3b.txt)" "to copy: 0 files"
#   index lost: nothing is re-copied, the overlap is compared by sha256 once
mv -n "$T/lane/state/wednesday.index.sqlite" "$T/held/index.aside"
to t3c.txt nb --run --now "$(at 1 3 0)"
has "T3 index lost: still 0 files to copy" "$(OUTF t3c.txt)" "to copy: 0 files"
has "T3 index lost: the overlap is compared by sha256" "$(OUTF t3c.txt)" "compared by sha256"

#   the same-size change must be seen by the STAT comparison alone. With the sample on, the sample would find and
#   repair it too, and would hide a tool that trusts its index blindly (mutant M20): so here the sample is off.
fixture statonly; CONF_SAMPLE=0; write_conf
to q0.txt nb --run --now "$(at 0 1 0)"
sleep 1; printf 'BBBB' > "$T/vol/WEDNESDAY/same.txt"
to q1.txt nb --run --now "$(at 1 1 0)"
has "T3 sample off: a same-size change at the source is in the copy list by its stat alone" "$(OUTF q1.txt)" "to copy: 1 files"
yes "T3 sample off: ... and the destination holds the new content" /usr/bin/grep -q -F BBBB "$(CUR)/same.txt"
CONF_SAMPLE=10

echo; echo "T3x CAN-FAIL: the same predicates under sabotaged engines"
fixture sab1
S="$(mk_stub rsync_nobackup 'args=(); for a in "$@"; do case "$a" in --backup|--backup-dir=*) ;; *) args+=( "$a" );; esac; done; exec "$REAL" "${args[@]}"')"
write_conf "$S"
to s1a.txt nb --run --now "$(at 0 1 0)"
echo "new longer content of a" > "$T/vol/WEDNESDAY/a.txt"
to s1b.txt nb --run --now "$(at 1 1 0)"
canfail "an engine that keeps no previous version: 'previous a.txt kept'" p_prev_version_kept
fixture sab2
S="$(mk_stub rsync_loses_a_file '"$REAL" "$@"; rc=$?; f="$STUBDIR/../nas/General/Wednesday/nightly-backup/current/WEDNESDAY/sub/b.txt"; if [ -f "$f" ] && [ ! -f "$STUBDIR/../vol/WEDNESDAY/sub/b.txt" ]; then mkdir -p "$STUBDIR/taken"; mv -n "$f" "$STUBDIR/taken/b.txt"; fi; exit $rc')"
write_conf "$S"
to s2a.txt nb --run --now "$(at 0 1 0)"
mkdir -p "$T/held"; mv -n "$T/vol/WEDNESDAY/sub/b.txt" "$T/held/b.txt"; echo "x" > "$T/vol/WEDNESDAY/new.txt"
to s2b.txt nb --run --now "$(at 1 1 0)"
canfail "a destination file that goes away: 'deleted-at-source file still at destination'" p_deleted_source_still_at_dest

echo; echo "T4  SECRETS and excluded folders never arrive (neighbour: an ordinary file beside them does)"
fixture main4
mkdir -p "$T/vol/WEDNESDAY/4_Credentials" "$T/vol/WEDNESDAY/3_Access_Keys" "$T/vol/WEDNESDAY/sub/.git" "$T/vol/WEDNESDAY/node_modules/pkg" \
         "$T/vol/WEDNESDAY/_quarantine_2026-01-01" "$T/vol/WEDNESDAY/2_Project_Files/brain-db/pgdata-wednesday" "$T/vol/WEDNESDAY/2_Project_Files/tuesday" \
         "$T/vol/CODING/Secuura/Blockchain/4_Credentials"
echo "s3cr3t" > "$T/vol/WEDNESDAY/4_Credentials/secret.txt"
echo "key"    > "$T/vol/WEDNESDAY/3_Access_Keys/id_rsa"
echo "K=V"    > "$T/vol/WEDNESDAY/.env"
echo "pem"    > "$T/vol/WEDNESDAY/sub/deploy.pem"
echo "cfg"    > "$T/vol/WEDNESDAY/sub/.git/config"
echo "js"     > "$T/vol/WEDNESDAY/node_modules/pkg/x.js"
echo "q"      > "$T/vol/WEDNESDAY/_quarantine_2026-01-01/q.txt"
echo "16"     > "$T/vol/WEDNESDAY/2_Project_Files/brain-db/pgdata-wednesday/PG_VERSION"
echo "hers"   > "$T/vol/WEDNESDAY/2_Project_Files/tuesday/notes.md"
echo "s3cr3t" > "$T/vol/CODING/Secuura/Blockchain/4_Credentials/secret.txt"
echo "plain"  > "$T/vol/WEDNESDAY/sub/notsecret.txt"
to t4.txt nb --run --now "$(at 0 1 0)"
is  "T4 run exits 0" 0 "$RC"
yes "T4 no secret, .git, node_modules, quarantine, live-database or other-seat file is on the NAS" p_no_secret_on_nas
yes "T4 NEIGHBOUR: the ordinary file beside them arrived" test -f "$(CUR)/sub/notsecret.txt"
has "T4 the run names the exclusions by category" "$(OUTF t4.txt)" "secret="
echo "leak" > "$T/nas/General/Wednesday/nightly-backup/current/WEDNESDAY/secret.txt"
canfail "the no-secret predicate, with a secret planted on the fake NAS by hand" p_no_secret_on_nas
#   the engine-log secret check: an engine that claims it sent a secret-shaped path fails the run
fixture main4b
S="$(mk_stub rsync_claims_secret '"$REAL" "$@"; rc=$?; echo ">f+++++++++ 4_Credentials/leaked.txt"; exit $rc')"
write_conf "$S"
to t4b.txt nb --run --now "$(at 0 1 0)"
no  "T4 an engine log naming a secret-shaped path FAILS the run" test "$RC" -eq 0
has "T4 ... and says so" "$(OUTF t4b.txt)" "secret-shaped name travelled"

echo; echo "T5  REFUSALS, each with a must-succeed neighbour"
#  a. NAS not mounted
fixture r_mount; write_mounts none
to a.txt nb --run --now "$(at 0 1 0)"
is  "T5a NAS not in the mount table: exit 2" 2 "$RC"
has "T5a says not mounted" "$(OUTF a.txt)" "not mounted as a network share"
no  "T5a nothing written to the fake NAS" test -e "$T/nas/General/Wednesday"
is  "T5a the refusal is recorded in the state file" refused "$(state last_attempt.status)"
write_mounts smbfs
to a2.txt nb --run --now "$(at 0 1 0)"
is  "T5a NEIGHBOUR mounted: exit 0" 0 "$RC"
#  a'. mounted, but not as a network share (a plain local folder named like the NAS)
fixture r_mount2; write_mounts "apfs, local"
to a.txt nb --run --now "$(at 0 1 0)"
is  "T5a' a LOCAL folder at the NAS path: exit 2" 2 "$RC"
#  b. expected top-level folder absent
fixture r_absent; mkdir -p "$T/held"; mv -n "$T/nas/General" "$T/held/General"
to b.txt nb --run --now "$(at 0 1 0)"
is  "T5b top-level client folder absent: exit 2" 2 "$RC"
has "T5b says which folder" "$(OUTF b.txt)" "no top-level folder 'General'"
no  "T5b the folder was NOT created for us" test -e "$T/nas/General"
mv -n "$T/held/General" "$T/nas/General"
to b2.txt nb --run --now "$(at 0 1 0)"
is  "T5b NEIGHBOUR folder present: exit 0" 0 "$RC"
#  c. top-level name differs in CASE (the 2026-08-25 shape: the scratch volume folds case like the share)
fixture r_case; mkdir -p "$T/held"; mv -n "$T/nas/Secuura" "$T/held/x"; mv -n "$T/held/x" "$T/nas/secuura"
to c.txt nb --run --now "$(at 0 1 0)"
is  "T5c 'secuura' where 'Secuura' is expected: exit 2" 2 "$RC"
has "T5c says the names differ in case" "$(OUTF c.txt)" "differ in CASE"
is  "T5c nothing started" 0 "$(started)"
mv -n "$T/nas/secuura" "$T/held/y"; mv -n "$T/held/y" "$T/nas/Secuura"
to c2.txt nb --run --now "$(at 0 1 0)"
is  "T5c NEIGHBOUR exact case: exit 0" 0 "$RC"
#  c'. a deeper level differs in case (the seat folder)
fixture r_case2; mkdir -p "$T/nas/General/wednesday"
to c.txt nb --run --now "$(at 0 1 0)"
is  "T5c' seat folder 'wednesday' where 'Wednesday' is expected: exit 2" 2 "$RC"
#  d. free space below the floor
fixture r_free; echo 5 > "$T/free_gib.txt"
to d.txt nb --run --now "$(at 0 1 0)"
is  "T5d free space under the floor: exit 2" 2 "$RC"
has "T5d says the floor" "$(OUTF d.txt)" "below the floor of 200 GiB"
echo 5000 > "$T/free_gib.txt"
to d2.txt nb --run --now "$(at 0 1 0)"
is  "T5d NEIGHBOUR enough space: exit 0" 0 "$RC"
#  e. lock held by a live run; then a STALE lock, which is reported and never removed silently
fixture r_lock; mkdir -p "$T/lane/state/wednesday.lock.d"
bash -c 'exec -a nas_backup_fakeholder sleep 120' & HOLDER=$!
sleep 1
owner_json "$HOLDER"
to e.txt nb --run --now "$(at 0 1 0)"
is  "T5e live lock: exit 6" 6 "$RC"
has "T5e names the holder" "$(OUTF e.txt)" "another run holds the lock"
kill "$HOLDER" 2>&1; wait "$HOLDER" 2>&1
to e2.txt nb --run --now "$(at 0 1 0)"
is  "T5e the holder died: the lock is now STALE: still exit 6" 6 "$RC"
has "T5e says STALE and that it was not removed" "$(OUTF e2.txt)" "STALE lock"
yes "T5e the stale lock is still there (never removed silently)" test -d "$T/lane/state/wednesday.lock.d"
to e3.txt nb --clear-stale-lock
is  "T5e --clear-stale-lock exits 0" 0 "$RC"
yes "T5e the stale lock was MOVED into a quarantine folder, not deleted" test -n "$(find "$T/lane/state" -path '*_quarantine_*' -name 'wednesday.stale.*' 2>&1)"
to e4.txt nb --run --now "$(at 0 1 0)"
is  "T5e NEIGHBOUR no lock: exit 0" 0 "$RC"
#  f. the source drive is not the seat's own
fixture r_src; write_mounts smbfs "smbfs, nodev"
to f.txt nb --run --now "$(at 0 1 0)"
is  "T5f source volume is a network mount, not a local drive: exit 2" 2 "$RC"
has "T5f says so" "$(OUTF f.txt)" "not mounted as a local drive"
write_mounts
to f2.txt nb --run --now "$(at 0 1 0)"
is  "T5f NEIGHBOUR local drive: exit 0" 0 "$RC"
fixture r_src2; mkdir -p "$T/othervol/proj"; echo z > "$T/othervol/proj/z.txt"
write_conf "" refuse "set=General|Other|$T/othervol/proj"
to f.txt nb --run --now "$(at 0 1 0)"
is  "T5f' a source outside the seat's drive: exit 2" 2 "$RC"
has "T5f' says so" "$(OUTF f.txt)" "not on the seat's own drive"
is  "T5f' nothing started" 0 "$(started)"
#  g. another client's folder, as destination and as source
fixture r_client; mkdir -p "$T/vol/CODING/plainproj"; echo p > "$T/vol/CODING/plainproj/p.txt"
write_conf "" refuse "set=Datasec|X|$T/vol/CODING/plainproj"      # an ordinary source: only the allow-list of client folders can refuse this line
to g.txt nb --run --now "$(at 0 1 0)"
is  "T5g destination in another client's folder: exit 2" 2 "$RC"
has "T5g says allow-list" "$(OUTF g.txt)" "not on seat wednesday's allow-list"
no  "T5g nothing written under Datasec" test -e "$T/nas/Datasec/Wednesday"
fixture r_client2; mkdir -p "$T/vol/CODING/Datasec/proj"; echo d > "$T/vol/CODING/Datasec/proj/d.txt"
write_conf "" refuse "set=General|Proj|$T/vol/CODING/Datasec/proj"
to g.txt nb --run --now "$(at 0 1 0)"
is  "T5g' a Datasec source path: exit 2" 2 "$RC"
has "T5g' says another client's material" "$(OUTF g.txt)" "another client's material"
write_conf
to g2.txt nb --run --now "$(at 0 1 0)"
is  "T5g NEIGHBOUR own clients only: exit 0" 0 "$RC"
#  h. the seat: disagreement and an unknown tree
fixture r_seat
env WED_AGENT=tuesday NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup.sh" --run --now "$(at 0 1 0)" > "$T/out/h.txt" 2>&1; RC=$?
is  "T5h WED_AGENT=tuesday on a WEDNESDAY tree: exit 2" 2 "$RC"
has "T5h says the sources disagree" "$(OUTF h.txt)" "disagree"
mkdir -p "$T/vol/ODDNAME"
env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/ODDNAME" "$LANE/nas_backup.sh" --run --now "$(at 0 1 0)" > "$T/out/h2.txt" 2>&1; RC=$?
is  "T5h a tree that is no seat's: exit 2" 2 "$RC"
has "T5h says it cannot tell the seat" "$(OUTF h2.txt)" "cannot tell which seat"
is  "T5h nothing started" 0 "$(started)"
env WED_AGENT=wednesday NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup.sh" --run --now "$(at 0 1 0)" > "$T/out/h3.txt" 2>&1; RC=$?
is  "T5h NEIGHBOUR WED_AGENT agrees with the tree: exit 0" 0 "$RC"
#  i. outside the window
fixture r_window
to i.txt nb --run --now "$(at 0 14 0)"
is  "T5i a real run at 14:00: exit 2" 2 "$RC"
has "T5i says outside the window and names Kam's approval" "$(OUTF i.txt)" "outside this seat's nightly window"
is  "T5i nothing started" 0 "$(started)"
to i2.txt nb --run --now "$(at 0 14 0)" --out-of-sequence "nas-backup-overdue-wednesday-20261201"
is  "T5i NEIGHBOUR the same time with --out-of-sequence <card id>: exit 0" 0 "$RC"
has "T5i the manifest records the approval" "$(find "$T/nas/General/Wednesday/nightly-backup/manifests" -name '*_manifest.json' | head -1)" "out-of-sequence: nas-backup-overdue-wednesday-20261201"
to i3.txt nb --run --now "$(at 1 14 0)" --out-of-sequence "x"
is  "T5i an empty-ish approval is refused: exit 2" 2 "$RC"
#  j. the hold file
fixture r_hold; echo "held" > "$T/lane/HOLD_wednesday"
to j.txt nb --run --now "$(at 0 1 0)"
is  "T5j HOLD file present: exit 3" 3 "$RC"
is  "T5j nothing started" 0 "$(started)"
to j1.txt nb --dry
is  "T5j a dry run is still allowed under the hold: exit 0" 0 "$RC"
mv -n "$T/lane/HOLD_wednesday" "$T/lane/HOLD_wednesday.lifted"
to j2.txt nb --run --now "$(at 0 1 0)"
is  "T5j NEIGHBOUR hold moved aside: exit 0" 0 "$RC"
#  k. an unconfirmed configuration, and a forbidden engine flag
fixture r_conf; CONF_STATUS=unconfirmed; write_conf
to k.txt nb --run --now "$(at 0 1 0)"
is  "T5k status=unconfirmed: exit 2" 2 "$RC"
CONF_STATUS=confirmed; write_conf
to k2.txt nb --run --now "$(at 0 1 0)"
is  "T5k NEIGHBOUR confirmed: exit 0" 0 "$RC"
"$PY" -c 'import sys; sys.path.insert(0, sys.argv[1]); import nb_core
for flag in ("--delete", "--delete-after", "--del", "--remove-source-files", "--inplace", "--force"):
    try:
        nb_core.check_argv(["rsync", "-t", flag, "a/", "b/"]); print("NOT REFUSED", flag); sys.exit(1)
    except nb_core.Refused: pass
print("all refused")' "$LANE" > "$T/out/k3.txt" 2>&1; RC=$?
is  "T5k every deletion-capable engine flag is refused before the engine starts" 0 "$RC"
#  m. a set too large to copy and count in one night
fixture r_max; write_conf "" refuse "max_files=3"
to m.txt nb --run --now "$(at 0 1 0)"
is  "T5m a set above max_files: exit 2" 2 "$RC"
has "T5m says where the files are" "$(OUTF m.txt)" "above max_files=3"
no  "T5m nothing copied for that set" test -e "$(CUR)/a.txt"
is  "T5m state: not good" None "$(state last_good)"
write_conf
to m2.txt nb --run --now "$(at 0 1 0)"
is  "T5m NEIGHBOUR default ceiling: exit 0" 0 "$RC"
#  n. a project folder that is not listed is never swept in, and never silently skipped
fixture r_unlisted; mkdir -p "$T/vol/CODING/NewProject" "$T/vol/CODING/Datasec"; echo n > "$T/vol/CODING/NewProject/n.txt"
write_conf "" refuse "report_unlisted_under=$T/vol/CODING"
to n.txt nb --run --now "$(at 0 1 0)"
is  "T5n run exits 0" 0 "$RC"
has "T5n the unlisted folder is named as NOT backed up" "$(OUTF n.txt)" "NOT backed up: $T/vol/CODING/NewProject"
has "T5n another client's folder is named as not this seat's" "$(OUTF n.txt)" "not this seat's (never backed up from here): $T/vol/CODING/Datasec"
no  "T5n the unlisted folder did not travel" test -n "$(find "$T/nas" -name 'n.txt' 2>&1)"
hasnt "T5n NEIGHBOUR the listed Secuura folder is not reported as unlisted" "$(OUTF n.txt)" "NOT backed up: $T/vol/CODING/Secuura"
#  l. --now outside test mode is refused (the real clock is never supplied by hand)
env -u WED_AGENT -u NB_TEST_ROOT "$LANE/nas_backup_watch.sh" --check --now 1 > "$T/out/l.txt" 2>&1; RC=$?
is  "T5l --now without test mode: exit 2" 2 "$RC"

echo; echo "T6  a DELETING line in the engine's log fails the run whatever the exit code"
fixture del
S="$(mk_stub rsync_deleting '"$REAL" "$@"; rc=$?; echo "*deleting   planted/gone.txt"; exit $rc')"
write_conf "$S"
to d.txt nb --run --now "$(at 0 1 0)"
is  "T6 exit 9 although the engine exited 0" 9 "$RC"
has "T6 says DELETING" "$(OUTF d.txt)" "DELETING line"
is  "T6 state: the attempt is failed, not good" failed "$(state last_attempt.status)"
is  "T6 state: no good backup recorded" None "$(state last_good)"
is  "T6 no COMPLETE marker" 0 "$(completed)"
write_conf
to d2.txt nb --run --now "$(at 0 2 0)"
is  "T6 NEIGHBOUR the real engine, same fixture: exit 0" 0 "$RC"
#   stall and cap
fixture stall
S="$(mk_stub rsync_silent 'sleep 30')"; CONF_STALL=3; write_conf "$S"
to s.txt nb --run --now "$(at 0 1 0)"
is  "T6 a silent, idle engine is stopped as STALLED: exit 7" 7 "$RC"
is  "T6 state says stalled" stalled "$(state last_attempt.status)"
fixture cap
S="$(mk_stub rsync_slow 'echo "cd+++++++++ ./"; sleep 30')"; write_conf "$S"
to c.txt nb --run --now "$(at 0 1 0)" --max-seconds 3
is  "T6 an overlong engine is stopped by the cap: exit 4" 4 "$RC"
is  "T6 state says killed-cap" killed-cap "$(state last_attempt.status)"

echo; echo "T7  NIGHTLY catch-up, with the clock supplied"
fixture night
to n0.txt nightly --now "$(at 0 0 31)"
is  "T7 first night, in the window, no backup on record: runs, exit 0" 0 "$RC"
has "T7 decision RUN" "$(OUTF n0.txt)" "RUN: no good backup on record"
to n1.txt nightly --now "$(at 0 1 31)"
has "T7 a second fire the same night SKIPS (already backed up)" "$(OUTF n1.txt)" "SKIP: already backed up"
is  "T7 ... and only one run happened" 2 "$(started)"
is  "T7 ... the fire and its decision are RECORDED in the state file" "skip" "$(state last_fire.decision)"
to n2.txt nightly --now "$(at 0 14 0)"
has "T7 a fire at 14:00 the same day SKIPS (already backed up for that window)" "$(OUTF n2.txt)" "SKIP: already backed up"
#   missed ONE night: nothing fired on day 1; day 2's window catches up
to n3.txt nightly --now "$(at 2 0 31)"
has "T7 missed one night: the next window RUNS and says it is catching up" "$(OUTF n3.txt)" "1 night(s) missed: catching up"
is  "T7 ... good" good "$(state last_attempt.status)"
#   a fire OUTSIDE the window with a night missed does not run on its own (pair: the same state inside the window runs)
to n4.txt nightly --now "$(at 3 14 0)" --decide-only
has "T7 day 3, 14:00, day-3 night missed: SKIP, outside the window" "$(OUTF n4.txt)" "SKIP: fired outside the nightly window"
to n5.txt nightly --now "$(at 3 3 0)" --decide-only
has "T7 PAIR the same state at 03:00: RUN" "$(OUTF n5.txt)" "RUN: no good backup since"
#   late_fire=run: the looser reading, selectable in the conf
write_conf "" run
to n6.txt nightly --now "$(at 3 14 0)" --decide-only
has "T7 with late_fire=run the 14:00 fire would run" "$(OUTF n6.txt)" "RUN-LATE"
write_conf
#   a run in progress
mkdir -p "$T/lane/state/wednesday.lock.d"
bash -c 'exec -a nas_backup_fakeholder sleep 120' & HOLDER=$!
sleep 1
owner_json "$HOLDER"
to n7.txt nightly --now "$(at 3 0 31)"
has "T7 a run in progress: SKIP with the reason" "$(OUTF n7.txt)" "SKIP: a run is in progress"
is  "T7 ... exit 0" 0 "$RC"
kill "$HOLDER" 2>&1; wait "$HOLDER" 2>&1
to n7b.txt nb --clear-stale-lock
yes "T7 every nightly decision is in the nightly log" test "$(/usr/bin/grep -c -F 'nightly[wednesday]' "$T/lane/logs/wednesday/nightly.log")" -ge 6

echo; echo "T8  THREE nights missed: the card reaches the place a booting seat READS, consumes nothing, and exists once per gap"
#   last good = day 2 00:31. The NAS is away for the nights of day 3, 4 and 5.
write_mounts none
to f3.txt nightly --now "$(at 3 0 31)"
is  "T8 night 1 without the NAS: refused, exit 2" 2 "$RC"
to f4.txt nightly --now "$(at 4 0 31)"
to f4w.txt watch --check --now "$(at 4 9 0)"
is  "T8 after 2 days: not yet overdue (exit 0)" 0 "$RC"
to f5.txt nightly --now "$(at 5 0 31)"
has   "T8 night 3: the nightly job says OVERDUE in its own log" "$(OUTF f5.txt)" "OVERDUE"
hasnt "T8 ... but the nightly job (a launchd log no seat reads) NEVER prints the card command" "$(OUTF f5.txt)" "CARD-COMMAND:"
to f5d.txt doctor_block "$(at 5 8 0)"
has "T8 at the next boot doctor prints a HARD-failure line" "$(OUTF f5d.txt)" "✗ NO GOOD NAS BACKUP FOR 3 DAYS"
HARD="$(/usr/bin/grep -F '✗' "$(OUTF f5d.txt)" | cut -c1-400)"
yes "T8 that line, cut at 400 characters as the launcher cuts it, still names the one command to run" test "${HARD#*nas_backup_watch.sh --card}" != "$HARD"
to f5c.txt watch --card --now "$(at 5 8 1)"
is  "T8 running that command: exit 3" 3 "$RC"
has "T8 ... prints the card command" "$(OUTF f5c.txt)" "CARD-COMMAND:"
has "T8 it is a decision_queue.sh add with a fixed id for the gap" "$(OUTF f5c.txt)" "decision_queue.sh add --id nas-backup-overdue-wednesday-20261203"
has "T8 option a = approve an out-of-sequence backup now" "$(OUTF f5c.txt)" "a:Approve an out-of-sequence backup now"
has "T8 option b = wait for tonight's window, the default" "$(OUTF f5c.txt)" "--recommended b"
has "T8 the BLUF carries the failure reason" "$(OUTF f5c.txt)" "not mounted as a network share"
has "T8 the BLUF counts all three failed nights (the attempt history is not cut short)" "$(OUTF f5c.txt)" "3 attempts"
to f5c2.txt watch --card --now "$(at 5 20 0)"
has "T8 printing consumed nothing: a second call prints the command again" "$(OUTF f5c2.txt)" "CARD-COMMAND:"
to f6.txt nightly --now "$(at 6 0 31)"
to f6d.txt doctor_block "$(at 6 8 0)"
has "T8 a later boot, card still not raised: doctor still fails hard" "$(OUTF f6d.txt)" "✗ NO GOOD NAS BACKUP"
to g_mark.txt watch --mark-raised nas-backup-overdue-wednesday-20261203 --now "$(at 6 9 5)"
is  "T8 state records the card as raised" True "$(state flag.raised)"
to g6c.txt watch --card --now "$(at 6 9 6)"
is  "T8 once raised: exit 4" 4 "$RC"
hasnt "T8 once raised, the card command is not printed again for this gap" "$(OUTF g6c.txt)" "CARD-COMMAND:"
to g6d.txt doctor_block "$(at 6 9 7)"
hasnt "T8 once raised, doctor no longer fails hard" "$(OUTF g6d.txt)" "✗"
has   "T8 ... it warns instead" "$(OUTF g6d.txt)" "⚠ no good NAS backup for 3 days"
#   the NAS comes back: the next window runs, the gap closes
write_mounts
to g7.txt nightly --now "$(at 7 0 31)"
has "T8 NAS back: the next window runs and names the missed nights" "$(OUTF g7.txt)" "night(s) missed: catching up"
to g7w.txt watch --check --now "$(at 7 9 0)"
is  "T8 after a good backup the watch is quiet (exit 0)" 0 "$RC"
to g7d.txt doctor_block "$(at 7 9 1)"
hasnt "T8 ... and so is doctor" "$(OUTF g7d.txt)" "✗"
#   a NEW gap is a NEW card
write_mounts none
to h8.txt nightly --now "$(at 8 0 31)"; to h9.txt nightly --now "$(at 9 0 31)"; to h10.txt nightly --now "$(at 10 0 31)"
to h10c.txt watch --card --now "$(at 10 9 0)"
has "T8 a second gap: a NEW card id" "$(OUTF h10c.txt)" "decision_queue.sh add --id nas-backup-overdue-wednesday-20261208"

echo; echo "T9  the watch does not depend on the backup job, on the NAS, or on any mark set by another script"
fixture never
to w0.txt watch --check --now "$(at 0 9 0)"
is  "T9 nothing on record: exit 0" 0 "$RC"
has "T9 the watch starts the clock itself" "$(OUTF w0.txt)" "the three-day clock starts now"
to w2.txt watch --check --now "$(at 2 9 0)"
is  "T9 48 h, the job never fired: not yet overdue" 0 "$RC"
to w3.txt watch --card --now "$(at 3 9 1)"
is  "T9 72 h, the job NEVER fired and nobody armed anything: OVERDUE (exit 3)" 3 "$RC"
has "T9 the card says the job did not fire" "$(OUTF w3.txt)" "the job did not fire"
mv -n "$T/lane/seats/wednesday.conf" "$T/lane/seats/wednesday.conf.aside"; write_mounts none
to w4.txt watch --check --now "$(at 3 9 2)"
is  "T9 it still reports with the NAS away and the conf missing (exit 3)" 3 "$RC"
mv -n "$T/lane/seats/wednesday.conf.aside" "$T/lane/seats/wednesday.conf"
echo "held" > "$T/lane/HOLD_wednesday"
to w5.txt watch --card --now "$(at 4 9 0)"
is  "T9 HELD: exit 0" 0 "$RC"
has "T9 HELD is said out loud" "$(OUTF w5.txt)" "HELD:"
hasnt "T9 HELD raises no card" "$(OUTF w5.txt)" "CARD-COMMAND:"
to w5d.txt doctor_block "$(at 4 9 0)"
has "T9 doctor reports HELD" "$(OUTF w5d.txt)" "⚠ nightly NAS backup HELD"
to w5e.txt doctor_block "$(at 4 9 1)"
hasnt "T9 ... once a day at most: the second boot the same day does not warn again" "$(OUTF w5e.txt)" "⚠"
mv -n "$T/lane/HOLD_wednesday" "$T/lane/HOLD_wednesday.lifted"
to w6.txt watch --check --now "$(at 4 9 2)"
is  "T9 PAIR the hold moved aside, same state: overdue (exit 3)" 3 "$RC"
#   finding 5: ten days of refused fires, four a night, and no arming mark: the first attempt must not roll away
fixture noarm; write_mounts none
for d in 0 1 2 3 4 5 6 7 8 9; do for hm in "0 31" "1 30" "2 30" "3 30"; do nightly --now "$(at $d $hm)" > "$T/out/roll.txt" 2>&1; done; done
is  "T9 forty refused attempts on record are capped, not unbounded" 40 "$("$PY" -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["recent_attempts"]))' "$T/lane/state/wednesday.json")"
to r3.txt watch --check --now "$(at 9 9 0)"
is  "T9 day 10, never armed, 40 refused fires: OVERDUE (exit 3), not 'ok since the first recorded attempt'" 3 "$RC"
has "T9 the clock still starts at the FIRST attempt (day 1)" "$(OUTF r3.txt)" "2026-12-01 00:31"

echo; echo "T10 the oldest python on the target machines (/usr/bin/python3)"
if [ -x /usr/bin/python3 ]; then
  fixture py39
  env -u WED_AGENT NB_PYTHON=/usr/bin/python3 NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup.sh" --run --now "$(at 0 1 0)" > "$T/out/p.txt" 2>&1; RC=$?
  is  "T10 a real run under $(/usr/bin/python3 --version 2>&1): exit 0" 0 "$RC"
  has "T10 GOOD" "$(OUTF p.txt)" "GOOD: every in-scope"
else
  echo "  SKIP  /usr/bin/python3 not present"
fi

echo; echo "T11 names that differ only in case: neither is copied, both are named (the scratch volume cannot hold such a pair, so the listing is supplied)"
fixture collide
env -u WED_AGENT NB_TEST_ROOT="$T" "$PY" -c 'import sys, os
sys.path.insert(0, sys.argv[1]); import nb_core
T = os.environ["NB_TEST_ROOT"]
ctx = nb_core.Ctx("wednesday", T + "/vol/WEDNESDAY", 1); ctx.load_conf()
real = nb_core.walk
def fake(top, rules=None, **kw):
    if rules is None:
        return real(top)
    return {"files": {"keep.txt": (1, 1, 1), "Logs/x.txt": (1, 1, 1), "logs/y.txt": (1, 1, 1), "ev/A.out": (1, 1, 1), "ev/a.out": (1, 1, 1)},
            "dirs": set(["Logs", "logs", "ev"]), "links": {}, "specials": [], "excluded": {}, "errors": [], "hardlinks": []}
nb_core.walk = fake
plan = nb_core.plan_set(ctx, ctx.conf["sets"][0], {}, None, None, do_hash=False)
print("copy=%s" % ",".join(plan["copy"]))
print("copy_dirs=%s" % ",".join(plan["copy_dirs"]))
print("skipped=%d names=%d problems=%d" % (len(plan["collision_skipped"]), len(plan["collisions"]), len(plan["problems"])))' "$LANE" > "$T/out/c.txt" 2>&1; RC=$?
is  "T11 the planner ran" 0 "$RC"
has "T11 only the non-colliding file is planned for copy" "$(OUTF c.txt)" "copy=keep.txt"
has "T11 a folder pair that collides is not created; the clean folder is" "$(OUTF c.txt)" "copy_dirs=ev"
has "T11 four files under four colliding names are counted as not backed up, and it is not a failure" "$(OUTF c.txt)" "skipped=4 names=4 problems=0"
env -u WED_AGENT NB_TEST_ROOT="$T" "$PY" -c 'import sys, os
sys.path.insert(0, sys.argv[1]); import nb_core
T = os.environ["NB_TEST_ROOT"]
ctx = nb_core.Ctx("wednesday", T + "/vol/WEDNESDAY", 1); ctx.load_conf()
real = nb_core.walk
def fake(top, rules=None, **kw):
    if rules is None:
        return real(top)
    return {"files": {"ev/A.out": (1, 1, 1), "ev/a.out": (1, 1, 1)}, "dirs": set(["ev"]), "links": {}, "specials": [], "excluded": {}, "errors": [], "hardlinks": []}
nb_core.walk = fake
plan = nb_core.plan_set(ctx, ctx.conf["sets"][0], {}, None, None, do_hash=False)
print("copy=%d skipped=%d empty-scope-problems=%d" % (len(plan["copy"]), len(plan["collision_skipped"]), sum(1 for p in plan["problems"] if p.startswith("EMPTY SCOPE"))))' "$LANE" > "$T/out/c2.txt" 2>&1; RC=$?
has "T11 a set whose ONLY files are a case-colliding pair has an EMPTY plan, and that is a failure (round 3)" "$(OUTF c2.txt)" "copy=0 skipped=2 empty-scope-problems=1"

# ═════════════════════════════════════════════ ROUND 2: the checker's attacks, lifted ═════════════════════════
MARK="NBSECRETMARKERr2"
on_nas() { /usr/bin/grep -r -l -F -- "$1" "$T/nas" 2>&1 | wc -l | tr -d ' '; }

echo; echo "T12 FALSE GOOD (QA finding 1): a changed file that was not delivered must FAIL the run, be NAMED, and stay unproven"
#   H1: the destination copy is immutable (stands in for a file locked on the share); same-size change at the source
fixture fg1; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do echo "filler $i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
printf 'LEDGER-v1-AAAA\n' > "$T/vol/WEDNESDAY/ledger.db"
to r0.txt nb --run --now "$(at 0 1 0)"
is  "T12 first night GOOD" 0 "$RC"
chflags uchg "$(CUR)/ledger.db"
sleep 1; printf 'LEDGER-v2-BBBB\n' > "$T/vol/WEDNESDAY/ledger.db"
to r1.txt nb --run --now "$(at 1 1 0)"
chflags nouchg "$(CUR)/ledger.db"
no  "T12 H1 same-size change, destination copy immutable: the run is NOT exit 0" test "$RC" -eq 0
hasnt "T12 H1 it does not say GOOD" "$(OUTF r1.txt)" "GOOD: every in-scope"
has "T12 H1 the undelivered file is NAMED in the run's last lines" "$(OUTF r1.txt)" "NOT DELIVERED: WEDNESDAY/ledger.db"
is  "T12 H1 the state the watch reads counts it" 1 "$(state last_attempt.undelivered_count)"
is  "T12 H1 the last good run is still the first night" "$(at 0 1 0).0" "$(state last_good.time)"
to r1w.txt watch --check --now "$(at 1 2 0)"
has "T12 H1 the watch's line names the file" "$(OUTF r1w.txt)" "NOT DELIVERED, first: WEDNESDAY/ledger.db"
yes "T12 H1 control: the destination really is stale" /usr/bin/grep -q -F 'LEDGER-v1-AAAA' "$(CUR)/ledger.db"
chflags uchg "$(CUR)/ledger.db"
to r2.txt nb --run --now "$(at 2 1 0)"
chflags nouchg "$(CUR)/ledger.db"
no  "T12 H1 next night, NOTHING changed at the source: still not GOOD (the file was never indexed as arrived)" test "$RC" -eq 0
has "T12 H1 ... and it is sent again" "$(OUTF r2.txt)" "to copy: 1 files"
to r3.txt nb --run --now "$(at 3 1 0)"
is  "T12 H1 NEIGHBOUR the lock on the destination copy lifted: GOOD" 0 "$RC"
yes "T12 H1 ... and the new content is there" /usr/bin/grep -q -F 'LEDGER-v2-BBBB' "$(CUR)/ledger.db"
#   H2: an engine that skips one listed file and exits 23
fixture fg2; printf 'LEDGER-v1-AAAA\n' > "$T/vol/WEDNESDAY/ledger.db"
to r0.txt nb --run --now "$(at 0 1 0)"
S="$(mk_stub rsync_skip_one 'args=(); for a in "$@"; do case "$a" in --files-from=*) L="${a#--files-from=}"; tr "\0" "\n" < "$L" | /usr/bin/grep -v "^ledger.db$" | tr "\n" "\0" > "$L.filtered"; args+=( "--files-from=$L.filtered" );; *) args+=( "$a" );; esac; done; "$REAL" "${args[@]}"; echo "rsync: [sender] read errors mapping \"ledger.db\": Input/output error (5)" >&2; exit 23')"
write_conf "$S"
sleep 1; printf 'LEDGER-v2-CCCC\n' > "$T/vol/WEDNESDAY/ledger.db"; echo "also changed" > "$T/vol/WEDNESDAY/a.txt"
to r1.txt nb --run --now "$(at 1 1 0)"
no  "T12 H2 engine skips one file and exits 23: the run is NOT exit 0" test "$RC" -eq 0
has "T12 H2 the skipped file is named" "$(OUTF r1.txt)" "NOT DELIVERED: WEDNESDAY/ledger.db"
yes "T12 H2 the file that DID arrive is proven and current" cmp -s "$T/vol/WEDNESDAY/a.txt" "$(CUR)/a.txt"
write_conf
to r2.txt nb --run --now "$(at 2 1 0)"
is  "T12 H2 NEIGHBOUR a healthy engine the next night: GOOD" 0 "$RC"
yes "T12 H2 ... the changed content arrived" /usr/bin/grep -q -F 'LEDGER-v2-CCCC' "$(CUR)/ledger.db"
#   exit 23 with every listed path proven is survived (a listed file that vanished before the copy)
fixture fg3
S="$(mk_stub rsync_exit23_all_arrive '"$REAL" "$@"; echo "rsync: some noise" >&2; exit 23')"; write_conf "$S"
to r0.txt nb --run --now "$(at 0 1 0)"
is  "T12 an engine that exits 23 although EVERY listed file arrived and is proven: GOOD (the proof decides, not the code)" 0 "$RC"
#   a file not sent tonight whose destination copy has gone bad is caught by the sample (QA mutant Q09)
fixture fg4
to r0.txt nb --run --now "$(at 0 1 0)"
printf 'XXX content of a\n' > "$(CUR)/a.txt"
to r1.txt nb --run --now "$(at 1 1 0)"
is  "T12 a destination copy that changed behind our back (same size) is found by the sample and REPAIRED in the same run: exit 0" 0 "$RC"
has "T12 ... the sample of unsent files says so" "$(OUTF r1.txt)" "SAMPLE: 1 of"
yes "T12 ... the destination holds the source's content again" cmp -s "$T/vol/WEDNESDAY/a.txt" "$(CUR)/a.txt"
yes "T12 ... and the wrong content it held is kept under versions/" test -n "$(/usr/bin/grep -r -l -x -F 'XXX content of a' "$(VER)" 2>&1)"
is  "T12 ... the repair is counted in the state" 1 "$(state last_good.counts.repaired)"

#   a file that CHANGES WHILE the run is copying is sent again, and the re-send never overwrites the previous night's kept copy
fixture live; echo "night1 content" > "$T/vol/WEDNESDAY/live.log"
to r0.txt nb --run --now "$(at 0 1 0)"
echo "night2 content, longer" > "$T/vol/WEDNESDAY/live.log"
S="$(mk_stub rsync_source_moves_once '"$REAL" "$@"; rc=$?; if [ ! -e "$STUBDIR/once" ]; then : > "$STUBDIR/once"; echo "appended during the copy" >> "$STUBDIR/../vol/WEDNESDAY/live.log"; fi; exit $rc')"; write_conf "$S"
to r1.txt nb --run --now "$(at 1 1 0)"
is  "T12 a file appended to DURING the copy: the run re-sends it and is GOOD" 0 "$RC"
has "T12 ... it says one file was re-sent" "$(OUTF r1.txt)" "1 re-sent because the source changed meanwhile"
yes "T12 ... the destination holds the source's FINAL content" cmp -s "$T/vol/WEDNESDAY/live.log" "$(CUR)/live.log"
yes "T12 ... night 1's copy is STILL kept under versions/ (the re-send did not overwrite it)" test -n "$(/usr/bin/grep -r -l -x -F 'night1 content' "$(VER)" 2>&1)"
yes "T12 ... and the intermediate copy went to its own _pass2 folder" test -n "$(find "$(VER)" -path '*_pass2*' -name live.log 2>&1)"
fixture live2; echo "night1 content" > "$T/vol/WEDNESDAY/live.log"
to r0.txt nb --run --now "$(at 0 1 0)"
S="$(mk_stub rsync_source_always_moves '"$REAL" "$@"; rc=$?; echo "appended again" >> "$STUBDIR/../vol/WEDNESDAY/live.log"; exit $rc')"; write_conf "$S"
echo "night2" >> "$T/vol/WEDNESDAY/live.log"
to r1.txt nb --run --now "$(at 1 1 0)"
no  "T12 a file that changes after EVERY pass is never proven: the run is NOT exit 0" test "$RC" -eq 0
has "T12 ... and it is named" "$(OUTF r1.txt)" "NOT DELIVERED: WEDNESDAY/live.log"

echo; echo "T13 SECRETS BY SHAPE (QA finding 2): any case, any decoration, and hard links"
fixture sec; W="$T/vol/WEDNESDAY"
mkdir -p "$W/v1/4_credentials" "$W/v2/4_CREDENTIALS" "$W/v3/3_access_keys" "$W/v4/.SSH" "$W/v5/.AWS" \
         "$W/d1/4_Credentials (conflict_on_2026-09-17)" "$W/d2/4_Credentials.bak" "$W/d3/4_Credentials copy" "$W/d4/old_3_Access_Keys" \
         "$W/files" "$W/4_Credentials"
for d in v1/4_credentials v2/4_CREDENTIALS v3/3_access_keys v4/.SSH v5/.AWS "d1/4_Credentials (conflict_on_2026-09-17)" d2/4_Credentials.bak "d3/4_Credentials copy" d4/old_3_Access_Keys; do echo "$MARK $d" > "$W/$d/inside.txt"; done
for f in .ENV .Env.local server.PEM private.KEY ID_RSA Credentials.json Secrets.json ".env (conflict_on_2026-09-17)" prod.env.bak .envrc .env1 \
         github_deploy_rw .git-credentials key.ppk terraform.tfstate client_secret.json x.p12 y.pfx z.key q.env id_ed25519.pub wallet.skey my_deploy_key server.pem.bak; do
  echo "$MARK $f" > "$W/files/$f"; done
echo "$MARK real secret" > "$W/4_Credentials/token.txt"
ln "$W/4_Credentials/token.txt" "$W/files/innocent_name.txt"        # a hard link INTO the secrets folder, under an ordinary name
echo "ordinary neighbour" > "$W/files/neighbour.txt"
is  "T13 control: the marker is planted in 35 files at the source" 35 "$(/usr/bin/grep -r -l -F -- "$MARK" "$W" | wc -l | tr -d ' ')"
to s.txt nb --run --now "$(at 0 1 0)"
is  "T13 run exits 0" 0 "$RC"
is  "T13 NOT ONE of the 35 marked files is on the NAS (case variants, decorated names, unlisted shapes, the hard link)" 0 "$(on_nas "$MARK")"
yes "T13 NEIGHBOUR the ordinary file beside them arrived" test -f "$(CUR)/files/neighbour.txt"
has "T13 the summary counts exclusions per secret shape" "$(OUTF s.txt)" "excluded as secret-shaped (entries, by shape; counts only): credential-file="
has "T13 ... the folder-name shape" "$(OUTF s.txt)" "credentials-folder-name=8"
has "T13 the hard-linked file is skipped and counted" "$(OUTF s.txt)" "SKIPPED: 1 file(s) with more than one hard link"
yes "T13 ... and NAMED in the manifest" /usr/bin/grep -r -q -F 'innocent_name.txt' "$T/lane/manifests/wednesday"
hasnt "T13 the summary prints counts, never a secret's name" "$(OUTF s.txt)" "github_deploy_rw"
echo "$MARK leak" > "$(CUR)/files/leaked_by_hand.txt"
is  "T13 CAN-FAIL: a marked file put on the fake NAS by hand IS found by the same count" 1 "$(on_nas "$MARK")"
#   AppleDouble litter is a FILE; a real folder of that shape is kept (QA minor)
fixture dotunder; mkdir -p "$T/vol/WEDNESDAY/._realfolder"; echo keep > "$T/vol/WEDNESDAY/._realfolder/keep.txt"; echo litter > "$T/vol/WEDNESDAY/._litter"
to s.txt nb --run --now "$(at 0 1 0)"
yes "T13 a real FOLDER named ._something is backed up with its contents" test -f "$(CUR)/._realfolder/keep.txt"
no  "T13 a ._ FILE (AppleDouble litter) is not" test -e "$(CUR)/._litter"

echo; echo "T14 OTHER CLIENTS AND SEATS (QA finding 3)"
fixture cli; W="$T/vol/WEDNESDAY"
mkdir -p "$W/sub/DataSec" "$W/sub/DATAsec-notes" "$W/sub/Tuesday-handover" "$W/projects/nexusai" "$W/projects/MPS Calculator" "$T/vol/CODING/Secuura/Blockchain/dataSEC" "$T/vol/CODING/Secuura/Blockchain/src/friday-lib"
echo "$MARK d1" > "$W/sub/DataSec/x.txt"; echo "$MARK d2" > "$W/sub/DATAsec-notes/x.txt"; echo "$MARK d3" > "$W/sub/Tuesday-handover/x.txt"; echo "$MARK d4" > "$T/vol/CODING/Secuura/Blockchain/dataSEC/x.txt"
echo "report" > "$W/projects/nexusai/report.md"; echo "calc" > "$W/projects/MPS Calculator/calc.md"; echo "lamps" > "$W/sub/lamps.txt"; echo "lib" > "$T/vol/CODING/Secuura/Blockchain/src/friday-lib/nextFriday.js"
printf 'token=nexusai\nword=mps\n' > "$T/lane/seats/wednesday.tokens"
to c.txt nb --run --now "$(at 0 1 0)"
is  "T14 run exits 0" 0 "$RC"
is  "T14 a name containing the other client's name, in ANY case, does not travel (4 planted, 3 spellings, both sets)" 0 "$(on_nas "$MARK")"
has "T14 ... and is counted as other-client" "$(OUTF c.txt)" "other-client="
yes "T14 inside a PROJECT folder a seat's weekday name is not a seat (a library file stays)" test -f "$T/nas/Secuura/Wednesday/nightly-backup/current/Secuura/Blockchain/src/friday-lib/nextFriday.js"
yes "T14 a folder under the other client's PROJECT name inside this seat's own tree is backed up (Kam's ruling on shared folders)" test -f "$(CUR)/projects/nexusai/report.md"
has "T14 ... and REPORTED per token" "$(OUTF c.txt)" "nexusai=1"
has "T14 the short token is a whole word: 'MPS Calculator' counts, 'lamps' does not" "$(OUTF c.txt)" "mps (whole word)=1"
#   set= sources: realpath first, forbidden by containment
fixture cli2; mkdir -p "$T/vol/CODING/Datasec/proj" "$T/vol/CODING/Datasec-archive/proj" "$T/vol/CODING/plain/proj"; echo d > "$T/vol/CODING/Datasec/proj/d.txt"; echo d > "$T/vol/CODING/Datasec-archive/proj/d.txt"; echo p > "$T/vol/CODING/plain/proj/p.txt"
ln -s "$T/vol/CODING/Datasec" "$T/vol/CODING/alias"; ln -s "$T/vol/CODING/plain/proj" "$T/vol/CODING/linkproj"; ln -s "$T/vol/CODING/plain" "$T/vol/CODING/plainalias"
write_conf "" refuse "set=General|Proj|$T/vol/CODING/Datasec-archive/proj"
to a.txt nb --run --now "$(at 0 1 0)"
is  "T14 a source under a folder whose name merely CONTAINS the client (Datasec-archive): exit 2" 2 "$RC"
has "T14 ... says why" "$(OUTF a.txt)" "contains 'datasec'"
write_conf "" refuse "set=General|Proj|$T/vol/CODING/alias/proj"
to b.txt nb --run --now "$(at 0 1 0)"
is  "T14 a source reached through a symlinked parent (alias -> Datasec): exit 2" 2 "$RC"
has "T14 ... the REAL path is named" "$(OUTF b.txt)" "real path $T/vol/CODING/Datasec/proj"
write_conf "" refuse "set=General|Proj|$T/vol/CODING/linkproj"
to c.txt nb --run --now "$(at 0 1 0)"
is  "T14 a source that is itself a symlink: exit 2" 2 "$RC"
has "T14 ... says it is a symlink" "$(OUTF c.txt)" "is a symlink"
write_conf "" refuse "set=General|Proj|$T/vol/CODING/plainalias/proj"
to c2.txt nb --run --now "$(at 0 1 0)"
is  "T14 a clean source reached through a symlinked parent: exit 2" 2 "$RC"
is  "T14 nothing started in any of the four" 0 "$(started)"
write_conf "" refuse "set=General|Proj|$T/vol/CODING/plain/proj"
to d.txt nb --run --now "$(at 0 1 0)"
is  "T14 NEIGHBOUR the same folder named by its real path: exit 0" 0 "$RC"
write_conf "" refuse "set=General|../escape|$T/vol/CODING/plain/proj"
to e.txt nb --run --now "$(at 1 1 0)"
is  "T14 a destination name with .. in it: exit 2" 2 "$RC"
has "T14 ... says so" "$(OUTF e.txt)" "must be a plain relative name"
#   DEEPER than the forbidden-root search looks (it looks two levels down): the rule on every COMPONENT of the given
#   and of the real path is then the only thing that refuses (round 3: the root check had been answering for it)
mkdir -p "$T/vol/CODING/plain/deep/Datasec-old/proj"; echo d > "$T/vol/CODING/plain/deep/Datasec-old/proj/d.txt"; ln -s "$T/vol/CODING/plain/deep/Datasec-old" "$T/vol/CODING/deepalias"
write_conf "" refuse "set=General|Deep|$T/vol/CODING/plain/deep/Datasec-old/proj"
to f1.txt nb --run --now "$(at 2 1 0)"
is  "T14 a source inside a datasec-named folder four levels down, where no forbidden root is searched for: exit 2" 2 "$RC"
has "T14 ... refused by the name of a component" "$(OUTF f1.txt)" "has the component 'Datasec-old', which contains 'datasec'"
write_conf "" refuse "set=General|Deep|$T/vol/CODING/deepalias/proj"
to f2.txt nb --run --now "$(at 2 1 0)"
is  "T14 the same folder through a symlinked parent with an innocent name: exit 2" 2 "$RC"
has "T14 ... refused by its REAL path's name" "$(OUTF f2.txt)" "(real path $T/vol/CODING/plain/deep/Datasec-old/proj) has the component 'Datasec-old'"
#   the other seats are not runnable from this lane at all
mkdir -p "$T/vol/TUESDAY" "$T/vol/FRIDAY"
env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/TUESDAY" "$LANE/nas_backup.sh" --dry > "$T/out/tu.txt" 2>&1; RC=$?
is  "T14 a TUESDAY tree: exit 2 even for a dry run" 2 "$RC"
has "T14 ... no confirmed scope" "$(OUTF tu.txt)" "has no confirmed scope in this lane"
env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/FRIDAY" "$LANE/nas_backup.sh" --dry > "$T/out/fr.txt" 2>&1; RC=$?
is  "T14 a FRIDAY tree: exit 2" 2 "$RC"
#   a state file that belongs to another seat is refused
fixture cli3; mkdir -p "$T/lane/state"; echo '{"seat": "tuesday", "schema": 2}' > "$T/lane/state/wednesday.json"
to s.txt nb --run --now "$(at 0 1 0)"
no  "T14 a state file that says it is another seat's: the run is NOT exit 0" test "$RC" -eq 0
has "T14 ... says whose it is" "$(OUTF s.txt)" "belongs to seat 'tuesday'"
#   the test-mode fence
env -u WED_AGENT NB_TEST_ROOT="$HOME" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup.sh" --dry > "$T/out/fence.txt" 2>&1; RC=$?
has "T14 test mode outside /private/tmp is refused BY THE FENCE" "$(OUTF fence.txt)" "must be an existing directory under /private/tmp"

echo; echo "T15 THE CONFIGURATION FAILS CLOSED (QA finding 4)"
fixture cf; W="$T/vol/WEDNESDAY"; mkdir -p "$W/bulk/deep" "$W/_q" "$W/keepme" "$W/cachedir" "$T/vol/CODING/Secuura/Blockchain/onlyhere"
echo "$MARK bulk" > "$W/bulk/deep/big.bin"; echo "$MARK byname" > "$W/cachedir/c.bin"; echo "$MARK setname" > "$T/vol/CODING/Secuura/Blockchain/onlyhere/s.bin"; echo keep > "$W/keepme/k.txt"
mkdir -p "$W/onlyhere"; echo "wed" > "$W/onlyhere/w.txt"
write_conf "" refuse "exclude_path=WEDNESDAY|bulk" "exclude_name=cachedir" "exclude_name_in=Secuura|onlyhere"
to ok.txt nb --run --now "$(at 0 1 0)"
is  "T15 intact conf: exit 0" 0 "$RC"
is  "T15 exclude_path, exclude_name and exclude_name_in each keep their folder out (3 marked files)" 0 "$(on_nas "$MARK")"
yes "T15 NEIGHBOUR an ordinary folder arrives" test -f "$(CUR)/keepme/k.txt"
yes "T15 exclude_name_in applies to ITS set only: the same folder name in the other set arrives" test -f "$(CUR)/onlyhere/w.txt"
C="$T/lane/seats/wednesday.conf"
#   truncated: the END marker is gone
cp "$C" "$T/conf.good"; /usr/bin/grep -v -E '^END ' "$T/conf.good" > "$C"
to t1.txt nb --run --now "$(at 1 1 0)"
is  "T15 a conf that lost its END marker (truncated): exit 2" 2 "$RC"
has "T15 ... says so" "$(OUTF t1.txt)" "does not end with its"
#   every exclude line lost, END marker still there
/usr/bin/grep -v -E '^exclude' "$T/conf.good" > "$C"
to t2.txt nb --run --now "$(at 1 1 0)"
is  "T15 a conf that lost its exclude lines but kept the marker: exit 2" 2 "$RC"
has "T15 ... both numbers are printed" "$(OUTF t2.txt)" "declares 16 lines and holds 13"
#   a one-letter typo in an exclude_path
sed -e 's/^exclude_path=WEDNESDAY|bulk$/exclude_path=WEDNESDAY|bulc/' "$T/conf.good" > "$C"
to t3.txt nb --run --now "$(at 1 1 0)"
is  "T15 an exclude_path that names nothing: exit 2" 2 "$RC"
has "T15 ... refused BY NAME" "$(OUTF t3.txt)" "exclude_path=WEDNESDAY|bulc names nothing"
#   exclude_name=*
sed -e 's/^exclude_name=cachedir$/exclude_name=*/' "$T/conf.good" > "$C"
to t4.txt nb --run --now "$(at 1 1 0)"
is  "T15 exclude_name=*: exit 2" 2 "$RC"
has "T15 ... says it would empty the backup" "$(OUTF t4.txt)" "matches every name"
is  "T15 none of the four damaged confs copied anything: the marked files are still not on the NAS" 0 "$(on_nas "$MARK")"
cp "$T/conf.good" "$C"
to t5.txt nb --run --now "$(at 1 1 0)"
is  "T15 NEIGHBOUR the intact conf again: exit 0" 0 "$RC"
#   an emptied source, and a sharp fall
fixture shrink; W="$T/vol/WEDNESDAY"; for i in 1 2 3 4 5 6 7 8 9 10 11 12; do echo "$i" > "$W/sub/n$i.txt"; done
to g.txt nb --run --now "$(at 0 1 0)"
is  "T15 first night GOOD with 17 files" "0/17" "$RC/$(state last_good.set_counts.WEDNESDAY)"
mkdir -p "$T/held2"; for i in 1 2 3 4 5 6 7 8 9 10 11 12; do mv -n "$W/sub/n$i.txt" "$T/held2/"; done; mv -n "$W/a.txt" "$W/same.txt" "$T/held2/"
to s1.txt nb --run --now "$(at 1 1 0)"
no  "T15 a set that lost more than half its files overnight (17 -> 3): the run is NOT exit 0" test "$RC" -eq 0
has "T15 ... with the two numbers" "$(OUTF s1.txt)" "SCOPE FELL SHARPLY: 3 files in scope now, 17 at the last good run"
is  "T15 ... and the last good run is still night 1" "$(at 0 1 0).0" "$(state last_good.time)"
to s2.txt nb --run --now "$(at 1 2 0)" --accept-shrink "card-accept-shrink-1"
is  "T15 NEIGHBOUR the same state, accepted once on a card: exit 0" 0 "$RC"
mv -n "$T/vol/CODING/Secuura/Blockchain" "$T/held2/Blockchain"
to s3.txt nb --run --now "$(at 2 1 0)"
no  "T15 a set that became EMPTY: the run is NOT exit 0" test "$RC" -eq 0
has "T15 ... says EMPTY SCOPE" "$(OUTF s3.txt)" "EMPTY SCOPE"
hasnt "T15 ... and never GOOD" "$(OUTF s3.txt)" "GOOD: every in-scope"
#   an unreadable source folder, and an engine that is not rsync 3
fixture unread; mkdir -p "$T/vol/WEDNESDAY/locked"; echo x > "$T/vol/WEDNESDAY/locked/x.txt"; chmod 000 "$T/vol/WEDNESDAY/locked"
to u.txt nb --run --now "$(at 0 1 0)"
chmod 755 "$T/vol/WEDNESDAY/locked"
no  "T15 a source folder that cannot be read: the run is NOT exit 0" test "$RC" -eq 0
has "T15 ... says the source could not be fully read" "$(OUTF u.txt)" "source could not be fully read"
fixture oldrsync; f="$T/stub/rsync_old"; printf '#!/bin/bash\necho "rsync  version 2.6.9  protocol version 29"\n' > "$f"; chmod +x "$f"; write_conf "$f"
to v.txt nb --run --now "$(at 0 1 0)"
is  "T15 an engine that is not rsync 3: exit 2" 2 "$RC"
has "T15 ... says so" "$(OUTF v.txt)" "is not rsync 3"

echo; echo "T16 A DAMAGED STATE FILE (QA finding 9) stops neither the flag nor the backup"
fixture dmg
to g.txt nb --run --now "$(at 0 1 0)"
echo '{"seat": "wednesday", "last_go' > "$T/lane/state/wednesday.json"
to w.txt watch --check --now "$(at 0 9 0)"
is  "T16 the watch on a truncated state file: exit 5 (a damage notice, flag-worthy), not a crash" 5 "$RC"
has "T16 one plain line naming the file" "$(OUTF w.txt)" "STATE FILE DAMAGED: $T/lane/state/wednesday.json"
hasnt "T16 no Python traceback" "$(OUTF w.txt)" "Traceback"
yes "T16 the damaged file was MOVED into the lane's quarantine, not deleted" test -n "$(find "$T/lane/state" -path '*_quarantine_*' -name 'wednesday.json.damaged.*' 2>&1)"
to w2.txt watch --check --now "$(at 0 9 1)"
is  "T16 the next check STILL says so (exit 5): printing the notice does not use it up" 5 "$RC"
to wack.txt watch --ack-damage --now "$(at 0 9 2)"
to w3.txt watch --check --now "$(at 0 9 3)"
is  "T16 after a seat acknowledged it the check runs on a clean state (exit 0)" 0 "$RC"
to n.txt nightly --now "$(at 1 0 31)"
is  "T16 the next night's run starts clean and is GOOD" 0 "$RC"
echo 'garbage' > "$T/lane/state/wednesday.json"
to n2.txt nightly --now "$(at 2 0 31)"
has "T16 the nightly job on a garbage state file SAYS it started clean" "$(OUTF n2.txt)" "STATE FILE DAMAGED"
yes "T16 ... and wrote that to its own log" /usr/bin/grep -q -F 'STATE FILE DAMAGED' "$T/lane/logs/wednesday/nightly.log"
hasnt "T16 ... no traceback there either" "$(OUTF n2.txt)" "Traceback"
: > "$T/lane/state/wednesday.json"
to d.txt doctor_block "$(at 2 9 0)"
has "T16 doctor on an EMPTY state file: a hard-failure line in its own words, not a traceback" "$(OUTF d.txt)" "✗ NAS BACKUP STATE WAS FOUND DAMAGED"
hasnt "T16 ... no traceback" "$(OUTF d.txt)" "Traceback"

echo; echo "T17 A TYPE CHANGE (QA finding 7): the old entry is kept in versions/, the new one is copied, the run is GOOD"
fixture typ; W="$T/vol/WEDNESDAY"; mkdir -p "$W/thing"; echo "inside the folder" > "$W/thing/in.txt"; echo "i am a file" > "$W/shape"
to g.txt nb --run --now "$(at 0 1 0)"
mkdir -p "$T/held"; mv -n "$W/thing" "$T/held/thing"; echo "thing is now a FILE" > "$W/thing"
mv -n "$W/shape" "$T/held/shape"; mkdir -p "$W/shape"; echo "shape is now a FOLDER" > "$W/shape/new.txt"
to c.txt nb --run --now "$(at 1 1 0)"
is  "T17 folder -> file and file -> folder in one night: exit 0" 0 "$RC"
yes "T17 the new FILE is at the destination" /usr/bin/grep -q -F 'thing is now a FILE' "$(CUR)/thing"
yes "T17 the new FOLDER is at the destination" /usr/bin/grep -q -F 'shape is now a FOLDER' "$(CUR)/shape/new.txt"
yes "T17 the old folder's content is kept under versions/" test -n "$(/usr/bin/grep -r -l -F 'inside the folder' "$(VER)" 2>&1)"
yes "T17 the old file's content is kept under versions/" test -n "$(/usr/bin/grep -r -l -F 'i am a file' "$(VER)" 2>&1)"
has "T17 the run says what it did" "$(OUTF c.txt)" "TYPE CHANGE: thing"
to c2.txt nb --run --now "$(at 2 1 0)"
is  "T17 the night after is GOOD too (round 1 failed forever here)" 0 "$RC"

echo; echo "T18 THE LOCK MEANS ONE WRITER (QA finding 8 and minors)"
fixture grp
S="$(mk_stub rsync_slow_then_real 'sleep 6; exec "$REAL" "$@"')"; write_conf "$S"
nb --run --now "$(at 0 1 0)" > "$T/out/bg.txt" 2>&1 & BG=$!
sleep 3
yes "T18 the lock records the engine's own process group" test "$(state_owner engine_pgid)" != "None"
TOOLPID="$(state_owner pid)"          # the tool itself (python), not the shell that launched it
kill -KILL "$TOOLPID" 2>&1; wait "$BG" 2>&1
no  "T18 control: the tool process is gone" kill -0 "$TOOLPID"
to k1.txt nb --clear-stale-lock
is  "T18 the tool was killed outright but its engine is still running: --clear-stale-lock REFUSES (exit 6)" 6 "$RC"
has "T18 ... and says the engine is still running" "$(OUTF k1.txt)" "STILL RUNNING"
write_conf
to k2.txt nb --run --now "$(at 0 1 1)"
is  "T18 a second run beside the orphan engine is refused (exit 6)" 6 "$RC"
has "T18 ... for the same reason" "$(OUTF k2.txt)" "copy engine is STILL RUNNING"
sleep 7
to k3.txt nb --clear-stale-lock
is  "T18 NEIGHBOUR once the engine has ended, the stale lock can be moved aside (exit 0)" 0 "$RC"
to k4.txt nb --run --now "$(at 0 1 2)"
is  "T18 ... and the next run is GOOD" 0 "$RC"
#   the loser of a simultaneous start is not told STALE about a live run
fixture race; mkdir -p "$T/lane/state/wednesday.lock.d"
to r.txt nb --run --now "$(at 0 1 0)"
is  "T18 a lock taken this very moment (no owner record yet): exit 6" 6 "$RC"
has "T18 ... it is 'another run holds the lock'" "$(OUTF r.txt)" "another run holds the lock"
hasnt "T18 ... not STALE" "$(OUTF r.txt)" "STALE lock"
#   a reused pid is not the holder
bash -c 'exec -a nas_backup_lookalike sleep 60' & HOLDER=$!
sleep 1
printf '{"pid": %s, "pid_started": "Thu Jan  1 00:00:00 1970", "started_local": "long ago"}\n' "$HOLDER" > "$T/lane/state/wednesday.lock.d/owner.json"
touch -t 202601010000 "$T/lane/state/wednesday.lock.d"
to r2.txt nb --run --now "$(at 0 1 0)"
has "T18 a live process that merely has the holder's pid (started at another time) does not hold the lock: STALE" "$(OUTF r2.txt)" "STALE lock"
kill "$HOLDER" 2>&1; wait "$HOLDER" 2>&1

echo; echo "T19 DAYLIGHT SAVING: the window is local wall time on both change days (Australia/Sydney)"
TZ=Australia/Sydney "$PY" -c 'import sys, time, datetime
sys.path.insert(0, sys.argv[1]); import nb_core
def ep(y, mo, d, h, mi): return time.mktime((y, mo, d, h, mi, 0, 0, 0, -1))
def w(y, mo, d, h, mi, fh=2, fm=30, hrs=3):
    o, c, inw = nb_core.window_for(ep(y, mo, d, h, mi), fh, fm, hrs)
    return "%s-%s %s" % (o.strftime("%H:%M"), c.strftime("%H:%M"), inw)
print("spring 03:20 ->", w(2026, 10, 4, 3, 20))     # clocks go 02:00 -> 03:00 on 2026-10-04
print("spring 05:20 ->", w(2026, 10, 4, 5, 20))
print("spring 05:40 ->", w(2026, 10, 4, 5, 40))
print("autumn 02:40 ->", w(2027, 4, 4, 2, 40))      # clocks go 03:00 -> 02:00 on 2027-04-04
print("autumn 05:40 ->", w(2027, 4, 4, 5, 40))
print("plain  01:00 ->", w(2026, 12, 1, 1, 0, 0, 30, 5))
print("plain  05:30 ->", w(2026, 12, 1, 5, 30, 0, 30, 5))' "$LANE" > "$T/out/dst.txt" 2>&1; RC=$?
is  "T19 the arithmetic ran" 0 "$RC"
has "T19 spring-forward night, 03:20 on the wall: inside a 02:30-05:30 window" "$(OUTF dst.txt)" "spring 03:20 -> 02:30-05:30 True"
has "T19 spring-forward night, 05:20: still inside" "$(OUTF dst.txt)" "spring 05:20 -> 02:30-05:30 True"
has "T19 spring-forward night, 05:40: outside (it closes at the 05:30 shift change, not an hour later)" "$(OUTF dst.txt)" "spring 05:40 -> 02:30-05:30 False"
has "T19 fall-back night, 02:40: inside" "$(OUTF dst.txt)" "autumn 02:40 -> 02:30-05:30 True"
has "T19 fall-back night, 05:40: outside" "$(OUTF dst.txt)" "autumn 05:40 -> 02:30-05:30 False"
has "T19 an ordinary night, 05:30 exactly: the window has closed" "$(OUTF dst.txt)" "plain  05:30 -> 00:30-05:30 False"

echo; echo "T20 THE INSTALL CANNOT WALK PAST A HOLD (QA finding 11), and a dry run only LISTS the destination (note 13)"
fixture inst
sed -e "s|@PROJECT_DIR@|/some/tree|g" -e "s|@SEAT@|wednesday|g" -e "s|@HOME@|/Users/x|g" -e "s|@NASHOUR@|3|g" -e "s|@NASMIN@|30|g" "$LANE/jobs/nasbackup.plist.template" > "$T/out/rendered.plist"
yes "T20 the template rendered by the UNEDITED installer's own five substitutions is a valid plist" /usr/bin/plutil -lint "$T/out/rendered.plist"
is  "T20 ... with no placeholder left in it" 0 "$(/usr/bin/grep -c -E '@[A-Z0-9_]+@' "$T/out/rendered.plist")"
is  "T20 ... and 24 fires, one an hour" 24 "$(/usr/bin/grep -c -F '<key>Minute</key><integer>30</integer>' "$T/out/rendered.plist")"
echo "held" > "$T/lane/HOLD_wednesday"
to h.txt nightly --now "$(at 0 0 31)"
is  "T20 the script launchd calls, under the hold, inside the window: exit 3" 3 "$RC"
has "T20 ... says HELD" "$(OUTF h.txt)" "HELD:"
is  "T20 ... nothing started on the NAS" 0 "$(started)"
yes "T20 ... and the refusal is in the nightly log, where a morning seat reads it" /usr/bin/grep -q -F 'HELD' "$T/lane/logs/wednesday/nightly.log"
mv -n "$T/lane/HOLD_wednesday" "$T/lane/HOLD_wednesday.lifted"
to h2.txt nightly --now "$(at 0 1 30)"
is  "T20 NEIGHBOUR hold moved aside: the next fire runs (exit 0)" 0 "$RC"
#   dry run against an EXISTING destination: it lists it, says so, and changes nothing there
echo "changed since" > "$T/vol/WEDNESDAY/a.txt"
snapnas() { find "$T/nas" -exec stat -f '%N %z %m %i' {} + 2>&1 | sort | shasum -a 256 | cut -c1-64; }
B4="$(snapnas)"
to dry.txt nb --dry
is  "T20 dry run exits 0" 0 "$RC"
has "T20 the dry run says what it LISTED on the NAS" "$(OUTF dry.txt)" "listed on the NAS (read-only): $(CUR): 5 files"
has "T20 ... measures 'to copy' against it" "$(OUTF dry.txt)" "to copy: 1 files"
is  "T20 ... and the NAS is byte-for-byte as it was (names, sizes, times, inodes)" "$B4" "$(snapnas)"
is  "T20 the engine was never handed a NAS path in the dry run (lines naming the NAS in its check)" 0 "$(/usr/bin/grep -F 'engine check of the list' "$(OUTF dry.txt)" | /usr/bin/grep -c -F "$T/nas")"
echo "x" > "$T/nas/General/extra.txt"
no  "T20 CAN-FAIL: the same snapshot DOES change when a file is added to the NAS" test "$B4" = "$(snapnas)"

# ═════════════════════════════ ROUND 3: one rule, "unproven means failed" (ANSWER-4; the second check's attacks, lifted) ═════════════════════════════
idxrows() { "$PY" -c 'import sqlite3,sys
try:
    print(sqlite3.connect(sys.argv[1]).execute("select count(*) from files").fetchone()[0])
except Exception as e: print("ERR", e)' "$T/lane/state/wednesday.index.sqlite" 2>&1; }
nbx() { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$@"; }
# stub prologue: N = how many times this engine was called; V = the seat tree; SET1 = this call is for the seat tree's set
PRE='[ -f "$STUBDIR/calls" ] && N=$(cat "$STUBDIR/calls") || N=0; N=$((N+1)); echo $N > "$STUBDIR/calls"; DEST="${@: -1}"; V="$STUBDIR/../vol/WEDNESDAY"; mkdir -p "$STUBDIR/taken"; SET1=no; case "$DEST" in */current/WEDNESDAY/) SET1=yes;; esac; '
wait_calls() { # n : wait (at most 30 s) until the stub engine has been called n times
  local i=0; while [ "$i" -lt 150 ]; do [ -f "$T/stub/calls" ] && [ "$(cat "$T/stub/calls")" -ge "$1" ] && return 0; sleep 0.2; i=$((i+1)); done; return 1; }

echo; echo "T21 UNREADABLE IS NOT GONE (finding 1): a planned file that cannot be READ is NOT DELIVERED; only a file provably DELETED is let go, counted and named"
#  a. a source file that cannot be read, from the first night on
fixture one_a; printf 'PRIVATE-LEDGER-MARK-1a\n' > "$T/vol/WEDNESDAY/ledger.db"; chmod 000 "$T/vol/WEDNESDAY/ledger.db"
to r0.txt nb --run --now "$(at 0 1 0)"; RC0=$RC
to r1.txt nb --run --now "$(at 1 1 0)"
chmod 644 "$T/vol/WEDNESDAY/ledger.db"
no    "T21a a source file with mode 000 from the first night: night 1 is NOT exit 0" test "$RC0" -eq 0
no    "T21a ... nor is night 2" test "$RC" -eq 0
hasnt "T21a it never says GOOD (night 1)" "$(OUTF r0.txt)" "GOOD: every in-scope"
hasnt "T21a it never says GOOD (night 2)" "$(OUTF r1.txt)" "GOOD: every in-scope"
has   "T21a the file is NAMED as not delivered, with the reason" "$(OUTF r0.txt)" "NOT DELIVERED: WEDNESDAY/ledger.db (the source could not be read"
is    "T21a state: no good backup on record" None "$(state last_good)"
is    "T21a the file's content is not on the NAS" 0 "$(on_nas 'PRIVATE-LEDGER-MARK-1a')"
to r2.txt nb --run --now "$(at 2 1 0)"
is    "T21a NEIGHBOUR the same file readable: GOOD" 0 "$RC"
is    "T21a ... and it arrived" 1 "$(on_nas 'PRIVATE-LEDGER-MARK-1a')"
#  b. a backed-up file that changes and then cannot be read
fixture one_b; printf 'LEDGER-v1\n' > "$T/vol/WEDNESDAY/ledger.db"
to r0.txt nb --run --now "$(at 0 1 0)"
sleep 1; printf 'LEDGER-v2-newer-content\n' > "$T/vol/WEDNESDAY/ledger.db"; chmod 000 "$T/vol/WEDNESDAY/ledger.db"
to r1.txt nb --run --now "$(at 1 1 0)"; RC1=$RC
to r2.txt nb --run --now "$(at 2 1 0)"
chmod 644 "$T/vol/WEDNESDAY/ledger.db"
no    "T21b a backed-up file that changed and became unreadable: the next night is NOT exit 0" test "$RC1" -eq 0
no    "T21b ... and the night after is NOT exit 0 either (it does not age into GOOD)" test "$RC" -eq 0
yes   "T21b control: the destination still holds LAST night's content" /usr/bin/grep -q -x -F 'LEDGER-v1' "$(CUR)/ledger.db"
is    "T21b the last good run is still night 0" "$(at 0 1 0).0" "$(state last_good.time)"
to r3.txt nb --run --now "$(at 3 1 0)"
is    "T21b NEIGHBOUR readable again: GOOD" 0 "$RC"
yes   "T21b ... with the new content" /usr/bin/grep -q -x -F 'LEDGER-v2-newer-content' "$(CUR)/ledger.db"
#  c. a source FOLDER that becomes unreadable between the listing and the copy
fixture one_c; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do echo "payload-1c $i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
S="$(mk_stub rsync_chmod "$PRE"'[ "$SET1" = yes ] && chmod 000 "$V/sub"; exec "$REAL" "$@"')"; write_conf "$S"
to r0.txt nb --run --now "$(at 0 1 0)"; chmod 755 "$T/vol/WEDNESDAY/sub"
[ -d "$(CUR)/sub" ] && chmod 755 "$(CUR)/sub"      # the engine gave the new folder the source folder's mode; a share has no such modes
no    "T21c a folder of 31 files unreadable between the listing and the copy: the run is NOT exit 0" test "$RC" -eq 0
hasnt "T21c ... it does not say GOOD" "$(OUTF r0.txt)" "GOOD: every in-scope"
has   "T21c ... its files are named as not delivered" "$(OUTF r0.txt)" "NOT DELIVERED: WEDNESDAY/sub/"
hasnt "T21c ... none of them is counted as deleted" "$(OUTF r0.txt)" "DELETED at the source during the run"
is    "T21c state: not good" None "$(state last_good)"
is    "T21c no COMPLETE marker in the seat's client folder" 0 "$(find "$T/nas/General" -name 'RUN_*_COMPLETE.txt' 2>&1 | wc -l | tr -d ' ')"
#  d. the coordinator's question (ANSWER-3): EVERY folder under the root unreadable mid-run
fixture one_d; mkdir -p "$T/vol/WEDNESDAY/a" "$T/vol/WEDNESDAY/b"; for i in 1 2 3 4 5 6 7 8 9 10; do echo "payload-A $i" > "$T/vol/WEDNESDAY/a/f$i.txt"; echo "payload-B $i" > "$T/vol/WEDNESDAY/b/g$i.txt"; done
to r0.txt nb --run --now "$(at 0 1 0)"
sleep 1; for f in "$T/vol/WEDNESDAY"/a/*.txt "$T/vol/WEDNESDAY"/b/*.txt; do echo "changed overnight" >> "$f"; done
S="$(mk_stub rsync_all000 "$PRE"'[ "$SET1" = yes ] && chmod 000 "$V/a" "$V/b"; exec "$REAL" "$@"')"; write_conf "$S"
to r1.txt nb --run --now "$(at 1 1 0)"; chmod 755 "$T/vol/WEDNESDAY/a" "$T/vol/WEDNESDAY/b"
no    "T21d every changed file's folder unreadable mid-run: the run is NOT exit 0" test "$RC" -eq 0
hasnt "T21d ... not GOOD" "$(OUTF r1.txt)" "GOOD: every in-scope"
is    "T21d control: all 20 destination copies still hold last night's content" 20 "$(/usr/bin/grep -r -L -F 'changed overnight' "$(CUR)/a" "$(CUR)/b" | wc -l | tr -d ' ')"
has   "T21d ... and the run says 20 are not proven" "$(OUTF r1.txt)" "NOT PROVEN: 20"
write_conf
to r2.txt nb --run --now "$(at 2 1 0)"
is    "T21d NEIGHBOUR the folders readable again: GOOD, and nothing is stale" "0/0" "$RC/$(/usr/bin/grep -r -L -F 'changed overnight' "$(CUR)/a" "$(CUR)/b" | wc -l | tr -d ' ')"
#  e. the whole source folder of a set goes away mid-run
fixture one_e
S="$(mk_stub rsync_rootgone "$PRE"'[ "$SET1" = yes ] && mv -n "$V" "$V.gone"; "$REAL" "$@"; exit $?')"; write_conf "$S"
to r0.txt nb --run --now "$(at 0 1 0)"; mv -n "$T/vol/WEDNESDAY.gone" "$T/vol/WEDNESDAY"
no    "T21e the set's root folder moved away mid-run: the run is NOT exit 0" test "$RC" -eq 0
hasnt "T21e ... not GOOD, and nothing counted as deleted" "$(OUTF r0.txt)" "DELETED at the source during the run"
is    "T21e state: not good" None "$(state last_good)"
#  f. a file that really IS deleted between the plan and the proof: let go, COUNTED and NAMED
fixture one_f
S="$(mk_stub rsync_del1 "$PRE"'[ "$SET1" = yes ] && [ -f "$V/sub/b.txt" ] && mv -n "$V/sub/b.txt" "$STUBDIR/taken/"; "$REAL" "$@"; exit $?')"; write_conf "$S"
to r0.txt nb --run --now "$(at 0 1 0)"
is    "T21f one planned file deleted from the source during the run (its folder is listable, the name is absent): GOOD" 0 "$RC"
has   "T21f ... it is COUNTED" "$(OUTF r0.txt)" "DELETED at the source during the run: 1 planned file(s)"
has   "T21f ... and NAMED" "$(OUTF r0.txt)" "First: sub/b.txt"
has   "T21f ... and named again, by its full path, in the run's last lines" "$(OUTF r0.txt)" "DELETED AT SOURCE: WEDNESDAY/sub/b.txt"
has   "T21f ... the GOOD line says so too" "$(OUTF r0.txt)" "DELETED at the source during the run, confirmed absent twice"
is    "T21f state: the good run records 1 deleted file" 1 "$(state last_good.counts.deleted)"
no    "T21f the deleted file is not at the destination" test -e "$(CUR)/sub/b.txt"
#  g. more deletions than the stated limit (5 files, or 0.1% of the plan if that is more) fail the night
fixture one_g; for i in 1 2 3 4 5 6 7 8; do echo "tmp $i" > "$T/vol/WEDNESDAY/sub/t$i.txt"; done
S="$(mk_stub rsync_del6 "$PRE"'if [ "$SET1" = yes ]; then for i in 1 2 3 4 5 6; do [ -f "$V/sub/t$i.txt" ] && mv -n "$V/sub/t$i.txt" "$STUBDIR/taken/"; done; fi; "$REAL" "$@"; exit $?')"; write_conf "$S"
to r0.txt nb --run --now "$(at 0 1 0)"
no    "T21g six planned files deleted during the run, above the 5 allowed: the run is NOT exit 0" test "$RC" -eq 0
has   "T21g ... with the numbers" "$(OUTF r0.txt)" "6 planned files were deleted from the source during the run, above the 5 allowed"
fixture one_g2; for i in 1 2 3 4 5 6 7 8; do echo "tmp $i" > "$T/vol/WEDNESDAY/sub/t$i.txt"; done
S="$(mk_stub rsync_del5 "$PRE"'if [ "$SET1" = yes ]; then for i in 1 2 3 4 5; do [ -f "$V/sub/t$i.txt" ] && mv -n "$V/sub/t$i.txt" "$STUBDIR/taken/"; done; fi; "$REAL" "$@"; exit $?')"; write_conf "$S"
to r0.txt nb --run --now "$(at 0 1 0)"
is    "T21g NEIGHBOUR five deleted, at the limit: GOOD, counted" "0/5" "$RC/$(state last_good.counts.deleted)"
#  h. the file's PARENT folder is gone: the parent cannot be listed, so this is NOT a proven deletion (the strict reading)
fixture one_h
S="$(mk_stub rsync_parentgone "$PRE"'[ "$SET1" = yes ] && [ -d "$V/sub" ] && mv -n "$V/sub" "$STUBDIR/taken/sub"; "$REAL" "$@"; exit $?')"; write_conf "$S"
to r0.txt nb --run --now "$(at 0 1 0)"
no    "T21h a planned file whose parent folder went away: NOT exit 0 (a folder that cannot be listed proves nothing)" test "$RC" -eq 0
has   "T21h ... named" "$(OUTF r0.txt)" "NOT DELIVERED: WEDNESDAY/sub/b.txt"
#  i. a source file replaced by a FOLDER between the copy and the proof
fixture one_i
S="$(mk_stub rsync_f2d "$PRE"'"$REAL" "$@"; rc=$?; f="$V/a.txt"; if [ -f "$f" ]; then mv -n "$f" "$STUBDIR/taken/a.aside"; mkdir "$f"; echo inner > "$f/inner.txt"; fi; exit $rc')"; write_conf "$S"
to r0.txt nb --run --now "$(at 0 1 0)"
no    "T21i a planned file that became a folder before its proof: NOT exit 0" test "$RC" -eq 0
has   "T21i ... named, with the reason" "$(OUTF r0.txt)" "NOT DELIVERED: WEDNESDAY/a.txt (the source is no longer a regular file)"
#  j. the DESTINATION copy cannot be read back (the checker's mutant K19)
fixture one_j
S="$(mk_stub rsync_dst000 "$PRE"'"$REAL" "$@"; rc=$?; f="$STUBDIR/../nas/General/Wednesday/nightly-backup/current/WEDNESDAY/a.txt"; [ -f "$f" ] && chmod 000 "$f"; exit $rc')"; write_conf "$S"
to r0.txt nb --run --now "$(at 0 1 0)"; chmod 644 "$(CUR)/a.txt"
no    "T21j a destination copy that cannot be read back is NOT proven: NOT exit 0" test "$RC" -eq 0
has   "T21j ... named, with the reason" "$(OUTF r0.txt)" "NOT DELIVERED: WEDNESDAY/a.txt (the destination copy is absent or could not be read"
write_conf
to r1.txt nb --run --now "$(at 1 1 0)"
is    "T21j NEIGHBOUR readable: GOOD" 0 "$RC"
#  k. a file that WAS delivered and becomes unreadable before its proof
fixture one_k
S="$(mk_stub rsync_post000 "$PRE"'"$REAL" "$@"; rc=$?; [ "$SET1" = yes ] && chmod 000 "$V/a.txt"; exit $rc')"; write_conf "$S"
to r0.txt nb --run --now "$(at 0 1 0)"; chmod 644 "$T/vol/WEDNESDAY/a.txt"
no    "T21k delivered, then unreadable before the proof: NOT exit 0 (delivered is not proven)" test "$RC" -eq 0
#  l. the deletion proof itself, as a function
mkdir -p "$T/u/root/dir" "$T/u/other/dir" "$T/u/root/locked"; echo x > "$T/u/root/dir/here.txt"; chmod 000 "$T/u/root/locked"
"$PY" -c 'import os, sys
sys.path.insert(0, sys.argv[1]); import nb_core
U = sys.argv[2]; r = os.stat(U + "/root"); rid = (r.st_dev, r.st_ino); o = os.stat(U + "/other"); oid = (o.st_dev, o.st_ino)
print("absent-in-listable-parent=%s" % nb_core.source_deleted(U + "/root", rid, "dir/gone.txt"))
print("present=%s" % nb_core.source_deleted(U + "/root", rid, "dir/here.txt"))
print("parent-unlistable=%s" % nb_core.source_deleted(U + "/root", rid, "locked/x.txt"))
print("parent-missing=%s" % nb_core.source_deleted(U + "/root", rid, "nodir/x.txt"))
print("root-is-another-folder=%s" % nb_core.source_deleted(U + "/root", oid, "dir/gone.txt"))
print("allowed-small=%d allowed-large=%d" % (nb_core.deleted_allowed({"max_deleted_files": 5, "max_deleted_fraction": 0.001}, 12), nb_core.deleted_allowed({"max_deleted_files": 5, "max_deleted_fraction": 0.001}, 587130)))' "$LANE" "$T/u" > "$T/out/unit.txt" 2>&1; RC=$?
chmod 755 "$T/u/root/locked"
is    "T21l the deletion proof ran" 0 "$RC"
has   "T21l deleted = the name is absent from a parent that could be listed" "$(OUTF unit.txt)" "absent-in-listable-parent=True"
has   "T21l a name that is still there is not deleted" "$(OUTF unit.txt)" "present=False"
has   "T21l a parent that cannot be listed proves nothing" "$(OUTF unit.txt)" "parent-unlistable=False"
has   "T21l a parent that is itself gone proves nothing" "$(OUTF unit.txt)" "parent-missing=False"
has   "T21l a root that is no longer the folder that was listed proves nothing" "$(OUTF unit.txt)" "root-is-another-folder=False"
has   "T21l the limit: 5 files for a small plan, 0.1% for a large one" "$(OUTF unit.txt)" "allowed-small=5 allowed-large=587"

echo; echo "T22 AN EMPTY PLAN IS NEVER GOOD (finding 4), on a first run too"
fixture empty1; mkdir -p "$T/vol/CODING/Emptyish/d1/d2" "$T/held"
write_conf "" refuse "set=General|Emptyish|$T/vol/CODING/Emptyish"
to r0.txt nb --run --now "$(at 0 1 0)"
is    "T22 FIRST run of a set holding folders and ZERO files: exit 8, not good" 8 "$RC"
has   "T22 ... says EMPTY SCOPE" "$(OUTF r0.txt)" "EMPTY SCOPE: 0 files in the plan"
hasnt "T22 ... never GOOD" "$(OUTF r0.txt)" "GOOD: every in-scope"
is    "T22 state: no good backup" None "$(state last_good)"
has   "T22 a first run says it has NO BASELINE to compare a set with" "$(OUTF r0.txt)" "NO BASELINE"
echo x > "$T/vol/CODING/Emptyish/d1/x.txt"
to r1.txt nb --run --now "$(at 1 1 0)"
is    "T22 NEIGHBOUR one file in it: GOOD" 0 "$RC"
mv -n "$T/vol/CODING/Emptyish/d1/x.txt" "$T/held/"
write_conf "" refuse "set=General|Emptyish|$T/vol/CODING/Emptyish" "allow_empty=Emptyish"
to r2.txt nb --run --now "$(at 2 1 0)"
is    "T22 the ONE exception: a set the conf names in allow_empty= may hold zero files: GOOD" 0 "$RC"
has   "T22 ... and the run says so" "$(OUTF r2.txt)" "the conf allows it to be empty"
write_conf "" refuse "allow_empty=Nope"
to r3.txt nb --run --now "$(at 3 1 0)"
is    "T22 allow_empty naming a set that is not defined: exit 2" 2 "$RC"
#  exclusions that empty a set are refused before anything runs
for pat in '*.*' '[!~]*' '*[a-z0-9]*' '?*' '**'; do
  fixture "pat_$(printf '%s' "$pat" | od -An -tx1 | tr -d ' \n')"; write_conf "" refuse "exclude_name=$pat"
  to p.txt nb --run --now "$(at 0 1 0)"
  is  "T22 exclude_name=$pat on a first run: exit 2" 2 "$RC"
  has "T22 ... refused as matching every name ($pat)" "$(OUTF p.txt)" "matches every name"
done
write_conf "" refuse "exclude_name=*.log"
to p2.txt nb --run --now "$(at 0 1 0)"
is    "T22 NEIGHBOUR an ordinary pattern (*.log): exit 0" 0 "$RC"
#  a damaged state file the same night as a mistyped exclusion: the baseline survives in the index
fixture basel; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do echo "filler $i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
to r0.txt nb --run --now "$(at 0 1 0)"
write_conf "" refuse "exclude_name=f*"; echo '{"truncated' > "$T/lane/state/wednesday.json"
to r1.txt nb --run --now "$(at 1 1 0)"
no    "T22 state file damaged AND 20 of 25 files newly excluded the same night: NOT exit 0" test "$RC" -eq 0
has   "T22 ... the fall is still seen (the baseline is kept a second time, in the index)" "$(OUTF r1.txt)" "SCOPE FELL SHARPLY: 5 files in scope now, 25 at the last good run"
has   "T22 ... and the damage is said" "$(OUTF r1.txt)" "STATE FILE DAMAGED"
#  the nightly job cannot accept a shrink itself (mutant K10), and a set whose scope is broken is not copied (K03)
fixture k10; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do echo "filler $i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
to n0.txt nightly --now "$(at 0 0 31)"
mkdir -p "$T/held"; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; do mv -n "$T/vol/WEDNESDAY/sub/f$i.txt" "$T/held/"; done
echo "$MARK k03 new file in a set whose scope is broken" > "$T/vol/WEDNESDAY/sub/newfile.txt"
to n1.txt nightly --now "$(at 1 0 31)"
no    "T22 the NIGHTLY job on a set that fell from 25 to 8 files: NOT exit 0 (it can never accept a shrink on its own)" test "$RC" -eq 0
has   "T22 ... SCOPE FELL" "$(OUTF n1.txt)" "SCOPE FELL SHARPLY"
is    "T22 ... the last good run is still night 0" "$(at 0 0 31).0" "$(state last_good.time)"
has   "T22 a set whose scope is broken is NOT COPIED" "$(OUTF n1.txt)" "NOT COPIED: the scope of this set is broken"
is    "T22 ... a new file in it did not travel" 0 "$(on_nas "$MARK k03")"
#  conf shapes: a wildcard in exclude_path (K05), a source that is a file (K23), a key given twice (finding 14)
fixture confshapes; echo plain > "$T/vol/CODING/plainfile"
write_conf "" refuse "exclude_path=WEDNESDAY|su*"
to c1.txt nb --run --now "$(at 0 1 0)"
is    "T22 a wildcard in exclude_path: exit 2" 2 "$RC"
has   "T22 ... refused as not a literal path" "$(OUTF c1.txt)" "must be a literal path inside the set (no wildcards)"
write_conf "" refuse "set=General|AFile|$T/vol/CODING/plainfile"
to c2.txt nb --run --now "$(at 0 1 0)"
is    "T22 a set source that is a FILE: exit 2" 2 "$RC"
has   "T22 ... refused as not a folder" "$(OUTF c2.txt)" "is absent or not a folder"
write_conf; { /usr/bin/grep -v -E '^END ' "$T/lane/seats/wednesday.conf"; echo "status=confirmed"; } > "$T/c.tmp"; mv "$T/c.tmp" "$T/lane/seats/wednesday.conf"; seal_conf
to c3.txt nb --run --now "$(at 0 1 0)"
is    "T22 a key given twice in the conf: exit 2" 2 "$RC"
has   "T22 ... says which key and that it never guesses" "$(OUTF c3.txt)" "gives the key 'status' twice"
"$PY" -c 'import sys
sys.path.insert(0, sys.argv[1]); import nb_core
bad = ["*", "?*", "**", "*.*", "[!~]*", "*[a-z0-9]*", ""]
ok = ["*.log", "wt_*", "*node_modules*", ".[a-z][0-9][0-9]t", "cachedir", "f*", "quarantine"]
print("refused=%d/%d accepted=%d/%d" % (sum(1 for p in bad if nb_core.match_everything(p)), len(bad), sum(1 for p in ok if not nb_core.match_everything(p)), len(ok)))' "$LANE" > "$T/out/pat.txt" 2>&1
has   "T22 the pattern rule as a function: 7 emptying patterns refused, 7 ordinary ones accepted" "$(OUTF pat.txt)" "refused=7/7 accepted=7/7"

echo; echo "T23 A SAMPLE FINDING IS REPAIRED OR THE NIGHT FAILS, AND IT NEVER AGES OUT (finding 5)"
fixture rep1
to r0.txt nb --run --now "$(at 0 1 0)"
printf 'XXX content of a\n' > "$(CUR)/a.txt"; chflags uchg "$(CUR)/a.txt"
to r1.txt nb --run --now "$(at 1 1 0)"; RC1=$RC
no    "T23 a wrong destination copy that CANNOT be replaced (immutable): the night is NOT exit 0" test "$RC1" -eq 0
has   "T23 ... the sample says it withdrew the earlier proof" "$(OUTF r1.txt)" "SAMPLE: 1 of"
has   "T23 ... and the file is named" "$(OUTF r1.txt)" "NOT DELIVERED: WEDNESDAY/a.txt"
CONF_SAMPLE=0; write_conf
to r2.txt nb --run --now "$(at 2 1 0)"; RC2=$RC
to r3.txt nb --run --now "$(at 3 1 0)"
no    "T23 the NEXT night, with the sample switched off so it cannot find the file again: still NOT exit 0" test "$RC2" -eq 0
has   "T23 ... because its index row is gone: it is compared by content and sent again" "$(OUTF r2.txt)" "to copy: 1 files"
no    "T23 ... and the night after that: still NOT exit 0 (a finding never ages out)" test "$RC" -eq 0
chflags nouchg "$(CUR)/a.txt"
to r4.txt nb --run --now "$(at 4 1 0)"
is    "T23 NEIGHBOUR the destination copy replaceable again: GOOD" 0 "$RC"
yes   "T23 ... the destination holds the source's content" cmp -s "$T/vol/WEDNESDAY/a.txt" "$(CUR)/a.txt"
yes   "T23 ... and the wrong content it held is kept under versions/" test -n "$(/usr/bin/grep -r -l -x -F 'XXX content of a' "$(VER)" 2>&1)"
CONF_SAMPLE=10
#  every file altered behind the tool (an index from another destination): all repaired in ONE night
fixture rep30; for i in 1 2 3 4 5 6 7 8 9 10; do printf 'filler %05d\n' "$i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
to r0.txt nb --run --now "$(at 0 1 0)"
for i in 1 2 3 4 5 6 7 8 9 10; do printf 'FILLER %05d\n' "$i" > "$(CUR)/sub/f$i.txt"; done
CONF_SAMPLE=40; write_conf
to r1.txt nb --run --now "$(at 1 1 0)"
is    "T23 ten destination copies altered, all in the sample: the same run repairs them and is GOOD" 0 "$RC"
is    "T23 ... none is still altered at the destination" 0 "$(/usr/bin/grep -r -l -F 'FILLER' "$(CUR)" 2>&1 | wc -l | tr -d ' ')"
is    "T23 ... and the ten wrong copies are kept under versions/" 10 "$(/usr/bin/grep -r -l -F 'FILLER' "$(VER)" 2>&1 | wc -l | tr -d ' ')"
CONF_SAMPLE=10
#  ONE wrong destination copy withdraws every earlier proof of the set: a full read-back in the same run (the checker's N3d)
fixture repall; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do printf 'filler %05d\n' "$i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
to r0.txt nb --run --now "$(at 0 1 0)"
"$PY" -c 'import os, sys
n = 0
for dp, dn, fn in os.walk(sys.argv[1]):
    for f in fn:
        p = os.path.join(dp, f); size = os.path.getsize(p); open(p, "wb").write(b"Z" * size); n += 1
print(n)' "$(CUR)" > "$T/out/altered.txt" 2>&1
is    "T23 control: all 35 destination copies of the set were altered behind the tool, same sizes" 35 "$(cat "$T/out/altered.txt")"
CONF_SAMPLE=3; write_conf
to r1.txt nb --run --now "$(at 1 1 0)"
is    "T23 a sample of only 3 finds a wrong copy: the SAME run reads back every other file of the set, repairs all 35 and is GOOD" 0 "$RC"
has   "T23 ... it says it withdrew the other proofs and read everything back" "$(OUTF r1.txt)" "FULL READ-BACK after the sample finding: the earlier proofs of all 32 other unsent files"
is    "T23 ... not one destination copy differs from its source afterwards" 0 "$(for f in a.txt same.txt sub/b.txt sub/f1.txt sub/f17.txt sub/f30.txt "sp ace/c d.txt"; do cmp -s "$T/vol/WEDNESDAY/$f" "$(CUR)/$f" || echo differs; done | wc -l | tr -d ' ')"
is    "T23 ... all 35 are counted as repaired" 35 "$(state last_good.counts.repaired)"
CONF_SAMPLE=10

echo; echo "T24 FORBIDDEN ROOTS IN BOTH DIRECTIONS (finding 3): a source that is an ANCESTOR of another seat's tree or of the other client's folder is refused"
fixture anc; mkdir -p "$T/vol/TUESDAY/0_Brain" "$T/vol/FRIDAY" "$T/vol/CODING/Datasec/NexusAI" "$T/vol/Notes" "$T/vol/Shared/tuesday-handover" "$T/vol/Shared/other"
echo "TUE-SEAT-MARK" > "$T/vol/TUESDAY/0_Brain/tuesday_ledger.md"; echo "TUE-SEAT-MARK" > "$T/vol/TUESDAY/plain.md"; echo "FRI-SEAT-MARK" > "$T/vol/FRIDAY/plain.md"
echo "DATASEC-MARK" > "$T/vol/CODING/Datasec/NexusAI/plain.md"; echo "VAULT-MARK" > "$T/vol/Notes/n.md"; echo "TUE-HANDOVER-MARK" > "$T/vol/Shared/tuesday-handover/h.md"; echo "OTHER-MARK" > "$T/vol/Shared/other/o.md"
write_conf "" refuse "set=General|DRIVE|$T/vol"
to a.txt nb --run --now "$(at 0 1 0)"
is    "T24 a set= naming the folder that HOLDS the seat trees (the drive root): exit 2" 2 "$RC"
has   "T24 ... refused as an ANCESTOR of a forbidden root" "$(OUTF a.txt)" "is an ANCESTOR of the forbidden root"
is    "T24 ... nothing started" 0 "$(started)"
is    "T24 ... nothing of TUESDAY's, FRIDAY's or the other client's is on the NAS" "0/0/0" "$(on_nas TUE-SEAT-MARK)/$(on_nas FRI-SEAT-MARK)/$(on_nas DATASEC-MARK)"
write_conf "" refuse "set=General|CODINGALL|$T/vol/CODING"
to b.txt nb --run --now "$(at 0 1 0)"
is    "T24 a set= naming the folder that holds the CLIENT folders: exit 2" 2 "$RC"
has   "T24 ... names the other client's folder as the root" "$(OUTF b.txt)" "another client's folder"
write_conf "" refuse "set=General|Shared|$T/vol/Shared"
to c.txt nb --run --now "$(at 0 1 0)"
is    "T24 a set= whose folder holds a 'tuesday-handover' folder beside ordinary ones: exit 2" 2 "$RC"
is    "T24 ... nothing of it travelled" 0 "$(on_nas TUE-HANDOVER-MARK)"
write_conf "" refuse "set=General|Notes|$T/vol/Notes" "set=General|Other|$T/vol/Shared/other"
to d.txt nb --run --now "$(at 0 1 0)"
is    "T24 NEIGHBOUR ordinary folders under the same roots, named one by one: exit 0" 0 "$RC"
is    "T24 ... and they arrived" "1/1" "$(on_nas VAULT-MARK)/$(on_nas OTHER-MARK)"
nbx "$PY" -c 'import os, sys
sys.path.insert(0, sys.argv[1]); import nb_core
T = os.environ["NB_TEST_ROOT"]; ctx = nb_core.Ctx("wednesday", T + "/vol/WEDNESDAY", 1)
print(" ".join(sorted(os.path.relpath(r, T + "/vol") for r, _ in ctx.forbidden_roots(T + "/vol"))))' "$LANE" > "$T/out/roots.txt" 2>&1
has   "T24 the forbidden roots found on this drive: the other client's folder, both other seats' trees, the handover folder" "$(OUTF roots.txt)" "CODING/Datasec FRIDAY Shared/tuesday-handover TUESDAY"
#  with no other seat's tree on the drive at all, the drive root is still refused: it is an ancestor of this seat's own tree
fixture ownanc
write_conf "" refuse "set=General|DRIVE|$T/vol"
to o.txt nb --run --now "$(at 0 1 0)"
is    "T24 a set= naming the drive root where no forbidden root exists: exit 2" 2 "$RC"
has   "T24 ... refused as an ANCESTOR of this seat's own tree" "$(OUTF o.txt)" "is an ANCESTOR of this seat's own tree"
#  one set inside another: only with the matching exclude_path
fixture nested
write_conf "" refuse "set=General|Sub|$T/vol/WEDNESDAY/sub"
to e.txt nb --run --now "$(at 1 1 0)"
is    "T24 a set INSIDE another set with no exclude_path for it: exit 2" 2 "$RC"
has   "T24 ... says the files would travel twice" "$(OUTF e.txt)" "the same files would travel twice"
write_conf "" refuse "set=General|Sub|$T/vol/WEDNESDAY/sub" "exclude_path=WEDNESDAY|sub"
to f.txt nb --run --now "$(at 1 1 0)"
is    "T24 NEIGHBOUR the same with exclude_path=WEDNESDAY|sub: exit 0" 0 "$RC"
yes   "T24 ... the file arrives under its own set" test -f "$T/nas/General/Wednesday/nightly-backup/current/Sub/b.txt"
no    "T24 ... and not a second time under the outer set" test -e "$(CUR)/sub/b.txt"
#  a FOLDER named exactly as another seat, inside a project set
fixture seatdir; mkdir -p "$T/vol/CODING/Secuura/Blockchain/src/Tuesday" "$T/vol/CODING/Secuura/Blockchain/src/tuesday-notes"
echo "$MARK exact seat folder" > "$T/vol/CODING/Secuura/Blockchain/src/Tuesday/x.txt"; echo "library words stay" > "$T/vol/CODING/Secuura/Blockchain/src/tuesday-notes/y.txt"
to s.txt nb --run --now "$(at 0 1 0)"
is    "T24 a FOLDER named exactly as another seat inside a project set does not travel" "0/0" "$RC/$(on_nas "$MARK exact seat folder")"
yes   "T24 NEIGHBOUR a folder whose name merely contains the word does (in project folders those are library words)" test -f "$T/nas/Secuura/Wednesday/nightly-backup/current/Secuura/Blockchain/src/tuesday-notes/y.txt"

echo; echo "T25 DAMAGE REACHES A SEAT WHOEVER FINDS IT (findings 6, 7, 13, 15)"
fixture dmg2
to n0.txt nightly --now "$(at 0 0 31)"
write_mounts none
to n1.txt nightly --now "$(at 1 0 31)"; to n2.txt nightly --now "$(at 2 0 31)"
echo '{"seat": "wednesday", "last_good": {"time": 17' > "$T/lane/state/wednesday.json"
to n3.txt nightly --now "$(at 3 0 31)"
has   "T25 the NIGHTLY job is the first reader of a damaged state file: it says so in its own log" "$(OUTF n3.txt)" "STATE FILE DAMAGED"
yes   "T25 ... and LEAVES A NOTICE on the drive" test -s "$T/lane/state/DAMAGE_NOTICE_wednesday.jsonl"
to d3.txt doctor_block "$(at 3 8 0)"
has   "T25 at the next boot doctor fails hard, in its OWN words" "$(OUTF d3.txt)" "✗ NAS BACKUP STATE WAS FOUND DAMAGED"
hasnt "T25 ... not with the three-day text (the mislabel of finding 15)" "$(OUTF d3.txt)" "NO GOOD NAS BACKUP FOR 3 DAYS"
HARD="$(/usr/bin/grep -F '✗' "$(OUTF d3.txt)" | cut -c1-400)"
yes   "T25 that line, cut at 400 characters as the launcher cuts it, still names the command to run" test "${HARD#*nas_backup_watch.sh --check}" != "$HARD"
to w3.txt watch --check --now "$(at 3 8 1)"
is    "T25 the watch: exit 5" 5 "$RC"
has   "T25 ... says what was damaged and who found it" "$(OUTF w3.txt)" "DAMAGE NOTICE, not yet acknowledged by a seat: the state file was found damaged"
has   "T25 ... (the nightly job)" "$(OUTF w3.txt)" "by the nightly job"
to n4.txt nightly --now "$(at 4 0 31)"
to d4.txt doctor_block "$(at 4 8 0)"
has   "T25 another nightly fire and another boot later: doctor STILL fails hard (nothing was used up)" "$(OUTF d4.txt)" "✗ NAS BACKUP STATE WAS FOUND DAMAGED"
echo "held" > "$T/lane/HOLD_wednesday"
to d4h.txt doctor_block "$(at 4 8 1)"
has   "T25 ... also while the seat is HELD" "$(OUTF d4h.txt)" "✗ NAS BACKUP STATE WAS FOUND DAMAGED"
mv -n "$T/lane/HOLD_wednesday" "$T/lane/HOLD_wednesday.lifted"
to ack.txt watch --ack-damage --now "$(at 4 8 5)"
is    "T25 a seat acknowledges: exit 0" 0 "$RC"
yes   "T25 ... the notice was MOVED into the lane's quarantine, not deleted" test -n "$(find "$T/lane/state" -path '*_quarantine_*' -name 'DAMAGE_NOTICE_wednesday.acknowledged.*' 2>&1)"
to d4b.txt doctor_block "$(at 4 8 6)"
hasnt "T25 ... and doctor no longer reports damage" "$(OUTF d4b.txt)" "FOUND DAMAGED"
#  a damaged INDEX: one plain line, moved aside, the run goes on, the lock is not left
fixture ix
to r0.txt nb --run --now "$(at 0 1 0)"
for k in 1 2 3 4 5 6 7 8 9 10 11 12; do echo 'this is not a sqlite database at all, just bytes'; done > "$T/lane/state/wednesday.index.sqlite"
to dry.txt nb --dry
is    "T25 a DRY run with a damaged index: exit 0" 0 "$RC"
hasnt "T25 ... no traceback" "$(OUTF dry.txt)" "Traceback"
has   "T25 ... it says so" "$(OUTF dry.txt)" "INDEX DAMAGED"
yes   "T25 ... and leaves the file where it is (a dry run writes nothing)" /usr/bin/grep -q -F 'not a sqlite database' "$T/lane/state/wednesday.index.sqlite"
no    "T25 ... no notice either" test -e "$T/lane/state/DAMAGE_NOTICE_wednesday.jsonl"
to r1.txt nb --run --now "$(at 1 1 0)"
is    "T25 a REAL run with a damaged index: it moves it aside, compares again, and is GOOD (exit 0)" 0 "$RC"
has   "T25 ... one plain line" "$(OUTF r1.txt)" "INDEX DAMAGED:"
hasnt "T25 ... no traceback" "$(OUTF r1.txt)" "Traceback"
no    "T25 ... the lock is not left behind" test -d "$T/lane/state/wednesday.lock.d"
yes   "T25 ... the damaged index was MOVED into the lane's quarantine" test -n "$(find "$T/lane/state" -path '*_quarantine_*' -name 'wednesday.index.sqlite.damaged.*' 2>&1)"
has   "T25 ... every file already on the NAS was compared by content again" "$(OUTF r1.txt)" "compared by sha256"
to w.txt watch --check --now "$(at 1 9 0)"
is    "T25 ... and the watch reports the damage to whoever asks (exit 5)" 5 "$RC"
#  a DRY run never moves a damaged state file
fixture drydmg
to r0.txt nb --run --now "$(at 0 1 0)"
echo 'garbage' > "$T/lane/state/wednesday.json"
to dry.txt nb --dry
has   "T25 a DRY run with a damaged state file says so" "$(OUTF dry.txt)" "STATE FILE DAMAGED"
yes   "T25 ... and leaves it where it is" /usr/bin/grep -q -x -F 'garbage' "$T/lane/state/wednesday.json"
is    "T25 ... nothing moved into a quarantine by the dry run" 0 "$(find "$T/lane/state" -name '*.damaged.*' 2>&1 | wc -l | tr -d ' ')"
#  valid JSON that is not a valid state: one plain line, never a traceback (finding 13)
fixture badstate
to r0.txt nb --run --now "$(at 0 1 0)"
echo '{"seat": "wednesday", "last_good": {}, "recent_attempts": [{}]}' > "$T/lane/state/wednesday.json"
to w.txt watch --check --now "$(at 1 9 0)"
is    "T25 a state file that is valid JSON with its fields missing: the watch exits 5" 5 "$RC"
hasnt "T25 ... no traceback" "$(OUTF w.txt)" "Traceback"
has   "T25 ... one plain line" "$(OUTF w.txt)" "STATE FILE DAMAGED"
echo '{"seat": "wednesday", "last_good": {"note": "x"}, "recent_attempts": []}' > "$T/lane/state/wednesday.json"
to n.txt nightly --now "$(at 2 0 31)"
hasnt "T25 the nightly job on a last_good without its time: no traceback" "$(OUTF n.txt)" "Traceback"
has   "T25 ... it says so and goes on" "$(OUTF n.txt)" "STATE FILE DAMAGED"
is    "T25 ... and that night's run is GOOD" good "$(state last_attempt.status)"
#  a last_good in the FUTURE (one run under a wrong clock) is damage, not 'already backed up'
fixture future
to r0.txt nb --run --now "$(at 0 1 0)"
"$PY" -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["last_good"]["time"]+=86400*400; json.dump(d,open(p,"w"))' "$T/lane/state/wednesday.json"
to n.txt nightly --now "$(at 5 0 31)" --decide-only
has   "T25 a last_good 400 days in the future is treated as damage" "$(OUTF n.txt)" "is in the FUTURE"
has   "T25 ... so the nightly job decides to RUN, not to skip every night" "$(OUTF n.txt)" "RUN: no good backup on record"
#  an unexpected error anywhere in a run: one plain line, the lock released, the state not left 'running'
fixture crash; mkdir -p "$T/lane/manifests/wednesday"; chmod 555 "$T/lane/manifests/wednesday"
to c.txt nb --run --now "$(at 0 1 0)"; chmod 755 "$T/lane/manifests/wednesday"
no    "T25 a run that cannot write its manifest: NOT exit 0" test "$RC" -eq 0
hasnt "T25 ... no traceback" "$(OUTF c.txt)" "Traceback"
no    "T25 ... the lock is not left behind" test -d "$T/lane/state/wednesday.lock.d"
is    "T25 ... the state says failed, not running" failed "$(state last_attempt.status)"
to c2.txt nb --run --now "$(at 0 1 1)"
is    "T25 NEIGHBOUR writable again: the next run is GOOD without anyone clearing a lock" 0 "$RC"

echo; echo "T26 PROOF IS SAVED AS IT GOES (finding 8): an interrupted copy resumes without re-reading what it proved, and never says GOOD"
for sig in TERM HUP; do
  fixture "chunks_$sig"; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do echo "payload $i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
  S="$(mk_stub rsync_third_hangs "$PRE"'if [ "$N" -ge 3 ]; then sleep 60; fi; exec "$REAL" "$@"')"; CONF_CHUNK=5; write_conf "$S"
  nb --run --now "$(at 0 1 0)" > "$T/out/bg.txt" 2>&1 & BG=$!
  yes "T26 SIG$sig: the engine reached its third chunk (25 files, 5 a chunk)" wait_calls 3
  sleep 1; TOOLPID="$(state_owner pid)"; kill -"$sig" "$TOOLPID" 2>&1; wait "$BG" 2>&1
  is  "T26 SIG$sig mid-copy: the two finished chunks are PROVEN AND SAVED (10 index rows)" 10 "$(idxrows)"
  is  "T26 SIG$sig: the state never says good" None "$(state last_good)"
  is  "T26 SIG$sig: the attempt is recorded as failed, not left running" failed "$(state last_attempt.status)"
  no  "T26 SIG$sig: the lock is released" test -d "$T/lane/state/wednesday.lock.d"
  is  "T26 SIG$sig: no COMPLETE marker" 0 "$(completed)"
  sleep 1
  is  "T26 SIG$sig: the engine was stopped with the tool" 0 "$(pgrep -f "$T/stub/rsync_third_hangs" | wc -l | tr -d ' ')"
  write_conf
  to r1.txt nb --run --now "$(at 0 1 10)"
  is  "T26 SIG$sig: the resume is GOOD" 0 "$RC"
  has "T26 SIG$sig: ... and sends only the 15 files that were not proven" "$(OUTF r1.txt)" "to copy: 15 files"
  hasnt "T26 SIG$sig: ... re-reading nothing that was proven" "$(OUTF r1.txt)" "compared by sha256 (same size"
  CONF_CHUNK=""
done
#  the cap: honoured between chunks and between files; what was proven is kept
fixture capchunks; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do echo "payload $i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
S="$(mk_stub rsync_2s "$PRE"'sleep 2; exec "$REAL" "$@"')"; CONF_CHUNK=5; write_conf "$S"
to k.txt nb --run --now "$(at 0 1 0)" --max-seconds 5
is    "T26 a copy stopped by the cap: exit 4" 4 "$RC"
is    "T26 ... state says killed-cap, never good" "killed-cap/None" "$(state last_attempt.status)/$(state last_good)"
ROWS="$(idxrows)"
yes   "T26 ... the chunks proven before the cap are saved ($ROWS index rows, at least 5, fewer than 25)" test "$ROWS" -ge 5 -a "$ROWS" -lt 25
has   "T26 ... a set the run never reached is named as not proven" "$(OUTF k.txt)" "Secuura: this set was not reached"
write_conf; CONF_CHUNK=""
to k2.txt nb --run --now "$(at 0 1 10)"
is    "T26 NEIGHBOUR the next run finishes GOOD" 0 "$RC"
#  the watchdog (the checker's mutant K17): a read that blocks past the cap is stopped, and the lock is released
fixture wdog
nbx NB_TEST_WATCHDOG_MARGIN=2 NB_TEST_HASH_DELAY=30 "$LANE/nas_backup.sh" --run --now "$(at 0 1 0)" --max-seconds 3 > "$T/out/w.txt" 2>&1; RC=$?
is    "T26 a proof read that blocks past the cap: the WATCHDOG stops the run (exit 4)" 4 "$RC"
has   "T26 ... and it is the WATCHDOG that says so" "$(OUTF w.txt)" "WATCHDOG: the run was still going 2 s after its 3 s cap"
no    "T26 ... the lock is released" test -d "$T/lane/state/wednesday.lock.d"
is    "T26 ... the state is not good" None "$(state last_good)"
"$PY" -c 'import os, sys
sys.path.insert(0, sys.argv[1]); import nb_core
class C: troot = None
os.environ["NB_TEST_WATCHDOG_MARGIN"] = "2"
print("margin-outside-test-mode=%d" % nb_core.watchdog_margin(C()))' "$LANE" > "$T/out/wm.txt" 2>&1
has   "T26 outside test mode the margin is 900 s whatever the environment says" "$(OUTF wm.txt)" "margin-outside-test-mode=900"

echo; echo "T27 THE MINORS (findings 10 to 15) and the guards the second check found untested"
#  10. refusals under the HOLD never start the three-day clock; lifting the hold starts it
fixture holdclock; mkdir -p "$T/lane/state"
"$PY" -c 'import json, sys
t = float(sys.argv[2]); r = "REFUSED — /x/HOLD_wednesday exists: real runs are HELD (arming is the coordinators word); --dry is still allowed; nothing run"
a = {"reason": r, "status": "refused", "time": t, "time_local": "2026-12-01 14:46:18 AEDT"}
json.dump({"armed_at": None, "first_attempt_at": t, "flag": None, "last_attempt": dict(a, pid=1), "last_fire": None, "last_good": None, "recent_attempts": [a], "schema": 1, "seat": "wednesday"}, open(sys.argv[1], "w"))' "$T/lane/state/wednesday.json" "$(at 0 14 46)"
echo "held" > "$T/lane/HOLD_wednesday"
to h0.txt watch --check --now "$(at 3 9 0)"
is    "T27 the real lane's state as it is today (one refusal under the hold, 2.8 days ago), still held: exit 0" 0 "$RC"
mv -n "$T/lane/HOLD_wednesday" "$T/lane/HOLD_wednesday.lifted"
to h1.txt watch --check --now "$(at 4 9 0)"
is    "T27 the hold lifted four days after that refusal: NOT overdue (exit 0)" 0 "$RC"
has   "T27 ... the clock starts at the lift" "$(OUTF h1.txt)" "the three-day clock starts now"
hasnt "T27 ... no OVERDUE" "$(OUTF h1.txt)" "OVERDUE"
to h1d.txt doctor_block "$(at 4 9 1)"
hasnt "T27 ... and doctor does not fail hard that morning" "$(OUTF h1d.txt)" "✗"
to h2.txt watch --check --now "$(at 6 9 0)"
is    "T27 two days after the lift: still ok (the start is not rolled forward by every check)" 0 "$RC"
to h3.txt watch --check --now "$(at 7 9 1)"
is    "T27 three days after the lift with no backup: OVERDUE (exit 3)" 3 "$RC"
fixture holdnew; echo "held" > "$T/lane/HOLD_wednesday"
to j.txt nb --run --now "$(at 0 1 0)"
is    "T27 a refusal under the hold is recorded as held" held "$(state last_attempt.status)"
is    "T27 ... and does not start the clock" None "$(state first_attempt_at)"
#  11. SIGHUP is T26.  12. the mount is checked before every set and before GOOD
fixture unmount
S="$(mk_stub rsync_unmount "$PRE"'if [ "$N" = 1 ]; then /usr/bin/grep -v smbfs "$STUBDIR/../mount.txt" > "$STUBDIR/../mount.tmp"; mv "$STUBDIR/../mount.tmp" "$STUBDIR/../mount.txt"; fi; exec "$REAL" "$@"')"; write_conf "$S"
to u.txt nb --run --now "$(at 0 1 0)"
no    "T27 the NAS leaves the mount table during the first set: the run is NOT exit 0" test "$RC" -eq 0
hasnt "T27 ... it does not say GOOD" "$(OUTF u.txt)" "GOOD: every in-scope"
has   "T27 ... it says the share is no longer mounted" "$(OUTF u.txt)" "no longer mounted as a network share"
is    "T27 ... the second set was not started" 1 "$(/usr/bin/grep -c -F -- '--- set' "$(OUTF u.txt)")"
write_mounts
to u2.txt nb --run --now "$(at 0 1 5)"
is    "T27 NEIGHBOUR mounted throughout: GOOD" 0 "$RC"
#  15. a reused engine GROUP id is not this seat's engine
fixture pgid; mkdir -p "$T/lane/state/wednesday.lock.d"
SP="$("$PY" -c 'import subprocess; D = subprocess.DEVNULL; print(subprocess.Popen(["/bin/sleep", "60"], start_new_session=True, stdin=D, stdout=D, stderr=D).pid)')"; SG="$SP"   # its own process group
printf '{"pid": 999999, "pid_started": "x", "started_local": "x", "engine_pgid": %s, "engine_started": "%s"}\n' "$SG" "$(ps -o lstart= -p "$SG" | sed -e 's/^ *//' -e 's/ *$//')" > "$T/lane/state/wednesday.lock.d/owner.json"
to g1.txt nb --clear-stale-lock
is    "T27 a dead holder whose recorded engine group is ALIVE and started when the lock says: clear refused (exit 6)" 6 "$RC"
printf '{"pid": 999999, "pid_started": "x", "started_local": "x", "engine_pgid": %s, "engine_started": "Thu Jan  1 00:00:00 1970"}\n' "$SG" > "$T/lane/state/wednesday.lock.d/owner.json"
to g2.txt nb --clear-stale-lock
is    "T27 the same group id now held by something that started at ANOTHER time (a reused id): the lock can be cleared (exit 0)" 0 "$RC"
kill "$SP" 2>&1
#  K18: an engine of this seat is recognised by its command line too, not only by the recorded group
fixture k18; mkdir -p "$T/lane/state/wednesday.lock.d"
printf '{"pid": 999999, "pid_started": "x", "started_local": "x", "engine_pgid": null}\n' > "$T/lane/state/wednesday.lock.d/owner.json"
bash -c 'exec -a rsync /usr/bin/tail -f /dev/null "$0"' "$T/nas/General/Wednesday/nightly-backup/current/x/" > "$T/out/fake_engine.txt" 2>&1 & FAKE=$!
sleep 1
to k.txt nb --clear-stale-lock
is    "T27 a lock with no recorded engine group, and an rsync writing to this seat's folder still alive: clear refused (exit 6)" 6 "$RC"
has   "T27 ... says the engine is still running" "$(OUTF k.txt)" "STILL RUNNING"
kill "$FAKE" 2>&1; wait "$FAKE" 2>&1
to k2.txt nb --clear-stale-lock
is    "T27 NEIGHBOUR once it has ended: cleared (exit 0)" 0 "$RC"
#  the tool's own run state (lock, index) is never in a plan: it changes while the run proves files
fixture ownstate; mkdir -p "$T/vol/WEDNESDAY/2_Project_Files/nas-backup/state" "$T/vol/WEDNESDAY/2_Project_Files/nas-backup/logs"
nbx "$PY" -c 'import os, sys
sys.path.insert(0, sys.argv[1]); import nb_core
T = os.environ["NB_TEST_ROOT"]; ctx = nb_core.Ctx("wednesday", T + "/vol/WEDNESDAY", 1); ctx.load_conf()
ctx.state_dir = T + "/vol/WEDNESDAY/2_Project_Files/nas-backup/state"          # where the real lane keeps it: inside the seat tree
r = nb_core.Rules(ctx, ctx.conf["sets"][0])
print("state=%s logs=%s" % (r.match("state", "2_Project_Files/nas-backup/state", True), r.match("logs", "2_Project_Files/nas-backup/logs", True)))
r2 = nb_core.Rules(ctx, ctx.conf["sets"][1])
print("other-set-state=%s" % (r2.match("state", "2_Project_Files/nas-backup/state", True),))' "$LANE" > "$T/out/own.txt" 2>&1
has   "T27 the lane's own state folder (lock, index) is excluded from the seat tree's plan; its logs are not" "$(OUTF own.txt)" "state=('own-run-state', '2_Project_Files/nas-backup/state') logs=None"
has   "T27 ... and only where it really lies inside the set" "$(OUTF own.txt)" "other-set-state=None"
#  K06: the engine itself refuses a tree that is not this seat's, without the wrapper
fixture k06; mkdir -p "$T/vol/ODDNAME"
env -u WED_AGENT NB_TEST_ROOT="$T" "$PY" "$LANE/nb_core.py" backup --seat wednesday --tree "$T/vol/ODDNAME" --dry > "$T/out/k06.txt" 2>&1; RC=$?
is    "T27 the engine called directly with --seat wednesday and a tree of another name: exit 2" 2 "$RC"
has   "T27 ... says the tree is not this seat's" "$(OUTF k06.txt)" "is not a 'wednesday' tree"
#  K12: test mode refuses a NAS root outside the test folder
sed -e "s|^nas_root=.*|nas_root=/private/tmp|" "$T/lane/seats/wednesday.conf" > "$T/c.tmp"; mv "$T/c.tmp" "$T/lane/seats/wednesday.conf"
to k12.txt nb --run --now "$(at 0 1 0)"
is    "T27 test mode with a nas_root outside the test folder: exit 2" 2 "$RC"
has   "T27 ... refused BY THE TEST-MODE FENCE" "$(OUTF k12.txt)" "TEST MODE: nas_root and source_volume must both live under NB_TEST_ROOT"
#  K14: a planned folder that is missing at the destination fails the night
fixture k14
S="$(mk_stub rsync_no_emptydir 'args=(); for a in "$@"; do case "$a" in --files-from=*) L="${a#--files-from=}"; tr "\0" "\n" < "$L" | /usr/bin/grep -v "^emptydir$" | tr "\n" "\0" > "$L.filtered"; args+=( "--files-from=$L.filtered" );; *) args+=( "$a" );; esac; done; exec "$REAL" "${args[@]}"')"; write_conf "$S"
to k14.txt nb --run --now "$(at 0 1 0)"
no    "T27 an engine that does not create one planned (empty) folder: NOT exit 0" test "$RC" -eq 0
has   "T27 ... the folder is named" "$(OUTF k14.txt)" "NOT DELIVERED: WEDNESDAY/emptydir/"
#  K22: an engine exit code other than 0, 23, 24 is never success
fixture k22
S="$(mk_stub rsync_exit12 '"$REAL" "$@"; exit 12')"; write_conf "$S"
to k22.txt nb --run --now "$(at 0 1 0)"
no    "T27 an engine that exits 12: NOT exit 0" test "$RC" -eq 0
has   "T27 ... says so" "$(OUTF k22.txt)" "engine exit code 12"

echo; echo "T28 CONVENTIONAL CREDENTIAL NAMES (finding 2; BEST-EFFORT by ruling): the checker's 40 and the two real files' patterns stay out; ordinary neighbours arrive"
fixture names; P="$T/vol/WEDNESDAY/proj"
NAMES=".netrc|.pgpass|credentials.json|service-account.json|service-account-prod-1234.json|.aws/credentials|.kube/config|release.keystore|upload.jks|.htpasswd|secrets.yml|.npmrc|terraform.tfvars|prod.auto.tfvars|.docker/config.json|api/local.settings.json|playwright/.auth/token.json|application_default_credentials.json|serviceAccountKey.json|.git-credentials|id_ed25519|payment.skey|mnemonic.txt|wallet/seed-phrase.txt|.vault-token|kubeconfig|auth.json|secrets.toml|AuthKey_ABC123.p8|private_key.txt|.dockercfg|.boto|credentials|htpasswd|key.der|backup.kdbx|terraform.tfstate|.env.production|client_secret_123.json|.pypirc"
MORE="token.json|azureProfile.json|env.backup|cert.crt|my-sa.json|x.tfvars.json|gcloud/legacy_credentials|accessTokens.json|payment.vkey|stake.addr|vc_signing_key.out|recovery-phrase.md|T6-no-MNEMONIC.json|post_api_credentials_ok.json|secrets.ts|.secrets/x|wallet.dat|UTC--2026-key|server.privkey|site.ovpn|a.mobileprovision|dev.kubeconfig|.s3cfg|keystore.json|e2e/.auth/user.json"
NEIGH="ordinary-neighbour.md|keyboard.js|environment.ts|tokenomics.md|credentials.ts|authorize.json|secrets.example.yml|certificate-notes.md|token-launch.txt|account-service.json"
plant() { local IFS='|'; local n; for n in $1; do mkdir -p "$(dirname "$P/$n")"; echo "$2 $n" > "$P/$n"; done; }
plant "$NAMES" "CRED40"; plant "$MORE" "CREDMORE"; plant "$NEIGH" "NEIGHBOUR"
is    "T28 control: 40 + 25 marked files and 10 neighbours are planted" "40/25/10" "$(/usr/bin/grep -r -l -F 'CRED40' "$P" | wc -l | tr -d ' ')/$(/usr/bin/grep -r -l -F 'CREDMORE' "$P" | wc -l | tr -d ' ')/$(/usr/bin/grep -r -l -F 'NEIGHBOUR' "$P" | wc -l | tr -d ' ')"
to n.txt nb --run --now "$(at 0 1 0)"
is    "T28 run exits 0" 0 "$RC"
is    "T28 NOT ONE of the checker's 40 conventional names is on the NAS (23 of them travelled in round 2)" 0 "$(on_nas CRED40)"
is    "T28 nor one of 25 more (an ordinary-named file inside a .auth folder, token stores, wallet and key names)" 0 "$(on_nas CREDMORE)"
is    "T28 NEIGHBOURS: all 10 ordinary names beside them arrive" 10 "$(on_nas NEIGHBOUR)"
has   "T28 the summary counts the new shapes" "$(OUTF n.txt)" "terraform-variables="
echo "CRED40 leak" > "$(CUR)/proj/leaked_by_hand.txt"
is    "T28 CAN-FAIL: a marked file put on the fake NAS by hand IS found by the same count" 1 "$(on_nas CRED40)"
#  the lane's own independent scan agrees on a list it is handed (and can fail)
mkdir -p "$T/scan"; printf 'ok/readme.md\0ok/my-environment.ts\0ok/keyboard.js\0' > "$T/scan/s1_dry_A.files0"
"$PY" "$LANE/tests/scan_dry_lists.py" "$T/scan" s1 > "$T/out/scan_ok.txt" 2>&1; RC=$?
is    "T28 the independent scan on a clean list: exit 0" 0 "$RC"
printf 'ok/readme.md\0ok/my-environment.ts\0ok/keyboard.js\0api/local.settings.json\0p/.auth/token.json\0' > "$T/scan/s2_dry_A.files0"
"$PY" "$LANE/tests/scan_dry_lists.py" "$T/scan" s2 > "$T/out/scan_bad.txt" 2>&1; RC=$?
is    "T28 CAN-FAIL: the same scan on a list holding the two real files' names: exit 1" 1 "$RC"

echo
echo "=== $PASS passed, $FAIL failed — fixtures kept at $RUN ==="
if [ "$FAIL" -ne 0 ]; then printf 'FAILED:%s\n' "$FAILED"; exit 1; fi
exit 0
