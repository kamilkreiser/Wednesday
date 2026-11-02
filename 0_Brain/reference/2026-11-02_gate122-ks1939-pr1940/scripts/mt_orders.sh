#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940; R=$W/repo
G="git -C $R -c user.name=gate122 -c user.email=gate122@invalid"
echo "PR1941 head $(git -C $R rev-parse refs/remotes/pr/1941) parent $(git -C $R rev-parse refs/remotes/pr/1941^) commits-over-mb $(git -C $R rev-list --count $(git -C $R merge-base refs/remotes/pr/1941 origin/develop)..refs/remotes/pr/1941)"
echo "PR1941 alone onto develop: $(git -C $R merge-tree --write-tree origin/develop refs/remotes/pr/1941 | head -1) rc=${PIPESTATUS[0]}"
for order in "1940 1941" "1941 1940"; do set -- $order
  T1=$(git -C $R merge-tree --write-tree origin/develop refs/remotes/pr/$1); r1=$?
  C1=$($G commit-tree $T1 -p origin/develop -p refs/remotes/pr/$1 -m "gate122 scratch $1")
  T2=$(git -C $R merge-tree --write-tree $C1 refs/remotes/pr/$2); r2=$?
  echo "order $1 then $2: step1 rc=$r1 step2 rc=$r2 final tree $(echo "$T2" | head -1)"
  echo "  verification.ts blob $(git -C $R rev-parse $(echo "$T2" | head -1):Blockchain/Dev/services/originate/src/routes/verification.ts)"
  echo "  verificationV2.ts blob $(git -C $R rev-parse $(echo "$T2" | head -1):Blockchain/Dev/services/originate/src/routes/verificationV2.ts)"
done
# the union tree must hold the PR1940 hunks verbatim
T=$(git -C $R merge-tree --write-tree $($G commit-tree $(git -C $R merge-tree --write-tree origin/develop refs/remotes/pr/1940) -p origin/develop -p refs/remotes/pr/1940 -m s) refs/remotes/pr/1941 | head -1)
git -C $R show $T:Blockchain/Dev/services/originate/src/routes/verification.ts > $W/logs/union_verification.ts
/usr/bin/grep -c "return await respondExistenceOnly(" $W/logs/union_verification.ts; /usr/bin/grep -n -A6 "catch (dbErr: any)" $W/logs/union_verification.ts
git -C $R diff -U0 refs/remotes/pr/1940 $T -- Blockchain/Dev/services/originate/src/routes/verification.ts | /usr/bin/grep '^@@'
