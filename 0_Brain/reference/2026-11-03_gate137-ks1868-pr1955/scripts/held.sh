#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955
R=$G/repo
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c5199eda-e2e8-42ab-989c-f3882d521117/scratchpad
export GIT_INDEX_FILE=$S/held.index
FILES="Blockchain/Dev/services/anchoring/src/index.ts Blockchain/Dev/services/originate/src/routes/anchors.ts Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-message-coercion-unreadable-throw.test.ts Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts"
for BASE in 3e688ee239f2b742feb658c2763e11d5cdd99521 9a9bf86967e31166ed4aba863e4c1fc4b763bfe8; do
  echo "BASE $BASE"
  git -C $R read-tree $BASE
  git -C $R apply --cached $G/evidence/held/o82_p5.patch.diff; a=$?; git -C $R apply --cached $G/evidence/held/o82_p6.patch.diff; b=$?; echo "apply rc=$a,$b"
  for f in $FILES; do h=$(git -C $R ls-files -s -- "$f" | awk '{print $2}'); p=$(git -C $R rev-parse pr/1955:"$f"); [ "$h" = "$p" ] && echo "EQUAL $h $f" || echo "DIFF held=$h pr=$p $f"; done
  t=$(git -C $R write-tree); echo "held tree vs PR tree (names):"; git -C $R diff --name-status $t pr/1955
done
echo CONTROL corrupted context
git -C $R read-tree 9a9bf86967e31166ed4aba863e4c1fc4b763bfe8
awk 'BEGIN{d=0} /^ / && !d {print $0 "CORRUPT"; d=1; next} {print}' $G/evidence/held/o82_p6.patch.diff > $S/corrupt.diff
git -C $R apply --cached $S/corrupt.diff; echo "control rc=$?"
