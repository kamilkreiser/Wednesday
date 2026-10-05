#!/usr/bin/env python3
"""c1_pin_gate63.py — C1 PIN + SCOPE for #1388 (KS-1404 wiring, T1). READ verbs only (lib_gate63.git); measures, then judges.

  P1  origin (ONE ls-remote): refs/pull/1388/head == the exact kit branch == --head. develop is RECORDED (INFO) and must
      DESCEND from the base (merge-base --is-ancestor) — a moved develop is expected, never a FAIL here    (skipped: --no-remote)
  P2  EXACTLY one parent, == the kit base f01c1da5717f (single-parent head; the merge-in is Q-M's)
  P3  EXACTLY the 9 kit paths, each with the kit +/- by `git diff --numstat base head` (both ways: none extra, none missing)
  P4  head^{tree} == kit end_tree 979926afe755; CONTROL base^{tree} differs
  P5  `%(trailers)` RAW bytes == 1; CONTROL bf277eead268 raw bytes == 55 (else the instrument is blind)
  P6  Co-Authored-By lines in the head message == 0; CONTROL bf277eead268 carries >= 1
  P7  subject == kit subject (85 chars), <= 92, no `(#`
  P8  ONE `Refs KS-1404` line; the ONLY hyphenated key is KS-1404; STRICT closing references (lib STRICT_CLOSE_RX) == 0 in the
      message, beside a planted CONTROL string that must score 2. WIDE (120-char) hits are printed as INFO for the gate to rule.
  P9  `git ls-tree` modes of the 9 paths: all 100644 (core.filemode is false in the checkout: never ls -l)
  P10 COMPOSE HUNKS: every hunk of `git diff -U0 base head -- compose` lies inside the `  timestamping:` block whose range is read
      FROM THE BASE TREE (2-space-indent key boundaries, the same rule as the PR's own test); CONTROL the range is non-empty and
      the next key is `  anchoring:`
  P11 COMPOSE SEMANTICS (security: nothing else in compose changed): the timestamping `environment:` entries at base vs head
      differ by EXACTLY one ADDED key, TSA_TRUST_ANCHORS_PEM, whose value is exactly the kit entry; 0 removed, 0 changed keys;
      every other added/removed line is a `#` comment; every line OUTSIDE the block is byte-identical
  P12 DOCKERFILE: 0 removed lines; exactly ONE added non-comment line == `COPY --from=builder /app/config ./config`; it sits in
      the FINAL stage (after the last FROM) and BEFORE `chmod -R a+rX`; every other added line is a `#` comment
  P13 the kit's must-be-unchanged paths (production compose, both .env.example, package.json/lock, openapi, the old KS-1404
      test, the two-root bundle, .dockerignore) have IDENTICAL blobs at base and head; CONTROL the compose blob differs

Usage: c1_pin_gate63.py --repo <git dir> [--head <sha>] [--no-remote]  |  --selftest
rc 0 all PASS / rc 1 any FAIL (or 0 checked)."""
import copy, io, contextlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate63 import K, git, Tally, STRICT_CLOSE_RX, WIDE_CLOSE_RX, KEY_RX

PLANTED = 'Fixes KS-1404 and closes #42'


def ts_block_range(text):
    """0-based [start, end) of the `  timestamping:` block by 2-space-indent key boundaries (the PR test's own rule)."""
    lines = text.split('\n')
    starts = [i for i, l in enumerate(lines) if l.startswith(K['compose_block_key'])]
    if len(starts) != 1:
        return None, None, None
    s = starts[0]; e = len(lines)
    for i in range(s + 1, len(lines)):
        l = lines[i]
        if l.startswith('  ') and not l.startswith('   ') and l.strip().endswith(':'):
            e = i; break
    return s, e, (lines[e].strip() if e < len(lines) else None)


def env_entries(block_lines):
    out = {}; at = [i for i, l in enumerate(block_lines) if l.strip() == 'environment:']
    if not at:
        return out
    for l in block_lines[at[0] + 1:]:
        if not l.strip():
            continue
        ind = len(l) - len(l.lstrip())
        if ind < 6:
            break
        if l.strip().startswith('#') or not re.match(r'^\s{6}- ', l):
            continue
        m = l.strip()[2:]
        if '=' in m:
            k, v = m.split('=', 1); out[k] = v
    return out


def hunks_u0(diff_text):
    """[(old_start, old_count, new_start, new_count, removed_lines, added_lines)] from a -U0 diff."""
    out = []; cur = None
    for l in diff_text.split('\n'):
        m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', l)
        if m:
            cur = [int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1), [], []]; out.append(cur); continue
        if cur is not None and l.startswith('-') and not l.startswith('---'):
            cur[4].append(l[1:])
        elif cur is not None and l.startswith('+') and not l.startswith('+++'):
            cur[5].append(l[1:])
    return out


def measure(repo, head, remote=True):
    base = K['base']; m = {'head': head, 'base': base}
    if remote:
        ls = git(repo, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/heads/' + K['branch'], 'refs/pull/%s/head' % K['pr'])
        refs = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
        dev = refs.get('refs/heads/develop')
        rc = git(repo, 'merge-base', '--is-ancestor', base, dev, check=False)[0] if dev and git(repo, 'cat-file', '-t', dev, check=False)[0] == 0 else None
        m['ls'] = {'develop': dev, 'branch': refs.get('refs/heads/' + K['branch']), 'pull': refs.get('refs/pull/%s/head' % K['pr']),
                   'develop_descends': (rc == 0) if rc is not None else None}
    m['parents'] = git(repo, 'log', '-1', '--format=%P', head).split()
    ns = {}
    for l in git(repo, 'diff', '--numstat', base, head).splitlines():
        a, d, p = l.split('\t', 2); ns[p] = [int(a), int(d)]
    m['numstat'] = ns
    m['tree'] = git(repo, 'rev-parse', head + '^{tree}').strip()
    m['base_tree'] = git(repo, 'rev-parse', base + '^{tree}').strip()
    m['trailer_bytes'] = len(git(repo, 'log', '-1', '--format=%(trailers)', head).encode())
    ctl = K['trailer_control_commit']
    m['control_trailer_bytes'] = len(git(repo, 'log', '-1', '--format=%(trailers)', ctl).encode())
    m['message'] = git(repo, 'log', '-1', '--format=%B', head)
    m['control_coauthor'] = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', ctl)))
    m['subject'] = git(repo, 'log', '-1', '--format=%s', head).rstrip('\n')
    modes = {}
    for l in git(repo, 'ls-tree', head, '--', *K['files'].keys()).splitlines():
        meta, p = l.split('\t', 1); modes[p] = meta.split()[0]
    m['modes'] = modes
    m['compose_base'] = git(repo, 'show', '%s:%s' % (base, K['compose']))
    m['compose_head'] = git(repo, 'show', '%s:%s' % (head, K['compose']))
    m['compose_diff'] = git(repo, 'diff', '-U0', base, head, '--', K['compose'])
    m['docker_base'] = git(repo, 'show', '%s:%s' % (base, K['dockerfile']))
    m['docker_head'] = git(repo, 'show', '%s:%s' % (head, K['dockerfile']))
    m['docker_diff'] = git(repo, 'diff', '-U0', base, head, '--', K['dockerfile'])
    m['unchanged'] = {p: (git(repo, 'rev-parse', '%s:%s' % (base, p)).strip(), git(repo, 'rev-parse', '%s:%s' % (head, p)).strip())
                      for p in K['must_be_unchanged']}
    m['compose_blobs'] = (git(repo, 'rev-parse', '%s:%s' % (base, K['compose'])).strip(), git(repo, 'rev-parse', '%s:%s' % (head, K['compose'])).strip())
    return m


def judge(m, t):
    if 'ls' in m:
        L = m['ls']
        t.check('P1', L['pull'] == m['head'] and L['branch'] == m['head'] and L['develop_descends'] is True,
                'origin pull/%s %s | branch %s (want head %s) | develop %s RECORDED, descends from base %s: %s' % (
                    K['pr'], str(L['pull'])[:12], str(L['branch'])[:12], m['head'][:12], str(L['develop'])[:12], K['base'][:12], L['develop_descends']))
    else:
        t.info('P1', 'skipped (--no-remote): origin NOT read — this run proves nothing about origin')
    t.check('P2', m['parents'] == [m['base']], 'parents %s (want exactly [%s])' % ([p[:12] for p in m['parents']], m['base'][:12]))
    want = K['files']
    extra = sorted(set(m['numstat']) - set(want)); missing = sorted(set(want) - set(m['numstat']))
    drift = sorted(p for p in want if p in m['numstat'] and m['numstat'][p] != want[p])
    t.check('P3', not extra and not missing and not drift, '%d paths (want %d); extra %s missing %s +/- drift %s' % (
        len(m['numstat']), len(want), extra, missing, [(p, m['numstat'][p], want[p]) for p in drift]))
    t.check('P4', m['tree'] == K['end_tree'] and m['base_tree'] != m['tree'],
            'head tree %s (want %s); CONTROL base tree %s %s' % (m['tree'][:12], K['end_tree'][:12], m['base_tree'][:12],
                                                                 'differs' if m['base_tree'] != m['tree'] else 'EQUAL (control blind)'))
    t.check('P5', m['trailer_bytes'] == K['trailer_head_bytes_raw'] and m['control_trailer_bytes'] == K['trailer_control_bytes_raw'],
            '%%(trailers) raw head %d byte(s) (want %d); CONTROL %s %d (want %d)' % (
                m['trailer_bytes'], K['trailer_head_bytes_raw'], K['trailer_control_commit'], m['control_trailer_bytes'], K['trailer_control_bytes_raw']))
    co = len(re.findall(r'(?im)^co-authored-by:', m['message']))
    t.check('P6', co == 0 and m['control_coauthor'] >= 1, 'Co-Authored-By in head message %d (want 0); CONTROL %s %d (want >= 1)' % (
        co, K['trailer_control_commit'], m['control_coauthor']))
    s = m['subject']
    t.check('P7', s == K['subject'] and len(s) <= K['subject_max'] and '(#' not in s, 'subject %r, %d chars (want the kit subject, <= %d, no "(#")' % (
        s, len(s), K['subject_max']))
    refs = re.findall(r'(?m)^Refs KS-1404\s*$', m['message']); keys = sorted(set(KEY_RX.findall(m['message'])))
    strict = [x.group(0) for x in STRICT_CLOSE_RX.finditer(m['message'])]; ctl = len(STRICT_CLOSE_RX.findall(PLANTED))
    t.check('P8', len(refs) == 1 and keys == ['KS-1404'] and not strict and ctl == 2,
            '`Refs KS-1404` lines %d (want 1); hyphenated keys %s (want only KS-1404); STRICT closing refs %d %s (want 0); planted CONTROL %r scores %d (want 2)' % (
                len(refs), keys, len(strict), strict, PLANTED, ctl))
    t.info('P8-wide', 'WIDE 120-char closing hits in the message (INFO, the gate rules): %s' % [x.group(0)[:100] for x in WIDE_CLOSE_RX.finditer(m['message'])])
    bad = {p: m['modes'].get(p) for p in K['files'] if m['modes'].get(p) != K['modes_all']}
    t.check('P9', not bad and len(m['modes']) == len(K['files']), '%d modes read; not %s: %s' % (len(m['modes']), K['modes_all'], bad))
    # P10 compose hunks inside the base block
    s0, e0, nxt = ts_block_range(m['compose_base'])
    hk = hunks_u0(m['compose_diff'])
    outside = []
    for h in hk:
        lo = h[0]; hi = h[0] + max(h[1], 1) - 1   # 1-based old-side lines; a pure insert (count 0) sits AFTER old line h[0]
        if s0 is None or not (s0 + 1 <= lo and hi <= e0):
            outside.append((h[0], h[1], h[2], h[3]))
    t.check('P10', s0 is not None and nxt == 'anchoring:' and hk and not outside,
            'BASE block `  timestamping:` lines %s-%s (1-based), next key %r; hunks (old,cnt,new,cnt) %s; outside the block %s' % (
                (s0 + 1) if s0 is not None else None, e0, nxt, [(h[0], h[1], h[2], h[3]) for h in hk], outside))
    # P11 compose semantics
    bl = m['compose_base'].split('\n'); hl = m['compose_head'].split('\n')
    s1, e1, _ = ts_block_range(m['compose_head'])
    eb = env_entries(bl[s0:e0]) if s0 is not None else {}; eh = env_entries(hl[s1:e1]) if s1 is not None else {}
    added = sorted(set(eh) - set(eb)); removed = sorted(set(eb) - set(eh)); changed = sorted(k for k in eb if k in eh and eb[k] != eh[k])
    k_new, v_new = K['compose_new_entry'].split('=', 1)
    noncomment = [x for h in hk for x in h[4] + h[5] if x.strip() and not x.strip().startswith('#') and x.strip() != '- ' + K['compose_new_entry']]
    outside_eq = s0 is not None and s1 is not None and bl[:s0] == hl[:s1] and bl[e0:] == hl[e1:]
    t.check('P11', added == [k_new] and eh.get(k_new) == v_new and not removed and not changed and not noncomment and outside_eq,
            'env entries base %d head %d; added %s value %r; removed %s; changed %s; non-comment changed lines other than the entry %s; outside-block lines identical %s' % (
                len(eb), len(eh), added, eh.get(k_new), removed, changed, noncomment, outside_eq))
    # P12 Dockerfile
    dk = hunks_u0(m['docker_diff']); rem = [x for h in dk for x in h[4]]; add = [x for h in dk for x in h[5]]
    code_add = [x for x in add if x.strip() and not x.strip().startswith('#')]
    dl = m['docker_head'].split('\n'); froms = [i for i, l in enumerate(dl) if re.match(r'^FROM ', l)]
    cp = [i for i, l in enumerate(dl) if l.strip() == K['dockerfile_new_line']]; ch = [i for i, l in enumerate(dl) if re.search(r'chmod -R a\+rX', l)]
    order = bool(froms and len(cp) == 1 and len(ch) == 1 and froms[-1] < cp[0] < ch[0])
    t.check('P12', not rem and code_add == [K['dockerfile_new_line']] and order,
            'removed %d; added non-comment %s; last FROM :%s, COPY config :%s, chmod :%s (want FROM < COPY < chmod) %s' % (
                len(rem), code_add, froms[-1] + 1 if froms else None, [c + 1 for c in cp], [c + 1 for c in ch], order))
    moved = {p: (a[:12], b[:12]) for p, (a, b) in m['unchanged'].items() if a != b}
    cb = m['compose_blobs']
    t.check('P13', not moved and cb[0] != cb[1], '%d must-be-unchanged paths; changed %s; CONTROL compose blob %s -> %s %s' % (
        len(m['unchanged']), moved, cb[0][:12], cb[1][:12], 'differs' if cb[0] != cb[1] else 'EQUAL (control blind)'))


def selftest(repo):
    """synthetic + REAL-text arms: the good fixture is the REAL measurement at the kit head (no remote), each arm mutates a copy."""
    real = measure(repo, K['head'], remote=False)
    real['ls'] = {'develop': K['develop_at_draft'], 'branch': K['head'], 'pull': K['head'], 'develop_descends': True}
    def run(m):
        t = Tally(); buf = io.StringIO()
        with contextlib.redirect_stdout(buf): judge(m, t)
        return t
    t0 = run(real); ok = int(not t0.fails and t0.n == 13); total = 1
    print('SELFTEST %s T0 positive control (REAL head measurement): %d checked, fails %s' % ('OK' if ok else 'MISS', t0.n, t0.fails))
    E = K['compose_new_entry']
    def comp(fn):
        def mut(m):
            new = fn(m['compose_head']); assert new != m['compose_head'], 'compose tamper did not land'
            m['compose_head'] = new
            import difflib
            a = m['compose_base'].split('\n'); b = new.split('\n'); out = []
            for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                if o[0] == 'equal': continue
                out.append('@@ -%d,%d +%d,%d @@' % (o[1] + 1 if o[2] > o[1] else o[1], o[2] - o[1], o[3] + 1 if o[4] > o[3] else o[3], o[4] - o[3]))
                out += ['-' + x for x in a[o[1]:o[2]]] + ['+' + x for x in b[o[3]:o[4]]]
            m['compose_diff'] = '\n'.join(out)
        return mut
    def dock(fn):
        def mut(m):
            new = fn(m['docker_head']); assert new != m['docker_head'], 'dockerfile tamper did not land'
            m['docker_head'] = new
            import difflib
            a = m['docker_base'].split('\n'); b = new.split('\n'); out = []
            for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                if o[0] == 'equal': continue
                out.append('@@ -%d,%d +%d,%d @@' % (o[1] + 1, o[2] - o[1], o[3] + 1, o[4] - o[3]))
                out += ['-' + x for x in a[o[1]:o[2]]] + ['+' + x for x in b[o[3]:o[4]]]
            m['docker_diff'] = '\n'.join(out)
        return mut
    def once(s, a, b):
        assert s.count(a) == 1, 'anchor must occur exactly once (%d): %r' % (s.count(a), a[:60]); return s.replace(a, b)
    arms = [
        ('a 10th path', lambda m: m['numstat'].update({'Blockchain/Dev/.env.example': [1, 0]}), ['P3']),
        ('+/- drift on compose', lambda m: m['numstat'].update({K['compose']: [8, 1]}), ['P3']),
        ('the anchor file missing', lambda m: m['numstat'].pop(K['anchor_file']), ['P3']),
        ('a merge-in (two parents)', lambda m: m.update(parents=[K['base'], 'b' * 40]), ['P2']),
        ('tree == base tree (blind control)', lambda m: m.update(tree=K['base_tree']), ['P4']),
        ('a trailer on the head', lambda m: m.update(trailer_bytes=55), ['P5']),
        ('blind trailer control', lambda m: m.update(control_trailer_bytes=1), ['P5']),
        ('Co-Authored-By in the body', lambda m: m.update(message=m['message'] + 'Co-Authored-By: X <x@invalid>\n'), ['P6']),
        ('subject carries (#1388)', lambda m: m.update(subject=K['subject'] + ' (#1388)'), ['P7']),
        ('a second Refs line', lambda m: m.update(message=m['message'] + 'Refs KS-1404\n'), ['P8']),
        ('KS-1376 hyphenated', lambda m: m.update(message=m['message'] + 'see KS-1376\n'), ['P8']),
        ('"Closes KS-1404" in the message (STRICT)', lambda m: m.update(message=m['message'] + 'Closes KS-1404\n'), ['P8']),
        ('the test at 100755', lambda m: m['modes'].update({K['test']: '100755'}), ['P9']),
        ('origin pull/head moved', lambda m: m['ls'].update(pull='d' * 40), ['P1']),
        ('develop does not descend from base', lambda m: m['ls'].update(develop_descends=False), ['P1']),
        ('compose: the entry moved into the anchoring block', comp(lambda s: once(once(s, '      - ' + E + '\n', ''), '  anchoring:\n', '  anchoring:\n    environment:\n      - ' + E + '\n')), ['P10', 'P11']),
        ('compose: a second env entry changed (LOG_LEVEL)', comp(lambda s: s.replace('      - LOG_LEVEL=${LOG_LEVEL:-info}\n      - PORT=4004', '      - LOG_LEVEL=${LOG_LEVEL:-debug}\n      - PORT=4004', 1)), ['P11']),
        ('compose: default points at the TWO-ROOT bundle', comp(lambda s: once(s, ':-/app/config/tsa-trust-anchors-dtrust.crt}', ':-/app/config/tsa-trust-anchors.crt}')), ['P11']),
        ('compose: a line outside the block edited', comp(lambda s: s.replace('  anchoring:\n    labels:', '  anchoring:\n    labels: ', 1)), ['P10', 'P11']),
        ('Dockerfile: COPY moved AFTER the chmod', dock(lambda s: once(once(s, 'COPY --from=builder /app/config ./config\n', ''), 'RUN chmod -R a+rX /app /shared\n', 'RUN chmod -R a+rX /app /shared\nCOPY --from=builder /app/config ./config\n')), ['P12']),
        ('Dockerfile: a second code line (USER root)', dock(lambda s: once(s, 'COPY --from=builder /app/config ./config\n', 'COPY --from=builder /app/config ./config\nUSER root\n')), ['P12']),
        ('a must-be-unchanged path moved (production compose)', lambda m: m['unchanged'].update({'Blockchain/Dev/docker-compose.production.yml': ('a' * 40, 'b' * 40)}), ['P13']),
    ]
    for name, mut, want in arms:
        m = copy.deepcopy(real); mut(m); t = run(m); total += 1
        new = set(t.fails) - set(t0.fails); g = set(want) <= new; ok += g
        print('SELFTEST %s %s: want NEW FAIL %s | got %s' % ('OK' if g else 'MISS', name, want, sorted(new)))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--help' in A or '-h' in A or not A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    repo = opt('--repo', K['checkout'])
    if '--selftest' in A: raise SystemExit(selftest(repo))
    head = opt('--head', K['head'])
    print('c1_pin_gate63 repo %s head %s base %s remote %s' % (repo, head, K['base'], '--no-remote' not in A))
    t = Tally(); judge(measure(repo, head, remote='--no-remote' not in A), t); raise SystemExit(t.end())
