#!/usr/bin/env python3
"""c5_prtext_gate62.py — C5 PR TEXT for #1387 (KS-1388 s1, a NARROWING PR: KS-1388 must NOT move to Done on it).

  --fetch <dir>   read-only GitHub GET of pulls/1387 (GH_TOKEN by name, never printed); writes <dir>/pr1387_body.md and
                  <dir>/pr1387_meta.json (title, head sha, state, base, merged); then judges them.
  --body <file> --title <text> [--message <file>]   judge offline (the self-test fixtures use this).
  T1  exactly ONE `Refs KS-1388` in the body (markdown emphasis allowed), and the ticket URL https://linear.app/secuura/issue/KS-1388
  T2  CLOSING WORDS: 0 Linear magic-word references (close/closes/closed/closing, fix…, resolve…, complete… followed within the same
      sentence by a hyphenated KS key — Linear does NOT parse negation, so "does not close KS-1388" COUNTS) in title, body and commit
      message; 0 GitHub `<keyword> #n`
  T3  the only hyphenated KS key in title + body is KS-1388
  T4  title == the kit subject (74 chars), no `(#`
  T5  the narrowing is stated: section 1 only, sections 2 and 3 untouched, live sweep owed / NOT COVERED, KS-1388 not moved to Done
  T6  0 Co-Authored-By lines in the body (a squash may carry the body into the landed message)
  T7  the body does not quote the FABRICATED tree 0c0f8e5e…; any id it labels END_TREE is fd6eb92cf942… (other tree ids: INFO)
  INFO the figures the body states (4 -> 6, 67, rc 1 / 4 passed / 2 failed, preflight legs) are printed for the gate to compare with C3.
--selftest  synthetic bodies in fixtures/ (beside this file): T0 a clean body passes; every arm must FAIL its named check.
rc 0 all PASS / rc 1 any FAIL or 0 checked."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate62 import K, Tally, gh_get, HERE, SCRATCH

CLOSE_RX = re.compile(r'\b(close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?|completing)\b[^.\n]{0,60}?\bKS-\d+', re.I)
GHCLOSE_RX = re.compile(r'\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#\d+', re.I)
KEY_RX = re.compile(r'\bKS-\d+\b')


def judge(title, body, message, t):
    refs = re.findall(r'\bRefs\W{0,4}KS-1388\b', body)   # markdown emphasis allowed (`**Refs KS-1388**`): ex1 history
    t.check('T1', len(refs) == 1 and K['ticket_url'] in body, '`Refs KS-1388` lines %d (want 1); ticket URL present %s' % (len(refs), K['ticket_url'] in body))
    hits = []
    for where, txt in (('title', title), ('body', body), ('message', message or '')):
        hits += ['%s: %r' % (where, m.group(0)[:90]) for m in CLOSE_RX.finditer(txt)]
        hits += ['%s: %r' % (where, m.group(0)) for m in GHCLOSE_RX.finditer(txt)]
    t.check('T2', not hits, 'closing references %d %s' % (len(hits), hits))
    keys = sorted(set(KEY_RX.findall(title + '\n' + body)))
    t.check('T3', keys == ['KS-1388'], 'hyphenated keys in title+body %s (want only KS-1388)' % keys)
    t.check('T4', title == K['subject'] and '(#' not in title, 'title %r %d chars (want the kit subject, no "(#")' % (title, len(title)))
    need = {'section 1 only': bool(re.search(r'(§|section |s)1\b[^\n]{0,40}only|only[^\n]{0,20}(§|section )1\b', body, re.I)),
            'sections 2/3 untouched': bool(re.search(r'(§|sections? )2 and (§|section )?3[^\n]{0,120}(untouched|not touched|out of scope)', body, re.I | re.S)),
            'live sweep owed': bool(re.search(r'live sweep', body, re.I)),
            'not covered / NOT run': bool(re.search(r'not covered|not run', body, re.I)),
            'not Done': bool(re.search(r'(not|never)[^\n]{0,40}\bDone\b|\bDone\b[^\n]{0,40}\bnot\b', body))}
    miss = [k for k, v in need.items() if not v]
    t.check('T5', not miss, 'narrowing statements missing %s' % miss)
    co = len(re.findall(r'(?im)^co-authored-by:', body))
    t.check('T6', co == 0, 'Co-Authored-By lines in body %d' % co)
    fab = K['fabricated_tree_prefix'] in body
    trees = sorted(set(re.findall(r'(?i)end_tree\W{0,6}`?([0-9a-f]{12,40})', body)))   # END_TREE-labelled only: ex1 history (04d226 is the independent-apply tree)
    t.info('TREES', 'every tree-like id quoted: %s' % sorted(set(re.findall(r'(?i)tree\W{0,6}`?([0-9a-f]{12,40})', body))))
    badt = [x for x in trees if not K['end_tree'].startswith(x) and not K['develop_tree'].startswith(x)]
    t.check('T7', not fab and not badt, 'fabricated %s… present %s; tree ids quoted %s; neither END_TREE nor develop tree %s' % (
        K['fabricated_tree_prefix'], fab, trees, badt))
    for lbl, rx in (('4 -> 6', r'4\s*(->|→|&rarr;|to)\s*6'), ('67', r'\b67\b'), ('rc 1', r'rc 1'), ('4 passed / 2 failed', r'4 passed\s*/\s*2 failed'),
                    ('preflight', r'preflight[^\n]{0,160}')):
        m = re.search(rx, body, re.I)
        t.info('FIG', '%s: %s' % (lbl, repr(m.group(0)[:160]) if m else 'ABSENT'))


def selftest():
    import io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    good = ('Covers KS 1388 section 1 only; sections 2 and 3 are untouched.\n\n## Test Evidence\nKS 971 suite 4 -> 6, 67 suites, red-first rc 1, 4 passed / 2 failed.\n'
            'END_TREE fd6eb92cf942\n\n## NOT COVERED\nNo live sweep, so KS 1388 does not move to Done.\n\n'
            'Ticket: https://linear.app/secuura/issue/KS-1388\n\nRefs KS-1388\n')
    open(os.path.join(fx, 'c5_good_body.md'), 'w').write(good)
    def run(title, body, msg=''):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge(title, body, msg, t)
        return t
    t0 = run(K['subject'], good); ok = int(not t0.fails); total = 1
    print('SELFTEST %s T0 clean synthetic body (fixtures/c5_good_body.md): %d checked, fails %s' % ('OK' if not t0.fails else 'MISS', t0.n, t0.fails))
    arms = [('Refs removed', None, good.replace('Refs KS-1388\n', ''), '', ['T1']),
            ('a second Refs', None, good + 'Refs KS-1388\n', '', ['T1']),
            ('URL removed', None, good.replace(K['ticket_url'], 'the ticket'), '', ['T1']),
            ('NEGATED closing phrase "does not close KS-1388"', None, good + 'This does not close KS-1388.\n', '', ['T2']),
            ('"Fixes KS-1388" in the commit message', None, good, 'x\n\nFixes KS-1388\n', ['T2']),
            ('"closes #1387"', None, good + 'closes #1387\n', '', ['T2']),
            ('KS-971 hyphenated', None, good.replace('KS 971', 'KS-971'), '', ['T3']),
            ('title with (#1387)', K['subject'] + ' (#1387)', good, '', ['T4']),
            ('sections 2/3 statement removed', None, good.replace('sections 2 and 3 are untouched', 'more later'), '', ['T5']),
            ('live sweep removed', None, good.replace('No live sweep, so', 'So'), '', ['T5']),
            ('Co-Authored-By', None, good + 'Co-Authored-By: X <x@invalid>\n', '', ['T6']),
            ('the FABRICATED tree', None, good.replace('fd6eb92cf942', '0c0f8e5e1234'), '', ['T7']),
            ('a WRONG END_TREE', None, good.replace('END_TREE fd6eb92cf942', 'END_TREE 04d226e93b48'), '', ['T7']),
            ('a bold Refs PLUS a bare Refs', None, '**Refs KS-1388** - x\n' + good, '', ['T1'])]
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
        p = gh_get('pulls/' + K['pr'])
        body = p.get('body') or ''; title = p['title']
        open(os.path.join(d, 'pr1387_body.md'), 'w', encoding='utf-8').write(body)
        meta = {'title': title, 'head': p['head']['sha'], 'branch': p['head']['ref'], 'base': p['base']['ref'], 'base_sha': p['base']['sha'],
                'state': p['state'], 'merged': p.get('merged'), 'draft': p.get('draft'), 'body_bytes': len(body.encode()), 'user': (p.get('user') or {}).get('login')}
        json.dump(meta, open(os.path.join(d, 'pr1387_meta.json'), 'w'), indent=1)
        print('API #%s head %s branch %s base %s (%s) state %s merged %s body %d bytes' % (K['pr'], meta['head'], meta['branch'], meta['base'], meta['base_sha'][:12],
              meta['state'], meta['merged'], meta['body_bytes']))
    else:
        body = open(opt('--body'), encoding='utf-8').read(); title = opt('--title', K['subject'])
    t = Tally(); judge(title, body, msg, t); raise SystemExit(t.end())
