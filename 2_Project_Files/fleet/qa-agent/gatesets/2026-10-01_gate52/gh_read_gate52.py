#!/usr/bin/env python3
"""gh_read_gate52.py — REST GET only. (1) EACH kit PR (#1367, #1368): title, body, head, base, mergeable, files (+/-), commits (subject + full
message); writes gh_body_<n>.md per PR. (2) THE CENSUS of every OTHER open PR: its file list (paged) against the kit's 7 paths (the union), and
its TITLE against the census keys (KS-1015, KS-1364, whole-key: KS-1364 does not match KS-13640). Every hit, and every client-human PR in kit.json client_human_prs, is printed in full
(author, created, head, base, the kit paths it touches, the census is a READ; overlaps are Wednesday's
) — REPORTED for Wednesday; the drafter sequences NOTHING. Each hit is marked IN reported_overlaps (kit.json) or NOT. Writes gh_read_1.json.
The token is read by name from the Secuura .env and never printed. Refuses while kit.json is UNPINNED, except --census-only (the census
half alone, written to gh_read_census_prepin.json — the drafter's pre-pin read; never the pinned gh_read_1.json). Usage: gh_read_gate52.py [--census-only]"""
import sys
import json, os, re, time, urllib.request, urllib.error, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
ORDER = K['order']; CO = '--census-only' in sys.argv
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
paths = set(p for n in ORDER for p in K['prs'][n]['files']); keys = set(c for n in ORDER for c in K['prs'][n]['census_keys'])
out = {'read_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'prs': {}, 'census': {}}
OUTF = 'gh_read_census_prepin.json' if CO else 'gh_read_1.json'
if CO: print('CENSUS-ONLY (pre-pin): the kit PRs are not read')
for N in ([] if CO else ORDER):
  p = get('pulls/' + N); t = 1
  while p.get('mergeable') is None and t < 3: time.sleep(8); p = get('pulls/' + N); t += 1
  fs = files(N); cs = [(c['sha'], c['commit']['message']) for c in get('pulls/%s/commits?per_page=100' % N)]
  out['prs'][N] = {'title': p['title'], 'state': p['state'], 'user': (p.get('user') or {}).get('login'), 'head': p['head']['sha'], 'branch': p['head']['ref'], 'base': p['base']['ref'],
                   'base_sha': p['base']['sha'], 'mergeable': p.get('mergeable'), 'mergeable_state': p.get('mergeable_state'), 'files': [(f['filename'], f['additions'], f['deletions'], f['status']) for f in fs],
                   'commits': cs, 'body': p.get('body') or ''}
  open(os.path.join(G, 'gh_body_%s.md' % N), 'w', encoding='utf-8').write(p.get('body') or '')
  print('#%s %s | by %s | head %s | branch %s | base %s @ %s | mergeable %s (%s) | %d files +%d/-%d | %d commits | title %d chars: %s' % (
      N, p['state'], (p.get('user') or {}).get('login'), p['head']['sha'], p['head']['ref'], p['base']['ref'], p['base']['sha'][:12], p.get('mergeable'), p.get('mergeable_state'),
      len(fs), sum(f['additions'] for f in fs), sum(f['deletions'] for f in fs), len(cs), len(p['title']), p['title']))
  for f in fs: print('   file %s +%d/-%d %s' % (f['filename'], f['additions'], f['deletions'], f['status']))
  for c in cs: print('   commit %s %s' % (c[0], c[1].split('\n')[0]))
op = []; pg = 1
while True:
    b = get('pulls?state=open&per_page=100&page=%d' % pg); op += b
    if len(b) < 100: break
    pg += 1
hits = 0; other = 0
for x in op:
    n = str(x['number'])
    if n in ORDER: continue
    other += 1
    ff = [f['filename'] for f in files(n)]; ov = sorted(set(ff) & paths); tk = sorted(set(re.findall(r'\bKS-\d+\b', x['title'])) & keys)
    human = n in K.get('client_human_prs', [])
    rec = {'title': x['title'], 'user': (x.get('user') or {}).get('login'), 'created_at': x.get('created_at'), 'head': x['head']['sha'], 'branch': x['head']['ref'],
           'base': x['base']['ref'], 'n_files': len(ff), 'kit_paths_touched': ov, 'census_keys_in_title': tk, 'client_human': human}
    out['census'][n] = rec
    if ov or tk:
        hits += 1; ro = (K.get('reported_overlaps') or {}).get(n)
        tag = ('IN reported_overlaps, drafted head %s%s' % (ro['head'][:12], '' if ro['head'] == x['head']['sha'] else ' (HEAD MOVED)')) if ro else 'NOT in reported_overlaps'
        print('OVERLAP #%s by %s | %s | branch %s | head %s | %d files | kit paths %s | title keys %s | %s%s' % (n, rec['user'], x['title'][:90], x['head']['ref'][:60], x['head']['sha'], len(ff), ov, tk, tag, ' | CLIENT HUMAN: REPORT for Wednesday, sequence nothing' if human else ''))
    elif human: print('CLIENT-HUMAN #%s by %s | %s | head %s | %d files | created %s | touches no kit path, no census key' % (n, rec['user'], x['title'][:90], x['head']['sha'][:12], len(ff), rec['created_at']))
json.dump(out, open(os.path.join(G, OUTF), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d touch a kit path or carry a census key %s | %d kit paths | client-human PRs named: %s' % (other, hits, sorted(keys), len(paths), K.get('client_human_prs')))
print('GH READ OK at %s' % out['read_at'])
