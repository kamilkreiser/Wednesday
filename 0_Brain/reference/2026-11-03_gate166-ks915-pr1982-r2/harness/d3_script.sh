#!/bin/bash
# D3: does the script at head REFUSE each new spelling (d3_cases.sh) the consumers read as remote/production?
# Each case's body is placed in a completed .env with ADMIN blank (so any accepted run WOULD write).
# Prints rc, tree_same, admin_now_set, mode; never a value.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2/harness/lib.sh
TAG=${1:-d3}; LOCALE=${2:-C}
L=$W/runs/$TAG; mkdir -p "$L"
M=gate166rmt
BOM=$'\xef\xbb\xbf'; NB=$'\xc2\xa0'; CR=$'\r'; TAB=$'\t'
source "$W/harness/d3_cases.sh"
G="$(mkclone ${TAG}-golden)" || exit 1
rc=$(run "$G" "$L/golden.log"); echo "golden rc=$rc"
GB="$L/golden_blankadmin.env.bin"
awk 'index($0,"ADMIN_USER_PASSWORD=")==1{print "ADMIN_USER_PASSWORD="; next}{print}' "$G/Blockchain/Dev/.env" \
  | grep -v -E '^(DATABASE_URL|NODE_ENV)=' > "$GB"
LOC=(); [[ "$LOCALE" != C ]] && LOC=("LANG=$LOCALE" "LC_ALL=$LOCALE")
cell() {  # cell ID BODY WHERE(append|prepend) [VAR=v ...]
  local id="$1" body="$2" where="$3"; shift 3
  local c e t0 t1 rc
  c="$(mkclone ${TAG}-$id-$where)" || return; e="$c/Blockchain/Dev/.env"
  if [[ $where == prepend ]]; then { printf '%s' "$body"; cat "$GB"; } > "$e"; else { cat "$GB"; printf '%s' "$body"; } > "$e"; fi
  chmod 644 "$e"; t0=$(treesum "$c")
  rc=$(run "$c" "$L/$id-$where.log" ${LOC[@]+"${LOC[@]}"} "$@")
  t1=$(treesum "$c")
  printf '%-4s %-7s rc=%-2s tree_same=%s admin_now_set=%s mode=%s marker_in_log=%s %s | %q\n' "$id" "$where" "$rc" \
    "$([[ $t0 == $t1 ]] && echo y || echo N)" "$([[ -n "$(valof "$e" ADMIN_USER_PASSWORD)" ]] && echo y || echo n)" \
    "$(mode "$e")" "$(grep -c "$M" "$L/$id-$where.log")" "$*" "$body"
}
echo "== locale=$LOCALE; each case APPENDED to a completed .env (key lines stripped), and PREPENDED (first line) =="
for ix in "${!IDS[@]}"; do
  cell "${IDS[$ix]}" "${BODIES[$ix]}" append
  cell "${IDS[$ix]}" "${BODIES[$ix]}" prepend
done
echo "== shell-side interpolation source: shell GATE_SHELLX=production, .env NODE_ENV=\${GATE_SHELLX} =="
cell s01 'NODE_ENV=${GATE_SHELLX}'$'\n' append GATE_SHELLX=production
cell s02 "DATABASE_URL=postgres://u:p@localhost/x\${GATE_SQ}"$'\n' append "GATE_SQ=?host=$M.host"
echo "== controls: local spellings that must still be ACCEPTED =="
cell k01 'NODE_ENV=development'$'\n' append
cell k02 'DATABASE_URL=postgres://u:p@localhost:6432/x'$'\n' append
cell k03 'DATABASE_URL=postgres:///x'$'\n' append
cell k04 'DATABASE_URL=postgres:///x?host=/tmp'$'\n' append
