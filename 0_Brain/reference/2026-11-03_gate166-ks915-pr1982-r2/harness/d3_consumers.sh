#!/bin/bash
# D3: what the real consumers (dotenv 16.6.1, docker compose v5 `config`, bash `set -a; .`) read
# from new .env spellings. Test files hold only crafted lines (no generated values).
set -uo pipefail
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2
NM="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules"
D=$W/scratch/d3c; mkdir -p "$D" "$W/scratch/chome"
M=gate166rmt
BOM=$'\xef\xbb\xbf'; NB=$'\xc2\xa0'; CR=$'\r'; TAB=$'\t'
source "$W/harness/d3_cases.sh"
printf 'services:\n  probe:\n    image: busybox\n    environment:\n      - DATABASE_URL=${DATABASE_URL:-}\n      - NODE_ENV=${NODE_ENV:-development}\n' > "$D/compose.yml"
printf '%-4s %-26s %-26s %-26s | %s\n' id dotenv-16.6.1 bash-set-a compose-v5-config case
for ix in "${!IDS[@]}"; do
  id="${IDS[$ix]}"; body="${BODIES[$ix]}"
  f="$D/$id.env"; printf '%s' "$body" > "$f"
  # DB: the host pg-connection-string 2.12.0 (pg 8.20.0) resolves from the value the consumer read
  cls() { local u="$1" n="$2" h; if [[ -n "$u" ]]; then
      h=$(node -e 'const {parse}=require(process.argv[1]+"/pg-connection-string"); try{const c=parse(process.argv[2]); process.stdout.write(String(c.host))}catch(e){process.stdout.write("THROWS")}' "$NM" "$u")
      if [[ "$h" == *"$M"* ]]; then echo "DB=REMOTE(pg host)"; else echo "DB=local(pg:$h)"; fi
    else echo "NODE_ENV=$(printf %q "$n")"; fi; }
  dn=$(node -e '
    const d=require(process.argv[1]+"/dotenv"); const fs=require("fs");
    const o=d.parse(fs.readFileSync(process.argv[2]));
    process.stdout.write((o.DATABASE_URL||"")+"\n"+(o.NODE_ENV===undefined?"<unset>":o.NODE_ENV)+"\n");' "$NM" "$f" 2>&1)
  dn=$(cls "$(sed -n 1p <<<"$dn")" "$(sed -n 2p <<<"$dn")")
  bs=$(env -i PATH=/usr/bin:/bin bash -c 'set -a; . "$1" >/dev/null 2>&1; printf "%s\n%s\n" "${DATABASE_URL:-}" "${NODE_ENV-<unset>}"' _ "$f")
  bs=$(cls "$(sed -n 1p <<<"$bs")" "$(sed -n 2p <<<"$bs")")
  cf=$(env -i PATH=/Users/kamilkreiser/.docker/bin:/opt/homebrew/bin:/usr/bin:/bin HOME=$W/scratch/chome DOCKER_CONFIG=/Users/kamilkreiser/.docker docker compose -p gate166probe --env-file "$f" -f "$D/compose.yml" config --format json 2>&1)
  cs=$(python3 -I -c 'import json,sys
try:
  e=json.loads(sys.stdin.read())["services"]["probe"]["environment"]; print((e.get("DATABASE_URL") or "")); print(e.get("NODE_ENV"))
except Exception as x: print(""); print("ERR")' <<<"$cf")
  cs=$(cls "$(sed -n 1p <<<"$cs")" "$(sed -n 2p <<<"$cs")")
  printf '%-4s %-26s %-26s %-26s | %q\n' "$id" "$dn" "$bs" "$cs" "$body"
done
