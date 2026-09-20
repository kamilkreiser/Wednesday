#!/usr/bin/env python3
"""shape_1.py — READ-ONLY local object reads in the Secuura checkout (rev-list / rev-parse / diff --raw / ls-tree / cat-file): each head is ONE
commit whose parent is 778e6cfe2; head trees; the changed paths per PR with (develop blob | ABSENT, head blob, mode); pairwise disjointness of
the union; the same blobs at the NEW develop cbae988db (the #1105 squash) — the twelve paths the seat named vs the eight PR paths; the 12 #1105
paths vs the 8. Nothing written to the checkout."""
import subprocess, sys, itertools
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BASE = '778e6cfe2b6061d60ffcf3a57a951c84dc152b67'
DEV = 'cbae988dbe90ebe556459ada2cb437eaf80e2402'
PRS = [('1106', 'KS-1232', '2abc82d11014f00567b75a6b8fab5ec5e78f9df2'), ('1107', 'KS-753', '7e7da2f88f9ef8dcf571a5720bb7bffcd700aa30'),
       ('1108', 'KS-1234', '4904c081c4f9be776acef78349bc10384f10de35'), ('1109', 'KS-1279', 'f592268af36b282029e50ff2fa1ebe2614304b81'),
       ('1110', 'KS-880', 'a2a7d7845e75dac2df5c6ad0c4109d5f63394d4c'), ('1111', 'KS-1223', '3d1ea289a0c367af5cd0d060322e46fc900a1c76')]
def git(*a):
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr
print('date', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
for c in [BASE, DEV] + [h for _, _, h in PRS]:
    rc, o, e = git('cat-file', '-t', c); print('object', c[:9], (o.strip() or e.strip()))
rc, o, e = git('rev-parse', BASE + '^{tree}', DEV + '^{tree}'); print('trees base/dev', o.split())
rc, o, e = git('rev-list', '--parents', '-n1', DEV); print('develop parents', o.split()[1:], '| == [BASE]:', o.split()[1:] == [BASE])
rc, o, e = git('diff', '--name-only', BASE, DEV); P1105 = [l for l in o.splitlines() if l]
print('#1105 squash paths', len(P1105))
for l in P1105: print('   ', l)
union = {}; per = {}
for n, tk, h in PRS:
    rc, o, e = git('rev-list', '--parents', '-n1', h); par = o.split()[1:]
    rc, t, e = git('rev-parse', h + '^{tree}')
    rc, raw, e = git('diff', '--raw', '--abbrev=40', BASE, h)
    files = []
    for l in raw.strip().splitlines():
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split()
        files.append((path, 'ABSENT' if b1 == '0' * 40 else b1, b2, st, m2))
    rc, ns, e = git('diff', '--numstat', BASE, h)
    per[n] = files
    print('#%s %s head %s parents %s (== [BASE] %s) tree %s files %d' % (n, tk, h[:9], [p[:9] for p in par], par == [BASE], t.strip(), len(files)))
    for f in files:
        print('    %s %-8s dev %s head %s mode %s' % (f[3], f[0].split('/')[-1][:40], f[1][:12], f[2][:12], f[4]))
        print('       ', f[0])
        union.setdefault(f[0], []).append(n)
    print('    numstat:', ' | '.join(l.replace('\t', ' ') for l in ns.strip().splitlines()))
    # the same paths at the NEW develop: blobs identical to BASE?
    for f in files:
        rc, o, e = git('rev-parse', '-q', '--verify', DEV + ':' + f[0]); bd = o.strip() or 'ABSENT'
        print('       at develop cbae988db:', bd[:12], '== base-side', bd == f[1])
print('UNION paths', len(union), '| multi-PR paths', {k: v for k, v in union.items() if len(v) > 1})
print('pairwise overlap counts:', [(a, b, len(set(f[0] for f in per[a]) & set(f[0] for f in per[b]))) for a, b in itertools.combinations(per, 2) if set(f[0] for f in per[a]) & set(f[0] for f in per[b])] or 'ALL ZERO (15 pairs)')
print('#1105 paths ∩ the 8 PR paths:', sorted(set(P1105) & set(union)) or 'NONE')
