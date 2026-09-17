#!/usr/bin/env python3
"""drafter_other_1030.py — class census of every moved OTHER (non vitest/@vitest/*) entry across the 27 locks, merge-base vs head, and the root
lock's OTHER detail (which fields moved). Read-only git show in the drafter clone."""
import json, re, subprocess, collections
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1030'
P = json.load(open(G + '/drafter_paths.json')); C = P['C']; B = P['BASE']; H = P['HEAD']
def show(s, p): return json.loads(subprocess.run(['git', '-C', C, 'show', s + ':' + p], capture_output=True, text=True, check=True).stdout)
locks = [x for x in subprocess.run(['git', '-C', C, 'diff', '--name-only', B, H], capture_output=True, text=True).stdout.split() if x.endswith('package-lock.json')]
FAM = re.compile(r'(^|/)node_modules/(vitest|@vitest/[^/]+)$')
def cls(v): return 'ABSENT' if v is None else (','.join(f for f in ('dev', 'devOptional', 'optional', 'peer') if v.get(f)) or 'PROD')
tally = collections.Counter()
for p in locks:
    a, b = show(B, p)['packages'], show(H, p)['packages']
    for k in sorted(set(a) | set(b)):
        if a.get(k) == b.get(k) or FAM.search(k): continue
        c = cls(a.get(k)) + '->' + cls(b.get(k)); tally[c] += 1
        if p == 'Blockchain/Dev/package-lock.json':
            fa, fb = a.get(k) or {}, b.get(k) or {}
            print('ROOT OTHER', k, c, sorted(x for x in set(fa) | set(fb) if fa.get(x) != fb.get(x)), (fa.get('version'), fb.get('version')))
print('OTHER class transitions across 27 locks:', dict(tally))
