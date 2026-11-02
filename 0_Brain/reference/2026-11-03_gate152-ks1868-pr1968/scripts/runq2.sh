W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968; R=$W/repo; V=$R/Blockchain/Dev/services/vc-issuer
which=$1
mkdir -p $W/logs/_quarantine $W/logs/cwd
cp $W/gate_tests/gate152-q2.test.ts $V/src/__tests__/gate152-q2.test.ts
if [ "$which" = base ]; then
  git -C $R show 2f9f7db313b3:Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts > $V/src/repositories/credentialRepo.ts
  git -C $R show 2f9f7db313b3:Blockchain/Dev/services/vc-issuer/src/db.ts > $V/src/db.ts
fi
npx --prefix $R/Blockchain/Dev vitest run --root $V src/__tests__/gate152-q2.test.ts --reporter=verbose > $W/logs/q2_$which.log 2>&1; echo rc=$? >> $W/logs/q2_$which.log
mv $V/src/__tests__/gate152-q2.test.ts $W/logs/_quarantine/gate152-q2.$which.test.ts
git -C $R checkout -q pr1968 -- Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts Blockchain/Dev/services/vc-issuer/src/db.ts
git -C $R status --short > $W/logs/q2_${which}_status.log
