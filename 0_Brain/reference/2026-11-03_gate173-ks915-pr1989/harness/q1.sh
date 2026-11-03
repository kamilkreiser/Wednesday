#!/bin/bash
# Q1: gate 166's 28 slip forms (+ its controls) against the head script, both placements, C and UTF-8 locales;
# then gate 166's shell forms. Each cell: completed .env with ADMIN blank (an accepted run WOULD write).
# Prints rc, tree_same, admin_now_set, mode, marker count in output; consumers' reading of the SAME pre-file.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989/harness/lib.sh
TAG=${1:-q1}; LOCALE=${2:-C}
L=$W/runs/$TAG; mkdir -p "$L"
M=gate173rmt; BOM=$'\xef\xbb\xbf'; NB=$'\xc2\xa0'; CR=$'\r'; TAB=$'\t'
source "$W/harness/q1_cases.sh"
G="$(mkclone ${TAG}-golden)" || exit 1
rc=$(run "$G" "$L/golden.log"); echo "golden rc=$rc"
GB="$L/golden_blankadmin.env.bin"
awk 'index($0,"ADMIN_USER_PASSWORD=")==1{print "ADMIN_USER_PASSWORD="; next}{print}' "$G/Blockchain/Dev/.env" | grep -v -E '^(DATABASE_URL|NODE_ENV)=' > "$GB"
LOC=(); [[ "$LOCALE" != C ]] && LOC=("LANG=$LOCALE" "LC_ALL=$LOCALE")
consumers() {  # consumers CLONE PREFILE [VAR=v] -> labels
  local c="$1" f="$2" extra="${3-}" a b d
  a=$(env ${extra:+"$extra"} node "$W/harness/classify.js" dotenv "$NM" "$M" "$f")
  b=$(cd "$W/tmp" && env -i PATH=/usr/bin:/bin ${extra:+"$extra"} bash -c 'set -a; . "$1" >/dev/null 2>&1; printf "%s\0" "${DATABASE_URL-}" "${NODE_ENV-}" "${PGHOST-}" "${PGHOSTADDR-}" "${PGSERVICE-}" "${POSTGRES_HOST-}"' _ "$f" | node "$W/harness/classify.js" bashvals "$NM" "$M")
  d=$(cd "$c/Blockchain/Dev" && env -i PATH="$GPATH" HOME="$W/home" ${extra:+"$extra"} docker compose --env-file "$f" config --format json 2>/dev/null | node "$W/harness/classify.js" compose "$NM" "$M")
  echo "dotenv[$a] bash[$b] compose-dev[$d]"
}
cell() {  # cell ID BODY WHERE [VAR=v]
  local id="$1" body="$2" where="$3"; shift 3
  local c e t0 t1 rc o0 o1
  c="$(mkclone ${TAG}-$id-$where)" || return; e="$c/Blockchain/Dev/.env"
  if [[ $where == prepend ]]; then { printf '%s' "$body"; cat "$GB"; } > "$e"; else { cat "$GB"; printf '%s' "$body"; } > "$e"; fi
  cp "$G/Blockchain/Dev/.env.local" "$c/Blockchain/Dev/.env.local"
  chmod 644 "$e"; cp "$e" "$L/$id-$where.pre.env.bin"; t0=$(treesum "$c"); o0=$(outsidesum)
  rc=$(run "$c" "$L/$id-$where.log" ${LOC[@]+"${LOC[@]}"} "$@")
  t1=$(treesum "$c"); o1=$(outsidesum)
  printf '%-4s %-7s rc=%-2s tree_same=%s outside_same=%s admin_now_set=%s mode=%s marker_in_log=%s | %s %s | %q\n' "$id" "$where" "$rc" \
    "$([[ $t0 == $t1 ]] && echo y || echo N)" "$([[ $o0 == $o1 ]] && echo y || echo N)" "$([[ -n "$(valof "$e" ADMIN_USER_PASSWORD)" ]] && echo y || echo n)" \
    "$(mode "$e")" "$(grep -c "$M" "$L/$id-$where.log")" "$(consumers "$c" "$L/$id-$where.pre.env.bin" "$@")" "$*" "$body"
  printf '      why: %s\n' "$(grep -oE 'refused by [^.]*|cannot check safely: [^.]*' "$L/$id-$where.log" | head -1 | cut -c1-150)"
}
echo "== locale=$LOCALE; gate 166 forms appended to / prepended before a completed .env =="
for ix in "${!IDS[@]}"; do cell "${IDS[$ix]}" "${BODIES[$ix]}" append; cell "${IDS[$ix]}" "${BODIES[$ix]}" prepend; done
echo "== gate 166 shell-side forms =="
cell s01 'NODE_ENV=${GATE_SHELLX}'$'\n' append GATE_SHELLX=production
cell s02 "DATABASE_URL=postgres://u:p@localhost/x\${GATE_SQ}"$'\n' append "GATE_SQ=?host=$M.host"
cell e01 '' append "DATABASE_URL="$'postgres://u:p@localhost/x?ho\tst='"$M.host"
cell e02 '' append "DATABASE_URL="$'postgres://u:p@localhost/x?host\t='"$M.host"
cell e03 '' append "DATABASE_URL="$'postgres://u:p@localhost/x?ho\rst='"$M.host"
echo "== controls: canonical remote/production must be refused AND read remote/production by the consumers =="
cell k91 "DATABASE_URL=postgres://u:p@$M.host/x"$'\n' append
cell k92 'NODE_ENV=production'$'\n' append
echo "== controls: local spellings that must be ACCEPTED =="
cell k01 'NODE_ENV=development'$'\n' append
cell k02 'DATABASE_URL=postgres://u:p@localhost:6432/x'$'\n' append
cell k03 'DATABASE_URL=postgres:///x'$'\n' append
cell k05 'DATABASE_URL=postgres://u:p@pgbouncer:6432/x # pooled'$'\n' append
