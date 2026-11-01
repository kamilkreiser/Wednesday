#!/bin/bash
# Re-check the -C1 apply conditions in a throwaway git dir inside the workdir.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911
R=$W/repo; S=$W/c1scratch; RU=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_
F=Blockchain/Dev/services/auth/src/routes/auth.ts
[ -e $S ] && { echo "scratch exists, abort"; exit 1; }
mkdir -p $S/$(dirname $F); git -C $S init -q
git -C $R show refs/gate/develop:$F > $S/$F; cp $S/$F $W/logs/base_auth.ts
git -C $R show refs/gate/pr1911:$F > $W/logs/head_auth.ts
for p in p1_auth_register_publish_event_unreadable_throw p2_auth_login_publish_event_unreadable_throw; do
  SEC=$RU$p/out.md.checker/section_1.diff; k=${p:0:2}
  echo "== $k (1) plain apply --check"; git -C $S apply --check -p1 $SEC; echo "rc=$?"
  echo "== $k -C1 --check (real)"; git -C $S apply --check -C1 -p1 $SEC; echo "rc=$?"
  # (2) corrupted content controls: alter the context line next to the change, the removed line, and the outermost context line
  for which in adjacent removed outermost; do
    cp $W/logs/base_auth.ts $S/$F
    python3 -I - "$S/$F" "$SEC" "$which" <<'PY'
import sys,re
f,sec,which=sys.argv[1:]
lines=[l for l in open(sec).read().splitlines() if l.startswith((' ','-')) and not l.startswith('---')]
ctx=[l[1:] for l in lines if l[0]==' ']; rem=[l[1:] for l in lines if l[0]=='-']
t={'adjacent':ctx[-1],'removed':rem[0],'outermost':ctx[0]}[which]
s=open(f).read(); n=s.count(t+'\n')
# corrupt only the occurrence inside the hunk's region: hunk start line
m=re.search(r'@@ -(\d+)',open(sec).read()); start=int(m.group(1))
L=s.split('\n'); idx=[i for i,x in enumerate(L) if x==t and abs(i+1-start)<12]
assert len(idx)==1,(which,idx); L[idx[0]]=L[idx[0]]+' /*CORRUPT*/'
open(f,'w').write('\n'.join(L)); print('corrupted',which,'line',idx[0]+1)
PY
    git -C $S apply --check -C1 -p1 $SEC 2>&1 | head -2; echo "$k -C1 corrupt-$which rc=${PIPESTATUS[0]}"
  done
  cp $W/logs/base_auth.ts $S/$F
done
# (3) apply all three in the author's order P3, P1, P2 and compare to head
cp $W/logs/base_auth.ts $S/$F
git -C $S apply -p1 ${RU}p3_auth_reset_password_revoke_unreadable_throw/out.md.checker/section_1.diff; echo "p3 strict apply rc=$?"
git -C $S apply -C1 -p1 ${RU}p1_auth_register_publish_event_unreadable_throw/out.md.checker/section_1.diff; echo "p1 -C1 apply rc=$?"
git -C $S apply -C1 -p1 ${RU}p2_auth_login_publish_event_unreadable_throw/out.md.checker/section_1.diff; echo "p2 -C1 apply rc=$?"
cmp $S/$F $W/logs/head_auth.ts && echo "applied(P3,P1,P2) == HEAD auth.ts: IDENTICAL"
shasum -a 256 $S/$F $W/logs/head_auth.ts $W/logs/base_auth.ts
echo "p2 no-suffix vs -r2 section_1:"; diff ${RU}p2_auth_login_publish_event_unreadable_throw/out.md.checker/section_1.diff ${RU}p2_auth_login_publish_event_unreadable_throw-r2/out.md.checker/section_1.diff; echo "diff rc=$?"
