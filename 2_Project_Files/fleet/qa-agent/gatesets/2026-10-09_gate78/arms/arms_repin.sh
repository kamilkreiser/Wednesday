#!/bin/bash
# gate78 repin arms. Every arm is a --dry-run (or refuses before any launch step). Each arm is matched on rc AND its own asserting line.
# Output: $G/arms/repin_<arm>.{out,rc}; the summary prints MATCH / MISMATCH per arm.
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate78; A=$G/arms; X=$G/_scratch/arms; mkdir -p $A $X
R=$G/repin_and_launch_gate78.sh
H=6f4adfe8835ec8ece51653f3f758d6a55ce12348; BR=feature/ks-1452-handlebars-lock-refresh-v1-1; B=1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0; T=ccbb76460ad630ab9fdb74b31dfc16502eee94ac
read SIM_OK SIM_TOOL < $X/sims.txt
OK=(--pr 1435 --head $H --branch $BR --base $B --parents-n 1 --end-tree $T --develop $B --dry-run --no-api)
NM=0; NX=0
arm() { local name=$1 want=$2 pat=$3; shift 3; "$@" > $A/repin_$name.out 2>&1 < /dev/null; echo $? > $A/repin_$name.rc
  local got; got=$(cat $A/repin_$name.rc); local line; line=$(grep -m1 -E -- "$pat" $A/repin_$name.out | cut -c1-140)
  if [ "$got" = "$want" ] && [ -n "$line" ]; then v=MATCH; NM=$((NM+1)); else v=MISMATCH; NX=$((NX+1)); fi
  printf '%-8s %-30s rc %s (want %s) | %s\n' "$v" "$name" "$got" "$want" "${line:-<asserting line ABSENT: $pat>}"; }
sub() { local k=$1 v=$2; local out=(); local i=0; local a=("${OK[@]}"); while [ $i -lt ${#a[@]} ]; do if [ "${a[$i]}" = "$k" ]; then out+=("$k" "$v"); i=$((i+2)); else out+=("${a[$i]}"); i=$((i+1)); fi; done; printf '%s\n' "${out[@]}"; }
drop() { local k=$1; local out=(); local i=0; local a=("${OK[@]}"); while [ $i -lt ${#a[@]} ]; do if [ "${a[$i]}" = "$k" ]; then i=$((i+2)); else out+=("${a[$i]}"); i=$((i+1)); fi; done; printf '%s\n' "${out[@]}"; }
for k in --pr --head --branch --base --parents-n --end-tree --develop; do arm "missing$k" 9 'REFUSING: a REQUIRED argument is missing' bash $R $(drop $k); done
arm wrong--pr 11 'WRONG VALUE --pr' bash $R $(sub --pr 1406)
arm wrong--head 11 'WRONG VALUE --head' bash $R $(sub --head 4a400d7aa9dd273d91fb62375cb4b0598aa4405f)
arm wrong--branch 11 'WRONG VALUE --branch' bash $R $(sub --branch feature/ks-1437-advisory-lock-refresh-g3-1)
arm wrong--base 11 'WRONG VALUE --base' bash $R $(sub --base b39051390ff6f252601d6f7b45f0ea6c21c31023)
arm wrong--parents-n 11 'WRONG VALUE --parents-n' bash $R $(sub --parents-n 2)
arm wrong--end-tree 11 'WRONG VALUE --end-tree' bash $R $(sub --end-tree 85820a21f80c02d542ca1cf62e194750f2779c28)
arm wrong--develop 11 'WRONG VALUE --develop' bash $R $(sub --develop b39051390ff6f252601d6f7b45f0ea6c21c31023)
arm short--head 9 'must be the FULL 40-hex' bash $R $(sub --head 6f4adfe8835e)
arm noapi-real-launch 9 'dry-run option only' bash $R $(printf '%s\n' "${OK[@]}" | grep -v -- '--dry-run')
arm stale-repin-develop 10 'stale re-pin' bash $R "${OK[@]}" --repin-develop 4a400d7aa9dd273d91fb62375cb4b0598aa4405f
ls_() { printf '%s\trefs/heads/develop\n%s\trefs/pull/1435/head\n%s\trefs/heads/%s\n' "$1" "$2" "$3" $BR > $X/$4; }
ls_ $B $B $H ls_headmoved.txt; ls_ $B $H $B ls_branchmoved.txt
ls_ b39051390ff6f252601d6f7b45f0ea6c21c31023 $H $H ls_dev_not_descendant.txt
ls_ $SIM_TOOL $H $H ls_dev_touches_tooling.txt; ls_ $SIM_OK $H $H ls_dev_sim_ok.txt; ls_ $H $H $H ls_dev_is_head.txt
arm lsfile-headmoved 11 'MISMATCH' env G78_LSFILE=$X/ls_headmoved.txt bash $R "${OK[@]}"
arm lsfile-branchmoved 11 'MISMATCH' env G78_LSFILE=$X/ls_branchmoved.txt bash $R "${OK[@]}"
arm lsfile-dev-not-descendant 13 'C1 FAILED' env G78_LSFILE=$X/ls_dev_not_descendant.txt bash $R "${OK[@]}"
arm lsfile-dev-touches-tooling 13 'C1 FAILED' env G78_LSFILE=$X/ls_dev_touches_tooling.txt bash $R "${OK[@]}"
arm lsfile-dev-is-the-head 13 'C1 FAILED' env G78_LSFILE=$X/ls_dev_is_head.txt bash $R "${OK[@]}"
arm lsfile-dev-sim-clean-no-repin 10 're-run with:  --repin-develop' env G78_LSFILE=$X/ls_dev_sim_ok.txt bash $R "${OK[@]}"
arm lsfile-dev-sim-clean-stale-repin 10 'stale re-pin' env G78_LSFILE=$X/ls_dev_sim_ok.txt bash $R "${OK[@]}" --repin-develop $SIM_TOOL
arm lsfile-dev-sim-clean-repinned 0 'DRY RUN COMPLETE' env G78_LSFILE=$X/ls_dev_sim_ok.txt bash $R "${OK[@]}" --repin-develop $SIM_OK
arm lsfile-in-real-launch 16 'G78_LSFILE is a dry-run control only' env G78_LSFILE=$X/ls_dev_sim_ok.txt bash $R $(printf '%s\n' "${OK[@]}" | grep -v -E -- '^--(dry-run|no-api)$')
echo "REPIN ARMS: $NM MATCH, $NX MISMATCH"
