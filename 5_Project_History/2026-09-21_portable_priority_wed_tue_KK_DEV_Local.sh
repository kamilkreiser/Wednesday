#!/bin/bash
# Kam 2026-09-21 18:5x: "I'd like to unplug ... your folder, and Tuesday's folder. Can you make sure those two are there?"
# A PARALLEL, targeted, ADDITIVE copy of WEDNESDAY and TUESDAY (the main blind copy is alphabetical and had only created the
# empty dirs). Same flags/excludes as the blind copy; NO --delete; the main run later skips what is already present.
LOG=/Volumes/DevMASTER/WEDNESDAY/5_Project_History/2026-09-21_portable_priority_wed_tue_KK_DEV_Local.log
echo "=== priority copy start $(date '+%F %T') ===" | tee -a "$LOG"
RC=0
for D in TUESDAY WEDNESDAY; do
  echo "--- $D $(date '+%T') ---" | tee -a "$LOG"
  rsync -a --no-perms --no-owner --no-group --info=progress2,stats2 \
    --exclude 'node_modules' --exclude '.DS_Store' --exclude '.Spotlight-V100' --exclude '.fseventsd' --exclude '.Trashes' \
    --exclude '2_Project_Files/local-model/models' \
    "/Volumes/DevMASTER/$D/" "/Volumes/KK_DEV_Local/$D/" 2>&1 | tee -a "$LOG"
  r=${PIPESTATUS[0]}; [ "$r" -ne 0 ] && RC=$r
  echo "--- $D done $(date '+%T') rc=$r ---" | tee -a "$LOG"
done
echo "=== priority copy done $(date '+%F %T') rc=$RC ===" | tee -a "$LOG"
exit $RC
