#!/usr/bin/env python3
"""fill_prompt_gate15.py — assemble the batch-gate prompt from prompt_gate15.DRAFT.part1..3.txt, substituting the PR numbers / heads / READY
timestamps of seat PRs 5..10 from the captured READY mails (mail_seatB15_ready*_pr<N>_*.md; PRs 1-4 = #1136 / #1137 / #1139 / #1140 are typed
into the draft after their READYs landed). Writes briefs/2026-09-21_secuura-batch1136-<last>.prompt.txt when all ten READYs are captured; when
fewer are captured (the drafter's 60-minute bound), writes briefs/2026-09-21_secuura-batch15_partial.prompt.txt with every missing PR's tokens
replaced by `PENDING-PR-<n>` markers and a leading line naming which PRs are IN — Wednesday decides whether to wait. Refuses (rc 1) on any residual
`__TOKEN__`. Prints lines / bytes / sha256. Idempotent. Writes nothing else. Derived from gatesets/2026-09-21_gate1130to1135/fill_prompt_1130.py."""
import glob, hashlib, os, re, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__))
BRIEFS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs'
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB15_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    t = open(f, encoding='utf-8').read()
    m = re.search(r'READY FOR QA \(Seat B 15th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', t)
    ts = re.search(r'^TS: (\S+)', t, re.M)
    if m: READY[m.group(1)] = dict(n=m.group(3), h=m.group(4), key=m.group(2), ts=ts.group(1) if ts else '?', file=os.path.basename(f))
print('READYs:', {k: (v['n'], v['h'][:9], v['ts']) for k, v in sorted(READY.items(), key=lambda kv: int(kv[0]))})
PUSH = [str(i) for i in range(1, 11)]
fixed = {'1': '1136', '2': '1137', '3': '1139', '4': '1140'}
for p, n in fixed.items():
    if p in READY and READY[p]['n'] != n: print('REFUSING: the draft types PR %s as #%s but its READY says #%s' % (p, n, READY[p]['n'])); sys.exit(1)
missing = [p for p in PUSH if p not in READY]
partial = bool(missing)
def tsz(t): return t[11:19] + 'Z' if len(t) >= 19 else t
SUBS = {}
for p in ['5', '6', '7', '8', '9', '10']:
    if p in READY: SUBS['__N%s__' % p] = READY[p]['n']; SUBS['__H%s__' % p] = READY[p]['h']; SUBS['__TS%s__' % p] = tsz(READY[p]['ts'])
    else: SUBS['__N%s__' % p] = 'PENDING-PR-%s' % p; SUBS['__H%s__' % p] = 'PENDING-HEAD-PR-%s' % p; SUBS['__TS%s__' % p] = 'PENDING'
nums = sorted(int(v['n']) for v in READY.values()); last = str(nums[-1]) if nums else '1140'
if not partial and int(READY['10']['n']) != nums[-1]: print('REFUSING: PR 10 (%s) is not the highest PR number %s — the draft names PR 10 as #<last>' % (READY['10']['n'], last)); sys.exit(1)
SUBS['__NLAST__'] = last if not partial else ('%s-PARTIAL' % last)
parts = [open(os.path.join(G, 'prompt_gate15.DRAFT.part%d.txt' % i), encoding='utf-8').read() for i in range(1, 4)]
s = ''.join(parts)
for k, v in SUBS.items():
    c = s.count(k); print('  %-10s -> %-42s x%d' % (k, v, c))
    if c == 0: print('REFUSING: token never used', k); sys.exit(1)
    s = s.replace(k, v)
res = re.findall(r'__[A-Z0-9]+__', s)
if res: print('REFUSING: residual tokens', sorted(set(res))); sys.exit(1)
if not s.startswith('ultrathink\n'): print('REFUSING: the first line is not ultrathink'); sys.exit(1)
if partial:
    present = [p for p in PUSH if p in READY]
    s = s.replace('ultrathink\n', 'ultrathink\n\nPARTIAL PROMPT — written at the drafter\'s bound with %d of 10 READYs captured (seat PRs %s IN = %s; PRs %s NOT YET RAISED at %s). Every `PENDING-PR-n` / `PENDING-HEAD-PR-n` token below is a slot for a READY that had not landed; Wednesday re-fills with fill_prompt_gate15.py once the captures exist (README.md section 8) and does NOT launch this file as it stands.\n' % (
        len(present), present, ['#' + READY[p]['n'] for p in present], missing, subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()), 1)
    out = os.path.join(BRIEFS, '2026-09-21_secuura-batch15_partial.prompt.txt')
else:
    out = os.path.join(BRIEFS, '2026-09-21_secuura-batch1136-%s.prompt.txt' % last)
if os.path.exists(out):
    old = open(out, encoding='utf-8').read()
    if old != s:
        bk = out + '.pre-' + subprocess.run(['date', '-u', '+%H%M%S'], capture_output=True, text=True).stdout.strip()
        os.replace(out, bk); print('backup of the previous prompt beside it:', bk)
open(out, 'w', encoding='utf-8').write(s)
b = s.encode('utf-8')
print('written', out); print('lines', s.count('\n'), 'bytes', len(b), 'sha256', hashlib.sha256(b).hexdigest())
print('PARTIAL' if partial else 'COMPLETE', '| missing seat PRs:', missing or 'none')
print('report dir named in the prompt:', (re.search(r'reports/(2026-09-21-batch1136-[^/]+-tier2-r1)/', s) or [None, '?'])[1])
print('verdict subject prefix:', (re.search(r'^\[QA -> Wednesday\] BATCH GATE [^\n]*?\) —', s, re.M) or [None])[0])
