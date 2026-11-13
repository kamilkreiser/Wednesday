#!/bin/bash
export GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config"
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/07a6a72d-9013-4f91-8a06-18332bafe50a/scratchpad
F=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatS78-hono-core; C=$F/clone2
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" GIT_CONFIG_VALUE_0="Authorization: Basic $(printf 'x-access-token:%s' "$(gh auth token)" | base64)"
git -C $C diff --numstat origin/develop pr/2226 > $F/numstat_2226.out; cat $F/numstat_2226.out
git -C $C diff origin/develop pr/2226 -- Blockchain/Dev/package-lock.json | grep '^[+-]' > $F/diff_root_2226.out; cat $F/diff_root_2226.out
git -C $C merge-tree --write-tree origin/develop pr/2226 > $F/mt_develop_2226.out 2>&1; echo mt rc=$?; cat $F/mt_develop_2226.out
M=$(head -1 $F/mt_develop_2226.out); MC=$(git -C $C -c user.name=d -c user.email=d@d commit-tree $M -p origin/develop -p pr/2226 -m scratch-merge); echo MC=$MC; git -C $C update-ref refs/scratch/merged2226 $MC
python3 -I $S/census_hono.py $C refs/scratch/merged2226 > $F/census_merged2226.out 2>&1; echo census rc=$?; cat $F/census_merged2226.out
