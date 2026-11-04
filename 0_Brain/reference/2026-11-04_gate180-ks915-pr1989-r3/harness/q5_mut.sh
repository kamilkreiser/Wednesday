#!/bin/bash
# Gate 180 Q3: the surviving mutant e33_canon_value_pool_any. Run with SCRIPT_SRC=<head|mutant>. Plus what each consumer reads (digits? label only).
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate180-ks915-pr1989-r3/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q5}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
M=gate180rmt; N=$'\n'
GB=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
poolread() { local c="$1" d="$1/Blockchain/Dev" k=PGBOUNCER_MAX_CLIENT_CONN
  local a b x y
  a=$(node -e 'const d=require(process.argv[1]+"/dotenv");const v=d.parse(require("fs").readFileSync(process.argv[2]))[process.argv[3]];console.log(v==null?"unset":/^[0-9]+$/.test(v)?"digits":"NONDIGIT")' "$NM" "$d/.env" $k)
  b=$(env -i PATH=/usr/bin:/bin bash -c 'cd /tmp; set -a; . "$1" >/dev/null 2>&1; v="${PGBOUNCER_MAX_CLIENT_CONN-}"; [[ -z $v ]] && echo unset || { [[ $v =~ ^[0-9]+$ ]] && echo digits || echo NONDIGIT; }' _ "$d/.env")
  x=$(cd "$d" && env -i PATH="$GPATH" HOME="$W/home" docker compose config --format json 2>/dev/null | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const v=JSON.parse(s).services.pgbouncer.environment.PGBOUNCER_MAX_CLIENT_CONN;console.log(/^[0-9]+$/.test(v)?"digits":"NONDIGIT")})')
  y=$(cd "$c" && env -i PATH="$GPATH" HOME="$W/home" docker compose -f docker-compose.local.yml config --format json 2>/dev/null | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const v=JSON.parse(s).services.pgbouncer.environment.PGBOUNCER_MAX_CLIENT_CONN;console.log(/^[0-9]+$/.test(v)?"digits":"NONDIGIT")})')
  echo "      reads of PGBOUNCER_MAX_CLIENT_CONN: dotenv=$a bash=$b compose-dev=$x compose-root=$y"; }
NOCONS=1 gcell u1 "PGBOUNCER_MAX_CLIENT_CONN=1x$N" '' ''; poolread "$LASTCLONE"
NOCONS=1 gcell u2 "PGBOUNCER_MAX_CLIENT_CONN=abc${N}PGBOUNCER_MAX_CLIENT_CONN=10$N" '' ''; poolread "$LASTCLONE"
NOCONS=1 gcell u3 "PGBOUNCER_MAX_CLIENT_CONN=10${N}PGBOUNCER_MAX_CLIENT_CONN=abc$N" '' ''; poolread "$LASTCLONE"
NOCONS=1 gcell u4 "GATE_NOTE=\"first${N}PGBOUNCER_MAX_CLIENT_CONN=abc${N}last\"$N" '' ''; poolread "$LASTCLONE"
NOCONS=1 gcell u5 '' '' '' PGBOUNCER_MAX_CLIENT_CONN=abc
NOCONS=1 gcell u6 "PGBOUNCER_MAX_CLIENT_CONN=10$N" '' ''; poolread "$LASTCLONE"
