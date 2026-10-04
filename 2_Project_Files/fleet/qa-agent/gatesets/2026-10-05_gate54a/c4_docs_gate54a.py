#!/usr/bin/env python3
"""c4_docs_gate54a.py — gate54a C4: the project skill's §4 ("Documentation that must move with the code") applied to the diff, from git objects.
  D0 the RULE, read at the BASE sha: .claude/skills/secuura-test-discipline/SKILL.md blob == kit skill_blob_base, and §4 carries the three
     clauses this check enforces (both docs in the same commit; the docs carry the TIMINGS; "If you changed which tests run, you changed a timing").
  D1 BOTH platform-k docs changed (kit docs), and 0 platform-s docs (kit docs_platform_s) — "Never cross platforms".
  D2 ADDITIONS ONLY: removed lines per doc == 0; any removed line is PRINTED by number (the commission: "additions only or each removed line named").
  D3 ONE SELF-CONTAINED KS 1402 BLOCK per doc: the added lines form exactly ONE contiguous hunk, carry kit block_rx, open with a heading-shaped
     element (h2 / sec-head / diagram-title), and balance their own <div>…</div> (a block that closes an existing element is not self-contained).
  D4 NO TIMING ROW CHANGED WITHOUT A RE-MEASURE: no removed or replaced line carries a timing figure (kit timing_rx); every ADDED line that states
     one also names a date (YYYY-MM-DD) and a NAMED host (`host <Name>`, not the phrase "a host") within 3 added lines either side (a wrapped HTML sentence)
     (§4: "a figure without a host is meaningless").
  D5 THE TIMING GREP, reproduced at BASE in both docs (case-insensitive line counts): kit timing_suite_terms vs kit timing_claim_counts, with the
     MUST-HIT control term (`auth`) — a zero from a grep that cannot hit is not a measurement.
  D6 THE PR BODY says no stated timing covers these suites, with its grep: the literal kit body_timing_phrase_rx (reported LITERAL yes/no), or the
     equivalent sentence (reported SEMANTIC), plus the grep terms with their counts and the must-hit control figures in the body.
  INFO: each block's hunk position (for THE DOC RULE: the second PR to merge rebases keeping BOTH blocks), and the timing lines found.
--body-file <f> (default gh_body_<expected_pr>.md beside this script, written by the census).  --selftest: plants into copies of the real
texts (never a repo write). --base-vs-base: BASE as the head (must FAIL D1/D3).
Usage: c4_docs_gate54a.py --repo <clone> [--base sha] [--head sha] [--body-file f] [--selftest | --base-vs-base]   rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys, difflib, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate54a import K, G, git, now, Checks, has_commit, show

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head', K['expected_head'])
BODYF = opt('--body-file', os.path.join(G, 'gh_body_%s.md' % K['expected_pr']))
for s in (BASE, HEAD):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s): print('REFUSING: %s is not a 40-hex commit present in %s' % (s, REPO)); raise SystemExit(2)
TRX = re.compile(K['timing_rx'], re.I); BRX = re.compile(K['block_rx'])
HOSTRX = re.compile(r'(?<!\ba )\bhost\b\s*(?:<[^>]+>\s*)*[`"\']?[A-Z0-9]')   # `host <Name>` naming one; never the phrase "a host is meaningless"
HEADING = re.compile(r'<h[1-4][ >]|class="sec-head"|class="diagram-title"')

def hunks(a, b):
    sm = difflib.SequenceMatcher(None, a.split('\n'), b.split('\n'), autojunk=False)
    return [op for op in sm.get_opcodes() if op[0] != 'equal']

def analyse(BD, HD, body, skill, plat_s_changed, label):
    C = Checks()
    sk_ok = skill is not None and git(REPO, 'rev-parse', '%s:%s' % (BASE, K['skill'])).strip() == K['skill_blob_base']
    clauses = ['Every test change updates its platform\'s two HTML docs, in the same commit', 'the HTML docs carry the TIMINGS', 'If you changed which tests run, you changed a timing']
    have = [c for c in clauses if skill and c in skill]
    C.chk('D0 rule at base', sk_ok and len(have) == 3, '[%s] SKILL.md at %s blob == %s: %s | §4 clauses present %d of 3%s' % (label, BASE[:12], K['skill_blob_base'][:12], sk_ok, len(have), '' if len(have) == 3 else ' missing %s' % [c for c in clauses if c not in have]))
    changed = [d for d in K['docs'] if BD[d] != HD[d]]
    C.chk('D1 both docs, one platform', len(changed) == 2 and not plat_s_changed, 'platform-k docs changed %d of 2 %s | platform-s docs changed %s' % (len(changed), [os.path.basename(d) for d in changed], plat_s_changed or 'NONE'))
    for d in K['docs']:
        nm = os.path.basename(d)[:28]; bl = BD[d].split('\n'); hl = HD[d].split('\n'); H = hunks(BD[d], HD[d])
        rem = [(i + 1, bl[i]) for op, i1, i2, j1, j2 in H for i in range(i1, i2)]
        add = [(j + 1, hl[j]) for op, i1, i2, j1, j2 in H for j in range(j1, j2)]
        C.chk('D2 additions only %s' % nm, not rem, 'hunks %d | +%d / -%d%s' % (len(H), len(add), len(rem), '' if not rem else ' | REMOVED: ' + '; '.join('base:%d %r' % (n, l.strip()[:70]) for n, l in rem[:8])))
        blk = '\n'.join(l for _, l in add)
        opens = len(re.findall(r'<div\b', blk)); closes = len(re.findall(r'</div>', blk)); head = next((l.strip()[:80] for _, l in add if HEADING.search(l)), None)
        one = len(H) == 1 and H[0][0] == 'insert'
        C.chk('D3 one KS 1402 block %s' % nm, one and bool(BRX.search(blk)) and head is not None and opens == closes,
              'one contiguous INSERT hunk: %s (hunks %s) | %s hits %d | first heading %r | <div %d / </div> %d balanced %s' % (
                  one, [(op, i1 + 1, j1 + 1, j2 - j1) for op, i1, i2, j1, j2 in H], K['block_rx'], len(BRX.findall(blk)), head, opens, closes, opens == closes))
        if H: print('INFO D3 %s block inserted before base line %d (head lines %d-%d); THE DOC RULE: a co-tenant block at the same anchor conflicts textually — keep BOTH' % (nm, H[0][1] + 1, H[0][3] + 1, H[0][4]))
        trem = [(n, l) for n, l in rem if TRX.search(l)]
        tadd = [(n, l) for n, l in add if TRX.search(re.sub(r'<[^>]+>', '', l))]
        AL = dict(add)   # a wrapped HTML sentence: the date and host may sit on the neighbouring ADDED lines (window +/- 3)
        win = lambda n: ' '.join(AL.get(k, '') for k in range(n - 3, n + 4))
        bad = [(n, l) for n, l in tadd if not (re.search(r'\b20\d\d-\d\d-\d\d\b', win(n)) and HOSTRX.search(win(n)))]
        C.chk('D4 timings %s' % nm, not trem and not bad, 'removed/replaced lines carrying a timing %d | added lines stating a timing %d, of which without a date AND a host within +/-3 added lines: %d%s' % (
            len(trem), len(tadd), len(bad), '' if not bad else ' ' + '; '.join('head:%d %r' % (n, re.sub(r'<[^>]+>', '', l).strip()[:90]) for n, l in bad[:4])))
        for n, l in tadd:
            txt = re.sub(r'<[^>]+>', '', l); print('INFO D4 %s head:%d timing %s | %r' % (nm, n, [m[0] for m in TRX.findall(txt)][:3], txt.strip()[:110]))
    got = {}
    for t in K['timing_suite_terms'] + [K['timing_control_term']]:
        got[t] = [sum(1 for l in BD[d].split('\n') if t.lower() in l.lower()) for d in K['docs']]
    want = {k: list(v) for k, v in K['timing_claim_counts'].items()}
    ctl = got[K['timing_control_term']]
    C.chk('D5 timing grep at base', all(got[t] == [0, 0] for t in K['timing_suite_terms']) and all(c > 0 for c in ctl),
          'line counts [flow, cheat] at %s: %s | MUST-HIT control %r %s | builder %s | agree with builder %s' % (BASE[:12], {t: got[t] for t in K['timing_suite_terms']}, K['timing_control_term'], ctl, want, got == want))
    lit = re.search(K['body_timing_phrase_rx'], body or '', re.I) is not None
    sem = re.search(r'no (tier budget or )?timing row covers the auth vitest suite|no stated timing covers', body or '', re.I) is not None
    terms = [t for t in K['timing_suite_terms'] if re.search(r'`%s`\s*\*\*0\*\*' % re.escape(t), body or '')]
    ctlb = re.search(r'`auth`\s*52\b.*?59', body or '', re.S) is not None
    C.chk('D6 PR body timing statement', (lit or sem) and len(terms) == len(K['timing_suite_terms']) and ctlb,
          'LITERAL %r: %s | SEMANTIC equivalent: %s | grep terms stated with 0: %d of %d %s | must-hit control (`auth` 52 / 59) stated: %s%s' % (
              K['body_timing_phrase_rx'], lit, sem, len(terms), len(K['timing_suite_terms']), terms, ctlb, '' if lit else '  <- the commission\'s words are NOT verbatim in the body: the gate rules whether the equivalent suffices'))
    return C

def load(sha):
    T = {}
    for d in K['docs']:
        T[d] = show(REPO, sha, d)
        if T[d] is None: raise SystemExit('REFUSING: %s absent at %s' % (d, sha[:12]))
    return T

print('c4_docs_gate54a %s | repo %s | base %s | head %s | body %s | mode %s' % (now(), REPO, BASE[:12], HEAD[:12], os.path.basename(BODYF), 'selftest' if '--selftest' in A else 'base-vs-base' if '--base-vs-base' in A else 'gate'))
BD = load(BASE); SK = show(REPO, BASE, K['skill']); BODY = open(BODYF, encoding='utf-8').read() if os.path.isfile(BODYF) else ''
if not BODY: print('INFO no PR body file (%s): D6 will FAIL' % BODYF)
def plat_s(sha):
    names = git(REPO, 'diff', '--name-only', BASE, sha).splitlines(); return sorted(set(names) & set(K['docs_platform_s']))
if '--base-vs-base' in A:
    C = analyse(BD, dict(BD), BODY, SK, plat_s(BASE), 'BASE as head'); n = C.nfail()
    print('C4 DOCS %s (base-vs-base, a control: D1 and D3 MUST fail): %d FAIL of %d' % ('PASS' if n == 0 else 'FAIL', n, len(C.res))); raise SystemExit(1 if n else 0)
HD = load(HEAD); PS = plat_s(HEAD)
if '--selftest' in A:
    F, Q = K['docs']
    def plant(d, fn):
        t = dict(HD); t[d] = fn(t[d]); return t
    def rm_first_base_line_with(s, needle):
        L = s.split('\n'); i = next(i for i, l in enumerate(L) if needle in l); return '\n'.join(L[:i] + L[i + 1:])
    def retime(s):
        L = s.split('\n'); bl = BD[Q].split('\n'); i = next(i for i, l in enumerate(L) if TRX.search(re.sub(r'<[^>]+>', '', l)) and l in bl)
        L[i] = re.sub(r'(\d+)(\s?(ms|s|min))', lambda m: str(int(m.group(1)) + 1) + m.group(2), L[i], count=1); return '\n'.join(L)
    arms = [
        ('T0 real head', HD, BODY, PS, None),
        ('T1 only one doc changed', plant(F, lambda s: BD[F]), BODY, PS, 'D1'),
        ('T2 a platform-s doc in the diff', HD, BODY, [K['docs_platform_s'][0]], 'D1'),
        ('T3 a pre-existing line removed', plant(Q, lambda s: rm_first_base_line_with(s, '<div')), BODY, PS, 'D2'),
        ('T4 an existing timing row edited (no re-measure)', plant(Q, retime), BODY, PS, 'D4'),
        ('T5 the block loses its KS 1402 tag', plant(F, lambda s: s.replace('KS-1402', 'KS-9999').replace('KS 1402', 'KS 9999')), BODY, PS, 'D3'),
        ('T6 a second hunk elsewhere', plant(Q, lambda s: s.replace('</head>', '<!-- g54a plant -->\n</head>', 1)), BODY, PS, 'D3'),
        ('T7 an added timing with no host', plant(Q, lambda s: s.replace('host <code>Kamils-Mac-Studio</code>', 'machine X').replace('host Kamils-Mac-Studio', 'machine X')), BODY, PS, 'D4'),
        ('T8 the body drops the timing statement', HD, re.sub(r'(?i)no tier budget or timing row covers the auth vitest suite', 'the suite is fine', BODY), PS, 'D6'),
        ('T9 an unbalanced block (closes an existing div)', plant(F, lambda s: s.replace('<h2>9. Auth surface', '</div>\n    <h2>9. Auth surface', 1)), BODY, PS, 'D3'),
    ]
    ok = 0
    for name, hd, body, ps, want in arms:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): C = analyse(BD, hd, body, SK, ps, name)
        f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
        ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        for l in buf.getvalue().splitlines():
            if l.startswith('FAIL') or want is None: print('    ' + l[:300])
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); raise SystemExit(0 if ok == len(arms) else 1)
C = analyse(BD, HD, BODY, SK, PS, 'HEAD'); n = C.nfail()
print('C4 DOCS %s: %d FAIL of %d checks | base %s | head %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), BASE[:12], HEAD[:12]))
raise SystemExit(1 if n else 0)
