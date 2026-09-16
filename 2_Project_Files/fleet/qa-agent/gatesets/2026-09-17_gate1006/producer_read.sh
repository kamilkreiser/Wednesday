#!/bin/zsh
# producer_read.sh — READ-ONLY: the error producers upstream of demo-service's errorHandler at head, and the
# express / body-parser versions that decide their shape. Read verbs only (git show, git grep, cat-file).
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1006'
H=86fe59e6bf07108142fb3dbd06bef8747d2a4687
D=Blockchain/Dev/services/demo-service
echo "producer_read $(date '+%Y-%m-%d %H:%M:%S %Z') at head $H"
mkdir -p "$G/src/demo-service"
for f in package.json Dockerfile src/index.ts src/middleware/demoGuard.ts src/routes/health.ts src/routes/persona.ts src/routes/state.ts src/routes/reset.ts src/routes/scenario.ts src/services/authClient.ts src/services/resetService.ts; do
  out="$G/src/demo-service/$(echo $f | tr '/' '_')"
  git -C "$R" show "$H:$D/$f" > "$out"
  echo "dumped $f blob $(git -C "$R" rev-parse "$H:$D/$f") lines $(wc -l < "$out" | tr -d ' ')"
done
echo "--- package.json deps"
/usr/bin/grep -n -i -E '"(express|body-parser|cors|helmet|cookie-parser|morgan|axios|@secuura/shared)"' "$G/src/demo-service/package.json"
echo "--- lockfile: express / body-parser / finalhandler / raw-body resolved (demo-service package-lock.json)"
git -C "$R" show "$H:$D/package-lock.json" | python3 -c '
import json,sys
d=json.load(sys.stdin); p=d.get("packages",{})
for k in sorted(p):
    n=k.split("node_modules/")[-1]
    if n in ("express","body-parser","finalhandler","raw-body","http-errors","axios","cors"): print(" ", k, p[k].get("version"))
'
echo "--- root Dev lockfile: the same (hoisted install the tests actually load)"
git -C "$R" show "$H:Blockchain/Dev/package-lock.json" | python3 -c '
import json,sys
d=json.load(sys.stdin); p=d.get("packages",{})
for k in sorted(p):
    n=k.split("node_modules/")[-1]
    if n in ("express","body-parser","finalhandler","raw-body","http-errors") and k.count("node_modules/")==1 or ("demo-service" in k and n in ("express","body-parser","finalhandler")): print(" ", k, p[k].get("version"))
'
echo "--- next( / throw / status( in demo-service src (non-test) — the producers (git grep -n -I -E, positive control: errorHandler.ts res.status)"
git -C "$R" grep -n -I -E 'next\(|throw |\.status\(|statusCode|\.status =|asyncHandler|catch \(' "$H" -- "$D/src" ':!*__tests__*'
echo "--- rejectNulBytes in packages/shared (the guard between parser and routes)"
git -C "$R" grep -n -I -F 'rejectNulBytes' "$H" -- Blockchain/Dev/packages/shared/src ':!*__tests__*'
