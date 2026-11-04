#!/bin/bash
# Gate 190 mutant oracle. For a given 058 file, apply it through the REAL run-migrations.sh in 4 scenarios and print a fingerprint.
#   K  : kintsugi-bent shape, runner as postgres (superuser)
#   O  : kintsugi-bent shape, the four tables + tracker owned by mig_owner (NOSUPERUSER NOBYPASSRLS), runner as mig_owner
#   D  : run-migrations.sh shape as built (certifications has no tenant_id, no RLS)
#   X  : kintsugi-bent with svc_webhooks absent
#   L  : (only with LOCK=1) kintsugi-bent, ACCESS SHARE held on certifications for 12s
. /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/harness/lib.sh
F=$1; TAG=$2; N58=058_ks1401_tenant_isolation_after_039.sql
RD=$(mkrun mut_$TAG "$F")
fp(){ local db=$1 role=$2
  echo "rec=$(rec $db $N58) nulls=$(nulls $db) defs=$(defs $db) nn=$(nonnull_md5 $db | cut -c1-8)"
  for t in $TABLES; do echo "$(reading $db $t)"; done
  matrix $db secuura_app
  [ -n "$role" ] && echo "owner-noGUC: $(for t in $TABLES; do printf '%s=%s ' $t "$(AS $db $role none "SELECT count(*) FROM $t")"; done)"
  echo "W1(A->B insert ce): $(AS $db secuura_app A "INSERT INTO charge_events (id,event_type,tenant_id,amount) VALUES ('w1','fx','$TB',1)" | grep -oE 'violates row-level|ERROR' | head -1)"
  echo "W7(A own cert): $(AS $db secuura_app A "INSERT INTO certifications (id,certification_type,tenant_id) VALUES (gen_random_uuid(),'fx','$TA')" | grep -oE 'violates row-level|ERROR' | head -1)"
}
fptext(){ for t in $TABLES; do echo "pol $t $(polmd5 $1 $t)"; done; }
scen(){ local s=$1 db=m_$(echo $TAG | tr A-Z a-z)_$(echo $1 | tr A-Z a-z)
  mkdb $db tpl056 >/dev/null; mkdb plat_$db plat_tpl056 >/dev/null
  case $s in D) ;; *) bend_k $db >/dev/null 2>&1;; esac
  grants $db; plant $db 2>/dev/null
  local user=postgres role=""
  if [ $s = O ]; then
    P $db -c "ALTER TABLE charge_events OWNER TO mig_owner; ALTER TABLE certifications OWNER TO mig_owner; ALTER TABLE oauth_apps OWNER TO mig_owner; ALTER TABLE svc_webhooks OWNER TO mig_owner; ALTER TABLE _secuura_migrations OWNER TO mig_owner; GRANT CREATE, USAGE ON SCHEMA public TO mig_owner;"
    user=mig_owner; role=mig_owner
  fi
  [ $s = X ] && P $db -c "DROP TABLE svc_webhooks CASCADE" 2>/dev/null
  if [ $s = L ]; then
    ( "$PGB/psql" -h "$SOCK" -p $PORT -U postgres -d $db -q -c "BEGIN; LOCK TABLE certifications IN ACCESS SHARE MODE; SELECT pg_sleep(12); COMMIT;" >/dev/null 2>&1 ) &
    LP=$!; sleep 1
  fi
  local t0=$(date +%s)
  runmig "$RD" $db $user > $WD/runs/mut_${TAG}_$s.log 2>&1
  local t1=$(date +%s)
  echo "## $s rc=$(grep -oE 'RC=[0-9]+' $WD/runs/mut_${TAG}_$s.log) applied=$(grep -oE 'applied=[0-9]+ failed=[0-9]+' $WD/runs/mut_${TAG}_$s.log) $( [ $s = L ] && echo "failed_fast=$([ $((t1-t0)) -lt 11 ] && echo yes || echo no)")"
  if [ $s = L ]; then wait $LP; echo "rec=$(rec $db $N58)"; else fp $db $role | sed "s/^/$s /"; fi
  [ $s = K ] && fptext $db | sed "s/^/T /"
}
for s in K O D X ${LOCK:+L}; do scen $s; done
