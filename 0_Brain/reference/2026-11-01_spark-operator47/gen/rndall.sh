#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator47/gen
for k in p1 p2 p3 p4 p5; do bash $G/stage47.sh $k dry 4; bash $G/stage47.sh $k round 4; done
echo RNDDONE >> /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator47/stages.log
