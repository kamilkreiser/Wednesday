#!/usr/bin/env python3
"""fill_prompt_gate20T1.py — assembles the gate20T1 prompt from prompt_gate20T1.DRAFT.txt: every __H<n>__ head is filled from `git ls-remote origin`
READ IN THIS SAME ACTION (refs/pull/N/head AND the branch), asserted equal to round20T1.py AND to the captured READY (three sources agree or the script
refuses rc 3); the launch-develop tokens (__DEV__, __DEVTREE__, __BEHIND__, __DEVMOVE__, the seven merged trees __M<n>__, __END__, __T1SUB__, __ALL11BASE__)
from newdev_tree.txt + devmove.txt (the predict run) — REFUSES rc 3 unless newdev_tree's dev_launch == origin develop read in THIS action (a stale
reading never reaches a prompt), rc 4 unless it is MEASURED on seven real heads. REFUSES rc 8 while PR 11 is PENDING (no READY 11 captured): a tier-1
gate without PR 11 is not the batch (Wednesday's AMENDMENT 18:1x). Refuses on a residual token, a `deadbeef` literal, a missing thinking directive, or a
PENDING-PR- token. Writes the prompt beside this script (the drafter's write fence is this gateset dir); a COPY of any previous prompt is kept beside as
.pre-HHMMSS (never a rename). The gate20T2 script re-keyed.
  --control-six <path under /private/tmp/claude-501/…/scratchpad>: PR 11 PENDING only — writes a CONTROL prompt (PR 11's tokens replaced by
  PR11-NOT-YET-RAISED markers, never PENDING-PR-) to the scratchpad path, for exercising the launcher's other guards on the six real heads. Never the
  real prompt path."""
import os, re, shutil, subprocess, sys, hashlib
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round20T1 as R
OUT = os.path.join(G, '2026-09-23_secuura-batch1204-t1.prompt.txt')
CONTROL = None
if len(sys.argv) > 2 and sys.argv[1] == '--control-six':
    CONTROL = os.path.realpath(sys.argv[2])
    if not (CONTROL.startswith('/private/tmp/claude-501/') and '/scratchpad' in CONTROL): print('REFUSING: --control-six writes only under a scratchpad'); sys.exit(9)
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
print('fill_prompt_gate20T1', now(), '| PR11_PENDING', R.PR11_PENDING, '| mode', 'CONTROL-SIX -> ' + CONTROL if CONTROL else 'REAL -> ' + OUT)
if R.PR11_PENDING and not CONTROL: print('REFUSING: PR 11 (KS-1143) is PENDING — no READY 11 captured; run take_pr11_gate20T1.sh when it lands'); sys.exit(8)
if CONTROL and not R.PR11_PENDING: print('REFUSING: --control-six is for the PENDING state only; PR 11 is pinned — fill the real prompt'); sys.exit(8)
LIVE = [p for p in R.PUSH if R.PRS[p]['n']]
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % R.PRS[p]['n'] for p in LIVE] + [R.PRS[p]['branch'] for p in LIVE if R.PRS[p]['branch']]
p_ = subprocess.run(['git', '-C', R.REPO, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if p_.returncode != 0: print('REFUSING: ls-remote rc', p_.returncode, p_.stderr.strip()[:200]); sys.exit(2)
lsr = dict(l.split('\t')[::-1] for l in p_.stdout.strip().splitlines()); print('ls-remote', now(), len(lsr), 'refs')
dev = lsr.get('refs/heads/develop'); nd = R.read_newdev()
print('origin develop', dev, '| newdev_tree dev_launch', nd.get('dev_launch'), '| equal', dev == nd.get('dev_launch'), '| newdev read', nd.get('read'))
if not nd or dev != nd.get('dev_launch'): print('REFUSING: origin develop is not the develop the predict run measured — re-run predict_batch_scratch_gate20T1.py (or the repin script) first'); sys.exit(3)
if nd.get('base') != R.BASE: print('REFUSING: newdev_tree base != BASE'); sys.exit(4)
if not CONTROL and (nd.get('t1sub_kind') != 'MEASURED' or nd.get('pr11_head') != R.PRS['11']['head']): print('REFUSING: the predict run was PREDICTED or pre-dates PR 11\'s head — re-run predict'); sys.exit(4)
txt = open(os.path.join(G, 'prompt_gate20T1.DRAFT.txt'), encoding='utf-8').read()
agree = 0
for p in LIVE:
    pr = R.PRS[p]; h_pull = lsr.get('refs/pull/%s/head' % pr['n']); h_br = lsr.get(pr['branch'])
    rn, rh = R.parse_ready(os.path.join(G, R.READY_FILES[p]))
    ok = h_pull == h_br == pr['head'] == rh and rn == pr['n']
    print('  #%s pull %s branch %s round20T1 %s READY %s (READY #%s) -> %s' % (pr['n'], (h_pull or '?')[:9], (h_br or '?')[:9], pr['head'][:9], (rh or '?')[:9], rn, 'AGREE' if ok else 'DISAGREE'))
    if not ok: print('REFUSING: head disagreement on #%s' % pr['n']); sys.exit(3)
    agree += 1; txt = txt.replace('__H%s__' % pr['n'], h_pull) if p != '11' else txt.replace('__H11__', h_pull)
    txt = txt.replace('__M%s__' % (pr['n'] if p != '11' else '11'), nd['merged_' + pr['n']])
if CONTROL:
    for tok in ('__N11__', '__H11__', '__B11__', '__TREE11__', '__BLOB11__', '__M11__', '__H11S__'): txt = txt.replace(tok, 'PR11-NOT-YET-RAISED')
    go = 'GO: merge #1204, #1207, #1208, #1209, #1210, #1211, #PR11-NOT-YET-RAISED batch'
else:
    pr = R.PRS['11']; hd = pr['head']
    b11 = [v for k, v in [l.split(' ', 1) for l in open(os.path.join(G, 'newdev_tree.txt')).read().splitlines()] if k == 'blob' and v.startswith(pr['files'][0]['path'] + ' ')]
    blob40 = b11[0].split(' ')[1] if b11 else '?'
    txt = txt.replace('__N11__', pr['n']).replace('__H11S__', hd[:9]).replace('__B11__', (pr['branch'] or '?').replace('refs/heads/', '')).replace('__BLOB11__', blob40)
    if not nd.get('tree11') or blob40 == '?': print('REFUSING: newdev_tree.txt lacks PR 11\'s head tree / blob — re-run predict'); sys.exit(4)
    txt = txt.replace('__TREE11__', nd['tree11'])
    go = R.go_string()
dm = open(os.path.join(G, 'devmove.txt')).read().strip().splitlines()[1:]
txt = txt.replace('__DEVMOVE__', '\n'.join('  ' + l.split(' ', 1)[0] + ' ' + l.split(' ', 3)[3] for l in dm))
for k, v in (('__DEV__', nd['dev_launch']), ('__DEVTREE__', nd['dev_launch_tree']), ('__BEHIND__', nd['behind']), ('__END__', nd['end_tree']), ('__T1SUB__', nd['t1sub']), ('__ALL11BASE__', nd['all11_over_base']), ('__GO__', go)):
    txt = txt.replace(k, v)
res = re.findall(r'__[A-Z0-9]+__', txt)
if res: print('REFUSING: residual tokens', sorted(set(res))); sys.exit(5)
if 'deadbeef' in txt.lower(): print('REFUSING: a deadbeef literal'); sys.exit(6)
if not txt.startswith('ultrathink\n'): print('REFUSING: the first line is not the thinking directive'); sys.exit(7)
if 'PENDING-PR-' in txt: print('REFUSING: PARTIAL'); sys.exit(8)
must = [R.PRS[p]['head'] for p in LIVE] + [R.BASE, nd['dev_launch'], nd['end_tree'], nd['t1sub'], R.SEAT_T1SUB_6, R.SEAT_ALL10, R.T2_SUB, go, 'fleet/briefs_staged/2026-09-23_raise_seatB_21.md', 'mail_gate20T1_ready.md', R.REPORT_DIR]
miss = [h for h in must if not (h in re.sub(r'\n\s*', ' ', txt) or h in txt)]
if miss: print('REFUSING: missing from the filled prompt:', miss); sys.exit(5)
dst = CONTROL or OUT
if os.path.exists(dst):
    bk = dst + '.pre-' + now()[11:19].replace(':', ''); shutil.copyfile(dst, bk); print('previous prompt COPIED beside as', bk)
open(dst, 'w', encoding='utf-8').write(txt)
b = open(dst, 'rb').read(); print('WROTE', dst, len(txt.splitlines()), 'lines', len(b), 'B sha256', hashlib.sha256(b).hexdigest(), '| heads agree %d/%d' % (agree, len(LIVE)), '| GO', go, '| written', now())
