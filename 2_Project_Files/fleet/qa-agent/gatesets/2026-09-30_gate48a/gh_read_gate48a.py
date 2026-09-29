#!/usr/bin/env python3
"""gh_read_gate48a.py — REST GET only. (1) The kit PR #1354: title, body, head, base, mergeable, files (+/-), commits; writes gh_body_1354.md.
(2) THE CENSUS of every OTHER open PR: its file list against the kit's 2 paths, and its TITLE against the census keys (KS-470 / KS-1374 /
KS-1054, whole-key match: KS-470 does not match KS-4700). Every hit, and every client-human PR named in kit.json client_human_prs (Peter's
#1351/#1352/#1353), is read in full detail (author, created, head, base, files touching a kit path) — REPORTED for Wednesday; the drafter
sequences NOTHING. Writes gh_read_1.json. The token is read by name from the Secuura .env and never printed. Usage: gh_read_gate48a.py"""
import json, os, re, time, urllib.request, urllib.error, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
def get(u):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/' + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == 3: raise
            time.sleep(10)
def files(n):
    out = []; pg = 1
    while True:
        b = get('pulls/%s/files?per_page=100&page=%d' % (n, pg)); out += b
        if len(b) < 100: return out
        pg += 1
N = K['order'][0]; k = K['prs'][N]; paths = set(k['files']); keys = set(k['census_keys'])
out = {'read_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'prs': {}, 'census': {}}
p = get('pulls/' + N); t = 1
while p.get('mergeable') is None and t < 3: time.sleep(8); p = get('pulls/' + N); t += 1
fs = files(N); cs = [(c['sha'], c['commit']['message'].split('\n')[0]) for c in get('pulls/%s/commits?per_page=100' % N)]
out['prs'][N] = {'title': p['title'], 'state': p['state'], 'user': (p.get('user') or {}).get('login'), 'head': p['head']['sha'], 'branch': p['head']['ref'], 'base': p['base']['ref'],
                 'base_sha': p['base']['sha'], 'mergeable': p.get('mergeable'), 'mergeable_state': p.get('mergeable_state'), 'files': [(f['filename'], f['additions'], f['deletions'], f['status']) for f in fs],
                 'commits': cs, 'body': p.get('body') or ''}
open(os.path.join(G, 'gh_body_%s.md' % N), 'w', encoding='utf-8').write(p.get('body') or '')
print('#%s %s | by %s | head %s | branch %s | base %s @ %s | mergeable %s (%s) | %d files | %d commits | title %d chars: %s' % (
    N, p['state'], (p.get('user') or {}).get('login'), p['head']['sha'], p['head']['ref'], p['base']['ref'], p['base']['sha'][:12], p.get('mergeable'), p.get('mergeable_state'), len(fs), len(cs), len(p['title']), p['title']))
for f in fs: print('   file %s +%d/-%d %s' % (f['filename'], f['additions'], f['deletions'], f['status']))
for c in cs: print('   commit %s %s' % c)
op = []; pg = 1
while True:
    b = get('pulls?state=open&per_page=100&page=%d' % pg); op += b
    if len(b) < 100: break
    pg += 1
hits = 0; other = 0
for x in op:
    n = str(x['number'])
    if n == N: continue
    other += 1
    ff = [f['filename'] for f in files(n)]; ov = sorted(set(ff) & paths); tk = sorted(set(re.findall(r'\bKS-\d+\b', x['title'])) & keys)
    human = n in K.get('client_human_prs', [])
    rec = {'title': x['title'], 'user': (x.get('user') or {}).get('login'), 'created_at': x.get('created_at'), 'head': x['head']['sha'], 'branch': x['head']['ref'],
           'base': x['base']['ref'], 'n_files': len(ff), 'kit_paths_touched': ov, 'census_keys_in_title': tk, 'client_human': human}
    out['census'][n] = rec
    if ov or tk:
        hits += 1; print('OVERLAP #%s by %s | %s | head %s | %d files | kit paths %s | title keys %s%s' % (n, rec['user'], x['title'][:90], x['head']['sha'][:12], len(ff), ov, tk, ' | CLIENT HUMAN: REPORT for Wednesday, sequence nothing' if human else ''))
    elif human: print('CLIENT-HUMAN #%s by %s | %s | head %s | %d files | created %s | touches no kit path, no census key' % (n, rec['user'], x['title'][:90], x['head']['sha'][:12], len(ff), rec['created_at']))
json.dump(out, open(os.path.join(G, 'gh_read_1.json'), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d touch a kit path or carry a census key %s | client-human PRs named: %s' % (other, hits, sorted(keys), K.get('client_human_prs')))
print('GH READ OK at %s' % out['read_at'])
