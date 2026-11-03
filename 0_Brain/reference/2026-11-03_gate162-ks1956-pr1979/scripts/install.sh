#!/bin/bash
# Gate 162 install: the lockfile, root package.json, referral package.json and packages/shared tree are byte-identical
# (same git blob ids) to gate 153's clone, which ran `npm ci --ignore-scripts` rc 0. So clone (APFS clonefile, cp -c)
# its installed node_modules into THIS clone, read-only from gate 153's side, then build packages/shared here.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate153-ks1868-pr1969/repo/Blockchain/Dev
D=$W/repo/Blockchain/Dev
for p in node_modules services/referral/node_modules packages/shared/node_modules; do
  if [ -d "$G/$p" ]; then nice -n 10 cp -Rc "$G/$p" "$D/$p"; echo "copied $p rc=$?"; fi
done
rm -rf "$D/node_modules/.vite" "$D/services/referral/node_modules/.vite"
nice -n 10 npm run build --prefix $D/packages/shared > $W/logs/shared_build.log 2>&1; echo "shared build rc=$?"
date
