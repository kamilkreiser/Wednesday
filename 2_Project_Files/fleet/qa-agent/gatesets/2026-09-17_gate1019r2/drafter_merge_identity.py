#!/usr/bin/env python3
"""drafter_merge_identity.py — Q5 in the drafter clone (read verbs only): at 82f09c8bd, the PR's files byte-identical to 4d551f104 and develop's files byte-identical
to f8c7aaa39, by name lists AND per-file blob; the merge's parents; merge-tree re-prediction (drafter_setup.out) restated; CONTROL: the same comparison against a
commit that differs (8b8996f8b) must report a mismatch."""
import json, subprocess, os, datetime
GSD = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GSD + '/drafter_paths.json')); C = PA['C']; S = PA['sha']
g = lambda *a: subprocess.run(['git', '-C', C] + list(a), capture_output=True, text=True).stdout.strip()
print('merge identity', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print('head parents', g('rev-list', '--parents', '-n', '1', S['head']))
pr = g('diff', '--name-only', '--no-renames', S['dev'], S['head']).splitlines(); dv = g('diff', '--name-only', '--no-renames', S['r2'], S['head']).splitlines()
print('diff develop..head files', len(pr), pr); print('diff r2..head files', len(dv), dv)
print('overlap', sorted(set(pr) & set(dv)))
def blobs(files, a, b):
    out = []
    for f in files:
        x = g('rev-parse', a + ':' + f); y = g('rev-parse', b + ':' + f); out.append((f.split('/')[-1], x[:9], y[:9], x == y))
    return out
for row in blobs(pr, S['r2'], S['head']): print('  PR file r2 vs head', row)
for row in blobs(dv, S['dev'], S['head']): print('  develop file dev vs head', row)
ctl = blobs(pr, S['r1'], S['head']); print('  CONTROL PR files r1 vs head (must show a mismatch)', ctl, '-> fired:', not all(r[3] for r in ctl))
print('trees: head', g('rev-parse', S['head'] + '^{tree}'), '| merge-tree r2 x dev (setup)', PA['merge_tree']['r2xdev'], '| develop is ancestor of head rc', subprocess.run(['git', '-C', C, 'merge-base', '--is-ancestor', S['dev'], S['head']]).returncode)
