#!/bin/bash
# Make the golden completed .env (ADMIN blank, no DATABASE_URL/NODE_ENV lines) the cells start from. Hashes only.
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/harness/lib.sh
mkdir -p $W/runs/golden
G="$(mkclone golden)" || exit 1
rc=$(run "$G" "$W/runs/golden/golden.log"); echo "golden rc=$rc"
awk 'index($0,"ADMIN_USER_PASSWORD=")==1{print "ADMIN_USER_PASSWORD="; next}{print}' "$G/Blockchain/Dev/.env" | grep -v -E '^(DATABASE_URL|NODE_ENV)=' > "$W/runs/golden/golden_blankadmin.env.bin"
echo "golden lines=$(wc -l < $W/runs/golden/golden_blankadmin.env.bin) admin_blank=$(grep -c '^ADMIN_USER_PASSWORD=$' $W/runs/golden/golden_blankadmin.env.bin)"
grep -cE '[0-9a-f]{48}' $W/runs/golden/golden.log
