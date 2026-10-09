#!/bin/bash
# gate79 red arms on REAL data: each instrument, given a wrong value or a planted input, must FAIL by the NAMED check. rc AND line.
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate79; A=$G/arms; X=$G/_scratch/arms; mkdir -p $A $X
export PYTHONDONTWRITEBYTECODE=1
CL=$G/_scratch/clone; H=b4933a457f38fe12551839545431bba000e928fc; B=81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6; T=64d5bf0c31a371a968ec13474f3cdaf6b42541e9; D=349b35c9163ac59209366adb7a4a89d8779bd6d6
read SIM_OK SIM_ROUTE SIM_AUTH < $X/sims.txt
NM=0; NX=0
arm() { local name=$1 want=$2 pat=$3; shift 3; "$@" > $A/red_$name.out 2>&1 < /dev/null; echo $? > $A/red_$name.rc
  local got; got=$(cat $A/red_$name.rc); local line; line=$(grep -m1 -E -- "$pat" $A/red_$name.out | cut -c1-150)
  if [ "$got" = "$want" ] && [ -n "$line" ]; then v=MATCH; NM=$((NM+1)); else v=MISMATCH; NX=$((NX+1)); fi
  printf '%-8s %-30s rc %s (want %s) | %s\n' "$v" "$name" "$got" "$want" "${line:-<asserting line ABSENT: $pat>}"; }
C1="python3 $G/c1_pin_gate79.py --repo $CL --no-remote"
arm c1-real 0 '^0 FAIL' $C1 --head $H --base $B --develop $D --end-tree $T --parents-n 1
arm c1-end-tree-gate78 1 '^FAIL P4' $C1 --head $H --base $B --develop $D --end-tree ccbb76460ad630ab9fdb74b31dfc16502eee94ac --parents-n 1
arm c1-base-is-develop 1 '^FAIL P2 ' $C1 --head $H --base $D --develop $D --end-tree $T --parents-n 1
arm c1-parents-n-2 1 '^FAIL P2 ' $C1 --head $H --base $B --develop $D --end-tree $T --parents-n 2
arm c1-no-end-tree 2 'REFUSED: --end-tree is REQUIRED' $C1 --head $H --base $B --develop $D --parents-n 1
arm c1-develop-touches-route 1 '^FAIL P12' $C1 --head $H --base $B --develop $SIM_ROUTE --end-tree $T --parents-n 1
arm c1-develop-touches-auth 1 '^FAIL P10' $C1 --head $H --base $B --develop $SIM_AUTH --end-tree $T --parents-n 1
arm c1-develop-clean-sim 0 '^0 FAIL' $C1 --head $H --base $B --develop $SIM_OK --end-tree $T --parents-n 1
arm c2-head-is-base 1 '^FAIL D2' python3 $G/c2_code_gate79.py claims --repo $CL --head $B --base $B
arm c2-head-is-develop 1 '^FAIL D4' python3 $G/c2_code_gate79.py claims --repo $CL --head $D --base $B
arm c2-no-base 2 'REFUSED: --base is REQUIRED' python3 $G/c2_code_gate79.py claims --repo $CL --head $H
python3 - $G $X <<'PY'
import sys; g,x=sys.argv[1:3]
b=open(g+'/predictions/pr_body.md',encoding='utf-8').read()
open(x+'/body_foreign_key.md','w',encoding='utf-8').write(b+'\nsame shape as KS-1406.\n')
open(x+'/body_fixes.md','w',encoding='utf-8').write(b.replace('Refs KS-1402','Fixes KS-1402',1))
PY
arm gh-prtext-foreign-key 1 "T3 hyphenated keys .*KS-1406.*False" python3 $G/gh_gate79.py prtext --head $H --repo $CL --base $B --body-file $X/body_foreign_key.md
arm gh-prtext-closing-word 1 "T1 .Refs KS-1402. lines: 0" python3 $G/gh_gate79.py prtext --head $H --repo $CL --base $B --body-file $X/body_fixes.md
arm gh-prtext-real-14rows 1 'T6 CL-ROWS +MISMATCH stated \[\(14,\)\]' python3 $G/gh_gate79.py prtext --head $H --repo $CL --base $B --body-file $G/predictions/pr_body.md
echo "RED ARMS: $NM MATCH, $NX MISMATCH"
