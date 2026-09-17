#!/usr/bin/env python3
"""drafter_merged_moved.py <develop sha> — merge-tree --write-tree head x <develop> IN THE DRAFTER CLONE (never the checkout); assert the merged api-gateway and
shared subtrees equal the head's; list develop's delta since the merge-base under services/api-gateway or packages/shared (control: the whole delta listed)."""
import subprocess, json, os, sys, datetime
GS = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GS + '/drafter_paths.json')); C = PA['C']
H = 'e39521cfb54cb5fd47c6bdae64ce707b3c9befce'; MB = '19f1e54750ce2b65312a687add2db4f5628edb7d'; DV = sys.argv[1]
def run(*a): p = subprocess.run(['git', '-C', C] + list(a), capture_output=True, text=True); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('drafter_merged_moved', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), 'develop', DV)
print('object type in clone', run('cat-file', '-t', DV))
rc, o, e = run('merge-tree', '--write-tree', '--name-only', H, DV); t = o.split('\n')[0]; print('merge-tree head x develop rc', rc, 'tree', t, 'conflict-name lines', len(o.split('\n')) - 1, e[:200])
for sub in ('Blockchain/Dev/services/api-gateway', 'Blockchain/Dev/packages/shared'):
    a = run('rev-parse', t + ':' + sub)[1]; b = run('rev-parse', H + ':' + sub)[1]; print('  subtree', sub.split('/')[-1], 'merged', a[:9], 'head', b[:9], 'EQUAL' if a == b else 'DIFFERENT')
rc, o, e = run('diff', '--name-only', MB, DV); allf = o.split('\n') if o else []
print('develop delta since merge-base: files', len(allf), '| under api-gateway/shared:', [f for f in allf if '/services/api-gateway/' in f or '/packages/shared/' in f])
