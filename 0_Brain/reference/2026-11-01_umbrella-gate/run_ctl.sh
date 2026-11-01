#!/bin/bash
# run_ctl.sh <label> <ticket> <brief_dir|-> <extra PR urls|-> <real|stub>  -> writes <label>.txt, prints rc
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_umbrella-gate
D=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night
label=$1; tk=$2; bd=$3; urls=$4; mode=$5
args=""; if [ "$bd" != "-" ]; then
  args="brief_dir=$bd $(/usr/bin/grep -v '^#' $D/briefs/$bd/spark.pins | /usr/bin/grep -v '^tier=' | sed 's/^\([a-z_]*\)=\(.*\)$/\1=\2/' | tr '\n' '\001')"
fi
pins=(); if [ "$bd" != "-" ]; then pins=("brief_dir=$bd"); while IFS= read -r l; do case "$l" in \#*|tier=*|"") ;; *) pins+=("$l");; esac; done < $D/briefs/$bd/spark.pins; fi
pins+=($6)
env_extra=(); [ "$urls" != "-" ] && env_extra+=("NIGHT_TEST_EXTRA_PR_URLS=$urls")
[ "$mode" = "stub" ] && env_extra+=("NIGHT_GITHUB_API=http://127.0.0.1:18765" "PATH=$R/shim:$PATH")
[ "$mode" = "realshim" ] && env_extra+=("PATH=$R/shim:$PATH")
{ echo "# $label: ticket=$tk pins=${pins[*]} env=${env_extra[*]}"; env "${env_extra[@]}" bash $D/build_input.sh $tk /private/tmp/claude-501/$label.json "${pins[@]}"; echo "RC=$?"; } > $R/$label.txt 2>&1
tail -1 $R/$label.txt
