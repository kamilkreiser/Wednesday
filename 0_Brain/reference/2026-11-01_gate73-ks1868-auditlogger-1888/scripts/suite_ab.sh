#!/bin/bash
# Gate 73: shared whole suite at base (product file = base blob, new test moved aside) x2, then at head x2.
# Product file restored from refs/gate/head with a whole-file sha256 check; the new test is moved back.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate73-ks1868-auditlogger-1888
R=$G/repo; P=Blockchain/Dev/packages/shared
A=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c6cc71e2-d540-45eb-85fa-5aca0154bf77/scratchpad/g73aside
[ "$(git -C $R rev-parse --show-toplevel)" = "$R" ] || exit 98
mkdir -p $A
F=$R/$P/src/security/audit-logger.ts
T=$R/$P/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts
HSHA=$(git -C $R show refs/gate/head:$P/src/security/audit-logger.ts | shasum -a 256 | cut -d' ' -f1)
TSHA=$(shasum -a 256 $T | cut -d' ' -f1)
run() {
  bash $G/scripts/vt.sh $G/logs/suite_$1.log --maxWorkers=2 --reporter=default --reporter=json --outputFile.json=$G/logs/suite_$1.json
  echo "$1 rc=$? $(grep -E '^ +Tests ' $G/logs/suite_$1.log)"
}
git -C $R show refs/gate/base:$P/src/security/audit-logger.ts > $F
mv $T $A/
git -C $R status --short
run base1; run base2
git -C $R show refs/gate/head:$P/src/security/audit-logger.ts > $F
mv $A/$(basename $T) $T
[ "$(shasum -a 256 $F | cut -d' ' -f1)" = "$HSHA" ] && echo "product sha256 restored OK" || { echo "PRODUCT RESTORE FAILED"; exit 97; }
[ "$(shasum -a 256 $T | cut -d' ' -f1)" = "$TSHA" ] && echo "test sha256 restored OK" || { echo "TEST RESTORE FAILED"; exit 96; }
git -C $R status --short
run head1; run head2
git -C $R status --short; echo DONE
