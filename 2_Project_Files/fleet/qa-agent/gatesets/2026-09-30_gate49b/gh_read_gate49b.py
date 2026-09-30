#!/usr/bin/env python3
"""gh_read_gate49b.py — REST GET only. (1) EACH kit PR (kit.json order): title, body, head, base, mergeable, files (+/-), commits (subject + full
message); writes gh_body_<n>.md per PR. (2) THE CENSUS of every OTHER open PR: its file list (paged) against the UNION of the kit's paths, and its
TITLE against the union of census keys (whole-key: KS-1054 does not match KS-10540). Every hit, every client-human PR (kit.json client_human_prs)
and every seat-branch PR (kit.json widen_branch_rx) is printed with author, head and the kit paths it touches — REPORTED for Wednesday; the drafter
sequences NOTHING. Each hit is marked IN reported_overlaps (kit.json) or NOT. (3) OUT OF SCOPE items (kit.json out_of_scope): an open PR on a
branch matching the item's branch_rx is REPORTED (it is not in this batch by Wednesday's ruling). Writes gh_read_1.json. The token is read by name
from the Secuura .env and never printed. Usage: gh_read_gate49b.py"""
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
ORDER = K['order']; kit = set(ORDER)
paths = set(p for n in ORDER for p in K['prs'][n]['files']); keys = set(k for n in ORDER for k in K['prs'][n]['census_keys'])
owner = {p: n for n in ORDER for p in K['prs'][n]['files']}
AU = K.get('post_merge_audit') or {}; apaths = set(AU.get('files', [])); akeys = set(AU.get('census_keys', [])); out_a = {}
out = {'read_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'prs': {}, 'census': {}, 'out_of_scope': {}}
bad = []
for N in ORDER:
    p = get('pulls/' + N); t = 1
    while p.get('mergeable') is None and t < 3: time.sleep(8); p = get('pulls/' + N); t += 1
    fs = files(N); cs = [(c['sha'], c['commit']['message']) for c in get('pulls/%s/commits?per_page=100' % N)]
    out['prs'][N] = {'title': p['title'], 'state': p['state'], 'user': (p.get('user') or {}).get('login'), 'head': p['head']['sha'], 'branch': p['head']['ref'], 'base': p['base']['ref'],
                     'base_sha': p['base']['sha'], 'mergeable': p.get('mergeable'), 'mergeable_state': p.get('mergeable_state'), 'files': [(f['filename'], f['additions'], f['deletions'], f['status']) for f in fs],
                     'commits': cs, 'body': p.get('body') or ''}
    open(os.path.join(G, 'gh_body_%s.md' % N), 'w', encoding='utf-8').write(p.get('body') or '')
    print('#%s %s | by %s | head %s | branch %s | base %s @ %s | mergeable %s (%s) | %d files +%d/-%d | %d commit(s) | title %d chars (lands %d): %s' % (
        N, p['state'], (p.get('user') or {}).get('login'), p['head']['sha'], p['head']['ref'], p['base']['ref'], p['base']['sha'][:12], p.get('mergeable'), p.get('mergeable_state'),
        len(fs), sum(f['additions'] for f in fs), sum(f['deletions'] for f in fs), len(cs), len(p['title']), len(p['title']) + len(' (#%s)' % N), p['title']))
    for f in fs: print('   file %s +%d/-%d %s' % (f['filename'], f['additions'], f['deletions'], f['status']))
    for c in cs: print('   commit %s %s' % (c[0], c[1].split('\n')[0]))
    if p['head']['sha'] != K['prs'][N]['head']: bad.append('#%s API head %s != kit.json head %s' % (N, p['head']['sha'], K['prs'][N]['head']))
    if sorted(f['filename'] for f in fs) != sorted(K['prs'][N]['files']): bad.append('#%s API file list != kit.json files' % N)
    if p['state'] != 'open' or p['base']['ref'] != 'develop': bad.append('#%s is not open on develop' % N)
op = []; pg = 1
while True:
    b = get('pulls?state=open&per_page=100&page=%d' % pg); op += b
    if len(b) < 100: break
    pg += 1
hits = 0; other = 0; wide = 0; oos = 0
for x in op:
    n = str(x['number'])
    if n in kit: continue
    other += 1
    ff = [f['filename'] for f in files(n)]; ov = sorted(set(ff) & paths); tk = sorted(set(re.findall(r'\bKS-\d+\b', x['title'])) & keys)
    human = n in K.get('client_human_prs', []); wb = bool(re.search(K['widen_branch_rx'], x['head']['ref']))
    rec = {'title': x['title'], 'user': (x.get('user') or {}).get('login'), 'created_at': x.get('created_at'), 'head': x['head']['sha'], 'branch': x['head']['ref'],
           'base': x['base']['ref'], 'n_files': len(ff), 'kit_paths_touched': ov, 'kit_prs_touched': sorted(set(owner[q] for q in ov)), 'census_keys_in_title': tk, 'client_human': human}
    out['census'][n] = rec
    for item, v in (K.get('out_of_scope') or {}).items():
        if re.search(v['branch_rx'], x['head']['ref']):
            oos += 1; out['out_of_scope'][item] = {'pr': n, 'head': x['head']['sha'], 'branch': x['head']['ref']}
            print('OUT-OF-SCOPE #%s %s | %s | head %s — %s is NOT in this batch (Wednesday\'s ruling); reported only' % (n, x['head']['ref'], x['title'][:80], x['head']['sha'][:12], item))
    if ov or tk:
        hits += 1; ro = (K.get('reported_overlaps') or {}).get(n)
        tag = ('IN reported_overlaps, drafted head %s%s' % (ro['head'][:12], '' if ro['head'] == x['head']['sha'] else ' (HEAD MOVED)')) if ro else 'NOT in reported_overlaps'
        print('OVERLAP #%s by %s | %s | branch %s | head %s | %d files | kit paths %s (kit PR(s) %s) | title keys %s | %s%s' % (n, rec['user'], x['title'][:90], x['head']['ref'][:60], x['head']['sha'], len(ff), ov, rec['kit_prs_touched'], tk, tag, ' | CLIENT HUMAN: REPORT for Wednesday, sequence nothing' if human else ''))
    ao = sorted(set(ff) & apaths); ak = sorted(set(re.findall(r'\bKS-\d+\b', x['title'])) & akeys)
    if ao or ak:
        out_a[n] = dict(rec, audit_paths_touched=ao, audit_keys_in_title=ak)
        print('AUDIT-OVERLAP (#%s post-merge audit; reported, never refusing) #%s by %s | %s | head %s | audit paths %s | title keys %s' % (AU['pr'], n, rec['user'], x['title'][:80], x['head']['sha'][:12], ao, ak))
    if (ov or tk): pass
    elif human: print('CLIENT-HUMAN #%s by %s | %s | head %s | %d files | created %s | touches no kit path, no census key' % (n, rec['user'], x['title'][:90], x['head']['sha'][:12], len(ff), rec['created_at']))
    elif wb: wide += 1; print('DISJOINT OUT-OF-KIT #%s %s | %s | %d file(s), none a kit path' % (n, x['head']['ref'][:70], x['title'][:90], len(ff)))
for item in (K.get('out_of_scope') or {}):
    if item not in out['out_of_scope']: print('OUT-OF-SCOPE %s: no open PR on a matching branch at %s (by Wednesday\'s ruling it is not in this batch either way)' % (item, out['read_at']))
out['audit_census'] = out_a
json.dump(out, open(os.path.join(G, 'gh_read_1.json'), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d touch a kit path or carry a census key %s | %d seat-branch PR(s) disjoint | %d out-of-scope PR(s) | client-human PRs named: %s | %d kit paths | %d AUDIT-OVERLAP PR(s) on #%s\'s %d locks' % (
    other, hits, sorted(keys), wide, oos, K.get('client_human_prs'), len(paths), len(out_a), AU.get('pr'), len(apaths)))
for b in bad: print('PROBLEM: ' + b)
print('GH READ %s at %s' % ('OK' if not bad else 'FAILED', out['read_at']))
raise SystemExit(1 if bad else 0)
