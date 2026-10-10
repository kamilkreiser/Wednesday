#!/usr/bin/env python3
"""c2_code_gate84.py — the commit's CODE CLAIMS, measured against the diff (read verbs only; no node, no npm). Ported from c2_code_gate83.py; [g84] rebuilt for #1450 AT bbcbea0e3157
(KS-1426: report_surface is now a WRAPPER that runs report_surface_lines in a subshell with git's repository-local variables unset). Every census is taken CODE-ONLY (full-line `#` comments
blanked) BESIDE the raw count.

  c2_code_gate84.py claims --repo R --pr 1450 --head H --base B
  c2_code_gate84.py --selftest

F0  CODE-ONLY multiset of lockfile-cleanroom.sh base -> head: the one `echo "  covered: ..."` line out (re-emitted with a trailing `# KS-1426` comment), 56 code lines in; RAW 72 non-blank in / 1 out
    (numstat 74/1 counts the two added BLANK lines too).
F1  line-level opcodes base -> head are EXACTLY: insert 70 lines before the `FAILED=()` line, then replace 1 line by 4 (the covered echo + the 3-line call); every other line byte-identical
    (the install loop, the `find`, check() and the exit-code lines untouched).
F2  report_surface_lines and report_surface are each defined ONCE; report_surface is CALLED once, at the end of the file, directly under `if [ "$#" -eq 0 ]; then`; the wrapper's body is ONE `( ... )` subshell
    then `return 0` (its last statement); the ONLY `exit` in either function is the wrapper's `exit 0`, INSIDE the subshell; no FAILED+= / CHECKED+= / INFRA_SKIP= / set in either; the ONLY `unset` in the file is
    the wrapper's `unset "$v"` inside the subshell; report_surface_lines is called once, from the wrapper; there is no `set -e` in the leg.
F3  the exit-code lines OUTSIDE the two functions (`exit 0`, `exit 0`, `exit 1`) are identical at base and head (text and order); every one precedes the call: report_surface runs ONLY on an all-OK run
    (the Docker-advisory SKIP, the infra SKIP and the FAIL paths exit first and print no surface line) — a fact beside the PR's claim, for the gate to rule.
F4  THE GIT-CALL CENSUS: report_surface_lines makes 3 git calls and ALL 3 are guarded by `|| {` (gate83: 1 of 3); the wrapper makes 1 (`--local-env-vars`) that is not `||`-guarded but whose output is VALIDATED
    (GIT_DIR must be among the names or the wrapper prints "cannot list" and exits the subshell).
F5  `KS-1426` on script lines: 6 at head (91, 100, 106, 113, 134, 203; base 0), of 74 added; in the test: 2 (lines 3, 107) of 248. The body says exactly that.
F6  the FIRST commit's payload (d1d8b91b7c1f) equals the Spark pass's patch.diff (sha256/16 503b0cda009442f6, 7392 B) modulo ONLY the function-context text git appends to hunk headers: section by section, with the
    normaliser's CONTROLS. (The second commit is NOT part of any payload; the head diff is reported beside it, INFO.)
F7  the new test: 14 `# CELL n` markers; cells 6-9 and 13 RED at the previous head, 10-12 and 14 CONTROL; every git invocation carries `-C "$REPO"` / `-C "$WORK/..."` (list printed); it names neither bootstrap-env.sh
    nor env.example nor .githooks; it DOES name `core.hooksPath` (three `-c core.hooksPath=/dev/null`, a per-command override on its own scratch repo, writing no config); WORK is a mktemp -d under ${TMPDIR:-/tmp}.
F8  line 35 of the script, `cd "$(dirname "$0")/../.."`, is present at base and head at the same line.
F9  line counts: base 133, previous head 167, head 206.
F10 CI reach: 17 workflow files; ONE runs lockfile-cleanroom.sh (pr-lockfiles.yml line 40), whose `paths:` (lines 18-20) are exactly the two package-file globs; #1450 touches neither, so the CHANGED LEG has no CI run on
    this PR (the no-op twin reports success). The new test IS reached: pr-security-gates.yml / security-scan.yml run run-shell-suites.sh.
F11 preflight.sh prints `OK — all locks clean-room-installable` after the leg (unchanged): the sentence that reads like a total is still there.
D1..D6 the docs: each head doc == base prefix + ONE fragment + `</body>\\n</html>\\n` (an exact insert immediately before the closing tags, NOT at the byte tail); fragment sizes 12,055 B / 3,825 B; per-fragment COUNT
    `<h2>53.` x1 in the flow doc and the KS-1426 <h2> x1 in the cheat doc (the matrix cannot see duplicates); the fix round EDITED the fragments in place: prev-vs-head fragment delta reported (INFO); paired-tag
    balance of each fragment (with a planted-unbalanced control).
rc 0 all pass / 1 a FAIL / 2 refused."""
import difflib, hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate84 import K, PR, Tally, git, show, blob, req, resolvable, exact_tail_insert, tag_deltas, TAIL, docs_base


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


def sh_function(src, name):
    """(start_line, end_line, body_lines) of `name() {` .. first `^}` (1-based)."""
    ls = src.split('\n'); s = [i for i, l in enumerate(ls) if l.startswith(name + '() {')]
    if len(s) != 1: raise SystemExit('sh_function: %r defined %d times' % (name, len(s)))
    e = next(i for i in range(s[0] + 1, len(ls)) if ls[i] == '}')
    return s[0] + 1, e + 1, ls[s[0]:e + 1]


def git_calls(body_lines):
    """the lines of a function that invoke `git` -> [(lineno_in_body, text, guarded)]. Echo / comment lines are skipped. A call is guarded when its own line carries `||`."""
    out = []
    for i, l in enumerate(body_lines):
        if re.search(r'(?<![\w/-])git\b', l) and not l.lstrip().startswith(('#', 'echo')):
            out.append((i + 1, l.strip(), '||' in l))
    return out


# ---------------------------------------------------------------- the payload comparison (F6)
def split_sections(diff_text):
    """a unified diff -> {path: [lines]} keyed by the `+++ b/<path>` header; git header lines are dropped; the hunk-header FUNCTION-CONTEXT text is stripped."""
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
    a, b = split_sections(patch_text), split_sections(own_text)
    if set(a) != set(b): return False, 'section sets differ: patch %s vs own %s' % (sorted(a), sorted(b))
    bad = [k for k in a if a[k] != b[k]]
    return not bad, ('sections equal: %s' % sorted(a)) if not bad else 'sections DIFFER: %s' % bad


# ---------------------------------------------------------------- #1450
def run1450(repo, head, base):
    t = Tally(); P = PR(1450); g = P['gate_script']; s = P['suite']; prev = P['prev_head']
    b, h, pv = show(repo, base, g), show(repo, head, g), show(repo, prev, g); ts = show(repo, head, s)
    if not b or not h or not ts or not pv: print('REFUSED: the script or the suite is absent at base / prev / head'); return 2
    cb, ch = sh_code_only(b), sh_code_only(h)
    add, rem = added_removed(cb, ch); raw_a, raw_r = added_removed(b, h)
    t.check('F0', len(rem) == 1 and rem[0].startswith('echo " covered: ${CHECKED[*]-}"') and len(add) == 56 and len(raw_a) == 72 and len(raw_r) == 1,
            'CODE-ONLY multiset in lockfile-cleanroom.sh base %s -> head %s: added %d removed %d | RAW added %d removed %d NON-BLANK lines (numstat %s also counts the 2 added BLANK lines: 72 + 2 = 74) | removed %s | the added code lines include the re-emitted covered echo: %s' % (
                blob(repo, base, g)[-12:], blob(repo, head, g)[-12:], len(add), len(rem), len(raw_a), len(raw_r), P['numstat'][g], rem, any(x.startswith('echo " covered:') for x in add)))
    la, lb, lp = b.split('\n'), h.split('\n'), pv.split('\n')
    ops = [(o[0], o[2] - o[1], o[4] - o[3], o[1] + 1) for o in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if o[0] != 'equal']
    t.check('F1', [(o[0], o[1], o[2]) for o in ops] == [('insert', 0, 70), ('replace', 1, 4)] and la[0] == lb[0],
            'line-level opcodes base -> head: %s (want exactly: insert 70 | replace 1 by 4 (the covered echo re-emitted with its trailing comment, then the 3-line call); every other line byte-identical, so the install loop, the `find`, check() and the exit-code lines are untouched)' % ops)
    try:
        w0, w1, wbody = sh_function(h, 'report_surface'); l0, l1, lbody = sh_function(h, 'report_surface_lines')
    except SystemExit as e:
        t.check('F2', False, str(e)); wbody = lbody = []; w0 = w1 = l0 = l1 = 0
    calls = [i + 1 for i, l in enumerate(lb) if re.match(r'^\s*report_surface\s*$', l)]
    guard = [i + 1 for i, l in enumerate(lb) if l.strip() == 'if [ "$#" -eq 0 ]; then' and i + 1 > w1]
    inner = [i + 1 for i, l in enumerate(lb) if re.match(r'^\s*report_surface_lines\s*$', l)]
    wbody_s = [l.rstrip() for l in wbody]
    sub_open = [i for i, l in enumerate(wbody_s) if l == '    (']; sub_close = [i for i, l in enumerate(wbody_s) if l == '    )']
    exits_w = [i for i, l in enumerate(wbody_s) if re.match(r'^\s*exit\b', l)]
    exits_l = [l for l in lbody if re.match(r'^\s*exit\b', l)]
    bad_tokens = [l.strip() for l in wbody + lbody if re.search(r'FAILED\+=|CHECKED\+=|INFRA_SKIP=|\bset [-+]', l)]
    rets_l = [l.strip() for l in lbody if re.match(r'^\s*return\b', l)]; rets_w = [l.strip() for l in wbody if re.match(r'^\s*return\b', l)]
    unsets = [i + 1 for i, l in enumerate(lb) if re.match(r'^\s*unset\b', l)]
    set_e = [i + 1 for i, l in enumerate(lb) if re.match(r'^\s*set\s+-[a-z]*e', l)]
    t.check('F2', bool(wbody) and bool(lbody) and len(calls) == 1 and calls[0] > w1 and len(guard) == 1 and guard[0] == calls[0] - 1 and lb[calls[0]].strip() == 'fi'
            and len(sub_open) == 1 and len(sub_close) == 1 and sub_open[0] < sub_close[0] and wbody_s[-3] == '    )' and wbody_s[-2].strip() == 'return 0' and rets_w == ['return 0']
            and len(exits_w) == 1 and sub_open[0] < exits_w[0] < sub_close[0] and wbody_s[exits_w[0]].strip() == 'exit 0' and not exits_l and all(r == 'return 0' for r in rets_l)
            and not bad_tokens and b.count('report_surface') == 0 and len(inner) == 1 and w0 < inner[0] < w1 and len(unsets) == 1 and w0 < unsets[0] < w1 and not set_e,
            'report_surface_lines defined lines %d-%d (1x), report_surface (wrapper) lines %d-%d (1x); the wrapper CALLED %d time(s) at line(s) %s, directly under `if [ "$#" -eq 0 ]; then` at %s and closed by `fi`; wrapper = ONE `(...)` subshell (open %s close %s) then `%s` (last statement), return statements %s; `exit` in the wrapper: %d (inside the subshell: %s), in report_surface_lines: %d; report_surface_lines CALLED at %s (inside the wrapper); FAILED+= / CHECKED+= / INFRA_SKIP= / set inside either: %s; `unset` lines in the whole leg %s (want one, inside the wrapper); `set -e` in the leg: %s; mentions of report_surface at base: %d' % (
                l0, l1, w0, w1, len(calls), calls, guard, sub_open, sub_close, wbody_s[-2].strip() if len(wbody_s) > 1 else None, rets_w, len(exits_w), bool(exits_w and sub_open and sub_open[0] < exits_w[0] < sub_close[0]), len(exits_l), inner, bad_tokens or 'none', unsets, set_e or 'none', b.count('report_surface')))
    in_fn = lambda n: (w0 <= n <= w1) or (l0 <= n <= l1)
    exits_b = [(i + 1, l.strip()) for i, l in enumerate(la) if re.match(r'^\s*exit\s+\d', l)]; exits_h = [(i + 1, l.strip()) for i, l in enumerate(lb) if re.match(r'^\s*exit\s+\d', l) and not in_fn(i + 1)]
    t.check('F3', [x[1] for x in exits_b] == [x[1] for x in exits_h] and len(exits_h) == 3 and all(n < calls[0] for n, _ in exits_h),
            'exit-code lines outside the two functions: base %s | head %s (texts equal: %s) | every one precedes the call at line %s: %s -> report_surface is reached ONLY on an all-OK run; the Docker-advisory SKIP, the infra SKIP and the FAIL paths exit first and print no surface line (a FACT beside the PR\'s claim; gate83 ruled it Minor, BLOCKS no)' % (
                exits_b, exits_h, [x[1] for x in exits_b] == [x[1] for x in exits_h], calls[:1], all(n < calls[0] for n, _ in exits_h)))
    gl = git_calls(lbody); gw = git_calls(wbody)
    t.check('F4', len(gl) == 3 and all(c[2] for c in gl) and len(gw) == 1 and not gw[0][2] and 'git_env_has_dir' in h and 'cannot list' in h,
            'THE GIT-CALL CENSUS: report_surface_lines %d call(s), guarded by `||` %d (gate83: 1 of 3); the wrapper %d call(s): %s (not `||`-guarded; its output is VALIDATED: GIT_DIR must be among the names, else "git\'s list of repository-local variables is unusable - cannot list ..." and the subshell exits 0) | c3 `stubs` / `hook` MEASURE every failing variant' % (
                len(gl), sum(1 for c in gl if c[2]), len(gw), [(c[0], c[1][:70]) for c in gw]))
    ks_h = [i + 1 for i, l in enumerate(lb) if 'KS-1426' in l]; ks_b = [i + 1 for i, l in enumerate(la) if 'KS-1426' in l]
    ks_t = [i + 1 for i, l in enumerate(ts.split('\n')) if 'KS-1426' in l]
    t.check('F5', ks_h == [91, 100, 106, 113, 134, 203] and not ks_b and ks_t == [3, 107],
            '`KS-1426` on script lines at head %s (base %s) -> %d of %d added lines (numstat %s; the body: new-file lines 91, 100, 106, 113, 134, 203, "6 of the 74"); in the test: lines %s of %d added lines (the body: "2 of the 248", lines 3, 107)' % (
                ks_h, ks_b, len(ks_h), P['numstat'][g][0], P['numstat'][g], ks_t, P['numstat'][s][0]))
    # F6 the payload (the FIRST commit)
    sp = K['spark']
    if os.path.isfile(sp['patch']):
        pb = open(sp['patch'], 'rb').read(); ph = hashlib.sha256(pb).hexdigest()[:16]
        own = git(repo, 'diff', base, prev, '--', g, s); own_head = git(repo, 'diff', base, head, '--', g, s)
        eq, det = payload_compare(pb.decode('utf-8'), own)
        eq_h, det_h = payload_compare(pb.decode('utf-8'), own_head)
        pt = pb.decode('utf-8'); ctl = []
        def flip_first(txt, prefix, repl):
            ls = txt.split('\n'); i = next(i for i, l in enumerate(ls) if l.startswith(prefix) and not l.startswith(('+++', '---'))); ls[i] = repl(ls[i]); return '\n'.join(ls)
        ctl.append(('a + line altered', not payload_compare(flip_first(pt, '+', lambda l: l + 'x'), own)[0]))
        ctl.append(('a context line altered', not payload_compare(flip_first(pt, ' ', lambda l: l + 'x'), own)[0]))
        ctl.append(('a hunk-header NUMBER altered', not payload_compare(re.sub(r'@@ -88,6', '@@ -89,6', pt, count=1), own)[0]))
        ctl.append(('only the function-context suffix altered (must stay EQUAL)', payload_compare(re.sub(r'(?m)^(@@ -88,6 \+88,37 @@).*$', r'\1 zzz()', own, count=1), own)[0]))
        t.check('F6', ph == sp['patch_sha256_16'] and len(pb) == sp['patch_bytes'] and eq and not eq_h and all(c[1] for c in ctl),
                'patch.diff sha256/16 %s (kit %s), %d B (kit %d); the FIRST commit\'s diff (script + test, base..%s) EQUALS it section by section after stripping ONLY the hunk-header function-context text: %s | the HEAD diff (base..%s) vs patch.diff: %s (EXPECTED to differ: the second commit is the fix round, in no payload) | normaliser controls %s' % (
                    ph, sp['patch_sha256_16'], len(pb), sp['patch_bytes'], prev[:12], det, head[:12], 'EQUAL?!' if eq_h else det_h, ctl))
    else:
        t.info('F6', 'NOT RUN: %s is not readable here (never a pass)' % sp['patch'])
    # F7 the new test
    tl = ts.split('\n'); cells = re.findall(r'(?m)^# CELL (\d+)', ts)
    gitl = [l.strip() for l in tl if re.search(r'(?:^|[\s(`"])git (?:-C|-c) ', l) and not l.lstrip().startswith(('#', 'echo', 'if', 'elif', '&&'))]
    gitl += [l.strip() for l in tl if re.search(r'\$\(git ', l) and not l.lstrip().startswith('#')]
    cdl = [l.strip() for l in tl if re.match(r'\s*cd\b', l) or re.search(r'\$\(cd\b', l)]
    haz = [w for w in ('bootstrap-env.sh', 'env.example', '.githooks') if w in ts or w in h]
    hp = [l.strip() for l in tl if 'hooksPath' in l]
    red_prev = re.findall(r'(?m)^# CELL (\d+) \(RED before the fix', ts)
    t.check('F7', cells == [str(i) for i in range(1, 15)] and haz == [] and all(re.search(r'git -C "\$(REPO|WORK/\w+)"', l) for l in gitl)
            and 'mktemp -d "${TMPDIR:-/tmp}/ks1426.XXXXXX"' in ts and red_prev == ['6', '7', '8', '9', '13'] and len(hp) == 3 and all('-c core.hooksPath=/dev/null' in x for x in hp),
            'the new test: `# CELL n` markers %s (want 1..14); "RED before the fix" cells %s (want 6 7 8 9 13); git invocations %s; `cd` lines %s (the only one is HERE=$(cd ...) resolving its own dir); names bootstrap-env.sh / env.example / .githooks: %s; `hooksPath` lines %d (all per-command `-c core.hooksPath=/dev/null` on the suite\'s OWN scratch repo, no config written) -> the gate82 H9 hazard (TMPDIR inside a repo makes bootstrap-env.sh write that repo\'s core.hooksPath) does NOT apply to this test or to the leg, SAID after reading both whole' % (
                cells, red_prev, [x[:70] for x in gitl], cdl, haz or 'NONE', len(hp)))
    # F8 line 35
    cd_b = [i + 1 for i, l in enumerate(la) if l == 'cd "$(dirname "$0")/../.."   # Blockchain/Dev']; cd_h = [i + 1 for i, l in enumerate(lb) if l == 'cd "$(dirname "$0")/../.."   # Blockchain/Dev']
    t.check('F8', cd_b == cd_h == [35], 'the leg\'s `cd "$(dirname "$0")/../.."` is at line(s) base %s head %s (want [35], unchanged): every git call of the leg runs in the leg\'s own checkout, not the caller\'s cwd (Q-CWD1426 static half; c3 `cwd` MEASURES it)' % (cd_b, cd_h))
    t.check('F9', len(la) - (1 if la[-1] == '' else 0) == P['script_lines']['base'] and len(lp) - (1 if lp[-1] == '' else 0) == P['script_lines']['prev'] and len(lb) - (1 if lb[-1] == '' else 0) == P['script_lines']['head'],
            'script line counts base %d, previous head %d, head %d (kit %d / %d / %d)' % (len(la) - (la[-1] == ''), len(lp) - (lp[-1] == ''), len(lb) - (lb[-1] == ''), P['script_lines']['base'], P['script_lines']['prev'], P['script_lines']['head']))
    # F10 CI reach
    plk, nop = show(repo, head, '.github/workflows/pr-lockfiles.yml'), show(repo, head, '.github/workflows/pr-lockfiles-noop.yml')
    plk_l = plk.split('\n')
    paths = re.findall(r"(?m)^\s+- '([^']+)'", plk.split('paths:')[1].split('permissions:')[0]) if 'paths:' in plk else []
    p_line = [i + 1 for i, l in enumerate(plk_l) if l.strip() == 'paths:']; run_line = [i + 1 for i, l in enumerate(plk_l) if 'lockfile-cleanroom.sh' in l and 'run:' in l]
    wf = [x for x in git(repo, 'ls-tree', '--name-only', head, '.github/workflows/').split('\n') if x]
    users = [x for x in wf if 'lockfile-cleanroom.sh' in show(repo, head, x)]
    mine = [x for x in P['numstat'] if x.endswith('package.json') or x.endswith('package-lock.json')]
    sg = show(repo, head, '.github/workflows/pr-security-gates.yml')
    t.check('F10', paths == ['**/package.json', '**/package-lock.json'] and run_line == [40] and p_line == [18] and len(wf) == 17 and users == ['.github/workflows/pr-lockfiles.yml'] and not mine and 'paths-ignore' in nop and 'run-shell-suites.sh' in sg,
            '%d workflow files; those whose text names lockfile-cleanroom.sh as a run step: %s (the body: "1 of the 17", pr-lockfiles.yml line %s); its `paths:` at line %s (the body: lines 18 to 20) %s; #1450 touches package files: %s -> the CHANGED LEG has NO CI run on this PR (the no-op twin pr-lockfiles-noop.yml, `paths-ignore` the exact complement, reports success); the new TEST is reached: pr-security-gates.yml runs run-shell-suites.sh: %s' % (
                len(wf), users, run_line, p_line, paths, mine or 'none', 'run-shell-suites.sh' in sg))
    pf = show(repo, head, 'Blockchain/Dev/scripts/preflight/preflight.sh')
    t.check('F11', 'echo "OK — all locks clean-room-installable"' in pf and 'run_delegated bash scripts/preflight/lockfile-cleanroom.sh' in pf and show(repo, base, 'Blockchain/Dev/scripts/preflight/preflight.sh') == pf,
            'preflight.sh (unchanged base->head) runs the leg through run_delegated (prints the whole output) and then prints `OK — all locks clean-room-installable`: the total-sounding sentence is still there, now under the surface lines')
    docs(repo, head, base, prev, t, P)
    return t.end()


def docs(repo, head, base, prev, t, P):
    for i, d in enumerate(P['doc_paths']):
        b, h, pv = show(repo, base, d), show(repo, head, d), show(repo, prev, d)
        ok, frag, why = exact_tail_insert(b, h); okp, fragp, whyp = exact_tail_insert(b, pv)
        want = K['docfacts'][d]['fragment_bytes']; fb = len(frag.encode('utf-8')) if ok else -1
        t.check('D1', bool(b) and bool(h) and ok and fb == want and len(h.encode('utf-8')) - len(b.encode('utf-8')) == want,
                '%s: head doc == base prefix + ONE fragment + %r: %s (%s); fragment %d B (kit/seat %d), whole-doc delta %d B; fragment lines %d' % (
                    d.split('/')[-1][:44], TAIL, ok, why, fb, want, len(h.encode('utf-8')) - len(b.encode('utf-8')), len(frag.split('\n')) - 1 if ok else -1))
        h2s = [l for l in frag.split('\n') if '<h2' in l] if ok else []
        if i == 0:
            n_doc = len(re.findall(r'<h2>53\. ', h)); n_prev = len(re.findall(r'<h2>53\. ', pv))
            t.check('D2', len(h2s) == 1 and ('<h2>%s ' % P['flow_block']) in h2s[0] and n_doc == 1 and n_prev == 1, 'flow doc: the fragment has ONE <h2> and it opens <h2>%s (h2 lines %s); per-fragment COUNT of `<h2>53.` in the WHOLE head doc %d (want 1), in the previous head %d' % (P['flow_block'], [x[:70] for x in h2s], n_doc, n_prev))
        else:
            n_doc = len([l for l in h.split('\n') if '<h2' in l and P['cheat_key'] in l]); n_prev = len([l for l in pv.split('\n') if '<h2' in l and P['cheat_key'] in l])
            t.check('D2', len(h2s) == 1 and P['cheat_key'] in h2s[0] and n_doc == 1 and n_prev == 1, 'cheat doc: the fragment has ONE <h2> and it carries %s (h2 lines %s); per-fragment COUNT of the KS-1426 <h2> in the WHOLE head doc %d (want 1), in the previous head %d' % (P['cheat_key'], [x[:90] for x in h2s], n_doc, n_prev))
        dl = tag_deltas(frag) if ok else {'?': 1}; nz = dict((k, v) for k, v in dl.items() if v)
        bad_ctl = tag_deltas(frag + '<div>') if ok else {}
        t.check('D3', ok and not nz and bad_ctl.get('div', 0) != dl.get('div', 0), '%s: paired-tag open-minus-close deltas of the fragment %s (nonzero: %s) | CONTROL: the same fragment with one planted `<div>` reads div delta %s (the check can fail)' % (d.split('/')[-1][:44], dl, nz or 'none', bad_ctl.get('div')))
        # the fix round EDITED the fragment in place: report the prev-vs-head fragment delta (INFO)
        a_, r_ = added_removed(fragp, frag) if (ok and okp) else ([], [])
        t.info('D4', '%s: previous head fragment %d B (exact insert against the base: %s) -> head fragment %d B; non-blank lines added %d removed %d between the two (the fix round edited the fragments IN PLACE; the keep-both merge-in uses the HEAD fragment against the BASE)' % (
            d.split('/')[-1][:44], len(fragp.encode('utf-8')) if okp else -1, okp, fb, len(a_), len(r_)))
    b = show(repo, base, P['doc_paths'][0]); h = show(repo, head, P['doc_paths'][0])
    t.check('D1-CONTROL', not exact_tail_insert(b, h.replace('<html', '<HTML', 1))[0] and h.count('<html') + h.count('<HTML') > 0, 'CONTROL: the head doc with one base byte altered is NOT an exact tail insert (the instrument can fail)')
    mb, info = docs_base(repo, K['develop_at_draft'], head, base) if resolvable(repo, K['develop_at_draft']) else (None, None)
    t.info('D5', 'docs parent: merge-base(develop %s, head) = %s; head^ = %s (the PREVIOUS head) -> the fragment base is the merge-base, NEVER head^ (G83-1)' % (K['develop_at_draft'][:12], (mb or 'develop not in the store')[:12], (info or {}).get('head_parent', '?')[:12]))


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    ad, rm = added_removed('a\nb\nc', 'a\nB\nc\nd'); rep(ad == ['B', 'd'] and rm == ['b'], 'added_removed: replace + insert')
    ok, f, _ = exact_tail_insert('a\n' + TAIL, 'a\nNEW\n' + TAIL); rep(ok and f == 'NEW\n', 'exact_tail_insert: one inserted line before the tail passes')
    ok, _, _ = exact_tail_insert('a\n' + TAIL, 'A\nNEW\n' + TAIL); rep(not ok, 'PLANTED altered base line FAILS exact_tail_insert')
    ok, _, _ = exact_tail_insert('a\n' + TAIL, 'a\nN1\n' + TAIL + 'N2\n'); rep(not ok, 'PLANTED insert after the tail FAILS')
    ok, _, _ = exact_tail_insert('a\n' + TAIL, 'a\n' + TAIL); rep(not ok, 'PLANTED no change FAILS (nothing inserted)')
    rep(tag_deltas('<table><tr><td>x</td></tr></table>') == {'table': 0, 'tr': 0, 'td': 0} and tag_deltas('<div><div></div>')['div'] == 1, 'tag_deltas: a balanced fragment reads zeros; a planted unclosed <div> reads +1')
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
    for s, nm in ((head, 'head'), (base, 'base'), (PR(n)['prev_head'], 'previous head')):
        if not resolvable(repo, s): print('REFUSED: %s %s is not in %s' % (nm, s, repo)); return 2
    print('C2 claims #%s head %s base %s repo %s' % (n, head, base, repo))
    try:
        return run1450(repo, head, base)
    except SystemExit as e:   # a wrong head / foreign PR's tree makes a helper refuse: that is a FAIL of the claims, not a crash
        print('FAIL C2-REFUSED %s' % e); return 1


if __name__ == '__main__':
    sys.exit(main())
