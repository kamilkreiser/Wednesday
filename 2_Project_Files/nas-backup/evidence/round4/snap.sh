#!/bin/bash
# snap.sh <dest dir> : a snapshot of the lane's code and tests OUTSIDE the git work tree, in a WEDNESDAY-named tree,
# so that another session's git commit (which briefly swaps work-tree files for the committed ones) cannot change
# what a suite or mutant run executes. Verified: every copy equals the lane's file, read twice, 2 s apart, and the
# engine is not round 3's.
set -u
LANE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup; TREE=/Volumes/DevMASTER/WEDNESDAY
c="$1/WEDNESDAY/2_Project_Files"
mkdir -p "$c/nas-backup/tests" "$c/nas-backup/proposed" "$c/nas-backup/jobs" "$c/fleet/cockpit" "$c/tools" || exit 2
FILES="nb_core.py nb_common.sh nas_backup.sh nas_backup_nightly.sh nas_backup_watch.sh tests/run.sh tests/mutants.sh tests/scan_dry_lists.py proposed/doctor_nasbackup_block.sh jobs/nasbackup.plist.template"
try=0
while :; do
  try=$((try+1)); [ "$try" -le 5 ] || { echo "snap: could not get a stable copy in 5 tries" >&2; exit 1; }
  for f in $FILES; do cp "$LANE/$f" "$c/nas-backup/$f" || exit 2; done
  cp "$TREE/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$c/fleet/cockpit/"; cp "$TREE/2_Project_Files/tools/seat_note.sh" "$c/tools/"
  /opt/homebrew/bin/python3 -c 'import time; time.sleep(2)'
  bad=0
  for f in $FILES; do cmp -s "$LANE/$f" "$c/nas-backup/$f" || { bad=1; echo "snap: $f changed between the copy and the re-read (try $try)" >&2; }; done
  [ "$(shasum -a 256 < "$c/nas-backup/nb_core.py" | cut -c1-64)" != "$(shasum -a 256 < "$LANE/round3/nb_core.py.round3" | cut -c1-64)" ] || { bad=1; echo "snap: the engine copied is ROUND 3's (try $try)" >&2; }
  /usr/bin/grep -q -F 'stopped in set %s before chunk' "$c/nas-backup/nb_core.py" || { bad=1; echo "snap: the engine copied lacks the round 4 marker (try $try)" >&2; }
  /usr/bin/grep -q -F 'esc_g' "$c/nas-backup/tests/run.sh" || { bad=1; echo "snap: the suite copied lacks the round 4 cells (try $try)" >&2; }
  [ "$bad" -eq 0 ] && break
done
( for f in $FILES; do shasum -a 256 "$c/nas-backup/$f"; done ) | sed "s|$1/||" > "$1/sha256_of_the_snapshot.txt"
echo "$c/nas-backup"
