#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate84-ks1868-minting-1899
A=$G/repo/Blockchain/Dev/services/nft-certificate
nice -n 10 npm run lint --prefix $A > $G/logs/eslint_pkg.log 2>&1; echo "rc=$?" >> $G/logs/eslint_pkg.log
tail -5 $G/logs/eslint_pkg.log
echo "--- lines mentioning changed files:"; /usr/bin/grep -n -i -E 'minting\.service|ks1868-nft-' $G/logs/eslint_pkg.log; echo "(grep rc=$?)"
echo "--- positive control: any file path in output:"; /usr/bin/grep -c -i 'nft-certificate' $G/logs/eslint_pkg.log
