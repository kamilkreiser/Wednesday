#!/usr/bin/env python3
"""c5_docs_gateD2.py — gateD2 C5: skill §4 on the two platform-k docs + the verify RESPONSE SHAPE, from git objects (a NEW COPY of
c4_docs_gate54a.py, re-keyed for KS 1404, plus the shape check and THE DOC RULE's keep-both check).
  D0 the RULE at the BASE sha: SKILL.md blob == kit skill_blob_base and §4's three clauses present.
  D1 both platform-k docs changed, 0 platform-s docs.            D2 ADDITIONS ONLY (each removed line printed).
  D3 ONE self-contained KS 1404 block per doc: one contiguous INSERT hunk, carries KS[- ]1404, opens with a heading, balanced <div>s.
  D4 every ADDED line stating a timing names a date (YYYY-MM-DD) AND a host (`on <Host>` / `host <Host>`) within +/-3 added lines.
  D5 FIGURES: the blocks' cell count, suite before / after and red-first triple are equal ACROSS the two docs, equal to the commit
     message's, and — with --measured cells=N,base=F/T,head=F/T — equal to what THIS GATE measured in C3 (re-measured, not copied).
     The wall clock is host-specific: printed, never judged against another host.
  D6 RESPONSE SHAPE: index.ts verifyTimestamp's declared return keys == kit response_keys (verified/timestamp/tsaUrl/reason) AND the
     OpenAPI module declares the same key set for the verify response; cell 14 asserts the exact refusal key set ['reason','verified'] and
     cell 13 asserts `reason` ABSENT on the DB-row branch (static read of the test file; C3 runs them).
  D7 THE DOC RULE (co-tenants): every line carrying KS[- ]1402 (or kit co_tenant keys) at develop is present, in order, at head — the
     second PR to merge keeps BOTH blocks. Vacuous (0 lines) while develop == the pre-#1374 base: printed as such.
  INFO: whether each block names the committed bundle path (Wednesday's 14:2xZ second commit), and its anchor line.
--body-file f: the PR body (default: none -> D5 compares to the HEAD commit messages instead). --selftest (plants into copies of the head
texts) and --base-vs-base (must FAIL D1/D3).
Usage: c5_docs_gateD2.py --repo <clone> --head <sha> [--base sha] [--measured cells=25,base=5/44,head=6/69] [--selftest|--base-vs-base]"""
import os, re, sys, difflib, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gateD2 import K, git, now, Checks, has_commit, show, code_lines

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--head' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head')
for s_ in (BASE, HEAD):
    if not re.fullmatch(r'[0-9a-f]{40}', s_ or '') or not has_commit(REPO, s_): print('REFUSING: %s is not a 40-hex commit present in %s' % (s_, REPO)); raise SystemExit(2)
TRX = re.compile(K['timing_rx'], re.I); BRX = re.compile(K['block_rx'])
HOSTRX = re.compile(r'\b(?:on|host)\s+(?:<[^>]+>\s*)*[`"\']?[A-Z][A-Za-z0-9-]{2,}')
HEADING = re.compile(r'<h[1-4][ >]|class="sec-head"|class="diagram-title"')
MEAS = dict(kv.split('=', 1) for kv in (opt('--measured') or '').split(',') if '=' in kv)


def hunks(a, b):
    return [op for op in difflib.SequenceMatcher(None, a.split('\n'), b.split('\n'), autojunk=False).get_opcodes() if op[0] != 'equal']


def txt(s): return re.sub(r'\s+', ' ', re.sub(r'&[a-z]+;', ' ', re.sub(r'<[^>]+>', ' ', s)))


def figures(block):
    t = txt(block); f = {}
    m = re.search(r'Cells in the KS-1404 file\s+(\d+)|KS-1404 cells\s+(\d+)|#\s*(\d+) cells', t); f['cells'] = next((g for g in m.groups() if g), None) if m else None
    m = re.search(r'before\s*(?:&rarr;|→)?\s*(?:after\s*)?(\d+) files / (\d+) tests', t); f['before'] = '%s/%s' % m.groups() if m else None
    al = re.findall(r'(\d+) files / (\d+) tests', t); f['after'] = '%s/%s' % al[-1] if al else None
    m = re.search(r'(\d+) red, (\d+) pass, (\d+) skipped of (\d+)', t); f['redfirst'] = '%s/%s/%s/%s' % m.groups() if m else None
    m = re.search(r'wall clock (\d+)\s*[-–\s]\s*(\d+) ms', t); f['wall'] = '%s-%s ms' % m.groups() if m else None
    return f


def analyse(BD, HD, skill, plat_s, msgs, label, dev_docs=None):
    C = Checks()
    sk_ok = skill is not None and git(REPO, 'rev-parse', '%s:%s' % (BASE, K['skill'])).strip() == K['skill_blob_base']
    clauses = ['Every test change updates its platform\'s two HTML docs, in the same commit', 'the HTML docs carry the TIMINGS', 'If you changed which tests run, you changed a timing']
    have = [c for c in clauses if skill and c in skill]
    C.chk('D0 rule at base', sk_ok and len(have) == 3, '[%s] SKILL.md at %s blob == %s: %s | §4 clauses %d of 3' % (label, BASE[:12], K['skill_blob_base'][:12], sk_ok, len(have)))
    changed = [d for d in K['docs'] if BD[d] != HD[d]]
    C.chk('D1 both docs, one platform', len(changed) == 2 and not plat_s, 'platform-k docs changed %d of 2 | platform-s docs changed %s' % (len(changed), plat_s or 'NONE'))
    figs = {}
    for d in K['docs']:
        nm = os.path.basename(d)[:28]; bl = BD[d].split('\n'); hl = HD[d].split('\n'); H = hunks(BD[d], HD[d])
        rem = [(i + 1, bl[i]) for op, i1, i2, j1, j2 in H for i in range(i1, i2)]; add = [(j + 1, hl[j]) for op, i1, i2, j1, j2 in H for j in range(j1, j2)]
        C.chk('D2 additions only %s' % nm, not rem, 'hunks %d | +%d / -%d%s' % (len(H), len(add), len(rem), '' if not rem else ' | REMOVED: ' + '; '.join('base:%d %r' % (n, l.strip()[:70]) for n, l in rem[:6])))
        blk = '\n'.join(l for _, l in add); opens = len(re.findall(r'<div\b', blk)); closes = len(re.findall(r'</div>', blk)); head = next((l.strip()[:90] for _, l in add if HEADING.search(l)), None)
        one = len(H) == 1 and H[0][0] == 'insert'
        C.chk('D3 one KS 1404 block %s' % nm, one and bool(BRX.search(blk)) and head is not None and opens == closes,
              'one INSERT hunk %s %s | KS 1404 hits %d | heading %r | <div %d / </div> %d' % (one, [(op, i1 + 1, j2 - j1) for op, i1, i2, j1, j2 in H], len(BRX.findall(blk)), head, opens, closes))
        if H: print('INFO D3 %s block inserted before base line %d (head %d-%d) | names the bundle path: %s' % (nm, H[0][1] + 1, H[0][3] + 1, H[0][4], 'tsa-trust-anchors' in blk))
        AL = dict(add); win = lambda n: ' '.join(AL.get(k, '') for k in range(n - 3, n + 4))
        tadd = [(n, l) for n, l in add if TRX.search(txt(l))]
        bad = [(n, l) for n, l in tadd if not (re.search(r'\b20\d\d-\d\d-\d\d\b', win(n)) and HOSTRX.search(txt(win(n))))]
        C.chk('D4 timings %s' % nm, not [r for r in rem if TRX.search(r[1])] and not bad, 'added lines stating a timing %d, without a date AND a host nearby %d%s' % (len(tadd), len(bad), '' if not bad else ' ' + '; '.join('head:%d %r' % (n, txt(l).strip()[:90]) for n, l in bad[:3])))
        figs[nm] = figures(blk)
    fl = list(figs.values()); cm = figures(' '.join(msgs))
    cross = all(fl[0].get(k) == fl[1].get(k) or None in (fl[0].get(k), fl[1].get(k)) for k in ('cells', 'after', 'before'))
    vs_kit = all(f.get('cells') == str(K['cells_head']) and f.get('after') == '%d/%d' % (K['suite_claim']['head_files'], K['suite_claim']['head_tests']) for f in fl)
    meas = {'cells': MEAS.get('cells'), 'before': MEAS.get('base'), 'after': MEAS.get('head')}
    vs_meas = all(meas[k] is None or all(f.get(k) in (None, meas[k]) and any(g.get(k) == meas[k] for g in fl) for f in fl) for k in meas)
    C.chk('D5 figures', cross and vs_kit and vs_meas and bool(MEAS), 'per doc %s | commit message %s | equal across docs %s | == kit claim (25, 6/69) %s | == THIS GATE\'s C3 measurement %s %s%s' % (
        figs, {k: cm.get(k) for k in ('cells', 'after', 'redfirst')}, cross, vs_kit, meas, vs_meas, '' if MEAS else '  <- pass --measured cells=..,base=F/T,head=F/T from YOUR C3 run (a doc figure is re-measured, never copied)'))
    IX = code_lines(T_index); m = re.search(r'async function verifyTimestamp\(data: \{[^}]*\}\): Promise<\{([^}]*)\}>', IX, re.S)
    rk = sorted(re.findall(r'(\w+)\??\s*:', m.group(1))) if m else []
    oa = T_openapi or ''; om = re.search(r"'TimestampVerifyResponse'[\s\S]*?data:\s*z\s*\.object\(\{([\s\S]*?)\}\)\s*\.(passthrough|strict)?", oa)
    ok_ = sorted(set(re.findall(r'^\s*(\w+):\s*z\.', om.group(1), re.M))) if om else []
    print('INFO D6 the OpenAPI data object is %s' % (('.%s()' % om.group(2)) if om and om.group(2) else 'closed by default' if om else 'NOT FOUND') + ('  <- passthrough: the published schema ALLOWS extra keys; the exact key set is pinned only by cell 14' if om and om.group(2) == 'passthrough' else ''))
    t14 = "expect(Object.keys(r.body.data).sort()).toEqual(['reason', 'verified']);" in (T_test or '') and "const allowed = ['verified', 'timestamp', 'tsaUrl', 'reason'];" in (T_test or '')
    t13 = "expect(Object.keys(r.body.data)).not.toContain('reason');" in (T_test or '')
    C.chk('D6 response shape', rk == sorted(K['response_keys']) and ok_ == sorted(K['response_keys']) and t14 and t13, 'index.ts verifyTimestamp return keys %s | openapi verify response keys %s | want %s | cell 14 exact refusal key set + allowed list %s | cell 13 reason absent %s' % (rk, ok_, sorted(K['response_keys']), t14, t13))
    if dev_docs is None:
        print('INFO D7 THE DOC RULE: develop == the judged base; no co-tenant block to keep yet (vacuous)'); C.chk('D7 keep both blocks', True, 'vacuous at this base')
    else:
        keys = [k for k in K['co_tenants']]; lost = {}
        for d in K['docs']:
            dl = [l for l in dev_docs[d].split('\n') if any(re.search(k.replace('-', '[- ]'), l) for k in keys)]; hl = [l for l in HD[d].split('\n') if any(re.search(k.replace('-', '[- ]'), l) for k in keys)]
            lost[os.path.basename(d)[:20]] = (len(dl), len(hl), dl == hl)
        C.chk('D7 keep both blocks', all(v[2] for v in lost.values()), 'co-tenant-key lines at develop vs head, per doc (n_dev, n_head, identical in order): %s' % lost)
    return C


def load(sha):
    T = {}
    for d in K['docs']:
        T[d] = show(REPO, sha, d)
        if T[d] is None: raise SystemExit('REFUSING: %s absent at %s' % (d, sha[:12]))
    return T


print('c5_docs_gateD2 %s | repo %s | base %s | head %s | measured %s | mode %s' % (now(), REPO, BASE[:12], HEAD[:12], MEAS or 'NONE', 'selftest' if '--selftest' in A else 'base-vs-base' if '--base-vs-base' in A else 'gate'))
BD = load(BASE); SK = show(REPO, BASE, K['skill'])
T_index = show(REPO, HEAD, K['index_module']) or ''; T_openapi = show(REPO, HEAD, K['openapi_module']) or ''; T_test = show(REPO, HEAD, K['test_file']) or ''
def plat_s(sha): return sorted(set(git(REPO, 'diff', '--name-only', BASE, sha).splitlines()) & set(K['docs_platform_s']))
msgs = [git(REPO, 'log', '-1', '--format=%B', c) for c in git(REPO, 'log', '--format=%H', '%s..%s' % (BASE, HEAD)).split()]
co = any(re.search(k.replace('-', '[- ]'), BD[d]) for k in K['co_tenants'] for d in K['docs'])
DEV = BD if co else None
if '--base-vs-base' in A:
    C = analyse(BD, dict(BD), SK, plat_s(BASE), [], 'BASE as head'); n = C.nfail()
    print('C5 DOCS %s (base-vs-base, a control: D1 / D3 MUST fail): %d FAIL of %d' % ('PASS' if n == 0 else 'FAIL', n, len(C.res))); raise SystemExit(1 if n else 0)
HD = load(HEAD); PS = plat_s(HEAD)
if '--selftest' in A:
    F, Q = K['docs']
    def plant(d, fn): t = dict(HD); t[d] = fn(t[d]); return t
    def rm_base_line(s, needle):
        L = s.split('\n'); i = next(i for i, l in enumerate(L) if needle in l and l in BD[Q].split('\n')); return '\n'.join(L[:i] + L[i + 1:])
    MEAS.update({'cells': str(K['cells_head']), 'base': '%d/%d' % (K['suite_claim']['base_files'], K['suite_claim']['base_tests']), 'head': '%d/%d' % (K['suite_claim']['head_files'], K['suite_claim']['head_tests'])})
    arms = [('T0 real head (with the builder-claimed figures as the measurement)', HD, PS, None),
            ('T1 one doc unchanged', plant(F, lambda s: BD[F]), PS, 'D1'),
            ('T2 a platform-s doc in the diff', HD, [K['docs_platform_s'][0]], 'D1'),
            ('T3 a pre-existing line removed', plant(Q, lambda s: rm_base_line(s, '<div')), PS, 'D2'),
            ('T4 the block loses its KS 1404 tag', plant(F, lambda s: s.replace('KS-1404', 'KS-9999').replace('KS 1404', 'KS 9999')), PS, 'D3'),
            ('T5 a second hunk elsewhere', plant(Q, lambda s: s.replace('</head>', '<!-- gD2 plant -->\n</head>', 1)), PS, 'D3'),
            ('T6 an added timing with no host', plant(Q, lambda s: s.replace('on Kamils-Mac-Studio', 'on a machine')), PS, 'D4'),
            ('T7 the docs disagree on the cell count', plant(Q, lambda s: s.replace('# 25 cells', '# 24 cells')), PS, 'D5')]
    ok = 0
    for name, hd, ps, want in arms:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): C = analyse(BD, hd, SK, ps, msgs, name, DEV)
        f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
        ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        if want is None or not good:
            for l in buf.getvalue().splitlines():
                if l.startswith('FAIL'): print('    ' + l[:260])
    MEAS2 = dict(MEAS); MEAS.clear(); MEAS.update(MEAS2, head='6/70')
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): C = analyse(BD, HD, SK, PS, msgs, 'T8', DEV)
    g = any(x.startswith('D5') for x in C.failed()); ok += g; print('SELFTEST %s T8 the gate measured 6/70, the docs say 6/69: want FAIL on D5 | failed %s' % ('OK' if g else 'MISS', C.failed()))
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) + 1 else 'BROKEN', ok, len(arms) + 1)); raise SystemExit(0 if ok == len(arms) + 1 else 1)
C = analyse(BD, HD, SK, PS, msgs, 'HEAD', DEV); n = C.nfail()
print('C5 DOCS %s: %d FAIL of %d checks | base %s | head %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), BASE[:12], HEAD[:12]))
raise SystemExit(1 if n else 0)
