#!/bin/bash
# Start throwaway postgres:15-alpine as gate129-pg on 127.0.0.1:55129 and load schema. Removed by pg_down.sh.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947
F=$G/repo/Blockchain/Dev/docker/init/04-sprint2-service-tables.sql
sed -n '152,223p' $F > $G/logs/gov_ddl.sql
docker run -d --name gate129-pg -e POSTGRES_PASSWORD=gate129super -p 127.0.0.1:55129:5432 postgres:15-alpine; echo "run rc=$?"
for i in $(seq 1 30); do docker exec gate129-pg pg_isready -U postgres -q && break; sleep 1; done
sleep 2
docker exec -i gate129-pg psql -v ON_ERROR_STOP=1 -U postgres -q < $G/logs/gov_ddl.sql; echo "ddl rc=$?"
docker exec -i gate129-pg psql -v ON_ERROR_STOP=1 -U postgres -q < $G/scripts/schema.sql; echo "schema rc=$?"
docker exec gate129-pg psql -U postgres -tAc "select version(); select rolname, rolsuper, rolbypassrls from pg_roles where rolname='gate_app'; select relname, relrowsecurity, relforcerowsecurity from pg_class where relname='users';"
