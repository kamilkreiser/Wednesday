#!/bin/bash
W=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed/ks1334
C=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/sparkfeed
sed -i '' 's/so "leaked: false" above is not vacuous/so leaked: false above is not vacuous/' $W/t3_insert.ts
echo "double quotes in insert: $(grep -c '"' $W/t3_insert.ts)"
python3 - $W <<'EOF'
import sys
W=sys.argv[1]
P=open(f'{W}/adminConfig.tip.ts').read().split('\n')
T=open(f'{W}/ks730c.tip.ts').read().split('\n')
ins=open(f'{W}/t3_insert.ts').read().rstrip('\n').split('\n')
T2=T[:141]+["      .toEqual({ liveTernaries: 0, helperCalls: 48, distinctContexts: 48 });"]+T[142:171]+T[172:203]+ins+T[203:]
open(f'{W}/ks730c.A.ts','w').write('\n'.join(T2))
PP='Blockchain/Dev/services/originate/src/routes/adminConfig.ts'
TT='Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts'
n113="    fail500(res, 'Admin config request failed (POST /api/admin/refresh-tenants)', err);"
n1859="    fail500(res, 'Admin config request failed (POST /api/admin/backfill-certification-metadata)', err);"
L=lambda a,i:a[i-1]
prod=[f"--- a/{PP}",f"+++ b/{PP}","@@ -112,3 +112,3 @@"," "+L(P,112),"-"+L(P,113),"+"+n113," "+L(P,114),
 "@@ -1857,4 +1857,4 @@"," "+L(P,1857)," "+L(P,1858),"-"+L(P,1859),"+"+n1859," "+L(P,1860)]
t=[f"--- a/{TT}",f"+++ b/{TT}","@@ -141,3 +141,3 @@"," "+L(T,141),"-"+L(T,142),"+      .toEqual({ liveTernaries: 0, helperCalls: 48, distinctContexts: 48 });"," "+L(T,143),
 "@@ -171,3 +171,2 @@"," "+L(T,171),"-"+L(T,172)," "+L(T,173),
 f"@@ -203,2 +202,{len(ins)+2} @@"," "+L(T,203)]+["+"+x if x else "+" for x in ins]+[" "+L(T,204)]
open(f'{W}/KS-1334-A.golden.diff','w').write('\n'.join(prod+t)+'\n')
open(f'{W}/prod_hunks.txt','w').write('\n'.join(prod[2:])+'\n')
open(f'{W}/test_hunks.txt','w').write('\n'.join(t[2:])+'\n')
print('test lines after', len(T2)-1, 'insert lines', len(ins))
EOF
git -C $C apply --check $W/KS-1334-A.golden.diff; echo "git apply --check (strict) rc=$?"
rm -rf $W/pt; mkdir -p $W/pt
git -C $C archive 3f70224a Blockchain/Dev/services/originate/src/routes/adminConfig.ts Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts | tar -x -C $W/pt
patch -d $W/pt -p1 -F0 < $W/KS-1334-A.golden.diff; echo "patch -p1 -F0 rc=$?"
cmp $W/pt/Blockchain/Dev/services/originate/src/routes/adminConfig.ts $W/adminConfig.A.ts && echo "product == adminConfig.A.ts"
cmp $W/pt/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts $W/ks730c.A.ts && echo "test == ks730c.A.ts"
echo "blank context lines in diff: $(/usr/bin/grep -c '^ $' $W/KS-1334-A.golden.diff) (control, lone-plus lines: $(/usr/bin/grep -c '^+$' $W/KS-1334-A.golden.diff))"
# tamper control: :1859 changed -> patch must refuse
rm -rf $W/ptt; mkdir -p $W/ptt; cp -R $W/pt/../pt $W/ptt/ 2>/dev/null
rm -rf $W/ptt; mkdir -p $W/ptt
git -C $C archive 3f70224a Blockchain/Dev/services/originate/src/routes/adminConfig.ts Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts | tar -x -C $W/ptt
sed -i '' '1859s/err.message/err.msg/' $W/ptt/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
patch -d $W/ptt -p1 -F0 --dry-run < $W/KS-1334-A.golden.diff >/dev/null 2>&1; echo "control: :1859 tampered, patch -F0 dry-run rc=$? (want 1)"
