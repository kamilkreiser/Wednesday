#!/bin/bash
export GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config"
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/07a6a72d-9013-4f91-8a06-18332bafe50a/scratchpad
F=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatS78-hono-core; C=$F/clone2
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" GIT_CONFIG_VALUE_0="Authorization: Basic $(printf 'x-access-token:%s' "$(gh auth token)" | base64)"
git -C $C fetch origin refs/heads/develop:refs/remotes/origin/develop refs/pull/2226/head:refs/remotes/pr/2226 > $F/s78_fetch.out 2>&1; echo fetch rc=$?; tail -3 $F/s78_fetch.out
git -C $C rev-parse origin/develop pr/2226
git -C $C ls-files '*package-lock.json' 2>/dev/null | wc -l
git -C $C ls-tree -r --name-only origin/develop | grep -c 'package-lock.json$'
python3 -I $S/census_hono.py $C origin/develop > $F/s78_census_develop.out 2>&1; echo census rc=$?; cat $F/s78_census_develop.out
M=$(git -C $C merge-tree --write-tree origin/develop pr/2226); echo "merge-tree rc=$? $M"
MC=$(git -C $C -c user.name=d -c user.email=d@d commit-tree $M -p origin/develop -p pr/2226 -m scratch-merge); git -C $C update-ref refs/scratch/merged2226 $MC
python3 -I $S/census_hono.py $C refs/scratch/merged2226 > $F/s78_census_merged2226.out 2>&1; echo census rc=$?; cat $F/s78_census_merged2226.out
