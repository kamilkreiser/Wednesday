#!/bin/bash
# tsc with tests in the program (scratch configs here, outside the repo), base (pr1913 tree) vs head; eslint with planted control.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate100-ks1933-pr1918
R=$G/repo; D=$R/Blockchain/Dev; A=$D/services/billing; TSC=$D/node_modules/.bin/tsc; O=$G/logs/tsc_lint.log
F1=src/routes/webhooks.ts; F2=src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts; F3=src/__tests__/ks488-c4-webhook-idempotency-fail-closed.test.ts
put(){ git -C $R show $1:Blockchain/Dev/services/billing/$2 > $A/$2; }
: > $O
mk() { # name module excludeNew
  local EX='"'$A'/node_modules", "'$A'/dist"'
  [ "$3" = 1 ] && EX="$EX"', "'$A'/src/creditGrants.ts", "'$A'/src/__tests__/ks1933-*"'
  local EXTRA=''; [ "$2" = esnext ] && EXTRA='"module": "esnext", "moduleResolution": "bundler", "target": "ES2022",'
  cat > $G/scripts/tsconfig.$1.json <<JSON
{ "extends": "$A/tsconfig.json",
  "compilerOptions": { $EXTRA "noEmit": true, "declaration": false, "declarationMap": false, "sourceMap": false, "types": ["node"], "typeRoots": ["$D/node_modules/@types"] },
  "include": ["$A/src/**/*", "$D/shared/types/**/*"],
  "exclude": [$EX] }
JSON
}
mk svc_before commonjs 1; mk svc_after commonjs 0; mk esm_before esnext 1; mk esm_after esnext 0
run() {
  builtin cd "$A" || exit 9
  $TSC -p $G/scripts/tsconfig.$1.json --listFilesOnly 2>/dev/null | grep -c '/src/__tests__/' > $G/logs/tsc_$2.examined
  $TSC -p $G/scripts/tsconfig.$1.json > $G/logs/tsc_$2.raw 2>&1; local rc=$?
  grep -E 'error TS[0-9]+' $G/logs/tsc_$2.raw | sed "s#$A/##" | sort > $G/logs/tsc_$2.errors
  sed -E 's/\([0-9]+,[0-9]+\)//' $G/logs/tsc_$2.errors | sort > $G/logs/tsc_$2.multiset
  echo "$2 rc=$rc errors=$(wc -l < $G/logs/tsc_$2.errors) test_files_examined=$(cat $G/logs/tsc_$2.examined) in_changed=$(grep -cE 'webhooks.ts|creditGrants.ts|ks1933|ks1868-billing-webhook-stripe-handler|ks488-c4' $G/logs/tsc_$2.errors)" >> $O
}
for f in $F1 $F2 $F3; do put pr1913 $f; done
run svc_before svc_before; run esm_before esm_before
for f in $F1 $F2 $F3; do put pr1918 $f; done
run svc_after svc_after; run esm_after esm_after
echo "svc multiset diff (line numbers removed):" >> $O; diff $G/logs/tsc_svc_before.multiset $G/logs/tsc_svc_after.multiset >> $O && echo "  identical" >> $O
echo "esm multiset diff:" >> $O; diff $G/logs/tsc_esm_before.multiset $G/logs/tsc_esm_after.multiset >> $O && echo "  identical" >> $O
PL=$A/src/zz_gate100_planted.ts; echo 'export const x: number = "not a number";' > $PL
run esm_after esm_planted; mkdir -p $G/logs/_quarantine; mv $PL $G/logs/_quarantine/zz_gate100_planted.ts.moved
echo "planted reported lines: $(grep -c zz_gate100_planted $G/logs/tsc_esm_planted.errors)" >> $O
builtin cd "$A" || exit 9
$D/node_modules/.bin/eslint $F1 src/creditGrants.ts $F2 $F3 src/__tests__/ks1933-billing-one-purchase-credits-once.test.ts > $G/logs/eslint_pr_files.log 2>&1; echo "eslint 5 pr files rc=$?" >> $O
PL2=$A/src/zz_gate100_lint_planted.ts; printf 'export function f() {\n  const unused = 1;\n  debugger;\n}\n' > $PL2
$D/node_modules/.bin/eslint src/zz_gate100_lint_planted.ts > $G/logs/eslint_planted.log 2>&1; echo "eslint planted rc=$?" >> $O
mv $PL2 $G/logs/_quarantine/zz_gate100_lint_planted.ts.moved
echo "status lines: $(git -C $R status --short | wc -l)" >> $O
