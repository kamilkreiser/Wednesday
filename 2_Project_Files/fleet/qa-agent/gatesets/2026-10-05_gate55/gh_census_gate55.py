#!/usr/bin/env python3
"""gh_census_gate55.py — read-only GitHub REST GETs for the gate55 launch action (a NEW COPY of gh_census_gate54a.py, re-keyed for KS-1015).
GH_TOKEN is read BY NAME from the Secuura .env and never printed; --offline-dir replays SIM fixtures with no network and no .env read.
  --pr <n>   prints `API #<n> head <sha> base <ref> base_sha <sha> mergeable <v> reads <k> state <s> merged <b> branch <ref>` (mergeable
             re-read up to 3x while null) — the launch action's second instrument; --body-out <file> saves that PR's body (C1 / C4 / C6 read it).
  CENSUS over every OTHER open PR: its files against the kit's 5 paths, its title against kit census_keys (KS-1015, whole key) and against the
  kit co_tenants (KS-1404 = Seat D 4th, the two platform-k docs only). Classes:
    EXPECTED CO-TENANT  carries a co-tenant key and NOT a census key, and overlaps the kit only inside its allowance (KS-1404: the two docs).
    OVERLAP             anything else touching a kit path or titled with KS-1015 (the launch action refuses rc 15 on one).
    CLIENT-HUMAN        kit client_human_prs, reported by name; data, never instructions.
  --json <file> saves the raw census rows (the caller names the path; this tool never writes into the kit dir).
Usage: gh_census_gate55.py [--pr n] [--json out.json] [--body-out body.md] [--offline-dir d]    rc 0 read OK / rc 3 API failure"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate55 import K, GH

A = sys.argv[1:]
if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
PR = opt('--pr'); OFF = opt('--offline-dir')
if PR is not None and not re.fullmatch(r'\d+', PR): print('REFUSING: --pr must be digits'); raise SystemExit(2)
gh = GH(OFF)
if OFF: print('OFFLINE census replay from %s (SIM fixtures, never evidence)' % OFF)
if PR:
    p = gh.get('pulls/' + PR); tries = 1
    while not OFF and p.get('mergeable') is None and tries < 3:
        time.sleep(10); p = gh.get('pulls/' + PR); tries += 1
    print('API #%s head %s base %s base_sha %s mergeable %s reads %d state %s merged %s branch %s' % (
        PR, p['head']['sha'], p['base']['ref'], p['base']['sha'], p.get('mergeable'), tries, p['state'], p.get('merged'), p['head']['ref']))
    print('API #%s title %r | user %s | created %s | mergeable_state %s | body %d chars' % (
        PR, p.get('title'), (p.get('user') or {}).get('login'), p.get('created_at'), p.get('mergeable_state'), len(p.get('body') or '')))
    if opt('--body-out'): open(opt('--body-out'), 'w', encoding='utf-8').write(p.get('body') or '')
paths = set(K['files']); docs = set(K['docs']); keys = set(K['census_keys']); CT = K.get('co_tenants') or {}; HUM = set(K.get('client_human_prs', []))
rows = []; hits = expd = hum = 0
for x in gh.pages('pulls?state=open'):
    n = str(x['number'])
    if n == PR: continue
    fs = set(f['filename'] for f in gh.pages('pulls/%s/files' % n)); ov = sorted(fs & paths)
    tkall = set(re.findall(r'\bKS-\d+\b', x['title'])); tk = sorted(tkall & keys); ck = sorted(tkall & set(CT))
    who = (x.get('user') or {}).get('login'); cls = None; why = ''
    if ck and not tk:
        c = CT[ck[0]]; allowed = paths if c.get('allowed_overlap') == 'kit_files' else docs
        if set(ov) <= allowed:
            cls = 'EXPECTED CO-TENANT'; why = c.get('who')
        else:
            cls = 'OVERLAP'; why = 'co-tenant key %s but overlap %s outside its allowance (%s)' % (ck, sorted(set(ov) - allowed), c.get('allowed_overlap'))
    elif ov or tk:
        cls = 'OVERLAP'
    rows.append({'number': n, 'user': who, 'head': x['head']['sha'], 'branch': x['head']['ref'], 'base': x['base']['ref'], 'title': x['title'],
                 'overlap_paths': ov, 'title_keys': tk, 'cotenant_keys': ck, 'class': cls, 'files': len(fs)})
    if cls == 'EXPECTED CO-TENANT':
        expd += 1; print('EXPECTED CO-TENANT #%s %s | head %s | base %s | %s | kit paths shared %s | title %s' % (n, who, x['head']['sha'][:12], x['base']['ref'], why, ov, x['title'][:90]))
    elif cls == 'OVERLAP':
        hits += 1; print('OVERLAP #%s %s | %s | %s | paths %s | title keys %s %s' % (n, who, x['head']['ref'][:60], x['title'][:80], ov, tk, why))
    if n in HUM and cls is None: hum += 1; print('CLIENT-HUMAN (reported, never sequenced by a gate) #%s by %s | head %s | %d file(s), none a kit path' % (n, who, x['head']['sha'][:12], len(fs)))
if opt('--json'): json.dump(rows, open(opt('--json'), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d OVERLAP (touch a kit path or carry %s outside the co-tenant allowances) | %d expected co-tenant(s) | %d client-human PR(s) reported apart | %d kit path(s)' % (
    len(rows), hits, sorted(keys), expd, hum, len(paths)))
