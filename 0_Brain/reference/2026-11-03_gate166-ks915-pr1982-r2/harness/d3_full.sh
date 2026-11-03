#!/bin/bash
# D3 confirmation: the consumers read the WHOLE .env exactly as d3_script.sh built it (completed .env with key
# lines stripped + the case body), plus the REAL Blockchain/Dev/docker-compose.yml (api-gateway's NODE_ENV is
# ${NODE_ENV:-development} from .env). Files hold generated values, so they live as runs/**/*.bin (ignored);
# only classifications are printed.
set -uo pipefail
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2
NM="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules"
M=gate166rmt; BOM=$'\xef\xbb\xbf'; NB=$'\xc2\xa0'; CR=$'\r'; TAB=$'\t'
source "$W/harness/d3_cases.sh"
GB=$W/runs/d3C/golden_blankadmin.env.bin
D=$W/runs/d3full; mkdir -p "$D" "$W/scratch/chome" "$W/scratch/realcompose"
cp "$W/repo/Blockchain/Dev/docker-compose.yml" "$W/scratch/realcompose/docker-compose.yml"
printf 'services:\n  probe:\n    image: busybox\n    environment:\n      - DATABASE_URL=${DATABASE_URL:-}\n      - NODE_ENV=${NODE_ENV:-development}\n' > "$D/probe.yml"
dbcls() { local u="$1" h; [[ -z "$u" ]] && { echo "DB=<empty>"; return; }
  h=$(node -e 'const {parse}=require(process.argv[1]+"/pg-connection-string"); try{process.stdout.write(String(parse(process.argv[2]).host))}catch(e){process.stdout.write("THROWS")}' "$NM" "$u")
  [[ "$h" == *"$M"* ]] && echo "DB=REMOTE" || echo "DB=local"; }
necls() { [[ "$1" == production ]] && echo "NE=PRODUCTION" || echo "NE=other"; }
one() {  # one ID BODY WHERE [VAR=v]
  local id="$1" body="$2" where="$3" extra="${4-}" f="$D/$1-$3.env.bin" out a b c r
  if [[ $where == prepend ]]; then { printf '%s' "$body"; cat "$GB"; } > "$f"; else { cat "$GB"; printf '%s' "$body"; } > "$f"; fi
  out=$(env ${extra:+"$extra"} node -e 'const d=require(process.argv[1]+"/dotenv");const o=d.parse(require("fs").readFileSync(process.argv[2]));process.stdout.write((o.DATABASE_URL||"")+"\n"+(o.NODE_ENV??"")+"\n")' "$NM" "$f")
  a="$(dbcls "$(sed -n 1p <<<"$out")") $(necls "$(sed -n 2p <<<"$out")")"
  out=$(env -i PATH=/usr/bin:/bin ${extra:+"$extra"} bash -c 'set -a; . "$1" >/dev/null 2>&1; printf "%s\n%s\n" "${DATABASE_URL:-}" "${NODE_ENV:-}"' _ "$f")
  b="$(dbcls "$(sed -n 1p <<<"$out")") $(necls "$(sed -n 2p <<<"$out")")"
  out=$(env -i PATH=/Users/kamilkreiser/.docker/bin:/opt/homebrew/bin:/usr/bin:/bin HOME=$W/scratch/chome DOCKER_CONFIG=/Users/kamilkreiser/.docker ${extra:+"$extra"} docker compose -p gate166probe --env-file "$f" -f "$D/probe.yml" config --format json 2>/dev/null \
        | python3 -I -c 'import json,sys
try:
  e=json.load(sys.stdin)["services"]["probe"]["environment"]; print(e.get("DATABASE_URL") or ""); print(e.get("NODE_ENV") or "")
except Exception: print(""); print("ERR")')
  c="$(dbcls "$(sed -n 1p <<<"$out")") $(necls "$(sed -n 2p <<<"$out")")"
  [[ "$(sed -n 2p <<<"$out")" == ERR ]] && c="ERR(compose refused file)"
  out=$(env -i PATH=/Users/kamilkreiser/.docker/bin:/opt/homebrew/bin:/usr/bin:/bin HOME=$W/scratch/chome DOCKER_CONFIG=/Users/kamilkreiser/.docker ${extra:+"$extra"} docker compose -p gate166real --project-directory "$W/scratch/realcompose" --env-file "$f" -f "$W/scratch/realcompose/docker-compose.yml" config --format json 2>/dev/null \
        | python3 -I -c 'import json,sys
try:
  print(json.load(sys.stdin)["services"]["api-gateway"]["environment"].get("NODE_ENV"))
except Exception: print("ERR")')
  [[ "$out" == production ]] && r="api-gateway NE=PRODUCTION" || r="api-gateway NE=$out"
  printf '%-4s %-7s dotenv[%s]  bash[%s]  compose-probe[%s]  real-compose[%s] %s\n' "$id" "$where" "$a" "$b" "$c" "$r" "$extra"
}
for ix in "${!IDS[@]}"; do one "${IDS[$ix]}" "${BODIES[$ix]}" append; one "${IDS[$ix]}" "${BODIES[$ix]}" prepend; done
one s01 'NODE_ENV=${GATE_SHELLX}'$'\n' append GATE_SHELLX=production
one s02 'DATABASE_URL=postgres://u:p@localhost/x${GATE_SQ}'$'\n' append "GATE_SQ=?host=$M.host"
echo "== controls (consumer instrument fires): canonical remote / production lines =="
one k91 "DATABASE_URL=postgres://u:p@$M.host/x"$'\n' append
one k92 'NODE_ENV=production'$'\n' append
one k93 'NODE_ENV=development'$'\n' append
