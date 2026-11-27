#!/bin/bash
# Z9 — sha256 of every file of the lane and of both earlier checkers' folders, and the top-level listing of the two NAS mounts
# named in the commission, AFTER the check; compared with the lists taken at 19:41 before anything else was done.
Q=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/qa-checks/nasbackup-r3; L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup
date
( find $L -type f -print0 | sort -z | xargs -0 shasum -a 256 ) > $Q/raw/99_hash_lane_after.txt 2> $Q/raw/99_hash_lane_after.err
( find "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-nasbackup-r2" "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-nasbackup" -type f -print0 | sort -z | xargs -0 shasum -a 256 ) > $Q/raw/99_hash_checkers_after.txt 2> $Q/raw/99_hash_checkers_after.err
for m in /Volumes/Backup /Volumes/DEV-Working; do echo "== $m"; ls -la "$m" 2>&1; done > $Q/raw/99_nas_toplevel_after.txt 2>&1
echo "lane: $(wc -l < $Q/raw/00_hash_lane_before.txt | tr -d ' ') files before, $(wc -l < $Q/raw/99_hash_lane_after.txt | tr -d ' ') after; differing lines:"; diff $Q/raw/00_hash_lane_before.txt $Q/raw/99_hash_lane_after.txt; echo "  diff rc=$?"
echo "earlier checkers' folders: $(wc -l < $Q/raw/00_hash_checkers_before.txt | tr -d ' ') files before, $(wc -l < $Q/raw/99_hash_checkers_after.txt | tr -d ' ') after; differing lines:"; diff $Q/raw/00_hash_checkers_before.txt $Q/raw/99_hash_checkers_after.txt; echo "  diff rc=$?"
echo "NAS top-level listings ($(wc -l < $Q/raw/00_nas_toplevel_before.txt | tr -d ' ') lines): differing lines:"; diff $Q/raw/00_nas_toplevel_before.txt $Q/raw/99_nas_toplevel_after.txt; echo "  diff rc=$?"
echo "CAN-FAIL control: the same diff against a copy with one line changed:"; sed '3s/.$/X/' $Q/raw/00_hash_lane_before.txt > /private/tmp/qa3nb/hash_control.txt; diff -q $Q/raw/00_hash_lane_before.txt /private/tmp/qa3nb/hash_control.txt; echo "  diff rc=$? (1 = it can tell)"
echo "stderr of the hashing: $(cat $Q/raw/99_hash_lane_after.err $Q/raw/99_hash_checkers_after.err | wc -l | tr -d ' ') lines"
echo "disk images of mine still mounted: $(mount | /usr/bin/grep -c qa3nb) ; processes of mine still running under the scratch: $(pgrep -f /private/tmp/qa3nb | wc -l | tr -d ' ')"
git -C /Volumes/DevMASTER/WEDNESDAY status --porcelain 2>&1 | /usr/bin/grep -i -E 'nas-backup|qa-checks|qa-nasbackup' | cut -c1-120
