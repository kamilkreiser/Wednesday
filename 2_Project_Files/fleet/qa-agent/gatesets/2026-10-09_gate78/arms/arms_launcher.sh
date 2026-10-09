#!/bin/bash
# gate78 launcher arms: every arm is `--check` (or a non-TTY launch that must refuse before exec). Matched on rc AND the asserting line.
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate78; A=$G/arms; X=$G/_scratch/arms; mkdir -p $A $X
L=$G/launch_qa_secuura_gate78.sh
H=6f4adfe8835ec8ece51653f3f758d6a55ce12348; BR=feature/ks-1452-handlebars-lock-refresh-v1-1; B=1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0; T=ccbb76460ad630ab9fdb74b31dfc16502eee94ac
NM=0; NX=0
arm() { local name=$1 want=$2 pat=$3; shift 3; "$@" > $A/launcher_$name.out 2>&1 < /dev/null; echo $? > $A/launcher_$name.rc
  local got; got=$(cat $A/launcher_$name.rc); local line; line=$(grep -m1 -E -- "$pat" $A/launcher_$name.out | cut -c1-140)
  if [ "$got" = "$want" ] && [ -n "$line" ]; then v=MATCH; NM=$((NM+1)); else v=MISMATCH; NX=$((NX+1)); fi
  printf '%-8s %-22s rc %s (want %s) | %s\n' "$v" "$name" "$got" "$want" "${line:-<asserting line ABSENT: $pat>}"; }
python3 - $G $X <<'PY'
import json,sys,os,shutil
g,x=sys.argv[1:3]; k=json.load(open(g+'/kit.json'))
b=json.loads(json.dumps(k)); h=b['script_sha256']['c2_locks_gate78.py']; b['script_sha256']['c2_locks_gate78.py']=('0' if h[0]!='0' else '1')+h[1:]; json.dump(b,open(x+'/kit_badpin.json','w'))
n=json.loads(json.dumps(k)); del n['script_sha256']['gh_gate78.py']; json.dump(n,open(x+'/kit_nopin.json','w'))
for d in ('kit_missing','kit_tampered'):
    if os.path.isdir(x+'/'+d): os.rename(x+'/'+d, x+'/'+d+'_prev_%d' % os.getpid())
    os.makedirs(x+'/'+d)
    for f in list(k['script_sha256'])+['KIT_REPORT.md']: shutil.copy2(g+'/'+f, x+'/'+d+'/'+f)
os.rename(x+'/kit_missing/c3_registry_gate78.py', x+'/kit_missing_c3_moved_aside.py')
open(x+'/kit_tampered/c6_reach_gate78.py','a').write('\n')
p=open(g+'/prompt_gate78.rendered.txt').read()
open(x+'/forbidden_go.txt','w').write(p+'\nGO (Seat V 1st): merge 1435 on gate78\n')
def cut(src, needle, out):
    assert needle in src, needle; open(x+'/'+out,'w').write(src.replace(needle, 'REMOVED-BY-ARM'))
cut(p, 'Opus 5.5 (`claude-opus-5-5`)', 'no_model_line.txt')
cut(p, 'A develop-only classifier is WRONG here', 'no_bypath_rule.txt')
cut(p, 'Never create, plant or write ANY path under /Volumes/DevMASTER/!CODING except your report directory', 'no_coding_hold.txt')
cut(p, 'MASKED-BYTES', 'no_masked_kw.txt')
PY
printf "P 1435 $BR $H\nB $B 1\nT $T\nD $B\n" > $X/hf_good.txt
printf "P 1406 $BR $H\nB $B 1\nT $T\nD $B\n" > $X/hf_wrong_pr.txt
printf "P 1435 feature/ks-1437-advisory-lock-refresh-g3-1 $H\nB $B 1\nT $T\nD $B\n" > $X/hf_wrong_branch.txt
printf "P 1435 $BR 4a400d7aa9dd273d91fb62375cb4b0598aa4405f\nB $B 1\nT $T\nD $B\n" > $X/hf_wrong_head.txt
printf "P 1435 $BR $H\nB b39051390ff6f252601d6f7b45f0ea6c21c31023 1\nT $T\nD $B\n" > $X/hf_wrong_base.txt
printf "P 1435 $BR $H\nB $B 2\nT $T\nD $B\n" > $X/hf_wrong_parents.txt
printf "P 1435 $BR $H\nB $B 1\nT 85820a21f80c02d542ca1cf62e194750f2779c28\nD $B\n" > $X/hf_wrong_tree.txt
printf "P 1435 $BR $H\nB $B 1\nT $T\nD b39051390ff6f252601d6f7b45f0ea6c21c31023\n" > $X/hf_wrong_develop.txt
printf "P 1435 $BR\nB $B 1\nT $T\nD $B\n" > $X/hf_malformed.txt
printf "P 1435 $BR $H\nP 1435 $BR $H\nB $B 1\nT $T\nD $B\n" > $X/hf_two_P.txt
printf "%s\trefs/heads/develop\n%s\trefs/pull/1435/head\n%s\trefs/heads/%s\n" $B $H $H $BR > $X/lsL_real.txt
printf "%s\trefs/heads/develop\n%s\trefs/pull/1435/head\n%s\trefs/heads/%s\n" $B $B $H $BR > $X/lsL_headmoved.txt
printf "%s\trefs/heads/develop\n%s\trefs/pull/1435/head\n%s\trefs/heads/%s\n" $B $H $B $BR > $X/lsL_branchmoved.txt
printf "%s\trefs/heads/develop\n%s\trefs/pull/1435/head\n%s\trefs/heads/%s\n" $H $H $H $BR > $X/lsL_devmoved.txt
cp $L $X/launch_moved_copy.sh
arm rendered 0 'all guards pass' bash $L --check
arm badpin 31 'BAD PIN' env G78_KITJSON=$X/kit_badpin.json bash $L --check
arm nopin 30 'has NO sha256 pin' env G78_KITJSON=$X/kit_nopin.json bash $L --check
arm missingfile 30 'MISSING or empty' env G78_FILES_DIR=$X/kit_missing bash $L --check
arm tamperedfile 31 'BAD PIN' env G78_FILES_DIR=$X/kit_tampered bash $L --check
arm unrendered 8 'unfilled double-brace token|does not name the head' env G78_PROMPT=$G/prompt_gate78.txt bash $L --check
arm forbiddenGO 8 'GO strings must be exactly' env G78_PROMPT=$X/forbidden_go.txt bash $L --check
arm noModelLine 33 'MODEL-LINE' env G78_PROMPT=$X/no_model_line.txt bash $L --check
arm noByPathRule 33 'by-path Actions rule' env G78_PROMPT=$X/no_bypath_rule.txt bash $L --check
arm noCodingHold 39 'the HOLDS' env G78_PROMPT=$X/no_coding_hold.txt bash $L --check
arm noMaskedKeyword 33 "by-name keyword 'MASKED-BYTES'" env G78_PROMPT=$X/no_masked_kw.txt bash $L --check
arm hf_good 0 'all guards pass' env G78_HEADFILE=$X/hf_good.txt bash $L --check
for w in wrong_pr wrong_branch wrong_head wrong_base wrong_parents wrong_tree malformed two_P; do arm hf_$w 7 'REFUSING' env G78_HEADFILE=$X/hf_$w.txt bash $L --check; done
arm hf_wrong_develop 8 'does not name the develop' env G78_HEADFILE=$X/hf_wrong_develop.txt bash $L --check
arm lsReal 0 'all guards pass' env G78_LS=$X/lsL_real.txt bash $L --check
arm lsHeadMoved 6 'a verdict is valid ONLY at its head' env G78_LS=$X/lsL_headmoved.txt bash $L --check
arm lsBranchMoved 6 'a verdict is valid ONLY at its head' env G78_LS=$X/lsL_branchmoved.txt bash $L --check
arm lsDevMoved 17 'origin develop' env G78_LS=$X/lsL_devmoved.txt bash $L --check
arm movedKit 2 'MOVED KIT' bash $X/launch_moved_copy.sh --check
arm launchNonTTY 21 'stdin is not a TTY' env G78_LS=$X/lsL_real.txt bash $L
echo "LAUNCHER ARMS: $NM MATCH, $NX MISMATCH"
