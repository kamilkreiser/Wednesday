#!/usr/bin/env python3
"""pinpr_gate49a.py — the ONE step that turns the unpinned gate49a kit into a pinned one. Given the PR number and the head Wednesday names:
  P1 `git ls-remote origin refs/pull/<PR>/head` (from the Secuura checkout, READ-ONLY) == <HEAD> (whole-field);
  P2 the PULLS API (REST GET, GH_TOKEN read by NAME from the Secuura .env, never printed): state open, base develop, head.sha == <HEAD>;
     the branch name is taken from the API (`head.ref`) — never typed;
  P3 `git ls-remote origin refs/heads/<branch>` == <HEAD> (the branch AND pull/head agree);
  P4 the PR's /files (paged) == kit.json prs.<PR>.files as a SET (the 18 locks; the drafter's list) — a mismatch is REPORTED and REFUSED (rc 1):
     a different file set is a different PR and a re-draft, not a pin.
Then it keeps the unpinned kit as kit.json.pre-pin-<HHMMSS> (never deleted) and writes kit.json with every `<PR>` / `<HEAD>` / `<BRANCH>`
replaced; refuses if any placeholder remains or if the kit is already pinned. Writes nothing else.
--check: P1-P4 only, no write. Usage: pinpr_gate49a.py <PR> <HEAD> [--check]"""
import json, os, re, subprocess, sys, datetime, shutil, urllib.request
G = os.path.dirname(os.path.abspath(__file__)); KP = os.path.join(G, 'kit.json'); raw = open(KP, encoding='utf-8').read(); K = json.loads(raw)
A = sys.argv[1:]
if len(A) < 2 or not re.fullmatch(r'\d+', A[0]) or not re.fullmatch(r'[0-9a-f]{40}', A[1]): raise SystemExit('usage: pinpr_gate49a.py <PR number> <40-hex head> [--check]')
N, H = A[0], A[1]; CHECK = '--check' in A
if '<PR>' not in raw: raise SystemExit('REFUSING: kit.json is already pinned (no <PR> placeholder) — a new head is a re-draft (README section 9)')
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
if not tok: raise SystemExit('REFUSING: GH_TOKEN unset in the Secuura .env')
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/' + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def lsr(*refs):
    r = subprocess.run(['git', '-C', K['checkout'], 'ls-remote', 'origin'] + list(refs), capture_output=True, text=True)
    if r.returncode: raise SystemExit('REFUSING: ls-remote rc %d: %s' % (r.returncode, r.stderr.strip()[:200]))
    return {l.split('\t')[1]: l.split('\t')[0] for l in r.stdout.splitlines() if '\t' in l}
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
bad = []
R = lsr('refs/pull/%s/head' % N, 'refs/heads/develop')
ph = R.get('refs/pull/%s/head' % N)
print('pinpr_gate49a %s | PR #%s | named head %s' % (now, N, H))
print('P1 ls-remote refs/pull/%s/head %s | == named: %s | develop %s' % (N, ph, ph == H, R.get('refs/heads/develop')))
if ph != H: bad.append('P1 refs/pull/%s/head is %s, not the named head' % (N, ph))
p = get('pulls/' + N); br = p['head']['ref']
print('P2 API #%s state %s | base %s | head %s | branch %s | title %d chars: %s' % (N, p['state'], p['base']['ref'], p['head']['sha'], br, len(p['title']), p['title']))
if p['state'] != 'open' or p['base']['ref'] != 'develop' or p['head']['sha'] != H: bad.append('P2 the API does not read an OPEN PR on develop at the named head')
bh = lsr('refs/heads/' + br).get('refs/heads/' + br)
print('P3 ls-remote refs/heads/%s %s | == named: %s' % (br, bh, bh == H))
if bh != H: bad.append('P3 the branch head %s != the named head' % bh)
fs = []; pg = 1
while True:
    b = get('pulls/%s/files?per_page=100&page=%d' % (N, pg)); fs += b
    if len(b) < 100: break
    pg += 1
got = sorted(f['filename'] for f in fs); want = sorted(K['prs']['<PR>']['files'])
print('P4 PR files %d (+%d/-%d) | == the kit\'s 18: %s%s' % (len(got), sum(f['additions'] for f in fs), sum(f['deletions'] for f in fs), got == want,
      '' if got == want else ' | extra %s | missing %s' % (sorted(set(got) - set(want)), sorted(set(want) - set(got)))))
if got != want: bad.append('P4 the PR file set differs from the kit\'s 18 locks')
if bad:
    print('REFUSED: %d problem(s):' % len(bad)); [print('  - ' + x) for x in bad]; raise SystemExit(1)
if CHECK: print('PINPR CHECK OK (no write)'); raise SystemExit(0)
bk = os.path.join(G, 'kit.json.pre-pin-' + datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S')); shutil.copy2(KP, bk)
new = raw.replace('<PR>', N).replace('<HEAD>', H).replace('<BRANCH>', 'refs/heads/' + br)
J = json.loads(new); J['placeholders'] = []; J['placeholders_note'] = 'PINNED by pinpr_gate49a.py at %s; the unpinned kit is %s' % (now, os.path.basename(bk));J['pinned'] = {'at': now, 'pr': N, 'head': H, 'branch': 'refs/heads/' + br, 'title_at_pin': p['title'], 'unpinned_copy': os.path.basename(bk)}
out = json.dumps(J, indent=1)
if any(x in out for x in ('<PR>', '<HEAD>', '<BRANCH>')): raise SystemExit('REFUSING: a placeholder survived the substitution (kept %s)' % bk)
open(KP, 'w', encoding='utf-8').write(out)
print('PINPR OK: kit.json pinned to #%s at %s (%s); unpinned copy kept as %s' % (N, H, br, os.path.basename(bk)))
