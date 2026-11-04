#!/bin/bash
# Gate 180 Q4 regression: gate 173 n01-n05 (G173-F1) + the credential-through-DATABASE_URL condition forms (gate 174 Q2 compose-working w-forms).
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate180-ks915-pr1989-r3/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q4r}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
M=gate180rmt; N=$'\n'
GB=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
gcell n01 "POSTGRES_HOST=$M.host$N" '' ''
gcell n02 '' "POSTGRES_HOST=$M.host$N" ''
gcell n03 '' '' '' "POSTGRES_HOST=$M.host"
gcell n04 "POSTGRES_DB=\"secuura host=$M.host\"$N" '' ''
gcell n05 "POSTGRES_PORT=5432$N" '' ''
gcell h10 "POSTGRES_HOST=postgres port=5432 host=$M.host$N" '' ''
gcell p02 "POSTGRES_PORT=+5432$N" '' ''
gcell w01 "APP_DB_PASSWORD='x@$M.host:5432/secuura?hostaddr=1.2.3.4&a='$N" '' ''
gcell w02 "APP_DB_PASSWORD=x@$M.host/secuura?x=$N" '' ''
gcell w03 '' "POSTGRES_PASSWORD=x@$M.host/secuura?x=$N" ''
gcell w04 '' '' '' "APP_DB_USER=u@$M.host/secuura?x="
gcell w05 "POSTGRES_USER=u?host=$M.host&x=$N" '' ''
gcell c01 "APP_DB_PASSWORD=plainLocalPw123$N" '' ''
