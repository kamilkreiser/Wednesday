#!/usr/bin/env python3
"""fill_prompt_gate20T2.py — assembles the gate20T2 prompt from prompt_gate20T2.DRAFT.txt: every __H<n>__ token is filled from `git ls-remote origin`
READ IN THIS SAME ACTION (refs/pull/N/head AND the branch), asserted equal to round20T2.py AND to the captured READY (three sources agree or the script
refuses rc 3; PR 5 also == the seat's committed head EXPECT_PR5_COMMIT); __T2SUB__ from newdev_tree.txt (the predict run's tier-2 sub-tree, asserted ==
round20T2 SEAT_T2SUB, MEASURED on the four real heads — a PREDICTED sub-tree refuses rc 4). REFUSES rc 8 while PR 5 is PENDING (no READY 5 captured):
a tier-2 gate without PR 5 is not the batch. Refuses on a residual token, a `deadbeef` literal, a missing thinking directive, or a PENDING-PR- token.
Writes the prompt to briefs/; a COPY of any previous prompt is kept beside as .pre-HHMMSS (never a rename). The gate19B script re-keyed."""
import os, re, shutil, subprocess, sys, hashlib
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round20T2 as R
OUT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_secuura-batch1202-t2.prompt.txt'
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
print('fill_prompt_gate20T2', now(), '| PR5_PENDING', R.PR5_PENDING)
if R.PR5_PENDING: print('REFUSING: PR 5 (KS-1139) is PENDING — no READY 5 captured; run take_pr5_gate20T2.sh when it lands'); sys.exit(8)
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % R.PRS[p]['n'] for p in R.PUSH] + [R.PRS[p]['branch'] for p in R.PUSH]
p_ = subprocess.run(['git', '-C', R.REPO, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if p_.returncode != 0: print('REFUSING: ls-remote rc', p_.returncode, p_.stderr.strip()[:200]); sys.exit(2)
lsr = dict(l.split('\t')[::-1] for l in p_.stdout.strip().splitlines()); print('ls-remote', now(), len(lsr), 'refs')
dev = lsr.get('refs/heads/develop'); print('origin develop', dev, '== pin', dev == R.DEV)
if dev != R.DEV: print('REFUSING: develop moved — re-run predict_batch_scratch_gate20T2.py and re-read THE SHAPE'); sys.exit(3)
READY = {'1': 'mail_seatB21_ready01_pr1_ks965.md', '2': 'mail_seatB21_ready02_pr2_ks1019.md', '4': 'mail_seatB21_ready04_pr4_ks1081.md', '5': 'mail_seatB21_ready05_pr5_ks1139.md'}
txt = open(os.path.join(G, 'prompt_gate20T2.DRAFT.txt'), encoding='utf-8').read()
agree = 0
for p in R.PUSH:
    pr = R.PRS[p]; h_pull = lsr.get('refs/pull/%s/head' % pr['n']); h_br = lsr.get(pr['branch'])
    rn, rh, rb = R.parse_ready(os.path.join(G, READY[p]), pr['key'].lower())
    ok = h_pull == h_br == pr['head'] == rh and rn == pr['n'] and (p != '5' or pr['head'] == R.EXPECT_PR5_COMMIT)
    print('  #%s pull %s branch %s round20T2 %s READY %s (READY #%s)%s -> %s' % (pr['n'], (h_pull or '?')[:9], (h_br or '?')[:9], pr['head'][:9], (rh or '?')[:9], rn, (' seat commits.tsv %s' % R.EXPECT_PR5_COMMIT[:9]) if p == '5' else '', 'AGREE' if ok else 'DISAGREE'))
    if not ok: print('REFUSING: head disagreement on #%s' % pr['n']); sys.exit(3)
    agree += 1; txt = txt.replace('__H%s__' % pr['n'], h_pull)
nd = dict(l.split(' ', 1) for l in open(os.path.join(G, 'newdev_tree.txt')).read().strip().splitlines())
print('newdev_tree.txt: develop', nd['develop'][:9], 't2sub', nd['t2sub'][:12], nd['t2sub_kind'], '== SEAT_T2SUB', nd['t2sub'] == R.SEAT_T2SUB, '| pr5_head', nd['pr5_head'][:9], '| read', nd['read'])
if nd['t2sub'] != R.SEAT_T2SUB or nd['develop'] != R.DEV or nd['t2sub_kind'] != 'MEASURED' or nd['pr5_head'] != R.PRS['5']['head']:
    print('REFUSING: the predict run disagrees with the pins or was PREDICTED — re-run predict_batch_scratch_gate20T2.py'); sys.exit(4)
txt = txt.replace('__T2SUB__', nd['t2sub'])
res = re.findall(r'__[A-Z0-9]+__', txt)
if res: print('REFUSING: residual tokens', res); sys.exit(5)
if 'deadbeef' in txt.lower(): print('REFUSING: a deadbeef literal'); sys.exit(6)
if not txt.startswith('ultrathink\n'): print('REFUSING: the first line is not the thinking directive'); sys.exit(7)
if 'PENDING-PR-' in txt: print('REFUSING: PARTIAL'); sys.exit(8)
for h in [R.PRS[p]['head'] for p in R.PUSH] + [R.DEV, R.SEAT_T2SUB, R.SEAT_GO_STRING, R.go_string(), 'fleet/briefs_staged/2026-09-23_raise_seatB_21.md', 'mail_gate20T2_ready.md', R.REPORT_DIR, R.BRIEF_ALL11]:
    assert h in re.sub(r'\n\s*', ' ', txt) or h in txt, 'missing ' + h
if os.path.exists(OUT):
    bk = OUT + '.pre-' + now()[11:19].replace(':', ''); shutil.copyfile(OUT, bk); print('previous prompt COPIED beside as', bk)
open(OUT, 'w', encoding='utf-8').write(txt)
b = open(OUT, 'rb').read(); print('WROTE', OUT, len(txt.splitlines()), 'lines', len(b), 'B sha256', hashlib.sha256(b).hexdigest(), '| heads agree 4/4 =', agree, '| written', now())
