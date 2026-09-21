#!/usr/bin/env python3
"""fill_prompt_gate1036.py — fill prompt_gate1036.TEMPLATE.txt into the launchable prompt. Every pin is RE-READ at origin (git ls-remote from the
Secuura checkout, READ) in the same action the prompt is written; the merged tree is RE-COMPUTED by merge-tree in the drafter's SCRATCH CLONE (never the
checkout); the 50 equality targets come from `git diff --raw -z --abbrev=40 <merge-base> <head>` (READ). Refuses on: head/develop not equal to the
expected pins, a target count != 50, any residual @@TOKEN@@, any `PENDING` or `deadbeef` literal, line 1 != ultrathink. Never overwrites without a
.pre-* copy. Usage: fill_prompt_gate1036.py <scratch clone> <expected head> <expected develop> <output prompt>"""
import datetime, hashlib, os, re, shutil, subprocess, sys
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
G = os.path.dirname(os.path.abspath(__file__))
CLONE, EXP_HEAD, EXP_DEV, OUT = sys.argv[1:5]
assert CLONE.startswith('/private/tmp/claude-501/'), 'scratch clone only'
def run(args):
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0: raise SystemExit('REFUSING: %r rc %d %s' % (args[:4], p.returncode, p.stderr[-300:]))
    return p.stdout
def git(*a): return run(['git', '-C', REPO] + list(a))
def sg(*a): return run(['git', '-C', CLONE] + list(a))
now = datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
lsr = git('ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1036/head', 'refs/heads/feature/ks-763-qs-in-range')
print('ls-remote at', now); print(lsr.rstrip())
refs = {l.split('\t')[1]: l.split('\t')[0] for l in lsr.splitlines()}
head, dev = refs['refs/pull/1036/head'], refs['refs/heads/develop']
if head != EXP_HEAD or refs['refs/heads/feature/ks-763-qs-in-range'] != EXP_HEAD: raise SystemExit('REFUSING: head at origin %s != expected %s' % (head, EXP_HEAD))
if dev != EXP_DEV: raise SystemExit('REFUSING: develop at origin %s != expected %s — re-predict the merged tree first (predict_merge_gate1036.py), then re-fill with the new develop' % (dev, EXP_DEV))
mb = git('merge-base', head, dev).strip()
mt = sg('merge-tree', '--write-tree', dev, head).split()
merged = mt[0]
if len(mt) != 1: raise SystemExit('REFUSING: merge-tree reports conflicts: %r' % mt[1:])
print('merge-base', mb, '| merged tree over develop', dev[:9], '=', merged)
raw = git('diff', '--raw', '-z', '--abbrev=40', mb, head).split('\0')
recs = []
for i in range(0, len(raw) - 1, 2):
    m = re.match(r':(\d{6}) (\d{6}) ([0-9a-f]{40}) ([0-9a-f]{40}) (\w)', raw[i])
    if m: recs.append((raw[i + 1], m.group(4), m.group(2)))
if len(recs) != 50: raise SystemExit('REFUSING: %d PR paths, want 50' % len(recs))
targets = ', '.join('%s %s (%s)' % r for r in recs)
tpl = open(os.path.join(G, 'prompt_gate1036.TEMPLATE.txt'), encoding='utf-8').read()
s = tpl.replace('@@HEAD@@', head).replace('@@DEV@@', dev).replace('@@DEV_SHORT@@', dev[:9]).replace('@@MERGED@@', merged).replace('@@TARGETS@@', targets)
for bad in ('@@', 'PENDING', 'deadbeef', 'DEADBEEF'):
    if bad in s: raise SystemExit('REFUSING: residual %r in the filled prompt' % bad)
if s.splitlines()[0] != 'ultrathink': raise SystemExit('REFUSING: line 1 is not ultrathink')
if s.count(head) < 5 or s.count(dev) < 1 or s.count(merged) < 2: raise SystemExit('REFUSING: pin counts head %d dev %d merged %d' % (s.count(head), s.count(dev), s.count(merged)))
raw_b = s.encode('utf-8')
if any((b < 0x20 and b not in (9, 10, 13)) or b == 0x7f for b in raw_b): raise SystemExit('REFUSING: control bytes')
if os.path.exists(OUT):
    bak = OUT + '.pre-' + datetime.datetime.now().strftime('%H%M%S'); shutil.copyfile(OUT, bak); print('existing prompt copied to', bak)
open(OUT, 'w', encoding='utf-8').write(s)
print(now, 'wrote', OUT, 'lines', s.count('\n'), 'bytes', len(raw_b), 'sha256', hashlib.sha256(raw_b).hexdigest(), '| head', head, '| develop', dev, '| merged', merged, '| targets', len(recs))
