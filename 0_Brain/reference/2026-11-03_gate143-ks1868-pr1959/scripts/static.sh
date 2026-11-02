#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959; R=$W/repo; L=$W/logs
D=$R/Blockchain/Dev; A=$D/services/auth; N=$D/node_modules/.bin
P=$A/src/events.ts; SHA=$(shasum -a 256 $P | cut -d' ' -f1)
echo "== tsc own tsconfig head"; $N/tsc -p $A/tsconfig.json --noEmit > $L/tsc_head_own.log 2>&1; echo rc=$? ; wc -l < $L/tsc_head_own.log
echo "== tsc tests head"; $N/tsc -p $A/tsconfig.test.json > $L/tsc_head_test.log 2>&1; echo rc=$?; grep -c 'error TS' $L/tsc_head_test.log
cp $A/src/events_base.ts $P
echo "== tsc tests base"; $N/tsc -p $A/tsconfig.test.json > $L/tsc_base_test.log 2>&1; echo rc=$?; grep -c 'error TS' $L/tsc_base_test.log
cp $L/events_head.ts.bak $P; [ "$(shasum -a 256 $P | cut -d' ' -f1)" = "$SHA" ] && echo restored-ok
echo "== eslint"; $N/eslint --no-warn-ignored $P $A/src/__tests__/ks1868-auth-events-*.test.ts > $L/eslint_head.log 2>&1; echo rc=$?; tail -5 $L/eslint_head.log
printf 'debugger;\nconst unusedGate = 1;\n' > $A/src/__gate_plant.ts
$N/eslint $A/src/__gate_plant.ts > $L/eslint_plant.log 2>&1; echo plant rc=$?; mv $A/src/__gate_plant.ts $L/_quarantine/
echo "== ratchet"; bash $D/scripts/preflight/test-types-ratchet.sh $A > $L/ratchet.log 2>&1; echo rc=$?; tail -4 $L/ratchet.log
echo "== docs-fragments"; node $D/scripts/docs-fragments.mjs check --root $R > $L/docs_check.log 2>&1; echo rc=$?; tail -5 $L/docs_check.log
for f in flow cheat; do F="$R/Projects Documents/fragments/$f/KS-1868-auth-events-bus.html"; S=$(shasum -a 256 "$F"|cut -d' ' -f1); cp "$F" $L/_frag_$f.bak
 if [ $f = flow ]; then sed -i '' 's/<!--n-->//' "$F"; else printf '<div>\n' >> "$F"; fi
 node $D/scripts/docs-fragments.mjs check --root $R > $L/docs_plant_$f.log 2>&1; echo "plant $f rc=$?"
 cp $L/_frag_$f.bak "$F"; [ "$(shasum -a 256 "$F"|cut -d' ' -f1)" = "$S" ] && echo "restored $f"
done
node $D/scripts/docs-fragments.mjs check --root $R > $L/docs_check_after.log 2>&1; echo after rc=$?
git -C $R status --short
