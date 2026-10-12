#!/usr/bin/env bash
# T5 mutants. Every mutation is asserted landed before the run; every run restores via git and asserts a clean tree.
S=<scratch>
W=$S/wt-head; D=$W/Blockchain/Dev; V=$D/services/vc-issuer; BL=$D/scripts/typecheck-tests/baseline-vc-issuer.txt
Q=$S/quarantine; mkdir -p $Q
F=$V/src/__tests__/smoke.test.ts
restore() {
  git -C $W checkout -q -- Blockchain/Dev
  [ -e $V/src/__tests__/zz-gate.test.ts ] && mv $V/src/__tests__/zz-gate.test.ts $Q/zz-gate.$RANDOM
  n=$(git -C $W status --porcelain | wc -l | tr -d ' '); echo "   restored, dirty=$n"
}
leg() { bash $S/harness/leg16.sh $D > $S/ev/$1.log 2>&1; echo "   rc=$?"; grep -E "$2" $S/ev/$1.log | sed 's/^/   /'; }
PAT='vc-issuer|OK —|FAIL —|EXAMINED|nocheck|no tsconfig|HARNESS'

echo "== T5b move tsconfig.test.json away"; mv $V/tsconfig.test.json $Q/; [ ! -e $V/tsconfig.test.json ] && echo "   landed"
leg T5b "$PAT"; restore
echo "== T5c1 move baseline away (clean tree)"; mv $BL $Q/; [ ! -e $BL ] && echo "   landed"
leg T5c1 "$PAT"; restore
echo "== T5c2 move baseline away AND move a test file away"; mv $BL $Q/; mv $F $Q/; [ ! -e $BL ] && [ ! -e $F ] && echo "   landed"
leg T5c2 "$PAT"; restore
echo "== T5e move one test file away (baseline present)"; mv $F $Q/; [ ! -e $F ] && echo "   landed"
leg T5e "$PAT"; restore
echo "== T5f add an 18th test file"; cp $F $V/src/__tests__/zz-gate.test.ts && echo "   landed"
leg T5f "$PAT"; restore
echo "== T5g @ts-nocheck in a vc-issuer test"; { echo '// @ts-nocheck'; cat $S/smoke.orig; } > $F; head -1 $F | sed 's/^/   landed: /'
leg T5g "$PAT"; restore
echo "== T5h @ts-expect-error over a planted error (documented hole)"; printf '\n// @ts-expect-error gate\nexport const __g: number = "x";\n' >> $F; grep -c 'ts-expect-error gate' $F | sed 's/^/   landed: /'
leg T5h "$PAT"; restore
echo "== T5i hand-add a baseline entry admitting a planted error, in the same change"
printf '\nexport const __gatePlant: number = "x";\n' >> $F
FP=$(node -e '
const c=require("crypto");const code="TS2322",t="Type '"'"'string'"'"' is not assignable to type '"'"'number'"'"'.";
console.log(c.createHash("sha1").update(code+"\n"+t).digest("hex").slice(0,8))')
echo "src/__tests__/smoke.test.ts TS2322 $FP 1" >> $BL; echo "   landed: $(tail -1 $BL)"
leg T5i "$PAT"; restore
echo "== T5j hand-lower the floor to 16 and move a test file away"; sed -i '' 's/^examined-test-files 17$/examined-test-files 16/' $BL; mv $F $Q/; grep -c '^examined-test-files 16$' $BL | sed 's/^/   landed: /'
leg T5j "$PAT"; restore
