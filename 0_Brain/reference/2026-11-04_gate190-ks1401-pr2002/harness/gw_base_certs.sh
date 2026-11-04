#!/bin/bash
# GW base control: docker/init + real runStartupMigrations over <=056, plant certifications A,A,B, read the matrix (no 058).
. /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/harness/lib.sh
NM="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules"
GWNM="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/services/api-gateway/node_modules"
mkdb g_base >/dev/null
for f in "$DEV"/docker/init/0[1-9]*.sql; do P g_base -f "$f" >> $WD/tmp/gbase_init.log 2>&1 || true; done
bash -c 'cd "$1" && env -i PATH="/opt/homebrew/bin:/usr/bin:/bin" HOME="$2/home" TMPDIR="$2/tmp" NODE_PATH="$3:$4" DATABASE_URL="$5" MIGRATIONS_DIR="$6" NODE_ENV=test node "$4/tsx/dist/cli.mjs" "$2/harness/boot_driver.ts"' _ "$WD/cwd" "$WD" "$GWNM" "$NM" "postgresql://postgres@127.0.0.1:$PORT/g_base" "$WD/scratch/run_gw56/migrations" > $WD/runs/gw_base.log 2>&1
grep -oE 'SUMMARY .{0,100}' $WD/runs/gw_base.log
grants g_base
P g_base -c "INSERT INTO certifications (id,certification_type,tenant_id) VALUES (gen_random_uuid(),'fx','$TA'),(gen_random_uuid(),'fx','$TA'),(gen_random_uuid(),'fx','$TB')"
echo "g_base $(reading g_base certifications)"
echo "g_base (base, no 058) $(matrix g_base | grep certif)"
echo "W7 own insert at GW base: $(AS g_base secuura_app A "INSERT INTO certifications (id,certification_type,tenant_id) VALUES (gen_random_uuid(),'fx','$TA')")"
