#!/bin/bash
# Assemble the per-brief golden diffs and prove they apply as a chain (scratchpad only; no repo touched).
set -euo pipefail
D=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/ks1341
G=$D/golden
P=Blockchain/Dev/services/originate/src/routes/webhooks.ts
T=Blockchain/Dev/services/originate/src/__tests__

newfile_hunk() { # $1 = test file basename
  local f=$G/$1 n
  n=$(wc -l < "$f" | tr -d ' ')
  printf -- '--- /dev/null\n+++ b/%s/%s\n@@ -0,0 +1,%s @@\n' "$T" "$1" "$n"
  sed 's/^/+/' "$f"
}

# A: two site hunks from diff (U2), then the EOF pure insertion written by hand.
{
  { diff -U2 --label a/$P --label b/$P $D/src/webhooks.ts $G/webhooks.A.ts || true; } | awk '/^@@ -545/{exit} {print}'
  printf '@@ -546,4 +546,22 @@\n'
  printf '   }\n }\n \n'
  sed -n '549,566p' $G/webhooks.A.ts | sed 's/^/+/'
  printf ' export default webhooksRouter;\n'
  newfile_hunk ks1341a-webhooks-500-never-answers-err-message.test.ts
} > $G/A.golden.diff
{ diff -U2 --label a/$P --label b/$P $G/webhooks.A.ts $G/webhooks.AB.ts || true; newfile_hunk ks1341b-webhooks-500-never-answers-err-message.test.ts; } > $G/B.golden.diff
{ diff -U2 --label a/$P --label b/$P $G/webhooks.AB.ts $G/webhooks.ABC.ts || true; newfile_hunk ks1341c-webhooks-500-never-answers-err-message.test.ts; } > $G/C.golden.diff

W=$D/applytest
rm -rf "$W"; mkdir -p "$W/$(dirname $P)" "$W/$T"
cp $D/src/webhooks.ts "$W/$P"
for x in A B C; do
  git -C "$W" apply --check --verbose $G/$x.golden.diff >/dev/null
  git -C "$W" apply $G/$x.golden.diff
  echo "$x: applied strict (git apply, no --recount)"
done
cmp "$W/$P" $G/webhooks.ABC.ts && echo "product after A+B+C == golden ABC"
for x in a b c; do cmp "$W/$T/ks1341$x-webhooks-500-never-answers-err-message.test.ts" $G/ks1341$x-webhooks-500-never-answers-err-message.test.ts && echo "test $x == golden"; done
# A alone reproduces golden A
rm -rf "$W"; mkdir -p "$W/$(dirname $P)" "$W/$T"; cp $D/src/webhooks.ts "$W/$P"
git -C "$W" apply $G/A.golden.diff; cmp "$W/$P" $G/webhooks.A.ts && echo "A alone == golden A"
# B and C each apply on develop+A? (C needs A+B for its source cell only; its hunks are independent)
cp $G/webhooks.A.ts "$W/$P"; rm -f "$W/$T"/*; git -C "$W" apply --check $G/C.golden.diff && echo "C hunks also apply on develop+A (order B/C free for the patch; C's SOURCE cell needs B merged)"
wc -l $G/*.golden.diff
