#!/bin/bash
# Drive each surviving mutant (and head) on a form chosen to separate them. rc + admin_now_set only.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/harness/lib.sh
source $W/harness/cells.sh
L=$W/runs/q4b; mkdir -p $L $W/tmp/q4b; RUNTMP=$W/tmp/q4b; M=gate174rmt; N=$'\n'
GB=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
drive() {  # drive MUTANT_ID FORM_ID DEV_BODY ROOT LOCAL [VAR=v]
  local mid="$1" fid="$2"; shift 2
  for who in head "$mid"; do
    local src=$R/Blockchain/Dev/scripts/restore-local-secrets.sh; [[ $who != head ]] && src=$W/mut/$who.sh
    TAG="q4b-${mid%%_*}-$fid-$who" SCRIPT_SRC=$src NOCONS=1 gcell "x" "$@" | head -1 | awk -v w="$who" -v f="$fid" '{print f, w, $2, $6, $7}'
  done
}
while IFS='|' read -r mid fid dev root local var; do
  [[ -z "$mid" || "$mid" == \#* ]] && continue
  dev=${dev//\\n/$N}; root=${root//\\n/$N}; local=${local//\\n/$N}
  if [[ -n "$var" ]]; then drive "$mid" "$fid" "$dev" "$root" "$local" "$var"; else drive "$mid" "$fid" "$dev" "$root" "$local"; fi
done < $W/harness/q4b_forms.txt
