#!/bin/bash
# Apply held O75-P1/P2 patches strictly to a temp index (scratchpad) at base, compare blobs with PR head.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate114-ks1868-pr1932
R=$G/repo
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a974be12-1abe-4d9a-9532-9c46296d28fc/scratchpad
export GIT_INDEX_FILE=$S/held.index
for BASE in cd9c4a7dd3b87f4810d16b40352a63330d1d6793 04ff5262ad526a13c1a0df99480b76860a8d11d1; do
  echo "BASE $BASE"; git -C $R cat-file -t $BASE || continue
  for mode in alone_p1 alone_p2 combined; do
    git -C $R read-tree $BASE
    case $mode in
      alone_p1) git -C $R apply --cached --verbose $G/evidence/held/o75_p1.patch.diff 2>&1; echo "rc=$?";;
      alone_p2) git -C $R apply --cached --verbose $G/evidence/held/o75_p2.patch.diff 2>&1; echo "rc=$?";;
      combined) git -C $R apply --cached $G/evidence/held/o75_p1.patch.diff; a=$?; git -C $R apply --cached $G/evidence/held/o75_p2.patch.diff; b=$?; echo "rc=$a,$b"
        for f in Blockchain/Dev/services/anchoring/src/index.ts Blockchain/Dev/services/originate/src/routes/anchors.ts Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts; do
          h=$(git -C $R ls-files -s -- "$f" | awk '{print $2}'); p=$(git -C $R rev-parse pr/1932:"$f"); [ "$h" = "$p" ] && echo "EQUAL $h $f" || echo "DIFF held=$h pr=$p $f"; done
        t=$(git -C $R write-tree); echo "held tree vs PR tree (names):"; git -C $R diff --name-status $t pr/1932;;
    esac
  done
done
echo CONTROL corrupted context
git -C $R read-tree cd9c4a7dd3b87f4810d16b40352a63330d1d6793
awk 'BEGIN{d=0} /^ / && !d {print $0 "CORRUPT"; d=1; next} {print}' $G/evidence/held/o75_p2.patch.diff > $S/corrupt.diff
git -C $R apply --cached $S/corrupt.diff; echo "control rc=$?"
