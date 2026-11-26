#!/bin/bash
# QA-POLICY-WORDS: run the probe. usage: probe.sh <tree p184|phead> <rowset> <place tmp|plain|Claude|unset>
W=/private/tmp/claude-501/qpw; V=/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/state/qpw-tt
TREE=$1; SET=$2; PL=$3
case $PL in tmp) export TT=$W/tt_$TREE/fx_tmp;; plain) export TT=$V/plain;; Claude) export TT=$V/Claude;; unset) export TT=UNSET;; esac
export QPW_ROWS=$W/h/rows_$SET.jsonl QPW_OUT=$W/out/${TREE}_${SET}_${PL}.jsonl
mkdir -p $W/out
$W/h/cg.sh $W/$TREE $TREE test -p coagent-policy --locked --offline --test zz_qpw_probe -- --nocapture > $W/logs/probe_${TREE}_${SET}_${PL}.log 2>&1
echo "rc=$? $(grep -h 'QPW-PROBE\|test result' $W/logs/probe_${TREE}_${SET}_${PL}.log | tr '\n' ' ')"
