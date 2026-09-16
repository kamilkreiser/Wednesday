#!/bin/zsh
# check_launcher.sh — runs the #1011 ROUND 2 launcher with --check ONLY (never a launch), rc printed on its own line.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks871_1011r2.sh
echo "check start $(date '+%Y-%m-%d %H:%M:%S %Z') launcher sha256 $(shasum -a 256 "$L" | cut -c1-16)"
"$L" --check < /dev/null
rc=$?
echo "check end $(date '+%H:%M:%S %Z')"
echo "launcher --check rc=$rc"
