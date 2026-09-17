#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub reads for the #1017 (KS-1195) tier-1 ROUND 2 set. Derived from the round-1 set's gh_read.py. GH_TOKEN by NAME from the Secuura
.env; never printed. GET only. PR, files, commits, compare develop...head, closing-phrase scan (planted controls), KS-1187 count (control), the "Round 2" section,
deploy-precondition lines and whether they name F-1, unfilled template placeholders ({{...}}, control planted), issue comments, reviews, develop tip, open-PR
exact overlap."""
import json, os, re, urllib.request, urllib.error, subprocess
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017r2'
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(name, obj): open(os.path.join(G, 'gh', name), 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
H = 'a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66'
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?)\b[:\s]+(?:KS-[0-9]+|#[0-9]+)')
ctl = {'Fixes KS-1195': len(CLOSE.findall('Fixes KS-1195')), 'closes #12': len(CLOSE.findall('closes #12')), 'Refs KS-1195': len(CLOSE.findall('Refs KS-1195'))}
print('gh_read', now(), '| closing regex controls', ctl)
assert ctl == {'Fixes KS-1195': 1, 'closes #12': 1, 'Refs KS-1195': 0}
K1187 = re.compile(r'KS-1187(?![0-9])'); assert len(K1187.findall('x KS-1187 y KS-11870')) == 1
PH = re.compile(r'\{\{[A-Z_]+\}\}'); assert len(PH.findall('a {{PUSH}} b {PUSH} c')) == 1
DEPLOY = re.compile(r'(?i)deploy'); UNMEAS = re.compile(r'(?i)unmeasured')
pr = get('/pulls/1017'); save('pr1017.json', pr)
print('PR #1017', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], '| head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  head == pin:', pr['head']['sha'] == H, '| title:', pr['title'], '| title closing', CLOSE.findall(pr['title']))
print('  mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'], '| updated_at', pr['updated_at'])
body = pr.get('body') or ''
open(os.path.join(G, 'gh', 'pr1017_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), 'at-signs', body.count('@'), 'closing', CLOSE.findall(body), '| Refs KS-1195', body.count('Refs KS-1195'), '| KS-1187', len(K1187.findall(body + pr['title'])))
print('  "## Round 2" heading lines:', sum(1 for l in body.splitlines() if l.strip().lower().startswith('## round 2')), '| control "## " headings:', sum(1 for l in body.splitlines() if l.startswith('## ')))
print('  unfilled {{PLACEHOLDER}} tokens:', PH.findall(body))
dl = [l.strip()[:260] for l in body.splitlines() if DEPLOY.search(l) and UNMEAS.search(l)]
print('  deploy-precondition lines (deploy AND unmeasured):', len(dl), '| of them naming F-1:', sum(1 for x in dl if 'F-1' in x)); [print('    >', x) for x in dl]
print('  lines naming "a067d4e3e":', sum(1 for l in body.splitlines() if 'a067d4e3e' in l), '| lines naming G-BUCKET:', sum(1 for l in body.splitlines() if 'G-BUCKET' in l))
files = get('/pulls/1017/files?per_page=100'); save('pr1017_files.json', files)
for f in files: print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
commits = get('/pulls/1017/commits?per_page=100'); save('pr1017_commits.json', commits)
for c in commits: print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], 'closing', CLOSE.findall(c['commit']['message']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', c['commit']['message']))), 'KS-1187', len(K1187.findall(c['commit']['message'])), '|', c['commit']['message'].split('\n')[0][:120])
c = get('/compare/develop...' + H); save('compare_develop_head.json', c)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/1017/reviews')), '| review comments', len(get('/pulls/1017/comments')))
ics = get('/issues/1017/comments?per_page=100'); save('pr1017_issue_comments.json', ics)
for x in ics: print('  issue comment', x['id'], x['user']['login'], x['created_at'], 'chars', len(x['body']), 'closing', CLOSE.findall(x['body']), 'KS-1187', len(K1187.findall(x['body'])), 'at-signs', x['body'].count('@'))
dev = get('/branches/develop')['commit']['sha']; print('  develop (branches API)', dev)
opn = get('/pulls?state=open&per_page=100'); print('  open PRs:', len(opn))
mine = {f['filename'] for f in files}
for p in opn:
    if p['number'] == 1017: continue
    names = [f['filename'] for f in get('/pulls/%d/files?per_page=100' % p['number'])]
    ex = sorted(mine & set(names))
    if ex or p['number'] in (1018, 1019): print('  open #%d head %s files %d | exact shared with #1017 %s | %s' % (p['number'], p['head']['sha'][:9], len(names), ex, p['title'][:70]))
print('  (open PRs with 0 exact shared files and not #1018/#1019 are not printed)')
print('gh_read end', now('+%H:%M:%S %Z'))
