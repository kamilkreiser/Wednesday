#!/bin/bash
# QA-POLICY-B item 5: timing (interleaved base/head per row, smallest of five per process, the smaller of two runs),
# debug and release, three lists; A/A controls; the 70 ms spin control; the million-word row.
W=/private/tmp/claude-501/qpb
waitc() { until [ "$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh | tr -dc 0-9)" -lt 3 ] 2>/dev/null; do echo "heavy FULL $(date +%T)"; sleep 120; done; }
ex() { ls -t $W/tt_$1/$2/$2/build/coagent-policy/*/out/zz_qpb-* | head -1; }
EB=$(ex base debug); EH=$(ex head debug); ET=$(ex mu_T70 debug); RB=$(ex base release); RH=$(ex head release)
echo "== timing $(date +%T) exes $EB $EH $ET $RB $RH"; waitc
python3 -B $W/h/time_drive.py $EB $EH $W/rows/rows_time.jsonl $W/out/time_debug.tsv def,env,long debug-bh
python3 -B $W/h/time_drive.py $EB $EB $W/rows/rows_time.jsonl $W/out/time_debug_aa.tsv def debug-aa
python3 -B $W/h/time_drive.py $EB $ET $W/rows/rows_time.jsonl $W/out/time_debug_t70.tsv def debug-t70 0:120
python3 -B $W/h/time_drive.py $EB $EH $W/rows/rows_time_million.jsonl $W/out/time_debug_million.tsv def debug-million
waitc
python3 -B $W/h/time_drive.py $RB $RH $W/rows/rows_time.jsonl $W/out/time_release.tsv def,env,long release-bh
python3 -B $W/h/time_drive.py $RB $RB $W/rows/rows_time.jsonl $W/out/time_release_aa.tsv def release-aa
python3 -B $W/h/time_drive.py $RB $RH $W/rows/rows_time_million.jsonl $W/out/time_release_million.tsv def release-million
echo "== TIME END $(date +%T)"
