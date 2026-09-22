#!/usr/bin/env python3
"""fill_prompt_gate18B.py — assemble the batch-gate prompt from prompt_gate18B.DRAFT.part1..3.txt, substituting the PR numbers / heads / READY
timestamps of the seven seat PRs from THREE agreeing sources read IN THIS ACTION: (i) round18B.py (the pins), (ii) the captured READY mails
(mail_seatB18_ready*_pr<N>_*.md), (iii) `git ls-remote origin` of refs/heads/develop + every refs/pull/N/head + every branch (READ-ONLY in the
Secuura checkout) — REFUSES (rc 1) if any of the three disagrees on a head, if origin develop is not the pin 8c2f7b3fd (a move: re-run
predict_batch_scratch_gate18B.py, re-read THE SHAPE, then re-fill), on a residual `__TOKEN__`, or if fewer than seven READYs are captured (this
round has no PARTIAL form: all seven landed before the drafter started). Also substitutes __PARENT__ / __PARENTTREE__ / __DEV__ / __DEVTREE__ /
__ALL7P__ (the all-7 tree over the parent) / __ENDTREE__ (the all-7 tree over develop — from newdev_tree.txt, which must be for THIS develop) /
__M1__..__M7__ (the per-PR MERGED trees over develop, from newdev_tree.txt). Writes briefs/2026-09-22_secuura-batch1170-1179.prompt.txt
(backup beside on change). Prints lines / bytes / sha256. Idempotent. Derived from gatesets/2026-09-22_gate16B_seatB/fill_prompt_gate16B.py."""
import glob, hashlib, os, re, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round18B as R
BRIEFS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs'
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
print('fill_prompt_gate18B', now())
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB18_ready*_pr*_*.md'))):
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
    print('  PR %-2s #%s origin pull/head %s branch %s | round18B %s | READY %s (#%s) -> %s' % (p, pr['n'], (ph or '?')[:9], (bh or '?')[:9], pr['head'][:9], READY[p]['h'][:9], READY[p]['n'], 'AGREE' if ok else 'DISAGREE'))
    if not ok: bad.append((p, ph, bh, pr['head'], READY[p]['h']))
if bad: print('REFUSING: a pin disagrees among origin / round18B / the READYs (or develop moved off the pin — re-run predict_batch_scratch_gate18B.py and re-read THE SHAPE):', bad); sys.exit(1)
nd = open(os.path.join(G, 'newdev_tree.txt')).read()
dev_now = re.search(r'^DEV_NOW ([0-9a-f]{40})', nd, re.M).group(1)
if dev_now != R.DEV: print('REFUSING: newdev_tree.txt is for another develop', dev_now[:9], '— re-run predict_batch_scratch_gate18B.py'); sys.exit(1)
END = re.search(r'^ALL7_OVER_NEW ([0-9a-f]{40})', nd, re.M).group(1); ALLP = re.search(r'^ALL7_OVER_PARENT ([0-9a-f]{40})', nd, re.M).group(1)
if ALLP != R.SEAT_ALL7: print('REFUSING: the all-7 tree over the parent in newdev_tree.txt is not the seat tree', ALLP[:12], R.SEAT_ALL7[:12]); sys.exit(1)
if END == ALLP: print('REFUSING: END_TREE == the parent-based tree — develop is the parent? newdev_tree.txt stale'); sys.exit(1)
M = {}
for l in nd.splitlines():
    m = re.match(r'^PR(\d+) ([0-9a-f]{40})', l)
    if m: M[m.group(1)] = m.group(2)
if sorted(M) != R.PUSH: print('REFUSING: newdev_tree.txt per-PR merged trees incomplete', sorted(M)); sys.exit(1)
def tsz(t): return t[11:19] + 'Z' if len(t) >= 19 else t
SUBS = {'__PARENT__': R.PARENT, '__PARENTTREE__': R.PARENT_TREE, '__DEV__': R.DEV, '__DEVTREE__': R.DEV_TREE, '__ALL7P__': ALLP, '__ENDTREE__': END}
for p in R.PUSH:
    SUBS['__N%s__' % p] = R.PRS[p]['n']; SUBS['__H%s__' % p] = R.PRS[p]['head']; SUBS['__TS%s__' % p] = tsz(READY[p]['ts']); SUBS['__M%s__' % p] = M[p]
parts = [open(os.path.join(G, 'prompt_gate18B.DRAFT.part%d.txt' % i), encoding='utf-8').read() for i in range(1, 4)]
s = ''.join(parts)
for k, v in sorted(SUBS.items(), key=lambda kv: -len(kv[0])):
    c = s.count(k); print('  %-14s -> %-42s x%d' % (k, v, c))
    if c == 0: print('REFUSING: token never used', k); sys.exit(1)
    s = s.replace(k, v)
res = re.findall(r'__[A-Z0-9]+__', s)
res = [x for x in res if x not in ('__tests__', '__pycache__')]
if res: print('REFUSING: residual tokens', sorted(set(res))); sys.exit(1)
if '__M<k>__' in s: pass   # the generic per-PR placeholder in prose (not a token: contains < >)
if not s.startswith('ultrathink\n'): print('REFUSING: the first line is not ultrathink'); sys.exit(1)
if 'PENDING-PR-' in s: print('REFUSING: a PENDING-PR- marker in a complete prompt'); sys.exit(1)
if re.search(r'\bdeadbeef\b', s): print('REFUSING: a deadbeef literal in the prompt'); sys.exit(1)
out = os.path.join(BRIEFS, '2026-09-22_secuura-batch1170-1179.prompt.txt')
if os.path.exists(out):
    old = open(out, encoding='utf-8').read()
    if old != s:
        bk = out + '.pre-' + subprocess.run(['date', '-u', '+%H%M%S'], capture_output=True, text=True).stdout.strip()
        os.replace(out, bk); print('backup of the previous prompt beside it:', bk)
open(out, 'w', encoding='utf-8').write(s)
b = s.encode('utf-8')
print('written', out); print('lines', s.count('\n'), 'bytes', len(b), 'sha256', hashlib.sha256(b).hexdigest())
print('report dir named in the prompt:', (re.search(r'reports/(2026-09-22-batch1170-1179-r1)/', s) or [None, '?'])[1])
print('verdict subject prefix:', (re.search(r'^\[QA -> Wednesday\] BATCH GATE [^\n]*?\) —', s, re.M) or [None])[0])
print('GO string present:', R.GO_STRING in s, '| END_TREE named in full:', END in s, '| BASE_GO named:', R.DEV in s)
