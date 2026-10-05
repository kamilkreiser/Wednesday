#!/usr/bin/env python3
"""c3_comments_gate63.py — the COMMENT-ONLY claim for #1388's two .ts edits (qualified-tsa.ts, rfc3161-verify.ts), measured by a
COMMENT-STRIPPED PROJECTION (the builder's method), never by `cmp` of dist/ (tsc copies JSDoc into the emitted JS, so dist bytes
DIFFER by design — a raw cmp is the wrong instrument and is reported only as INFO).

The projection: a JS/TS lexer that removes `//` and `/* */` comments while keeping strings ('…', "…"), template literals (with
`${…}` nesting) and regex literals intact; each comment becomes one space; the result is split on whitespace into a TOKEN LIST.
Two files are "comment-only different" iff their token lists are EQUAL and their raw bytes DIFFER.

  src  --repo <git dir> [--head <sha>]          the two .ts files, base vs head blobs (READ verbs only)
       S1 each file: raw bytes differ (else the claim is vacuous) AND token lists equal
       S2 instrument controls on the SAME lexer, every run: `const a=1` vs `const a=2` DIFFER; two different comments over the
          same code are EQUAL; a string holding `//` and `/*` survives; a regex literal holding `//` survives
  dist --base-dist <dir> --head-dist <dir>      every emitted .js under both dirs (the gate builds them with tsc in ITS worktrees)
       J1 the same set of .js files on both sides (count printed; builder claims 9)
       J2 every .js pair token-equal after stripping; >= 1 pair raw-different (the comment edit reached dist: the check is not
          vacuous); INFO the raw-different .js and .js.map counts
       J3 the same S2 controls
--selftest  arms on fixture copies in $G63_SCRATCH/fixtures: T0 the real base/head .ts pass S1; a CODE tamper inside the edited
            region must FAIL; a comment-only tamper must PASS; a string-literal tamper must FAIL (the lexer does not eat strings).
rc 0 all PASS / rc 1 any FAIL or 0 checked."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate63 import K, git, Tally, SCRATCH

REGEX_PRE = set('(,=:[!&|?{};+-*%<>~^')
REGEX_KW = ('return', 'typeof', 'case', 'do', 'else', 'in', 'of', 'new', 'delete', 'void', 'throw', 'instanceof', 'yield', 'await')


def strip_comments(src):
    out = []; i = 0; n = len(src); stack = []   # stack of '`' / '{' for template nesting
    def prev_sig():
        j = len(out) - 1
        txt = ''.join(out[-64:]).rstrip()
        return txt
    while i < n:
        c = src[i]; nx = src[i + 1] if i + 1 < n else ''
        if stack and stack[-1] == '`':
            if c == '\\': out.append(src[i:i + 2]); i += 2; continue
            if c == '`': stack.pop(); out.append(c); i += 1; continue
            if c == '$' and nx == '{': stack.append('{'); out.append('${'); i += 2; continue
            out.append(c); i += 1; continue
        if c == '/' and nx == '/':
            j = src.find('\n', i); i = n if j < 0 else j; out.append(' '); continue
        if c == '/' and nx == '*':
            j = src.find('*/', i + 2); i = n if j < 0 else j + 2; out.append(' '); continue
        if c in ('"', "'"):
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == '\\' else 1
            out.append(src[i:j + 1]); i = j + 1; continue
        if c == '`': stack.append('`'); out.append(c); i += 1; continue
        if c == '{' and stack: stack.append('{'); out.append(c); i += 1; continue
        if c == '}' and stack and stack[-1] == '{': stack.pop(); out.append(c); i += 1; continue
        if c == '/':
            p = prev_sig()
            is_re = (not p) or p[-1] in REGEX_PRE or any(p.endswith(k) and (len(p) == len(k) or not (p[-len(k) - 1].isalnum() or p[-len(k) - 1] == '_')) for k in REGEX_KW)
            if is_re:
                j = i + 1; cls = False
                while j < n and src[j] != '\n':
                    if src[j] == '\\': j += 2; continue
                    if src[j] == '[': cls = True
                    elif src[j] == ']': cls = False
                    elif src[j] == '/' and not cls: break
                    j += 1
                j += 1
                while j < n and (src[j].isalpha()): j += 1
                out.append(src[i:j]); i = j; continue
        out.append(c); i += 1
    return ''.join(out)


def tokens(src): return strip_comments(src).split()


def controls(t, cid):
    a = tokens('const a=1;'); b = tokens('const a=2;')
    c = tokens('/** one */\nconst x = f(1); // tail A\n'); d = tokens('/* two,\n  lines */ const x = f(1); // tail B\n')
    e = strip_comments("const u = 'http://x/*y*/'; const v = \"//z\";")
    f = strip_comments('const r = /a\\/\\/b/g.test(s); // gone')
    ok = a != b and c == d and "'http://x/*y*/'" in e and '"//z"' in e and '/a\\/\\/b/g' in f and 'gone' not in f
    t.check(cid, ok, 'lexer controls: code 1 vs 2 differ %s; two comments over the same code equal %s; strings survive %s; regex survives %s' % (
        a != b, c == d, "'http://x/*y*/'" in e and '"//z"' in e, '/a\\/\\/b/g' in f and 'gone' not in f))


def judge_src(pairs, t):
    rows = []; ok = True
    for p, (b, h) in pairs.items():
        raw = b != h; tb, th = tokens(b), tokens(h); eq = tb == th
        rows.append('%s raw-differ %s tokens %d/%d equal %s' % (os.path.basename(p), raw, len(tb), len(th), eq))
        if not eq:
            import difflib
            sm = difflib.SequenceMatcher(None, tb, th, autojunk=False)
            first = [o for o in sm.get_opcodes() if o[0] != 'equal'][:2]
            rows.append('   first token diffs %s' % [(o[0], ' '.join(tb[o[1]:o[2]])[:80], ' '.join(th[o[3]:o[4]])[:80]) for o in first])
        ok = ok and raw and eq and len(tb) > 50
    t.check('S1', ok and len(pairs) == len(K['comment_only_ts']), ' | '.join(rows))
    controls(t, 'S2')


def walk_js(d):
    out = {}
    for root, _, fs in os.walk(d):
        for f in fs:
            if f.endswith('.js') or f.endswith('.js.map'):
                out[os.path.relpath(os.path.join(root, f), d)] = open(os.path.join(root, f), encoding='utf-8', errors='replace').read()
    return out


def judge_dist(bd, hd, t):
    B = walk_js(bd); H = walk_js(hd)
    jb = sorted(p for p in B if p.endswith('.js')); jh = sorted(p for p in H if p.endswith('.js'))
    t.check('J1', jb == jh and len(jb) > 0, '.js files base %d head %d; only-base %s only-head %s' % (len(jb), len(jh), sorted(set(jb) - set(jh))[:5], sorted(set(jh) - set(jb))[:5]))
    common = [p for p in jb if p in H]
    diff_tok = [p for p in common if tokens(B[p]) != tokens(H[p])]; raw = [p for p in common if B[p] != H[p]]
    maps = [p for p in B if p.endswith('.js.map') and p in H and B[p] != H[p]]
    t.check('J2', not diff_tok and len(raw) >= 1, 'token-different .js %d %s; raw-different .js %d %s (want >= 1: the edit reached dist)' % (
        len(diff_tok), diff_tok[:5], len(raw), raw[:5]))
    t.info('J2-map', 'raw-different .js.map %d %s (expected: mappings shift with the comment line counts)' % (len(maps), maps[:5]))
    controls(t, 'J3')


def src_pairs(repo, head):
    return {p: (git(repo, 'show', '%s:%s' % (K['base'], p)), git(repo, 'show', '%s:%s' % (head, p))) for p in K['comment_only_ts']}


def selftest(repo):
    import io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    real = src_pairs(repo, K['head'])
    for p, (b, h) in real.items():
        open(os.path.join(fx, 'c3_real_base_' + os.path.basename(p)), 'w').write(b); open(os.path.join(fx, 'c3_real_head_' + os.path.basename(p)), 'w').write(h)
    def run(pairs):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge_src(pairs, t)
        return t
    t0 = run(real); ok = int(not t0.fails and t0.n == 2); total = 1
    print('SELFTEST %s T0 the REAL base/head .ts: %d checked, fails %s' % ('OK' if ok else 'MISS', t0.n, t0.fails))
    Q, V = K['comment_only_ts']
    def mut(path, a, b):
        d = dict(real); h = d[path][1]; assert h.count(a) == 1, 'anchor must occur exactly once (%d): %r' % (h.count(a), a); d[path] = (d[path][0], h.replace(a, b)); return d
    arms = [('CODE tamper: readTrustAnchorsPem returns raw for any value', mut(Q, "  if (raw.includes('-----BEGIN CERTIFICATE-----')) return raw;", "  if (raw) return raw;"), ['S1'], True),
            ('CODE tamper: the fail-closed refusal text changed', mut(V, "refuse('no trust anchor configured')", "refuse('no anchor')"), ['S1'], True),
            ('STRING tamper inside the logger message', mut(Q, "'[TSA] TSA_TRUST_ANCHORS_PEM points at a file that could not be read'", "'[TSA] could not be read'"), ['S1'], True),
            ('COMMENT-ONLY tamper (a word in the new JSDoc)', mut(Q, ' * STILL NOT COVERED, and in the PR body', ' * STILL NOT COVERED (edited), and in the PR body'), [], False)]
    for name, pairs, want, must_fail in arms:
        t = run(pairs); total += 1
        g = (set(want) <= set(t.fails)) if must_fail else (not t.fails)
        ok += g; print('SELFTEST %s %s: want %s | got FAIL %s' % ('OK' if g else 'MISS', name, ('FAIL %s' % want) if must_fail else 'QUIET (pass)', t.fails))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    if '--selftest' in A: raise SystemExit(selftest(opt('--repo', K['checkout'])))
    t = Tally()
    if A[0] == 'src':
        judge_src(src_pairs(opt('--repo', K['checkout']), opt('--head', K['head'])), t)
    elif A[0] == 'dist':
        judge_dist(opt('--base-dist'), opt('--head-dist'), t)
    else:
        print(__doc__); raise SystemExit(2)
    raise SystemExit(t.end())
