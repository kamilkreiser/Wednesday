#!/bin/bash
# G189: create the throwaway DB on the gate's own cluster (127.0.0.1:56390), apply 057 twice, read the seed.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate189-ks1256-pr2001
PGB=/opt/homebrew/opt/postgresql@15/bin
export HOME=$W/home
psq() { "$PGB/psql" -X -v ON_ERROR_STOP=1 -h 127.0.0.1 -p 56390 -U g189su "$@"; }
M=$W/repo/Blockchain/Dev/migrations/057_ks1256_gateway_settings_store.sql
DB=${1:-g189}
psq -d postgres -c "DROP DATABASE IF EXISTS $DB" -c "CREATE DATABASE $DB"
psq -d postgres -tA -c "SELECT 1 FROM pg_roles WHERE rolname='g189app'" | grep -q 1 || psq -d postgres -c "CREATE ROLE g189app LOGIN"
# as docker/init/01-create-app-role.sh lines 64-71 do for secuura_app
psq -d $DB -c "GRANT USAGE ON SCHEMA public TO g189app" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO g189app"
psq -d $DB -f "$M"; echo "apply1 rc=$?"
psq -d $DB -At -c "SELECT key, origin, settings::text FROM svc_gateway_settings"
psq -d $DB -f "$M"; echo "apply2 rc=$?"
psq -d $DB -At -c "SELECT count(*), string_agg(origin, ',') FROM svc_gateway_settings"
psq -d $DB -At -c "SELECT has_table_privilege('g189app','svc_gateway_settings','SELECT'), has_table_privilege('g189app','svc_gateway_settings','INSERT'), has_table_privilege('g189app','svc_gateway_settings','UPDATE')"
