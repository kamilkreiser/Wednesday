#!/bin/bash
# QA-POLICY-B: re-run of the plant baseline (base at a fifth) once, because the first run's 10 rows differ from the
# same inputs in the main base run (fixture disturbed); then the head and the nine plants re-compared (Python only).
W=/private/tmp/claude-501/qpb; S=0x9b17c4ec0001
until [ "$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh | tr -dc 0-9)" -lt 3 ] 2>/dev/null; do echo "heavy FULL $(date +%T)"; sleep 120; done
echo "fix before: $(ls -la $W/fix | tr '\n' ' ')"
bash $W/h/run_diff.sh base2 $S $W/out/fifth_base2.jsonl 1 QPB_FRAC=5
echo "fix after: $(ls -la $W/fix | tr '\n' ' ')"; find $W/fix -maxdepth 3 | sort | head -60
for P in head P1 P2 P3 P4 P5 P6 L1 L2 L3; do
  f=$W/out/fifth_$P.jsonl; [ $P = head ] && f=$W/out/fifth_head.jsonl
  python3 -B -I $W/h/cmp_qpb.py $W/out/fifth_base2.jsonl $f plant2-$P > $W/out/cmp2_plant_$P.txt; echo "cmp2 $P rc $?"
done
echo "== RERUN END $(date +%T)"
