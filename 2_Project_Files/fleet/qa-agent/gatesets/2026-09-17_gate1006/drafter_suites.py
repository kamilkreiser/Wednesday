#!/usr/bin/env python3
"""drafter_suites.py — whole packages/shared and services/demo-service suites at base (develop 40fe4db69) and head (86fe59e6b); porcelain printed first."""
import sys; sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1006')
from drafterlib import *
P('drafter_suites start', ts())
for t in ('base', 'head'):
    P('porcelain', t, porcelain(t))
    vitest('demo_suite_' + t, t, 'demo')
    vitest('shared_suite_' + t, t, 'shared')
    P('porcelain after', t, porcelain(t))
P('drafter_suites end', ts())
