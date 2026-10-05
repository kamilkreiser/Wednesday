#!/usr/bin/env python3
"""gh_census_gate61.py — read-only GitHub REST GETs for the gate61 launch action and the gate's COLLISION-CENSUS (a NEW COPY of gate59's
census, re-keyed). GH_TOKEN is read BY NAME from the Secuura .env and never printed.
  --pr <n>   also prints `API #<n> head <sha> base <ref> base_sha <sha> mergeable <v> reads <k> state <s> merged <b> branch <ref>
             changed_files <n>` (mergeable re-read up to 3x while null) — the launch action's second instrument (field positions fixed).
  CENSUS over every OTHER open PR (files paged):
    `MIGRATION #<n>` — the PR adds or changes a Blockchain/Dev/migrations/*.sql (kit census_migration_rx): the 049 number is contested or
                       develop's migration set moves under #1383 — ALWAYS an OVERLAP unless reported;
    `WRITER #<n>`    — the PR touches a charge_events writer file (kit writer_files): 049's FORCE changes what that code may write;
    `OVERLAP #<n>`   — a kit path, a migration, a writer file, or a title carrying KS-1401 / KS-1376, outside kit reported_overlaps (the
                       launch action refuses rc 15);
    `EXPECTED OVERLAP` — recorded in reported_overlaps (#1381, #1382: both docs), with HEAD MOVED when its head is not the drafted one.
  --offline <dir> replay fixtures (SELF-TEST only).   --json <file> saves the raw census.
  --selftest  the classifier on planted rows.
Usage: gh_census_gate61.py [--pr n] [--json out.json] [--offline dir] | --selftest      rc 0 read OK / rc 3 API failure / rc 1 selftest broken"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate61 import K, GH, opt_factory

A = sys.argv[1:]
if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
opt = opt_factory(A)
PATHS = set(K['files']); KEYS = set(K['census_keys']); MIGRX = re.compile(K['census_migration_rx']); WRITERS = set(K['writer_files'])
if os.environ.get('G61_OVERLAP_EXTRA'): PATHS.add(os.environ['G61_OVERLAP_EXTRA'])


def classify(n, title, head, fs, RO):
    out = []; ov = sorted(set(fs) & PATHS); mig = sorted(f for f in fs if MIGRX.match(f)); wr = sorted(set(fs) & WRITERS)
    tk = sorted(set(re.findall(r'\bKS-\d+\b', title)) & KEYS); ro = RO.get(n)
    if mig: out.append('MIGRATION #%s head %s | %s | %s' % (n, head[:12], title[:70], mig))
    if wr: out.append('WRITER #%s head %s | %s | %s' % (n, head[:12], title[:70], wr))
    hit = ov or mig or wr or tk
    if hit and ro and not mig and (not wr or ro.get('writer_ok')):
        out.append('EXPECTED OVERLAP (reported_overlaps; reported, never sequenced by a gate) #%s head %s%s | paths %s | title keys %s' % (
            n, head[:12], '' if ro.get('head') == head else ' (HEAD MOVED since drafting: was %s)' % str(ro.get('head'))[:12], ov, tk))
    elif hit:
        out.append('OVERLAP #%s | %s | paths %s | migrations %s | writers %s | title keys %s' % (n, title[:70], ov, mig, wr, tk))
    return out


if '--selftest' in A:
    RO = {'2': {'head': 'b' * 40}, '3': {'head': 'c' * 40}, '7': {'head': '7' * 40, 'writer_ok': True}}
    arms = [('another migration (050)', ('1', 'KS-9: x', 'a' * 40, ['Blockchain/Dev/migrations/050_x.sql']), ['MIGRATION', 'OVERLAP #1']),
            ('reported doc PR', ('2', 'KS-1345: y', 'b' * 40, [K['docs'][0]]), ['EXPECTED OVERLAP']),
            ('reported, head moved', ('3', 'KS-1005: y', 'd' * 40, [K['docs'][1]]), ['HEAD MOVED']),
            ('a charge_events writer file', ('4', 'KS-7: z', 'e' * 40, [K['writer_files'][0]]), ['WRITER', 'OVERLAP #4']),
            ('title-only KS-1376', ('5', 'KS-1376 follow-up', 'f' * 40, ['README.md']), ['OVERLAP #5']),
            ('a reported doc PR that ALSO adds a migration is NOT expected', ('2', 'KS-1345: y', 'b' * 40, [K['docs'][0], 'Blockchain/Dev/migrations/050_y.sql']), ['MIGRATION', 'OVERLAP #2']),
            ('a writer file on a reported PR marked writer_ok', ('7', 'KS-741: w', '7' * 40, [K['writer_files'][2]]), ['WRITER', 'EXPECTED OVERLAP']),
            ('disjoint', ('6', 'KS-1: z', '1' * 40, ['README.md']), [])]
    ok = 0
    for name, args, want in arms:
        got = classify(*args, RO); g = all(any(w in l for l in got) for w in want) and (want or not got)
        ok += bool(g); print('SELFTEST %s %s: want %s | got %s' % ('OK' if g else 'MISS', name, want or 'NOTHING', got or 'NOTHING'))
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); print('CHECKED %d arm(s)' % len(arms))
    raise SystemExit(0 if ok == len(arms) else 1)

gh = GH(opt('--offline')); PR = opt('--pr')
if PR:
    import time
    p = gh.get('pulls/' + PR); tries = 1
    while p.get('mergeable') is None and tries < 3 and not opt('--offline'):
        time.sleep(10); p = gh.get('pulls/' + PR); tries += 1
    print('API #%s head %s base %s base_sha %s mergeable %s reads %d state %s merged %s branch %s changed_files %s' % (
        PR, p['head']['sha'], p['base']['ref'], p['base']['sha'], p.get('mergeable'), tries, p['state'], p.get('merged'), p['head']['ref'], p.get('changed_files')))
    own = [f['filename'] for f in gh.pages('pulls/%s/files' % PR)]
    ctl = classify(PR, p['title'], p['head']['sha'], own, {})
    print('CONTROL the classifier on #%s ITSELF (must print MIGRATION and OVERLAP, or a zero below proves nothing): %s' % (PR, 'FIRES' if any(l.startswith('MIGRATION') for l in ctl) and any(l.startswith('OVERLAP') for l in ctl) else 'BLIND'))
RO = K.get('reported_overlaps') or {}
if os.environ.get('G61_REPORTED'): RO = json.load(open(os.environ['G61_REPORTED']))
rows = []; hits = expd = mg = wrn = 0
for x in gh.pages('pulls?state=open'):
    n = str(x['number'])
    if n == PR: continue
    fs = [f['filename'] for f in gh.pages('pulls/%s/files' % n)]
    lines = classify(n, x['title'], x['head']['sha'], fs, RO)
    for l in lines: print(l)
    hits += any(l.startswith('OVERLAP') for l in lines); expd += any(l.startswith('EXPECTED') for l in lines)
    mg += any(l.startswith('MIGRATION') for l in lines); wrn += any(l.startswith('WRITER') for l in lines)
    rows.append({'number': n, 'user': (x.get('user') or {}).get('login'), 'head': x['head']['sha'], 'branch': x['head']['ref'], 'title': x['title'],
                 'overlap_paths': sorted(set(fs) & PATHS), 'migrations': sorted(f for f in fs if MIGRX.match(f)), 'writers': sorted(set(fs) & WRITERS), 'files': len(fs)})
if opt('--json'): json.dump(rows, open(opt('--json'), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d add/change a migration .sql | %d touch a charge_events writer | %d OVERLAP outside reported_overlaps | %d expected overlap(s) reported | %d kit path(s), keys %s' % (
    len(rows), mg, wrn, hits, expd, len(PATHS), sorted(KEYS)))
