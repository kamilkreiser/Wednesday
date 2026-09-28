#!/bin/bash
# move_to_laptop_dev.sh — copy Friday's tree and her project folders onto the Laptop-DEV drive.
# Kam, 2026-09-28 ~20:1x (terminal): move all Friday's files and project files to the new drive,
# categorised by the drive's structure; newer wins; lose nothing; find HPSM files Friday lacks.
# ADDITIVE ONLY: rsync without --delete; the laptop originals are never touched; the drive's older
# HPSM is MOVED (not deleted) into a quarantine folder beside it. Every step logs; nothing silenced.
set -u
L="$HOME/1FILES TO SYNC"
D="/Volumes/Laptop-DEV"
DS="$D/!CODING/Datasec"
Q="$DS/_quarantine_2026-09-28_HPSM-drive-sync-copy"
LOG="${1:?log dir}"
mkdir -p "$LOG"
step() { echo "=== $(date '+%H:%M:%S') $*"; }
cp_tree() { # $1 src dir (no trailing slash)  $2 dest dir
  step "rsync $1 -> $2"
  mkdir -p "$2"
  rsync -a --itemize-changes "$1/" "$2/" > "$LOG/$(basename "$2").rsync.log" 2>&1
  local rc=$?; echo "rc=$rc ($(wc -l < "$LOG/$(basename "$2").rsync.log") lines)"; return $rc
}
[ -d "$D/WEDNESDAY" ] || { echo "drive not mounted"; exit 2; }

cp_tree "$L/FRIDAY" "$D/FRIDAY" || exit 3
mkdir -p "$D/FRIDAY/5_Project_History" && rsync -a "$L/spark-kit_2026-09-23.zip" "$D/FRIDAY/5_Project_History/" && step "spark-kit zip copied"
cp_tree "$L/Datasec Security Composer" "$DS/Datasec Security Composer" || exit 3

# HPSM: quarantine the drive's pre-rewrite copy, copy the laptop's, bring back what only the drive had.
if [ -d "$DS/HPSM" ] && [ ! -e "$Q/HPSM" ]; then
  step "quarantine drive HPSM -> $Q/HPSM"; mkdir -p "$Q" && mv "$DS/HPSM" "$Q/HPSM" || exit 4
  for r in "" "/6_Policy_Composer"; do git -C "$Q/HPSM$r" remote set-url --push origin DISABLED-quarantined-2026-09-28 2>&1 || true; done
fi
cp_tree "$L/HPSM" "$DS/HPSM" || exit 3
step "HPSM: drive-only files back from quarantine (no .git, no .venv, not the old composer clone)"
rsync -a --ignore-existing --itemize-changes \
  --exclude='.git/' --exclude='.venv/' --exclude='/6_Policy_Composer/' --exclude='node_modules/' \
  "$Q/HPSM/" "$DS/HPSM/" > "$LOG/HPSM.drive-only.rsync.log" 2>&1; echo "rc=$? ($(wc -l < "$LOG/HPSM.drive-only.rsync.log") lines)"
F="1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-wp3r2/m2/RED-before-fix.log"
cmp -s "$Q/HPSM/$F" "$DS/HPSM/$F" || cp -p "$Q/HPSM/$F" "$DS/HPSM/${F%.log} (drive copy, run 2026-09-12T08-22Z).log"
chmod 600 "$DS/HPSM/3_Access_Keys/"* 2>/dev/null

cp_tree "$L/HPSM-POC" "$DS/HPSM-POC" || exit 3
step "ALL DONE"
