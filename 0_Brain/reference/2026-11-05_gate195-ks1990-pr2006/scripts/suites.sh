#!/bin/bash
# gate 195 Q8: whole originate at head, then at base (overlay), tsc + control, eslint + control, docs-fragments + planted defects
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate195-ks1990-pr2006; R=$W/repo; D=$R/Blockchain/Dev; S=$D/services/originate
HEAD=6311c141f99e5ade8d94e60ee15b0c80006a52cd; BASE=07a2d62be6a09c9cd504864d1cf1906543d55317
P1=Blockchain/Dev/services/originate/src/routes/adminConfig.ts
P2=Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
P3=Blockchain/Dev/services/originate/src/__tests__/ks1990-seed-demo-users-success-follows-the-counts.test.ts
Q=$W/scratch/_quarantine; mkdir -p $Q $W/cwd
cd $W/cwd || exit 9
E="env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp"
JT(){ log=$1; shift; $E nice -n 10 $D/node_modules/.bin/jest --rootDir $S -c $S/jest.config.js "$@" > $log 2>&1; echo "rc=$?" >> $log; }
JT $W/logs/q8_whole_head.log
# base overlay
git -C $R show $BASE:$P1 > $R/$P1; git -C $R show $BASE:$P2 > $R/$P2; mv $R/$P3 $Q/ks1990.head.test.ts
JT $W/logs/q8_whole_base.log
JT $W/logs/q8_seatfiles_at_base.log ks1990 ks1802
git -C $R show $HEAD:$P1 > $R/$P1; git -C $R show $HEAD:$P2 > $R/$P2; git -C $R show $HEAD:$P3 > $R/$P3
echo "restored: $(git -C $R status --short | wc -l) status lines" > $W/logs/q8_restore.log
# red-at-base for the seat's files with per-test result: product at base, tests at head
git -C $R show $BASE:$P1 > $R/$P1
$E nice -n 10 $D/node_modules/.bin/jest --rootDir $S -c $S/jest.config.js ks1990 ks1802 --json --outputFile=$W/logs/q8_red_base.json > $W/logs/q8_red_base.log 2>&1; echo "rc=$?" >> $W/logs/q8_red_base.log
git -C $R show $HEAD:$P1 > $R/$P1
echo "restored2: $(git -C $R status --short | wc -l) status lines" >> $W/logs/q8_restore.log
# tsc head + planted control
$E nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.json --noEmit > $W/logs/q8_tsc_head.log 2>&1; echo "rc=$?" >> $W/logs/q8_tsc_head.log
printf 'export const g195TscControl: number = "not a number";\n' > $S/src/g195-tsc-control.ts
$E nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.json --noEmit > $W/logs/q8_tsc_control.log 2>&1; echo "rc=$?" >> $W/logs/q8_tsc_control.log
mv $S/src/g195-tsc-control.ts $Q/
# eslint
( cd $D && $E nice -n 10 $D/node_modules/.bin/eslint services/originate/src/routes/adminConfig.ts services/originate/src/__tests__/ks1990-seed-demo-users-success-follows-the-counts.test.ts services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts > $W/logs/q8_eslint_head.log 2>&1; echo "rc=$?" >> $W/logs/q8_eslint_head.log )
printf 'export function g195(): number {\n  const unused = 1;\n  debugger;\n  return 2;\n}\n' > $S/src/routes/g195-eslint-control.ts
( cd $D && $E nice -n 10 $D/node_modules/.bin/eslint services/originate/src/routes/g195-eslint-control.ts > $W/logs/q8_eslint_control.log 2>&1; echo "rc=$?" >> $W/logs/q8_eslint_control.log )
mv $S/src/routes/g195-eslint-control.ts $Q/
# docs fragments
chk(){ $E nice -n 10 node $D/scripts/docs-fragments.mjs check --root $R > "$1" 2>&1; echo "rc=$?" >> "$1"; }
chk $W/logs/q8_frag_clean.log
F="$R/Projects Documents/fragments/flow/KS-1990-seed-demo-users-success-follows-counts.html"
h=$(shasum -a 256 "$F" | awk '{print $1}'); cp "$F" $W/scratch/frag_orig.html
printf '\n<div>g195 planted unclosed</div><div>\n' >> "$F"
chk $W/logs/q8_frag_planted.log
cp $W/scratch/frag_orig.html "$F"; [ "$(shasum -a 256 "$F" | awk '{print $1}')" = "$h" ] && echo "frag restore OK" >> $W/logs/q8_restore.log
git -C $R status --short >> $W/logs/q8_restore.log
echo done > $W/logs/q8.done
