#!/usr/bin/env python3
"""fill_prompt_gate16B.py — assemble the batch-gate prompt from prompt_gate16B.DRAFT.part1..3.txt, substituting the PR numbers / heads / READY
timestamps of the eight seat PRs (1 2 3 4 5 6 7 9) from THREE agreeing sources read IN THIS ACTION: (i) round16B.py (the pins), (ii) the captured
READY mails (mail_seatB16_ready*_pr<N>_*.md), (iii) `git ls-remote origin` of refs/heads/develop + every refs/pull/N/head + every branch (READ-ONLY
in the Secuura checkout) — REFUSES (rc 1) if any of the three disagrees on a head or develop, on a residual `__TOKEN__`, or if fewer than eight
READYs are captured (this round has no PARTIAL form: all eight landed before the drafter started). Also substitutes __DEV__ / __DEVTREE__ / __ALL8__.
Writes briefs/2026-09-22_secuura-batch1147-1161.prompt.txt (backup beside on change). Prints lines / bytes / sha256. Idempotent. Derived from
gatesets/2026-09-21_gate15_docs_comments/fill_prompt_gate15.py."""
import glob, hashlib, os, re, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round16B as R
BRIEFS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs'
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
print('fill_prompt_gate16B', now())
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB16_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    t = open(f, encoding='utf-8').read(); m = re.search(R.ready_regex(), t); ts = re.search(r'^TS: (\S+)', t, re.M)
    if m: READY[m.group(1)] = dict(n=m.group(3), h=m.group(4), key=m.group(2), ts=ts.group(1) if ts else '?', file=os.path.basename(f))
print('READYs:', {k: (v['n'], v['h'][:9], v['ts']) for k, v in sorted(READY.items(), key=lambda kv: int(kv[0]))})
missing = [p for p in R.PUSH if p not in READY]
if missing: print('REFUSING: READY(s) not captured for seat PR(s)', missing); sys.exit(1)
# (iii) origin, in this action
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % R.PRS[p]['n'] for p in R.PUSH] + [R.PRS[p]['branch'] for p in R.PUSH]
p_ = subprocess.run(['git', '-C', R.REPO, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if p_.returncode: print('REFUSING: ls-remote rc', p_.returncode, p_.stderr[:200]); sys.exit(1)
origin = dict((l.split('\t')[1], l.split('\t')[0]) for l in p_.stdout.strip().splitlines())
print('ls-remote', now(), '| develop', origin.get('refs/heads/develop', '?')[:9], '| refs read', len(origin), '(want %d)' % len(refs))
bad = []
if origin.get('refs/heads/develop') != R.DEV: bad.append(('develop', origin.get('refs/heads/develop'), R.DEV))
for p in R.PUSH:
    pr = R.PRS[p]; ph = origin.get('refs/pull/%s/head' % pr['n']); bh = origin.get(pr['branch'])
    ok = ph == pr['head'] == bh == READY[p]['h'] and READY[p]['n'] == pr['n']
    print('  PR %-2s #%s origin pull/head %s branch %s | round16B %s | READY %s (#%s) -> %s' % (p, pr['n'], (ph or '?')[:9], (bh or '?')[:9], pr['head'][:9], READY[p]['h'][:9], READY[p]['n'], 'AGREE' if ok else 'DISAGREE'))
    if not ok: bad.append((p, ph, bh, pr['head'], READY[p]['h']))
if bad: print('REFUSING: a pin disagrees among origin / round16B / the READYs:', bad); sys.exit(1)
def tsz(t): return t[11:19] + 'Z' if len(t) >= 19 else t
SUBS = {'__DEV__': R.DEV, '__DEVTREE__': R.DEV_TREE, '__ALL8__': R.SEAT_ALL8}
for p in R.PUSH:
    SUBS['__N%s__' % p] = R.PRS[p]['n']; SUBS['__H%s__' % p] = R.PRS[p]['head']; SUBS['__TS%s__' % p] = tsz(READY[p]['ts'])
parts = [open(os.path.join(G, 'prompt_gate16B.DRAFT.part%d.txt' % i), encoding='utf-8').read() for i in range(1, 4)]
s = ''.join(parts)
for k, v in sorted(SUBS.items(), key=lambda kv: -len(kv[0])):
    c = s.count(k); print('  %-12s -> %-42s x%d' % (k, v, c))
    if c == 0: print('REFUSING: token never used', k); sys.exit(1)
    s = s.replace(k, v)
res = re.findall(r'__[A-Z0-9]+__', s)
if res: print('REFUSING: residual tokens', sorted(set(res))); sys.exit(1)
if not s.startswith('ultrathink\n'): print('REFUSING: the first line is not ultrathink'); sys.exit(1)
if 'PENDING-PR-' in s: print('REFUSING: a PENDING-PR- marker in a complete prompt'); sys.exit(1)
out = os.path.join(BRIEFS, '2026-09-22_secuura-batch1147-1161.prompt.txt')
if os.path.exists(out):
    old = open(out, encoding='utf-8').read()
    if old != s:
        bk = out + '.pre-' + subprocess.run(['date', '-u', '+%H%M%S'], capture_output=True, text=True).stdout.strip()
        os.replace(out, bk); print('backup of the previous prompt beside it:', bk)
open(out, 'w', encoding='utf-8').write(s)
b = s.encode('utf-8')
print('written', out); print('lines', s.count('\n'), 'bytes', len(b), 'sha256', hashlib.sha256(b).hexdigest())
print('report dir named in the prompt:', (re.search(r'reports/(2026-09-22-batch1147-1161-r1)/', s) or [None, '?'])[1])
print('verdict subject prefix:', (re.search(r'^\[QA -> Wednesday\] BATCH GATE [^\n]*?\) —', s, re.M) or [None])[0])
print('GO string present:', 'GO: merge #1147, #1149, #1151, #1153, #1155, #1157, #1159, #1161 batch' in s)
