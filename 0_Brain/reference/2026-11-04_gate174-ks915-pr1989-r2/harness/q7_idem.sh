#!/bin/bash
# Q7: second run byte-identical; output files ignored; git status clean of env files. Hashes and counts only.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/harness/lib.sh
TAG=${1:-q7}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
c=$(mkclone $TAG-idem) || exit 1; d=$c/Blockchain/Dev
r1=$(run $c $L/idem1.log); s1=$(sha $d/.env); sl1=$(sha $d/.env.local)
r2=$(run $c $L/idem2.log); s2=$(sha $d/.env); sl2=$(sha $d/.env.local)
echo "run1 rc=$r1 run2 rc=$r2 env_same=$([[ $s1 == $s2 ]] && echo y || echo N) envlocal_same=$([[ $sl1 == $sl2 ]] && echo y || echo N) kept_msg=$(grep -c 'kept ADMIN_USER_PASSWORD' $L/idem2.log) mode=$(mode $d/.env)/$(mode $d/.env.local)"
cp $d/.env $L/pre_rotate.env.bin; r3=$(run $c $L/idem3.log -- --rotate)
echo "rotate rc=$r3 difflines=$(diff $L/pre_rotate.env.bin $d/.env | grep -c '^[<>]') changed_keys=$(diff $L/pre_rotate.env.bin $d/.env | grep '^[<>]' | cut -c3- | cut -d= -f1 | sort -u | tr '\n' ' ')"
r4=$(run $c $L/idem4.log); s4=$(sha $d/.env); r5=$(run $c $L/idem5.log); echo "after rotate: run rc=$r4/$r5 byte_identical=$([[ $s4 == $(sha $d/.env) ]] && echo y || echo N)"
for p in Blockchain/Dev/.env Blockchain/Dev/.env.local Blockchain/Dev/.env-ks915.AbCdEf Blockchain/Dev/.env.ks915.AbCdEf Blockchain/Dev/env.example; do
  printf '   %-36s %s\n' "$p" "$(git -C $c check-ignore -q --no-index "$p" && echo ignored || echo NOT-IGNORED)"; done
echo "   git status -uall lines naming an env file: $(git -C $c status --porcelain -uall | grep -c -E '\.env($|[-.])')   control (lines naming env.example): $(git -C $c status --porcelain -uall | grep -c 'env.example')"
echo "   git objects in the clone: $(find $c/.git/objects -type f | wc -l | tr -d ' ') (none committed)"
