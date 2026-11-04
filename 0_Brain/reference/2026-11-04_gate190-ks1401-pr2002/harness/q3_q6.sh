#!/bin/bash
# Q3 + Q6: base vs head reader/writer matrix on two shapes, 058 applied through the REAL run-migrations.sh
. /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/harness/lib.sh
writes(){ local db=$1
  echo "W1 app A inserts a B-tenant charge_event: $(AS $db secuura_app A "INSERT INTO charge_events (id,event_type,tenant_id,amount) VALUES ('w1-$RANDOM','fx','$TB',1)" | cut -c1-80)"
  echo "W2 app A inserts its own charge_event:     $(AS $db secuura_app A "INSERT INTO charge_events (id,event_type,tenant_id,amount) VALUES ('w2-$RANDOM','fx','$TA',1)" | cut -c1-80)"
  echo "W3 app no-GUC inserts DEF charge_event:    $(AS $db secuura_app none "INSERT INTO charge_events (id,event_type,tenant_id,amount) VALUES ('w3-$RANDOM','fx','$DEF',1)" | cut -c1-80)"
  echo "W4 app BYP inserts NULL-tenant charge_event:$(AS $db secuura_app BYP "INSERT INTO charge_events (id,event_type,tenant_id,amount) VALUES ('w4-$RANDOM','fx',NULL,1)" | cut -c1-80)"
  echo "W5 app A updates B's charge_event (rows):  $(AS $db secuura_app A "WITH u AS (UPDATE charge_events SET amount=amount WHERE id='g-b1' RETURNING 1) SELECT count(*) FROM u")"
  echo "W6 app A moves own row to tenant B:        $(AS $db secuura_app A "UPDATE charge_events SET tenant_id='$TB' WHERE id='g-a1'" | cut -c1-80)"
  echo "W7 app A inserts own certification:        $(AS $db secuura_app A "INSERT INTO certifications (id,certification_type,tenant_id) VALUES (gen_random_uuid(),'fx','$TA')" | cut -c1-80)"
  echo "W8 app A inserts B certification:          $(AS $db secuura_app A "INSERT INTO certifications (id,certification_type,tenant_id) VALUES (gen_random_uuid(),'fx','$TB')" | cut -c1-80)"
  echo "W9 app A inserts B svc_webhook:            $(AS $db secuura_app A "INSERT INTO svc_webhooks (id,url,secret_v2,tenant_id) VALUES (gen_random_uuid(),'https://x.invalid/w9','s','$TB')" | cut -c1-80)"
  echo "P1 app A reads ids of own charge_events:   $(AS $db secuura_app A "SELECT string_agg(id,',' ORDER BY id) FROM charge_events WHERE id LIKE 'g-%'")"
  echo "P2 app A reads ids of own certifications:  $(AS $db secuura_app A "SELECT string_agg(right(id::text,2),',' ORDER BY id) FROM certifications")"
  echo "P3 app B reads A's charge_event g-a1:      $(AS $db secuura_app B "SELECT count(*) FROM charge_events WHERE id='g-a1'")"
  echo "P4 app DEF reads ex-NULL charge_event g-n1:$(AS $db secuura_app DEF "SELECT count(*) FROM charge_events WHERE id='g-n1'")"
  echo "P5 app DEF explicit WHERE tenant_id=DEF (chargeEvents.ts:205 shape) on g-n1: $(AS $db secuura_app DEF "SELECT count(*) FROM charge_events WHERE id='g-n1' AND tenant_id='$DEF'::uuid")"
}
one(){ local shape=$1; local db=s_$(echo $shape | tr A-Z a-z)
  mkdb $db tpl056 >/dev/null; mkdb plat_$db plat_tpl056 >/dev/null
  [ $shape = K ] && bend_k $db
  grants $db; plant $db
  echo "=== SHAPE $shape BASE (develop 536642104002, 039 recorded, 058 absent)"
  for t in $TABLES; do echo "  $(reading $db $t)  pol=$(polmd5 $db $t)"; done
  echo "  NULLs(ce/cert/oa/wh)=$(nulls $db)  DEF-rows=$(defs $db)  nonnull_md5=$(nonnull_md5 $db | cut -c1-12)"
  matrix $db | sed 's/^/  M /'
  # writes on a throwaway clone so base data stays identical for apply
  mkdb ${db}_w $db >/dev/null; writes ${db}_w | sed 's/^/  /'
  echo "=== SHAPE $shape APPLY 058 via real run-migrations.sh"
  RD=$(mkrun head "$F058_REAL")
  runmig "$RD" $db > $WD/runs/q3_${shape}_apply.log 2>&1
  grep -E 'Applying|Summary|RC=|FAILED' $WD/runs/q3_${shape}_apply.log | sed 's/^/  /'
  echo "  058 recorded: $(rec $db 058_ks1401_tenant_isolation_after_039.sql)"
  echo "=== SHAPE $shape HEAD"
  for t in $TABLES; do echo "  $(reading $db $t)  pol=$(polmd5 $db $t)"; done
  echo "  039 users-policy md5 (control text): $(polmd5 $db users)"
  echo "  NULLs(ce/cert/oa/wh)=$(nulls $db)  DEF-rows=$(defs $db)  nonnull_md5=$(nonnull_md5 $db | cut -c1-12)"
  matrix $db | sed 's/^/  M /'
  mkdb ${db}_w $db >/dev/null; writes ${db}_w | sed 's/^/  /'
}
one K
one D
