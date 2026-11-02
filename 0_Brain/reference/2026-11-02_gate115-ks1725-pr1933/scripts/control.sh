#!/bin/bash
# Control cells: swap files in the gate's own clone, run the gates, restore by git show, assert sha256.
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate115-ks1725-pr1933/repo
L=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate115-ks1725-pr1933/logs
D=$R/Blockchain/Dev
BASE=8f313815f415c65849210f5d3e30cae44d15a516
HEAD=750da5097e6ba79c0c8c624da4de0f5e2acd4a9d
LOCKS="Blockchain/Dev/package-lock.json Blockchain/Dev/packages/shared/package-lock.json Blockchain/Dev/services/m365-integration/package-lock.json"
BL=Blockchain/Dev/scripts/audit/audit-baseline.json
ALL="$LOCKS $BL Blockchain/Dev/packages/shared/package.json Blockchain/Dev/services/m365-integration/package.json"
sums() { for f in $ALL; do shasum -a 256 "$R/$f"; done; }
sums > $L/ctl_sums_before.txt
restore() { for f in $ALL; do git -C "$R" show "$HEAD:$f" > "$R/$f"; done; sums > $L/ctl_sums_after_$1.txt; cmp -s $L/ctl_sums_before.txt $L/ctl_sums_after_$1.txt && echo "restore $1 OK" || echo "restore $1 MISMATCH"; }
run() { name=$1; (cd "$D" && node scripts/audit/audit-gate.mjs) > $L/ctl_${name}_gate.log 2>&1; g=$?; (cd "$D" && node scripts/audit/audit-locks.mjs) > $L/ctl_${name}_locks.log 2>&1; k=$?; echo "$name gate_rc=$g locks_rc=$k gate_xcx6=$(grep -c xcx6 $L/ctl_${name}_gate.log) locks_xcx6=$(grep -c xcx6 $L/ctl_${name}_locks.log) gate_mrhx=$(grep -c mrhx $L/ctl_${name}_gate.log) locks_mrhx=$(grep -c mrhx $L/ctl_${name}_locks.log)"; }
# C1: base locks + base manifests, head baseline (row removed) -> expect red naming xcx6
for f in $LOCKS Blockchain/Dev/packages/shared/package.json Blockchain/Dev/services/m365-integration/package.json; do git -C "$R" show "$BASE:$f" > "$R/$f"; done
run C1_baselocks_headbaseline; restore C1
# C2: head locks, baseline with BOTH 11-09 rows removed -> expect only mrhx named
python3 -I -c "
import json,sys; p=sys.argv[1]; d=json.load(open(p)); a=d['accepted']
k=[x for x in a if x.startswith('GHSA-mrhx')]; assert len(k)==1; del a[k[0]]; json.dump(d,open(p,'w'),indent=2)" "$R/$BL"
run C2_headlocks_nozodrow; restore C2
# C3: base everything (base baseline) -> expect green (BEFORE)
for f in $ALL; do git -C "$R" show "$BASE:$f" > "$R/$f"; done
run C3_base; restore C3
# C4: head locks + base baseline (row still present) -> expect CLEANUP note for xcx6
git -C "$R" show "$BASE:$BL" > "$R/$BL"
run C4_headlocks_basebaseline; restore C4
