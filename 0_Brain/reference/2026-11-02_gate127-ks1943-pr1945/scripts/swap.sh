#!/bin/bash
# usage: swap.sh base|head  -> puts that version of db.ts + gdprService.ts in the clone and asserts the sha256
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945
O=$W/repo/Blockchain/Dev/services/originate/src
cp $W/evidence/src/db_$1.ts $O/db.ts; cp $W/evidence/src/gdpr_$1.ts $O/services/gdprService.ts
a=$(shasum -a 256 $O/db.ts | cut -d' ' -f1); b=$(shasum -a 256 $W/evidence/src/db_$1.ts | cut -d' ' -f1)
c=$(shasum -a 256 $O/services/gdprService.ts | cut -d' ' -f1); d=$(shasum -a 256 $W/evidence/src/gdpr_$1.ts | cut -d' ' -f1)
[ "$a" = "$b" ] && [ "$c" = "$d" ] && echo "SWAP_OK $1" || { echo "SWAP_BAD $1"; exit 9; }
