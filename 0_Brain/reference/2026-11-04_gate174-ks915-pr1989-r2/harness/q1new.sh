#!/bin/bash
# Q1: gate 173's n01-n05 at the round-2 head, then forms neither gate nor the seat tried. Labels only, never a value.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q1n}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
M=gate174rmt; N=$'\n'
GB=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
echo "== A. gate 173 n01-n05 =="
gcell n01 "POSTGRES_HOST=$M.host$N" '' ''
gcell n02 '' "POSTGRES_HOST=$M.host$N" ''
gcell n03 '' '' '' "POSTGRES_HOST=$M.host"
gcell n04 "POSTGRES_DB=\"secuura host=$M.host\"$N" '' ''
gcell n05 "POSTGRES_PORT=5432$N" '' ''
echo "== B. POSTGRES_HOST spellings =="
gcell h01 "POSTGRES_HOST=postgres.$N" '' ''
gcell h02 "POSTGRES_HOST=localhost.$N" '' ''
gcell h03 "POSTGRES_HOST=::1$N" '' ''
gcell h04 "POSTGRES_HOST=[::1]$N" '' ''
gcell h05 "POSTGRES_HOST=2001:db8::1$N" '' ''
gcell h06 "POSTGRES_HOST=postgres.$M.host$N" '' ''
gcell h07 "POSTGRES_HOST=POSTGRES$N" '' ''
gcell h08 "POSTGRES_HOST=127.0.0.2$N" '' ''
gcell h09 "POSTGRES_HOST=\"postgres host=$M.host\"$N" '' ''
gcell h10 "POSTGRES_HOST=postgres port=5432 host=$M.host$N" '' ''
gcell h11 '' '' "POSTGRES_HOST=$M.host$N"
echo "== C. POSTGRES_PORT spellings =="
gcell p01 "POSTGRES_PORT=05432$N" '' ''
gcell p02 "POSTGRES_PORT=+5432$N" '' ''
gcell p03 "POSTGRES_PORT=\" 5432\"$N" '' ''
gcell p04 "POSTGRES_PORT=65536$N" '' ''
gcell p05 "POSTGRES_PORT=99999$N" '' ''
gcell p06 "POSTGRES_PORT=123456$N" '' ''
gcell p07 '' '' '' "POSTGRES_PORT=5432 "
echo "== D. POSTGRES_DB spellings =="
gcell d01 "POSTGRES_DB=sécuura$N" '' ''
gcell d02 "POSTGRES_DB=$(printf 'a%.0s' $(seq 1 300))$N" '' ''
gcell d03 "POSTGRES_DB=$N" '' ''
gcell d04 '' '' '' "POSTGRES_DB=sécuura"
echo "== E. the remote host in .env AND the shell, different values =="
gcell x01 "POSTGRES_HOST=localhost$N" '' '' "POSTGRES_HOST=$M.host"
gcell x02 "POSTGRES_HOST=$M.host$N" '' '' "POSTGRES_HOST=localhost"
gcell x03 "POSTGRES_HOST=localhost$N" "POSTGRES_HOST=$M.host$N" ''
gcell x04 "POSTGRES_HOST=$M.host$N" "POSTGRES_HOST=localhost$N" ''
echo "== F. override / extra file / COMPOSE_FILE / COMPOSE_ENV_FILES =="
OV="services:${N}  pgbouncer:${N}    environment:${N}      POSTGRES_HOST: $M.host${N}"
PREP="printf '%s' \"\$OV\" > \"\$c/Blockchain/Dev/docker-compose.override.yml\"" gcell o01 '' '' ''
OV="services:${N}  pgbouncer:${N}    environment:${N}      POSTGRES_HOST: \${GATE_UP:-postgres}${N}"
PREP="printf '%s' \"\$OV\" > \"\$c/Blockchain/Dev/docker-compose.override.yml\"" gcell o02 "GATE_UP=$M.host$N" '' ''
OV="services:${N}  pgbouncer:${N}    environment:${N}      POSTGRES_HOST: $M.host${N}"
PREP="printf '%s' \"\$OV\" > \"\$c/Blockchain/Dev/gate-extra.yml\"" gcell o03 "COMPOSE_FILE=docker-compose.yml:gate-extra.yml$N" '' ''
PREP="printf '%s' \"\$OV\" > \"\$c/Blockchain/Dev/gate-extra.yml\"" gcell o04 '' '' '' "COMPOSE_FILE=docker-compose.yml:gate-extra.yml"
PREP="printf 'POSTGRES_HOST=%s.host\n' $M > \"\$c/gate-extra.env\"" gcell o05 '' '' '' "COMPOSE_ENV_FILES=../../gate-extra.env"
PREP="printf '%s' \"\$OV\" > \"\$c/Blockchain/Dev/gate-extra.yml\"" gcell o06 '' '' ''
echo "   o06 = the extra file exists but nothing names it (the user would pass -f); the script cannot see it, by design"
echo "== G. pgbouncer pool keys compose passes and entrypoint.sh renders by sed (not judged) =="
gcell g01 "PGBOUNCER_MAX_CLIENT_CONN='10000\\n[databases]\\nsecuura = host=$M.host port=5432 dbname=secuura'$N" '' ''
gcell g02 "PGBOUNCER_DEFAULT_POOL_SIZE=1000\\n[databases]\\nsecuura = host=$M.host port=5432 dbname=secuura$N" '' ''
gcell g03 '' "PGBOUNCER_RESERVE_POOL_SIZE='100\\n[databases]\\nsecuura = host=$M.host port=5432 dbname=secuura'$N" ''
gcell g04 '' '' '' "PGBOUNCER_MAX_DB_CONNECTIONS=0\\n[databases]\\nsecuura = host=$M.host port=5432 dbname=secuura"
echo "== controls in the same run =="
gcell k01 "NODE_ENV=development$N" '' ''
gcell k92 "NODE_ENV=production$N" '' ''
gcell k93 "POSTGRES_HOST=postgres$N" '' ''
