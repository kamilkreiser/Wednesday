#!/bin/bash
# QA-POLICY-WORDS property (b): t28 in three fixture places at the head, then t27/t25/t12/t21
W=/private/tmp/claude-501/qpw; V=/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/state/qpw-tt
TT=$W/tt_head/fx_tmp $W/h/cg.sh $W/head head test -p coagent-policy --locked --offline --test t28_at_names -- --nocapture > $W/logs/b1_t28_tmp.log 2>&1
TT=$V/plain $W/h/cg.sh $W/head head test -p coagent-policy --locked --offline --test t28_at_names -- --nocapture > $W/logs/b2_t28_volplain.log 2>&1
TT=$V/Claude $W/h/cg.sh $W/head head test -p coagent-policy --locked --offline --test t28_at_names -- --nocapture > $W/logs/b2_t28_volClaude.log 2>&1
TT=$W/tt_head/fx_tmp $W/h/cg.sh $W/head head test -p coagent-policy --locked --offline --test t27_owner_dark -- --nocapture > $W/logs/b4_t27.log 2>&1
for t in t25_owner_allow t12_docs t21_bypass_refusals; do
TT=$W/tt_head/fx_tmp $W/h/cg.sh $W/head head test -p coagent-policy --locked --offline --test $t > $W/logs/b4_$t.log 2>&1
done
echo ALLDONE
