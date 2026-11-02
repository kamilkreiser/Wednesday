#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959; R=$W/repo; Q=$W/logs/q5
[ -e $Q ] && { echo q5 exists; exit 1; }
mkdir -p $Q/p $Q/o1 $Q/o2 $Q/ref
F=Blockchain/Dev/services/auth/src/events.ts
git -C $R diff 2d3b3bb3 pr1959 -- $F > $Q/full.patch
python3 - <<'PY'
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959/logs/q5/'
s=open(W+'full.patch').read().split('\n'); hdr=[];hunks=[];cur=None
for l in s:
    if l.startswith('@@'): cur=[l];hunks.append(cur)
    elif cur is None: hdr.append(l)
    else: cur.append(l)
print('hunks',len(hunks),[h[0] for h in hunks])
for i,h in enumerate(hunks): open(W+'p/h%d.patch'%(i+1),'w').write('\n'.join(hdr+h).rstrip('\n')+'\n')
PY
for o in o1 o2 ref; do mkdir -p $Q/$o/$(dirname $F); git -C $R show 2d3b3bb3:$F > $Q/$o/$F; done
ap() { (cd $1 && git apply --verbose -p1 --whitespace=nowarn $2 2>&1); echo "  rc=$?"; }
echo "== order h1 then h2"; ap $Q/o1 $Q/p/h1.patch; ap $Q/o1 $Q/p/h2.patch
echo "== order h2 then h1"; ap $Q/o2 $Q/p/h2.patch; ap $Q/o2 $Q/p/h1.patch
echo "== whole patch"; ap $Q/ref $Q/full.patch
shasum -a 256 $Q/o1/$F $Q/o2/$F $Q/ref/$F $R/$F
grep -h '^@@' $Q/p/h1.patch $Q/p/h2.patch
