#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938
R=$W/repo; D=$R/Blockchain/Dev; L=$W/logs
bash $W/scripts/co.sh pr1938 > /dev/null
cd $D
node scripts/docs-fragments.mjs check > $L/docs_head.log 2>&1; echo "head rc=$?" > $L/docs_sum.txt
F="Projects Documents/fragments/cheat/KS-1725-zod-4-prep-issues-and-record-key-on-zod-3.html"
ls "$R/$F" >> $L/docs_sum.txt 2>&1
# planted defect: unbalanced tag in the cheat fragment
echo '<div class="note"><table>' >> "$R/$F"
node scripts/docs-fragments.mjs check > $L/docs_planted.log 2>&1; echo "planted rc=$?" >> $L/docs_sum.txt
git -C $R checkout -q -- "$F"
node scripts/docs-fragments.mjs check > $L/docs_restored.log 2>&1; echo "restored rc=$?" >> $L/docs_sum.txt
git -C $R status --short | head -5 >> $L/docs_sum.txt
