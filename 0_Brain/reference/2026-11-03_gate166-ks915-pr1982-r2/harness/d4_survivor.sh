#!/bin/bash
# D4: drive the dangerous-direction survivor r2_cand_no_anyhash on the form it opens, head as control.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2/harness/lib.sh
NM="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules"
L=$W/runs/d4; mkdir -p "$L"; GB=$W/runs/d3C/golden_blankadmin.env.bin
for v in head r2_cand_no_anyhash; do
  for line in 'NODE_ENV=production#x' 'DATABASE_URL=postgres://u:p@gate166rmt.host/x#@localhost/y'; do
    [[ $v == head ]] && SCRIPT_SRC=$R/Blockchain/Dev/scripts/restore-local-secrets.sh || SCRIPT_SRC=$W/mut/scripts/$v.sh
    export SCRIPT_SRC; id=$v-$(printf %s "$line" | shasum | cut -c1-6)
    c="$(SCRIPT_SRC=$SCRIPT_SRC mkclone d4-$id)" || continue; e="$c/Blockchain/Dev/.env"; { cat "$GB"; printf '%s\n' "$line"; } > "$e"
    cp "$e" "$L/$id.pre.env.bin"; rc=$(run "$c" "$L/$id.log")
    dn=$(node -e 'const d=require(process.argv[1]+"/dotenv");const o=d.parse(require("fs").readFileSync(process.argv[2]));process.stdout.write((o.NODE_ENV||"")+" | db-has-marker="+String((o.DATABASE_URL||"").includes("gate166rmt")))' "$NM" "$L/$id.pre.env.bin")
    printf '%-20s rc=%s admin_now_set=%s dotenv_reads=[%s] | %s\n' "$v" "$rc" "$([[ -n "$(valof "$e" ADMIN_USER_PASSWORD)" ]] && echo y || echo n)" "$dn" "$line"
  done
done
