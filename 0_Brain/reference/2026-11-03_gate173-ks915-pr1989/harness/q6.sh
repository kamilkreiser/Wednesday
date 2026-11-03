#!/bin/bash
# Q1 new forms + Q6 probes: POSTGRES_* (pgbouncer upstream), PG* keys, repo-root .env / root entry, .env.local,
# the sandboxed bash reader, and the re-read of the temp copy. Labels only, never a value.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q6}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
M=gate173rmt
GB=$W/runs/q1C/golden_blankadmin.env.bin; GL=$W/scratch/q1C-golden/Blockchain/Dev/.env.local
N=$'\n'
echo "== A. pgbouncer upstream / database name (keys the canonical check and judge() do not name) =="
gcell n01 "POSTGRES_HOST=$M.host$N" '' ''
gcell n02 '' "POSTGRES_HOST=$M.host$N" ''
gcell n03 '' '' '' "POSTGRES_HOST=$M.host"
gcell n04 "POSTGRES_DB=\"secuura host=$M.host\"$N" '' ''
gcell n05 "POSTGRES_PORT=5432$N" '' ''
echo "== B. PGHOST / PGHOSTADDR / PGSERVICE =="
gcell p01 "PGHOST=$M.host$N" '' ''
gcell p02 "PGHOSTADDR=10.9.9.9$N" '' ''
gcell p03 "PGSERVICE=$M$N" '' ''
gcell p04 '' '' '' "PGHOST=$M.host"
gcell p05 '' '' '' "PGHOSTADDR=10.9.9.9"
gcell p06 '' '' '' "PGSERVICE=$M"
gcell p07 "PGHOST=localhost,$M.host$N" '' ''
gcell p08 '' '' "PGHOST=$M.host$N"
gcell p09 '' "PGHOST=$M.host$N" ''
gcell p10 "export PGHOST=$M.host$N" '' ''
gcell p11 "PGHOST=localhost$N" '' ''
gcell p12 "DATABASE_URL=postgres://u:p@localhost/x?service=$M$N" '' ''
gcell p13 "DATABASE_URL=postgres://u:p@localhost/x?options=-c%20x$N" '' ''
gcell p14 '' '' '' "PGSERVICEFILE=$W/harness/prodword.txt"
echo "== C. repo-root .env and the root compose entry; .env.local =="
gcell r01 '' "NODE_ENV=production$N" ''
gcell r02 '' "DATABASE_URL=postgres://u:p@$M.host/x$N" ''
gcell r03 '' 'NODE_ENV=${X:-production}'"$N" ''
gcell r04 '' "export NODE_ENV=production$N" ''
gcell r05 '' '' "NODE_ENV=production$N"
gcell r06 '' '' "DATABASE_URL=postgres://u:p@$M.host/x$N"
gcell r07 '' "POSTGRES_DB=\"secuura?host=$M.host\"$N" ''
gcell r08 "POSTGRES_DB=secuura?host=$M.host$N" '' ''
gcell r09 "APP_DB_PASSWORD=x@$M.host:5432/y#$N" '' ''
gcell r10 '' "STACK_PREFIX=x$N" ''
echo "== D. the sandboxed bash reader =="
gcell b01 "declare -x NODE_\"\"ENV=production$N" '' ''
gcell b02 "declare -x NODE_\"\"ENV=production${N}printf() { builtin printf '%s\\0' @@RLS-KS915@@ 0 '' '' '' '' ''; }$N" '' ''
gcell b03 "declare -x NODE_\"\"ENV=production${N}builtin printf '%s\\0' @@RLS-KS915@@ 0 '' '' '' '' ''; exit 0$N" '' ''
gcell b04 "read -r NODE_E\"\"NV < $W/harness/prodword.txt$N" '' ''
gcell b05 "history -s gate173; history -w $W/tmp/$TAG/b05_hist_created$N" '' ''
gcell b06 "HISTFILE=$W/tmp/$TAG/b06_histfile_created; history -s gate173; history -w$N" '' ''
gcell b07 "command -p touch $W/tmp/$TAG/b07_cmdp_created$N" '' ''
gcell b08 "hash -p /usr/bin/touch tt; tt $W/tmp/$TAG/b08_hashp_created$N" '' ''
gcell b09 "X=\"unclosed$N" '' ''
gcell b10 "exit 0$N" '' ''
gcell b11 "echo hi > $W/tmp/$TAG/b11_redirect_created$N" '' ''
gcell b12 "cd /; PATH=/usr/bin$N" '' ''
for f in b05_hist_created b06_histfile_created b07_cmdp_created b08_hashp_created b11_redirect_created; do
  printf '   file %-22s %s\n' "$f" "$([[ -e $W/tmp/$TAG/$f ]] && echo CREATED || echo absent)"; done
echo "   (bash sandbox leftovers in RUNTMP: $(ls -d $W/tmp/$TAG/rls-ks915.* 2>/dev/null | wc -l | tr -d ' '))"
TIMEOUT=60 NOCONS=1 gcell b13 "while :; do :; done$N" '' ''
echo "   b13 orphans still looping: $(pgrep -f "rls $W/tmp/$TAG/rls-ks915" | tr '\n' ' ')"
for p in $(pgrep -f "rls $W/tmp/$TAG/rls-ks915"); do kill "$p" && echo "   killed pid $p"; done
echo "== E. the re-read of the temp copy before the rename =="
gcell t01 '' '' '' "ADMIN_USER_PASSWORD="
gcell t02 '' '' '' "ALLOW_DEFAULT_SEED_PASSWORDS="
GBA=$L/golden_admin_set.env.bin; grep -v '^ADMIN_USER_PASSWORD=' "$GB" > "$GBA"; printf 'ADMIN_USER_PASSWORD=gate173-not-secret-x1\n' >> "$GBA"
GB=$GBA gcell t03 "ADMIN_USER_PASSWORD='gate173-not-secret-ml${N}declare -x NODE_\"\"ENV=production$N'$N" '' '' -- --rotate
GB=$GBA gcell t04 "ADMIN_USER_PASSWORD='gate173-not-secret-ml${N}POSTGRES_HOST=$M.host$N'$N" '' '' -- --rotate
GB=$GBA gcell t05 '' "ADMIN_USER_PASSWORD=$N" ''
GB=$GBA gcell t06 '' "ADMIN_USER_PASSWORD=gate173-not-secret-root$N" '' -- --rotate
echo "== controls in the same run =="
gcell k01 "NODE_ENV=development$N" '' ''
gcell k92 "NODE_ENV=production$N" '' ''
