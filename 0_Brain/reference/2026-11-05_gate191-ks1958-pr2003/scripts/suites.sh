#!/bin/bash
# gate 191 Q8 + red-first: whole vc-issuer suite at head, PR file red at base, tsc incl tests, eslint, docs-fragments.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate191-ks1958-pr2003; R=$W/repo; D=$R/Blockchain/Dev; S=$D/services/vc-issuer
HEAD=8b140178276457116714892fe0cf73b9f1e92c8c; BASE=035685291b9d58ae6ea8ba5f05adf9379f9c2944
P1=Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
P2=Blockchain/Dev/services/vc-issuer/src/services/revocationResolvers.ts
T=src/__tests__/ks1958-revocation-read-fails-closed.test.ts
cd $W/cwd || exit 9
E="env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp"
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ log=$1; shift; $E nice -n 10 $D/node_modules/.bin/vitest run --root $S "$@" > $log 2>&1; echo "rc=$?" >> $log; }
# 1 whole suite at head
vt $W/logs/q8_whole_head.log
# 2 red first: PR file against base product bytes
git -C $R show $BASE:$P1 > $R/$P1; git -C $R show $BASE:$P2 > $R/$P2
vt $W/logs/q7_red_base_prfile.log $T
# tsc incl tests at base product (control: same config, base bytes)
$E nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.test.json > $W/logs/q8_tsc_tests_baseproduct.log 2>&1; echo "rc=$?" >> $W/logs/q8_tsc_tests_baseproduct.log
git -C $R checkout -q $HEAD -- $P1 $P2
# 3 tsc incl tests at head (tsconfig.test.json includes src/**/*), and the service's own tsconfig
$E nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.test.json > $W/logs/q8_tsc_tests_head.log 2>&1; echo "rc=$?" >> $W/logs/q8_tsc_tests_head.log
$E nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.json --noEmit > $W/logs/q8_tsc_own_head.log 2>&1; echo "rc=$?" >> $W/logs/q8_tsc_own_head.log
# 4 eslint on the three touched .ts files (repo config at Blockchain/Dev), then a planted control file
( cd $D && $E nice -n 10 $D/node_modules/.bin/eslint services/vc-issuer/$T services/vc-issuer/src/repositories/credentialRepo.ts services/vc-issuer/src/services/revocationResolvers.ts > $W/logs/q8_eslint_head.log 2>&1; echo "rc=$?" >> $W/logs/q8_eslint_head.log )
printf 'export function g191(): number {\n  const unused = 1;\n  debugger;\n  return 2;\n}\n' > $S/src/services/g191-eslint-control.ts
( cd $D && $E nice -n 10 $D/node_modules/.bin/eslint services/vc-issuer/src/services/g191-eslint-control.ts > $W/logs/q8_eslint_control.log 2>&1; echo "rc=$?" >> $W/logs/q8_eslint_control.log )
mkdir -p $W/scratch/_quarantine; mv $S/src/services/g191-eslint-control.ts $W/scratch/_quarantine/
# 5 docs-fragments: clean, planted defect in each new fragment, restore by sha
F="$R/Projects Documents/fragments"; N=KS-1958-revocation-read-fails-closed.html
chk(){ $E nice -n 10 node $D/scripts/docs-fragments.mjs check --root $R > "$1" 2>&1; echo "rc=$?" >> "$1"; }
chk $W/logs/q8_frag_clean.log
for k in flow cheat; do
  f="$F/$k/$N"; h=$(sha "$f"); cp "$f" $W/scratch/frag_orig_$k.html
  printf '\n<div>g191 planted unclosed</div><div>\n' >> "$f"
  chk $W/logs/q8_frag_planted_$k.log
  cp $W/scratch/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k restore OK" >> $W/logs/q8_frag_restore.log || echo "$k RESTORE FAIL" >> $W/logs/q8_frag_restore.log
done
chk $W/logs/q8_frag_after.log
git -C $R status --short > $W/logs/q8_status_after.log
echo done > $W/logs/q8.done
