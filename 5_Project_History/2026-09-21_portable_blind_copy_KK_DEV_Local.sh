#!/bin/bash
# Kam 2026-09-21 16:2x: "There's nothing on that drive, so just copy everything blindly."
# One-way ADDITIVE copy DevMASTER -> KK_DEV_Local. No --delete anywhere. Excludes: node_modules (Kam 15:48 "skip node_modules"),
# the local-model weights (his devnas.prf ignores them; 20+ GB of Ollama blobs), and macOS volume junk. Everything else, .git and worktrees included.
SRC=/Volumes/DevMASTER/
DST=/Volumes/KK_DEV_Local/
LOG=/Volumes/DevMASTER/WEDNESDAY/5_Project_History/2026-09-21_portable_blind_copy_KK_DEV_Local.log
echo "=== blind copy start $(date '+%F %T') src=$SRC dst=$DST ===" | tee -a "$LOG"
rsync -a --no-perms --no-owner --no-group --info=progress2,stats2 \
  --exclude 'node_modules' --exclude '.Spotlight-V100' --exclude '.fseventsd' --exclude '.Trashes' --exclude '.TemporaryItems' --exclude '.DS_Store' --exclude '.DocumentRevisions-V100' \
  --exclude 'WEDNESDAY/2_Project_Files/local-model/models' --exclude 'TUESDAY/2_Project_Files/local-model/models' \
  "$SRC" "$DST" 2>&1 | tee -a "$LOG"
RC=${PIPESTATUS[0]}
echo "=== blind copy done $(date '+%F %T') rc=$RC ===" | tee -a "$LOG"
exit $RC
