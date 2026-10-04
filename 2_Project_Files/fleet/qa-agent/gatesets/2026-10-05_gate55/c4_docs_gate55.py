#!/usr/bin/env python3
"""c4_docs_gate55.py — gate55 C4: the project skill's §4 applied to PR B's two doc blocks, from git objects (READ ONLY; prints only, writes
nothing — gate54a's c5 `static` wrote into its kit dir, N-1374-5; this one never does).
  D0  THE RULE at the BASE sha: SKILL.md blob == kit skill_blob_base and §4 carries the three clauses enforced here.
  D1  BOTH platform-k docs changed; 0 platform-s docs in the diff ("Never cross platforms").
  D2  ADDITIONS ONLY: 0 removed lines per doc (any removed line is PRINTED by number).
  D3  ONE SELF-CONTAINED KS 1015 BLOCK per doc: exactly ONE contiguous INSERT hunk whose text carries kit block_rx_new, opens (first
      non-blank added line) with a heading-shaped element (h2 / sec-head / diagram-title) and balances its own <div>..</div>.
  D3b PURELY ADDITIVE AFTER #1374's BLOCK: the insert sits AFTER the KS 1402 block's last base line (kit prev_blocks_base) and immediately
      before the doc's closing anchor (kit new_block_anchor_base: flow `<script>`, cheat `</body>`).
  D3c THE KS 1402 BLOCK IS BYTE-IDENTICAL: base lines first..last hash to kit sha256 (>= 20 lines: a 2-line span is vacuous, B 58th's own
      lesson), and the SAME bytes sit at the SAME line numbers in the head (the insert is after it).
  D4  TIMINGS: no removed line carries a timing; every ADDED line stating one (kit timing_rx, matched on HTML-UNESCAPED text so `375&nbsp;ms`
      is seen) has, within +/-3 added lines, a date (YYYY-MM-DD) AND a NAMED host (`host <Name>`, never the phrase "a host"), OR says it is a
      projection (§4: "Re-measure, or say explicitly that the figure is a projection").
  D5  THE TIMING GREP at BASE reproduced in both docs (case-insensitive line counts == kit timing_base_counts), every hit of the three suite
      terms INSIDE the KS 1402 block's lines; MUST-HIT control `auth` == kit timing_control_counts (a zero from a grep that cannot hit is
      not a measurement).
  D5b THE STABLE CLAIM at HEAD (the doc block's own wording): every hit of the three suite terms lies inside the KS 1402 block or the new
      KS 1015 block, 0 elsewhere; and the added lines carry 0 table rows/cells (`<tr` / `<td`), i.e. no timing row or tier budget was added.
  D6  NOTHING OUTSIDE THE KS 1015 BLOCK CHANGED: changed base lines outside the insert == 0 (D2 + D3 restated as one number per doc).
  D7  THE PR BODY (--body-file, the body the launch action saved) states the timing measurement: "0 hits outside the KS 1402 block" or
      "no stated timing", with the three terms and the must-hit control figures (68 / 67). Without --body-file D7 is NOT RUN (said so).
--selftest: plants into COPIES of the real texts (never a repo write), every arm must land on its named check.
--base-vs-base: BASE as the head — a control that MUST fail D1 and D3.
Usage: c4_docs_gate55.py --repo <clone or checkout> [--base sha] [--head sha] [--body-file f] [--selftest | --base-vs-base]
rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys, difflib, io, contextlib, html, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate55 import K, git, now, Checks, has_commit, show, blob_id

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head', K['expected_head']); BODYF = opt('--body-file')
for s in (BASE, HEAD):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s): print('REFUSING: %s is not a 40-hex commit present in %s' % (s, REPO)); raise SystemExit(2)
TRX = re.compile(K['timing_rx'], re.I); NEW = re.compile(K['block_rx_new'])
HOSTRX = re.compile(r'(?<!\ba )\bhost\b\s*(?:<[^>]+>\s*)*[`"\']?[A-Z0-9]')
HEADING = re.compile(r'<h[1-4][ >]|class="sec-head"|class="diagram-title"')
SUITE = [t for t in K['timing_base_counts'] if t in ('services/transfer', 'generate-openapi', 'check:openapi')]
MIN_LINES = 20
def plain(l): return html.unescape(re.sub(r'<[^>]+>', ' ', l))
def hunks(a, b):
    return [op for op in difflib.SequenceMatcher(None, a.split('\n'), b.split('\n'), autojunk=False).get_opcodes() if op[0] != 'equal']
def cnt(text, term, lines=None):
    rx = re.compile(term, re.I); L = text.split('\n')
    return [i + 1 for i, l in enumerate(L) if rx.search(l) and (lines is None or i + 1 in lines)]

def analyse(BD, HD, body, skill, plat_s, label):
    C = Checks()
    sk_ok = skill is not None and blob_id(REPO, BASE, K['skill']) == K['skill_blob_base']
    clauses = ["Every test change updates its platform's two HTML docs, in the same commit", 'the HTML docs carry the TIMINGS', 'If you changed which tests run, you changed a timing']
    have = [c for c in clauses if skill and c in skill]
    C.chk('D0 rule at base', sk_ok and len(have) == 3, '[%s] SKILL.md at %s blob == %s: %s | §4 clauses present %d of 3' % (label, BASE[:12], K['skill_blob_base'][:12], sk_ok, len(have)))
    changed = [d for d in K['docs'] if BD[d] != HD[d]]
    C.chk('D1 both docs, one platform', len(changed) == 2 and not plat_s, 'platform-k docs changed %d of 2 | platform-s docs in the diff %s' % (len(changed), plat_s or 'NONE'))
    allnew = {}
    for d in K['docs']:
        nm = os.path.basename(d)[:24]; bl = BD[d].split('\n'); hl = HD[d].split('\n'); H = hunks(BD[d], HD[d]); pb = K['prev_blocks_base'][d]
        rem = [(i + 1, bl[i]) for op, i1, i2, j1, j2 in H for i in range(i1, i2)]
        add = [(j + 1, hl[j]) for op, i1, i2, j1, j2 in H for j in range(j1, j2)]
        C.chk('D2 additions only %s' % nm, not rem, 'hunks %d | +%d / -%d%s' % (len(H), len(add), len(rem), '' if not rem else ' | REMOVED: ' + '; '.join('base:%d %r' % (n, l.strip()[:70]) for n, l in rem[:6])))
        blk = '\n'.join(l for _, l in add); opens = len(re.findall(r'<div\b', blk)); closes = len(re.findall(r'</div>', blk))
        first = next((l.strip()[:90] for _, l in add if l.strip()), None); one = len(H) == 1 and H[0][0] == 'insert'
        C.chk('D3 one KS 1015 block %s' % nm, one and bool(NEW.search(blk)) and first is not None and HEADING.search(first) is not None and opens == closes,
              'one contiguous INSERT hunk: %s %s | %s hits %d | opens with %r | <div %d / </div> %d' % (one, [(op, i1 + 1, j1 + 1, j2 - j1) for op, i1, i2, j1, j2 in H], K['block_rx_new'], len(NEW.findall(blk)), first, opens, closes))
        ins = H[0][1] if H else -1   # 0-based base index the insert precedes
        anchor = K['new_block_anchor_base'][d]; nxt = bl[ins].strip() if 0 <= ins < len(bl) else 'EOF'
        C.chk('D3b after the KS 1402 block %s' % nm, one and ins >= pb['last'] and nxt.startswith(anchor),
              'insert before base line %d (KS 1402 block ends at base %d: after it %s) | next base line %r starts with anchor %r: %s' % (ins + 1, pb['last'], ins >= pb['last'], nxt[:40], anchor, nxt.startswith(anchor)))
        span = '\n'.join(bl[pb['first'] - 1:pb['last']]); hs = hashlib.sha256(span.encode()).hexdigest()
        hspan = '\n'.join(hl[pb['first'] - 1:pb['last']])
        C.chk('D3c KS 1402 block byte-identical %s' % nm, pb['last'] - pb['first'] + 1 >= MIN_LINES and hs == pb['sha256'] and hspan == span and HD[d].count(span) == 1,
              'base %d-%d (%d lines, MIN %d) sha256 %s == kit: %s | same bytes at the same lines in head: %s | occurrences in head %d' % (pb['first'], pb['last'], pb['last'] - pb['first'] + 1, MIN_LINES, hs[:16], hs == pb['sha256'], hspan == span, HD[d].count(span)))
        tadd = [(n, l) for n, l in add if TRX.search(plain(l))]; AL = dict(add)
        win = lambda n: ' '.join(AL.get(k, '') for k in range(n - 3, n + 4))
        ok_t = lambda n: (re.search(r'\b20\d\d-\d\d-\d\d\b', win(n)) and HOSTRX.search(win(n))) or re.search(r'(?i)\bprojecti?on\b|\bprojected\b', plain(win(n)))
        bad = [(n, l) for n, l in tadd if not ok_t(n)]; trem = [(n, l) for n, l in rem if TRX.search(plain(l))]
        C.chk('D4 timings %s' % nm, not trem and not bad, 'removed lines with a timing %d | added lines stating a timing %d, without (date AND host) or "projection": %d%s' % (
            len(trem), len(tadd), len(bad), '' if not bad else ' ' + '; '.join('head:%d %r' % (n, plain(l).strip()[:80]) for n, l in bad[:4])))
        for n, l in tadd: print('INFO D4 %s head:%d timing %s | %r' % (nm, n, [m for m in TRX.findall(plain(l))][:3], plain(l).strip()[:100]))
        newlines = set(j + 1 for op, i1, i2, j1, j2 in H for j in range(j1, j2) if NEW.search('\n'.join(hl[j1:j2])))   # ONLY a hunk that IS a KS 1015 block
        allnew[d] = (newlines, add)
        print('INFO D6 %s: base lines changed outside the inserted block %d | inserted %d lines at head %s' % (nm, len(rem), len(add), '%d-%d' % (min(newlines), max(newlines)) if newlines else '-'))
    prev = {d: set(range(K['prev_blocks_base'][d]['first'], K['prev_blocks_base'][d]['last'] + 1)) for d in K['docs']}
    got = {t: [len(cnt(BD[d], t)) for d in K['docs']] for t in K['timing_base_counts']}
    inside = {t: [len(cnt(BD[d], t, prev[d])) for d in K['docs']] for t in SUITE}
    ctl = [len(cnt(BD[d], K['timing_control_term'])) for d in K['docs']]
    want = {t: list(v) for t, v in K['timing_base_counts'].items()}
    C.chk('D5 timing grep at base', got == want and all(inside[t] == got[t] for t in SUITE) and ctl == K['timing_control_counts'] and all(c > 0 for c in ctl),
          '[flow, cheat] at %s: %s | suite-term hits INSIDE the KS 1402 block %s | kit %s | MUST-HIT %r %s (kit %s)' % (BASE[:12], got, inside, want, K['timing_control_term'], ctl, K['timing_control_counts']))
    out_h = {}; rows = 0
    for d in K['docs']:
        newl, add = allnew[d]; pb = K['prev_blocks_base'][d]; n_pb = pb['last'] - pb['first'] + 1
        bl = BD[d].split('\n'); hl = HD[d].split('\n'); want_span = bl[pb['first'] - 1:pb['last']]
        at = next((i for i in range(len(hl) - n_pb + 1) if hl[i:i + n_pb] == want_span), None)   # LOCATE the KS 1402 block in the head (never assume its line numbers)
        hp = set(range(at + 1, at + n_pb + 1)) if at is not None else set()
        out_h[os.path.basename(d)[:5]] = {t: [n for n in cnt(HD[d], t) if n not in hp and n not in newl] for t in SUITE}
        rows += sum(len(re.findall(r'<t[rd]\b', l)) for _, l in add)
    nout = sum(len(v) for x in out_h.values() for v in x.values())
    C.chk('D5b stable claim at head', nout == 0 and rows == 0, 'suite-term hits OUTSIDE the KS 1402 and KS 1015 blocks at %s: %d %s | table rows/cells in the added lines: %d' % (HEAD[:12], nout, {k: {t: v for t, v in x.items() if v} for k, x in out_h.items()}, rows))
    if body is None:
        print('NOT RUN D7 PR body statement: no --body-file given (the launch action saves it; the gate must pass it)')
    else:
        stmt = re.search(r'(?i)0 hits outside the KS[- ]1402 block|no stated timing', body) is not None
        terms = [t for t in SUITE if t in body]; c68 = re.search(r'`?auth`?\D{0,20}68\D{1,6}67', body) is not None
        C.chk('D7 PR body timing statement', stmt and len(terms) == 3 and c68, 'statement present %s | terms named %d of 3 %s | must-hit control auth 68 / 67 stated %s' % (stmt, len(terms), terms, c68))
    return C

def load(sha):
    T = {}
    for d in K['docs']:
        T[d] = show(REPO, sha, d)
        if T[d] is None: raise SystemExit('REFUSING: %s absent at %s' % (d, sha[:12]))
    return T
print('c4_docs_gate55 %s | repo %s | base %s | head %s | body %s | mode %s' % (now(), REPO, BASE[:12], HEAD[:12], BODYF or 'NONE', 'selftest' if '--selftest' in A else 'base-vs-base' if '--base-vs-base' in A else 'gate'))
BD = load(BASE); SK = show(REPO, BASE, K['skill']); BODY = open(BODYF, encoding='utf-8').read() if BODYF else None
def plat_s(sha): return sorted(set(git(REPO, 'diff', '--name-only', BASE, sha).splitlines()) & set(K['docs_platform_s']))
if '--base-vs-base' in A:
    C = analyse(BD, dict(BD), BODY, SK, plat_s(BASE), 'BASE as head'); n = C.nfail()
    print('C4 DOCS %s (base-vs-base, a control: D1 and D3 MUST fail): %d FAIL of %d | failed %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), C.failed())); raise SystemExit(1 if n else 0)
HD = load(HEAD); PS = plat_s(HEAD)
if '--selftest' in A:
    F, Q = K['docs']
    def plant(d, fn):
        t = dict(HD); t[d] = fn(t[d]); return t
    def at_line(s, n, fn):
        L = s.split('\n'); L[n - 1] = fn(L[n - 1]); return '\n'.join(L)
    pf = K['prev_blocks_base'][F]; pq = K['prev_blocks_base'][Q]
    fl = HD[F].split('\n'); i10 = next(i for i, l in enumerate(fl) if l.strip().startswith('<h2>10.'))
    newblk = '\n'.join(fl[i10:fl.index('    <script>', i10)])
    def move_before(s):   # the KS 1015 block cut from its place and put BEFORE the KS 1402 block
        s2 = s.replace(newblk + '\n', '', 1); L = s2.split('\n'); return '\n'.join(L[:pf['first'] - 1] + newblk.split('\n') + L[pf['first'] - 1:])
    SB = BODY if BODY is not None else open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sim', 'SIM_body_ok.md'), encoding='utf-8').read()
    arms = [
        ('T0 real head', HD, SB, PS, None),
        ('T1 only one doc changed', plant(F, lambda s: BD[F]), SB, PS, 'D1'),
        ('T2 a platform-s doc in the diff', HD, SB, [K['docs_platform_s'][0]], 'D1'),
        ('T3 a KS 1402 block line removed', plant(Q, lambda s: '\n'.join(l for i, l in enumerate(s.split('\n')) if i != pq['first'] + 2)), SB, PS, 'D2'),
        ('T4 one trailing space inside the KS 1402 block', plant(F, lambda s: at_line(s, pf['first'] + 5, lambda l: l + ' ')), SB, PS, 'D3c'),
        ('T5 the new block loses its KS 1015 tag', plant(Q, lambda s: s.replace('KS-1015', 'KS-9999').replace('KS 1015', 'KS 9999')), SB, PS, 'D3'),
        ('T6 a second hunk elsewhere', plant(Q, lambda s: s.replace('</head>', '<!-- g55 plant -->\n</head>', 1)), SB, PS, 'D3'),
        ('T7 an added timing with no host', plant(F, lambda s: s.replace('host\n        <strong>Kamils-Mac-Studio</strong>', 'machine\n        <strong>X</strong>')), SB, PS, 'D4'),
        ('T8 an &nbsp; timing with no date or host', plant(F, lambda s: s.replace('<strong>It NARROWS KS-1015', 'It runs in 912&nbsp;ms. <strong>It NARROWS KS-1015', 1)), SB, PS, 'D4'),
        ('T9 the KS 1015 block inserted BEFORE the KS 1402 block', plant(F, move_before), SB, PS, 'D3b'),
        ('T10 an unbalanced block (closes an existing div)', plant(Q, lambda s: s.replace('    <div class="sec-head">\n      📜', '    </div>\n    <div class="sec-head">\n      📜', 1)), SB, PS, 'D3'),
        ('T11 a suite term added OUTSIDE both blocks', plant(F, lambda s: s.replace('</head>', '<!-- npm run check:openapi -->\n</head>', 1)), SB, PS, 'D5b'),
        ('T12 a timing stated as a projection (allowed)', plant(F, lambda s: s.replace('<strong>It NARROWS KS-1015', 'A projection: about 5 s per CI run. <strong>It NARROWS KS-1015', 1)), SB, PS, None),
        ('T13 the body drops the timing statement', HD, re.sub(r'(?i)0 hits outside the KS[- ]1402 block|no stated timing', 'nothing', SB), PS, 'D7'),
        ('T14 a timing row (<tr>) added inside the block', plant(F, lambda s: s.replace('<strong>It NARROWS KS-1015', '<table><tr><td>x</td></tr></table><strong>It NARROWS KS-1015', 1)), SB, PS, 'D5b'),
    ]
    ok = 0
    for name, hd, body, ps, want in arms:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): C = analyse(BD, hd, body, SK, ps, name)
        f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
        ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        for l in buf.getvalue().splitlines():
            if l.startswith('FAIL') or (want is None and not good): print('    ' + l[:260])
    print('SELFTEST %s %d of %d (body: %s)' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms), BODYF or 'sim/SIM_body_ok.md')); raise SystemExit(0 if ok == len(arms) else 1)
C = analyse(BD, HD, BODY, SK, PS, 'HEAD'); n = C.nfail()
print('C4 DOCS %s: %d FAIL of %d checks%s | base %s | head %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), '' if BODY is not None else ' (D7 NOT RUN: no body file)', BASE[:12], HEAD[:12]))
raise SystemExit(1 if n else 0)
