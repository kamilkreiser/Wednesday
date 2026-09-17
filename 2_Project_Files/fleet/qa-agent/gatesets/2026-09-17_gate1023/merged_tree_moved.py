#!/usr/bin/env python3
"""merged_tree_moved.py — in the drafter's OWN clone only: merge-tree --write-tree 2f74491eb x 81ee4b729 (develop after #1021 merged, seen 18:30), plus the controls
that the PR files and the api-gateway / shared trees are unchanged by the move."""
import json, os, subprocess, datetime
GS = os.path.dirname(os.path.abspath(__file__)); C = json.load(open(GS + '/drafter_paths.json'))['C']
def run(*a): p = subprocess.run(['git', '-C', C, *a], capture_output=True, text=True); return p.returncode, p.stdout.strip(), p.stderr.strip()[:200]
print('read at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'), '| clone', C)
print('81ee4b729 in clone (via --shared alternates):', run('cat-file', '-t', '81ee4b729e86a645fc9098aafa1aaf39035a9950'))
print('merge-tree head x 81ee4b729:', run('merge-tree', '--write-tree', '--name-only', '2f74491ebd6211e722f778838339c55e8add008d', '81ee4b729e86a645fc9098aafa1aaf39035a9950'))
for t in ('581c9db0d', '81ee4b729', '2f74491eb'):
    print(t, 'api-gateway tree / shared tree:', run('rev-parse', t + ':Blockchain/Dev/services/api-gateway', t + ':Blockchain/Dev/packages/shared')[1].split())
