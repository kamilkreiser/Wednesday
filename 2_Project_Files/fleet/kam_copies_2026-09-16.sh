#!/bin/bash
# Kam, panel 2026-09-16 18:49:52 (verbatim):
#   "do this then. copy Datasec folder from t9 to dev master. copy secuura folder from dev master to t9.
#    copy Wednesday to t9. sync Tuesday so t9 has all todays changes"
#
# Run sequentially, never in parallel: both legs touch the same two spindles and today already proved
# that concurrency here starves everything else on the machine.
#
# EVERY DIRECTION WAS MEASURED BEFORE THIS FILE WAS WRITTEN, because rsync without --delete still
# OVERWRITES newer files with older ones, and three of these four could have gone the wrong way:
#   Datasec   T9 -> DevMASTER : T9 has 27,769 files changed in 3 days, DevMASTER 0.     his direction ✓
#   Secuura   DevMASTER -> T9 : DevMASTER 8,888 files in 3 days, T9 0.                  his direction ✓
#   Wednesday DevMASTER -> T9 : DevMASTER HEAD ee01911b0 (19:00 today) CONTAINS the T9 HEAD d9d4e726
#                               (2026-09-08) — merge-base --is-ancestor says yes.       his direction ✓
#   Tuesday   *** NOT A COPY *** : the T9's TUESDAY is at 08353b963 (2026-09-15) and DevMASTER's is at
#                               8105f925 (2026-09-08) — THE T9 IS A WEEK NEWER. Copying DevMASTER over
#                               it would push a stale tree onto the current one. And it is unnecessary:
#                               TUESDAY and WEDNESDAY are THE SAME REPO (kamilkreiser/Wednesday.git), so
#                               today's Tuesday fixes are in git. Its tree is CLEAN, so a pull is safe.
#                               Kam asked for an OUTCOME ("so t9 has all todays changes"), not a
#                               direction — this delivers the outcome by the safe means.
#
# NO --delete ANYWHERE. Cleanup means quarantine, and a sync that can delete is a delete with a delay
# (2026-08-26). `-a` preserves modes, which matters: 0600 keys live in these trees (2026-08-25).
#
# EXCLUDED: `worktrees` — throwaway per-PR checkouts, rebuilt from git, and 82.6% of the paths the
# unison scan was walking (measured 18:4x). Kam ruled the same class excludable twice today. Stated to
# him rather than done quietly. node_modules is KEPT so the copies are working trees, not just source.
set -u
LOG=/private/tmp/kam_copies_2026-09-16.log
say() { printf '%s %s\n' "$(date '+%H:%M:%S')" "$*" >> "$LOG"; }
RS=(rsync -a --human-readable --stats --exclude 'worktrees/' --exclude '.DS_Store')

say "START — three copies + one git pull, sequential"

say "[1/4] Datasec: T9 -> DevMASTER"
"${RS[@]}" "/Volumes/KK_T9_External_HDD/!CODING/Datasec/" "/Volumes/DevMASTER/!CODING/Datasec/" >> "$LOG" 2>&1
say "[1/4] rc=$?"

say "[2/4] Secuura: DevMASTER -> T9"
"${RS[@]}" "/Volumes/DevMASTER/!CODING/Secuura/" "/Volumes/KK_T9_External_HDD/!CODING/Secuura/" >> "$LOG" 2>&1
say "[2/4] rc=$?"

# WEDNESDAY measures 136G — and 128G of that is `2_Project_Files/local-model/models`, the ORPHAN ollama
# store found at 18:4x: four models, all four already in the live 269G store the running server actually
# uses (OLLAMA_MODELS read from the process, 13 models served). Copying it would spend 128G of Kam's
# 801G of T9 headroom duplicating a duplicate. Excluded, and said to him rather than done quietly.
# Without it the Wednesday copy is ~8G.
say "[3/4] Wednesday: DevMASTER -> T9 (excluding the 128G orphan model store)"
"${RS[@]}" --exclude '2_Project_Files/local-model/models/' \
  "/Volumes/DevMASTER/WEDNESDAY/" "/Volumes/KK_T9_External_HDD/WEDNESDAY/" >> "$LOG" 2>&1
say "[3/4] rc=$?"

say "[4/4] Tuesday: git pull in the T9 checkout (NOT a copy — see the header)"
git -C /Volumes/KK_T9_External_HDD/TUESDAY pull --rebase >> "$LOG" 2>&1
say "[4/4] rc=$? — HEAD now $(git -C /Volumes/KK_T9_External_HDD/TUESDAY rev-parse --short HEAD 2>/dev/null)"

say "DONE"
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/chat_reply.sh "The four drive jobs have finished. I am verifying the content at the destinations now — exit codes only prove each leg was internally consistent, they do not prove your files arrived — and I will tell you when the T9 is safe to unplug." >> "$LOG" 2>&1
