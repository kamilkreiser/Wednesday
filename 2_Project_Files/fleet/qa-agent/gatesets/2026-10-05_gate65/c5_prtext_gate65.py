#!/usr/bin/env python3
"""c5_prtext_gate65.py — C5 PR TEXT + C6 NOT COVERED for #1393 (KS-1278). Whether KS-1278 moves is Wednesday's, never the gate's.

  --fetch <dir>   read-only GitHub GET of pulls/1393 (GH_TOKEN by name, never printed); writes <dir>/pr1393_body.md + pr1393_meta.json
  --body <file> --title <text> [--message <file>]   judge offline (the self-test fixtures use this)
  T1  exactly ONE `Refs KS-1278` in the body and the ticket URL https://linear.app/secuura/issue/KS-1278
  T2  CLOSING WORDS: 0 Linear magic-word references (close/fix/resolve/complete… then a hyphenated KS key in the same sentence — Linear
      does NOT parse negation) in title, body AND commit message; 0 GitHub `<kw> #n`
  T3  the only hyphenated KS key in title + body is KS-1278 (one hyphenated key; others de-hyphenated)
  T4  title == the kit subject (75 chars), <= 92, no `(#`
  T5  the RESIDUAL is NAMED by its ticket: KS 1419 (de-hyphenated, any spacing) appears in the body beside the 400-vs-404 residual —
      the READY says KS-1419 was filed AFTER the raise; "being filed separately" is not a name
  T6  0 Co-Authored-By lines in the body (a squash may carry the body into the landed message)
  T7  the doc placement is stated as RULED: flow `15.` between `14.` and `19.`; the cheat sheet has NO readable ordering invariant, so the
      position was ruled, not inferred
  C6  NOT COVERED names, by sentence: N1 no live sweep AND the ticket does not move to Done on this account; N2 the mocked Prisma driver /
      concurrent serialisation UNMEASURED; N3 the deleted-mid-race 400-vs-404 residual; N4 PREFLIGHT INCOMPLETE 12/15, legs 3 4 8, "not a
      pass"; N5 a docs-only merge-in is required, its tree from the gate's key-anchored prediction
  INFO every figure the body states (red-first, suite totals, 14 passed, the tamper rows, the timing controls, the route line numbers,
       the body length) for the gate to compare with C1-C4; and the "a null can only mean the row became revoked" claim (C3b N2 / N3)
--selftest  synthetic bodies in <G65_SCRATCH>/fixtures: T0 a clean body passes; every arm must FAIL its named check.
rc 0 all PASS / rc 1 any FAIL or 0 checked."""
import hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate65 import K, Tally, gh_get, SCRATCH

CLOSE_RX = re.compile(r'\b(close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?|completing)\b[^.\n]{0,60}?\bKS-\d+', re.I)
GHCLOSE_RX = re.compile(r'\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#\d+', re.I)
KEY_RX = re.compile(r'\bKS-\d+\b')


def judge(title, body, message, t):
    refs = re.findall(r'\bRefs\W{0,4}KS-1278\b', body)
    t.check('T1', len(refs) == 1 and K['ticket_url'] in body, '`Refs KS-1278` %d (want 1); ticket URL present %s' % (len(refs), K['ticket_url'] in body))
    hits = []
    for where, txt in (('title', title), ('body', body), ('message', message or '')):
        hits += ['%s: %r' % (where, m.group(0)[:90]) for m in CLOSE_RX.finditer(txt)] + ['%s: %r' % (where, m.group(0)) for m in GHCLOSE_RX.finditer(txt)]
    t.check('T2', not hits, 'closing references %d %s' % (len(hits), hits))
    keys = sorted(set(KEY_RX.findall(title + '\n' + body)))
    t.check('T3', keys == ['KS-1278'], 'hyphenated keys in title+body %s (want only KS-1278)' % keys)
    t.check('T4', title == K['subject'] and len(title) <= K['subject_max'] and '(#' not in title, 'title %r %d chars (want the kit subject, <= %d, no "(#")' % (title, len(title), K['subject_max']))
    named = re.findall(r'KS\s?1419', body); near = bool(re.search(r'KS\s?1419[^\n]{0,300}(404|deleted)|(404|deleted)[^\n]{0,300}KS\s?1419', body))
    t.check('T5', bool(named) and near, 'residual ticket named (KS 1419, de-hyphenated) %d time(s); beside the 400-vs-404 residual %s; "filed separately" without a name: %s' % (
        len(named), near, bool(re.search(r'filed separately', body))))
    co = len(re.findall(r'(?im)^co-authored-by:', body))
    t.check('T6', co == 0, 'Co-Authored-By lines in body %d' % co)
    p15 = bool(re.search(r'block `?15\.`?\s+between\s+`?14\.`?\s+and\s+`?19\.`?', body)); inv = bool(re.search(r'\*\*no\*\* readable ordering invariant|no readable ordering invariant', body, re.I))
    ruled = bool(re.search(r'was \*\*ruled\*\*|was ruled', body))
    t.check('T7', p15 and inv and ruled, 'flow 15. between 14. and 19. stated %s; cheat "no readable ordering invariant" %s; position "ruled" %s' % (p15, inv, ruled))
    nc = body[body.rfind('NOT COVERED'):] if 'NOT COVERED' in body else ''   # the LAST occurrence = the section heading, not a forward reference
    need = {'N1 no live sweep + not Done': bool(re.search(r'No live sweep', nc)) and bool(re.search(r'does not move to Done', nc)),
            'N2 mocked driver, serialisation UNMEASURED': bool(re.search(r'mock the Prisma driver', nc)) and bool(re.search(r'serialise[^\n]{0,80}\n?[^\n]{0,40}UNMEASURED|UNMEASURED', nc)),
            'N3 400-vs-404 residual': bool(re.search(r'deleted', nc)) and '404' in nc,
            'N4 preflight 12/15 not a pass': bool(re.search(r'12/15', body)) and bool(re.search(r'legs 3 4 8|legs \*\*3, 4 and 8\*\*', body)) and bool(re.search(r'NOT a pass|not 15 of 15', body)),
            'N5 docs merge-in from the gate prediction': bool(re.search(r'merge-in will be required', nc)) and bool(re.search(r'key-anchored', nc))}
    miss = [k for k, v in need.items() if not v]
    t.check('C6', bool(nc) and not miss, 'NOT COVERED section %d chars; missing %s' % (len(nc), miss))
    for lbl, rx in (('red-first', r'2 failed / 2 passed of 4[^\n]{0,20}'), ('suite', r'BEFORE 90 suites / 1063 tests[^\n]{0,30}\n?[^\n]{0,20}'), ('targeted', r'14 passed, 14 total'),
                    ('tamper rows', r'\|\s*\*\*(R1|R2|C2)\*\*\s*\|'), ('timing', r'auth` → \*\*76 / 75\*\*[^\n]{0,60}'), ('route lines', r'404s at `:\d+`\*\* and \*\*403s at\s+`:\d+`'),
                    ('read-400 line', r'400s on the read at `:\d+`'), ('repo line', r'documentRepo\.ts:\d+'), ('null claim', r'a `null` can only mean[^.]{0,80}')):
        f = re.findall(rx, body)
        t.info('FIG', '%s: %s' % (lbl, (repr(f[:4]) if isinstance(f[0], str) else repr(f[:4])) if f else 'ABSENT'))
    t.info('BYTES', 'body %d UTF-8 bytes / %d characters / sha256 %s (READY: "8,435 bytes", sha 9088067183c5e57f)' % (len(body.encode()), len(body), hashlib.sha256(body.encode()).hexdigest()[:16]))


GOOD = ('Refs KS-1278 — %s\n\nThe decision now lives IN the UPDATE. The row-lock alternative is not taken.\n\n'
        'Both platform-k documents: flow gains block `15.` between `14.` and `19.`. The cheat sheet has **no** readable ordering invariant, so the new '
        "section's position was **ruled**, not inferred.\n\n**Push preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran` / `legs 3 4 8 — local stack not up`. **12 of 15 is not 15 of 15**.\n\n"
        '### NOT COVERED (skill §5f)\n\n- **No live sweep**, so **KS 1278 does not move to Done on this change\'s account.**\n'
        '- The cells mock the Prisma driver; that two concurrent transactions really serialise on this WHERE is UNMEASURED.\n'
        '- Residual, filed as KS 1419: a document deleted between the read and the guarded write answers 400 where 404 belongs.\n'
        '- A docs-only merge-in will be required; its target tree comes from the gate\'s key-anchored prediction.\n')


def selftest():
    import io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    good = GOOD % K['ticket_url']; open(os.path.join(fx, 'c5_good_body.md'), 'w').write(good)
    def run(title, body, msg=''):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge(title, body, msg, t)
        return t
    t0 = run(K['subject'], good); ok = int(not t0.fails and t0.n == 8); total = 1
    print('SELFTEST %s T0 clean synthetic body (fixtures/c5_good_body.md): %d checked, fails %s' % ('OK' if ok else 'MISS', t0.n, t0.fails))
    arms = [('Refs removed', None, good.replace('Refs KS-1278 — ', ''), '', ['T1']),
            ('a second bold Refs', None, '**Refs KS-1278**\n' + good, '', ['T1']),
            ('URL removed', None, good.replace(K['ticket_url'], 'the ticket'), '', ['T1']),
            ('"Closes KS-1278"', None, good + 'Closes KS-1278\n', '', ['T2']),
            ('NEGATED "does not close KS-1419" in the body', None, good + 'This does not close KS-1419.\n', '', ['T2', 'T3']),
            ('"completes KS-1278" in the commit message', None, good, 'x\n\nThis completes KS-1278.\n', ['T2']),
            ('"fixes #1393"', None, good + 'fixes #1393\n', '', ['T2']),
            ('KS-1419 hyphenated', None, good.replace('KS 1419', 'KS-1419'), '', ['T3']),
            ('title with (#1393)', K['subject'] + ' (#1393)', good, '', ['T4']),
            ('residual NOT named ("being filed separately")', None, good.replace('filed as KS 1419', 'being filed separately'), '', ['T5']),
            ('Co-Authored-By', None, good + 'Co-Authored-By: X <x@invalid>\n', '', ['T6']),
            ('"ordering invariant" claim dropped', None, good.replace('has **no** readable ordering invariant', 'is ordered'), '', ['T7']),
            ('live-sweep line dropped', None, good.replace('- **No live sweep**, so **KS 1278 does not move to Done on this change\'s account.**\n', ''), '', ['C6']),
            ('mocked-driver line dropped', None, good.replace('- The cells mock the Prisma driver; that two concurrent transactions really serialise on this WHERE is UNMEASURED.\n', ''), '', ['C6']),
            ('preflight "not a pass" dropped', None, good.replace('**12 of 15 is not 15 of 15**', 'fine'), '', ['C6']),
            ('merge-in line dropped', None, good.replace("- A docs-only merge-in will be required; its target tree comes from the gate's key-anchored prediction.\n", ''), '', ['C6'])]
    for name, title, body, msg, want in arms:
        assert body != good or msg or title, 'tamper did not land: ' + name
        p = os.path.join(fx, 'c5_arm_%02d.md' % total); open(p, 'w').write(body)
        t = run(title or K['subject'], body, msg); total += 1; g = set(want) <= set(t.fails); ok += g
        print('SELFTEST %s %s (fixture %s): want FAIL %s | got %s' % ('OK' if g else 'MISS', name, os.path.basename(p), want, t.fails))
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
        open(os.path.join(d, 'pr%s_body.md' % K['pr']), 'w', encoding='utf-8').write(body)
        meta = {'title': title, 'head': p['head']['sha'], 'branch': p['head']['ref'], 'base': p['base']['ref'], 'base_sha': p['base']['sha'],
                'state': p['state'], 'merged': p.get('merged'), 'draft': p.get('draft'), 'body_bytes': len(body.encode()), 'updated_at': p.get('updated_at')}
        json.dump(meta, open(os.path.join(d, 'pr%s_meta.json' % K['pr']), 'w'), indent=1)
        print('API #%s head %s branch %s base %s (%s) state %s merged %s body %d bytes updated %s' % (K['pr'], meta['head'], meta['branch'], meta['base'],
              meta['base_sha'][:12], meta['state'], meta['merged'], meta['body_bytes'], meta['updated_at']))
    else:
        body = open(opt('--body'), encoding='utf-8').read(); title = opt('--title', K['subject'])
    t = Tally(); judge(title, body, msg, t); raise SystemExit(t.end())
