#!/bin/bash
# G161: drive /register and /forgot-password with the real base and head email.ts (clone in this workdir only).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate161-ks1868-pr1978; R=$W/repo; A=$R/Blockchain/Dev/services/auth; T=$A/src/__tests__/g161-route-driver.test.ts
cp $W/harness/g161-route-driver.test.ts $T
for v in base:66cbe4e52d5afadc9d13ca141200026cc68d5095 head:1062b621269dac98f618a89f10baa51ff49c8c34; do n=${v%%:*}; c=${v#*:}
  git -C $R show $c:Blockchain/Dev/services/auth/src/services/email.ts > $A/src/services/email.ts; echo "$n email=$(git -C $R hash-object $A/src/services/email.ts | cut -c1-12)"
  G161_ROUTE_OUT=$W/logs/route_$n.json node $W/harness/vt.js $W/logs/vt_route_$n.json src/__tests__/g161-route-driver.test.ts; echo "rc=$?"
done
git -C $R checkout -q -- Blockchain/Dev/services/auth/src/services/email.ts; mkdir -p $W/harness/_moved_out_of_clone; mv $T $W/harness/_moved_out_of_clone/
echo "status=$(git -C $R status --porcelain | wc -l) email=$(git -C $R hash-object $A/src/services/email.ts | cut -c1-12)"
node -e 'const b=require(process.argv[1]),h=require(process.argv[2]);for(const x of b){const y=h.find(r=>r.route===x.route&&r.kind===x.kind&&r.email===x.email);const f=r=>r.status+" "+r.code+" ["+r.calls.join(",")+"]";console.log((x.route+" "+(x.email||"")+" "+x.kind).padEnd(50),"base:",f(x).padEnd(64),"head:",f(y))}' $W/logs/route_base.json $W/logs/route_head.json | tee $W/logs/route_compare.txt
