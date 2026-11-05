#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate195-ks1990-pr2006; R=$W/repo
F=Blockchain/Dev/services/originate/src/routes/adminConfig.ts
T=Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
echo "head lines:"; git -C $R show 6311c141f99e:$F | grep -n -i -e "ON CONFLICT (email)" -e "catch { /\* skip \*/ }" -e "Admin config request failed (POST /api/admin/seed"
echo "base lines:"; git -C $R show 07a2d62be6a0:$F | grep -n -i -e "ON CONFLICT (email)" -e "catch { /\* skip \*/ }"
echo "ks1802 line counts base/head: $(git -C $R show 07a2d62be6a0:$T | wc -l) $(git -C $R show 6311c141f99e:$T | wc -l)"
echo "openapi seed-demo hits: $(git -C $R grep -c -i 'seed-demo' 6311c141f99e -- Blockchain/Dev/docs/openapi/secuura-api.yaml)"
echo "openapi /admin hits (control): $(git -C $R grep -c '/admin' 6311c141f99e -- Blockchain/Dev/docs/openapi/secuura-api.yaml)"
git -C $R merge-tree --write-tree 07a2d62be6a09c9cd504864d1cf1906543d55317 6311c141f99e5ade8d94e60ee15b0c80006a52cd > $W/logs/q7.txt 2>&1
echo mt_rc=$?
cat $W/logs/q7.txt
echo "head tree: $(git -C $R rev-parse 6311c141f99e^{tree})"
