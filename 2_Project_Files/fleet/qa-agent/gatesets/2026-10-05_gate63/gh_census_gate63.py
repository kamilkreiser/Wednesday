#!/usr/bin/env python3
"""gh_census_gate63.py — COLLISION CENSUS for #1388: every OTHER open PR, classified (read-only GitHub GETs, GH_TOKEN by name).

  OVERLAP  touches any of the 7 NON-DOC kit paths (compose, the timestamping Dockerfile, config/README.md, the anchor file, the new
           test, qualified-tsa.ts, rfc3161-verify.ts), OR anything under services/timestamping/config/ or src/tsa/, OR any
           docker-compose*.yml, OR names KS-1404 in its title
  NEAR     touches any OTHER services/timestamping/ file (e.g. a dependabot package.json bump): REPORTED, never refused — it can
           change what `npm ci` installs in the image, so the gate names it in C7 (ex1 history: the drafter's first classifier
           called #649 / #575, open since 2026-07/08, OVERLAP and would have refused every launch)
  DOCS     touches only the two platform-k docs among the kit paths (EXPECTED: merge-in material for Q-M)
  CONTROL  the same classifier run on #1388 itself must say OVERLAP, or the census is blind (rc 3)
Prints `API #1388 head <sha> branch <b> base <b> state <s> merged <m>` (the launch action reads it), then one line per hit.
--selftest  synthetic file lists: 8 arms.   --json <file>: write the full census.
rc 0 no OVERLAP / rc 15 an OVERLAP / rc 3 API failure or blind control."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate63 import K, gh_get, gh_pages

DOCS = {K['flow'], K['cheat']}


def classify(title, files):
    hot = [f for f in files if f in K['code_paths'] or f.startswith('Blockchain/Dev/services/timestamping/config/')
           or f.startswith('Blockchain/Dev/services/timestamping/src/tsa/') or os.path.basename(f).startswith('docker-compose')]
    if hot or 'KS-1404' in (title or ''):
        return 'OVERLAP', hot
    near = [f for f in files if f.startswith('Blockchain/Dev/services/timestamping/')]
    if near:
        return 'NEAR', near
    d = sorted(DOCS & set(files))
    return ('DOCS', d) if d else ('NONE', [])


def selftest():
    arms = [('the real file list of #1388', 'KS-1404: x', list(K['files']), 'OVERLAP'),
            ('docs only', 'KS-1388: y', [K['flow'], K['cheat']], 'DOCS'),
            ('the production compose', 'KS-9: z', ['Blockchain/Dev/docker-compose.production.yml'], 'OVERLAP'),
            ('another timestamping file (src/index.ts)', 'KS-9: z', ['Blockchain/Dev/services/timestamping/src/index.ts'], 'NEAR'),
            ('a dependabot package.json bump', 'chore(deps): bump pg', ['Blockchain/Dev/services/timestamping/package.json'], 'NEAR'),
            ('a new file under config/', 'KS-9: z', ['Blockchain/Dev/services/timestamping/config/other.crt'], 'OVERLAP'),
            ('KS-1404 in a title, unrelated files', 'KS-1404: follow-up', ['README.md'], 'OVERLAP'),
            ('unrelated', 'KS-1: a', ['Blockchain/Dev/services/auth/src/x.ts'], 'NONE')]
    ok = 0
    for name, title, files, want in arms:
        got = classify(title, files)[0]; ok += got == want
        print('SELFTEST %s %s: want %s got %s' % ('OK' if got == want else 'MISS', name, want, got))
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); print('CHECKED %d arm(s)' % len(arms))
    return 0 if ok == len(arms) else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    if '--selftest' in A: raise SystemExit(selftest())
    out = A[A.index('--json') + 1] if '--json' in A else None
    try:
        me = gh_get('pulls/' + K['pr'])
        prs = gh_pages('pulls?state=open')
    except Exception as e:
        print('API FAILURE %s' % e); raise SystemExit(3)
    print('API #%s head %s branch %s base %s state %s merged %s' % (K['pr'], me['head']['sha'], me['head']['ref'], me['base']['ref'], me['state'], me.get('merged')))
    rows = []; over = 0; ctl = None
    for p in prs:
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % p['number'])]
        c, hit = classify(p['title'], files)
        if p['number'] == int(K['pr']):
            ctl = c; continue
        rows.append({'pr': p['number'], 'title': p['title'], 'head': p['head']['sha'], 'class': c, 'hits': hit})
        if c != 'NONE':
            print('%s #%d %s %s | %s' % (c, p['number'], p['head']['sha'][:12], p['title'][:80], hit[:4]))
        over += c == 'OVERLAP'
    print('CENSUS %d other open PRs | OVERLAP %d | NEAR %d | DOCS %d | CONTROL #%s classified %s' % (
        len(rows), over, sum(r['class'] == 'NEAR' for r in rows), sum(r['class'] == 'DOCS' for r in rows), K['pr'], ctl))
    if out: json.dump({'control': ctl, 'rows': rows}, open(out, 'w'), indent=1)
    if ctl != 'OVERLAP':
        print('BLIND: the classifier does not fire on #%s itself' % K['pr']); raise SystemExit(3)
    raise SystemExit(15 if over else 0)
