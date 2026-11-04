#!/bin/bash
# Gate 192: docs-fragments check clean / planted dangling ref / restored; eslint planted control. All in the gate's own clone.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004
R=$W/repo; D=$R/Blockchain/Dev; S=$D/services/originate
E="env -i PATH=$PATH HOME=$W/home TMPDIR=$W/tmp"
FL="$R/Projects Documents/fragments/flow/KS-1986-v1-original-across-tenants.html"
cd $R || exit 9
$E node $D/scripts/docs-fragments.mjs check > $W/runs/docs_clean.out 2>&1; echo "docs clean rc=$?"
cp "$FL" $W/tmp/flow.orig
printf '%s\n' '<p>see <!--ref:KS-9999-g192-planted-dangling-ref--></p>' >> "$FL"
$E node $D/scripts/docs-fragments.mjs check > $W/runs/docs_planted.out 2>&1; echo "docs planted (dangling ref) rc=$?"
cp $W/tmp/flow.orig "$FL"
git -C $R diff --quiet -- "Projects Documents" && echo "restored: git diff clean"
$E node $D/scripts/docs-fragments.mjs check > $W/runs/docs_restored.out 2>&1; echo "docs restored rc=$?"
# eslint planted control: a copy of the PR test file with a lint error, inside the clone's src, then removed
P=$S/src/__tests__/g192-planted-lint.test.ts
cp $S/src/__tests__/ks1986-v1-original-across-tenants.test.ts $P
printf '%s\n' 'var g192Planted: any = 1; // eslint control' >> $P
cd $D || exit 9
$E $D/node_modules/.bin/eslint $P > $W/runs/eslint_planted.out 2>&1; echo "eslint planted control rc=$? problems=$(grep -cE '^\s+[0-9]+:[0-9]+' $W/runs/eslint_planted.out)"
rm -f $P
git -C $R status --porcelain
