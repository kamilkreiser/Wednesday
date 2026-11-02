#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate104-ks1868-pr1923; R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/originate; L=$W/logs
F="src/routes/signatories.ts src/routes/thirdPartyVerifiers.ts src/services/retentionScheduler.ts src/__tests__/ks1868-retention-scheduler-run-enforcement-p3-unreadable-throw.test.ts src/__tests__/ks1868-signatories-read-routes-p1-unreadable-throw.test.ts src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts src/__tests__/ks1868-third-party-verifiers-admin-routes-p3-unreadable-throw.test.ts src/__tests__/ks1868-third-party-verifiers-verify-routes-p4-unreadable-throw.test.ts"
(cd $A && $D/node_modules/.bin/eslint $F > $L/eslint_pr_files.log 2>&1; echo "rc=$?" >> $L/eslint_pr_files.log); echo ESLINT; cat $L/eslint_pr_files.log
FR="$R/Projects Documents/fragments/cheat/KS-1868-originate-signatories-verifiers-retention-catches-unreadable-thrown-value.html"
(cd $R && node Blockchain/Dev/scripts/docs-fragments.mjs check > $L/frag_head.log 2>&1; echo "rc=$?" >> $L/frag_head.log); echo FRAG; tail -4 $L/frag_head.log
h0=$(shasum -a 256 "$FR" | cut -d" " -f1); cp "$FR" $L/_quarantine/frag_orig.html; printf "<div>\n" >> "$FR"
(cd $R && node Blockchain/Dev/scripts/docs-fragments.mjs check > $L/frag_planted.log 2>&1; echo "rc=$?" >> $L/frag_planted.log); echo PLANTED; grep -i "balanced\|rc=" $L/frag_planted.log | head -3
cp $L/_quarantine/frag_orig.html "$FR"; [ "$(shasum -a 256 "$FR" | cut -d" " -f1)" = "$h0" ] && echo FRAG_RESTORED
git -C $R status --short
