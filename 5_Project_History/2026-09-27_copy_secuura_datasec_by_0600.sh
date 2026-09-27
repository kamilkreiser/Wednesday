#!/bin/bash
# 2026-09-27 21:5x (Wednesday). Kam, live board 21:48: "I need to unplug at 6am. I will wait for it to be done properly.
# Sync Secuura and then do the same for Datasec. As the drive already has a copy, a check of whats changed would be good and
# only sync whats required". rsync -a already copies only files whose size/mtime differ (a delta sync). Added: the seats'
# regenerable worktree node_modules are excluded (Seat B 34th measured them as the machine-load driver). NO full pass after.
LOG=/Volumes/DevMASTER/WEDNESDAY/5_Project_History/2026-09-25_copy_DevMASTER_to_Laptop-DEV.log
DST=/Volumes/Laptop-DEV/
[ -d "$DST" ] || { echo "REFUSED: $DST not mounted" | tee -a "$LOG"; exit 2; }
for P in '!CODING/Secuura' '!CODING/Datasec'; do
  echo "=== DELTA $P start $(date '+%F %T') ===" | tee -a "$LOG"
  /opt/homebrew/bin/rsync -a --relative --info=stats2 \
    --exclude-from='/Volumes/DevMASTER/WEDNESDAY/5_Project_History/2026-09-27_copy_excludes_scratch_clones.txt' \
    --exclude 'worktrees/*/**/node_modules' \
    --exclude '/.Spotlight-V100' --exclude '/.fseventsd' --exclude '/.Trashes' --exclude '/.TemporaryItems' --exclude '/.DocumentRevisions-V100' \
    --exclude '/!CODING/Docker - Containers/DockerDesktop/Docker.raw' \
    "/Volumes/DevMASTER/./$P" "$DST" >> "$LOG" 2>&1
  RC=$?
  echo "=== DELTA $P done $(date '+%F %T') rc=$RC ===" | tee -a "$LOG"
done
echo "=== DELTA Secuura+Datasec complete $(date '+%F %T') ===" | tee -a "$LOG"
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/chat_reply.sh --project WED "Laptop drive: the Secuura and Datasec sync has FINISHED. The log shows each folder's result. The drive stays mounted until the scheduled 05:40 eject, or say unplug and I will eject it now." >/dev/null 2>&1
