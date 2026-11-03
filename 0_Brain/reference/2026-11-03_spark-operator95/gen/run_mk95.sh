#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator95
python3 $O/gen/mk95.py "$@" > $O/mk_$1.out 2>&1; echo rc=$?; tail -15 $O/mk_$1.out | cut -c1-200
