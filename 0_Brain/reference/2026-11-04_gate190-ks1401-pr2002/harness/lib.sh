#!/bin/bash
# Gate 190 harness library. Everything lives under WD. Cluster: WD/tmp/pgdata, socket WD/tmp/s.
WD=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002
PGB=/opt/homebrew/opt/postgresql@15/bin
PORT=55190
SOCK=$WD/tmp/s
DEV=$WD/scratch/dev/Blockchain/Dev
F058_REAL=$WD/scratch/real/058_ks1401_tenant_isolation_after_039.sql
F057=$WD/scratch/real/057_ks1256_gateway_settings_store.sql
export TMPDIR=$WD/tmp HOME=$WD/home PGCONNECT_TIMEOUT=5
DEF=a0000000-0000-4000-8000-000000000001
TA=c0000000-0000-4000-8000-00000000000a
TB=b0000000-0000-4000-8000-00000000000b
P(){ "$PGB/psql" -h "$SOCK" -p $PORT -U postgres -d "$1" -v ON_ERROR_STOP=1 -q "${@:2}"; }
S(){ "$PGB/psql" -h "$SOCK" -p $PORT -U postgres -d "$1" -tAc "$2" 2>&1 | tail -1; }
# as a role with a context: $1 db, $2 role, $3 ctx (none|A|B|DEF|EMPTY|BYP), $4 sql
AS(){
  local ctx=""
  case "$3" in
    none) ctx="";;
    A) ctx="SELECT set_config('app.current_tenant_id','$TA',false);";;
    B) ctx="SELECT set_config('app.current_tenant_id','$TB',false);";;
    DEF) ctx="SELECT set_config('app.current_tenant_id','$DEF',false);";;
    EMPTY) ctx="SELECT set_config('app.current_tenant_id','',false);";;
    BYP) ctx="SELECT set_config('app.tenant_scope_bypass','platform_admin',false);";;
  esac
  "$PGB/psql" -h "$SOCK" -p $PORT -U postgres -d "$1" -tAq -c "SET ROLE $2;" -c "$ctx" -c "$4" 2>&1 | grep -v '^$' | grep -v '^a0000000\|^c0000000\|^b0000000\|^platform_admin$' | tail -1
}
TCPURL(){ printf 'postgresql://%s@127.0.0.1:%s/%s' "${2:-postgres}" "$PORT" "$1"; }
mkdb(){ S postgres "DROP DATABASE IF EXISTS $1;" >/dev/null; S postgres "CREATE DATABASE $1 ${2:+TEMPLATE $2};"; }
# runner dir: $1 name, then list of extra files to include beyond develop's <=056 set
mkrun(){
  local d=$WD/scratch/run_$1; rm -rf "$d"; mkdir -p "$d/migrations" "$d/scripts"
  cp "$DEV"/migrations/*.sql "$d/migrations/"
  shift; for f in "$@"; do cp "$f" "$d/migrations/$(basename "$f" | sed 's/^mut_[A-Z0-9]*_//')"; done
  # The ONLY edit to the real runner: its fixed /tmp/migrate-err.log (line 127/128/133) -> the workdir.
  sed "s|/tmp/migrate-err.log|$WD/tmp/migrate-err.log|g" "$DEV/scripts/run-migrations.sh" > "$d/scripts/run-migrations.sh"
  echo "$d"
}
# run the real runner: $1 rundir, $2 db, $3 user (default postgres) ; prints rc on last line
runmig(){
  bash -c 'cd "$1" && env -i PATH="'"$PGB"':/usr/bin:/bin" HOME="'"$WD/home"'" TMPDIR="'"$WD/tmp"'" DATABASE_URL="$2" PLATFORM_DATABASE_URL="$3" sh scripts/run-migrations.sh; echo "RC=$?"' _ "$1" "$(TCPURL "$2" "${3:-postgres}")" "$(TCPURL plat_$2 postgres)"
}
reading(){ S "$1" "SELECT c.relname||':rls='||c.relrowsecurity||',force='||c.relforcerowsecurity||',pol='||(SELECT count(*) FROM pg_policies p WHERE p.schemaname='public' AND p.tablename=c.relname)||',tid='||EXISTS(SELECT 1 FROM information_schema.columns k WHERE k.table_schema='public' AND k.table_name=c.relname AND k.column_name='tenant_id') FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relname='$2'"; }
plant(){ # $1 db ; plants A,A,B,NULL on all four (certifications only if tenant_id exists)
  P "$1" -c "
  INSERT INTO charge_events (id,event_type,tenant_id,amount) VALUES ('g-a1','fx','$TA',1),('g-a2','fx','$TA',1),('g-b1','fx','$TB',1),('g-n1','fx',NULL,1);
  INSERT INTO oauth_apps (id,name,client_id,tenant_id) VALUES ('10000000-0000-4000-8000-0000000000a1','a1','ca1','$TA'),('10000000-0000-4000-8000-0000000000a2','a2','ca2','$TA'),('10000000-0000-4000-8000-0000000000b1','b1','cb1','$TB'),('10000000-0000-4000-8000-0000000000f1','n1','cn1',NULL);
  INSERT INTO svc_webhooks (id,url,secret_v2,tenant_id) VALUES ('20000000-0000-4000-8000-0000000000a1','https://x.invalid/a1','s','$TA'),('20000000-0000-4000-8000-0000000000a2','https://x.invalid/a2','s','$TA'),('20000000-0000-4000-8000-0000000000b1','https://x.invalid/b1','s','$TB'),('20000000-0000-4000-8000-0000000000f1','https://x.invalid/n1','s',NULL);
  "
  if [ "$(S "$1" "SELECT count(*) FROM information_schema.columns WHERE table_schema='public' AND table_name='certifications' AND column_name='tenant_id'")" = 1 ]; then
    P "$1" -c "INSERT INTO certifications (id,certification_type,tenant_id) VALUES ('30000000-0000-4000-8000-0000000000a1','fx','$TA'),('30000000-0000-4000-8000-0000000000a2','fx','$TA'),('30000000-0000-4000-8000-0000000000b1','fx','$TB'),('30000000-0000-4000-8000-0000000000f1','fx',NULL);"
  else
    P "$1" -c "INSERT INTO certifications (id,certification_type) VALUES ('30000000-0000-4000-8000-0000000000f1','fx'),('30000000-0000-4000-8000-0000000000f2','fx');"
  fi
}
grants(){ P "$1" -c "GRANT SELECT,INSERT,UPDATE,DELETE ON charge_events,certifications,oauth_apps,svc_webhooks TO secuura_app; GRANT USAGE ON SCHEMA public TO secuura_app;" ; }
# kintsugi bend (Seat B 50th 2026-09-30 reading): charge_events rls off/0 policies, certifications tenant_id + forced + 0 policies
bend_k(){ P "$1" -c "
  ALTER TABLE certifications ADD COLUMN IF NOT EXISTS tenant_id UUID;
  DROP POLICY IF EXISTS tenant_isolation ON certifications;
  ALTER TABLE certifications ENABLE ROW LEVEL SECURITY; ALTER TABLE certifications FORCE ROW LEVEL SECURITY;
  DROP POLICY IF EXISTS tenant_isolation ON charge_events;
  ALTER TABLE charge_events NO FORCE ROW LEVEL SECURITY; ALTER TABLE charge_events DISABLE ROW LEVEL SECURITY;"; }
# reader matrix: one line per table: ctx=count for the app role
TABLES="charge_events certifications oauth_apps svc_webhooks"
matrix(){ local db=$1 role=${2:-secuura_app} t c out
  for t in $TABLES; do out="$t"
    for c in none EMPTY A B DEF BYP; do out="$out $c=$(AS $db $role $c "SELECT count(*) FROM $t")"; done
    echo "$out"; done; }
nulls(){ S "$1" "SELECT (SELECT count(*) FROM charge_events WHERE tenant_id IS NULL)||'/'||(SELECT count(*) FROM certifications WHERE tenant_id IS NULL)||'/'||(SELECT count(*) FROM oauth_apps WHERE tenant_id IS NULL)||'/'||(SELECT count(*) FROM svc_webhooks WHERE tenant_id IS NULL)"; }
defs(){ S "$1" "SELECT (SELECT count(*) FROM charge_events WHERE tenant_id='$DEF')||'/'||(SELECT count(*) FROM certifications WHERE tenant_id='$DEF')||'/'||(SELECT count(*) FROM oauth_apps WHERE tenant_id='$DEF')||'/'||(SELECT count(*) FROM svc_webhooks WHERE tenant_id='$DEF')"; }
nonnull_md5(){ S "$1" "SELECT md5((SELECT string_agg(id||':'||tenant_id,',' ORDER BY id) FROM charge_events WHERE id IN ('g-a1','g-a2','g-b1'))||(SELECT coalesce(string_agg(id||':'||tenant_id,',' ORDER BY id),'') FROM certifications WHERE id::text LIKE '%a1' OR id::text LIKE '%a2' OR id::text LIKE '%b1')||(SELECT string_agg(id||':'||tenant_id,',' ORDER BY id) FROM oauth_apps WHERE tenant_id IN ('$TA','$TB'))||(SELECT string_agg(id||':'||tenant_id,',' ORDER BY id) FROM svc_webhooks WHERE tenant_id IN ('$TA','$TB')))"; }
polmd5(){ S "$1" "SELECT coalesce(md5(qual),'-')||'/'||coalesce(md5(with_check),'-')||'/'||permissive||'/'||array_to_string(roles,',') FROM pg_policies WHERE schemaname='public' AND tablename='$2' AND policyname='tenant_isolation'"; }
rec(){ S "$1" "SELECT count(*) FROM _secuura_migrations WHERE filename='$2'"; }
