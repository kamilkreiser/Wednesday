#!/bin/bash
# Kam 2026-09-25 (terminal): "I have formatted the drive. Please sync all the files and folders from DevMaster to this new external drive."
# One-way ADDITIVE copy DevMASTER -> Laptop-DEV (Case-sensitive APFS, encrypted, 2 TB, formatted by Kam today). No --delete anywhere.
# Unlike the 2026-09-21 KK_DEV_Local copy (exFAT-era flags): permissions ARE kept (-a without --no-perms), because
# 3_Access_Keys/ and 4_Credentials/ must stay 0600 on the copy. "All files" = node_modules and the local-model weights INCLUDED;
# only macOS volume bookkeeping is excluded. Everything else, .git and worktrees included.
# AMENDED 2026-09-25 11:4x, Kam: "no Need to sync a local LLM." -> excluded: SYSTEM/ollama (269G, Ollama store), the local-model
# weights (WEDNESDAY 54G; TUESDAY if present) and the Ollama runtime (tools/ollama). tools/media/models (speech, 464M) stays.
SRC=/Volumes/DevMASTER/
DST=/Volumes/Laptop-DEV/
LOG=/Volumes/DevMASTER/WEDNESDAY/5_Project_History/2026-09-25_copy_DevMASTER_to_Laptop-DEV.log
[ -d "$DST" ] || { echo "REFUSED: $DST not mounted" | tee -a "$LOG"; exit 2; }
echo "=== copy start $(date '+%F %T') src=$SRC dst=$DST ===" | tee -a "$LOG"
/opt/homebrew/bin/rsync -a --info=progress2,stats2 \
  --exclude '/.Spotlight-V100' --exclude '/.fseventsd' --exclude '/.Trashes' --exclude '/.TemporaryItems' --exclude '/.DocumentRevisions-V100' \
  --exclude '/SYSTEM/ollama' --exclude '/WEDNESDAY/2_Project_Files/local-model/models' --exclude '/TUESDAY/2_Project_Files/local-model/models' --exclude '/WEDNESDAY/2_Project_Files/tools/ollama' \
  "$SRC" "$DST" >> "$LOG" 2>&1
RC=$?
echo "=== copy done $(date '+%F %T') rc=$RC ===" | tee -a "$LOG"
exit $RC
