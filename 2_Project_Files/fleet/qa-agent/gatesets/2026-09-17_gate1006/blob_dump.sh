#!/bin/zsh
# blob_dump.sh — READ-ONLY: git show the PR's files at develop / prev / head into src/, plus the diffs. Read verbs only.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1006'
H=86fe59e6bf07108142fb3dbd06bef8747d2a4687
P=e28c91f9b990273ea34036cb88ad6abf0f39e73b
DEV=40fe4db6963cd11dba06bd46e0b00af39e68ef3a
D=Blockchain/Dev
mkdir -p "$G/src"
echo "blob_dump $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" diff $DEV $H > "$G/diff_develop_to_head.patch"; echo "diff develop..head rc=$? lines $(wc -l < "$G/diff_develop_to_head.patch")"
git -C "$R" diff $P $H > "$G/diff_prev_to_head.patch"; echo "diff prev..head rc=$? lines $(wc -l < "$G/diff_prev_to_head.patch")"
for spec in \
  "services/demo-service/src/app.ts:app" \
  "services/demo-service/src/middleware/errorHandler.ts:errorHandler" \
  "services/demo-service/src/__tests__/ks844-demo-service-mounts-no-error-handler.test.ts:ks844" \
  "packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts:ks727" \
  "packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts:ks781p33" ; do
  f="${spec%%:*}"; n="${spec##*:}"
  for pair in "develop:$DEV" "prev:$P" "head:$H"; do
    t="${pair%%:*}"; s="${pair##*:}"
    if git -C "$R" cat-file -e "$s:$D/$f" 2>/dev/null; then
      git -C "$R" show "$s:$D/$f" > "$G/src/${n}_${t}.ts"
      echo "$t $n blob $(git -C "$R" rev-parse "$s:$D/$f") lines $(wc -l < "$G/src/${n}_${t}.ts" | tr -d ' ') sha256 $(shasum -a 256 "$G/src/${n}_${t}.ts" | cut -c1-16)"
    else
      echo "$t $n ABSENT"
    fi
  done
done
echo "--- demo-service tree at head"
git -C "$R" ls-tree -r --name-only $H -- $D/services/demo-service | grep -v node_modules
