#!/usr/bin/env python3
"""c2_code_gate83.py — the commit's CODE CLAIMS, measured against the diff (read verbs only; no node, no npm). Carried in shape from c2_code_gate82.py `claims`;
[g83] rebuilt for #1450 (KS-1426: lockfile-cleanroom.sh gains report_surface()). Every census is taken CODE-ONLY (full-line `#` comments blanked) BESIDE the raw count.

  c2_code_gate83.py claims --repo R --pr 1450 --head H --base B
  c2_code_gate83.py --selftest

F0  CODE-ONLY multiset of lockfile-cleanroom.sh: the one `echo "  covered: ..."` line out (re-emitted with a trailing `# KS-1426` comment), the function's 27 code lines + the
    3-line call in (31 code lines in); raw +35/-1 by numstat (34 non-blank + 1 blank).
F1  line-level opcodes base -> head are EXACTLY: insert 31 lines (3 comment + 27 function + 1 blank) before the `FAILED=()` line, then replace 1 line by 4 (the `covered:` echo
    re-emitted with its trailing comment + the 3-line call that directly follows it); every other line byte-identical (so the exit-code lines, the install loop and the `find` line are untouched).
F2  report_surface is defined once and CALLED once, at the end of the file, inside `if [ "$#" -eq 0 ]`; its last statement is `return 0`; it contains no `exit`, no
    `FAILED+=`, no `CHECKED+=`, no `INFRA_SKIP=`; every `return` in it is `return 0`.
F3  the exit-code lines (`exit 0`, `exit 0`, `exit 1`) are identical at base and head (text and order); every `exit` precedes the call: report_surface runs ONLY on an all-OK run
    (the Docker-advisory SKIP, the infra SKIP and the FAIL paths exit first and print no surface line) — a fact beside the PR's claim, for the gate to rule.
F4  THE F1 CENSUS: the git calls inside report_surface (3) and which are guarded (`|| {` / `||`): the `--show-toplevel` call is; `--show-prefix` and the `ls-files` process
    substitution are NOT (1 of 3). The wrong-number consequence is MEASURED by c3 `stubs`.
F5  `KS-1426` on added script lines: 2 (the block comment and the trailing comment on the covered echo); in the test: 1 (line 3). The body says "2 of 35" and "1 of 107".
F6  the payload equals the Spark pass's patch.diff (sha256/16 503b0cda009442f6, 7392 B) modulo ONLY the function-context text git appends to hunk headers: section by
    section, with the normaliser's CONTROLS (a changed + line / context line / header number each flip the verdict).
F7  the new test: 5 `# CELL n` markers; cells 1-2 RED at base, 3-5 CONTROL; no `cd` line; every `git` call is `git -C "$REPO"`; it names neither bootstrap-env.sh nor env.example
    nor hooksPath (the gate82 H9 hazard does not apply to it: SAID after reading); WORK is a mktemp -d under ${TMPDIR:-/tmp}.
F8  line 35 of the script, `cd "$(dirname "$0")/../.."`, is present at base and head at the same line (Q-CWD1426: it puts every git call of the leg inside the scratch repo).
F9  line counts: base 133, head 167 (the flow doc says "133 -> 167 lines").
F10 CI reach (INFO + one check): the only workflow that runs lockfile-cleanroom.sh is pr-lockfiles.yml, whose `paths:` list is exactly the two package-file globs; #1450 touches
    neither, so the CHANGED LEG has no CI run on this PR (the no-op twin reports success). The new test IS reached: pr-security-gates.yml / security-scan.yml run run-shell-suites.sh.
F11 preflight.sh prints `OK — all locks clean-room-installable` after the leg (unchanged): the sentence that reads like a total is still there.
D1/D1b/D1c/D1d/D1-CONTROL the docs: each change is a PURE INSERTION (head minus the block == base byte for byte) immediately before </body>, the flow heading carries `53.` and
    the cheat heading `KS-1426`; fragment byte sizes (the body says 7,743 B and 3,155 B).
rc 0 all pass / 1 a FAIL / 2 refused."""
import difflib, hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate83 import K, PR, Tally, git, show, blob, req, resolvable


def norm(l): return re.sub(r'\s+', ' ', l).strip()


def added_removed(a, b):
    """multiset diff of normalised non-blank lines: (added, removed)."""
    la = [norm(x) for x in a.split('\n') if x.strip()]; lb = [norm(x) for x in b.split('\n') if x.strip()]
    add, rem = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes():
        if op in ('replace', 'delete'): rem += la[i1:i2]
        if op in ('replace', 'insert'): add += lb[j1:j2]
    return add, rem


def sh_code_only(txt):
    return '\n'.join('' if l.lstrip().startswith('#') else l for l in txt.split('\n'))


def blob_id(b):
    b = b if isinstance(b, bytes) else b.encode('utf-8')
    return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


def pure_insertion(base, head):
    """-> (ok, info). head == base with ONE contiguous block inserted; removing the block gives base byte for byte."""
    la = base.split('\n'); lb = head.split('\n')
    ops = [o for o in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if o[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'insert': return False, 'opcodes %s' % [(o[0], o[1], o[2], o[3], o[4]) for o in ops[:4]]
    _, i1, _, j1, j2 = ops[0]
    rebuilt = '\n'.join(lb[:j1] + lb[j2:])
    return rebuilt == base, 'one insertion of %d line(s) at head line %d of %d (base %d lines); head minus block == base: %s; first line %r; next line %r' % (
        j2 - j1, j1 + 1, len(lb), len(la), rebuilt == base, lb[j1][:60], (lb[j2] if j2 < len(lb) else '<EOF>')[:60])


def docs(repo, head, base, t, P):
    for d in P['doc_paths']:
        b, h = show(repo, base, d), show(repo, head, d)
        ok, info = pure_insertion(b, h)
        t.check('D1', bool(b) and bool(h) and ok, '%s: %s' % (d.split('/')[-1], info))
        la, lb = b.split('\n'), h.split('\n')
        ops = [o for o in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if o[0] != 'equal']
        frag = lb[ops[0][3]:ops[0][4]] if len(ops) == 1 else []
        nxt = lb[ops[0][4]] if len(ops) == 1 and ops[0][4] < len(lb) else ''
        t.check('D1c', nxt == '</body>' and bool(frag), '%s: the block ends immediately before %r; fragment %d lines, %d bytes (joined with \\n); added bytes by blob size %d; first line %r' % (
            d.split('/')[-1], nxt, len(frag), len('\n'.join(frag).encode()), len(h.encode()) - len(b.encode()), (frag[0] if frag else '')[:70]))
        h2s = [l for l in frag if '<h2' in l]
        if d == P['doc_paths'][0]:
            t.check('D1b', len(h2s) == 1 and ('<h2>%s ' % P['flow_block']) in h2s[0], 'flow doc fragment has ONE <h2> and it opens <h2>%s (h2 lines: %s)' % (P['flow_block'], [x[:70] for x in h2s]))
        else:
            t.check('D1d', len(h2s) == 1 and P['cheat_key'] in h2s[0], 'cheat doc fragment has ONE <h2> and it carries %s (h2 lines: %s)' % (P['cheat_key'], [x[:90] for x in h2s]))
    b = show(repo, base, P['doc_paths'][0]); h = show(repo, head, P['doc_paths'][0])
    t.check('D1-CONTROL', not pure_insertion(b, h.replace('<html', '<HTML', 1))[0] and h.count('<html') + h.count('<HTML') > 0, 'CONTROL: the head doc with one base byte altered is NOT a pure insertion (the instrument can fail)')


# ---------------------------------------------------------------- the payload comparison (F6)
def split_sections(diff_text):
    """a unified diff -> {path: [lines]} keyed by the `+++ b/<path>` header; git header lines (diff --git / index / new file mode) are dropped; the hunk-header
    FUNCTION-CONTEXT text (everything after the closing `@@`) is stripped: it is the one thing a re-generated diff may legitimately differ in."""
    out = {}; cur = None
    for l in diff_text.split('\n'):
        if l.startswith(('diff --git ', 'index ', 'new file mode ', 'deleted file mode ', 'similarity index ')): continue
        if l.startswith('--- '): cur_old = l; continue
        if l.startswith('+++ '):
            cur = l[6:] if l.startswith('+++ b/') else l[4:]; out[cur] = [cur_old, l]; continue
        if cur is None: continue
        m = re.match(r'^(@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@)', l)
        out[cur].append(m.group(1) if m else l)
    for k in out:
        while out[k] and out[k][-1] == '': out[k].pop()
    return out


def payload_compare(patch_text, own_text):
    """-> (equal, details). Per section lines equal after the normalisation."""
    a, b = split_sections(patch_text), split_sections(own_text)
    if set(a) != set(b): return False, 'section sets differ: patch %s vs own %s' % (sorted(a), sorted(b))
    bad = [k for k in a if a[k] != b[k]]
    return not bad, ('sections equal: %s' % sorted(a)) if not bad else 'sections DIFFER: %s' % bad


def sh_function(src, name):
    """(start_line, end_line, body_lines) of `name() {` .. first `^}` (1-based)."""
    ls = src.split('\n'); s = [i for i, l in enumerate(ls) if l.startswith(name + '() {')]
    if len(s) != 1: raise SystemExit('sh_function: %r defined %d times' % (name, len(s)))
    e = next(i for i in range(s[0] + 1, len(ls)) if ls[i] == '}')
    return s[0] + 1, e + 1, ls[s[0]:e + 1]


def git_calls(body_lines):
    """the lines of a function that invoke `git` -> [(lineno_in_body, text, guarded)]. A call is guarded when its own line (or the closing of its brace group) carries `||`."""
    out = []
    for i, l in enumerate(body_lines):
        if re.search(r'(?<![\w/-])git\b', l) and not l.lstrip().startswith(('#', 'echo')):
            out.append((i + 1, l.strip(), '||' in l))
    return out


# ---------------------------------------------------------------- #1450
def run1450(repo, head, base):
    t = Tally(); P = PR(1450); g = P['gate_script']; s = P['suite']
    b, h = show(repo, base, g), show(repo, head, g); ts = show(repo, head, s)
    if not b or not h or not ts: print('REFUSED: the script or the suite is absent at base / head'); return 2
    cb, ch = sh_code_only(b), sh_code_only(h)
    add, rem = added_removed(cb, ch); raw_a, raw_r = added_removed(b, h)
    want_rem = ['echo " covered: ${CHECKED[*]-}"']
    t.check('F0', len(rem) == 1 and rem[0].startswith('echo " covered: ${CHECKED[*]-}"') and len(add) == 31 and len(raw_a) == 34 and len(raw_r) == 1,
            'CODE-ONLY multiset in lockfile-cleanroom.sh base %s -> head %s: added %d removed %d | RAW added %d removed %d NON-BLANK lines (numstat %s counts the one added BLANK line too: 34 + 1 = 35) | removed %s | the added code lines include the re-emitted covered echo: %s' % (
                blob(repo, base, g)[-12:], blob(repo, head, g)[-12:], len(add), len(rem), len(raw_a), len(raw_r), P['numstat'][g], rem, any(x.startswith('echo " covered:') for x in add)))
    la, lb = b.split('\n'), h.split('\n')
    ops = [(o[0], o[2] - o[1], o[4] - o[3], o[1] + 1) for o in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if o[0] != 'equal']
    t.check('F1', [(o[0], o[1], o[2]) for o in ops] == [('insert', 0, 31), ('replace', 1, 4)] and la[0] == lb[0],
            'line-level opcodes base -> head: %s (want exactly: insert 31 | replace 1 by 4 (the covered echo re-emitted with its trailing comment, then the 3-line call that directly follows it); every other line byte-identical, so the install loop, the `find`, the check() function and the exit-code lines are untouched)' % ops)
    try:
        f0, f1, body = sh_function(h, 'report_surface')
    except SystemExit as e:
        t.check('F2', False, str(e)); body = []; f0 = f1 = 0
    calls = [i + 1 for i, l in enumerate(lb) if re.match(r'^\s*report_surface\s*$', l)]
    guard = [i + 1 for i, l in enumerate(lb) if l.strip() == 'if [ "$#" -eq 0 ]; then' and i + 1 > f1]
    rets = [l.strip() for l in body if re.match(r'^\s*return\b', l)]
    bad_tokens = [l.strip() for l in body if re.search(r'\bexit\b|FAILED\+=|CHECKED\+=|INFRA_SKIP=|\bset [-+]', l)]
    t.check('F2', bool(body) and len(calls) == 1 and calls[0] > f1 and len(guard) == 1 and guard[0] == calls[0] - 1 and lb[calls[0]].strip() == 'fi' and
            body[-2].strip() == 'return 0' and all(r == 'return 0' for r in rets) and not bad_tokens and b.count('report_surface') == 0,
            'report_surface defined lines %d-%d (1x); CALLED %d time(s) at line(s) %s, directly under `if [ "$#" -eq 0 ]; then` at %s and closed by `fi`; last statement `%s`; return statements %s; exit / FAILED+= / CHECKED+= / INFRA_SKIP= / set inside it: %s; mentions at base: %d' % (
                f0, f1, len(calls), calls, guard, body[-2].strip() if len(body) > 1 else None, rets, bad_tokens or 'none', b.count('report_surface')))
    exits_b = [(i + 1, l.strip()) for i, l in enumerate(la) if re.match(r'^\s*exit\s+\d', l)]; exits_h = [(i + 1, l.strip()) for i, l in enumerate(lb) if re.match(r'^\s*exit\s+\d', l)]
    t.check('F3', [x[1] for x in exits_b] == [x[1] for x in exits_h] and len(exits_h) == 3 and all(n < calls[0] for n, _ in exits_h),
            'exit-code lines base %s | head %s (texts equal: %s) | every `exit` precedes the call at line %s: %s -> report_surface is reached ONLY on an all-OK run; the Docker-advisory SKIP, the infra SKIP and the FAIL paths exit first and print no surface line (a FACT beside the PR\'s claim; the gate rules whether it matters)' % (
                exits_b, exits_h, [x[1] for x in exits_b] == [x[1] for x in exits_h], calls[:1], all(n < calls[0] for n, _ in exits_h)))
    gc = git_calls(body); unguarded = [c for c in gc if not c[2]]
    t.check('F4', len(gc) == 3 and len(unguarded) == 2,
            'THE F1 CENSUS: git calls inside report_surface %d; guarded by `||` %d, UNGUARDED %d: %s -> with `--show-prefix` failing the prefix is empty and no lock matches (`surface: 0 of N`); with ls-files failing the loop never runs (`surface: 0 of 0`); exit code stays 0 (c3 `stubs` MEASURES all three variants)' % (
                len(gc), len(gc) - len(unguarded), len(unguarded), [(c[0], c[1][:70]) for c in unguarded]))
    ks_h = [i + 1 for i, l in enumerate(lb) if 'KS-1426' in l]; ks_b = [i + 1 for i, l in enumerate(la) if 'KS-1426' in l]
    ks_t = [i + 1 for i, l in enumerate(ts.split('\n')) if 'KS-1426' in l]
    tail_comment = [l for l in lb if l.rstrip().endswith('# KS-1426: report_surface names what was NOT installed')]
    t.check('F5', len(ks_h) == 2 and not ks_b and len(ks_t) == 1 and len(tail_comment) == 1 and ks_t == [3],
            '`KS-1426` on script lines at head %s (base %s) -> 2 of 35 added lines (the body: new-file lines 91 and 164); one TRAILING comment on a code line: %d; in the test: lines %s of %d (the body: 1 of 107, line 3)' % (
                ks_h, ks_b, len(tail_comment), ks_t, len(ts.split('\n')) - 1))
    # F6 the payload
    sp = K['spark']
    if os.path.isfile(sp['patch']):
        pb = open(sp['patch'], 'rb').read(); ph = hashlib.sha256(pb).hexdigest()[:16]
        own = git(repo, 'diff', base, head, '--', g, s)
        eq, det = payload_compare(pb.decode('utf-8'), own)
        # the normaliser's own controls: each planted change must flip the verdict
        pt = pb.decode('utf-8'); ctl = []
        def flip_first(txt, prefix, repl):
            ls = txt.split('\n'); i = next(i for i, l in enumerate(ls) if l.startswith(prefix) and not l.startswith(('+++', '---'))); ls[i] = repl(ls[i]); return '\n'.join(ls)
        ctl.append(('a + line altered', not payload_compare(flip_first(pt, '+', lambda l: l + 'x'), own)[0]))
        ctl.append(('a context line altered', not payload_compare(flip_first(pt, ' ', lambda l: l + 'x'), own)[0]))
        ctl.append(('a hunk-header NUMBER altered', not payload_compare(re.sub(r'@@ -88,6', '@@ -89,6', pt, count=1), own)[0]))
        ctl.append(('only the function-context suffix altered (must stay EQUAL)', payload_compare(re.sub(r'(?m)^(@@ -88,6 \+88,37 @@).*$', r'\1 zzz()', own, count=1), own)[0]))
        t.check('F6', ph == sp['patch_sha256_16'] and len(pb) == sp['patch_bytes'] and eq and all(c[1] for c in ctl),
                'patch.diff sha256/16 %s (kit %s), %d B (kit %d); the head diff (script + test) EQUALS it section by section after stripping ONLY the hunk-header function-context text: %s | normaliser controls %s' % (
                    ph, sp['patch_sha256_16'], len(pb), sp['patch_bytes'], det, ctl))
        ctxs = re.findall(r'(?m)^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@(.*)$', own); pcx = re.findall(r'(?m)^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@(.*)$', pb.decode())
        t.info('F6-CONTEXT-TEXT', 'the only difference: function-context text on the head diff\'s hunk headers %s vs the patch.diff\'s %s' % ([x.strip() for x in ctxs if x.strip()], [x.strip() for x in pcx if x.strip()]))
    else:
        t.info('F6', 'NOT RUN: %s is not readable here (never a pass)' % sp['patch'])
    # F7 the new test
    tl = ts.split('\n'); cells = len(re.findall(r'(?m)^# CELL \d', ts))
    gitl = [l.strip() for l in tl if re.search(r'(?<![\w/-])git\b', l) and not l.lstrip().startswith('#') and 'command -v git' not in l and 'echo "FATAL' not in l]
    cdl = [l.strip() for l in tl if re.match(r'\s*cd\b', l) or re.search(r'\$\(cd\b', l)]
    haz = [w for w in ('bootstrap-env.sh', 'env.example', 'hooksPath', '.githooks') if w in ts or w in h]
    t.check('F7', cells == 5 and all('git -C "$REPO"' in l for l in gitl) and len(gitl) == 2 and haz == [] and 'mktemp -d "${TMPDIR:-/tmp}/ks1426.XXXXXX"' in ts and 'RED at the tip' in ts,
            'the new test: %d `# CELL n` markers (want 5; cells 1-2 RED at the tip, 3-5 CONTROL); git calls %s (all `git -C "$REPO"`); `cd` lines %s (the only one is HERE=$(cd ...) resolving its own dir); names bootstrap-env.sh / env.example / hooksPath / .githooks: %s -> the gate82 H9 hazard (TMPDIR inside a repo makes bootstrap-env.sh write that repo\'s core.hooksPath) does NOT apply to this test or to the leg, SAID after reading both whole' % (
                cells, gitl, cdl, haz or 'NONE'))
    # F8 line 35
    cd_b = [i + 1 for i, l in enumerate(la) if l == 'cd "$(dirname "$0")/../.."   # Blockchain/Dev']; cd_h = [i + 1 for i, l in enumerate(lb) if l == 'cd "$(dirname "$0")/../.."   # Blockchain/Dev']
    t.check('F8', cd_b == cd_h == [35], 'the leg\'s `cd "$(dirname "$0")/../.."` is at line(s) base %s head %s (want [35], unchanged): every git call of the leg runs in the leg\'s own checkout, not the caller\'s cwd (Q-CWD1426 static half; c3 `cwd` MEASURES it)' % (cd_b, cd_h))
    t.check('F9', len(la) - (1 if la[-1] == '' else 0) == P['script_lines']['base'] and len(lb) - (1 if lb[-1] == '' else 0) == P['script_lines']['head'],
            'script line counts base %d, head %d (kit %d / %d; the flow doc says "133 -> 167")' % (len(la) - (la[-1] == ''), len(lb) - (lb[-1] == ''), P['script_lines']['base'], P['script_lines']['head']))
    # F10 CI reach
    plk, nop = show(repo, head, '.github/workflows/pr-lockfiles.yml'), show(repo, head, '.github/workflows/pr-lockfiles-noop.yml')
    paths = re.findall(r"(?m)^\s+- '([^']+)'", plk.split('paths:')[1].split('permissions:')[0]) if 'paths:' in plk else []
    runs_leg = [l.strip() for l in plk.split('\n') if 'lockfile-cleanroom.sh' in l and 'run:' in l]
    mine = [x for x in P['numstat'] if x.endswith('package.json') or x.endswith('package-lock.json')]
    sg = show(repo, head, '.github/workflows/pr-security-gates.yml')
    t.check('F10', paths == ['**/package.json', '**/package-lock.json'] and len(runs_leg) == 1 and not mine and 'paths-ignore' in nop and 'run-shell-suites.sh' in sg,
            'pr-lockfiles.yml `paths:` %s; its leg-2 invocation %s; #1450 touches package files: %s -> the CHANGED LEG has NO CI run on this PR (the no-op twin pr-lockfiles-noop.yml, `paths-ignore` the exact complement, reports success); the new TEST is reached: pr-security-gates.yml runs run-shell-suites.sh: %s. The PR body says "This PR\'s own CI run is the instrument" for the CI checkout: that is NOT so for the leg itself (a finding to rule)' % (
                paths, runs_leg, mine or 'none', 'run-shell-suites.sh' in sg))
    pf = show(repo, head, 'Blockchain/Dev/scripts/preflight/preflight.sh')
    t.check('F11', 'echo "OK — all locks clean-room-installable"' in pf and 'run_delegated bash scripts/preflight/lockfile-cleanroom.sh' in pf and show(repo, base, 'Blockchain/Dev/scripts/preflight/preflight.sh') == pf,
            'preflight.sh (unchanged base->head) runs the leg through run_delegated (prints the whole output) and then prints `OK — all locks clean-room-installable`: the total-sounding sentence is still there, now under the surface lines')
    docs(repo, head, base, t, P)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    ad, rm = added_removed('a\nb\nc', 'a\nB\nc\nd'); rep(ad == ['B', 'd'] and rm == ['b'], 'added_removed: replace + insert')
    ok, _ = pure_insertion('a\nb\n', 'a\nNEW\nb\n'); rep(ok, 'pure_insertion: one inserted line passes')
    ok, _ = pure_insertion('a\nb\n', 'a\nNEW\nB\n'); rep(not ok, 'PLANTED altered base line FAILS pure_insertion')
    ok, _ = pure_insertion('a\nb\n', 'a\nN1\nb\nN2\n'); rep(not ok, 'PLANTED two separate insertions FAIL (one contiguous block only)')
    ok, _ = pure_insertion('a\nb\n', 'a\nb\n'); rep(not ok, 'PLANTED no change FAILS (nothing inserted)')
    rep(sh_code_only('a\n  # x\nb').split('\n') == ['a', '', 'b'], 'sh_code_only blanks full-line comments only')
    rep(sh_code_only('echo x # KS-1426: y') == 'echo x # KS-1426: y', 'sh_code_only keeps a TRAILING comment on a code line (it is code-line text; F5 counts it separately)')
    rep(blob_id(b'hello\n') == 'ce013625030ba8dba906f756967f9e9ca394464a', 'blob_id: the git blob id of "hello\\n" is ce013625030b (a known value)')
    rep(blob_id(b'hello\n ') != blob_id(b'hello\n'), 'blob_id: one added byte changes the id (the CONTROL of the re-derivations)')
    a = '--- a/x\n+++ b/x\n@@ -1,2 +1,3 @@\n a\n+b\n c\n'
    rep(payload_compare(a, 'diff --git a/x b/x\nindex 1..2 100644\n' + a.replace('@@ -1,2 +1,3 @@', '@@ -1,2 +1,3 @@ check() {'))[0], 'payload_compare: git header lines and the hunk-header function-context text are ignored (equal)')
    rep(not payload_compare(a, a.replace('+b', '+B'))[0], 'PLANTED + line altered -> DIFFERS')
    rep(not payload_compare(a, a.replace(' c', ' C'))[0], 'PLANTED context line altered -> DIFFERS')
    rep(not payload_compare(a, a.replace('+1,3', '+1,4'))[0], 'PLANTED hunk-header number altered -> DIFFERS')
    rep(not payload_compare(a, a.replace('x', 'y'))[0], 'PLANTED different file set -> DIFFERS')
    src = 'a\nfoo() {\n  git x || true\n  git y\n  return 0\n}\nz\n'
    s0, e0, bd = sh_function(src, 'foo'); rep((s0, e0) == (2, 6) and bd[-1] == '}', 'sh_function reads the function span (lines 2-6)')
    gc = git_calls(bd); rep(len(gc) == 2 and [c[2] for c in gc] == [True, False], 'git_calls: two calls, the first guarded by `||`, the second not')
    try: sh_function('foo() {\n}\nfoo() {\n}\n', 'foo'); rep(False, 'a function defined twice was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a function defined twice -> refused')
    try: sh_function('x\n', 'foo'); rep(False, 'an absent function was ACCEPTED')
    except SystemExit: rep(True, 'ARM: an absent function -> refused')
    try: req(['--repo', 'x', '--head', 'abc'], '--head', hex40=True); rep(False, 'short head ACCEPTED')
    except SystemExit: rep(True, 'REQUIRED-ARG ARM short --head -> refused')
    for foreign in (1441, 1443, 1444, 1446, 1447, 1448, 1449):
        try: PR(foreign); rep(False, '--pr %s ACCEPTED' % foreign)
        except SystemExit: rep(True, 'WRONG-PR ARM --pr %s (not the gated PR) -> refused' % foreign)
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A or A[0] != 'claims': print(__doc__); return 2
    try:
        repo = req(A, '--repo'); n = req(A, '--pr'); head = req(A, '--head', True); base = req(A, '--base', True); PR(n)
    except SystemExit as e:
        print(e); return 2
    for s, nm in ((head, 'head'), (base, 'base')):
        if not resolvable(repo, s): print('REFUSED: %s %s is not in %s' % (nm, s, repo)); return 2
    print('C2 claims #%s head %s base %s repo %s' % (n, head, base, repo))
    try:
        return run1450(repo, head, base)
    except SystemExit as e:   # a wrong head / foreign PR's tree makes a helper refuse: that is a FAIL of the claims, not a crash
        print('FAIL C2-REFUSED %s' % e); return 1


if __name__ == '__main__':
    sys.exit(main())
