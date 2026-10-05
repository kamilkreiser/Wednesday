#!/usr/bin/env python3
"""gh_census_gate60.py — read-only GitHub REST GETs for the gate60 launch action and the gate's COLLISION-CENSUS (a NEW COPY of gate59's
census). GH_TOKEN is read BY NAME from the Secuura .env and never printed.
  --pr <n>   also prints `API #<n> head <sha> base <ref> base_sha <sha> mergeable <v> reads <k> state <s> merged <b> branch <ref>
             changed_files <n>` (mergeable re-read up to 3x while null) — the launch action's second instrument.
  CENSUS: every OTHER open PR's file list (paged) against the kit's 4 paths, and its title against kit census_keys (whole key).
    `OAUTH #<n> ...` is printed for EVERY other open PR touching routes/oauth.ts or services/oauth.ts (kit census_focus), whether or not
    it is reported — the census the commission asked for by name (the class: any route that reads / writes OAuth app scopes).
    A hit outside kit.json reported_overlaps prints `OVERLAP ...` (the launch action refuses rc 15); a hit recorded there prints
    `EXPECTED OVERLAP` (with HEAD MOVED when its head is not the drafted one).
  --offline <dir>  replay fixtures (SELF-TEST only, never evidence).   --json <file> saves the raw census.
  --selftest  drives the classifier on planted rows: an unreported oauth.ts PR -> OAUTH + OVERLAP; an unreported services/oauth.ts PR
              (not a kit path) -> OAUTH only; a reported one -> EXPECTED; a reported one whose head moved -> EXPECTED + HEAD MOVED; a
              title-only KS-1210 hit -> OVERLAP; a disjoint PR -> nothing.
Usage: gh_census_gate60.py [--pr n] [--json out.json] [--offline dir] | --selftest      rc 0 read OK / rc 3 API failure / rc 1 selftest broken"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate60 import K, GH, opt_factory

A = sys.argv[1:]
if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
opt = opt_factory(A)
PATHS = set(K['files']); KEYS = set(K['census_keys']); FOCUS = list(K['census_focus'])
if os.environ.get('G60_OVERLAP_EXTRA'): PATHS.add(os.environ['G60_OVERLAP_EXTRA'])


def classify(n, title, head, fs, RO):
    """-> list of printed lines for one other open PR"""
    out = []; ov = sorted(set(fs) & PATHS); tk = sorted(set(re.findall(r'\bKS-\d+\b', title)) & KEYS); ro = RO.get(n)
    fo = sorted(set(fs) & set(FOCUS))
    if fo:
        out.append('OAUTH #%s head %s | %s | %d file(s) | %s' % (n, head[:12], title[:80], len(fs), [f.split('/src/')[-1] for f in fo]))
    if (ov or tk) and ro:
        out.append('EXPECTED OVERLAP (reported_overlaps; reported, never sequenced by a gate) #%s head %s%s | paths %s | title keys %s' % (
            n, head[:12], '' if ro.get('head') == head else ' (HEAD MOVED since drafting: was %s)' % str(ro.get('head'))[:12], ov, tk))
    elif ov or tk:
        out.append('OVERLAP #%s | %s | paths %s | title keys %s' % (n, title[:80], ov, tk))
    return out


if '--selftest' in A:
    RO = {'2': {'head': 'b' * 40}, '3': {'head': 'c' * 40}}
    arms = [('unreported oauth.ts PR', ('1', 'KS-9999: x', 'a' * 40, [FOCUS[0]]), ['OAUTH', 'OVERLAP #1']),
            ('unreported services/oauth.ts PR (not a kit path)', ('6', 'KS-9998: w', '9' * 40, [FOCUS[1]]), ['OAUTH #6']),
            ('reported doc PR', ('2', 'KS-1345: y', 'b' * 40, [K['docs'][0]]), ['EXPECTED OVERLAP']),
            ('reported, head moved', ('3', 'KS-1345: y', 'd' * 40, [K['docs'][1]]), ['HEAD MOVED']),
            ('title-only own key', ('4', 'KS-1210 follow-up', 'e' * 40, ['README.md']), ['OVERLAP #4']),
            ('disjoint', ('5', 'KS-1: z', 'f' * 40, ['README.md']), [])]
    ok = 0
    for name, args, want in arms:
        got = classify(*args, RO); g = all(any(w in l for l in got) for w in want) and (want or not got) and (name.startswith('unreported services') is False or not any(l.startswith('OVERLAP') for l in got))
        ok += bool(g); print('SELFTEST %s %s: want %s | got %s' % ('OK' if g else 'MISS', name, want or 'NOTHING', got or 'NOTHING'))
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); raise SystemExit(0 if ok == len(arms) else 1)

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
    print('CONTROL the classifier on #%s ITSELF (must print OAUTH and OVERLAP, or a zero below proves nothing): %s' % (PR, 'FIRES' if any(l.startswith('OAUTH') for l in ctl) and any(l.startswith('OVERLAP') for l in ctl) else 'BLIND'))
RO = K.get('reported_overlaps') or {}
if os.environ.get('G60_REPORTED'): RO = json.load(open(os.environ['G60_REPORTED']))
rows = []; hits = expd = foc = 0
for x in gh.pages('pulls?state=open'):
    n = str(x['number'])
    if n == PR: continue
    fs = [f['filename'] for f in gh.pages('pulls/%s/files' % n)]
    lines = classify(n, x['title'], x['head']['sha'], fs, RO)
    for l in lines: print(l)
    hits += any(l.startswith('OVERLAP') for l in lines); expd += any(l.startswith('EXPECTED') for l in lines); foc += any(l.startswith('OAUTH') for l in lines)
    rows.append({'number': n, 'user': (x.get('user') or {}).get('login'), 'head': x['head']['sha'], 'branch': x['head']['ref'], 'title': x['title'],
                 'overlap_paths': sorted(set(fs) & PATHS), 'oauth_focus': sorted(set(fs) & set(FOCUS)), 'files': len(fs)})
if opt('--json'): json.dump(rows, open(opt('--json'), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d touch routes/oauth.ts or services/oauth.ts | %d touch a kit path or carry a kit key outside reported_overlaps | %d expected overlap(s) reported | %d kit path(s), keys %s' % (
    len(rows), foc, hits, expd, len(PATHS), sorted(KEYS)))
