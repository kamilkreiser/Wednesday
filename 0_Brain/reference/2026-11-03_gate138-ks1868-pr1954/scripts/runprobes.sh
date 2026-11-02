#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate138-ks1868-pr1954
bash $W/scripts/probe.sh base
bash $W/scripts/probe.sh head
RC_ON=1 SUF=_console bash $W/scripts/probe.sh base
RC_ON=1 SUF=_console bash $W/scripts/probe.sh head
echo ALLDONE
