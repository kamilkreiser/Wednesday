#!/bin/bash
# 2026-09-27 17:1x (Wednesday day seat). Kam, live board 17:12: "how is the Laptop external drive looking. I leave first thing
# tomorrow and would like to unplug tonight". The full additive pass walks ~38M small files and will not finish tonight, so the
# folders he works from go FIRST (same flags + the proven exclude list; --relative keeps the anchored excludes valid), then the
# full pass resumes. Additive only: no --delete anywhere. Stop cleanly (SIGTERM) before unplugging; rsync is restartable.
LOG=/Volumes/DevMASTER/WEDNESDAY/5_Project_History/2026-09-25_copy_DevMASTER_to_Laptop-DEV.log
DST=/Volumes/Laptop-DEV/
[ -d "$DST" ] || { echo "REFUSED: $DST not mounted" | tee -a "$LOG"; exit 2; }
for P in 'WEDNESDAY' 'TUESDAY' 'Notes (MASTER)' '!CODING/Secuura' '!CODING/Datasec'; do
  echo "=== PRIORITY $P start $(date '+%F %T') ===" | tee -a "$LOG"
  /opt/homebrew/bin/rsync -a --relative --info=stats2 \
    --exclude-from='/Volumes/DevMASTER/WEDNESDAY/5_Project_History/2026-09-27_copy_excludes_scratch_clones.txt' \
    --exclude '/.Spotlight-V100' --exclude '/.fseventsd' --exclude '/.Trashes' --exclude '/.TemporaryItems' --exclude '/.DocumentRevisions-V100' \
    --exclude '/!CODING/Docker - Containers/DockerDesktop/Docker.raw' --exclude '/SYSTEM/ollama' --exclude '/WEDNESDAY/2_Project_Files/local-model/models' \
    --exclude '/TUESDAY/2_Project_Files/local-model/models' --exclude '/WEDNESDAY/2_Project_Files/tools/ollama' \
    "/Volumes/DevMASTER/./$P" "$DST" >> "$LOG" 2>&1
  echo "=== PRIORITY $P done $(date '+%F %T') rc=$? ===" | tee -a "$LOG"
done
echo "=== priority folders complete; full pass follows ===" | tee -a "$LOG"
exec /bin/bash /Volumes/DevMASTER/WEDNESDAY/5_Project_History/2026-09-25_copy_DevMASTER_to_Laptop-DEV.sh
