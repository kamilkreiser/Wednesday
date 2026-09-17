#!/usr/bin/env python3
"""drafter_merged_1034.py NEWDEV — in the drafter CLONE only: merge-tree --write-tree fd81a75f0 x NEWDEV; name the merged tree; assert its
services/api-gateway and packages/shared subtrees equal the head's; the files differing merged vs head tree = exactly develop's own delta 27e53ec3a..NEWDEV;
the two PR blobs unchanged. The object is already in the checkout's store (read through the clone's alternates; nothing fetched)."""
import subprocess, sys, json, os, datetime
GSD = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GSD + '/drafter_paths.json')); C = PA['C']
H = PA['sha']['head']; PIN = PA['sha']['dev']; NEW = sys.argv[1]
def run(*a): p = subprocess.run(['git', '-C', C, *a], capture_output=True, text=True); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('drafter_merged_1034', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| new develop object:', run('cat-file', '-t', NEW)[1])
rc, o, e = run('merge-tree', '--write-tree', '--name-only', H, NEW); lines = o.split('\n'); MT = lines[0]
print('merge-tree --write-tree head x %s rc %d tree %s | conflicted-name lines %d %s' % (NEW[:9], rc, MT, len(lines) - 1, e[:200]))
ht = run('rev-parse', H + '^{tree}')[1]
for sub in ('Blockchain/Dev/services/api-gateway', 'Blockchain/Dev/packages/shared', 'Blockchain/Dev/services/originate'):
    a, b = run('rev-parse', H + ':' + sub)[1], run('rev-parse', MT + ':' + sub)[1]; print('  subtree %-40s head %s merged %s equal %s' % (sub.split('Dev/')[1], a[:9], b[:9], a == b))
d1 = sorted(run('diff', '--name-only', ht, MT)[1].split('\n')); d2 = sorted(run('diff', '--name-only', PIN, NEW)[1].split('\n'))
print('  files differing head tree vs merged tree:', len(d1), '| develop own delta %s..%s: %d | equal: %s' % (PIN[:9], NEW[:9], len(d2), d1 == d2))
for p in ('Blockchain/Dev/services/api-gateway/src/middleware/auth.ts', 'Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts'):
    print('  blob', p.split('/')[-1][:40], 'head', run('rev-parse', H + ':' + p)[1][:9], 'merged', run('rev-parse', MT + ':' + p)[1][:9])
print('  compare merge-base(head, new develop):', run('merge-base', H, NEW)[1][:9])
