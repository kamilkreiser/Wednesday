#!/bin/bash
# usage: run.sh <label> [vitest args...] ; runs billing tests of the gate69 clone (or $BILLING)
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate69-ks1911-1883
B=${BILLING:-$D/repo/Blockchain/Dev/services/billing}
L=$1; shift
nice -n 10 $B/../../node_modules/.bin/vitest run --root "$B" --maxWorkers=3 --reporter=json --outputFile=$D/evidence/$L.json "$@" > $D/evidence/$L.log 2>&1
echo rc=$?
python3 -I - "$D/evidence/$L.json" <<'P'
import json,sys
d=json.load(open(sys.argv[1]))
st={}
bad=[]
for f in d['testResults']:
    for a in f['assertionResults']:
        st[a['status']]=st.get(a['status'],0)+1
        if a['status']!='passed': bad.append(a['title'])
print(len(d['testResults']),'files',st,'suiteFail',sum(1 for f in d['testResults'] if f['status']!='passed' and not f['assertionResults']))
for b in bad: print(' NOTPASS:',b)
P
