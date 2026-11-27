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
    echo "hash_sample=10"
    echo "rsync=${1:-$REAL_RSYNC}"
    echo "set=General|WEDNESDAY|$T/vol/WEDNESDAY"
    echo "set=Secuura|Secuura|$T/vol/CODING/Secuura"
    [ -n "${3:-}" ] && echo "$3"
  } > "$T/lane/seats/wednesday.conf"
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
  CONF_STATUS=confirmed; CONF_STALL=900
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
is  "T1 no run markers on the NAS" 0 "$(started)"

echo; echo "T2  a real run copies, counts both sides, records state (neighbour of T1: this one DOES write)"
to t2.txt nb --run --now "$(at 0 1 0)"
is  "T2 real run exits 0" 0 "$RC"
has "T2 says GOOD" "$(OUTF t2.txt)" "GOOD: every in-scope source file"
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
echo "{\"pid\": $HOLDER, \"started_local\": \"test\"}" > "$T/lane/state/wednesday.lock.d/owner.json"
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
fixture r_client; write_conf "" refuse "set=Datasec|X|$T/vol/WEDNESDAY/sub"
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
        nb_core.run_rsync(None, ["rsync", "-t", flag, "a/", "b/"], "/dev/null", "/dev/null", 0, 0); print("NOT REFUSED", flag); sys.exit(1)
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
echo "{\"pid\": $HOLDER, \"started_local\": \"test\"}" > "$T/lane/state/wednesday.lock.d/owner.json"
to n7.txt nightly --now "$(at 3 0 31)"
has "T7 a run in progress: SKIP with the reason" "$(OUTF n7.txt)" "SKIP: a run is in progress"
is  "T7 ... exit 0" 0 "$RC"
kill "$HOLDER" 2>&1; wait "$HOLDER" 2>&1
to n7b.txt nb --clear-stale-lock
yes "T7 every nightly decision is in the nightly log" test "$(/usr/bin/grep -c -F 'nightly[wednesday]' "$T/lane/logs/wednesday/nightly.log")" -ge 6

echo; echo "T8  THREE nights missed: the flag fires once and only once per gap"
#   last good = day 2 00:31. The NAS is away for the nights of day 3, 4 and 5.
write_mounts none
to f3.txt nightly --now "$(at 3 0 31)"
is  "T8 night 1 without the NAS: refused, exit 2" 2 "$RC"
to f4.txt nightly --now "$(at 4 0 31)"
to f4w.txt watch --flag --now "$(at 4 9 0)"
is  "T8 after 2 days: not yet overdue (exit 0)" 0 "$RC"
is  "T8 no card command yet" 0 "$(cards f)"
to f5.txt nightly --now "$(at 5 0 31)"
has "T8 night 3: the nightly job itself raises the flag (72 h since the last good backup)" "$(OUTF f5.txt)" "CARD-COMMAND:"
has "T8 the card command is a decision_queue.sh add" "$(OUTF f5.txt)" "decision_queue.sh add --id nas-backup-overdue-wednesday-"
has "T8 option a = approve an out-of-sequence backup now" "$(OUTF f5.txt)" "a:Approve an out-of-sequence backup now"
has "T8 option b = wait for tonight's window, the default" "$(OUTF f5.txt)" "--recommended b"
has "T8 the BLUF carries the failure reason" "$(OUTF f5.txt)" "not mounted as a network share"
to f5w.txt watch --flag --now "$(at 5 8 0)"
is  "T8 the launcher's check the same morning: still overdue (exit 3)" 3 "$RC"
hasnt "T8 ... but the card command is NOT issued a second time" "$(OUTF f5w.txt)" "CARD-COMMAND:"
to f5x.txt watch --flag --now "$(at 5 20 0)"
to f6.txt nightly --now "$(at 6 0 31)"
is  "T8 across five more checks and fires in the same gap: exactly ONE card command" 1 "$(cards f)"
to f6c.txt watch --check --now "$(at 6 9 0)"
is  "T8 --check stays read-only and reports overdue (exit 3)" 3 "$RC"
to g_mark.txt watch --mark-raised nas-backup-overdue-wednesday-20261203 --now "$(at 6 9 5)"
is  "T8 state records the card as raised" True "$(state flag.raised)"
#   the NAS comes back: the next window runs, the gap closes
write_mounts
to g7.txt nightly --now "$(at 7 0 31)"
has "T8 NAS back: the next window runs and names the missed nights" "$(OUTF g7.txt)" "night(s) missed: catching up"
to g7w.txt watch --flag --now "$(at 7 9 0)"
is  "T8 after a good backup the watch is quiet (exit 0)" 0 "$RC"
#   a NEW gap raises a NEW card, once
write_mounts none
to h8.txt nightly --now "$(at 8 0 31)"; to h9.txt nightly --now "$(at 9 0 31)"; to h10.txt nightly --now "$(at 10 0 31)"
to h10w.txt watch --flag --now "$(at 10 9 0)"
is  "T8 a second gap: exactly one NEW card command" 1 "$(cards h)"

echo; echo "T9  the watch does not depend on the backup job (a job that never fires cannot report itself)"
fixture never
to w0.txt watch --flag --now "$(at 0 9 0)"
is  "T9 nothing armed, nothing on record: exit 0" 0 "$RC"
has "T9 says NOT ARMED" "$(OUTF w0.txt)" "NOT ARMED"
to w1.txt watch --mark-armed --now "$(at 0 9 0)"
to w2.txt watch --flag --now "$(at 2 9 0)"
is  "T9 armed, 48 h, the job never fired: not yet overdue" 0 "$RC"
to w3.txt watch --flag --now "$(at 3 9 1)"
is  "T9 armed, 72 h, the job NEVER fired once: OVERDUE (exit 3)" 3 "$RC"
has "T9 the card says the job did not fire" "$(OUTF w3.txt)" "the job did not fire"
mv -n "$T/lane/seats/wednesday.conf" "$T/lane/seats/wednesday.conf.aside"; write_mounts none
to w4.txt watch --check --now "$(at 3 9 2)"
is  "T9 it still reports with the NAS away and the conf missing (exit 3)" 3 "$RC"

#   HELD is not a missed backup: no card while the hold file exists (pair: the same state without it is overdue)
mv -n "$T/lane/seats/wednesday.conf.aside" "$T/lane/seats/wednesday.conf"
echo "held" > "$T/lane/HOLD_wednesday"
to w5.txt watch --flag --now "$(at 4 9 0)"
is  "T9 HELD: exit 0" 0 "$RC"
has "T9 HELD is said out loud" "$(OUTF w5.txt)" "HELD:"
hasnt "T9 HELD raises no card" "$(OUTF w5.txt)" "CARD-COMMAND:"
mv -n "$T/lane/HOLD_wednesday" "$T/lane/HOLD_wednesday.lifted"
to w6.txt watch --check --now "$(at 4 9 1)"
is  "T9 PAIR the hold moved aside, same state: overdue (exit 3)" 3 "$RC"

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
            "dirs": set(["Logs", "logs", "ev"]), "links": {}, "specials": [], "excluded": {}, "errors": [], "excluded_list": []}
nb_core.walk = fake
plan = nb_core.plan_set(ctx, ctx.conf["sets"][0], {}, [], do_hash=False)
print("copy=%s" % ",".join(plan["copy"]))
print("copy_dirs=%s" % ",".join(plan["copy_dirs"]))
print("skipped=%d names=%d problems=%d" % (len(plan["collision_skipped"]), len(plan["collisions"]), len(plan["problems"])))' "$LANE" > "$T/out/c.txt" 2>&1; RC=$?
is  "T11 the planner ran" 0 "$RC"
has "T11 only the non-colliding file is planned for copy" "$(OUTF c.txt)" "copy=keep.txt"
has "T11 a folder pair that collides is not created; the clean folder is" "$(OUTF c.txt)" "copy_dirs=ev"
has "T11 four files under four colliding names are counted as not backed up, and it is not a failure" "$(OUTF c.txt)" "skipped=4 names=4 problems=0"

echo
echo "=== $PASS passed, $FAIL failed — fixtures kept at $RUN ==="
if [ "$FAIL" -ne 0 ]; then printf 'FAILED:%s\n' "$FAILED"; exit 1; fi
exit 0
