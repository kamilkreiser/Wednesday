#!/bin/bash
# Q4 order with PR 2001's 057 (both orders + fresh), Q5 re-run safety and failure atomicity. Real run-migrations.sh.
. /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/harness/lib.sh
N57=057_ks1256_gateway_settings_store.sql; N58=058_ks1401_tenant_isolation_after_039.sql
st(){ echo "057rec=$(rec $1 $N57) 058rec=$(rec $1 $N58) settings_tbl=$(S $1 "SELECT to_regclass('public.svc_gateway_settings') IS NOT NULL") settings_rows=$(S $1 "SELECT count(*) FROM svc_gateway_settings" | grep -E '^[0-9]+$' || echo absent) ce=$(reading $1 charge_events) order=$(S $1 "SELECT string_agg(filename,'<' ORDER BY applied_at, filename) FROM _secuura_migrations WHERE filename IN ('$N57','$N58')")"; }
echo "=== Q4-A: 058 merges first (dir = <=056 + 058), then PR 2001 merges (dir gains 057)"
mkdb o_a tpl056 >/dev/null; mkdb plat_o_a plat_tpl056 >/dev/null; bend_k o_a
runmig "$(mkrun o58 "$F058_REAL")" o_a > $WD/runs/q4_a1.log 2>&1; grep -E 'Applying|Summary|RC=' $WD/runs/q4_a1.log | sed 's/^/  step1 /'
echo "  after step1: $(st o_a)"
runmig "$(mkrun o5758 "$F057" "$F058_REAL")" o_a > $WD/runs/q4_a2.log 2>&1; grep -E 'Applying|Summary|RC=' $WD/runs/q4_a2.log | sed 's/^/  step2 /'
echo "  after step2: $(st o_a)"
echo "=== Q4-B: 057 merges first, then 058"
mkdb o_b tpl056 >/dev/null; mkdb plat_o_b plat_tpl056 >/dev/null; bend_k o_b
runmig "$(mkrun o57 "$F057")" o_b > $WD/runs/q4_b1.log 2>&1; grep -E 'Applying|Summary|RC=' $WD/runs/q4_b1.log | sed 's/^/  step1 /'
echo "  after step1: $(st o_b)"
runmig "$(mkrun o5758 "$F057" "$F058_REAL")" o_b > $WD/runs/q4_b2.log 2>&1; grep -E 'Applying|Summary|RC=' $WD/runs/q4_b2.log | sed 's/^/  step2 /'
echo "  after step2: $(st o_b)"
echo "=== Q4-C: fresh database, both present (docker/init then the runner over <=056+057+058)"
mkdb o_c >/dev/null; mkdb plat_o_c >/dev/null
for f in "$DEV"/docker/init/0[1-9]*.sql; do P o_c -f "$f" >> $WD/tmp/o_c_init.log 2>&1 || echo "INITFAIL $f"; done
runmig "$(mkrun o5758 "$F057" "$F058_REAL")" o_c > $WD/runs/q4_c.log 2>&1; grep -E 'Applying 05[78]|Summary|RC=' $WD/runs/q4_c.log | sed 's/^/  /'
echo "  after: $(st o_c)"; for t in $TABLES; do echo "   $(reading o_c $t)"; done
echo "  CONTROL the runner does skip a recorded file: rerun on o_c -> $(runmig "$(mkrun o5758 "$F057" "$F058_REAL")" o_c 2>&1 | grep -E 'Summary' )"

echo "=== Q5-1: re-run 058 on a database where it is already applied (tracker row deleted so the runner re-applies it)"
mkdb r_1 s_k >/dev/null; mkdb plat_r_1 plat_tpl056 >/dev/null
B_MD=$(S r_1 "SELECT md5(string_agg(id||':'||coalesce(tenant_id::text,'-'),',' ORDER BY id)) FROM charge_events")
B_POL=$(for t in $TABLES; do polmd5 r_1 $t; done | md5)
S r_1 "DELETE FROM _secuura_migrations WHERE filename='$N58'" >/dev/null
runmig "$(mkrun head "$F058_REAL")" r_1 > $WD/runs/q5_1.log 2>&1; grep -E 'Applying|Summary|RC=' $WD/runs/q5_1.log | sed 's/^/  /'
A_MD=$(S r_1 "SELECT md5(string_agg(id||':'||coalesce(tenant_id::text,'-'),',' ORDER BY id)) FROM charge_events")
A_POL=$(for t in $TABLES; do polmd5 r_1 $t; done | md5)
echo "  rows md5 before/after: ${B_MD:0:12}/${A_MD:0:12}  policies md5 before/after: ${B_POL:0:12}/${A_POL:0:12}  058rec=$(rec r_1 $N58)"
echo "  direct psql re-apply NOTICEs:"; P r_1 -f "$F058_REAL" 2>&1 | grep -oE 'KS-1401: [a-z_]+\.tenant_id had [0-9]+ NULL rows|REPLACED|CREATED' | sort | uniq -c | sed 's/^/    /'

echo "=== Q5-2: failure mid-way, planted absent table (svc_webhooks is LAST in the loop, so 3 tables were already altered in-transaction)"
mkdb f_1 tpl056 >/dev/null; mkdb plat_f_1 plat_tpl056 >/dev/null; bend_k f_1; grants f_1; plant f_1
P f_1 -c "DROP TABLE svc_webhooks CASCADE" 2>/dev/null
echo "  before: $(reading f_1 charge_events) | $(reading f_1 certifications) nulls ce/cert=$(S f_1 "SELECT (SELECT count(*) FROM charge_events WHERE tenant_id IS NULL)||'/'||(SELECT count(*) FROM certifications WHERE tenant_id IS NULL)")"
runmig "$(mkrun head "$F058_REAL")" f_1 > $WD/runs/q5_2.log 2>&1; grep -E 'Applying|FAILED|KS-1401|Summary|RC=' $WD/runs/q5_2.log | cut -c1-160 | sed 's/^/  /'
echo "  after:  $(reading f_1 charge_events) | $(reading f_1 certifications) nulls ce/cert=$(S f_1 "SELECT (SELECT count(*) FROM charge_events WHERE tenant_id IS NULL)||'/'||(SELECT count(*) FROM certifications WHERE tenant_id IS NULL)")  058rec=$(rec f_1 $N58)"

echo "=== Q5-3: lock_timeout path: another session holds ACCESS SHARE on certifications (2nd table) for 20s"
mkdb f_2 tpl056 >/dev/null; mkdb plat_f_2 plat_tpl056 >/dev/null; bend_k f_2; grants f_2; plant f_2
( "$PGB/psql" -h "$SOCK" -p $PORT -U postgres -d f_2 -q -c "BEGIN; LOCK TABLE certifications IN ACCESS SHARE MODE; SELECT pg_sleep(20); COMMIT;" > $WD/tmp/locker.log 2>&1 & echo $! > $WD/tmp/locker.pid; wait ) &
sleep 1; echo "  locker psql pid $(cat $WD/tmp/locker.pid); lock held: $(S f_2 "SELECT count(*) FROM pg_locks l JOIN pg_class c ON c.oid=l.relation WHERE c.relname='certifications' AND l.mode='AccessShareLock' AND l.granted")"
T0=$(date +%s)
runmig "$(mkrun head "$F058_REAL")" f_2 > $WD/runs/q5_3.log 2>&1; T1=$(date +%s)
grep -E 'Applying|FAILED|lock|Summary|RC=' $WD/runs/q5_3.log | cut -c1-160 | sed 's/^/  /'
echo "  runner wall ${T1}-${T0}=$((T1-T0))s (lock held 20s)"
echo "  after: $(reading f_2 charge_events) nulls ce=$(S f_2 "SELECT count(*) FROM charge_events WHERE tenant_id IS NULL") 058rec=$(rec f_2 $N58)"
wait
echo "  locker finished; retry after release:"; runmig "$(mkrun head "$F058_REAL")" f_2 > $WD/runs/q5_3b.log 2>&1; grep -E 'Summary|RC=' $WD/runs/q5_3b.log | sed 's/^/  /'; echo "  after retry: $(reading f_2 charge_events) 058rec=$(rec f_2 $N58)"
