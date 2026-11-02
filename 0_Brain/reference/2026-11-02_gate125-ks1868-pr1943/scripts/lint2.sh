#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
D=$W/repo/Blockchain/Dev
(cd $D && $D/node_modules/.bin/eslint services/originate/src/repositories/certificationRepo.ts services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts > $W/logs/eslint_$1.log 2>&1; echo eslint rc=$?)
tail -15 $W/logs/eslint_$1.log
