#!/usr/bin/env python3
"""gh_census_gate58.py — read-only GitHub REST GETs for the gate58 launch action (a NEW COPY of gate54f's census (itself gate52's step-2 heredoc), so it can
run standalone). GH_TOKEN is read BY NAME from the Secuura .env and never printed.
  --pr <n>   also prints `API #<n> head <sha> base <ref> base_sha <sha> mergeable <v> reads <k> state <s> merged <b> branch <ref>` (mergeable
             re-read up to 3x while null) — the launch action's second instrument.
  CENSUS: every OTHER open PR's file list (paged) against the kit's 7 paths, and its title against kit census_keys (whole key). A hit outside
  kit.json reported_overlaps prints `OVERLAP ...` (the launch action refuses rc 15 on one); a hit recorded there prints `EXPECTED OVERLAP`
  (with HEAD MOVED when its head is not the drafted one); a kit client-human PR is always REPORTED by name. --json <file> saves the raw census.
Usage: gh_census_gate58.py [--pr n] [--json out.json]    rc 0 read OK / rc 3 API failure"""
import json, os, re, sys, time, urllib.request, urllib.error
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]
if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
PR = opt('--pr')
tok = ''
for l in open(K['secuura_env'], encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
if not tok: print('REFUSING: GH_TOKEN unset'); raise SystemExit(3)
def get(u):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], u),
                headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == 3: print('API %s HTTP %d' % (u, e.code)); raise SystemExit(3)
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:   # gate53's fix: a dropped connection is retried, not fatal
            if i == 3: print('API %s unreachable: %s' % (u, e)); raise SystemExit(3)
            print('RETRY %s: %s' % (u, e), file=sys.stderr)
        time.sleep(10)
def pages(u):
    out = []; pg = 1
    while True:
        b = get('%s%sper_page=100&page=%d' % (u, '&' if '?' in u else '?', pg)); out += b
        if len(b) < 100: return out
        pg += 1
if PR:
    p = get('pulls/' + PR); tries = 1
    while p.get('mergeable') is None and tries < 3: time.sleep(10); p = get('pulls/' + PR); tries += 1
    print('API #%s head %s base %s base_sha %s mergeable %s reads %d state %s merged %s branch %s' % (
        PR, p['head']['sha'], p['base']['ref'], p['base']['sha'], p.get('mergeable'), tries, p['state'], p.get('merged'), p['head']['ref']))
paths = set(K['files']); keys = set(K['census_keys']); RO = K.get('reported_overlaps') or {}; HUM = set(K.get('client_human_prs', []))
if os.environ.get('G58_OVERLAP_EXTRA'): paths.add(os.environ['G58_OVERLAP_EXTRA'])
if os.environ.get('G58_REPORTED'): RO = json.load(open(os.environ['G58_REPORTED']))
rows = []; hits = expd = hum = 0
for x in pages('pulls?state=open'):
    n = str(x['number'])
    if n == PR: continue
    fs = set(f['filename'] for f in pages('pulls/%s/files' % n)); ov = sorted(fs & paths); tk = sorted(set(re.findall(r'\bKS-\d+\b', x['title'])) & keys)
    who = (x.get('user') or {}).get('login'); ro = RO.get(n)
    rows.append({'number': n, 'user': who, 'head': x['head']['sha'], 'branch': x['head']['ref'], 'title': x['title'], 'overlap_paths': ov, 'title_keys': tk, 'files': len(fs)})
    if (ov or tk) and ro:
        expd += 1; print('EXPECTED OVERLAP (reported_overlaps; reported, never sequenced by a gate) #%s %s | head %s%s | paths %s | title keys %s' % (
            n, who, x['head']['sha'][:12], '' if ro.get('head') == x['head']['sha'] else ' (HEAD MOVED since drafting: was %s)' % str(ro.get('head'))[:12], ov, tk))
    elif ov or tk:
        hits += 1; print('OVERLAP #%s %s | %s | %s | paths %s | title keys %s' % (n, who, x['head']['ref'][:60], x['title'][:80], ov, tk))
    if n in HUM and not (ov or tk): hum += 1; print('CLIENT-HUMAN (reported, never sequenced by a gate) #%s by %s | head %s | %d file(s), none a kit path' % (n, who, x['head']['sha'][:12], len(fs)))
if opt('--json'): json.dump(rows, open(opt('--json'), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d touch a kit path or carry a kit key outside reported_overlaps | %d expected overlap(s) reported | %d client-human PR(s) reported apart | %d kit path(s), keys %s' % (
    len(rows), hits, expd, hum, len(paths), sorted(keys)))
