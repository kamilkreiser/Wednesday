#!/bin/bash
# Schema from the repo (head tree; the PR touches no SQL): docker/init/0*.sql then migrations/*.sql, then the app role.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate164-ks1868-pr1981
L=$W/logs/pg_setup.log; : > $L
for i in $(seq 1 30); do docker exec gate164-pg pg_isready -U secuura -d secuura >/dev/null 2>&1 && break; sleep 1; done
P="docker exec -i gate164-pg psql -U secuura -d secuura -v ON_ERROR_STOP=0 -q"
docker exec gate164-pg psql -U secuura -d secuura -c "CREATE ROLE secuura_app LOGIN PASSWORD 'g164app' NOSUPERUSER NOBYPASSRLS" >>$L 2>&1
for f in $(docker exec gate164-pg sh -c 'ls /dev_ro/docker/init/0*.sql'); do
  case "$(basename $f)" in 00-create-platform-db.sql) continue;; esac
  echo "== $f" >>$L; docker exec gate164-pg psql -U secuura -d secuura -v ON_ERROR_STOP=0 -q -f $f >>$L 2>&1
done
for f in $(docker exec gate164-pg sh -c 'ls /dev_ro/migrations/*.sql'); do
  echo "== $f" >>$L; docker exec gate164-pg psql -U secuura -d secuura -v ON_ERROR_STOP=0 -q -f $f >>$L 2>&1
done
$P >>$L 2>&1 <<'EOSQL'
GRANT CONNECT ON DATABASE secuura TO secuura_app;
GRANT USAGE ON SCHEMA public TO secuura_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO secuura_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO secuura_app;
EOSQL
echo "errors in setup log: $(grep -c ERROR $L)" | tee -a $L
docker exec gate164-pg psql -U secuura -d secuura -tAc "select relname, relrowsecurity, relforcerowsecurity from pg_class where relname='svc_api_keys'" | tee -a $L
docker exec gate164-pg psql -U secuura -d secuura -tAc "select polname, pg_get_expr(polqual, polrelid) from pg_policy where polrelid='svc_api_keys'::regclass" | tee -a $L
docker exec gate164-pg psql -U secuura -d secuura -tAc "select rolname, rolsuper, rolbypassrls from pg_roles where rolname like 'secuura%'" | tee -a $L
