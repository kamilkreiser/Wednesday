#!/usr/bin/env python3
"""c5_prtext_gate63.py — C5 PR TEXT for #1388 (KS-1404 wiring; KS-1404 stays In Progress: the PR must not close it).

  --fetch <dir>   read-only GitHub GET of pulls/1388 (GH_TOKEN by name, never printed): writes <dir>/pr1388_body.md and
                  <dir>/pr1388_meta.json, prints an `API #1388 head … branch … base … state … merged … body … bytes` line; then judges.
  --body <file> [--title <text>] [--message <file>]   judge offline.
  T1  exactly ONE `Refs KS-1404` (markdown emphasis allowed) and the ticket URL
  T2  STRICT closing references (lib STRICT_CLOSE_RX: a closing keyword IMMEDIATELY before KS-n / #n / owner/repo#n) == 0 in title,
      body and commit message; planted CONTROL "Fixes KS-1404 and closes #42" scores 2. WIDE (120-char) hits: INFO, the gate rules
  T3  the only hyphenated key in title + body is KS-1404
  T4  title == the kit subject, no `(#`
  T5  the brief's required content (seat brief ITEM 2 step 6): per-box readings for kintsugi AND demo with D-Trust; what the anchor
      does NOT prove (the root-to-TSA binding, CRL/OCSP, policy OIDs); the "from `false` to `true`" deploy sentence; demo's status;
      the #1383 order
  T6  0 Co-Authored-By lines in the body
  T7  the image proof is declared NOT run (the gate's to run) — a body that claimed it would be a claim to refute
  INFO the figures the body states (3 failed / 3 passed, 86 passed, 1937 packages, TS2345, 9 emitted .js) for C3 to compare.
--selftest  synthetic bodies in $G63_SCRATCH/fixtures: T0 the drafter's saved real body (api/pr1388_body_drafter.md) passes; arms FAIL.
rc 0 all PASS / rc 1 any FAIL or 0 checked."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate63 import K, Tally, gh_get, HERE, SCRATCH, STRICT_CLOSE_RX, WIDE_CLOSE_RX, KEY_RX

PLANTED = 'Fixes KS-1404 and closes #42'


def judge(title, body, message, t):
    refs = re.findall(r'\bRefs\W{0,4}KS-1404\b', body)
    t.check('T1', len(refs) == 1 and K['ticket_url'] in body, '`Refs KS-1404` %d (want 1); ticket URL present %s' % (len(refs), K['ticket_url'] in body))
    hits = []; wide = []
    for where, txt in (('title', title), ('body', body), ('message', message or '')):
        hits += ['%s: %r' % (where, m.group(0)) for m in STRICT_CLOSE_RX.finditer(txt)]
        wide += ['%s: %r' % (where, m.group(0)[:90]) for m in WIDE_CLOSE_RX.finditer(txt)]
    ctl = len(STRICT_CLOSE_RX.findall(PLANTED))
    t.check('T2', not hits and ctl == 2, 'STRICT closing refs %d %s (want 0); planted CONTROL %r scores %d (want 2)' % (len(hits), hits, PLANTED, ctl))
    t.info('T2-wide', 'WIDE 120-char hits %d %s (INFO: GitHub/Linear parse only the STRICT shape; the gate rules)' % (len(wide), wide[:4]))
    keys = sorted(set(KEY_RX.findall(title + '\n' + body)))
    t.check('T3', keys == ['KS-1404'], 'hyphenated keys in title+body %s (want only KS-1404)' % keys)
    t.check('T4', title == K['subject'] and '(#' not in title, 'title %r %d chars (want the kit subject, no "(#")' % (title, len(title)))
    need = {'kintsugi reading': bool(re.search(r'kintsugi', body, re.I)), 'demo reading': bool(re.search(r'\bdemo\b', body, re.I)),
            'D-Trust per box': bool(re.search(r'D-Trust', body)),
            'binding not proved': bool(re.search(r'signs under this root', body, re.I)),
            'CRL/OCSP': bool(re.search(r'CRL|OCSP', body)), 'policy OIDs': bool(re.search(r'policy OID', body, re.I)),
            'false -> true sentence': bool(re.search(r'from `?false`? to `?true`?', body)),
            "demo's status": bool(re.search(r'MOCK-ONLY|mock', body)), '#1383 order': bool(re.search(r'#1383', body))}
    miss = [k for k, v in need.items() if not v]
    t.check('T5', not miss, 'required content missing %s' % miss)
    co = len(re.findall(r'(?im)^co-authored-by:', body))
    t.check('T6', co == 0, 'Co-Authored-By lines in body %d' % co)
    nr = re.search(r'NOT run[^\n]{0,40}\n?[^\n]{0,200}image', body, re.I) or re.search(r'image build proof[^\n]{0,200}', body, re.I)
    t.check('T7', bool(re.search(r'NOT run', body)) and bool(re.search(r'docker build', body)), 'image proof declared NOT run: "NOT run" %s, "docker build" %s' % (
        bool(re.search(r'NOT run', body)), bool(re.search(r'docker build', body))))
    for lbl, rx in (('red/green', r'3 failed / 3 passed[^\n]{0,60}'), ('suite', r'86 passed'), ('packages', r'\d{3,4} packages'),
                    ('tsc', r'TS2345[^\n]{0,60}'), ('emitted', r'\d+ emitted `?\.js`? files[^\n]{0,40}|all \d+ emitted[^\n]{0,40}')):
        m = re.search(rx, body); t.info('FIG', '%s: %s' % (lbl, repr(m.group(0)[:120]) if m else 'ABSENT'))


def selftest():
    import io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    good = open(os.path.join(HERE, 'api', 'pr1388_body_drafter.md'), encoding='utf-8').read()
    def run(title, body, msg=''):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge(title, body, msg, t)
        return t
    t0 = run(K['subject'], good); ok = int(not t0.fails); total = 1
    print('SELFTEST %s T0 the REAL body (api/pr1388_body_drafter.md, %d bytes): %d checked, fails %s' % ('OK' if not t0.fails else 'MISS', len(good.encode()), t0.n, t0.fails))
    def sub(s, a, b):
        assert s.count(a) >= 1, 'tamper anchor absent: %r' % a[:50]; return s.replace(a, b)
    arms = [('Refs removed', None, sub(good, 'Refs KS-1404\n', ''), '', ['T1']),
            ('a second Refs', None, good + '\nRefs KS-1404\n', '', ['T1']),
            ('"Closes KS-1404" in the body', None, good + '\nCloses KS-1404\n', '', ['T2']),
            ('"fixes #1388" in the commit message', None, good, 'x\n\nfixes #1388\n', ['T2']),
            ('"resolves: KS-1404"', None, good + '\nresolves: KS-1404\n', '', ['T2']),
            ('KS-1376 hyphenated', None, good + '\nsee KS-1376\n', '', ['T3']),
            ('title with (#1388)', K['subject'] + ' (#1388)', good, '', ['T4']),
            ('CRL/OCSP sentence removed', None, re.sub(r'(?m)^- \*\*Revocation\.\*\*.*\n', '', good), '', ['T5']),
            ('false -> true sentence removed', None, re.sub(r'from `false` to `true`', 'differently', good), '', ['T5']),
            ('Co-Authored-By', None, good + '\nCo-Authored-By: X <x@invalid>\n', '', ['T6']),
            ('image proof claimed as RUN (NOT run removed)', None, good.replace('NOT run', 'Ran'), '', ['T7'])]
    for name, title, body, msg, want in arms:
        assert body != good or msg or title, 'tamper did not land: ' + name
        p = os.path.join(fx, 'c5_arm_%02d.md' % total); open(p, 'w').write(body)
        t = run(title or K['subject'], body, msg); total += 1; g = set(want) <= set(t.fails); ok += g
        print('SELFTEST %s %s (fixture %s): want FAIL %s | got %s' % ('OK' if g else 'MISS', name, os.path.basename(p), want, t.fails))
    ctl_txt = 'a develop SHA carrying this fix without migration 049 (KS-1404)'
    t = run(K['subject'], good + '\n' + ctl_txt + '\n'); total += 1; g = 'T2' not in t.fails; ok += g
    print('SELFTEST %s the English noun "fix" in prose stays QUIET under STRICT (Seat D 8th\'s READY fault 1): got FAIL %s' % ('OK' if g else 'MISS', t.fails))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    if '--selftest' in A: raise SystemExit(selftest())
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    msg = open(opt('--message'), encoding='utf-8').read() if opt('--message') else ''
    if opt('--fetch'):
        d = opt('--fetch'); os.makedirs(d, exist_ok=True)
        p = gh_get('pulls/' + K['pr']); body = p.get('body') or ''; title = p['title']
        open(os.path.join(d, 'pr1388_body.md'), 'w', encoding='utf-8').write(body)
        meta = {'title': title, 'head': p['head']['sha'], 'branch': p['head']['ref'], 'base': p['base']['ref'], 'base_sha': p['base']['sha'],
                'state': p['state'], 'merged': p.get('merged'), 'draft': p.get('draft'), 'updated_at': p.get('updated_at'),
                'body_bytes': len(body.encode()), 'user': (p.get('user') or {}).get('login')}
        json.dump(meta, open(os.path.join(d, 'pr1388_meta.json'), 'w'), indent=1)
        print('API #%s head %s branch %s base %s state %s merged %s body %d bytes updated %s' % (
            K['pr'], meta['head'], meta['branch'], meta['base'], meta['state'], meta['merged'], meta['body_bytes'], meta['updated_at']))
    else:
        body = open(opt('--body'), encoding='utf-8').read(); title = opt('--title', K['subject'])
    t = Tally(); judge(title, body, msg, t); raise SystemExit(t.end())
