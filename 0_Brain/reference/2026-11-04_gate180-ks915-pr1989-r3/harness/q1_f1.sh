#!/bin/bash
# Gate 180 Q1: G174-F1 forms at head (and, with SCRIPT_SRC=round2, at round 2). Labels/counts only.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate180-ks915-pr1989-r3/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q1}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
M=gate180rmt; N=$'\n'; CR=$'\r'
GB=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
SL="[databases]\\nsecuura = host=$M.host port=5432 dbname=secuura"
echo "== A. gate 174 g01-g04 (verbatim forms) + the fifth key =="
gcell g01 "PGBOUNCER_MAX_CLIENT_CONN='10000\\n$SL'$N" '' ''
gcell g02 "PGBOUNCER_DEFAULT_POOL_SIZE=1000\\n$SL$N" '' ''
gcell g03 '' "PGBOUNCER_RESERVE_POOL_SIZE='100\\n$SL'$N" ''
gcell g04 '' '' '' "PGBOUNCER_MAX_DB_CONNECTIONS=0\\n$SL"
gcell g05 "PGBOUNCER_MAX_USER_CONNECTIONS='0\\n$SL'$N" '' ''
echo "== B. new forms (not in gate 174 or the READY) =="
gcell v01 "PGBOUNCER_MAX_CLIENT_CONN=\"10000\\n$SL\"$N" '' ''
gcell v02 '' '' '' "PGBOUNCER_MAX_USER_CONNECTIONS=0${N}[databases]${N}secuura = host=$M.host port=5432 dbname=secuura"
gcell v03 "PGBOUNCER_MAX_CLIENT_CONN=10${CR}[databases]${CR}secuura = host=$M.host port=5432 dbname=secuura$N" '' ''
gcell v04 "PGBOUNCER_DEFAULT_POOL_SIZE=+100$N" '' ''
gcell v05 "PGBOUNCER_DEFAULT_POOL_SIZE=-1$N" '' ''
gcell v06 "PGBOUNCER_DEFAULT_POOL_SIZE=１００$N" '' ''
gcell v07 "PGBOUNCER_RESERVE_POOL_SIZE=0x10$N" '' ''
gcell v08 "PGBOUNCER_MAX_DB_CONNECTIONS=\${GATE_X}$N" '' '' "GATE_X=0${N}[databases]${N}secuura = host=$M.host"
gcell v09 "export PGBOUNCER_MAX_CLIENT_CONN='10|$M'$N" '' ''
gcell v10 "PGBOUNCER_MAX_CLIENT_CONN=10$N" "PGBOUNCER_MAX_CLIENT_CONN='10\\n$SL'$N" ''
gcell v11 "PGBOUNCER_MAX_CLIENT_CONN=abc${N}PGBOUNCER_MAX_CLIENT_CONN=10$N" '' ''
echo "== C. line-break rule on other judged keys =="
gcell l01 '' '' '' "NODE_ENV=development${N}staging"
gcell l02 '' '' '' "DATABASE_URL=postgres://u@localhost:5432/secuura${N}"
gcell l03 "NODE_ENV=\"development\\nstaging\"$N" '' ''
gcell l04 '' '' '' "GATE_UNJUDGED=a${N}b"
echo "== D. benign controls (must be accepted) =="
gcell b01 "PGBOUNCER_MAX_CLIENT_CONN=100${N}PGBOUNCER_DEFAULT_POOL_SIZE=20${N}PGBOUNCER_RESERVE_POOL_SIZE=5${N}PGBOUNCER_MAX_DB_CONNECTIONS=50${N}PGBOUNCER_MAX_USER_CONNECTIONS=0$N" '' ''
gcell b02 '' '' '' PGBOUNCER_MAX_CLIENT_CONN=100 PGBOUNCER_DEFAULT_POOL_SIZE=20 PGBOUNCER_RESERVE_POOL_SIZE=5 PGBOUNCER_MAX_DB_CONNECTIONS=50 PGBOUNCER_MAX_USER_CONNECTIONS=0
gcell b03 "PGBOUNCER_MAX_CLIENT_CONN=${N}PGBOUNCER_DEFAULT_POOL_SIZE=$N" '' ''
gcell b04 "PGBOUNCER_MAX_CLIENT_CONN=100 # sized for laptop$N" "PGBOUNCER_RESERVE_POOL_SIZE=7$N" ''
gcell b05 "NODE_ENV=development$N" '' ''
