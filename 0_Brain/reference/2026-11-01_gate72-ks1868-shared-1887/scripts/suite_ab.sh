#!/bin/bash
# Gate 72: shared whole suite at base (product reverted, 2 new tests moved aside) x2, then at head x2.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate72-ks1868-shared-1887
R=$G/repo; P=Blockchain/Dev/packages/shared; S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c6cc71e2-d540-45eb-85fa-5aca0154bf77/scratchpad/g72aside
[ "$(git -C $R rev-parse --show-toplevel)" = "$R" ] || exit 98
mkdir -p $S
T1=$P/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts
T2=$P/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts
run() { # tag
  bash $G/scripts/vt.sh $G/logs/suite_$1.log --reporter=default --reporter=json --outputFile.json=$G/logs/suite_$1.json
  echo "$1 rc=$?"
}
# base
git -C $R checkout a71479b49bf3 -- $P/src/cache/response-cache.ts $P/src/utils/gracefulShutdown.ts
mv $R/$T1 $S/; mv $R/$T2 $S/
run base1; run base2
# head
git -C $R checkout 2d1a2265bbab7bef1b689087e021a412b08fabae -- $P/src/cache/response-cache.ts $P/src/utils/gracefulShutdown.ts
mv $S/$(basename $T1) $R/$T1; mv $S/$(basename $T2) $R/$T2
run head1; run head2
git -C $R status --short; git -C $R diff 2d1a2265 --stat | tail -1; echo DONE
