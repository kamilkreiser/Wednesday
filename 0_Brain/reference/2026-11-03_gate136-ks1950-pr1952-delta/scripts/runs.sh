#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate136-ks1950-pr1952-delta
R=$G/repo
bash $G/scripts/jt.sh $G/logs/head_whole.log --json --outputFile=$G/logs/head_whole.json; echo "head whole rc=$?"
bash $G/scripts/swap.sh r1
bash $G/scripts/jt.sh $G/logs/r1prod_whole.log --json --outputFile=$G/logs/r1prod_whole.json; echo "r1 product + head tests whole rc=$?"
bash $G/scripts/swap.sh base
bash $G/scripts/jt.sh $G/logs/baseprod_changed.log --json --outputFile=$G/logs/baseprod_changed.json "ks1950-an-admin|ks1940-failed|ks1942-register"; echo "base product + head tests (3 changed files) rc=$?"
bash $G/scripts/swap.sh head
git -C $R status --short; echo "(status above; empty = clean)"
