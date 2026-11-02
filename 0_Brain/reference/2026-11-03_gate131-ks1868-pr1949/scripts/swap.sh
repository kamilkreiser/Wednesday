#!/bin/bash
# usage: swap.sh base|head  -- puts the 4 product route files at base or head content (git show), prints sha256
set -eu
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate131-ks1868-pr1949
R=$G/repo
P=Blockchain/Dev/services/auth/src/routes
case "$1" in base) REV=3e688ee239f2b742feb658c2763e11d5cdd99521;; head) REV=d2b49790d72ca21d526f0135316e4cb0f41831dc;; *) exit 2;; esac
for f in auth.ts internal.ts issuerCerts.ts oauth.ts; do git -C $R show $REV:$P/$f > $R/$P/$f; done
shasum -a 256 $R/$P/auth.ts $R/$P/internal.ts $R/$P/issuerCerts.ts $R/$P/oauth.ts | awk '{print substr($1,1,12), $2}' | sed "s#$R/##"
git -C $R status --short -- $P
