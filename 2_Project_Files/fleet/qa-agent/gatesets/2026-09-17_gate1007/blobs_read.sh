#!/bin/zsh
# blobs_read.sh — #1007 drafter: full blob shas of the launcher's JUDGED files at develop 40fe4db69 and head b28ed490a, read with rev-parse in the
# DRAFTER'S OWN CLONE (not the Secuura checkout). Cross-checked against git show | git hash-object --stdin (no -w: nothing written).
C=$(python3 -c "import json;print(json.load(open('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007/drafter_paths.json'))['C'])")
D=40fe4db6963cd11dba06bd46e0b00af39e68ef3a; H=b28ed490ada70df2056763f4512c98443285a694
echo "blobs_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
for f in services/api-gateway/src/routes/system-status.ts services/api-gateway/src/index.ts services/api-gateway/vitest.config.ts services/api-gateway/vitest.setup.ts services/api-gateway/package.json services/api-gateway/tsconfig.json eslint.config.mjs; do
  p="Blockchain/Dev/$f"
  bd=$(git -C "$C" rev-parse "$D:$p" 2>&1); bh=$(git -C "$C" rev-parse "$H:$p" 2>&1)
  hx=$(git -C "$C" show "$D:$p" | git hash-object --stdin)
  echo "$f develop $bd head $bh same $([ "$bd" = "$bh" ] && echo yes || echo NO) hash-object-check $([ "$hx" = "$bd" ] && echo ok || echo MISMATCH)"
done
