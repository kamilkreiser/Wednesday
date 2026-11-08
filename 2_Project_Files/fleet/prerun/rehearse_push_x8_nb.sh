#!/bin/bash
# LINEAGE (Seat X 7th, 2026-11-06): re-keyed from Seat V 24th's rehearse_push_v24_nb.sh (sha256 8d292b28...) by tools/rekey_push_x7.py: RECORD and CELLS arguments passed to the driver. Modes dryrun and gatetest only.
# LINEAGE (Seat V 24th, 2026-11-06): re-keyed from Seat V 23rd's rehearse_push_v23_nb.sh by COUNT-ASSERTED token pairs (tools/rekey_push_v24.py); gate logic unchanged; two path-value deviations declared in evidence/declared_changes_push.md.
# LINEAGE (Seat V 24th, 2026-11-06 ~13:55 AEDT): TMPDIR changed from <record folder>/evidence/tmp_v24 to /private/tmp/v24t (count-asserted: 4). The long path made tsx's IPC socket path 121 bytes, over macOS's 104-byte sun_path limit, so leg 1 of the real pre-push hook failed (the KS-1509 push, 02:53Z, rehearsal skips the hook so could not see it). The family's own short convention is restored.
# LINEAGE (Seat V 23rd, 2026-11-05): re-keyed from Seat V 22nd's rehearse_push_v22_nb.sh by COUNT-ASSERTED token pairs (tools/rekey_push_v23.py). Logic unchanged.
# LINEAGE (Seat V 22nd, 2026-11-05): re-keyed from Seat V 21st's rehearse_push_v21_nb.sh by COUNT-ASSERTED token pairs (tools/rekey_push_v22.py). Logic unchanged.
# Seat X 8th: rehearse pushlock_x8_newbranch_v3.sh against SCRATCH lock/queue dirs only (the real ones are never named). Modes: dryrun, gatetest (both stop before any push).
# usage: rehearse_push_x8_nb.sh WORKTREE BRANCH HEAD BASE PATHSFILE OTHER_PATHSFILE RECORD CELLS OUTROOT SEATNAME
set -u
WT="$1"; BR="$2"; HEAD="$3"; BASE="$4"; PATHS="$5"; OTHER="$6"; RECORD="$7"; CELLS="$8"; ROOT="$9"; SEAT="${10}"
B=/Volumes/DevMASTER/!CODING/Secuura/Blockchain
case "$0" in /*) ;; *) echo "invoke by ABSOLUTE path (no cd)" >&2; exit 64 ;; esac
D="$(dirname "$0")/pushlock_x8_newbranch_v3.sh"
QTOOL=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/push_queue.sh
KEY=$B/3_Access_Keys/github_deploy_rw
S=/private/tmp/prt/scratch_nb
mkdir -p "$S" "$ROOT"
case "$S" in /private/tmp/prt/*) ;; *) echo "refusing: scratch path is not under /private/tmp/prt"; exit 64 ;; esac
run() {  # name mode expect pathsfile
  name="$1"; mode="$2"; expect="$3"; pf="$4"
  out="$ROOT/$name"; lock="$S/lock_$name"; q="$S/queue_$name"; mkdir -p "$q"
  X8_NETMAX=5 TMPDIR=/private/tmp/prt bash "$D" "$WT" "$BR" "$expect" "$BASE" "$out" "$lock" "$q" "$QTOOL" 60 30 "$mode" "$KEY" "$pf" "$RECORD" "$CELLS" "$SEAT" > "$out.stdout" 2>&1
  rc=$?
  echo "=== $name (mode=$mode) rc=$rc | lock dir left behind: $([ -d "$lock" ] && echo YES || echo no) | queue files left: $(ls -1 "$q" 2>/dev/null | wc -l | tr -d ' ')"
  /usr/bin/grep -E 'PRECHECK FAIL|GATE FAIL|precheck ok|gate ok|gatetest|dryrun|released|queue leave' "$out/status.txt" | cut -c1-300
}
run n1_dryrun dryrun "$HEAD" "$PATHS"
run n2_gatetest_pass gatetest "$HEAD" "$PATHS"
run n3_wrong_head gatetest "$BASE" "$PATHS"
run n4_overlap_fires gatetest "$HEAD" "$OTHER"
