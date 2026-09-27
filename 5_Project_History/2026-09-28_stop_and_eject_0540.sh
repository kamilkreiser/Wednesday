#!/bin/bash
# Kam: unplug at 06:00 on 2026-09-28. At 05:40 stop any copy cleanly (SIGTERM, rsync is restartable), eject Laptop-DEV,
# and post the result to the live board. Detached (nohup) so it survives a Wednesday seat rotation.
LOG=/Volumes/DevMASTER/WEDNESDAY/5_Project_History/2026-09-25_copy_DevMASTER_to_Laptop-DEV.log
TARGET=$(date -j -f '%Y-%m-%d %H:%M' '2026-09-28 05:40' +%s)
while [ "$(date +%s)" -lt "$TARGET" ]; do sleep 30; done
pkill -TERM -f 'copy_secuura_datasec_by_0600.sh'; pkill -TERM -f 'copy_priority_then_full.sh'; pkill -TERM -f 'copy_DevMASTER_to_Laptop-DEV.sh'; pkill -TERM -f 'rsync.*Laptop-DEV'
for i in $(seq 1 24); do pgrep -f 'rsync.*Laptop-DEV' >/dev/null || break; sleep 5; done
STILL=$(pgrep -f 'rsync.*Laptop-DEV' | wc -l | tr -d ' ')
DONE=$(tail -c 50000 "$LOG" | tr '\r' '\n' | grep -a -E '=== (PRIORITY|DELTA) .* done' | sed 's/^=== //; s/ ===$//' | tail -8 | tr '\n' ';')
echo "=== 05:40 STOP $(date '+%F %T') rsync still running: $STILL ===" | tee -a "$LOG"
diskutil eject /Volumes/Laptop-DEV >> "$LOG" 2>&1; ERC=$?
echo "=== eject rc=$ERC ===" | tee -a "$LOG"
if [ "$ERC" = 0 ]; then MSG="Laptop drive EJECTED at $(date +%H:%M); it is safe to unplug. Completed folders: $DONE"; else MSG="Laptop drive did NOT eject (rc $ERC; rsync still running: $STILL). Do not pull it yet. Completed folders: $DONE"; fi
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/chat_reply.sh --project WED "$MSG" >> "$LOG" 2>&1
