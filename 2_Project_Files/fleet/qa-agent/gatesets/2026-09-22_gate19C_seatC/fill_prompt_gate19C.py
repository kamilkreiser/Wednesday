#!/usr/bin/env python3
"""fill_prompt_gate19C.py — assembles the gate19C prompt from prompt_gate19C.DRAFT.txt: every __H<n>__ token is filled from `git ls-remote origin`
READ IN THIS SAME ACTION (refs/pull/N/head AND the branch), asserted equal to round19C.py AND to the captured READY (three sources agree or the
script refuses rc 3); __ALL12__ from newdev_tree.txt (the predict run's all-12 tree, asserted == round19C SEAT_ALL14). Refuses on a residual token,
a `deadbeef` literal, a missing thinking directive, or a PENDING-PR- token. Writes the prompt to briefs/; a COPY of any previous prompt is kept
beside as .pre-HHMMSS (never a rename)."""
import glob, os, re, shutil, subprocess, sys, hashlib
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round19C as R
OUT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1180-1197.prompt.txt'
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
print('fill_prompt_gate19C', now())
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % R.PRS[p]['n'] for p in R.PUSH] + [R.PRS[p]['branch'] for p in R.PUSH]
o = subprocess.run(['git', '-C', R.REPO, 'ls-remote', 'origin'] + refs, capture_output=True, text=True).stdout
lsr = dict(l.split('\t')[::-1] for l in o.strip().splitlines()); print('ls-remote', now(), len(lsr), 'refs')
dev = lsr.get('refs/heads/develop'); print('origin develop', dev, '== pin', dev == R.DEV)
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatC19_ready*_pr*_*.md'))):
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (m.group(3), m.group(4))
txt = open(os.path.join(G, 'prompt_gate19C.DRAFT.txt'), encoding='utf-8').read()
agree = 0
for p in R.PUSH:
    pr = R.PRS[p]; h_pull = lsr.get('refs/pull/%s/head' % pr['n']); h_br = lsr.get(pr['branch']); h_ready = READY.get(p, ('?', '?'))[1]
    ok = h_pull == h_br == pr['head'] == h_ready and READY.get(p, ('?',))[0] == pr['n']
    print('  #%s pull %s branch %s round19C %s READY %s -> %s' % (pr['n'], (h_pull or '?')[:9], (h_br or '?')[:9], pr['head'][:9], h_ready[:9], 'AGREE' if ok else 'DISAGREE'))
    if not ok: print('REFUSING: head disagreement on #%s' % pr['n']); sys.exit(3)
    agree += 1; txt = txt.replace('__H%s__' % pr['n'], h_pull)
nd = dict(l.split(' ', 1) for l in open(os.path.join(G, 'newdev_tree.txt')).read().strip().splitlines())
print('newdev_tree.txt: develop', nd['develop'][:9], 'all12', nd['all12'][:12], '== SEAT_ALL14', nd['all12'] == R.SEAT_ALL14, '| pairblob ==', nd['pairblob'] == R.PAIR_BLOB)
if nd['all12'] != R.SEAT_ALL14 or nd['develop'] != R.DEV: print('REFUSING: the predict run disagrees with the pins — re-run predict_batch_scratch_gate19C.py'); sys.exit(4)
txt = txt.replace('__ALL12__', nd['all12'])
res = re.findall(r'__[A-Z0-9]+__', txt)
if res: print('REFUSING: residual tokens', res); sys.exit(5)
if 'deadbeef' in txt.lower(): print('REFUSING: a deadbeef literal'); sys.exit(6)
if not txt.startswith('ultrathink\n'): print('REFUSING: the first line is not the thinking directive'); sys.exit(7)
if 'PENDING-PR-' in txt: print('REFUSING: PARTIAL'); sys.exit(8)
for h in [R.PRS[p]['head'] for p in R.PUSH] + [R.DEV, R.SEAT_ALL14, R.PAIR_BLOB, R.GO_STRING, 'fleet/briefs_staged/2026-09-22_raise_seatC_19.md']:
    assert h in txt, 'missing ' + h
if os.path.exists(OUT):
    bk = OUT + '.pre-' + now()[11:19].replace(':', ''); shutil.copyfile(OUT, bk); print('previous prompt COPIED beside as', bk)
open(OUT, 'w', encoding='utf-8').write(txt)
b = open(OUT, 'rb').read(); print('WROTE', OUT, len(txt.splitlines()), 'lines', len(b), 'B sha256', hashlib.sha256(b).hexdigest(), '| heads agree 12/12 =', agree, '| written', now())
