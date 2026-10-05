#!/usr/bin/env python3
"""gh_census_gate56a.py — read-only GitHub REST GETs for the gate56a launch action (a NEW COPY of gh_census_gate55.py, re-keyed for the
TWO re-date PRs). GH_TOKEN is read BY NAME from the Secuura .env and never printed; --offline-dir replays SIM fixtures with no network.
  --pr <n>   prints `API #<n> head <sha> base <ref> base_sha <sha> mergeable <v> reads <k> state <s> merged <b> branch <ref>` and a title line;
             --body-out <file> saves that PR's body (C1 / C5 read it). Run once per PR.
  CENSUS over every OTHER open PR (--exclude n3,n4 names the gate's own two): its files against the kit's TWO paths, its title against
  kit census_keys (KS-528, KS-769). Classes:
    OVERLAP   touches audit-baseline.json or lock-discovery.mjs (any title) — the launch action refuses rc 15 (e.g. KS 528's v7 migration
              removing the react-router rows would collide with PR 3: Wednesday sequences it).
    SAME-KEY  carries KS-528 or KS-769 in its title but touches neither kit path — REPORTED, never refused (the v7 migration lane).
  --json <file> saves the raw census rows (the caller names the path; this tool never writes into the kit dir).
Usage: gh_census_gate56a.py [--pr n] [--body-out f] [--exclude n3,n4] [--json out.json] [--offline-dir d]    rc 0 read OK / 3 API failure"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate56a import K, GH, opt_factory

A = sys.argv[1:]
if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
opt = opt_factory(A)
PR = opt('--pr'); OFF = opt('--offline-dir'); EX = set(x for x in (opt('--exclude') or '').split(',') if x)
for x in ([PR] if PR else []) + sorted(EX):
    if not re.fullmatch(r'\d+', x): print('REFUSING: PR numbers must be digits, got %r' % x); raise SystemExit(2)
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
    EX.add(PR)
paths = set(q['path'] for q in K['prs'].values()); keys = set(K['census_keys'])
rows = []; hits = same = 0
for x in gh.pages('pulls?state=open'):
    n = str(x['number'])
    if n in EX: continue
    fs = set(f['filename'] for f in gh.pages('pulls/%s/files' % n)); ov = sorted(fs & paths)
    tk = sorted(set(re.findall(r'\bKS-\d+\b', x['title'])) & keys); who = (x.get('user') or {}).get('login')
    cls = 'OVERLAP' if ov else ('SAME-KEY' if tk else None)
    rows.append({'number': n, 'user': who, 'head': x['head']['sha'], 'branch': x['head']['ref'], 'title': x['title'], 'overlap_paths': ov, 'title_keys': tk, 'class': cls, 'files': len(fs)})
    if cls == 'OVERLAP':
        hits += 1; print('OVERLAP #%s %s | %s | %s | kit paths %s | title keys %s' % (n, who, x['head']['ref'][:60], x['title'][:80], ov, tk))
    elif cls == 'SAME-KEY':
        same += 1; print('SAME-KEY (reported, never refused) #%s %s | %s | %s | %d file(s), no kit path' % (n, who, x['head']['ref'][:60], x['title'][:80], len(fs)))
if opt('--json'): json.dump(rows, open(opt('--json'), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d OVERLAP (touch a kit path) | %d SAME-KEY (%s in the title, no kit path) | excluded %s' % (len(rows), hits, same, sorted(keys), sorted(EX)))
