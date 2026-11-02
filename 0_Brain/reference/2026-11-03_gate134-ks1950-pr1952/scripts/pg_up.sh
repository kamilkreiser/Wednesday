#!/bin/bash
# Start throwaway postgres:15-alpine as gate134-pg on 127.0.0.1:55134 and load schema. Removed by pg_down.sh.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate134-ks1950-pr1952
F=$G/repo/Blockchain/Dev/docker/init/04-sprint2-service-tables.sql
sed -n '152,220p' $F > $G/logs/gov_ddl.sql
docker run -d --name gate134-pg -e POSTGRES_PASSWORD=gate134super -p 127.0.0.1:55134:5432 postgres:15-alpine; echo "run rc=$?"
for i in $(seq 1 30); do docker exec gate134-pg pg_isready -U postgres -q && break; sleep 1; done
sleep 2
docker exec -i gate134-pg psql -v ON_ERROR_STOP=1 -U postgres -q < $G/logs/gov_ddl.sql; echo "ddl rc=$?"
docker exec -i gate134-pg psql -v ON_ERROR_STOP=1 -U postgres -q < $G/scripts/schema.sql; echo "schema rc=$?"
docker exec gate134-pg psql -U postgres -tAc "select version(); select rolname, rolsuper, rolbypassrls from pg_roles where rolname='gate_app'; select relname, relrowsecurity, relforcerowsecurity from pg_class where relname='users'; select conname from pg_constraint where conrelid='svc_governance_participants'::regclass; select indexrelid::regclass, indexrelid::int from pg_index where indrelid='svc_governance_participants'::regclass order by 2;"
