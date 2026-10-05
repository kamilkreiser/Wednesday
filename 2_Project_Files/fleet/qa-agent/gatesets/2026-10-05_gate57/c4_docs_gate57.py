#!/usr/bin/env python3
"""c4_docs_gate57.py — gate57 C4: the project skill's §4 applied to EACH PR's own doc block, from git objects (READ ONLY; prints only).
Run once per PR (--pr 1380 | 1381).
  D0  THE RULE at cut_base: SKILL.md blob == kit skill_blob_base and §4 carries "Every test change updates its platform's two HTML docs,
      in the same commit" and the two platform-k paths.
  D1  SAME COMMIT, BOTH DOCS, ONE PLATFORM: the PR is ONE commit (parent == cut_base) whose diff carries a test path (kit test_path_rx) AND
      both platform-k docs; 0 platform-s docs.
  D2  ONE TAIL INSERT per doc: exactly one INSERT hunk, immediately before the base `  </body>` line and after the KS 1404 block's last
      line (kit base_blocks); any other hunk must be one of PR 1's ruled replaced lines (C2b proves those character by character).
  D3  NUMBERED AND SHAPED: flow — the block's first non-blank line is THE ONLY <h2> in it and matches the PR's flow_h2_rx (`12.` for
      #1380, `13.` for #1381), its <h3> sub-headings carry the same number prefix (12.x / 13.x); cheat — opens `    <div class="section">`,
      then an UNNUMBERED <h2> matching cheat_h2_rx (the sheet's own convention, as D's KS 1404 block), closes `    </div>`; <div> balanced.
  D3b SELF-CONTAINED: the block (HTML-unescaped plain text) names every kit block_must_name string (own key, its test file, how to run it,
      §5f, live sweep; #1381 also webhooks.ts:412 — the deliveries half) and states "not covered".
  D4  TIMINGS: every added line stating a timing has a date AND a named host within +/-3 lines, or says "projection" (§4).
  D5  NUMBER ORDER AT HEAD: the flow doc's <h2> numbers at the PR head == base's [1..11] + [this PR's number] (Q-N: numbers follow rulings,
      not merge order; #1381 alone shows the 12 gap until the merge-in — C4b reads 1..13 back from T2).
  D6  THE LAST CONTENT: after the block, the doc ends `  </body>` / `</html>` exactly as at base.
--selftest: plants into COPIES of the real head texts; every arm must land on its named check; the real heads must PASS.
--base-vs-base: cut_base as the head — a control that MUST fail D1 and D2.
Usage: c4_docs_gate57.py --repo <clone> --pr <1380|1381> [--head sha] [--selftest | --base-vs-base]     rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys, io, contextlib, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate57 import K, git, now, Checks, opt_factory, show, has_commit, opcodes, blob, pr_cfg

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--pr' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); CUT = K['cut_base']
key, P = pr_cfg(opt('--pr')); HEAD = opt('--head', P['ready_head'])
for s in (CUT, HEAD):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s):
        print('REFUSING: %s is not a 40-hex commit present in %s' % (s, REPO)); raise SystemExit(2)
FLOW, CHEAT = K['docs']; BB = K['base_blocks']; ANCH = K['doc_close_anchor']
TRX = re.compile(r'(\b\d+(?:[.,]\d+)?(?:\s?(?:-|–|&ndash;)\s?\d+(?:[.,]\d+)?)?\s?(?:ms|s|sec|secs|seconds|min|mins|minutes)\b)', re.I)
HOSTRX = re.compile(r'(?<!\ba )\bhost\b\s*(?:<[^>]+>\s*)*[`"\']?[A-Z0-9]')
RULED = {}
for f in K['doc_fixes'].values():
    RULED.setdefault(f['doc'], set()).add(f['line'])


def plain(s): return html.unescape(re.sub(r'<[^>]+>', ' ', s))


def h2nums(t): return [int(m) for m in re.findall(r'(?m)^\s*<h2>(\d+)\.', t)]


def analyse(BD, HD, files, skill, label):
    C = Checks()
    sk = skill or ''; clause = "Every test change updates its platform's two HTML docs, in the same commit"
    C.chk('D0 rule at base', blob(REPO, CUT, K['skill'])[1] == K['skill_blob_base'] and clause in sk and all(d in sk for d in K['docs']),
          '[%s] SKILL.md at %s blob == kit: %s | §4 clause present: %s | both platform-k paths named: %s' % (label, CUT[:12], blob(REPO, CUT, K['skill'])[1] == K['skill_blob_base'], clause in sk, all(d in sk for d in K['docs'])))
    tests = [f for f in files if re.search(K['test_path_rx'], f)]; changed = [d for d in K['docs'] if BD[d] != HD[d]]; ps = sorted(set(files) & set(K['docs_platform_s']))
    C.chk('D1 same commit, both docs', len(changed) == 2 and tests and not ps and all(d in files for d in K['docs']),
          'one commit on cut_base | test paths in it %s | platform-k docs changed %d of 2 | platform-s docs %s' % ([t.split('/')[-1] for t in tests], len(changed), ps or 'NONE'))
    for d in K['docs']:
        nm = 'flow' if d == FLOW else 'cheat'; bl = BD[d].split('\n'); hl = HD[d].split('\n'); ops = opcodes(bl, hl)
        anchor = [i for i, l in enumerate(bl) if l == ANCH]; k1404 = BB[d]['KS1404']['last']
        ins = [o for o in ops if o[0] == 'insert']; rest = [o for o in ops if o[0] != 'insert']
        rest_ok = all(o[0] == 'replace' and o[2] - o[1] == o[4] - o[3] and set(range(o[1] + 1, o[2] + 1)) <= RULED.get(d, set()) for o in rest) and (key == 'pr1' or not rest)
        one = len(ins) == 1 and len(anchor) == 1 and ins[0][1] == anchor[0] and ins[0][1] >= k1404
        C.chk('D2 one tail insert %s' % nm, one and rest_ok, 'insert hunks %s | base %r at line %s | after the KS 1404 block (ends %d) | other hunks %s (allowed: %s)' % (
            [(o[1] + 1, o[4] - o[3]) for o in ins], ANCH.strip(), [a + 1 for a in anchor], k1404, [(o[0], o[1] + 1, o[2]) for o in rest],
            'PR 1 ruled lines %s' % sorted(RULED.get(d, ())) if key == 'pr1' else 'none'))
        blk = hl[ins[0][3]:ins[0][4]] if ins else []; nb = [l for l in blk if l.strip()]; text = '\n'.join(blk)
        opens, closes = len(re.findall(r'<div\b', text)), len(re.findall(r'</div>', text))
        if d == FLOW:
            h2 = [l for l in blk if '<h2' in l]; h3 = re.findall(r'<h3>(\d+)\.\d+ ', text)
            ok3 = bool(nb) and re.match(P['flow_h2_rx'], nb[0]) is not None and len(h2) == 1 and h3 and set(h3) == {P['flow_number']} and opens == closes
            C.chk('D3 numbered block flow', ok3, 'first line %r matches %s | <h2> in block %d | <h3> prefixes %s (want all %s.) | <div %d / </div> %d' % (
                nb[0].strip()[:90] if nb else None, P['flow_h2_rx'], len(h2), sorted(set(h3)), P['flow_number'], opens, closes))
        else:
            ok3 = len(nb) >= 3 and nb[0] == '    <div class="section">' and re.match(P['cheat_h2_rx'], nb[1]) is not None and nb[-1] == '    </div>' and opens == closes and not re.search(r'<h2>\d+\.', text)
            C.chk('D3 cheat convention', ok3, 'opens %r | h2 %r matches %s (unnumbered) | closes %r | <div %d / </div> %d' % (
                nb[0] if nb else None, nb[1].strip()[:80] if len(nb) > 1 else None, P['cheat_h2_rx'], nb[-1] if nb else None, opens, closes))
        pt = plain(text); miss = [s for s in P['block_must_name'] if s.lower() not in pt.lower()]
        C.chk('D3b self-contained %s' % nm, not miss and re.search(r'(?i)not covered', pt) is not None, 'block %d lines | must-name missing %s | states "not covered": %s' % (
            len(blk), miss or 'NONE', re.search(r'(?i)not covered', pt) is not None))
        AL = {j: hl[j] for j in range(ins[0][3], ins[0][4])} if ins else {}
        win = lambda j: ' '.join(AL.get(x, '') for x in range(j - 3, j + 4))
        tl = [j for j, l in AL.items() if TRX.search(plain(l))]
        bad = [j for j in tl if not ((re.search(r'\b20\d\d-\d\d-\d\d\b', win(j)) and HOSTRX.search(plain(win(j)))) or re.search(r'(?i)projecti?on|projected', plain(win(j))))]
        C.chk('D4 timings %s' % nm, not bad, 'added lines stating a timing %d | without (date AND named host) or "projection": %s' % (len(tl), ['head:%d %r' % (j + 1, plain(hl[j]).strip()[:70]) for j in bad] or 'NONE'))
        for j in tl: print('INFO D4 %s head:%d %r' % (nm, j + 1, plain(hl[j]).strip()[:110]))
        tail_b = bl[anchor[0]:] if anchor else []; tail_h = hl[ins[0][4]:] if ins else []
        C.chk('D6 last content %s' % nm, tail_b == tail_h and tail_h[:2] == [ANCH, '</html>'], 'after the block: %r (base after the anchor: %r)' % (tail_h[:3], tail_b[:3]))
    # D7 the block's own timing statement, re-measured at cut_base (the gate rules what counts as a "stated timing")
    for d in K['docs']:
        L = BD[d].split('\n'); suite = 'anchoring' if key == 'pr1' else 'originate'
        both = [(i + 1, plain(l).strip()[:120]) for i, l in enumerate(L) if TRX.search(plain(l)) and re.search(suite, l, re.I)]
        print('INFO D7 %s at %s: lines with a duration figure AND %r: %d %s | lines with a duration figure: %d | `auth` lines (case-insensitive): %d' % (
            'flow' if d == FLOW else 'cheat', CUT[:12], suite, len(both), both[:3], sum(1 for l in L if TRX.search(plain(l))), sum(1 for l in L if re.search('auth', l, re.I))))
    if key == 'pr2':
        au = [sum(1 for l in BD[d].split('\n') if re.search('auth', l, re.I)) for d in K['docs']]
        st = all(re.search(r'auth\W.{0,40}?\b70\b.{0,40}?\b69\b', ' '.join(plain(HD[d]).split())) for d in K['docs'])
        C.chk('D7 must-hit control re-measured', au == [70, 69] and st, "`auth` line counts at cut_base [flow, cheat] %s (the blocks state 70 / 69 in both docs: %s)" % (au, st))
    else:
        print('INFO D7 #1380 states "0 stated timings name the anchoring suite" against a must-hit control of 23 (flow) / 35 (cheat) duration figures: the kit\'s instrument reads the counts above; NOT REPRODUCED as 23 / 35 by it — the gate re-measures with the seat\'s named instrument or rules it (README D5)')
    nb_, nh = h2nums(BD[FLOW]), h2nums(HD[FLOW])
    C.chk('D5 flow numbers', nh == nb_ + [int(P['flow_number'])] and nb_ == list(range(1, 12)), 'base %s | head %s (want base + [%s])' % (nb_, nh, P['flow_number']))
    return C


def load(sha):
    T = {}
    for d in K['docs']:
        T[d] = show(REPO, sha, d)
        if T[d] is None: raise SystemExit('REFUSING: %s absent at %s' % (d, sha[:12]))
    return T


print('c4_docs_gate57 %s | repo %s | %s #%s %s | cut_base %s | head %s | mode %s' % (now(), REPO, key, P['number'], P['ticket'], CUT[:12], HEAD[:12],
      'selftest' if '--selftest' in A else 'base-vs-base' if '--base-vs-base' in A else 'gate'))
BD = load(CUT); SK = show(REPO, CUT, K['skill'])
parents = git(REPO, 'log', '-1', '--format=%P', HEAD).split()
if parents != [CUT] and '--base-vs-base' not in A:
    print('REFUSING: HEAD %s is not ONE commit on cut_base (parents %s) — C1 P3 first' % (HEAD[:12], parents)); raise SystemExit(2)
if '--base-vs-base' in A:
    C = analyse(BD, dict(BD), [], SK, 'BASE as head'); n = C.nfail()
    print('C4 DOCS (base-vs-base, a control: D1 and D2 MUST fail): %d FAIL of %d | failed %s' % (n, len(C.res), C.failed()))
    raise SystemExit(0 if ('D1 same commit, both docs' in C.failed() and any(x.startswith('D2') for x in C.failed())) else 1)
HD = load(HEAD); FILES = git(REPO, 'diff', '--name-only', CUT, HEAD).splitlines()
if '--selftest' in A:
    def plant(d, fn):
        t = dict(HD); t[d] = fn(t[d]); return t
    hf = HD[FLOW].split('\n'); i = next(k for k, l in enumerate(hf) if re.match(P['flow_h2_rx'], l))
    end = hf.index(ANCH, i); blkf = hf[i:end]
    def move_up(s):   # the flow block cut from the tail and put BEFORE the KS 1404 block
        L = s.split('\n'); L = L[:i] + L[end:]; at = BB[FLOW]['KS1404']['first'] - 1; return '\n'.join(L[:at] + blkf + L[at:])
    other = '13' if P['flow_number'] == '12' else '12'
    arms = [
        ('T0 real head', HD, FILES, None),
        ('T1 the cheat block missing (one doc only)', plant(CHEAT, lambda s: BD[CHEAT]), FILES, 'D1'),
        ('T2 a platform-s doc in the diff', HD, FILES + [K['docs_platform_s'][0]], 'D1'),
        ('T3 the wrong number (%s.)' % other, plant(FLOW, lambda s: s.replace('<h2>%s. ' % P['flow_number'], '<h2>%s. ' % other, 1)), FILES, 'D3'),
        ('T4 the flow block placed before the KS 1404 block', plant(FLOW, move_up), FILES, 'D2'),
        ('T5 an unbalanced cheat block', plant(CHEAT, lambda s: s.replace('      </div>\n    </div>\n  </body>', '      </div>\n  </body>', 1)), FILES, 'D3'),
        ('T6 "not covered" removed from the flow block', plant(FLOW, lambda s: s[:s.index(blkf[0])] + re.sub(r'(?i)not covered', 'elsewhere', s[s.index(blkf[0]):])), FILES, 'D3b'),
        ('T7 a timing with no host or date', plant(FLOW, lambda s: s.replace(blkf[1], blkf[1] + '\n      It runs in 912&nbsp;ms.', 1)), FILES, 'D4'),
        ('T8 a second <h2> inside the flow block', plant(FLOW, lambda s: s.replace(blkf[1], blkf[1] + '\n    <h2>%s. extra</h2>' % other, 1)), FILES, 'D3'),
        ('T9 the test file dropped from the commit', HD, [f for f in FILES if not re.search(K['test_path_rx'], f)], 'D1'),
        ('T10 the cheat block numbered "12."', plant(CHEAT, lambda s: re.sub(r'(<h2>)(.* &mdash; %s</h2>)' % P['ticket'], r'\g<1>%s. \2' % P['flow_number'], s, 1)), FILES, 'D3'),
        ('T11 a line after the block before </body>', plant(CHEAT, lambda s: s.replace('    </div>\n  </body>', '    </div>\n    <p>x</p>\n  </body>', 1)), FILES, 'D'),
    ]
    ok = 0; buf = io.StringIO()
    with contextlib.redirect_stdout(buf): BASEF = set(analyse(BD, HD, FILES, SK, 'baseline').failed())
    print('SELFTEST BASELINE: the REAL head fails %s — a real finding carried into every arm (an arm passes only on a NEW failure of its named check)' % (sorted(BASEF) or 'NOTHING'))
    for name, hd, files, want in arms:
        if want is not None and hd == HD and files == FILES:
            print('SELFTEST MISS %s: the plant changed NOTHING' % name); continue
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): C = analyse(BD, hd, files, SK, name)
        f = C.failed(); new = [x for x in f if x not in BASEF]
        good = (set(f) == BASEF) if want is None else any(x.startswith(want) for x in new)
        ok += good; print('SELFTEST %s %s: want %s | NEW failures %s' % ('OK' if good else 'MISS', name, 'the baseline only' if want is None else 'FAIL on ' + want, new or 'NONE'))
        for l in buf.getvalue().splitlines():
            if not good and l.startswith(('FAIL', 'PASS')): print('    ' + l[:240])
    print('SELFTEST %s %d of %d (%s #%s)' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms), key, P['number'])); raise SystemExit(0 if ok == len(arms) else 1)
C = analyse(BD, HD, FILES, SK, 'HEAD'); n = C.nfail()
print('C4 DOCS %s: %d FAIL of %d checks | #%s %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), P['number'], HEAD[:12]))
raise SystemExit(1 if n else 0)
