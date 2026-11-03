#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator95
S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark
git clone --no-hardlinks -q --no-checkout $S/cache/src $O/repo
git --git-dir=$O/repo/.git --work-tree=$O/repo checkout -q 27fe5476526c4200b752449e04be689724289e6d && echo checked-out
git --git-dir=$O/repo/.git log -1 --format=%H
