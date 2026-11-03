#!/bin/bash
# Q2 (Wednesday's condition): the credential route through each of the 4 credential keys, compose reader WORKING and BROKEN.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q2}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
M=gate174rmt; N=$'\n'; SH=$W/harness/shim
GB=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
F_APW_HA="APP_DB_PASSWORD=p@localhost/x?hostaddr=10.9.9.9$N"
F_APW_HOST="APP_DB_PASSWORD=p@$M.host:5432/x#$N"
F_AUSER_HOST="APP_DB_USER=u:p@$M.host:5432/x#$N"
F_AUSER_SVC="APP_DB_USER=u:p@localhost/x?service=$M#$N"
F_PUSER_HOST="POSTGRES_USER=u:p@$M.host:5432/x#$N"
F_PPW_HA="POSTGRES_PASSWORD=p@localhost/x?hostaddr=10.9.9.9#$N"
F_PPW_HOST="POSTGRES_PASSWORD=p@$M.host:5432/x#$N"
echo "== A. compose reader WORKING: every credential form must be refused =="
i=0; for f in "$F_APW_HA" "$F_APW_HOST" "$F_AUSER_HOST" "$F_AUSER_SVC" "$F_PUSER_HOST" "$F_PPW_HA" "$F_PPW_HOST"; do i=$((i+1)); gcell w0$i "$f" '' ''; done
gcell w08 '' "$F_APW_HOST" ''
gcell w09 '' '' '' "APP_DB_PASSWORD=p@$M.host:5432/x#"
gcell w10 '' '' "$F_PPW_HOST"
echo "== B. compose reader BROKEN, same credential forms (APP_DB_PASSWORD host + POSTGRES_USER host + POSTGRES_PASSWORD hostaddr) =="
NOPATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin
for f in "$F_APW_HOST" "$F_PUSER_HOST" "$F_PPW_HA"; do i=$((i+1))
  k=${f%%=*}
  RUNPATH=$NOPATH NOCONS=1 gcell b${i}_nodocker_$k "$f" '' ''
  for s in nocompose failrc garbage emptyout emptyobj emptyarr envlist noenv truncated truncatedtail rc0stderr rootonlyfail; do
    RUNPATH=$SH:$GPATH NOCONS=1 gcell b${i}_${s}_$k "$f" '' '' GATE_SHIM=$s
  done
  PREP='printf "services: [\n" >> "$c/Blockchain/Dev/docker-compose.yml"' NOCONS=1 gcell b${i}_devfile_broken_$k "$f" '' ''
  TIMEOUT=45 RUNPATH=$SH:$GPATH NOCONS=1 gcell b${i}_hang_$k "$f" '' '' GATE_SHIM=hang
  echo "   hang leftovers (shim sleeps): $(pgrep -f 'sleep 600' | tr '\n' ' ')"
done
echo "== C. controls: the shim passes through when unset; a clean credential is accepted =="
RUNPATH=$SH:$GPATH gcell c01 "APP_DB_PASSWORD=gate174plainpw$N" '' ''
RUNPATH=$SH:$GPATH NOCONS=1 gcell c02 "$F_APW_HOST" '' ''
