#!/usr/bin/env python3
"""drafter_suites.py — whole api-gateway suite at base / head / merged (porcelain asserted first)."""
import sys; sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1005')
from drafterlib import *
P('drafter_suites start', ts())
for t in ('base','head','merged'):
    P('porcelain', t, porcelain(t))
    vitest('suite_'+t, t)
P('drafter_suites end', ts())
