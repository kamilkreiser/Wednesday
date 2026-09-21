#!/bin/bash
# launcher_controls_1130_part2.sh — F2: the redone behind=1 control (the drafter's F sed anchored `^1130 ` but that line begins `WANT_COMPARE="` —
# hit 0, the copy equalled the real launcher, rc 0: a mis-designed CONTROL, the launcher was right — drafter slip S7). F2 edits the SECOND compare
# line (`^1131 …`) so the copy expects behind=1 for #1131 and must refuse at exit 10. Optionally re-runs any control names given as arguments by
# re-invoking the main script's logic is NOT done here — the main script is idempotent per control; run it again whole if it was killed.
set -u
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135'
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1130-1135.sh'
C="$(cat "$G/controls_dir_1130.txt")"
OUT="$G/launcher_check_controls.out"
sed 's/^1131 \$MERGE_BASE ahead=1 behind=0 files=1$/1131 $MERGE_BASE ahead=1 behind=1 files=1/' "$L" > "$C/launcher_F2.sh"; chmod 755 "$C/launcher_F2.sh"
echo "F2: launcher copy expecting behind=1 for #1131 (sed hit: $(/usr/bin/grep -c 'behind=1 files=1' "$C/launcher_F2.sh"), real: $(/usr/bin/grep -c 'behind=1 files=1' "$L"))" | tee -a "$OUT"
t0=$(date -u +%H:%M:%SZ); "$C/launcher_F2.sh" --check > "$C/F2_behind1.out" 2>&1; rc=$?; [ "$rc" = 10 ] && v=OK || v=MISMATCH
echo "F2_behind1 rc=$rc want=10 $v ($t0 -> $(date -u +%H:%M:%SZ)) | $(tail -1 "$C/F2_behind1.out" | cut -c1-160)" | tee -a "$OUT"
echo "part2 end $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$OUT"
