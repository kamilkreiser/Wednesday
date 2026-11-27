#!/bin/bash
# lib.sh — QA harness for the nas-backup lane (independent checker, 2026-11-27).
# Runs ONLY a scratch COPY of the lane against FAKE trees under the session scratchpad. Never the real NAS.
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-nasbackup
LANE="${QA_LANE:-$S/copy/WEDNESDAY/2_Project_Files/nas-backup}"
HEREQ="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY=/opt/homebrew/bin/python3
REAL_RSYNC=/opt/homebrew/bin/rsync
case "$S" in /private/tmp/*) ;; *) echo "lib: scratch not under /private/tmp" >&2; exit 2;; esac
T=""
at() { "$PY" -c 'import datetime,sys; d=datetime.datetime(2026,12,1)+datetime.timedelta(days=int(sys.argv[1])); print(int(d.replace(hour=int(sys.argv[2]),minute=int(sys.argv[3])).timestamp()))' "$1" "$2" "$3"; }
write_conf() { # extra lines on stdin-free args: each arg is one conf line appended
  { echo "status=${CONF_STATUS:-confirmed}"; echo "source_volume=$T/vol"; echo "nas_root=$T/nas"; echo "fire=00:30"; echo "window_hours=5"
    echo "late_fire=refuse"; echo "min_free_gib=200"; echo "max_seconds=600"; echo "stall_seconds=900"; echo "hash_sample=10"
    echo "rsync=${CONF_RSYNC:-$REAL_RSYNC}"
    echo "set=General|WEDNESDAY|$T/vol/WEDNESDAY"; echo "set=Secuura|Secuura|$T/vol/CODING/Secuura"
    for l in "$@"; do echo "$l"; done
  } > "$T/lane/seats/wednesday.conf"
}
write_mounts() { { echo "/dev/disk9s1 on $T/vol (apfs, local, nodev, nosuid, journaled, noowners)"
  [ "${1:-smbfs}" = "none" ] || echo "//user@nas.example/DEV-Working on $T/nas (smbfs, nodev, nosuid, mounted by tester)"; } > "$T/mount.txt"; }
fixture() { # name  -> fresh fixture dir (suffix with pid so reruns never collide)
  T="$S/fx/$1_$$"
  mkdir -p "$T/vol/WEDNESDAY/sub" "$T/vol/CODING/Secuura/Blockchain/src" "$T/nas/Secuura" "$T/nas/General" "$T/nas/Datasec" "$T/lane/seats" "$T/stub" "$T/out"
  echo "old content of a" > "$T/vol/WEDNESDAY/a.txt"; echo "b" > "$T/vol/WEDNESDAY/sub/b.txt"
  echo "console.log(1)" > "$T/vol/CODING/Secuura/Blockchain/src/app.js"
  echo 5000 > "$T/free_gib.txt"; CONF_STATUS=confirmed; CONF_RSYNC=""; write_conf; write_mounts
}
nb()      { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup.sh" "$@"; }
nightly() { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup_nightly.sh" "$@"; }
watch()   { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup_watch.sh" "$@"; }
CUR() { echo "$T/nas/General/Wednesday/nightly-backup/current/WEDNESDAY"; }
VER() { echo "$T/nas/General/Wednesday/nightly-backup/versions"; }
state() { "$PY" -c 'import json,sys
d=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."):
    d = d.get(k) if isinstance(d, dict) else None
print(d)' "$T/lane/state/wednesday.json" "$1" 2>&1; }
# the destruction oracle: every content hash present under <nas> before must still be present after
snap() { "$PY" "$HEREQ/oracle.py" snap "$T/nas" "$T/snap_$1.json"; }
lost() { "$PY" "$HEREQ/oracle.py" lost "$T/nas" "$T/snap_$1.json"; }   # prints LOST lines; rc 1 if anything lost
say() { printf '%s\n' "$*"; }
verdict() { # label expected actual
  if [ "$2" = "$3" ]; then printf 'HELD   %s (expected %s, got %s)\n' "$1" "$2" "$3"; else printf 'BROKE  %s (expected %s, got %s)\n' "$1" "$2" "$3"; fi; }
