#!/bin/bash
# usage: build.sh <spec.py> <mk module: mk21ti|mk21|mk21t> ; GEN_BRIEFS set to the real briefs dir
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator21
export GEN_BRIEFS=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/
python3 -I $R/$2.py $1
