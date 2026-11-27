#!/bin/bash
# mkcopy.sh <dest dir> <nb_core.py to use> : a scratch copy of the lane in a WEDNESDAY-named tree (as tests/mutants.sh does)
set -u
LANE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup; TREE=/Volumes/DevMASTER/WEDNESDAY
c="$1/WEDNESDAY/2_Project_Files"
mkdir -p "$c/nas-backup/tests" "$c/nas-backup/proposed" "$c/nas-backup/jobs" "$c/fleet/cockpit" "$c/tools" "$1/base"
cp "$LANE/nb_common.sh" "$LANE/nas_backup.sh" "$LANE/nas_backup_nightly.sh" "$LANE/nas_backup_watch.sh" "$c/nas-backup/"
cp "$2" "$c/nas-backup/nb_core.py"
cp "$LANE/tests/run.sh" "$LANE/tests/scan_dry_lists.py" "$c/nas-backup/tests/"; cp "$LANE/proposed/doctor_nasbackup_block.sh" "$c/nas-backup/proposed/"
cp "$LANE/jobs/nasbackup.plist.template" "$c/nas-backup/jobs/"
cp "$TREE/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$c/fleet/cockpit/"; cp "$TREE/2_Project_Files/tools/seat_note.sh" "$c/tools/"
echo "$c/nas-backup"
