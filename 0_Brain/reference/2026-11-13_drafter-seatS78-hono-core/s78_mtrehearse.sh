#!/bin/bash
export GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config"
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" GIT_CONFIG_VALUE_0="Authorization: Basic $(printf 'x-access-token:%s' "$(gh auth token)" | base64)"
F=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatS78-hono-core; C=$F/clone2; W=$F/s78_work2
G="git -C $C -c user.name=d -c user.email=d@d"
R=Blockchain/Dev/package-lock.json; M=Blockchain/Dev/services/mcp-server/package-lock.json
mk() {
  export GIT_INDEX_FILE=$F/s78_idx_$2
  git -C $C read-tree origin/develop
  for P in $R $M; do
    git -C $C show origin/develop:$P > $F/s78_tmp_lock_$2.json
    python3 -I - "$F/s78_tmp_lock_$2.json" "$2" <<'PY'
import sys
p,mode=sys.argv[1:]
s=open(p).read()
if mode=="fix":
    s=s.replace('"version": "4.13.13",\n      "resolved": "https://registry.npmjs.org/hono/-/hono-4.13.13.tgz",\n      "integrity": "sha512-CQ46U0ZkAGmbT/4UxdzzGJpacP2IeKgY4a5/tOI9AABbpOMfK739wfDXmv1usCk+3RkKj1hQy4/fjhiwa2xlrA==",',
                '"version": "4.13.18",\n      "resolved": "https://registry.npmjs.org/hono/-/hono-4.13.18.tgz",\n      "integrity": "sha512-H9q/E1XizaWstJxUW881dmLxEj+t/TrGGnyxINkm4+sK0qUwsMtFdo2BWI9Vs3cIS19MU6b6iCijoUoEf4f3DA==",',1)
else:
    s=s.replace('"version": "2.1.5",\n      "resolved": "https://registry.npmjs.org/@hono/node-server/-/node-server-2.1.5.tgz"','"version": "2.1.9",\n      "resolved": "https://registry.npmjs.org/@hono/node-server/-/node-server-2.1.9.tgz"',1)
open(p,"w").write(s)
PY
    H=$(git -C $C hash-object -w $F/s78_tmp_lock_$2.json); git -C $C update-index --cacheinfo 100644,$H,$P
  done
  T=$(git -C $C write-tree); unset GIT_INDEX_FILE
  CM=$($G commit-tree $T -p origin/develop -m "s78 rehearsal $2"); git -C $C update-ref $1 $CM; echo "$2 commit $CM tree $T"
}
mk refs/scratch/s78fix fix; mk refs/scratch/s78plant plant
for X in s78fix s78plant; do
  git -C $C merge-tree --write-tree refs/scratch/$X pr/2226 > $F/s78_mt_$X.out 2>&1; echo "merge-tree $X vs 2226 rc=$?"; head -4 $F/s78_mt_$X.out
done
TR=$(head -1 $F/s78_mt_s78fix.out)
for P in $R $M; do
  A=$(git -C $C rev-parse $TR:$P); B=$(git hash-object $W/after/$P); echo "$P merged-blob $A vs npm-result-blob $B $([ $A = $B ] && echo IDENTICAL || echo DIFFER)"
done
MC=$($G commit-tree $TR -p refs/scratch/s78fix -p pr/2226 -m s78merge); git -C $C update-ref refs/scratch/s78merged $MC
python3 -I /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/07a6a72d-9013-4f91-8a06-18332bafe50a/scratchpad/census_hono.py $C refs/scratch/s78merged
