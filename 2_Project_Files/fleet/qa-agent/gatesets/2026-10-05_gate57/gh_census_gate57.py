#!/usr/bin/env python3
"""gh_census_gate57.py — read-only GitHub REST GETs for the gate57 launch action (a NEW COPY of gh_census_gate56a.py, re-keyed for #1380 +
#1381). GH_TOKEN is read BY NAME from the Secuura .env and never printed; --offline-dir replays SIM fixtures with no network (never evidence).
  --pr <n>   prints `API #<n> head <sha> base <ref> base_sha <sha> mergeable <v> reads <k> state <s> merged <b> branch <ref>` and a title line;
             --body-out <file> saves that PR's body (C6 reads it with --body-file).
  --advance <develop sha>   compare kit cut_base...<develop>: prints `ADVANCE behind=<n> files=<n> overlap=<csv|NONE>` — a develop that moved
             since the PRs were cut is acceptable ONLY when no moved path is a kit path or under Projects Documents/ (the launch refuses rc 10).
  CENSUS over every OTHER open PR (--exclude n1,n2 names the gate's own): its files against kit all_paths + anything under
  `Projects Documents/` (the §4 tail-block collision class: every such PR CONFLICTS with these two at the docs' tail), its title against kit
  census_keys. Classes: OVERLAP (touches a kit path or a Projects Documents file) -> the launch refuses rc 15; SAME-KEY (KS-1333 / KS-1345
  in the title, no kit path) -> reported only.
Usage: gh_census_gate57.py [--pr n [--body-out f]] [--exclude n1,n2] [--advance sha] [--json out.json] [--offline-dir d]   rc 0 / 2 / 3"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate57 import K, GH, opt_factory

A = sys.argv[1:]
if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
opt = opt_factory(A)
PR = opt('--pr'); OFF = opt('--offline-dir'); EX = set(x for x in (opt('--exclude') or '').split(',') if x); ADV = opt('--advance')
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
    print('API #%s title %r | user %s | mergeable_state %s | body %d chars' % (PR, p.get('title'), (p.get('user') or {}).get('login'), p.get('mergeable_state'), len(p.get('body') or '')))
    if opt('--body-out'): open(opt('--body-out'), 'w', encoding='utf-8').write(p.get('body') or '')
    EX.add(PR)
if ADV:
    if not re.fullmatch(r'[0-9a-f]{40}', ADV): print('REFUSING: --advance needs a 40-hex sha'); raise SystemExit(2)
    if ADV == K['cut_base']:
        print('ADVANCE behind=0 files=0 overlap=NONE')
    else:
        c = gh.get('compare/%s...%s' % (K['cut_base'], ADV)); fs = sorted(f['filename'] for f in (c.get('files') or []))
        ov = [f for f in fs if f in K['all_paths'] or f.startswith('Projects Documents/')]
        print('ADVANCE behind=%d files=%d overlap=%s status=%s merge_base=%s' % (c.get('ahead_by', -1), len(fs), ','.join(ov) or 'NONE', c.get('status'), c['merge_base_commit']['sha']))
        for f in fs: print('ADVANCE-PATH %s' % f)
paths = set(K['all_paths']); keys = set(K['census_keys'])
rows = []; hits = same = expd = 0
for x in gh.pages('pulls?state=open'):
    n = str(x['number'])
    if n in EX: continue
    fs = set(f['filename'] for f in gh.pages('pulls/%s/files' % n)); ov = sorted(f for f in fs if f in paths or f.startswith('Projects Documents/'))
    tk = sorted(set(re.findall(r'\bKS-\d+\b', x['title'])) & keys); who = (x.get('user') or {}).get('login')
    cls = 'OVERLAP' if ov else ('SAME-KEY' if tk else None)
    rows.append({'number': n, 'user': who, 'head': x['head']['sha'], 'branch': x['head']['ref'], 'title': x['title'], 'overlap_paths': ov, 'title_keys': tk, 'class': cls, 'files': len(fs)})
    ro = (K.get('reported_overlaps') or {}).get(n)
    if cls == 'OVERLAP' and ro and ro.get('head') == x['head']['sha'] and set(ov) <= set(ro.get('paths', [])):
        expd += 1; print('EXPECTED OVERLAP (kit reported_overlaps; reported, never sequenced) #%s %s | head %s unmoved | paths %s | %s' % (n, who, x['head']['sha'][:12], ov, ro.get('note', '')[:160]))
    elif cls == 'OVERLAP':
        hits += 1; print('OVERLAP #%s %s | %s | %s | kit / doc paths %s | title keys %s%s' % (n, who, x['head']['ref'][:60], x['title'][:80], ov, tk,
                         ' | HEAD MOVED since drafting (was %s): re-read the overlap' % ro['head'][:12] if ro and ro.get('head') != x['head']['sha'] else ''))
    elif cls == 'SAME-KEY':
        same += 1; print('SAME-KEY (reported, never refused) #%s %s | %s | %s | %d file(s), no kit path' % (n, who, x['head']['ref'][:60], x['title'][:80], len(fs)))
if opt('--json'): json.dump(rows, open(opt('--json'), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d OVERLAP (a kit path or a Projects Documents file) | %d EXPECTED OVERLAP (reported) | %d SAME-KEY (%s) | excluded %s' % (len(rows), hits, expd, same, sorted(keys), sorted(EX)))
