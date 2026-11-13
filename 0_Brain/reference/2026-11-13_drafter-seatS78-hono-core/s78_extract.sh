#!/bin/bash
export GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config"
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" GIT_CONFIG_VALUE_0="Authorization: Basic $(printf 'x-access-token:%s' "$(gh auth token)" | base64)"
F=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatS78-hono-core; C=$F/clone2; W=$F/s78_work2
test ! -e $W || { echo exists; exit 2; }
mkdir -p $W/merged
git -C $C ls-tree -r --name-only refs/scratch/merged2226 | grep -E '(^|/)package(-lock)?\.json$' > $F/s78_filelist.out
wc -l < $F/s78_filelist.out
git -C $C archive refs/scratch/merged2226 $(cat $F/s78_filelist.out | tr '\n' ' ') | tar -x -C $W/merged
echo "--- package.json mentioning hono:"
cd_none=1
for f in $(grep 'package.json$' $F/s78_filelist.out); do /usr/bin/grep -H -n -i hono $W/merged/$f; done > $F/s78_pkgjson_hono.out 2>&1
cat $F/s78_pkgjson_hono.out | sed "s#$W/merged/##"
echo "--- control: grep finds react in root package.json?"; /usr/bin/grep -c -i prisma $W/merged/Blockchain/Dev/package.json
