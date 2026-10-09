#!/bin/bash
# gate79 repin arms (carried from gate78's). Every arm is a --dry-run or refuses before any launch step. Matched on rc AND its own line.
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate79; A=$G/arms; X=$G/_scratch/arms; mkdir -p $A $X
R=$G/repin_and_launch_gate79.sh
H=b4933a457f38fe12551839545431bba000e928fc; BR=feature/ks-1402-originate-resolves-holder-email-itself-k2-1; B=81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6; T=64d5bf0c31a371a968ec13474f3cdaf6b42541e9; D=349b35c9163ac59209366adb7a4a89d8779bd6d6
G78H=6f4adfe8835ec8ece51653f3f758d6a55ce12348; G78B=1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0; G78T=ccbb76460ad630ab9fdb74b31dfc16502eee94ac
read SIM_OK SIM_ROUTE SIM_AUTH < $X/sims.txt
OK=(--pr 1437 --head $H --branch $BR --base $B --parents-n 1 --end-tree $T --develop $D --dry-run --no-api)
NM=0; NX=0
arm() { local name=$1 want=$2 pat=$3; shift 3; "$@" > $A/repin_$name.out 2>&1 < /dev/null; echo $? > $A/repin_$name.rc
  local got; got=$(cat $A/repin_$name.rc); local line; line=$(grep -m1 -E -- "$pat" $A/repin_$name.out | cut -c1-140)
  if [ "$got" = "$want" ] && [ -n "$line" ]; then v=MATCH; NM=$((NM+1)); else v=MISMATCH; NX=$((NX+1)); fi
  printf '%-8s %-34s rc %s (want %s) | %s\n' "$v" "$name" "$got" "$want" "${line:-<asserting line ABSENT: $pat>}"; }
sub() { local k=$1 v=$2; local out=(); local i=0; local a=("${OK[@]}"); while [ $i -lt ${#a[@]} ]; do if [ "${a[$i]}" = "$k" ]; then out+=("$k" "$v"); i=$((i+2)); else out+=("${a[$i]}"); i=$((i+1)); fi; done; printf '%s\n' "${out[@]}"; }
drop() { local k=$1; local out=(); local i=0; local a=("${OK[@]}"); while [ $i -lt ${#a[@]} ]; do if [ "${a[$i]}" = "$k" ]; then i=$((i+2)); else out+=("${a[$i]}"); i=$((i+1)); fi; done; printf '%s\n' "${out[@]}"; }
for k in --pr --head --branch --base --parents-n --end-tree --develop; do arm "missing$k" 9 'REFUSING: a REQUIRED argument is missing' bash $R $(drop $k); done
arm wrong--pr 11 'WRONG VALUE --pr' bash $R $(sub --pr 1435)
arm wrong--head 11 'WRONG VALUE --head' bash $R $(sub --head $G78H)
arm wrong--branch 11 'WRONG VALUE --branch' bash $R $(sub --branch feature/ks-1452-handlebars-lock-refresh-v1-1)
arm wrong--base 11 'WRONG VALUE --base' bash $R $(sub --base $G78B)
arm wrong--parents-n 11 'WRONG VALUE --parents-n' bash $R $(sub --parents-n 2)
arm wrong--end-tree 11 'WRONG VALUE --end-tree' bash $R $(sub --end-tree $G78T)
arm wrong--develop 11 'WRONG VALUE --develop' bash $R $(sub --develop $B)
arm short--head 9 'must be the FULL 40-hex' bash $R $(sub --head b4933a457f38)
arm noapi-real-launch 9 'dry-run option only' bash $R $(printf '%s\n' "${OK[@]}" | grep -v -- '--dry-run')
arm stale-repin-develop 10 'stale re-pin' bash $R "${OK[@]}" --repin-develop $G78B
ls_() { printf '%s\trefs/heads/develop\n%s\trefs/pull/1437/head\n%s\trefs/heads/%s\n' "$1" "$2" "$3" $BR > $X/$4; }
ls_ $D $B $H ls_headmoved.txt; ls_ $D $H $B ls_branchmoved.txt; ls_ $D $SIM_OK $SIM_OK ls_head_moved_both.txt
ls_ $G78B $H $H ls_dev_not_descendant.txt
ls_ $SIM_ROUTE $H $H ls_dev_touches_route.txt; ls_ $SIM_AUTH $H $H ls_dev_touches_auth.txt; ls_ $SIM_OK $H $H ls_dev_sim_ok.txt
arm lsfile-headmoved 11 'MISMATCH' env G79_LSFILE=$X/ls_headmoved.txt bash $R "${OK[@]}"
arm lsfile-branchmoved 11 'MISMATCH' env G79_LSFILE=$X/ls_branchmoved.txt bash $R "${OK[@]}"
arm lsfile-head-AND-branch-moved 11 'MISMATCH' env G79_LSFILE=$X/ls_head_moved_both.txt bash $R "${OK[@]}"
arm lsfile-dev-not-descendant 13 'C1 FAILED' env G79_LSFILE=$X/ls_dev_not_descendant.txt bash $R "${OK[@]}"
arm lsfile-dev-touches-documents.ts 13 'C1 FAILED' env G79_LSFILE=$X/ls_dev_touches_route.txt bash $R "${OK[@]}"
arm lsfile-dev-touches-auth 13 'C1 FAILED' env G79_LSFILE=$X/ls_dev_touches_auth.txt bash $R "${OK[@]}"
arm lsfile-dev-sim-clean-no-repin 10 're-run with:  --repin-develop' env G79_LSFILE=$X/ls_dev_sim_ok.txt bash $R "${OK[@]}"
arm lsfile-dev-sim-clean-stale-repin 10 'stale re-pin' env G79_LSFILE=$X/ls_dev_sim_ok.txt bash $R "${OK[@]}" --repin-develop $SIM_ROUTE
arm lsfile-dev-sim-clean-repinned 0 'DRY RUN COMPLETE' env G79_LSFILE=$X/ls_dev_sim_ok.txt bash $R "${OK[@]}" --repin-develop $SIM_OK
arm lsfile-in-real-launch 16 'G79_LSFILE is a dry-run control only' env G79_LSFILE=$X/ls_dev_sim_ok.txt bash $R $(printf '%s\n' "${OK[@]}" | grep -v -E -- '^--(dry-run|no-api)$')
echo "REPIN ARMS: $NM MATCH, $NX MISMATCH"
