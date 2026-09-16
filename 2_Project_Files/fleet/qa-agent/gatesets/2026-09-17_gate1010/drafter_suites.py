#!/usr/bin/env python3
"""drafter_suites.py — #1010 drafter: WHOLE api-gateway suite on base / head / merged in the --shared clone (JSON reporter, serial per tree)."""
import sys; sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1010')
from drafterlib import *
P('drafter_suites', ts())
for t in ('base', 'head', 'merged'):
    vitest('gw_suite_' + t, t, 'gw')
P('end', ts())
