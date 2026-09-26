#!/bin/bash
# KS-1349: shape the one-hunk golden from the edited clone file, then prove strict apply. Scratch clone only.
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad
C=$S/sparkfeed
W=$S/feed/ks1349
P=Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
python3 - $C $P $W/KS-1349.golden.diff $W/ks730c.1349.ts <<'PY'
import sys,subprocess
C,P,out,fixed=sys.argv[1:]
old=subprocess.run(['git','-C',C,'show','HEAD:'+P],capture_output=True,text=True).stdout.split('\n')
new=open(fixed).read().split('\n')
o=old[111:120]; n=new[111:122]
assert o[0]==n[0] and o[-1]==n[-1]
body=[' '+o[0],'+'+n[1],'+'+n[2]]+[' '+l for l in o[1:7]]+['-'+o[7],'+'+n[9],' '+o[8]]
s=f"--- a/{P}\n+++ b/{P}\n@@ -112,9 +112,11 @@\n"+'\n'.join(body)+'\n'
open(out,'w').write(s); print(s)
PY
git -C $C checkout -- Blockchain/Dev/services/originate
git -C $C apply --check $W/KS-1349.golden.diff; echo "git apply --check (strict) rc=$?"
git -C $C apply $W/KS-1349.golden.diff; echo "git apply rc=$?"
cmp $C/$P $W/ks730c.1349.ts && echo "applied result == ks730c.1349.ts"
git -C $C checkout -- Blockchain/Dev/services/originate
git -C $C show HEAD:$P > $W/tipcopy.ts
sed '1,2d' $W/KS-1349.golden.diff > $W/hunk.only
patch -F0 --dry-run $W/tipcopy.ts < $W/hunk.only; echo "patch -F0 --dry-run rc=$?"
sed 's/calls.at(-1))/calls.at( -1))/' $W/tipcopy.ts > $W/tipcopy_bad.ts
patch -F0 --dry-run $W/tipcopy_bad.ts < $W/hunk.only; echo "control (:119 altered) patch -F0 rc=$?"
rm -f $W/tipcopy_bad.ts $W/hunk.only
git -C $C status --porcelain
