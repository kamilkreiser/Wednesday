#!/usr/bin/env python3
"""gh_census_gate65.py — COLLISION-CENSUS for #1393 (KS-1278): read-only GitHub GETs of every OTHER open PR and its files (GH_TOKEN by name).
  OVERLAP #n   touches one of the 4 CODE paths (documentRepo.ts, routes/documents.ts, the ks1278 / ks1293 tests) or carries KS-1278 in its
               title: the launch action refuses (rc 15). (Spark KS-593 `share-null-recipient-cp2` edits documents.ts AND ks1293: if it is
               raised, it lands here.)
  NEAR #n      touches another file under services/originate/src/repositories/ or services/originate/src/routes/, a migration naming
               `documents`, or carries KS-1419 (the residual) in its title: REPORTED
  DOCS #n      touches either platform-k doc: EXPECTED (a later landing moves develop; #1393 then needs Seat B 64th's docs merge-in judged
               by c4_docs_gate65.py predict / qm on the real develop)
  CONTROL      the classifier run on #1393 ITSELF must print OVERLAP — else every zero below is blind (rc 3)
--selftest  the classifier on planted rows.   --json <file> saves the raw census.
rc 0 read OK and no OVERLAP / rc 15 an OVERLAP / rc 3 API failure or a BLIND control / rc 1 selftest broken."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate65 import K, gh_get, gh_pages

CODE = set(K['code_paths']); DOCS = {K['flow'], K['cheat']}
NEAR_DIRS = ('Blockchain/Dev/services/originate/src/repositories/', 'Blockchain/Dev/services/originate/src/routes/')


def classify(n, title, fs):
    c = sorted(set(fs) & CODE); tk = bool(re.search(r'KS[- ]1278\b', title))
    if c or tk: return ['OVERLAP #%s | %s | code paths %s | title KS-1278 %s' % (n, title[:70], [os.path.basename(x) for x in c], tk)]
    out = []
    nr = sorted(p for p in fs if p.startswith(NEAR_DIRS) or (re.search(r'/migrations/', p) and 'document' in p.lower()))
    if nr or re.search(r'KS[- ]1419\b', title): out.append('NEAR #%s | %s | %s' % (n, title[:60], [os.path.basename(x) for x in nr][:6] or 'title KS-1419'))
    d = sorted(set(fs) & DOCS)
    if d: out.append('DOCS #%s | %s | %s' % (n, title[:60], [os.path.basename(x)[:24] for x in d]))
    return out


def selftest():
    R, D, T, M = K['route_file'], K['repo_file'], K['test'], K['manifest_test']
    arms = [('documents.ts', ('1', 'KS-9: x', [R]), 'OVERLAP'),
            ('documentRepo.ts', ('2', 'KS-9: x', [D, 'a.ts']), 'OVERLAP'),
            ('the ks1293 register (KS-593 share-null-recipient-cp2 shape)', ('3', 'KS-593: share null recipient', [M, 'Blockchain/Dev/services/originate/src/routes/shares.ts']), 'OVERLAP'),
            ('the ks1278 test', ('4', 'KS-1: y', [T]), 'OVERLAP'),
            ('title KS-1278 only', ('5', 'KS-1278: follow-up', ['README.md']), 'OVERLAP'),
            ('another originate route', ('6', 'KS-2: y', ['Blockchain/Dev/services/originate/src/routes/webhooks.ts']), 'NEAR'),
            ('a documents migration', ('7', 'KS-3: y', ['Blockchain/Dev/migrations/050_documents_status_index.sql']), 'NEAR'),
            ('title KS-1419', ('8', 'KS-1419: 404 not 400 when deleted mid-race', ['x.ts']), 'NEAR'),
            ('docs only', ('9', 'KS-1408: y', [K['flow'], K['cheat'], 'a.ts']), 'DOCS'),
            ('docs + documents.ts', ('10', 'KS-1: z', [K['cheat'], R]), 'OVERLAP'),
            ('an auth route (another service)', ('11', 'KS-2: z', ['Blockchain/Dev/services/auth/src/routes/oauth.ts']), None),
            ('disjoint', ('12', 'KS-2: z', ['README.md']), None)]
    ok = 0
    for name, args, want in arms:
        got = classify(*args); g = (bool(got) and got[0].startswith(want)) if want else not got; ok += g
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
        ctl = classify(K['pr'], me['title'], own); ctl_ok = bool(ctl) and ctl[0].startswith('OVERLAP')
        print('CONTROL the classifier on #%s ITSELF: %s' % (K['pr'], 'FIRES' if ctl_ok else 'BLIND'))
        rows = []; cnt = {'OVERLAP': 0, 'NEAR': 0, 'DOCS': 0}; others = 0
        for x in gh_pages('pulls?state=open'):
            n = str(x['number'])
            if n == K['pr']: continue
            others += 1
            fs = [f['filename'] for f in gh_pages('pulls/%s/files' % n)]
            for c in classify(n, x['title'], fs):
                print(c + ' | head %s' % x['head']['sha'][:12]); cnt[c.split()[0]] += 1
            rows.append({'number': n, 'head': x['head']['sha'], 'title': x['title'], 'files': fs})
    except Exception as e:
        print('API FAILURE %s' % e); raise SystemExit(3)
    if '--json' in A: json.dump(rows, open(A[A.index('--json') + 1], 'w'), indent=1)
    print('CENSUS %d other open PR(s): %d OVERLAP, %d NEAR, %d DOCS; control #%s %s' % (others, cnt['OVERLAP'], cnt['NEAR'], cnt['DOCS'], K['pr'], 'FIRES' if ctl_ok else 'BLIND'))
    if not ctl_ok: raise SystemExit(3)
    raise SystemExit(15 if cnt['OVERLAP'] else 0)
