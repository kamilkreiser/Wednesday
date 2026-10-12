#!/bin/zsh
# Throwaway PG15 for the PR1525 gate (adapted from J 4th's setup1497.sh; paths and port mine)
set -u
SP=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g1525_pg
D=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g1525_head/Blockchain/Dev
PORT=55417; SOCK=/private/tmp/claude-501/pg1525; PGBIN=/opt/homebrew/opt/postgresql@15/bin; PGD=$SP/pgdata
die() { echo "STOP: $1"; exit ${2:-1}; }
mkdir -p $SP $SOCK
P() { $PGBIN/psql -h 127.0.0.1 -p $PORT -U postgres -v ON_ERROR_STOP=1 -q "$@"; }
[ -d $PGD ] && die "pgdata exists" 30
$PGBIN/initdb -D $PGD -U postgres --auth=trust -E UTF8 > /dev/null || die initdb 31
$PGBIN/pg_ctl -D $PGD -o "-p $PORT -k $SOCK -c listen_addresses=127.0.0.1" -l $SP/pg.log -w start > /dev/null || die start 32
P -d postgres -c "CREATE DATABASE ks_full" || die db 33
fail=0; ok=0
for f in $D/docker/init/[0-9]*.sql; do
  case $(basename $f) in 00-*) continue;; esac
  if P -d ks_full -f $f > $SP/init_$(basename $f).out 2>&1; then ok=$((ok+1)); else fail=$((fail+1)); echo "INIT FAIL: $(basename $f)"; fi
done
echo "init sql: applied=$ok failed=$fail"
P -d ks_full -c "CREATE TABLE _secuura_migrations (filename TEXT PRIMARY KEY, applied_at TIMESTAMPTZ DEFAULT NOW())" || die mt 34
ok=0; fail=0
for f in $D/migrations/*.sql; do
  b=$(basename $f)
  [[ $b == *[Pp][Ll][Aa][Tt][Ff][Oo][Rr][Mm]* ]] && continue
  if P -d ks_full -f $f > $SP/mig_$b.out 2>&1; then P -d ks_full -c "INSERT INTO _secuura_migrations(filename) VALUES ('$b')"; ok=$((ok+1)); else fail=$((fail+1)); echo "MIGRATION FAIL: $b"; fi
done
echo "migrations: applied=$ok failed=$fail"
P -d ks_full -f $D/migrations/003_platform_tenancy.sql > $SP/mig_platform.out 2>&1 && echo "platform tenancy: applied" || echo "PLATFORM FAIL"
umask 077
PW=$(openssl rand -hex 16); print -n "$PW" > $SP/app_pw
P -d postgres -c "CREATE ROLE secuura_app WITH LOGIN PASSWORD '$PW' NOSUPERUSER NOBYPASSRLS" || die role 35
P -d ks_full -c "GRANT CONNECT ON DATABASE ks_full TO secuura_app; GRANT USAGE ON SCHEMA public TO secuura_app; GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO secuura_app; GRANT USAGE,SELECT ON ALL SEQUENCES IN SCHEMA public TO secuura_app" || die grants 36
print "export TEST_DATABASE_URL=postgresql://postgres@127.0.0.1:$PORT/ks_full\nexport TEST_PLATFORM_DATABASE_URL=postgresql://postgres@127.0.0.1:$PORT/ks_full\nexport TEST_APP_DATABASE_URL=postgresql://secuura_app:$PW@127.0.0.1:$PORT/ks_full" > $SP/pg.env
chmod 600 $SP/pg.env
P -d ks_full -At -c "SELECT rolname, rolsuper, rolbypassrls FROM pg_roles WHERE rolname IN ('secuura_app','postgres') ORDER BY 1"
P -d ks_full -At -c "SELECT relname, relrowsecurity, relforcerowsecurity FROM pg_class WHERE relname IN ('documents','action_provenance') AND relkind='r' ORDER BY 1"
P -d ks_full -At -c "SELECT count(*) FROM _secuura_migrations"
echo SETUP DONE
