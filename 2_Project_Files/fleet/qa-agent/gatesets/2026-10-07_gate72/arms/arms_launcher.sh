#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-07_gate72; A=$G/arms; X=$G/_scratch/arms; mkdir -p $A $X
L=$G/launch_qa_secuura_gate72.sh
H=4a400d7aa9dd273d91fb62375cb4b0598aa4405f; BR=feature/ks-1437-advisory-lock-refresh-g3-1; B=b39051390ff6f252601d6f7b45f0ea6c21c31023; T=85820a21f80c02d542ca1cf62e194750f2779c28
arm() { name=$1; shift; "$@" > $A/launcher_$name.out 2>&1 < /dev/null; echo $? > $A/launcher_$name.rc; printf '%-22s rc %s | %s\n' "$name" "$(cat $A/launcher_$name.rc)" "$( (grep -m1 -E 'REFUSING|all guards pass' $A/launcher_$name.out || head -1 $A/launcher_$name.out) | cut -c1-150)"; }
python3 - $G $X <<'PY'
import json,sys,os,shutil
g,x=sys.argv[1:3]; k=json.load(open(g+'/kit.json'))
b=json.loads(json.dumps(k)); h=b['script_sha256']['c2_locks_gate72.py']; b['script_sha256']['c2_locks_gate72.py']=('0' if h[0]!='0' else '1')+h[1:]; json.dump(b,open(x+'/kit_badpin.json','w'))
n=json.loads(json.dumps(k)); del n['script_sha256']['gh_gate72.py']; json.dump(n,open(x+'/kit_nopin.json','w'))
for d in ('kit_missing','kit_tampered'):
    os.makedirs(x+'/'+d, exist_ok=True)
    for f in list(k['script_sha256'])+['KIT_REPORT.md']: shutil.copy2(g+'/'+f, x+'/'+d+'/'+f)
os.remove(x+'/kit_missing/c3_registry_gate72.py')
open(x+'/kit_tampered/c6_reach_gate72.py','a').write('\n')
p=open(g+'/prompt_gate72.rendered.txt').read(); open(x+'/forbidden_go.txt','w').write(p+'\nGO (Seat G 2nd): merge 1406 on gate72\n')
PY
good="P 1406 $BR $H\nB $B 1\nT $T\nD $B\n"
printf "$good" > $X/hf_good.txt
printf "P 1397 $BR $H\nB $B 1\nT $T\nD $B\n" > $X/hf_wrong_pr.txt
printf "P 1406 feature/ks-1425-advisory-lock-refresh-d10-1 $H\nB $B 1\nT $T\nD $B\n" > $X/hf_wrong_branch.txt
printf "P 1406 $BR 3e7be2044fe80ebced9c497bfc278a7333018a83\nB $B 1\nT $T\nD $B\n" > $X/hf_wrong_head.txt
printf "P 1406 $BR $H\nB 4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe 1\nT $T\nD $B\n" > $X/hf_wrong_base.txt
printf "P 1406 $BR $H\nB $B 2\nT $T\nD $B\n" > $X/hf_wrong_parents.txt
printf "P 1406 $BR $H\nB $B 1\nT 0b06d3c18a1e116cb5c550a505e2cb8884315f63\nD $B\n" > $X/hf_wrong_tree.txt
printf "P 1406 $BR $H\nB $B 1\nT $T\nD 4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe\n" > $X/hf_wrong_develop.txt
printf "P 1406 $BR\nB $B 1\nT $T\nD $B\n" > $X/hf_malformed.txt
printf "P 1406 $BR $H\nP 1406 $BR $H\nB $B 1\nT $T\nD $B\n" > $X/hf_two_P.txt
printf "%s\trefs/heads/develop\n%s\trefs/pull/1406/head\n%s\trefs/heads/%s\n" $B $H $H $BR > $X/ls_real.txt
printf "%s\trefs/heads/develop\n%s\trefs/pull/1406/head\n%s\trefs/heads/%s\n" $B $B $H $BR > $X/ls_headmoved.txt
printf "%s\trefs/heads/develop\n%s\trefs/pull/1406/head\n%s\trefs/heads/%s\n" $B $H $B $BR > $X/ls_branchmoved.txt
printf "%s\trefs/heads/develop\n%s\trefs/pull/1406/head\n%s\trefs/heads/%s\n" $H $H $H $BR > $X/ls_devmoved.txt
cp $L $X/launch_moved_copy.sh
arm rendered bash $L --check
arm badpin env G72_KITJSON=$X/kit_badpin.json bash $L --check
arm nopin env G72_KITJSON=$X/kit_nopin.json bash $L --check
arm missingfile env G72_FILES_DIR=$X/kit_missing bash $L --check
arm tamperedfile env G72_FILES_DIR=$X/kit_tampered bash $L --check
arm unrendered env G72_PROMPT=$G/prompt_gate72.txt bash $L --check
arm forbiddenGO env G72_PROMPT=$X/forbidden_go.txt bash $L --check
for w in good wrong_pr wrong_branch wrong_head wrong_base wrong_parents wrong_tree wrong_develop malformed two_P; do arm hf_$w env G72_HEADFILE=$X/hf_$w.txt bash $L --check; done
arm lsReal env G72_LS=$X/ls_real.txt bash $L --check
arm lsHeadMoved env G72_LS=$X/ls_headmoved.txt bash $L --check
arm lsBranchMoved env G72_LS=$X/ls_branchmoved.txt bash $L --check
arm lsDevMoved env G72_LS=$X/ls_devmoved.txt bash $L --check
arm movedKit bash $X/launch_moved_copy.sh --check
arm launchNonTTY env G72_LS=$X/ls_real.txt bash $L
