#!/bin/bash
# ks1350_verify.sh — extract the brief's fence as the golden, strict-apply it in a --shared scratch clone at 94c9c7aa,
# and run the controls: tsc --noEmit (originate) and eslint on webhooks.ts, at the tip AND on the golden result.
# Git write verbs only inside the scratch clone it makes (left in the scratchpad, never deleted). rc 0 = controls ran.
set -uo pipefail
B=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1350
SP=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad
SRC=$SP/sparkfeed; TIP=94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812
P=Blockchain/Dev/services/originate/src/routes/webhooks.ts
G=$B/golden/KS-1350.golden.diff
python3 - "$B/KS-1350.md" "$G" <<'PY'
import re,sys
t=open(sys.argv[1]).read(); ch=t.split("## The exact change",1)[1]
f=re.findall(r"^```diff\n(.*?)^```", ch, re.M|re.S); assert len(f)==1
open(sys.argv[2],"w").write(f[0])
PY
echo "golden sha1 $(shasum $G | cut -c1-12)"
C=$(mktemp -d "$SP/ks1350_verify.XXXX")/clone
git clone -q --shared --no-checkout $SRC $C && git -C $C checkout -q --detach $TIP || exit 1
ln -s $SRC/Blockchain/Dev/node_modules $C/Blockchain/Dev/node_modules
ln -s $SRC/Blockchain/Dev/services/originate/node_modules $C/Blockchain/Dev/services/originate/node_modules
ctl(){ ( cd $C/Blockchain/Dev/services/originate && npx --no-install tsc --noEmit -p . > /dev/null 2>&1; echo "  tsc --noEmit -p originate rc=$?"; npx --no-install eslint src/routes/webhooks.ts > /dev/null 2>&1; echo "  eslint src/routes/webhooks.ts rc=$?" ); }
echo "TIP controls:"; ctl
git -C $C apply --check $G; echo "golden git apply --check (strict) rc=$?"
git -C $C apply $G || exit 1
cp $C/$P $B/golden/webhooks.fixed.ts
echo "GOLDEN controls:"; ctl
echo "diff numstat: $(git -C $C diff --numstat)"
echo "changed lines that are not ' * ' comment lines: $(git -C $C diff -U0 | grep -E '^[-+][^-+]' | grep -vE '^[-+] \*' | wc -l | tr -d ' ')"
echo "scratch clone left at $C"
