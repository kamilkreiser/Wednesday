#!/bin/bash
# tsc (product tsconfig, and product+tests via a gate-local tsconfig that drops the __tests__ exclude) and eslint,
# at base, commit 1 (positive control for the unused vi) and head.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
O="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
if [ ! -d "$W/wt_c1" ]; then
  git -C "$W/repo" worktree add -q --detach "$W/wt_c1" bdc1d4d8449e74a5be0b231fe9efb759078333e0
  for nm in node_modules Blockchain/Dev/node_modules Blockchain/Dev/services/node_modules Blockchain/Dev/services/anchoring/node_modules Blockchain/Dev/packages/shared/node_modules Blockchain/Dev/packages/shared/dist; do
    ln -s "$O/$nm" "$W/wt_c1/$nm"
  done
fi
for side in base c1 head; do
  A=$W/wt_$side/Blockchain/Dev/services/anchoring
  TSC=$W/wt_$side/Blockchain/Dev/node_modules/.bin/tsc
  cat > "$A/tsconfig.gate159.json" <<'EOF'
{ "extends": "./tsconfig.json", "compilerOptions": { "noEmit": true, "rootDir": "." },
  "include": ["src/**/*"], "exclude": ["node_modules", "dist", "src/__tests__/zz_gate159_probe.test.ts"] }
EOF
  "$TSC" -p "$A/tsconfig.json" --noEmit > "$W/logs/tsc_product_$side.log" 2>&1; echo "rc=$?" >> "$W/logs/tsc_product_$side.log"
  "$TSC" -p "$A/tsconfig.gate159.json" > "$W/logs/tsc_tests_$side.log" 2>&1; echo "rc=$?" >> "$W/logs/tsc_tests_$side.log"
  echo "$side product: $(grep -c 'error TS' "$W/logs/tsc_product_$side.log") errors, $(tail -1 "$W/logs/tsc_product_$side.log")"
  echo "$side with-tests: $(grep -c 'error TS' "$W/logs/tsc_tests_$side.log") errors, $(tail -1 "$W/logs/tsc_tests_$side.log")"
  grep 'error TS' "$W/logs/tsc_tests_$side.log" | sed "s#$A/##"
done
# eslint over the PR's 4 code files
ES=$W/wt_head/Blockchain/Dev/node_modules/.bin/eslint
for side in base c1 head; do
  D=$W/wt_$side/Blockchain/Dev
  files=""
  for f in services/anchoring/src/reconciler.ts services/anchoring/src/cardano/threadTokenIndex.ts services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts; do
    [ -f "$D/$f" ] && files="$files $D/$f"
  done
  ( cd "$D" && "$ES" -f json $files ) > "$W/logs/eslint_$side.log" 2>&1; echo "rc=$?" >> "$W/logs/eslint_$side.log"
  echo "eslint $side: $(tail -2 "$W/logs/eslint_$side.log" | tr '\n' ' ')"
done
# eslint positive control: a planted file in the head worktree with an unused var and a debugger statement
mkdir -p "$W/logs/_plant"
P=$W/wt_head/Blockchain/Dev/services/anchoring/src/zz_gate159_plant.ts
printf 'export function f(): number {\n  const unused = 1;\n  debugger;\n  return 2;\n}\n' > "$P"
( cd "$W/wt_head/Blockchain/Dev" && "$ES" -f json "$P" ) > "$W/logs/eslint_plant.log" 2>&1; echo "rc=$?" >> "$W/logs/eslint_plant.log"
echo "eslint plant: $(cat "$W/logs/eslint_plant.log" | tr '\n' ' ')"
mv "$P" "$W/logs/_plant/zz_gate159_plant.ts"
