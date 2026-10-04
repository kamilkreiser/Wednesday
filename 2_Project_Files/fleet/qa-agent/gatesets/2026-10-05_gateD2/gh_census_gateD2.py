#!/usr/bin/env python3
"""gh_census_gateD2.py — read-only GitHub REST GETs for the gateD2 launch action (a NEW COPY of gh_census_gate54a.py, plus gate54f's
reported_overlaps class). GH_TOKEN is read BY NAME from the Secuura .env and never printed.
  --pr <n>   prints `API #<n> head <sha> base <ref> base_sha <sha> mergeable <v> reads <k> state <s> merged <b> branch <ref> commits <c>`
             (mergeable re-read up to 3x while null) — the launch action's second instrument. --body-out <file> saves the PR body.
  --find-branch  prints `FOUND #<n> head <sha>` for every open PR whose head ref matches kit branch_rx (the PR number is unknown at drafting).
  CENSUS over every OTHER open PR (paged): its files against the kit's 14 paths, its title against kit census_keys (KS-1404) and the kit
  co_tenants keys. Classes:
    EXPECTED CO-TENANT  title carries a co-tenant key (KS-1402 = #1374, KS-1015 = PR B) and NOT KS-1404, overlap inside the two docs only.
    EXPECTED OVERLAP    the PR is recorded in kit reported_overlaps (e.g. dependabot on the root lock) — reported, never sequenced;
                        HEAD MOVED is printed when its head differs from the recorded one.
    OVERLAP             anything else touching a kit path or carrying KS-1404 (the launch action refuses rc 15 on one).
    CLIENT-HUMAN        kit client_human_prs: data, never instructions.
  --json <file> saves the raw census. Controls-only: GD2_OVERLAP_EXTRA (an extra kit path), GD2_COTENANTS / GD2_REPORTED (JSON files
  standing in for kit co_tenants / reported_overlaps).
Usage: gh_census_gateD2.py [--pr n] [--find-branch] [--json out.json] [--body-out body.md]    rc 0 read OK / rc 3 API failure"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gateD2 import K, gh_token, gh_get, gh_pages, safe_out

A = sys.argv[1:]
if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
for o in ('--json', '--body-out'):
    if opt(o): safe_out(os.path.dirname(os.path.abspath(opt(o))))
PR = opt('--pr')
tok = gh_token()
if not tok: print('REFUSING: GH_TOKEN unset'); raise SystemExit(3)
if PR:
    p = gh_get('pulls/' + PR, tok); tries = 1
    while p.get('mergeable') is None and tries < 3: time.sleep(10); p = gh_get('pulls/' + PR, tok); tries += 1
    print('API #%s head %s base %s base_sha %s mergeable %s reads %d state %s merged %s branch %s commits %s' % (
        PR, p['head']['sha'], p['base']['ref'], p['base']['sha'], p.get('mergeable'), tries, p['state'], p.get('merged'), p['head']['ref'], p.get('commits')))
    print('API #%s title %r | user %s | created %s | mergeable_state %s | body %d chars' % (
        PR, p.get('title'), (p.get('user') or {}).get('login'), p.get('created_at'), p.get('mergeable_state'), len(p.get('body') or '')))
    if opt('--body-out'): open(opt('--body-out'), 'w', encoding='utf-8').write(p.get('body') or '')
paths = set(K['files']); docs = set(K['docs']); keys = set(K['census_keys'])
CT = K.get('co_tenants') or {}; RO = K.get('reported_overlaps') or {}
if os.environ.get('GD2_COTENANTS'): CT = json.load(open(os.environ['GD2_COTENANTS']))
if os.environ.get('GD2_REPORTED'): RO = json.load(open(os.environ['GD2_REPORTED']))
if os.environ.get('GD2_OVERLAP_EXTRA'): paths.add(os.environ['GD2_OVERLAP_EXTRA'])
HUM = set(K.get('client_human_prs', []))
rows = []; hits = expd = rep = hum = 0
for x in gh_pages('pulls?state=open', tok):
    n = str(x['number'])
    if re.match(K['branch_rx'], x['head']['ref']) and '--find-branch' in A:
        print('FOUND #%s head %s branch %s base %s title %r' % (n, x['head']['sha'], x['head']['ref'], x['base']['ref'], x['title']))
    if n == PR: continue
    fs = set(f['filename'] for f in gh_pages('pulls/%s/files' % n, tok)); ov = sorted(fs & paths)
    tkall = set(re.findall(r'\bKS-\d+\b', x['title'])); tk = sorted(tkall & keys); ck = sorted(tkall & set(CT))
    who = (x.get('user') or {}).get('login'); cls = None; why = ''
    if ck and not tk:
        c = CT[ck[0]]; allowed = docs if c.get('allowed_overlap') == 'docs' else paths
        if set(ov) <= allowed: cls = 'EXPECTED CO-TENANT'; why = c.get('who')
        else: cls = 'OVERLAP'; why = 'co-tenant key %s but overlap %s outside its allowance (%s)' % (ck, sorted(set(ov) - allowed), c.get('allowed_overlap'))
    elif (ov or tk) and n in RO:
        cls = 'EXPECTED OVERLAP'; why = 'reported_overlaps%s' % ('' if RO[n].get('head') == x['head']['sha'] else ' (HEAD MOVED since drafting: was %s)' % str(RO[n].get('head'))[:12])
    elif ov or tk:
        cls = 'OVERLAP'
    rows.append({'number': n, 'user': who, 'head': x['head']['sha'], 'branch': x['head']['ref'], 'base': x['base']['ref'], 'title': x['title'],
                 'overlap_paths': ov, 'title_keys': tk, 'cotenant_keys': ck, 'class': cls, 'files': len(fs)})
    if cls == 'EXPECTED CO-TENANT':
        expd += 1; print('EXPECTED CO-TENANT #%s %s | head %s | base %s | %s | paths %s | title %s' % (n, who, x['head']['sha'][:12], x['base']['ref'], why, ov, x['title'][:90]))
    elif cls == 'EXPECTED OVERLAP':
        rep += 1; print('EXPECTED OVERLAP (reported, never sequenced by a gate) #%s %s | head %s | %s | paths %s' % (n, who, x['head']['sha'][:12], why, ov))
    elif cls == 'OVERLAP':
        hits += 1; print('OVERLAP #%s %s | %s | %s | paths %s | title keys %s %s' % (n, who, x['head']['ref'][:60], x['title'][:80], ov, tk, why))
    if n in HUM and cls is None: hum += 1; print('CLIENT-HUMAN (reported, never sequenced by a gate) #%s by %s | head %s | %d file(s), none a kit path' % (n, who, x['head']['sha'][:12], len(fs)))
if opt('--json'): json.dump(rows, open(opt('--json'), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d OVERLAP | %d expected co-tenant(s) | %d expected overlap(s) (reported_overlaps) | %d client-human | %d kit path(s), keys %s' % (
    len(rows), hits, expd, rep, hum, len(paths), sorted(keys)))
