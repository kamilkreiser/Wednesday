#!/bin/bash
. /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/harness/lib.sh
set -u
R=$WD/repo
git -C "$R" show pr/2002:Blockchain/Dev/migrations/058_ks1401_tenant_isolation_after_039.sql > "$F058_REAL"
git -C "$R" show pr/2001:Blockchain/Dev/migrations/057_ks1256_gateway_settings_store.sql > "$F057"
echo "058 sha $(shasum -a 256 < "$F058_REAL" | cut -c1-12)  057 sha $(shasum -a 256 < "$F057" | cut -c1-12)"
if lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; then echo "PORT $PORT BUSY"; exit 1; fi
mkdir -p "$SOCK"
if [ ! -d "$WD/tmp/pgdata" ]; then
  "$PGB/initdb" -D "$WD/tmp/pgdata" -U postgres -A trust --no-locale -E UTF8 > "$WD/tmp/initdb.log" 2>&1 || { echo initdb failed; exit 1; }
fi
"$PGB/pg_ctl" -D "$WD/tmp/pgdata" -l "$WD/tmp/pg.log" -w -o "-c listen_addresses=127.0.0.1 -k $SOCK -p $PORT -c fsync=off -c synchronous_commit=off -c full_page_writes=off" start > "$WD/tmp/start.log" 2>&1 || { echo start failed; tail -5 "$WD/tmp/pg.log"; exit 1; }
echo "postmaster pid $(head -1 "$WD/tmp/pgdata/postmaster.pid") port $PORT"
S postgres "SELECT version()"
S postgres "SELECT current_setting('listen_addresses')||' '||current_setting('port')||' '||current_setting('data_directory')"
P postgres -c "CREATE ROLE secuura_app NOLOGIN NOSUPERUSER NOBYPASSRLS; CREATE ROLE mig_owner LOGIN NOSUPERUSER NOBYPASSRLS;" 2>&1 | tail -1
S postgres "SELECT rolname||' super='||rolsuper||' bypass='||rolbypassrls FROM pg_roles WHERE rolname IN ('secuura_app','mig_owner') ORDER BY 1"
# template at develop 536642104002 through 056: docker/init/0[1-9]*.sql then the REAL run-migrations.sh over develop's migrations
mkdb tpl056 >/dev/null; mkdb plat_tpl056 >/dev/null
for f in "$DEV"/docker/init/0[1-9]*.sql; do P tpl056 -f "$f" >> "$WD/tmp/tpl_init.log" 2>&1 || echo "INITFAIL $(basename "$f")"; done
RD=$(mkrun base)
runmig "$RD" tpl056 > "$WD/runs/setup_tpl056_runner.log" 2>&1
grep -E 'Summary|RC=|FAILED' "$WD/runs/setup_tpl056_runner.log"
echo "tracker rows: $(S tpl056 'SELECT count(*) FROM _secuura_migrations') ; 058 rows $(rec tpl056 058_ks1401_tenant_isolation_after_039.sql); 056 rows $(rec tpl056 056_ks1933_billing_credit_grants.sql); 039 rows $(rec tpl056 039_rls_fail_closed.sql)"
for t in $TABLES; do reading tpl056 $t; done
