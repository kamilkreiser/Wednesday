#!/usr/bin/env python3
"""c2_code_gate86.py — the CODE-CLAIM instruments for gate86 (a batch of four PRs). Read verbs only, in the gate's OWN clone (or the shared checkout, read-only). Every figure it prints is the
DRAFTER'S PREDICTION; the gate re-measures. Written new for this batch (the gate85 c2 is a single-predicate vitest PR); [g86] shape borrowed: Tally, required arguments, controls beside zeros.

  c2_code_gate86.py claims --repo R --pr N --head H --base B [--yaml-structural]   N in 1451 1452 (contract PRs) | 1454 (dev-reload.sh) | 1455 (env.local.example)
  c2_code_gate86.py handlers --repo R --pr N --head H                              (1451 / 1452) READ-ONLY census: where each declared-required operation is registered and what the lines after
                                                                                    the registration do with the body. EVIDENCE CLASS READ ONLY. It does NOT measure what a handler does
                                                                                    with an ABSENT body (that stays UNMEASURED until the gate probes it; see KIT_REPORT)
  c2_code_gate86.py --selftest

  1451 / 1452  Y1 the yaml diff is N pure `required: true` insertions, each directly under a `requestBody:` line; the N operations are RESOLVED (path + method) from the head yaml
               Y2 (--yaml-structural, ~1 min) PyYAML loads base and head: exactly those N operations change requestBody.required None -> True and head-minus-those == base (deep equality)
               O1 each *.openapi.ts diff: every added line is a `// KS-<n>` comment, a `required: true` line, or a removed line + `, required: true`; every removed line reappears
               T1 test cells per file (declared by the READY) and each asserts `.required).toBe(true)` or a control; the ticket key on every `it(` title
               R1 no non-test, non-doc, non-yaml, non-*.openapi.ts source path in base..head (a planted route path makes the same filter read 1)
  1454         S1 dev-reload.sh: -1 / +7 exact lines;  S2 stack_env.sh derives STACK_PREFIX (develop) and start-secuura.sh / stop-secuura.sh source it;  S3 `bash -n` of the head script;
               S4 the line-73 defect census (a variable directly followed by a non-ASCII char in tracked *.sh): the claim "1 of 192 scripts";  S5 new suite: 7 check() cells, shell-suite list +1
  1455         E1 env.local.example: -1 (API_GATEWAY_PORT=6882) +3 comment lines, no assignment added;  E2 reader census of API_GATEWAY_PORT at develop and head, code-only beside raw (controls);
               E3 the suite diff = cells 5 and 6 appended (existing file);  E4 the declared deviation: the third comment line is printed (the Spark original is not in this kit: NOT RUN)
rc 0 all pass / 1 a FAIL / 2 refused."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate86 import K, PR, Tally, git, req, opt, show, blob, resolvable

YAML = K['shared_yaml']; FLOW, CHEAT = K['known_develop_overlap']
EXPECT_CELLS = {  # declared by the READY ledgers (passed counts with the product): 1451 = 5 / 4 / 6 ; 1452 = 5 / 6 / 5 ; 1454 = 7 ; 1455 = suite 6 total
    '1451': {'anchoring': 5, 'staking': 4, 'transfer': 6}, '1452': {'analytics': 5, 'm365-integration': 6, 'api-gateway': 5}}
METHOD_RX = re.compile(r'^    (get|post|put|patch|delete|head|options):\s*$'); PATH_RX = re.compile(r'^  (/[^\s]*):\s*$')


def sh(cmd, cwd=None, inp=None):
    p = subprocess.run(cmd, capture_output=True, cwd=cwd, input=inp); return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def hunks(diff_text):
    """[(plus_start, [added lines], [removed lines], [context-free])] from a -U0 or -U1 diff of ONE file."""
    out = []; cur = None
    for l in diff_text.split('\n'):
        m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', l)
        if m:
            cur = {'minus_start': int(m.group(1)), 'plus_start': int(m.group(3)), 'added': [], 'removed': [], 'added_at': []}; out.append(cur); ln = int(m.group(3)); continue
        if cur is None or l.startswith(('+++', '---', 'diff ', 'index ')): continue
        if l.startswith('+'): cur['added'].append(l[1:]); cur['added_at'].append(ln); ln += 1
        elif l.startswith('-'): cur['removed'].append(l[1:])
        elif l.startswith(' '): ln += 1
    return out


def resolve_ops(head_text, linenos):
    """for each 1-based line number in the head yaml, the (path, method) of the operation it sits in (nearest method key at indent 4, then nearest path key at indent 2 above it)."""
    L = head_text.split('\n'); res = []
    for n in linenos:
        i = n - 1; meth = path = None
        while i >= 0:
            if meth is None and METHOD_RX.match(L[i]): meth = METHOD_RX.match(L[i]).group(1)
            elif meth is not None and PATH_RX.match(L[i]): path = PATH_RX.match(L[i]).group(1); break
            i -= 1
        res.append((path, meth))
    return res


def yaml_shape(diff_text, head_text, want_n):
    hs = hunks(diff_text); adds = [(a, ln) for h in hs for a, ln in zip(h['added'], h['added_at'])]; rem = [r for h in hs for r in h['removed']]
    L = head_text.split('\n')
    pure = not rem and len(adds) == want_n and all(a == '        required: true' for a, _ in adds)
    under = all(L[ln - 2].strip() == 'requestBody:' for _, ln in adds)
    ops = resolve_ops(head_text, [ln for _, ln in adds])
    return pure, under, ops, len(adds), len(rem)


def ts_shape(diff_text):
    hs = hunks(diff_text); adds = [a for h in hs for a in h['added']]; rem = [r for h in hs for r in h['removed']]; bad = []
    comments = [a for a in adds if re.match(r'^\s*// KS-\d+', a)]; reqs = [a for a in adds if a.strip() == 'required: true,']
    rest = [a for a in adds if a not in comments and a not in reqs]
    pair = [r for r in rem if any(a.replace(', required: true }', ' }', 1).rstrip() == r.rstrip() for a in rest)]
    left_adds = [a for a in rest if not any(a.replace(', required: true }', ' }', 1).rstrip() == r.rstrip() for r in rem)]
    left_rem = [r for r in rem if r not in pair]
    return {'adds': len(adds), 'rem': len(rem), 'comments': len(comments), 'req_lines': len(reqs), 'replaced': len(pair), 'stray_adds': left_adds, 'stray_rem': left_rem}


def cells(text): return re.findall(r"^\s*it(?:\.each)?\(\s*['\"`]([^'\"`]*)", text, re.M)


def nonascii_after_var(text):
    """lines where a shell variable `$NAME` (no braces) is DIRECTLY followed by a non-ASCII char (bash 3.2 + UTF-8 reads the multibyte lead byte as part of the name)."""
    return [(i + 1, l) for i, l in enumerate(text.split('\n')) if re.search(r'\$[A-Za-z_][A-Za-z0-9_]*[^\x00-\x7F]', l)]


def claims(A):
    n = req(A, '--pr'); P = PR(n); head = req(A, '--head', True); base = req(A, '--base', True); repo = req(A, '--repo'); t = Tally()
    if head != P['head_expected'] or base != P['base']: raise SystemExit('REFUSED: --head/--base differ from the kit pins for #%s (a wrong value: re-draft)' % n)
    for s in (head, base):
        if not resolvable(repo, s): raise SystemExit('REFUSED: %s not in %s' % (s[:12], repo))
    ns = {}
    for l in git(repo, 'diff', '--numstat', base, head).strip().split('\n'):
        a, d, p = l.split('\t'); ns[p] = (int(a), int(d))
    raw_add = {}
    for p in ns:
        if p in (FLOW, CHEAT): continue
        h = show(repo, head, p); b = show(repo, base, p)
        raw_add[p] = (len([x for x in h.split('\n') if x.strip()]) - len([x for x in b.split('\n') if x.strip()]))
    t.check('F0', all(ns[p] == (P['paths'][p]['add'], P['paths'][p]['del']) for p in ns), 'numstat for %d paths equals the kit (+%d/-%d); non-blank line deltas for the non-doc paths: %s' % (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values()), {os.path.basename(p)[:30]: v for p, v in raw_add.items()}))
    if n in ('1451', '1452'): contract(repo, P, n, head, base, t, '--yaml-structural' in A)
    elif n == '1454': script1454(repo, P, head, base, t)
    elif n == '1455': env1455(repo, P, head, base, t)
    return t.end()


def contract(repo, P, n, head, base, t, structural):
    want_n = P['declared_ops']
    ydiff = git(repo, 'diff', '-U1', base, head, '--', YAML); htext = show(repo, head, YAML); btext = show(repo, base, YAML)
    pure, under, ops, nadd, nrem = yaml_shape(ydiff, htext, want_n)
    t.check('Y1', pure and under and len(set(ops)) == want_n and all(o[0] and o[1] == 'post' for o in ops), 'yaml diff: %d added / %d removed lines; all `        required: true`: %s; each directly under `requestBody:`: %s; %d distinct operations, all POST: %s' % (nadd, nrem, pure, under, len(set(ops)), ['%s %s' % (m.upper(), p) for p, m in ops]))
    # controls: a stray added line, a removed line, a wrong count must each FAIL the same function
    bad1 = yaml_shape(ydiff.replace('+        required: true', '+        required: false', 1), htext, want_n)[0]; bad2 = yaml_shape(ydiff + '\n-x', htext, want_n)[0]; bad3 = yaml_shape(ydiff, htext, want_n + 1)[0]
    t.check('Y1-CONTROL', pure and not bad1 and not bad2 and not bad3, 'CONTROL: the shape check FAILS on a flipped value (%s), on an extra removed line (%s) and on a wrong declared count (%s)' % (not bad1, not bad2, not bad3))
    L = htext.split('\n'); sib = [i for i, l in enumerate(L) if l == '        required: true' and L[i - 1].strip() == 'requestBody:']
    bsib = [i for i, l in enumerate(btext.split('\n')) if l == '        required: true' and btext.split('\n')[i - 1].strip() == 'requestBody:']
    t.check('Y1b', len(sib) - len(bsib) == want_n, '`requestBody:` + `required: true` pairs in the whole yaml: base %d -> head %d (+%d = the declared %d)' % (len(bsib), len(sib), len(sib) - len(bsib), want_n))
    if structural:
        try:
            import yaml
            Ld = getattr(yaml, 'CSafeLoader', yaml.SafeLoader); bd = yaml.load(btext, Loader=Ld); hd = yaml.load(htext, Loader=Ld)
        except Exception as e:
            t.check('Y2', False, 'PyYAML load failed: %s' % str(e)[:120]); bd = hd = None
        if bd is not None:
            chg = []; stripped = hd
            import copy
            stripped = copy.deepcopy(hd)
            for path, ops_ in (hd.get('paths') or {}).items():
                for meth, op in ops_.items():
                    if isinstance(op, dict):
                        rb = op.get('requestBody'); brb = ((bd['paths'].get(path) or {}).get(meth) or {}).get('requestBody') if isinstance(bd['paths'].get(path), dict) else None
                        if isinstance(rb, dict) and rb.get('required') is True and not (isinstance(brb, dict) and brb.get('required') is True): chg.append((path, meth)); del stripped['paths'][path][meth]['requestBody']['required']
            t.check('Y2', sorted(chg) == sorted((p, m) for p, m in ops) and stripped == bd, 'PyYAML (%s): operations whose requestBody.required went absent/false -> true: %d %s; head minus exactly those keys == base (deep equality): %s; operations in head: %d' % (Ld.__name__, len(chg), 'EQUAL to the diff-resolved set' if sorted(chg) == sorted(ops) else 'DIFFERS', stripped == bd, sum(len(v) for v in hd['paths'].values())))
            copy2 = copy.deepcopy(stripped); p0, m0 = chg[0]; copy2['paths'][p0][m0]['summary'] = 'PLANTED'
            t.check('Y2-CONTROL', copy2 != bd and hd != bd, 'CONTROL: head != base before stripping, and a planted summary change makes the stripped copy != base (the equality can fail)')
    else:
        t.info('Y2', 'NOT RUN by name (no --yaml-structural): the PyYAML structural equality is the slow arm (~1 min)')
    tsd = [p for p in P['paths'] if p.endswith('.openapi.ts')]; tot = {'adds': 0, 'comments': 0, 'req_lines': 0, 'replaced': 0}
    for p in tsd:
        s = ts_shape(git(repo, 'diff', '-U0', base, head, '--', p))
        t.check('O1', not s['stray_adds'] and not s['stray_rem'] and s['rem'] == s['replaced'] and s['comments'] >= 1, '%s: +%d/-%d; %d comment line(s) naming the ticket, %d `required: true,` lines, %d replaced lines (the removed line reappears + `, required: true`); stray added %s stray removed %s' % (os.path.basename(p), s['adds'], s['rem'], s['comments'], s['req_lines'], s['replaced'], s['stray_adds'][:1], s['stray_rem'][:1]))
        for k in tot: tot[k] += s[k]
    decl = tot['req_lines'] + tot['replaced']
    t.check('O1-TOTAL', decl == want_n, 'declarations in the three *.openapi.ts files: %d `required: true,` lines + %d inline = %d == the declared %d operations' % (tot['req_lines'], tot['replaced'], decl, want_n))
    ctl = ts_shape('@@ -1 +1,2 @@\n-    body: { x },\n+    // note\n+    body: { y }, required: true },\n')
    t.check('O1-CONTROL', bool(ctl['stray_adds']) and not ts_shape('@@ -1 +1,2 @@\n-    body: { x } },\n+    // KS-1: c\n+    body: { x }, required: true },\n')['stray_adds'], 'CONTROL: a changed body line (not the same line + required) is reported stray; a faithful one is not')
    tests = [p for p in P['paths'] if '/__tests__/' in p]; got = {}
    for p in tests:
        txt = show(repo, head, p); c = cells(txt); svc = p.split('/services/')[1].split('/')[0]; got[svc] = len(c)
        t.check('T1', all(P['ticket'] in x for x in c) and len(c) == EXPECT_CELLS[n][svc] and '.required).toBe(true)' in txt, '%s: %d cells (the READY: %d), every title names %s, asserts `.required).toBe(true)`: %s' % (os.path.basename(p)[:52], len(c), EXPECT_CELLS[n][svc], P['ticket'], '.required).toBe(true)' in txt))
    t.check('T1-CONTROL', len(cells("it('x', () => {})\n  it(\"y\", () => {})")) == 2 and cells('nothing here') == [], 'CONTROL: the cell counter reads 2 on two planted `it(` lines and 0 on none')
    src = lambda paths: [p for p in paths if '/__tests__/' not in p and p not in (FLOW, CHEAT, YAML) and not p.endswith('.openapi.ts')]
    t.check('R1', src(P['paths']) == [] and src(list(P['paths']) + ['Blockchain/Dev/services/anchoring/src/routes/anchors.ts']) == ['Blockchain/Dev/services/anchoring/src/routes/anchors.ts'], 'no handler / route / source path in base..head (only the .openapi.ts declarations, the yaml, tests, two docs); CONTROL: the same filter returns the planted route path')


def script1454(repo, P, head, base, t):
    p = 'Blockchain/Dev/scripts/dev-reload.sh'; d = hunks(git(repo, 'diff', '-U0', base, head, '--', p)); adds = [a for h in d for a in h['added']]; rem = [r for h in d for r in h['removed']]
    s1 = lambda rem_, adds_: rem_ == ['CONTAINER="secuura-$SVC"'] and len(adds_) == 7 and adds_[-1] == 'CONTAINER="${STACK_PREFIX}-$SVC"' and 'source "$ROOT/scripts/stack_env.sh"' in adds_ and sum(1 for a in adds_ if a.startswith('# ')) == 4
    t.check('S1', s1(rem, adds), 'dev-reload.sh: removed %s; added %d lines (4 comment lines, PROJECT_ROOT, source stack_env.sh, CONTAINER from ${STACK_PREFIX}): %s' % (rem, len(adds), [a[:60] for a in adds if not a.startswith('#')]))
    t.check('S1-CONTROL', not s1(rem + ['x'], adds) and not s1(rem, adds[:-1]) and not s1(rem, adds[:-1] + ['CONTAINER="secuura-$SVC"']), 'CONTROL: an extra removed line, a missing added line and the slot-1 literal as the last added line each FAIL the same predicate')
    se = show(repo, head, 'Blockchain/Dev/scripts/stack_env.sh'); pref = [l for l in se.split('\n') if re.match(r'\s*STACK_PREFIX=', l)]
    st = [q for q in ('Start_Up/start-secuura.sh', 'Blockchain/Dev/stop-secuura.sh') if 'stack_env.sh' in show(repo, head, q)]
    t.check('S2', len(pref) >= 1 and len(st) == 2, 'stack_env.sh assigns STACK_PREFIX (%d line(s): %s); start-secuura.sh and stop-secuura.sh both mention stack_env.sh: %s' % (len(pref), [x.strip()[:70] for x in pref][:3], st))
    t.check('S2-CONTROL', 'NO_SUCH_NAME_QZX' not in se and 'STACK_PREFIX' in se, 'CONTROL: an impossible name (NO_SUCH_NAME_QZX) reads absent from stack_env.sh while STACK_PREFIX reads present, with the same read')
    txt = show(repo, head, p); rc, so, se2 = sh(['bash', '-n', '/dev/stdin'], inp=txt.encode())
    t.check('S3', rc == 0, '`bash -n` of the head script text: rc %d' % rc)
    rc2, _, _ = sh(['bash', '-n', '/dev/stdin'], inp=b'if then fi ((\n')
    t.check('S3-CONTROL', rc2 != 0, 'CONTROL: `bash -n` on a planted syntax error reads rc %d (non-zero)' % rc2)
    scripts = [f for f in git(repo, 'ls-tree', '-r', '--name-only', head).split('\n') if f.endswith('.sh')]; hits = {}
    for f in scripts:
        h = nonascii_after_var(show(repo, head, f))
        if h: hits[f] = h
    bh = nonascii_after_var(show(repo, base, p))
    t.check('S4', len(scripts) > 100 and 'Blockchain/Dev/scripts/dev-reload.sh' in hits and len(hits) >= 1, 'line-73 defect census over %d tracked *.sh at the head: %d script(s) hold a `$NAME` directly followed by a non-ASCII char: %s (the READY: 1 of 192; this count is code AND comment lines, raw); base dev-reload.sh hits: %s' % (len(scripts), len(hits), {k.split('/')[-1]: [x[0] for x in v] for k, v in hits.items()}, [x[0] for x in bh]))
    t.check('S4-CONTROL', nonascii_after_var('echo "$X\u2026"\n') == [(1, 'echo "$X\u2026"')] and nonascii_after_var('echo "${X}\u2026"\n') == [], 'CONTROL: the matcher fires on `$X…` and not on the braced `${X}…`')
    tp = 'Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh'; tx = show(repo, head, tp)
    nchk = len(re.findall(r'^\s*check ', tx, re.M)); t.check('S5', len(tx) > 0 and nchk >= 3, 'new suite %s: %d lines, %d `check ` call lines (the READY: 7 cells; call lines are fewer than cells where a loop runs)' % (os.path.basename(tp), tx.count('\n'), nchk))
    lst = [f for f in git(repo, 'ls-tree', '-r', '--name-only', head).split('\n') if re.search(r'/scripts/(__tests__/)?[^/]*\.test\.sh$', f)]; lb = [f for f in git(repo, 'ls-tree', '-r', '--name-only', base).split('\n') if re.search(r'/scripts/(__tests__/)?[^/]*\.test\.sh$', f)]
    t.check('S5b', len(lst) - len(lb) == 1 and tp in lst, '`*.test.sh` under scripts/ (flat glob over the tree): base %d -> head %d (+1: the new suite). The READY counts 77 -> 78 via run-shell-suites.sh --list (NOT RUN here: the glob and the list can differ)' % (len(lb), len(lst)))


def env1455(repo, P, head, base, t):
    p = 'Blockchain/Dev/env.local.example'; d = hunks(git(repo, 'diff', '-U0', base, head, '--', p)); adds = [a for h in d for a in h['added']]; rem = [r for h in d for r in h['removed']]
    e1 = lambda rem_, adds_: rem_ == ['API_GATEWAY_PORT=6882'] and len(adds_) == 3 and all(a.startswith('# ') for a in adds_) and not any(re.match(r'^[A-Z_]+=', a) for a in adds_)
    t.check('E1', e1(rem, adds), 'env.local.example: removed %s; added %d lines, all comments, no assignment: %s' % (rem, len(adds), adds))
    t.check('E1-CONTROL', not e1(rem, adds[:2] + ['API_GATEWAY_PORT=6882']) and not e1(rem, adds[:2]) and not e1([], adds), 'CONTROL: a re-added assignment, a missing comment line and a missing removal each FAIL the same predicate')
    t.info('E4', 'the declared deviation: the THIRD added comment line reads %r (the Spark original had a longer third line with a final clause about `.env`; the original payload is NOT in this kit: the byte comparison is NOT RUN; the PR body carries both blob ids)' % adds[2] if len(adds) == 3 else 'n/a')
    rows = {}
    for lab, rev in (('develop', K['develop_at_draft']), ('head', head)):
        out = git(repo, 'grep', '-n', '-I', 'API_GATEWAY_PORT', rev, '--', ':!Projects Documents', check=False)[1] if resolvable(repo, rev) else ''
        rows[lab] = [l.split(':', 1)[1] if ':' in l else l for l in out.split('\n') if l]
    iscom = lambda l: bool(re.match(r'^[^:]+:\d+:\s*(#|//)', l))
    per = lambda ls: {f: (len(v), len([x for x in v if not iscom(x)])) for f, v in ((k, list(g)) for k, g in __import__('itertools').groupby(sorted(ls), key=lambda l: l.split(':')[0]))}
    pd, ph = per(rows['develop']), per(rows['head']); ev = 'Blockchain/Dev/env.local.example'
    t.check('E2', pd.get(ev, (0, 0))[1] >= 1 and ph.get(ev, (0, 0))[1] == 0, 'env.local.example non-comment hits of API_GATEWAY_PORT: develop %s -> head %s (raw, code-only) [want code-only >=1 -> 0]; per file (raw, code-only) develop %s | head %s (git grep -n, the two HTML docs excluded)' % (pd.get(ev), ph.get(ev), {os.path.basename(k)[:30]: v for k, v in pd.items()}, {os.path.basename(k)[:30]: v for k, v in ph.items()}))
    other = {os.path.basename(k)[:40]: v[1] for k, v in ph.items() if k != ev and v[1]}
    t.info('E2b', 'code-only (non-comment) hits at head in files other than env.local.example: %s (the READY: 2 references: .planning/codebase/STRUCTURE.md:166 and the template\'s own line 5; this census counts the suite\'s own string literals too)' % other)
    gp = git(repo, 'grep', '-n', '-I', 'GATEWAY_PORT', head, '--', 'Blockchain/Dev/scripts/stack_env.sh', check=False)[1]; imp = git(repo, 'grep', '-n', '-I', 'NO_SUCH_KEY_QZX', head, check=False)[1]
    t.check('E2-CONTROL', len(gp.strip().split('\n')) >= 1 and gp.strip() != '' and imp.strip() == '', 'CONTROL: the live key GATEWAY_PORT reads %d hit(s) in stack_env.sh; an impossible name reads 0' % len([x for x in gp.split('\n') if x]))
    tp = 'Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh'; dd = hunks(git(repo, 'diff', '-U0', base, head, '--', tp)); aa = [a for h in dd for a in h['added']]; rr = [r for h in dd for r in h['removed']]
    t.check('E3', not rr and len(aa) == 15 and sum(1 for a in aa if a.startswith('# CELL')) == 2 and show(repo, base, tp).count('# CELL') + 2 == show(repo, head, tp).count('# CELL'), '%s: +%d/-%d (an existing file; cells 5 and 6 appended; `# CELL` markers %d -> %d)' % (os.path.basename(tp)[:50], len(aa), len(rr), show(repo, base, tp).count('# CELL'), show(repo, head, tp).count('# CELL')))


def handlers(A):
    n = req(A, '--pr'); P = PR(n); head = req(A, '--head', True); repo = req(A, '--repo'); t = Tally()
    if n not in ('1451', '1452'): raise SystemExit('REFUSED: handlers is for the contract PRs 1451 / 1452')
    base = P['base']; ydiff = git(repo, 'diff', '-U1', base, head, '--', YAML); htext = show(repo, head, YAML); pure, under, ops, _, _ = yaml_shape(ydiff, htext, P['declared_ops'])
    t.check('H0', pure and len(ops) == P['declared_ops'], 'resolved %d declared-required operations from the yaml diff' % len(ops))
    files = [f for f in git(repo, 'ls-tree', '-r', '--name-only', head, '--', 'Blockchain/Dev/services').split('\n') if f.endswith('.ts') and '/src/' in f and '/__tests__/' not in f and not f.endswith('.openapi.ts') and not f.endswith('.d.ts')]
    TXT = {f: show(repo, head, f).split('\n') for f in files}
    for path, meth in ops:
        colon = re.sub(r'\{([^}]+)\}', r':\1', path); segs = [s for s in colon.split('/') if s]; regs = []; used = None
        for k in range(len(segs), 0, -1):           # longest suffix of the path first: '/api/batch/certifications', '/batch/certifications', '/certifications'
            cand = '/' + '/'.join(segs[-k:]); rx = re.compile(r"\.%s\(\s*['\"`]%s['\"`]" % (meth, re.escape(cand)))
            for f in files:
                for i, l in enumerate(TXT[f]):
                    if rx.search(l): regs.append((f, i + 1))
            if regs: used = cand; break
        info = []
        for f, ln in regs[:3]:
            seg = TXT[f][ln - 1: ln + 24]; j = '\n'.join(seg)
            info.append('%s:%d | req.body %s | parse/validate %s | 400 %s' % (f.replace('Blockchain/Dev/services/', ''), ln, 'req.body' in j, bool(re.search(r'safeParse|\.parse\(|validate\w*\(', j)), '400' in j))
        full = (used == colon)
        if full: t.check('H1', bool(regs) and len(regs) <= 3, '%s %s -> registered with the FULL path in %d place(s): %s' % (meth.upper(), path, len(regs), info[:3]))
        else: t.info('H1-UNCONFIRMED', '%s %s -> NO full-path registration; the longest matching SUFFIX %r hits %d place(s) %s. A suffix hit may be a DIFFERENT operation that ends the same way (e.g. /delegations vs /batch/delegations): the gate reads the router mount before trusting it' % (meth.upper(), path, used, len(regs), info[:3] if info else 'NONE'))
    t.check('H1-CONTROL', True and len(files) > 50, 'CONTROL: the census scanned %d non-test .ts source files under services/*/src (a census over 0 files would also read "none")' % len(files))
    t.info('H2', 'EVIDENCE CLASS READ ONLY. This census does NOT say what a handler returns for an ABSENT body; the READYs call that UNMEASURED/UNVERIFIED. The gate probes it (a vitest harness mounting the router with stubbed deps, the ks815 shape) or names it NOT RUN.')
    return t.end()


def selftest():
    t = Tally()
    y = '''paths:\n  /api/x:\n    post:\n      requestBody:\n        required: true\n        content: {}\n  /api/y:\n    post:\n      requestBody:\n        required: true\n'''
    d = '@@ -4,0 +5,1 @@\n+        required: true\n@@ -8,0 +10,1 @@\n+        required: true\n'
    pure, under, ops, na, nr = yaml_shape(d, y, 2)
    t.check('S1', pure and under and ops == [('/api/x', 'post'), ('/api/y', 'post')] and (na, nr) == (2, 0), 'yaml_shape + resolve_ops on a planted document: %s' % ops)
    t.check('S2', not yaml_shape(d, y, 3)[0] and not yaml_shape(d + '-gone\n', y, 2)[0], 'wrong count / extra removal -> not pure')
    s = ts_shape('@@ -1 +1,2 @@\n-    body: { c: 1 } },\n+    // KS-9: c\n+    body: { c: 1 }, required: true },\n')
    t.check('S3', s['replaced'] == 1 and s['comments'] == 1 and not s['stray_adds'], 'ts_shape pairs the replaced line')
    t.check('S4', cells("it('a', f)\n  it(\"b\", f)\n// it('c')") == ['a', 'b'] , 'cells() counts plain it( lines (not commented ones); it.each rows are NOT counted: these tests use plain it()')
    t.check('S5', nonascii_after_var('x="$A\u2026"') and not nonascii_after_var('x="${A}\u2026"') and not nonascii_after_var('echo $A "\u2026"'), 'nonascii_after_var arms')
    t.check('S6', [h['plus_start'] for h in hunks('@@ -1,0 +5,2 @@\n+a\n+b\n')] == [5] and hunks('@@ -1,0 +5,2 @@\n+a\n+b\n')[0]['added_at'] == [5, 6], 'hunks() line numbers')
    return t.end()


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--selftest' in A: sys.exit(selftest())
    if not A or A[0] not in ('claims', 'handlers'): print(__doc__); sys.exit(2)
    sys.exit({'claims': claims, 'handlers': handlers}[A[0]](A[1:]))
