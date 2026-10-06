#!/bin/bash
# repin wrong-value / missing / live-mismatch arms. Every arm is a --dry-run. Output: $G/arms/repin_<arm>.{out,rc}
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-07_gate72; A=$G/arms; mkdir -p $A $G/_scratch/arms
R=$G/repin_and_launch_gate72.sh
H=4a400d7aa9dd273d91fb62375cb4b0598aa4405f; BR=feature/ks-1437-advisory-lock-refresh-g3-1; B=b39051390ff6f252601d6f7b45f0ea6c21c31023; T=85820a21f80c02d542ca1cf62e194750f2779c28
OK=(--pr 1406 --head $H --branch $BR --base $B --parents-n 1 --end-tree $T --develop $B --dry-run --no-api)
arm() { name=$1; shift; "$@" > $A/repin_$name.out 2>&1 < /dev/null; echo $? > $A/repin_$name.rc; printf '%-26s rc %s | %s\n' "$name" "$(cat $A/repin_$name.rc)" "$(grep -m1 -E 'REFUSING|DRY RUN COMPLETE' $A/repin_$name.out | cut -c1-150)"; }
sub() { local k=$1 v=$2; local out=(); local i=0; local a=("${OK[@]}"); while [ $i -lt ${#a[@]} ]; do if [ "${a[$i]}" = "$k" ]; then out+=("$k" "$v"); i=$((i+2)); else out+=("${a[$i]}"); i=$((i+1)); fi; done; printf '%s\n' "${out[@]}"; }
drop() { local k=$1; local out=(); local i=0; local a=("${OK[@]}"); while [ $i -lt ${#a[@]} ]; do if [ "${a[$i]}" = "$k" ]; then i=$((i+2)); else out+=("${a[$i]}"); i=$((i+1)); fi; done; printf '%s\n' "${out[@]}"; }
for k in --pr --head --branch --base --parents-n --end-tree --develop; do arm "missing$k" bash $R $(drop $k); done
arm wrong--pr bash $R $(sub --pr 1397)
arm wrong--head bash $R $(sub --head 3e7be2044fe80ebced9c497bfc278a7333018a83)
arm wrong--branch bash $R $(sub --branch feature/ks-1425-advisory-lock-refresh-d10-1)
arm wrong--base bash $R $(sub --base 4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe)
arm wrong--parents-n bash $R $(sub --parents-n 2)
arm wrong--end-tree bash $R $(sub --end-tree 0b06d3c18a1e116cb5c550a505e2cb8884315f63)
arm wrong--develop bash $R $(sub --develop 4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe)
arm short--head bash $R $(sub --head 4a400d7aa9dd)
arm noapi-real-launch bash $R $(printf '%s\n' "${OK[@]}" | grep -v -- '--dry-run')
arm stale-repin-develop bash $R "${OK[@]}" --repin-develop 3e7be2044fe80ebced9c497bfc278a7333018a83
printf '%s\trefs/heads/develop\n%s\trefs/pull/1406/head\n%s\trefs/heads/%s\n' $B $B $H $BR > $G/_scratch/arms/ls_headmoved.txt
printf '%s\trefs/heads/develop\n%s\trefs/pull/1406/head\n%s\trefs/heads/%s\n' $B $H $B $BR > $G/_scratch/arms/ls_branchmoved.txt
printf '%s\trefs/heads/develop\n%s\trefs/pull/1406/head\n%s\trefs/heads/%s\n' 3e7be2044fe80ebced9c497bfc278a7333018a83 $H $H $BR > $G/_scratch/arms/ls_dev_not_descendant.txt
printf '%s\trefs/heads/develop\n%s\trefs/pull/1406/head\n%s\trefs/heads/%s\n' $H $H $H $BR > $G/_scratch/arms/ls_dev_touches_paths.txt
arm lsfile-headmoved env G72_LSFILE=$G/_scratch/arms/ls_headmoved.txt bash $R "${OK[@]}"
arm lsfile-branchmoved env G72_LSFILE=$G/_scratch/arms/ls_branchmoved.txt bash $R "${OK[@]}"
arm lsfile-dev-not-descendant env G72_LSFILE=$G/_scratch/arms/ls_dev_not_descendant.txt bash $R "${OK[@]}"
arm lsfile-dev-touches-5-paths env G72_LSFILE=$G/_scratch/arms/ls_dev_touches_paths.txt bash $R "${OK[@]}"
