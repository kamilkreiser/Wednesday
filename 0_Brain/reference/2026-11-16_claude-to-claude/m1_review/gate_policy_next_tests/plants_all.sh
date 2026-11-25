#!/bin/bash
# QA-POLICY-NEXT: every plant in sequence (each a short run of one target), summary to qpx/pl/plants_summary.log
W=/private/tmp/claude-501/qpx; mkdir -p $W/pl
for p in p1a p1b p2 p3 p5 pT26a pT26b p4c p4s p4i; do echo "--- $p $(date +%T)"; bash $W/h/plants.sh $p; done > $W/pl/plants_summary.log 2>&1
echo "ALL DONE $(date +%T)" >> $W/pl/plants_summary.log
