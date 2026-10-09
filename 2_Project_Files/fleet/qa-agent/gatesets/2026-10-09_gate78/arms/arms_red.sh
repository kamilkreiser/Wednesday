#!/bin/bash
# gate78 RED ARMS ON REAL DATA: each check script run with a wrong pin / a planted input must FAIL (rc 1) or REFUSE (rc 2), on its named check.
# Every path written is under this kit's _scratch/. NO arm names a !CODING path (Wednesday's rule after a stray directory, 2026-10-09);
# the --wt / --out guard is proved lexically in c5 --selftest only. Output: $G/arms/red_<arm>.{out,rc}
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate78; A=$G/arms; S=$G/_scratch; X=$S/redarms; mkdir -p $A $X
export PYTHONDONTWRITEBYTECODE=1
H=6f4adfe8835ec8ece51653f3f758d6a55ce12348; B=1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0; T=ccbb76460ad630ab9fdb74b31dfc16502eee94ac; C=$S/clone
NM=0; NX=0
arm() { local name=$1 want=$2 pat=$3; shift 3; "$@" > $A/red_$name.out 2>&1 < /dev/null; echo $? > $A/red_$name.rc
  local got; got=$(cat $A/red_$name.rc); local line; line=$(grep -m1 -E -- "$pat" $A/red_$name.out | cut -c1-150)
  if [ "$got" = "$want" ] && [ -n "$line" ]; then v=MATCH; NM=$((NM+1)); else v=MISMATCH; NX=$((NX+1)); fi
  printf '%-8s %-30s rc %s (want %s) | %s\n' "$v" "$name" "$got" "$want" "${line:-<asserting line ABSENT: $pat>}"; }
python3 - $G $X <<'PY'
import json, sys
g, x = sys.argv[1:3]; k = json.load(open(g + '/kit.json'))
a = json.loads(json.dumps(k)); a['reach_builder_claims']['images_shipping'] = ['services/originate', 'services/governance']; a['reach_builder_claims']['not_shipping'] = ['services/referral', 'services/vc-issuer']
json.dump(a, open(x + '/kit_reach_planted.json', 'w'))
b = json.loads(json.dumps(k)); b['actions']['needles_change'] = b['actions']['needles_change'] + ['##[error]']; json.dump(b, open(x + '/kit_needle_planted.json', 'w'))
c = json.loads(json.dumps(k)); c['linear_ok_states'] = ['Done']; json.dump(c, open(x + '/kit_linear_planted.json', 'w'))
d = json.loads(json.dumps(k)); d['nc_arms'] = [['NC1', 'Blockchain/Dev/package-lock.json', 'leg7', 'leg6']]; json.dump(d, open(x + '/kit_nc_planted.json', 'w'))
body = open(g + '/predictions/gh_body.md').read()
assert 'all 7 declaring parents' in body and 'KS 1453 and is **not** touched' in body
open(x + '/body_8_parents.md', 'w').write(body.replace('all 7 declaring parents', 'all 8 declaring parents'))
open(x + '/body_hyphen_sib.md', 'w').write(body.replace('KS 1453 and is **not** touched', 'KS-1453 and is **not** touched'))
PY
arm c1-wrong-end-tree 1 'FAIL P4' python3 $G/c1_pin_gate78.py --repo $C --head $H --base $B --develop $B --end-tree 85820a21f80c02d542ca1cf62e194750f2779c28 --parents-n 1 --no-remote
arm c1-wrong-base 1 'FAIL P2 ' python3 $G/c1_pin_gate78.py --repo $C --head $H --base b39051390ff6f252601d6f7b45f0ea6c21c31023 --develop $B --end-tree $T --parents-n 1 --no-remote
arm c1-parents-n-2 1 'FAIL P2 ' python3 $G/c1_pin_gate78.py --repo $C --head $H --base $B --develop $B --end-tree $T --parents-n 2 --no-remote
arm c1-missing-end-tree 2 'REFUSED: --end-tree is REQUIRED' python3 $G/c1_pin_gate78.py --repo $C --head $H --base $B --develop $B --parents-n 1 --no-remote
arm c2-diff-head-is-base 1 'FAIL L1' python3 $G/c2_locks_gate78.py diff --repo $C --head $B --base $B
arm c2-diff-missing-base 2 'REFUSED: --base is REQUIRED' python3 $G/c2_locks_gate78.py diff --repo $C --head $H
arm c2-parse-base-expect-clean 1 'FAIL S2' python3 $G/c2_locks_gate78.py parse --repo $C --rev $B --expect-clean
arm c3-tarballs-head-is-base 1 'FAIL T3' python3 $G/c3_registry_gate78.py tarballs --repo $C --head $B --base $B --out $X/tar_headisbase
arm c3-tarballs-reused-dir 2 'REFUSED: .* exists and is not empty' python3 $G/c3_registry_gate78.py tarballs --repo $C --head $H --base $B --out $S/tar_draft1
arm c5-legs-base-expect-pass 1 'FAIL G-HEAD' python3 $G/c5_legs_gate78.py legs --wt $S/wtBase --expect pass --out $X/legs_base_pass
arm c5-legs-head-expect-fail 1 'FAIL G-BASE' python3 $G/c5_legs_gate78.py legs --wt $S/wtHead --expect fail --out $X/legs_head_fail
arm c5-omit-head-tagged-base 1 'FAIL OMIT-BASE' python3 $G/c5_legs_gate78.py omit --wt $S/wtHead --repo $C --base $B --out $X/omit_mistagged --tag base
arm c5-nc-legs-swapped 1 'FAIL NC1' env G78_KITJSON=$X/kit_nc_planted.json python3 $G/c5_legs_gate78.py nc --wt $S/wtHead --repo $C --base $B --out $X/nc_swapped
arm c6-reach-claims-planted 1 'FAIL R4' env G78_KITJSON=$X/kit_reach_planted.json python3 $G/c6_reach_gate78.py reach --repo $C --rev $H
arm gh-prtext-8-parents 1 'T6 CL-PARENTS +MISMATCH' python3 $G/gh_gate78.py prtext --head $H --measured $G/predictions/c2_diff.json --reach $G/predictions/c6_reach.json --tar $G/predictions/c3_tar.json --body-file $X/body_8_parents.md
arm gh-prtext-hyphen-sibling 1 'T3 hyphenated keys .*KS-1453' python3 $G/gh_gate78.py prtext --head $H --measured $G/predictions/c2_diff.json --reach $G/predictions/c6_reach.json --tar $G/predictions/c3_tar.json --body-file $X/body_hyphen_sib.md
arm gh-actions-needle-planted 1 'CLASSIFY .*UNCLASSIFIED' env G78_KITJSON=$X/kit_needle_planted.json python3 $G/gh_gate78.py actions --at $H --develop $B --out $X/actions_needle
arm gh-linear-state-planted 1 'VERDICT KS-1452 FINDING' env G78_KITJSON=$X/kit_linear_planted.json python3 $G/gh_gate78.py linear
echo "RED ARMS: $NM MATCH, $NX MISMATCH"
