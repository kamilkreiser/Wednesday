#!/usr/bin/env python3
"""gh_census_gate62.py — COLLISION-CENSUS for #1387: read-only GitHub GETs of every OTHER open PR and its files (GH_TOKEN by name).
  OVERLAP #n        touches a NON-DOC kit path (the KS 971 suite or either observability env example) or carries KS-1388 in its title:
                    the launch action refuses (rc 15) — read it before launching
  DOCS #n           touches only the two platform-k docs among kit paths: EXPECTED (every queue PR appends a block); a later landing
                    means #1387 needs a docs-only merge-in judged by c4 qm
  CONTROL           the classifier run on #1387 ITSELF must print OVERLAP (else every zero below is blind)
--selftest  the classifier on planted rows.   --json <file> saves the raw census.
rc 0 read OK and no OVERLAP / rc 15 an OVERLAP / rc 3 API failure / rc 1 selftest broken."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate62 import K, gh_get, gh_pages

NONDOC = set(K['qm_disjoint_paths']); DOCS = {K['flow'], K['cheat']}


def classify(n, title, fs):
    nd = sorted(set(fs) & NONDOC); dc = sorted(set(fs) & DOCS); tk = 'KS-1388' in title or 'KS 1388' in title
    if nd or tk: return 'OVERLAP #%s | %s | non-doc kit paths %s | title KS-1388 %s' % (n, title[:70], nd, tk)
    if dc: return 'DOCS #%s | %s | %s' % (n, title[:70], [os.path.basename(x)[:24] for x in dc])
    return None


def selftest():
    arms = [('env example', ('1', 'KS-9: x', ['observability/.env.example']), 'OVERLAP'),
            ('the KS 971 suite', ('2', 'KS-9: x', [K['test']]), 'OVERLAP'),
            ('title KS-1388 only', ('3', 'KS-1388: s2 slot-agnostic', ['README.md']), 'OVERLAP'),
            ('docs only', ('4', 'KS-1210: y', [K['flow'], K['cheat'], 'a.ts']), 'DOCS'),
            ('docs + env example', ('5', 'KS-1: z', [K['cheat'], 'observability/config/alerting.env.example']), 'OVERLAP'),
            ('disjoint', ('6', 'KS-2: z', ['README.md']), None)]
    ok = 0
    for name, args, want in arms:
        got = classify(*args); g = (got or '').startswith(want) if want else got is None; ok += g
        print('SELFTEST %s %s: want %s | got %s' % ('OK' if g else 'MISS', name, want or 'NOTHING', got or 'NOTHING'))
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); print('CHECKED %d arm(s)' % len(arms))
    return 0 if ok == len(arms) else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    if '--selftest' in A: raise SystemExit(selftest())
    try:
        me = gh_get('pulls/' + K['pr']); own = [f['filename'] for f in gh_pages('pulls/%s/files' % K['pr'])]
        print('API #%s head %s branch %s base %s state %s merged %s changed_files %s' % (K['pr'], me['head']['sha'], me['head']['ref'], me['base']['ref'],
              me['state'], me.get('merged'), me.get('changed_files')))
        ctl = classify(K['pr'], me['title'], own)
        print('CONTROL the classifier on #%s ITSELF: %s' % (K['pr'], 'FIRES' if (ctl or '').startswith('OVERLAP') else 'BLIND'))
        rows = []; nov = nd = 0; others = 0
        for x in gh_pages('pulls?state=open'):
            n = str(x['number'])
            if n == K['pr']: continue
            others += 1
            fs = [f['filename'] for f in gh_pages('pulls/%s/files' % n)]
            c = classify(n, x['title'], fs)
            if c:
                print(c + ' | head %s' % x['head']['sha'][:12]); nov += c.startswith('OVERLAP'); nd += c.startswith('DOCS')
            rows.append({'number': n, 'head': x['head']['sha'], 'title': x['title'], 'files': fs})
    except Exception as e:
        print('API FAILURE %s' % e); raise SystemExit(3)
    if '--json' in A: json.dump(rows, open(A[A.index('--json') + 1], 'w'), indent=1)
    print('CENSUS %d other open PR(s): %d OVERLAP, %d DOCS (expected), control %s' % (others, nov, nd, 'FIRES' if (ctl or '').startswith('OVERLAP') else 'BLIND'))
    if not (ctl or '').startswith('OVERLAP'): raise SystemExit(3)
    raise SystemExit(15 if nov else 0)
