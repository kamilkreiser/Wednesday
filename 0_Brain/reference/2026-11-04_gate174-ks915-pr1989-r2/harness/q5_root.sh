#!/bin/bash
# Q5 (G173-F4 reported truthfully): does the repo-root note print exactly when the root entry's auth would not get the
# written values? Independent instrument: rootadmin.js on the REAL root-entry compose config after the run.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q5}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
N=$'\n'; GB0=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
GBS=$L/golden_admin_set.env.bin; grep -v '^ADMIN_USER_PASSWORD=' "$GB0" > "$GBS"; printf 'ADMIN_USER_PASSWORD=gate174-not-secret-devset\n' >> "$GBS"
GBF=$L/golden_allow_false.env.bin; grep -v '^ALLOW_DEFAULT_SEED_PASSWORDS=' "$GB0" > "$GBF"; printf 'ALLOW_DEFAULT_SEED_PASSWORDS=false\n' >> "$GBF"
GBT=$L/golden_allow_true.env.bin; grep -v '^ALLOW_DEFAULT_SEED_PASSWORDS=' "$GB0" > "$GBT"; printf 'ALLOW_DEFAULT_SEED_PASSWORDS=true\n' >> "$GBT"
rr() { printf '      notes: admin=%s allow=%s couldnot=%s | written: %s | %s\n' "$(grep -c 'NOT pass the ADMIN_USER_PASSWORD' $L/$1.log)" "$(grep -c 'NOT pass ALLOW_DEFAULT_SEED_PASSWORDS=true' $L/$1.log)" "$(grep -c 'could not re-read the repo-root entry' $L/$1.log)" \
  "$(grep -oE '^restore-local-secrets: (generated|rotated|kept) ADMIN_USER_PASSWORD|(set|kept|rewrote) ALLOW_DEFAULT_SEED_PASSWORDS' $L/$1.log | sed 's/restore-local-secrets: //' | tr '\n' ',')" \
  "$(cd $LASTCLONE && env -i PATH=$GPATH HOME=$W/home docker compose -f docker-compose.local.yml config --format json 2>/dev/null | node $W/harness/rootadmin.js "$NM" "$LASTCLONE/Blockchain/Dev/.env")"; }
NOCONS=1 GB=$GB0 gcell ra0 '' '' '';                                                             rr ra0
NOCONS=1 GB=$GB0 gcell ra1 '' "ADMIN_USER_PASSWORD=$N" '';                                       rr ra1
NOCONS=1 GB=$GB0 gcell ra2 '' "ADMIN_USER_PASSWORD=gate174-not-secret-root$N" '';                rr ra2
NOCONS=1 GB=$GB0 gcell ra3 '' "ALLOW_DEFAULT_SEED_PASSWORDS=false$N" '';                         rr ra3
NOCONS=1 GB=$GB0 gcell ra4 '' "ALLOW_DEFAULT_SEED_PASSWORDS=true$N" '';                          rr ra4
NOCONS=1 GB=$GB0 gcell ra5 '' "ALLOW_DEFAULT_SEED_PASSWORDS=TRUE$N" '';                          rr ra5
NOCONS=1 GB=$GBS gcell ra6 '' "ADMIN_USER_PASSWORD=gate174-not-secret-root$N" '';                rr ra6
NOCONS=1 GB=$GBS gcell ra7 '' "ADMIN_USER_PASSWORD=gate174-not-secret-root$N" '' -- --rotate;    rr ra7
NOCONS=1 GB=$GBS gcell ra8 '' '' '' -- --rotate;                                                 rr ra8
NOCONS=1 GB=$GBT gcell ra9 '' "ALLOW_DEFAULT_SEED_PASSWORDS=false$N" '';                         rr ra9
NOCONS=1 GB=$GBF gcell raa '' "ALLOW_DEFAULT_SEED_PASSWORDS=true$N" '';                          rr raa
NOCONS=1 GB=$GB0 gcell rab '' "ADMIN_USER_PASSWORD=gate174-not-secret-root${N}ALLOW_DEFAULT_SEED_PASSWORDS=false$N" ''; rr rab
NOCONS=1 GB=$GB0 gcell rac '' "STACK_PREFIX=x$N" '';                                             rr rac
