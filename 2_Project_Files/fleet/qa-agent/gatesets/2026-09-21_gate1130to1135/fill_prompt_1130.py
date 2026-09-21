#!/usr/bin/env python3
"""fill_prompt_1130.py — assemble the batch-gate prompt from prompt_1130.DRAFT.part1..5.txt, substituting the PR numbers / heads / READY timestamps
of PR 3, PR 5 and PR 4 from the captured READY mails (mail_seatB14_ready*_pr<N>_*.md), and write
briefs/2026-09-21_secuura-batch1130-<last>.prompt.txt. Refuses (rc 1) on any residual `__TOKEN__`, on a missing READY, or if the last PR number
is not the highest of the six. Prints lines / bytes / sha256. Idempotent (re-run after the last READY lands). Writes nothing else."""
import glob, hashlib, os, re, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__))
BRIEFS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs'
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB14_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    t = open(f, encoding='utf-8').read()
    m = re.search(r'READY FOR QA \(Seat B 14th\): PR (\d) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', t)
    ts = re.search(r'^TS: (\S+)', t, re.M)
    if m: READY[m.group(1)] = dict(n=m.group(3), h=m.group(4), key=m.group(2), ts=ts.group(1) if ts else '?', file=os.path.basename(f))
print('READYs:', {k: (v['n'], v['h'][:9], v['ts']) for k, v in sorted(READY.items())})
missing = [p for p in ['1', '2', '6', '3', '5', '4'] if p not in READY]
if missing: print('REFUSING: READY(s) not captured for seat PR', missing, '- poll the inbox, run capture_ready_mail_1130.py, re-run'); sys.exit(1)
assert READY['1']['n'] == '1130' and READY['2']['n'] == '1131' and READY['6']['n'] == '1132', 'the first three PR numbers are pinned in the draft text'
nums = sorted(int(v['n']) for v in READY.values()); last = str(nums[-1])
if int(READY['4']['n']) != nums[-1]: print('REFUSING: PR 4 (%s) is not the highest PR number %s — the draft names PR 4 as #<last>' % (READY['4']['n'], last)); sys.exit(1)
def tsz(t): return t[11:19] + 'Z' if len(t) >= 19 else t
SUBS = {'__N3__': READY['3']['n'], '__H3__': READY['3']['h'], '__N5__': READY['5']['n'], '__H5__': READY['5']['h'], '__N4__': READY['4']['n'], '__H4__': READY['4']['h'],
        '__NLAST__': last, '__TS3__': tsz(READY['3']['ts']), '__TS5__': tsz(READY['5']['ts']), '__TS4__': tsz(READY['4']['ts'])}
parts = [open(os.path.join(G, 'prompt_1130.DRAFT.part%d.txt' % i), encoding='utf-8').read() for i in range(1, 6)]
s = ''.join(parts)
for k, v in SUBS.items():
    c = s.count(k); print('  %-10s -> %-42s x%d' % (k, v, c))
    if c == 0: print('REFUSING: token never used', k); sys.exit(1)
    s = s.replace(k, v)
res = re.findall(r'__[A-Z0-9]+__', s)
if res: print('REFUSING: residual tokens', sorted(set(res))); sys.exit(1)
if not s.startswith('ultrathink\n'): print('REFUSING: the first line is not ultrathink'); sys.exit(1)
out = os.path.join(BRIEFS, '2026-09-21_secuura-batch1130-%s.prompt.txt' % last)
if os.path.exists(out):
    old = open(out, encoding='utf-8').read()
    if old != s:
        bk = out + '.pre-' + subprocess.run(['date', '-u', '+%H%M%S'], capture_output=True, text=True).stdout.strip()
        os.replace(out, bk); print('backup of the previous prompt beside it:', bk)
open(out, 'w', encoding='utf-8').write(s)
b = s.encode('utf-8')
print('written', out); print('lines', s.count('\n'), 'bytes', len(b), 'sha256', hashlib.sha256(b).hexdigest())
print('report dir named in the prompt:', re.search(r'reports/(2026-09-21-batch1130-\d+-tier1-r1)/', s).group(1))
print('verdict subject prefix:', re.search(r'^\[QA -> Wednesday\] BATCH GATE [^\n]*?\) —', s, re.M).group(0))
