#!/usr/bin/env python3
"""drafter_merged2_1032.py — develop moved again bb848b828 -> 27e53ec3a (#1029, api-gateway test) at 22:47. In the drafter CLONE only (object present in the shared
store; nothing fetched): merge-tree --write-tree head x 27e53ec3a, conflicts, services/auth/src + packages/shared subtree equality merged = head."""
import json, subprocess, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1032'
C = json.load(open(GS + '/out/drafter_paths.json'))['C']
H = '70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039'; ND = '27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d'
def g(*a): p = subprocess.run(['git', '-C', C] + list(a), capture_output=True, text=True); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('drafter_merged2_1032', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| object', g('cat-file', '-t', ND)[1], '| parent', g('rev-parse', ND + '^')[1][:9])
rc, o, e = g('merge-tree', '--write-tree', '--name-only', H, ND); MT = o.split('\n')[0]
print('merge-tree head x 27e53ec3a rc', rc, 'MERGED TREE', MT, '| conflicts', o.split('\n')[1:][:4], e[:200])
for sub in ('Blockchain/Dev/services/auth/src', 'Blockchain/Dev/packages/shared'):
    print('subtree', sub, 'head', g('rev-parse', H + ':' + sub)[1][:9], 'merged', g('rev-parse', MT + ':' + sub)[1][:9], 'equal', g('rev-parse', H + ':' + sub)[1] == g('rev-parse', MT + ':' + sub)[1])
print('merged vs head files', len(g('diff', '--name-only', H + '^{tree}', MT)[1].split()), '= 0a2b1603f..27e53ec3a files', len(g('diff', '--name-only', '0a2b1603fe52f0f3b8152588af78bbeab0237be7', ND)[1].split()))
