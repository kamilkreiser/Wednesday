#!/bin/bash
# swap.sh base|head : put the service tree at base (79145a312f01) or head (74dc459edbb6) for the 9 PR paths under the service.
set -u
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate178-ks1868-pr1994
R=$W/repo
P=Blockchain/Dev/services/nft-certificate
case "$1" in
  base)
    git -C $R show 79145a312f01:$P/src/routes/nft.routes.ts > $R/$P/src/routes/nft.routes.ts
    mkdir -p $W/scratch/parked
    for f in $(git -C $R diff --name-only --diff-filter=A 79145a312f01 74dc459edbb6 -- $P); do mv $R/$f $W/scratch/parked/; done ;;
  head)
    git -C $R show 74dc459edbb6:$P/src/routes/nft.routes.ts > $R/$P/src/routes/nft.routes.ts
    for f in $(git -C $R diff --name-only --diff-filter=A 79145a312f01 74dc459edbb6 -- $P); do [ -f $W/scratch/parked/$(basename $f) ] && mv $W/scratch/parked/$(basename $f) $R/$f; done ;;
esac
echo "routes blob now: $(git hash-object $R/$P/src/routes/nft.routes.ts | cut -c1-9) (base 159cbb07f, head c8fd012f7)"
git -C $R status --porcelain -- $P | grep -v node_modules | head
