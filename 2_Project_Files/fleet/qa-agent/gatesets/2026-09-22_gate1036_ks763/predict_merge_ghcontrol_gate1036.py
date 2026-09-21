#!/usr/bin/env python3
"""predict_merge_ghcontrol_gate1036.py — CONTROL for the merge instrument, in the drafter's SCRATCH CLONE only (never the checkout): merge-tree of
#1036's head over the develop GitHub itself used for refs/pull/1036/merge (its first parent) must reproduce GitHub's merge commit tree.
Usage: predict_merge_ghcontrol_gate1036.py <scratch clone> <head> <current develop>"""
import datetime, json, subprocess, sys
C, HEAD, DEV = sys.argv[1], sys.argv[2], sys.argv[3]
assert C.startswith('/private/tmp/claude-501/'), 'scratch clone only'
def sg(*a, check=True):
    p = subprocess.run(['git', '-C', C] + list(a), capture_output=True, text=True)
    if check and p.returncode != 0: raise SystemExit('%r rc %d %s' % (a[:3], p.returncode, p.stderr[-300:]))
    return p
print('at', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), '— CONTROL: my merge-tree instrument over the develop GitHub used must reproduce GitHub merge tree')
gm = sg('rev-parse', 'refs/scratch/pull1036merge').stdout.strip()
parents = sg('log', '-1', '--format=%P', gm).stdout.split(); gh_dev = [p for p in parents if p != HEAD][0]
gtree = sg('rev-parse', gm + '^{tree}').stdout.strip()
print('GitHub merge ref', gm, 'parents', parents, 'tree', gtree)
print('its develop parent', gh_dev[:9], 'is an ancestor of the current develop?', sg('merge-base', '--is-ancestor', gh_dev, DEV, check=False).returncode == 0,
      '| commits gh_dev..DEV:', sg('rev-list', '--count', gh_dev + '..' + DEV).stdout.strip())
p = sg('merge-tree', '--write-tree', gh_dev, HEAD, check=False)
t = p.stdout.split()[0] if p.stdout.split() else ''
print('$ (scratch) git merge-tree --write-tree', gh_dev[:9], HEAD[:9], '-> rc', p.returncode, 'tree', t)
print('== GitHub tree?', t == gtree)
rows = len(json.loads(sg('show', t + ':Blockchain/Dev/scripts/audit/audit-baseline.json').stdout)['accepted'])
print('merged-over-gh_dev baseline rows:', rows)
print('NOTE: GitHub computed refs/pull/1036/merge over develop %s (2026-09-21 15:01 AEST), which is %s commits behind the current develop %s; that ref is STALE, not a verdict input. The gate re-predicts over the CURRENT develop.' % (gh_dev[:9], sg('rev-list', '--count', gh_dev + '..' + DEV).stdout.strip(), DEV[:9]))
