#!/bin/bash
# tsc with the tests in the program (billing has no test tsconfig: scratch configs here, outside the repo), base vs head;
# eslint on the changed .ts files with a planted control. Restores head product by sha256.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate95-ks1868-pr1913
R=$G/repo
D=$R/Blockchain/Dev
A=$D/services/billing
P=$A/src/routes/webhooks.ts
TSC=$D/node_modules/.bin/tsc
O=$G/logs/tsc_lint.log
: > $O
mk() { # $1 name, $2 module, $3 excludeNew(0/1)
  local EX='"'$A'/node_modules", "'$A'/dist"'
  [ "$3" = 1 ] && EX="$EX"', "'$A'/src/__tests__/ks1868-billing-webhook-stripe-*"'
  local EXTRA=''
  [ "$2" = esnext ] && EXTRA='"module": "esnext", "moduleResolution": "bundler", "target": "ES2022",'
  cat > $G/scripts/tsconfig.$1.json <<JSON
{ "extends": "$A/tsconfig.json",
  "compilerOptions": { $EXTRA "noEmit": true, "declaration": false, "declarationMap": false, "sourceMap": false, "types": ["node"], "typeRoots": ["/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate95-ks1868-pr1913/repo/Blockchain/Dev/node_modules/@types"] },
  "include": ["$A/src/**/*", "$D/shared/types/**/*"],
  "exclude": [$EX] }
JSON
}
mk svc_before commonjs 1; mk svc_after commonjs 0; mk esm_before esnext 1; mk esm_after esnext 0
run() { # $1 config, $2 label
  builtin cd "$A" || exit 9
  $TSC -p $G/scripts/tsconfig.$1.json --listFilesOnly 2>/dev/null | grep -c '/src/__tests__/' > $G/logs/tsc_$2.examined
  $TSC -p $G/scripts/tsconfig.$1.json > $G/logs/tsc_$2.raw 2>&1; local rc=$?
  grep -E 'error TS[0-9]+' $G/logs/tsc_$2.raw | sed "s#$A/##" | sort > $G/logs/tsc_$2.errors
  echo "$2 rc=$rc errors=$(wc -l < $G/logs/tsc_$2.errors) test_files_examined=$(cat $G/logs/tsc_$2.examined) in_webhooks.ts=$(grep -c 'routes/webhooks.ts' $G/logs/tsc_$2.errors)" >> $O
}
git -C $R show 03977e89a343:Blockchain/Dev/services/billing/src/routes/webhooks.ts > $P
run svc_before svc_before; run esm_before esm_before
git -C $R show pr1913:Blockchain/Dev/services/billing/src/routes/webhooks.ts > $P
echo "head restored sha256 $(shasum -a 256 $P | awk '{print $1}')" >> $O
run svc_after svc_after; run esm_after esm_after
echo "svc new errors (after minus before):" >> $O; comm -13 $G/logs/tsc_svc_before.errors $G/logs/tsc_svc_after.errors >> $O
echo "esm new errors (after minus before):" >> $O; comm -13 $G/logs/tsc_esm_before.errors $G/logs/tsc_esm_after.errors >> $O
# planted control: a type error in a scratch file under src (moved out afterwards)
PL=$A/src/zz_gate95_planted.ts
echo 'export const x: number = "not a number";' > $PL
run esm_after esm_planted
mkdir -p $G/logs/_quarantine; mv $PL $G/logs/_quarantine/zz_gate95_planted.ts.moved
grep -c zz_gate95_planted $G/logs/tsc_esm_planted.errors | sed 's/^/planted reported lines: /' >> $O
# eslint
builtin cd "$A" || exit 9
$D/node_modules/.bin/eslint src/routes/webhooks.ts src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts src/__tests__/ks1868-billing-webhook-stripe-claim-unreadable-throw.test.ts src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts > $G/logs/eslint_pr_files.log 2>&1; echo "eslint pr files rc=$?" >> $O
PL2=$A/src/zz_gate95_lint_planted.ts
printf 'export function f() {\n  const unused = 1;\n  debugger;\n}\n' > $PL2
$D/node_modules/.bin/eslint src/zz_gate95_lint_planted.ts > $G/logs/eslint_planted.log 2>&1; echo "eslint planted rc=$?" >> $O
mv $PL2 $G/logs/_quarantine/zz_gate95_lint_planted.ts.moved
git -C $R status --short >> $O
