#!/bin/bash
# Q4 (gateway runner) + gateway shape for Q3: the REAL runStartupMigrations() over tsx, MIGRATIONS_DIR override.
. /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/harness/lib.sh
NM="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules"
GWNM="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/services/api-gateway/node_modules"
N57=057_ks1256_gateway_settings_store.sql; N58=058_ks1401_tenant_isolation_after_039.sql
URL(){ printf 'postgresql://postgres@127.0.0.1:%s/%s' $PORT "$1"; }
BOOT(){ # $1 db $2 migrations dir
  bash -c 'cd "$1" && env -i PATH="/opt/homebrew/bin:/usr/bin:/bin" HOME="$2/home" TMPDIR="$2/tmp" NODE_PATH="$3:$4" DATABASE_URL="$5" MIGRATIONS_DIR="$6" NODE_ENV=test LOG_LEVEL=info node "$4/tsx/dist/cli.mjs" "$2/harness/boot_driver.ts"' _ "$WD/cwd" "$WD" "$GWNM" "$NM" "$(URL $1)" "$2"
}
st(){ echo "057rec=$(rec $1 $N57) 058rec=$(rec $1 $N58) settings_tbl=$(S $1 "SELECT to_regclass('public.svc_gateway_settings') IS NOT NULL")"; }
echo "=== GW-shape (Q3 gateway path): docker/init, then real runStartupMigrations over <=056 (base), then over <=056+058 (head)"
mkdb g_1 >/dev/null
for f in "$DEV"/docker/init/0[1-9]*.sql; do P g_1 -f "$f" >> $WD/tmp/g1_init.log 2>&1 || true; done
D56=$(mkrun gw56)/migrations; D58=$(mkrun gw58 "$F058_REAL")/migrations; D5758=$(mkrun gw5758 "$F057" "$F058_REAL")/migrations
BOOT g_1 "$D56" > $WD/runs/gw_1a.log 2>&1; grep -oE 'SUMMARY .{0,160}|THREW.*' $WD/runs/gw_1a.log | sed 's/^/  base boot /'
for t in $TABLES; do echo "   base $(reading g_1 $t)"; done
grants g_1; plant g_1
echo "   base matrix:"; matrix g_1 | sed 's/^/    M /'
BOOT g_1 "$D58" > $WD/runs/gw_1b.log 2>&1; grep -oE 'SUMMARY .{0,160}|THREW.*' $WD/runs/gw_1b.log | sed 's/^/  head boot /'
grep -oE 'applied 058[^"]*|migration 058[^}]*' $WD/runs/gw_1b.log | head -3 | sed 's/^/  /'
for t in $TABLES; do echo "   head $(reading g_1 $t)"; done
echo "   head NULLs=$(nulls g_1) DEF=$(defs g_1) 058rec=$(rec g_1 $N58)"
echo "   head matrix:"; matrix g_1 | sed 's/^/    M /'
echo "   second boot (CORE runs again after 058 recorded):"; BOOT g_1 "$D58" > $WD/runs/gw_1c.log 2>&1; grep -oE 'SUMMARY .{0,160}' $WD/runs/gw_1c.log | sed 's/^/    /'
for t in $TABLES; do echo "   boot2 $(reading g_1 $t) pol=$(polmd5 g_1 $t | cut -c1-12)"; done
echo "=== Q4-GW-A: 058 first, then 057 added (gateway runner)"
mkdb g_a tpl056 >/dev/null
BOOT g_a "$D58" > $WD/runs/gw_a1.log 2>&1; echo "  step1 $(grep -oE 'SUMMARY .{0,120}' $WD/runs/gw_a1.log) :: $(st g_a)"
BOOT g_a "$D5758" > $WD/runs/gw_a2.log 2>&1; echo "  step2 $(grep -oE 'SUMMARY .{0,120}' $WD/runs/gw_a2.log) :: $(st g_a)"
echo "  applied lines step2: $(grep -oE 'applied 05[78][a-z0-9_]*' $WD/runs/gw_a2.log | tr '\n' ' ')"
echo "=== Q4-GW-B: 057 first, then 058"
mkdb g_b tpl056 >/dev/null; D57=$(mkrun gw57 "$F057")/migrations
BOOT g_b "$D57" > $WD/runs/gw_b1.log 2>&1; echo "  step1 $(grep -oE 'SUMMARY .{0,120}' $WD/runs/gw_b1.log) :: $(st g_b)"
BOOT g_b "$D5758" > $WD/runs/gw_b2.log 2>&1; echo "  step2 $(grep -oE 'SUMMARY .{0,120}' $WD/runs/gw_b2.log) :: $(st g_b)"
echo "  applied lines step2: $(grep -oE 'applied 05[78][a-z0-9_]*' $WD/runs/gw_b2.log | tr '\n' ' ')"
