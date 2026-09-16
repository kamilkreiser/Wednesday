#!/usr/bin/env python3
"""drafter_merged_runs.py — #1012 drafter on the MERGED tree (head + develop 1125607e9): project tsc rc + WHOLE api-gateway suite. The two probes run via drafter_probe_generic.py."""
import sys, subprocess
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1012')
from drafterlib import *
P('drafter_merged_runs', ts())
p = subprocess.run([T['merged'] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', 'services/api-gateway'], cwd=T['merged'] + '/Blockchain/Dev', capture_output=True, text=True)
P('project tsc merged rc', p.returncode, (p.stdout + p.stderr).strip()[:300])
vitest('gw_suite_merged', 'merged', 'gw')
P('end', ts())
