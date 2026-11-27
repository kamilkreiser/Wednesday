#!/bin/bash
# lib3.sh — third checker's harness (2026-11-27). Works ONLY on the scratch COPY of the lane under /private/tmp/qa3nb
# with fake trees under /private/tmp/qa3nb/fx. Never a real NAS path. No rm. Modelled on the lane's tests/run.sh helpers.
S=/private/tmp/qa3nb
LANE="${LANE_OVERRIDE:-$S/copy/WEDNESDAY/2_Project_Files/nas-backup}"
PY=/opt/homebrew/bin/python3; REAL_RSYNC=/opt/homebrew/bin/rsync
FXBASE="${FXBASE:-$S/fx}/$(date +%H%M%S)_$$"; mkdir -p "$FXBASE"
T=""; RC=0
at() { "$PY" -c 'import datetime,sys; d=datetime.datetime(2026,12,1)+datetime.timedelta(days=int(sys.argv[1])); print(int(d.replace(hour=int(sys.argv[2]),minute=int(sys.argv[3])).timestamp()))' "$1" "$2" "$3"; }
seal_conf() { local f="$T/lane/seats/wednesday.conf"; local n; n="$(/usr/bin/grep -v -E '^[[:space:]]*(#|$)' "$f" | /usr/bin/grep -c -v -E '^END ')"; /usr/bin/grep -v -E '^END ' "$f" > "$f.tmp"; mv "$f.tmp" "$f"; echo "END lines=$n" >> "$f"; }
# conf_base: the scalar lines; then the caller appends set= and other lines with addc, then seal_conf
conf_base() { { echo "status=confirmed"; echo "source_volume=${VOL:-$T/vol}"; echo "nas_root=$T/nas"; echo "fire=00:30"; echo "window_hours=5"; echo "late_fire=refuse"; echo "min_free_gib=200"
  echo "max_seconds=${CONF_MAXS:-600}"; echo "stall_seconds=900"; echo "hash_sample=${CONF_SAMPLE:-10}"; [ -n "${CONF_CHUNK:-}" ] && echo "chunk_files=$CONF_CHUNK"; echo "rsync=${CONF_RSYNC:-$REAL_RSYNC}"; } > "$T/lane/seats/wednesday.conf"; }
addc() { echo "$1" >> "$T/lane/seats/wednesday.conf"; }
std_conf() { conf_base; addc "set=General|WEDNESDAY|${VOL:-$T/vol}/WEDNESDAY"; local x; for x in "$@"; do addc "$x"; done; seal_conf; }
write_mounts() { { echo "/dev/disk9s1 on ${VOL:-$T/vol} (apfs, local, nodev, nosuid, journaled, noowners)"; echo "//user@nas.example/DEV-Working on $T/nas (smbfs, nodev, nosuid, mounted by tester)"; } > "$T/mount.txt"; }
fixture() { T="$FXBASE/$1"; mkdir -p "$T/vol/WEDNESDAY/sub" "$T/nas/Secuura" "$T/nas/General" "$T/lane/seats" "$T/stub" "$T/o"
  echo "content of a" > "$T/vol/WEDNESDAY/a.txt"; echo "b" > "$T/vol/WEDNESDAY/sub/b.txt"; echo 5000 > "$T/free_gib.txt"
  CONF_SAMPLE=10; CONF_CHUNK=""; CONF_RSYNC=""; CONF_MAXS=""; std_conf; write_mounts; }
nb()      { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="${VOL:-$T/vol}/WEDNESDAY" "$LANE/nas_backup.sh" "$@"; }
nightly() { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="${VOL:-$T/vol}/WEDNESDAY" "$LANE/nas_backup_nightly.sh" "$@"; }
watch()   { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="${VOL:-$T/vol}/WEDNESDAY" "$LANE/nas_backup_watch.sh" "$@"; }
run() { nb --run --now "$1" > "$T/o/$2.txt" 2>&1; RC=$?; echo "$RC"; }   # prints rc
good() { /usr/bin/grep -c -F 'GOOD: every in-scope' "$T/o/$1.txt"; }
line() { /usr/bin/grep -F -- "$2" "$T/o/$1.txt" | head -${3:-1} | cut -c1-${4:-300}; }
CURG() { echo "$T/nas/General/Wednesday/nightly-backup/current"; }
VERG() { echo "$T/nas/General/Wednesday/nightly-backup/versions"; }
state() { "$PY" -c 'import json,sys
d=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."):
    d = d.get(k) if isinstance(d, dict) else None
print(d)' "$T/lane/state/wednesday.json" "$1" 2>&1; }
idxrows() { "$PY" -c 'import sqlite3,sys
try:
    print(sqlite3.connect(sys.argv[1]).execute("select count(*) from files").fetchone()[0])
except Exception as e: print("ERR", e)' "$T/lane/state/wednesday.index.sqlite" 2>&1; }
completed() { find "$T/nas" -name 'RUN_*_COMPLETE.txt' 2>&1 | wc -l | tr -d ' '; }
mk_stub() { local f="$T/stub/$1"; { echo '#!/bin/bash'; echo "REAL=$REAL_RSYNC"; echo 'STUBDIR="$(dirname "$0")"'; echo 'for a in "$@"; do if [ "$a" = "--version" ]; then exec "$REAL" --version; fi; done'
  echo '[ -f "$STUBDIR/calls" ] && N=$(cat "$STUBDIR/calls") || N=0; N=$((N+1)); echo $N > "$STUBDIR/calls"; DEST="${@: -1}"; V="$STUBDIR/../vol/WEDNESDAY"; mkdir -p "$STUBDIR/taken"'
  echo "$2"; } > "$f"; chmod +x "$f"; echo "$f"; }
say() { printf '%s\n' "$*"; }
