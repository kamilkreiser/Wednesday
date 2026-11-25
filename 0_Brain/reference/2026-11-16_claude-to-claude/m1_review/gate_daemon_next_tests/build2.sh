#!/bin/bash
W=/private/tmp/claude-501/qdnx
wait_counter(){ while :; do n=$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh 2>/dev/null); rc=$?; echo "$(date +%H:%M:%S) counter=$n rc=$rc"; if [ $rc -eq 0 ] && [ -n "$n" ] && [ "$n" -lt 3 ]; then return; fi; sleep 180; done; }
wait_counter
echo "head build start $(date +%T)"; bash $W/r.sh $W/c $W/t cargo build --workspace --bins --locked >$W/build_head.log 2>&1; echo "head build exit $? $(date +%T)"
wait_counter
echo "base build start $(date +%T)"; bash $W/r.sh $W/b $W/tb cargo build --workspace --bins --locked >$W/build_base.log 2>&1; echo "base build exit $? $(date +%T)"
