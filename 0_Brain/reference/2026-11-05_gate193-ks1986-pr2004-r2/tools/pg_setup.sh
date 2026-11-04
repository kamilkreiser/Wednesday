#!/bin/bash
# Gate 193: own PostgreSQL 15 cluster. Socket only (listen_addresses empty), /private/tmp/g193/s, port 55493.
# LINEAGE: Seat F 33rd's tools/pg_setup_f33.sh (itself F 32nd's / gate 192's recipe), re-keyed to the gate's clone and cluster.
# Databases: g_ten (caller), g_t02..g_t10, g_plat (registry). g_nodb must NOT exist. Schemas by git show at the built base.
set -u
K=/opt/homebrew/opt/postgresql@15/bin; D=/private/tmp/g193; P=55493
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2
R=$W/repo
[ -e "$D/pgdata" ] && { echo "REFUSE: $D/pgdata exists"; exit 2; }
mkdir -p "$D/s" $W/scratch
git -C $R show 035685291b9d58ae6ea8ba5f05adf9379f9c2944:Blockchain/Dev/docker/init/01-schema.sql > $W/scratch/01-schema.sql || exit 3
git -C $R show 035685291b9d58ae6ea8ba5f05adf9379f9c2944:Blockchain/Dev/docker/init-platform/01-platform-schema.sql > $W/scratch/01-platform-schema.sql || exit 3
"$K/initdb" -D "$D/pgdata" -U g193 -A trust -E UTF8 > $W/runs/initdb.log 2>&1; echo "initdb rc=$?"
"$K/pg_ctl" -D "$D/pgdata" -l $W/runs/pg.log -o "-k $D/s -c listen_addresses= -p $P" -w start > $W/runs/pgctl_start.out 2>&1; echo "pg_ctl start rc=$?"
head -1 "$D/pgdata/postmaster.pid" > $W/runs/postmaster.pid; echo "postmaster PID $(cat $W/runs/postmaster.pid)"
Q() { "$K/psql" -h "$D/s" -p $P -U g193 -X -q "$@"; }
Q -d postgres -c "CREATE DATABASE g_ten" && Q -d g_ten -f $W/scratch/01-schema.sql > $W/runs/schema_ten.log 2>&1
echo "schema g_ten ERROR lines: $(grep -c ERROR $W/runs/schema_ten.log)"
Q -d g_ten -c "ALTER TABLE documents ADD COLUMN IF NOT EXISTS parent_document_id uuid; ALTER TABLE documents ADD COLUMN IF NOT EXISTS tenant_id uuid;"
for n in 02 03 04 05 06 07 08 09 10; do Q -d postgres -c "CREATE DATABASE g_t$n TEMPLATE g_ten" || echo "createdb g_t$n FAILED"; done
Q -d postgres -c "CREATE DATABASE g_plat" && Q -d g_plat -f $W/scratch/01-platform-schema.sql > $W/runs/schema_plat.log 2>&1
echo "schema g_plat ERROR lines: $(grep -c ERROR $W/runs/schema_plat.log)"
Q -d postgres -At -c "SELECT string_agg(datname, ' ' ORDER BY datname) FROM pg_database WHERE datname LIKE 'g\_%'"
Q -d g_ten -At -c "SELECT count(*) FROM information_schema.columns WHERE table_name='documents' AND column_name IN ('parent_document_id','tenant_id','issuer_organization_id','owner_user_id')"
Q -d g_plat -At -c "SELECT count(*) FROM information_schema.tables WHERE table_name IN ('platform_document_registry','tenants')"
Q -d postgres -At -c "SHOW listen_addresses"
