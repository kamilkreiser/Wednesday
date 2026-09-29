#!/usr/bin/env python3
"""gh_read_overlap_gate47.py — REST GET only: every OPEN PR outside the kit whose file list touches one of the kit's 6 paths or whose title carries
KS-1374 / KS-1054 (the launch action's rc-15 census, re-read with full detail): number, title, state, author, created_at, head sha + branch,
base, mergeable, files, commits, body. Writes gh_read_overlap.json and gh_body_<n>.md beside this script. Found by the controls' R-series
at 2026-09-29T14:4xZ (#1351 opened while the controls ran). The token is read by name from the Secuura .env and never printed.
Usage: gh_read_overlap_gate47.py"""
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
kit = set(K['order']); paths = set(p for n in K['order'] for p in K['prs'][n]['files']); keys = set(k for n in K['order'] for k in K['prs'][n]['keys'])
out = {'read_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'hits': {}}
opened = get('pulls?state=open&per_page=100'); n_other = 0
for x in opened:
    if str(x['number']) in kit: continue
    n_other += 1
    fs = [f['filename'] for f in get('pulls/%s/files?per_page=100' % x['number'])]
    ov = sorted(set(fs) & paths); tk = sorted(set(re.findall(r'KS-\d+', x['title'])) & keys)
    if not (ov or tk): continue
    n = str(x['number']); p = get('pulls/' + n); t = 1
    while p.get('mergeable') is None and t < 3: time.sleep(8); p = get('pulls/' + n); t += 1
    cs = [(c['sha'], c['commit']['message'].split('\n')[0]) for c in get('pulls/%s/commits?per_page=100' % n)]
    out['hits'][n] = {'title': p['title'], 'state': p['state'], 'user': (p.get('user') or {}).get('login'), 'created_at': p.get('created_at'), 'head': p['head']['sha'],
                      'branch': p['head']['ref'], 'base': p['base']['ref'], 'mergeable': p.get('mergeable'), 'mergeable_state': p.get('mergeable_state'),
                      'files': fs, 'kit_paths_touched': ov, 'kit_keys_in_title': tk, 'commits': cs}
    open(os.path.join(G, 'gh_body_%s.md' % n), 'w', encoding='utf-8').write(p.get('body') or '')
    print('#%s %s | by %s | created %s | head %s | branch %s | base %s | mergeable %s (%s) | %d files | %d commits | title: %s' % (
        n, p['state'], (p.get('user') or {}).get('login'), p.get('created_at'), p['head']['sha'], p['head']['ref'], p['base']['ref'], p.get('mergeable'), p.get('mergeable_state'), len(fs), len(cs), p['title']))
    print('   KIT PATHS TOUCHED %s | kit keys in title %s' % (ov, tk))
    for f in fs: print('   file %s%s' % (f, '   <== KIT PATH' if f in paths else ''))
    for c in cs: print('   commit %s %s' % (c[0], c[1]))
json.dump(out, open(os.path.join(G, 'gh_read_overlap.json'), 'w'), indent=1)
print('OVERLAP READ at %s: %d other open PR(s) read, %d touch a kit path or carry a kit key: %s' % (out['read_at'], n_other, len(out['hits']), ' '.join('#' + h for h in out['hits']) or 'none'))
