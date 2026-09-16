#!/usr/bin/env python3
"""drafter_apply_numstat.py - `git apply --numstat` (reads the patch, writes nothing) in the drafter clone's BASE worktree on the READY split per file, with and
without --recount: what line count a no-recount apply of the +1,132 header would take. Never rm; stderr kept."""
import subprocess, json, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1016'
PATHS = json.load(open(GS + '/drafter_paths.json')); T = PATHS['trees']; W = PATHS['W']
print('apply_numstat', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for label in ('split-test-file', 'split-product-file'):
    for extra in ([], ['--recount']):
        p = subprocess.run(['git', '-C', T['base'], 'apply', '--numstat', *extra, '--directory=Blockchain/Dev', W + '/ready_ks1072.%s.patch' % label], capture_output=True, text=True)
        print('---', label, extra, 'rc', p.returncode, '|', (p.stdout + p.stderr).strip())
lines = open(W + '/ready_ks1072.split-test-file.patch').read().splitlines()
print('split-test-file patch lines', len(lines), '| + lines', sum(1 for l in lines if l.startswith('+') and not l.startswith('+++')), '| header', [l for l in lines if l.startswith('@@')])
