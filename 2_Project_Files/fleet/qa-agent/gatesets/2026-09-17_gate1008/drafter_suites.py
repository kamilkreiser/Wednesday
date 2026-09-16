#!/usr/bin/env python3
"""drafter_suites.py — whole api-gateway suite at base 93629700c and head dd7086d5a (+ packages/shared at head), in the drafter's --shared clone."""
import sys; sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008')
from drafterlib import *
P('drafter_suites', ts())
for t in ('base', 'head'): P('porcelain', t, len(porcelain(t)))
vitest('gw_suite_base', 'base', 'gw'); vitest('gw_suite_head', 'head', 'gw'); vitest('shared_suite_head', 'head', 'shared')
for t in ('base', 'head'): P('porcelain', t, len(porcelain(t)))
P('end', ts())
