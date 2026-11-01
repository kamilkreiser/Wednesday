#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator47/gen
for k in p1 p2 p3 p4 p5; do bash $G/stage47.sh $k control 3; done
echo CTLDONE >> /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator47/stages.log
