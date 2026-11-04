#!/bin/bash
# gate 194 Q9 (adapted from gate 191's suites.sh): whole vc-issuer at head, PR file red at base, tsc incl tests + control,
# eslint + control, docs-fragments + planted defects. Restores by `git show <head>:path > path`; never deletes (quarantine).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959; R=$W/repo; D=$R/Blockchain/Dev; S=$D/services/vc-issuer
HEAD=a968818a0038727399663775722017c130d4cb08; BASE=e899463d2a0b1b30f2cff46b23d001622620029a
P1=Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
P2=Blockchain/Dev/services/vc-issuer/src/routes/credentials.ts
T=src/__tests__/ks1959-revoke-write-fails-closed.test.ts
cd $W/cwd || exit 9
mkdir -p $W/scratch/_quarantine
E="env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp"
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ log=$1; shift; $E nice -n 10 $D/node_modules/.bin/vitest run --root $S "$@" > $log 2>&1; echo "rc=$?" >> $log; }
# 1 whole suite at head
vt $W/logs/q9_whole_head.log
# 2 red first: PR file against base product bytes (json for per-test failure messages)
git -C $R show $BASE:$P1 > $R/$P1; git -C $R show $BASE:$P2 > $R/$P2
$E nice -n 10 $D/node_modules/.bin/vitest run --root $S $T --reporter=json --outputFile=$W/logs/q9_red_base_prfile.json > $W/logs/q9_red_base_prfile.log 2>&1; echo "rc=$?" >> $W/logs/q9_red_base_prfile.log
$E nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.test.json > $W/logs/q9_tsc_tests_baseproduct.log 2>&1; echo "rc=$?" >> $W/logs/q9_tsc_tests_baseproduct.log
git -C $R show $HEAD:$P1 > $R/$P1; git -C $R show $HEAD:$P2 > $R/$P2
# 3 tsc incl tests at head, service tsconfig, and a planted type error (control)
$E nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.test.json > $W/logs/q9_tsc_tests_head.log 2>&1; echo "rc=$?" >> $W/logs/q9_tsc_tests_head.log
$E nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.json --noEmit > $W/logs/q9_tsc_own_head.log 2>&1; echo "rc=$?" >> $W/logs/q9_tsc_own_head.log
printf 'export const g194TscControl: number = "not a number";\n' > $S/src/__tests__/g194-tsc-control.ts
$E nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.test.json > $W/logs/q9_tsc_control.log 2>&1; echo "rc=$?" >> $W/logs/q9_tsc_control.log
mv $S/src/__tests__/g194-tsc-control.ts $W/scratch/_quarantine/
# 4 eslint on the three touched .ts files, then a planted control file
( cd $D && $E nice -n 10 $D/node_modules/.bin/eslint services/vc-issuer/$T services/vc-issuer/src/repositories/credentialRepo.ts services/vc-issuer/src/routes/credentials.ts > $W/logs/q9_eslint_head.log 2>&1; echo "rc=$?" >> $W/logs/q9_eslint_head.log )
printf 'export function g194(): number {\n  const unused = 1;\n  debugger;\n  return 2;\n}\n' > $S/src/routes/g194-eslint-control.ts
( cd $D && $E nice -n 10 $D/node_modules/.bin/eslint services/vc-issuer/src/routes/g194-eslint-control.ts > $W/logs/q9_eslint_control.log 2>&1; echo "rc=$?" >> $W/logs/q9_eslint_control.log )
mv $S/src/routes/g194-eslint-control.ts $W/scratch/_quarantine/
# 5 docs-fragments: clean, planted defect in each new fragment, restore by sha
F="$R/Projects Documents/fragments"; N=KS-1959-revoke-write-fails-closed.html
chk(){ $E nice -n 10 node $D/scripts/docs-fragments.mjs check --root $R > "$1" 2>&1; echo "rc=$?" >> "$1"; }
chk $W/logs/q9_frag_clean.log
rm -f $W/logs/q9_frag_restore.log
for k in flow cheat; do
  f="$F/$k/$N"; h=$(sha "$f"); cp "$f" $W/scratch/frag_orig_$k.html
  printf '\n<div>g194 planted unclosed</div><div>\n' >> "$f"
  chk $W/logs/q9_frag_planted_$k.log
  cp $W/scratch/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k restore OK" >> $W/logs/q9_frag_restore.log || echo "$k RESTORE FAIL" >> $W/logs/q9_frag_restore.log
done
chk $W/logs/q9_frag_after.log
git -C $R status --short > $W/logs/q9_status_after.log
echo done > $W/logs/q9.done
