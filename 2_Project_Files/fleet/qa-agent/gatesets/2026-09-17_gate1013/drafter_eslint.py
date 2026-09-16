#!/usr/bin/env python3
"""drafter_eslint.py — eslint on the three touched files, base (2 existing) and head, cwd <tree>/Blockchain/Dev, JSON counts."""
import sys, subprocess, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1013')
from drafterlib import *
F = ['services/auth/src/repositories/userRepo.ts', 'services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts', 'services/auth/src/__tests__/ks999-getuserbyid-awaits-fromrow.test.ts']
P('drafter_eslint', ts())
for tree in ('base', 'head'):
    files = [f for f in F if os.path.exists(T[tree] + '/Blockchain/Dev/' + f)] if False else [f for f in F if __import__('os').path.exists(T[tree] + '/Blockchain/Dev/' + f)]
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/eslint', '-f', 'json', *files], cwd=T[tree] + '/Blockchain/Dev', capture_output=True, text=True)
    try:
        for r in json.loads(p.stdout): P('  ', tree, r['filePath'].split('/src/')[-1], 'errors', r['errorCount'], 'warnings', r['warningCount'], sorted({m.get('ruleId') for m in r['messages']}, key=str))
    except Exception as e: P('  ', tree, 'rc', p.returncode, 'unparsed', p.stderr[-500:])
P('end', ts())
