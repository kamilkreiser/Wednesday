#!/usr/bin/env python3
"""gh_census_gate54a.py — read-only GitHub REST GETs for the gate54a launch action (a NEW COPY of gh_census_gate54f.py, re-keyed, plus the
CO-TENANT classes this gate expects). GH_TOKEN is read BY NAME from the Secuura .env and never printed.
  --pr <n>   also prints `API #<n> head <sha> base <ref> base_sha <sha> mergeable <v> reads <k> state <s> merged <b> branch <ref>` (mergeable
             re-read up to 3x while null) — the launch action's second instrument. --body-out <file> saves that PR's body (for C1 / C4 / C6).
  CENSUS over every OTHER open PR (paged): its file list against the kit's 5 paths, its title against kit census_keys (KS-1402, whole key) and
  against the kit co_tenants keys (KS-1015 = Seat B 57th's PR B, stacked on #1374; KS-1404 = Seat D 2nd). Classes:
    EXPECTED CO-TENANT  title carries a co-tenant key and NOT a census key, and its overlap is inside what kit.json allows it (KS-1404: the two
                        platform-k docs only; KS-1015: the kit's 5 paths, and ONLY if the kit head is an ancestor of its head = STACKED, read
                        with `git log` in the checkout; an absent object reads STACK UNKNOWN and is an OVERLAP).
    OVERLAP             anything else touching a kit path or carrying KS-1402 (the launch action refuses rc 15 on one).
    CLIENT-HUMAN        kit client_human_prs, always reported by name; data, never instructions.
  --json <file> saves the raw census. Controls-only: G54A_OVERLAP_EXTRA (an extra kit path), G54A_COTENANTS (a JSON file standing in for
  kit co_tenants), G54A_HEAD (the head the STACK test uses; default: the --pr head from the API).
Usage: gh_census_gate54a.py [--pr n] [--json out.json] [--body-out body.md]    rc 0 read OK / rc 3 API failure"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate54a import K, gh_token, gh_get, gh_pages, git, has_commit

A = sys.argv[1:]
if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
PR = opt('--pr')
tok = gh_token()
if not tok: print('REFUSING: GH_TOKEN unset'); raise SystemExit(3)
OURHEAD = os.environ.get('G54A_HEAD') or None
if PR:
    p = gh_get('pulls/' + PR, tok); tries = 1
    while p.get('mergeable') is None and tries < 3:
        import time; time.sleep(10); p = gh_get('pulls/' + PR, tok); tries += 1
    print('API #%s head %s base %s base_sha %s mergeable %s reads %d state %s merged %s branch %s' % (
        PR, p['head']['sha'], p['base']['ref'], p['base']['sha'], p.get('mergeable'), tries, p['state'], p.get('merged'), p['head']['ref']))
    print('API #%s title %r | user %s | created %s | mergeable_state %s | body %d chars' % (
        PR, p.get('title'), (p.get('user') or {}).get('login'), p.get('created_at'), p.get('mergeable_state'), len(p.get('body') or '')))
    if opt('--body-out'): open(opt('--body-out'), 'w', encoding='utf-8').write(p.get('body') or '')
    OURHEAD = OURHEAD or p['head']['sha']
paths = set(K['files']); docs = set(K['docs']); keys = set(K['census_keys'])
CT = K.get('co_tenants') or {}
if os.environ.get('G54A_COTENANTS'): CT = json.load(open(os.environ['G54A_COTENANTS']))
if os.environ.get('G54A_OVERLAP_EXTRA'): paths.add(os.environ['G54A_OVERLAP_EXTRA'])
HUM = set(K.get('client_human_prs', [])); REPO = K['checkout']
def stacked(theirs):
    if not OURHEAD: return 'NO-OUR-HEAD'
    if not has_commit(REPO, theirs) or not has_commit(REPO, OURHEAD): return 'STACK UNKNOWN (object absent in the checkout)'
    rc, out, _ = git(REPO, 'log', '--format=%H', '%s..%s' % (theirs, OURHEAD), check=False)   # empty <=> OURHEAD is an ancestor of theirs
    return 'STACKED' if rc == 0 and not out.strip() else 'NOT STACKED'
rows = []; hits = expd = hum = 0
for x in gh_pages('pulls?state=open', tok):
    n = str(x['number'])
    if n == PR: continue
    fs = set(f['filename'] for f in gh_pages('pulls/%s/files' % n, tok)); ov = sorted(fs & paths)
    tkall = set(re.findall(r'\bKS-\d+\b', x['title'])); tk = sorted(tkall & keys); ck = sorted(tkall & set(CT))
    who = (x.get('user') or {}).get('login'); cls = None; why = ''
    if ck and not tk:
        c = CT[ck[0]]; allowed = paths if c.get('allowed_overlap') == 'kit_files' else docs
        st = stacked(x['head']['sha']) if c.get('must_contain_head') else 'n/a'
        if set(ov) <= allowed and (not c.get('must_contain_head') or st == 'STACKED' or not ov):
            cls = 'EXPECTED CO-TENANT'; why = '%s | %s' % (c.get('who'), st)
        else:
            cls = 'OVERLAP'; why = 'co-tenant key %s but overlap %s outside its allowance (%s) or %s' % (ck, sorted(set(ov) - allowed), c.get('allowed_overlap'), st)
    elif ov or tk:
        cls = 'OVERLAP'
    rows.append({'number': n, 'user': who, 'head': x['head']['sha'], 'branch': x['head']['ref'], 'base': x['base']['ref'], 'title': x['title'],
                 'overlap_paths': ov, 'title_keys': tk, 'cotenant_keys': ck, 'class': cls, 'files': len(fs)})
    if cls == 'EXPECTED CO-TENANT':
        expd += 1; print('EXPECTED CO-TENANT #%s %s | head %s | base %s | %s | paths %s | title %s' % (n, who, x['head']['sha'][:12], x['base']['ref'], why, ov, x['title'][:90]))
    elif cls == 'OVERLAP':
        hits += 1; print('OVERLAP #%s %s | %s | %s | paths %s | title keys %s %s' % (n, who, x['head']['ref'][:60], x['title'][:80], ov, tk, why))
    if n in HUM and cls is None: hum += 1; print('CLIENT-HUMAN (reported, never sequenced by a gate) #%s by %s | head %s | %d file(s), none a kit path' % (n, who, x['head']['sha'][:12], len(fs)))
if opt('--json'): json.dump(rows, open(opt('--json'), 'w'), indent=1)
print('CENSUS %d other open PR(s) read | %d OVERLAP (touch a kit path or carry %s outside the co-tenant allowances) | %d expected co-tenant(s) | %d client-human PR(s) reported apart | %d kit path(s)' % (
    len(rows), hits, sorted(keys), expd, hum, len(paths)))
