#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
date -u > $W/logs/head_end.log
git -C $W/repo ls-remote origin refs/pull/1943/head refs/heads/develop >> $W/logs/head_end.log 2>&1
git -C $W/repo rev-parse HEAD >> $W/logs/head_end.log
shasum -a 256 < $W/repo/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts >> $W/logs/head_end.log
git -C $W/repo status --short >> $W/logs/head_end.log
cat $W/logs/head_end.log
echo PS:; ps -axo pid,etime,command | /usr/bin/grep -E 'jest|vitest|gate125|mutants|npm|tsc|eslint' | /usr/bin/grep -v grep | cut -c1-160
echo PSDONE
git -C /Volumes/DevMASTER/WEDNESDAY status --short | /usr/bin/grep -i gate125 | head
