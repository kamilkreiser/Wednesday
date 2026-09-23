#!/bin/bash
# repin_controls_gate20T1.sh <launcher> <scratchpad> — controls for repin_and_launch_gate20T1.sh, ALL in --dry-run (it stops before the usage gate,
# --check and cockpit.sh add: nothing is launched), each on a launcher COPY under the scratchpad except the positive:
# R1 POSITIVE dry run on the real launcher -> 0 · R2 a STALE HEAD pinned for the last row (#1212's last hex changed) -> 11 · R3 the KS-1143 row removed
# -> 8 · R4 CONTROL_COPY=1 -> 8 · R5 the launcher's pinned launch develop set to BASE (a develop that has since moved) -> 10 (the real run re-pins there).
set -u
L="$1"; SP="$2"
case "$SP" in /private/tmp/claude-501/*/scratchpad*) ;; *) echo "REFUSING: not a scratchpad"; exit 9;; esac
R='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T1_seatB/repin_and_launch_gate20T1.sh'
D="$(mktemp -d "$SP/repin_ctrl.XXXXXX")"; ok=0; bad=0
run() { name="$1"; want="$2"; shift 2; "$@" > "$D/$name.out" 2>&1; rc=$?; [ "$rc" = "$want" ] && { echo "OK   $name rc $rc (want $want)"; ok=$((ok+1)); } || { echo "MISMATCH $name rc $rc (want $want) — $D/$name.out"; bad=$((bad+1)); }; tail -2 "$D/$name.out" | sed 's/^/     /'; }
echo "repin controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $D"
run R1_positive_dry_run 0 bash "$R" "$L" "$SP" --dry-run
LASTH="$(sed -n 's/^  "1212|KS-1143|[^|]*|\([0-9a-f]\{40\}\)|1"$/\1/p' "$L")"; STALE="${LASTH%?}$( [ "${LASTH: -1}" = 0 ] && echo 1 || echo 0 )"
sed "s/$LASTH/$STALE/" "$L" > "$D/L_stale.sh"; chmod 755 "$D/L_stale.sh"; echo "  (R2 copy: #1212 pinned $STALE instead of $LASTH; PRS rows carrying the stale head $(/usr/bin/grep -c "^  \"1212|KS-1143|.*|$STALE|1\"$" "$D/L_stale.sh") — must be 1; the BOTH-list copy of the head is altered too and is never reached)"
run R2_stale_head_1212 11 bash "$R" "$D/L_stale.sh" "$SP" --dry-run
/usr/bin/grep -v -E '^  "1212\|KS-1143\|' "$L" > "$D/L_no11.sh"; chmod 755 "$D/L_no11.sh"
run R3_ks1143_row_removed 8 bash "$R" "$D/L_no11.sh" "$SP" --dry-run
sed 's/^CONTROL_COPY=0$/CONTROL_COPY=1/' "$L" > "$D/L_cc.sh"; chmod 755 "$D/L_cc.sh"
run R4_control_copy 8 bash "$R" "$D/L_cc.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='[0-9a-f]*'/DEVELOP_SHA='2bc5ccf63b8c40911afb568b03cace066238ffcf'/" "$L" > "$D/L_devstale.sh"; chmod 755 "$D/L_devstale.sh"
run R5_pinned_develop_stale 10 bash "$R" "$D/L_devstale.sh" "$SP" --dry-run
echo "repin controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH"
[ "$bad" -eq 0 ]
