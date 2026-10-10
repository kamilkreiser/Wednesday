#!/usr/bin/env python3
"""c2_code_gate82.py — the commits' CODE CLAIMS, measured against the diffs (read verbs only; `node -e` evaluates a pure expression, nothing else).
Carried in shape from c2_code_gate81.py `claims`; [g82] rebuilt for #1447, #1449 and #1448. Every census is taken CODE-ONLY (comments blanked, strings
kept) BESIDE the raw count. EACH PR has its OWN base (#1447/#1448 76b683c7dcd0, #1449 f247ff85b612): --base is that PR's parent.

  c2_code_gate82.py claims --repo R --pr 1447|1448|1449 --head H --base B
  c2_code_gate82.py --selftest

#1447 (run-migrations.sh failed-run message, KS-1456): M0 CODE-ONLY (full-line # comments blanked) multiset: the two `echo` lines that carried the
  sentence out, ONE `echo` in, raw +2/-2 (one of the two added raw lines is the Q-5D1456 comment); M1 the failed-run message block, exit code, Summary line and
  clean-run tail are byte-identical outside those lines; M2 the closed-defect claim: commit ae9bf6828f88 is an ancestor of the base and the runner counts
  skips apart (`skipped_count`, `applied_count=$((applied_count - skipped_count))`) at base AND head; M3 the ONE added comment line carries the key once, prints
  nothing, line number measured (the seat says :189); M4 the stale comment (KS-808 carries what is left) still present at head (the NOT-covered item, INFO);
  M5 the new test: 4 cells, cell 1 greps `counts-skips` AND `the remaining`; M6 no sibling or test greps the removed sentences (CONTROL: a present string reads >0);
  M7 the payload / as-committed blob ids RE-DERIVED (head minus the comment line == the seat's payload blob 7fd5f2ef2969; head == 1ba0f332a807; test == 0ef305a4a013);
  M8 the dangling `WARN: ... Pre-existing` echo is unchanged (INFO); M9 hyphenated foreign keys in ADDED lines (INFO).
#1449 (env.example, KS-1417): E0 CODE-ONLY diff of env.example: the `API_GATEWAY_PORT=6882` line out, 0 code lines in, raw +3/-1; E1 the key census at base: exactly the
  two template lines, 0 outside *.example, CONTROL `GATEWAY_PORT` hits >> 0; at head the census; E2 GATEWAY_PORT drives the gateway (stack_env.sh and docker-compose.yml
  lines measured); E3 bootstrap-env.sh, stack_env.sh, env.local.example, .env.example byte-identical base/head; the copy-only-when-.env-missing condition and the
  :315-324 hooksPath lines measured; E4 the new test: exactly ONE `cd "$TREE"` line, before the bootstrap invocation, 4 cells; E5 the two payload deviations RE-DERIVED
  (head minus the WHY line == 14c5eee2dfc5, head == 7e40960da9aa; test minus the cd line == ebfa7933d1ab, test == c06e085c439e); E6 the sibling probe moves (the
  `bootstrap_env_canonical_template` selection rule computed at base and head); E7 the "every clone's .env" wording census (commit message, both doc blocks); E8 the sibling
  roster (git grep) and the siblings that call bootstrap-env.sh WITHOUT a cd (the same hooksPath exposure, INFO).
#1448 (security.openapi.ts, KS-1434): S0 CODE-ONLY multiset: only the `rotate` property (raw +13/-0, the comment lines are WHY); S1 yaml: ONE hunk of 10 insertions, 0 removals,
  inside ApiKeyCreateRequest, `required` still [name]; S2 DESCRIPTION EQUALITY: the TS description (the string literals joined) equals the yaml description (folded lines joined);
  S3 runtime untouched: index.ts / requestSchemas.ts byte-identical base/head; S4 THE WORDING TRACE: each clause of the description traced to a measured line of
  services/security/src/index.ts at the head; S5 the five named wording gaps (W-GAP-1 grace parse, W-GAP-2 the "In that case" antecedent, W-GAP-3 the response schema,
  W-GAP-4 count semantics, W-GAP-5 Schemathesis exposure) as FACTS; S6 the test file: 7 cells, the EXISTING list equals the base yaml block's eight properties; S7 the
  security.openapi importers (CODE-ONLY); S8 the 4 consumers of priorKeysRevoked.
ALL THREE: D1 each doc change is a PURE INSERTION (one contiguous block; head minus the block == base byte for byte), immediately before </body>, the flow heading carries
  the kit's number (51. / 52. / 54.) and the cheat heading the kit's key; D1-CONTROL.
rc 0 all pass / 1 a FAIL / 2 refused."""
import difflib, hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate82 import K, PR, Tally, git, show, blob, req, code_only, resolvable


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


def drop_line(text, rx):
    """text minus the ONE line matching rx (refuses unless exactly one line matches) -> (text, lineno)."""
    ls = text.split('\n'); hits = [i for i, l in enumerate(ls) if re.search(rx, l)]
    if len(hits) != 1: raise SystemExit('drop_line: %r matched %d line(s) (want exactly 1)' % (rx[:50], len(hits)))
    return '\n'.join(ls[:hits[0]] + ls[hits[0] + 1:]), hits[0] + 1


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
        t.check('D1c', nxt == '</body>' and frag and frag[0].lstrip().startswith(('<h2', '<div', '<section', '<hr', '<!--')) or nxt == '</body>',
                '%s: the block ends immediately before %r; fragment %d lines, %d bytes (joined with \\n); first line %r' % (d.split('/')[-1], nxt, len(frag), len('\n'.join(frag).encode()), (frag[0] if frag else '')[:70]))
        h2s = [l for l in frag if '<h2' in l]
        if d == P['doc_paths'][0]:
            t.check('D1b', len(h2s) == 1 and ('<h2>%s ' % P['flow_block']) in h2s[0], 'flow doc fragment has ONE <h2> and it opens <h2>%s (h2 lines: %s)' % (P['flow_block'], [x[:70] for x in h2s]))
        else:
            t.check('D1d', len(h2s) == 1 and P['cheat_key'] in h2s[0], 'cheat doc fragment has ONE <h2> and it carries %s (h2 lines: %s)' % (P['cheat_key'], [x[:90] for x in h2s]))
    b = show(repo, base, P['doc_paths'][0]); h = show(repo, head, P['doc_paths'][0])
    t.check('D1-CONTROL', not pure_insertion(b, h.replace('<html', '<HTML', 1))[0] and h.count('<html') + h.count('<HTML') > 0, 'CONTROL: the head doc with one base byte altered is NOT a pure insertion (the instrument can fail)')


def foreign_in_added(repo, head, base, own, t):
    out = {}
    for p in P_numstat(repo, base, head):
        b, h = show(repo, base, p), show(repo, head, p)
        add, _ = added_removed(b, h); ks = sorted(set(k for l in add for k in re.findall(r'\bKS-\d+\b', l) if k != own))
        if ks: out[p.split('/')[-1]] = ks
    t.info('FK', 'hyphenated FOREIGN keys in ADDED lines (own key %s): %s (INFO: a source or doc line is not scanned by Linear; the commit message and PR body are, by c1 P8 and gh prtext)' % (own, out or 'none'))


def P_numstat(repo, base, head):
    return [l.split('\t')[2] for l in git(repo, 'diff', '--numstat', base, head).strip().split('\n') if l]


def test_cells(ts):
    return len(re.findall(r'^# CELL \d', ts, re.M))


# ---------------------------------------------------------------- #1447
def run1447(repo, head, base):
    t = Tally(); P = PR(1447); g = P['gate_script']; s = P['suite']
    b, h = show(repo, base, g), show(repo, head, g)
    if not b or not h: print('REFUSED: run-migrations.sh absent at base or head'); return 2
    cb, ch = sh_code_only(b), sh_code_only(h)
    add, rem = added_removed(cb, ch); raw_a, raw_r = added_removed(b, h)
    want_rem = ['echo "002/005 failing every boot) were changed under KS-1031; the remaining"', 'echo "applied=N-counts-skips defect is KS-808. Exit 3 - the code this"']
    want_add = ['echo "002/005 failing every boot) were changed under KS-1031. Exit 3 - the code this"']
    t.check('M0', sorted(rem) == sorted(want_rem) and sorted(add) == sorted(want_add) and len(raw_a) == 2 and len(raw_r) == 2,
            'CODE-ONLY multiset in run-migrations.sh base %s -> head %s: added %d removed %d | RAW added %d removed %d (numstat %s: the second added raw line is the Q-5D1456 comment) | removed %s | added %s' % (
                blob(repo, base, g)[-12:], blob(repo, head, g)[-12:], len(add), len(rem), len(raw_a), len(raw_r), P['numstat'][g], [x[:70] for x in rem], [x[:70] for x in add]))
    # M1: the whole file differs from base ONLY by (a) two echo lines becoming one, (b) one inserted comment line: everything else is byte-identical
    la, lb = b.split('\n'), h.split('\n')
    ops = [(o[0], o[2] - o[1], o[4] - o[3], o[1] + 1) for o in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if o[0] != 'equal']
    t.check('M1', ops == [('replace', 2, 1, ops[0][3] if ops else 0), ('insert', 0, 1, ops[1][3] if len(ops) > 1 else 0)] and 'exit 3' in h and 'Summary: applied=$applied_count failed=$failed_count skipped=$skipped_count' in h and lb[0] == la[0],
            'line-level opcodes base -> head: %s (want exactly: a 2-line -> 1-line replace at one place, then a 1-line insert; every other line byte-identical, so the Summary line, the exit-3 line and the clean-run tail are untouched); `exit 3` present %s; the Summary line present %s' % (
                ops, 'exit 3' in h, 'Summary: applied=' in h))
    # M2: the closed-defect claim
    C = 'ae9bf6828f88'; anc = git(repo, 'merge-base', '--is-ancestor', C, base, check=False)[0] == 0 if resolvable(repo, C) else None
    subj = git(repo, 'log', '-1', '--format=%s', C).strip() if resolvable(repo, C) else 'NOT IN THE STORE'
    need = ['applied_count=$((applied_count - skipped_count))', 'skipped_count=$((skipped_count + 1))']
    have_b = [n in b for n in need]; have_h = [n in h for n in need]
    t.check('M2', anc is True and all(have_b) and all(have_h),
            'the closed-defect claim: commit %s (%r) is an ancestor of the base: %s; the runner counts skips apart at BASE %s and HEAD %s (lines %s) — the sentence "the remaining applied=N-counts-skips defect" has no live defect behind it in THIS file (whether KS-808 has OTHER open items is a Linear question: KS-808 may be read)' % (
                C, subj[:70], anc, have_b, have_h, [i + 1 for i, l in enumerate(h.split('\n')) if 'skipped_count' in l][:8]))
    # M3: the ONE added comment line
    cm = [(i + 1, l) for i, l in enumerate(h.split('\n')) if re.match(r'\s*# KS-1456:', l)]
    t.check('M3', len(cm) == 1 and cm[0][1].lstrip().startswith('# ') and h.count('KS-1456') == 1,
            'the Q-5D1456 comment line: %d line(s) matching `# KS-1456:` at line %s (the seat says :189), full-line `#` comment (prints nothing): %s | text %r' % (
                len(cm), [c[0] for c in cm], bool(cm and cm[0][1].lstrip().startswith('# ')), (cm[0][1].strip()[:100] if cm else None)))
    stale = [(i + 1, l.strip()) for i, l in enumerate(h.split('\n')) if 'KS-808 carries what' in l or 'cites Linear keys' in l]
    t.info('M4', 'the stale comment the PR lists as NOT covered, at the head (line, text): %s' % stale)
    ts = show(repo, head, s)
    c1 = ts[ts.find('# CELL 1'):ts.find('# CELL 2')]
    t.check('M5', test_cells(ts) == 4 and "grep -qF 'counts-skips'" in c1 and "grep -qF 'the remaining'" in c1 and 'RUN_MIGRATIONS_SH' in ts and 'PATH="$WORK/bin:/usr/bin:/bin"' in ts,
            'new test %s: %d `# CELL` markers (the seat says 4); cell 1 greps `counts-skips` AND `the remaining` (it does NOT test for any OTHER wording: see the tamper rows); the RUN_MIGRATIONS_SH override and the private-PATH psql / pg_isready stubs are present; psql stub fails the migrations named in PSQL_FAIL' % (s.split('/')[-1], test_cells(ts)))
    gr = git(repo, 'grep', '-n', '-E', 'applied=N-counts-skips|defect is KS-808', head, '--', 'Blockchain/Dev/scripts', 'systemTest', '.githooks', check=False)
    hits = [x for x in gr[1].split('\n') if x.strip()] if isinstance(gr, tuple) else []
    ctl = git(repo, 'grep', '-c', 'Summary: applied=', head, '--', 'Blockchain/Dev/scripts/run-migrations.sh', check=False)
    bad = [x for x in hits if 'ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh' not in x and 'run-migrations.sh' not in x]
    t.check('M6', not bad and ctl[0] == 0, 'git grep -E `applied=N-counts-skips|defect is KS-808` over scripts / systemTest / .githooks at the head: %d hit(s), outside the new suite and the runner itself: %s | CONTROL `Summary: applied=` in the runner: rc %s %s' % (
        len(hits), [x[:120] for x in bad] or 'none', ctl[0], ctl[1].strip()[:80]))
    try:
        pay, ln = drop_line(h, r'^\s*# KS-1456:')
        ok7 = blob_id(pay)[:12] == '7fd5f2ef2969' and blob_id(h)[:12] == '1ba0f332a807' and blob_id(ts)[:12] == '0ef305a4a013'
        t.check('M7', ok7, 'RE-DERIVED blob ids: head minus the comment line (line %d) = %s (the seat says payload 7fd5f2ef2969) | head = %s (as-committed 1ba0f332a807) | test = %s (0ef305a4a013) | CONTROL the head with one byte changed = %s' % (
            ln, blob_id(pay)[:12], blob_id(h)[:12], blob_id(ts)[:12], blob_id(h + ' ')[:12]))
    except SystemExit as e:
        t.check('M7', False, str(e))
    t.info('M8', 'the dangling line before the ERROR echo (unchanged base/head: %s): %r' % (
        [l for l in b.split('\n') if 'Pre-existing' in l] == [l for l in h.split('\n') if 'Pre-existing' in l], [l.strip() for l in h.split('\n') if 'Pre-existing' in l]))
    foreign_in_added(repo, head, base, 'KS-1456', t)
    docs(repo, head, base, t, P)
    return t.end()


# ---------------------------------------------------------------- #1449
def var_names(txt): return sorted(set(re.findall(r'(?m)^([A-Z][A-Z0-9_]*)=', txt)))


def run1449(repo, head, base):
    t = Tally(); P = PR(1449); tpl = P['template']; oth = P['template_other']; s = P['suite']
    b, h = show(repo, base, tpl), show(repo, head, tpl)
    if not b or not h: print('REFUSED: env.example absent at base or head'); return 2
    cb, ch = sh_code_only(b), sh_code_only(h)
    add, rem = added_removed(cb, ch); raw_a, raw_r = added_removed(b, h)
    t.check('E0', add == [] and rem == ['API_GATEWAY_PORT=6882'] and len(raw_a) == 3 and len(raw_r) == 1,
            'CODE-ONLY diff of env.example base %s -> head %s: added %d removed %d (%s) | RAW added %d removed %d (numstat %s: the three added raw lines are comments) | added raw %s' % (
                blob(repo, base, tpl)[-12:], blob(repo, head, tpl)[-12:], len(add), len(rem), rem, len(raw_a), len(raw_r), P['numstat'][tpl], [x[:60] for x in raw_a]))
    def census(rev):
        r = git(repo, 'grep', '-n', 'API_GATEWAY_PORT', rev, '--', '.', ':!*.html', check=False)
        lines = [x.split(':', 1)[1] if x.startswith(rev + ':') else x for x in r[1].split('\n') if x.strip()]
        return lines
    cb_, ch_ = census(base), census(head)
    gp = git(repo, 'grep', '-c', '-w', 'GATEWAY_PORT', base, '--', '.', ':!*.html', ':!*.example', check=False)[1]
    gp_lines = sum(int(x.rsplit(':', 1)[1]) for x in gp.strip().split('\n') if x.strip())
    out_tpl_b = [x for x in cb_ if not x.split(':')[0].endswith('.example')]
    t.check('E1', len(cb_) == 2 and not out_tpl_b and gp_lines == 86,
            'API_GATEWAY_PORT census (git grep, *.html excluded) at the BASE: %d line(s) %s, outside *.example: %d | CONTROL the WHOLE-WORD `GATEWAY_PORT` (git grep -w) outside templates and *.html at base: %d matching line(s) (the body says 86; a substring count reads more because other keys END in GATEWAY_PORT, so the word match is the one that reproduces the body) | at the HEAD: %d line(s) %s' % (
                len(cb_), [x[:60] for x in cb_], len(out_tpl_b), gp_lines, len(ch_), [x[:70] for x in ch_]))
    se = show(repo, head, 'Blockchain/Dev/scripts/stack_env.sh'); dc = show(repo, head, 'Blockchain/Dev/docker-compose.yml')
    ln_se = [(i + 1, l.strip()) for i, l in enumerate(se.split('\n')) if re.match(r'\s*GATEWAY_PORT=', l)]
    ln_dc = [(i + 1, l.strip()) for i, l in enumerate(dc.split('\n')) if '${GATEWAY_PORT' in l]
    t.check('E2', bool(ln_se) and bool(ln_dc), 'GATEWAY_PORT drives the gateway: stack_env.sh %s | docker-compose.yml %s' % (ln_se[:2], ln_dc[:2]))
    same = [blob(repo, base, x) == blob(repo, head, x) and bool(blob(repo, head, x)) for x in ('Blockchain/Dev/scripts/bootstrap-env.sh', 'Blockchain/Dev/scripts/stack_env.sh', oth, 'Blockchain/Dev/.env.example')]
    be = show(repo, head, 'Blockchain/Dev/scripts/bootstrap-env.sh').split('\n')
    cond = [i + 1 for i, l in enumerate(be) if '[[ -f "$ENV_FILE" ]]' in l][:2]; leave = [i + 1 for i, l in enumerate(be) if 'leaving it untouched' in l][:2]
    hk = [i + 1 for i, l in enumerate(be) if 'git rev-parse --show-toplevel' in l]; hs = [i + 1 for i, l in enumerate(be) if 'config core.hooksPath .githooks' in l]
    t.check('E3', all(same) and cond and leave and hk and hs,
            'bootstrap-env.sh, stack_env.sh, env.local.example, .env.example byte-identical base/head: %s | the copy-only-when-.env-is-missing condition at line(s) %s / %s (the body says :76-81) | `git rev-parse --show-toplevel` at line(s) %s and `config core.hooksPath .githooks` at line(s) %s (the body says :315-324)' % (same, cond, leave, hk, hs))
    ts = show(repo, head, s); cds = [(i + 1, l) for i, l in enumerate(ts.split('\n')) if re.match(r'\s*cd "\$TREE"', l)]
    inv = [i + 1 for i, l in enumerate(ts.split('\n')) if 'bash "$TREE/scripts/bootstrap-env.sh"' in l]
    t.check('E4', len(cds) == 1 and inv and cds[0][0] < inv[0] and test_cells(ts) == 4 and '# KS-1417' in cds[0][1],
            'new test %s: exactly %d `cd "$TREE"` line at %s, BEFORE the bootstrap invocation at %s; %d `# CELL` markers (4 claimed); the cd line carries its own `# KS-1417` comment: %s' % (
                s.split('/')[-1], len(cds), [c[0] for c in cds], inv, test_cells(ts), bool(cds and '# KS-1417' in cds[0][1])))
    try:
        pe, l1 = drop_line(h, r'^# KS-1417: this block used to set'); pt, l2 = drop_line(ts, r'^cd "\$TREE"')
        ok5 = blob_id(pe)[:12] == '14c5eee2dfc5' and blob_id(h)[:12] == '7e40960da9aa' and blob_id(pt)[:12] == 'ebfa7933d1ab' and blob_id(ts)[:12] == 'c06e085c439e'
        t.check('E5', ok5, 'RE-DERIVED blob ids: env.example minus the WHY line (line %d) = %s (payload 14c5eee2dfc5) | env.example = %s (as-committed 7e40960da9aa) | test minus the cd line (line %d) = %s (payload ebfa7933d1ab) | test = %s (c06e085c439e) | CONTROL one byte added = %s' % (
            l1, blob_id(pe)[:12], blob_id(h)[:12], l2, blob_id(pt)[:12], blob_id(ts)[:12], blob_id(h + ' ')[:12]))
    except SystemExit as e:
        t.check('E5', False, str(e))
    sib = show(repo, head, P['siblings'][0])
    gen = re.search(r"GENERATED='([^']*)'", sib); gen_rx = re.compile(gen.group(1)) if gen else None
    leg_b, leg_h = var_names(show(repo, base, 'Blockchain/Dev/.env.example')), var_names(show(repo, head, 'Blockchain/Dev/.env.example'))
    def probe(env_txt, leg):
        co = [v for v in var_names(env_txt) if v not in leg and not (gen_rx and gen_rx.match(v))]
        return co[0] if co else None
    pb, ph = probe(b, leg_b), probe(h, leg_h)
    t.check('E6', gen_rx is not None and pb == 'API_GATEWAY_PORT' and ph == 'AUTH0_CLIENT_ID',
            'bootstrap_env_canonical_template selection rule (alphabetically first variable in env.example and not in .env.example, minus the GENERATED set; computed here with a byte sort, the suite uses the caller\'s locale): base -> %s, head -> %s (the READY says API_GATEWAY_PORT -> AUTH0_CLIENT_ID); counts unchanged is a RUN fact (c3 shells)' % (pb, ph))
    msg = git(repo, 'log', '-1', '--format=%B', head); frag_every = 0
    for d in P['doc_paths']:
        bd, hd = show(repo, base, d), show(repo, head, d); a_, _ = added_removed(bd, hd); frag_every += sum(len(re.findall(r"every\s+clone", l, re.I)) for l in a_)
    t.info('E7', 'wording census: "every clone" in the PUSHED commit message: %d, in the ADDED lines of the two doc blocks: %d (the READY / body: an overstatement, bootstrap-env.sh copies only when .env is missing; disclosed in the body, the pushed text unchanged)' % (len(re.findall(r'every\s+clone', msg, re.I)), frag_every))
    users = git(repo, 'grep', '-l', 'env.example', head, '--', 'Blockchain/Dev/scripts/__tests__', 'systemTest/__tests__', check=False)[1].split('\n')
    users = sorted(x.split(':', 1)[1] for x in users if x.strip())
    no_cd = []
    for x in users:
        txt = show(repo, head, x)
        if 'bootstrap-env.sh' in txt and not any(re.match(r'\s*cd "\$', l) and 'TREE' in l or re.match(r'\s*cd "\$[A-Z_]*(ROOT|BOTH|DIR)', l) for l in txt.split('\n')): no_cd.append(x.split('/')[-1])
    t.info('E8', 'suites that name env.example (git grep): %s | of them, calling bootstrap-env.sh with no `cd "$TREE"`-style line: %s (the READY: bootstrap_env_canonical_template and bootstrap_env_slot_ports share the exposure; REPORT ONLY, a heuristic: the c3 hooks command measures)' % (users, no_cd))
    t.check('E8b', sorted(x.split('/')[-1] for x in users) == sorted(x.split('/')[-1] for x in P['siblings'] + [s]), 'the roster of suites that name the template == the kit roster (4 siblings + the new suite): %s' % (sorted(x.split('/')[-1] for x in users) == sorted(x.split('/')[-1] for x in P['siblings'] + [s])))
    foreign_in_added(repo, head, base, 'KS-1417', t)
    docs(repo, head, base, t, P)
    return t.end()


# ---------------------------------------------------------------- #1448
def ts_parts(src):
    m = re.search(r"rotate: z\.boolean\(\)\.optional\(\)\.default\(false\)\.openapi\(\{\s*description:\s*(.*?)\s*,?\s*\}\)", src, re.S)
    return re.findall(r"'((?:[^'\\]|\\.)*)'", m.group(1)) if m else []


def ts_description(src):
    m = re.search(r"rotate: z\.boolean\(\)\.optional\(\)\.default\(false\)\.openapi\(\{\s*description:\s*(.*?)\s*,?\s*\}\)", src, re.S)
    if not m: return None
    parts = re.findall(r"'((?:[^'\\]|\\.)*)'", m.group(1))
    return ''.join(parts) if parts else None


def yaml_block(text):
    i = text.find('\n    ApiKeyCreateRequest:\n')
    if i < 0: return ''
    rest = text[i + 1:]; nx = re.search(r'\n {4}[A-Za-z0-9_]+:\n', rest[1:])
    return rest if not nx else rest[:nx.start() + 2]


def yaml_props(block):
    props = block.split('\n      required:')[0]
    return re.findall(r'(?m)^ {8}([A-Za-z0-9_]+):$', props)


def yaml_rotate_desc(block):
    m = re.search(r'(?m)^ {8}rotate:\n(?: {10}.*\n)+', block)
    if not m: return None
    d = re.search(r'description: "(.*?)"\s*$', m.group(0), re.S | re.M)
    return ' '.join(x.strip() for x in d.group(1).split('\n')) if d else None


def grace_bucket(raw):
    """what index.ts :248-249 does with API_KEY_ROTATION_GRACE_SECONDS, evaluated by node (pure expression)."""
    js = "const f=(raw)=>{const g=Number.parseInt(raw ?? '0',10);return Number.isFinite(g)&&g>0?g:0};console.log(JSON.stringify(process.argv.slice(1).map(a=>[a,f(a==='<unset>'?undefined:a)])))"
    p = subprocess.run(['node', '-e', js] + list(raw), capture_output=True, text=True, timeout=60)
    if p.returncode: raise SystemExit('grace_bucket: node rc %d %s' % (p.returncode, p.stderr[:160]))
    return json.loads(p.stdout)


def run1448(repo, head, base):
    t = Tally(); P = PR(1448); src = P['spec_source']; ym = P['spec_yaml']; rt = P['runtime_source']
    b, h = show(repo, base, src), show(repo, head, src)
    if not b or not h: print('REFUSED: security.openapi.ts absent at base or head'); return 2
    cb, ch = code_only(b), code_only(h)
    add, rem = added_removed(cb, ch); raw_a, raw_r = added_removed(b, h)
    t.check('S0', not rem and len(add) >= 4 and add[0].startswith('rotate: z.boolean().optional().default(false).openapi({') and len(raw_a) == 13 and len(raw_r) == 0,
            'CODE-ONLY diff of security.openapi.ts base %s -> head %s: added %d removed %d | RAW added %d removed %d (numstat %s: the 6 comment lines are WHY) | first added %r | the added code is ONLY the rotate property (%d lines)' % (
                blob(repo, base, src)[-12:], blob(repo, head, src)[-12:], len(add), len(rem), len(raw_a), len(raw_r), P['numstat'][src], add[0][:70] if add else None, len(add)))
    yb, yh = show(repo, base, ym), show(repo, head, ym)
    ops = [o for o in difflib.SequenceMatcher(None, yb.split('\n'), yh.split('\n'), autojunk=False).get_opcodes() if o[0] != 'equal']
    blk_b, blk_h = yaml_block(yb), yaml_block(yh); pb, ph = yaml_props(blk_b), yaml_props(blk_h)
    start_h = yh.find('\n    ApiKeyCreateRequest:\n'); line_blk = yh[:start_h + 1].count('\n') + 1 if start_h >= 0 else -1
    hunk = '@@ -%d,0 +%d,%d @@' % (ops[0][1], ops[0][3] + 1, ops[0][4] - ops[0][3]) if len(ops) == 1 and ops[0][0] == 'insert' else None
    t.check('S1', len(ops) == 1 and ops[0][0] == 'insert' and ops[0][4] - ops[0][3] == 10 and hunk == '@@ -8848,0 +8849,10 @@' and pb + ['rotate'] == ph[:len(pb)] + ['rotate'] and sorted(ph) == sorted(pb + ['rotate']) and '      required:\n        - name\n' in blk_h,
            'yaml: %s (the PR body: @@ -8848,0 +8849,10 @@, 10 insertions, 0 removals) | ApiKeyCreateRequest block starts at head line %d; properties base %s -> head %s | `required` still [name]: %s' % (
                hunk, line_blk, pb, ph, '      required:\n        - name\n' in blk_h))
    dts, dy = ts_description(h), yaml_rotate_desc(blk_h)
    t.check('S2', bool(dts) and dts == dy, 'DESCRIPTION EQUALITY: the security.openapi.ts description (the %d string literals joined) == the yaml description (folded lines joined) : %s | lengths %s / %s | CONTROL one character changed reads unequal: %s' % (
        len(ts_parts(h)), dts == dy, len(dts or ''), len(dy or ''), (dts or '') + 'x' != (dy or '')))
    rq = 'Blockchain/Dev/services/security/src/requestSchemas.ts'
    t.check('S3', blob(repo, base, rt) == blob(repo, head, rt) != '' and blob(repo, base, rq) == blob(repo, head, rq) != '',
            'runtime untouched: index.ts blob %s == %s ; requestSchemas.ts %s == %s (the kit builder\'s c1 P3 also pins the exact five paths)' % (blob(repo, base, rt)[-12:], blob(repo, head, rt)[-12:], blob(repo, base, rq)[-12:], blob(repo, head, rq)[-12:]))
    # ---- S4 the WORDING TRACE: every clause -> a measured line of index.ts at the head
    ix = show(repo, head, rt); ic = code_only(ix); L = ic.split('\n')
    def ln(rx, flags=0): return [i + 1 for i, l in enumerate(L) if re.search(rx, l, flags)]
    w = {}
    w['W1 optional boolean, default false'] = ln(r"rotate: z\.boolean\(\)\.optional\(\)\.default\(false\)")
    w['W2 needs rotate AND connectorId'] = ln(r"if \(data\.rotate && data\.connectorId\)")
    mint, rev = ic.find('await dbSaveApiKey(apiKey, { rethrow: true })'), ic.find('priorKeysRevoked = await revokePriorConnectorKeys(data.connectorId, tenantId, apiKey.id)')
    w['W3 minted before retired'] = [ic[:mint].count('\n') + 1, ic[:rev].count('\n') + 1] if 0 <= mint < rev else []
    w['W4 the other active keys, same connector + tenant (SQL)'] = ln(r"WHERE connector_id = \$1 AND tenant_id = \$2::uuid AND id <> \$3 AND is_active = true")
    w['W4b the same in memory'] = ln(r"k\.id === keepKeyId \|\| k\.connectorId !== connectorId \|\| k\.tenantId !== tenantId")
    w['W5 grace parse'] = ln(r"Number\.parseInt\(process\.env\.API_KEY_ROTATION_GRACE_SECONDS \?\? '0', 10\)") + ln(r"Number\.isFinite\(graceRaw\) && graceRaw > 0 \? graceRaw : 0")
    w['W6 positive grace: expiry NOW()+grace if earlier'] = ln(r"LEAST\(COALESCE\(expires_at, 'infinity'::timestamptz\), NOW\(\) \+ \(\$4 \|\| ' seconds'\)::interval\)")
    w['W6b in memory'] = ln(r"if \(!k\.expiresAt \|\| k\.expiresAt > until\) k\.expiresAt = until")
    w['W7 priorKeysRevoked in the 201 only when both'] = ln(r"\.\.\.\(data\.rotate && data\.connectorId \? \{ priorKeysRevoked \} : \{\}\)")
    f8 = ln(r"KS-577: revoke-on-rotate FAILED"); r8 = [i for i in ln(r"^\s*return null;") if f8 and i > f8[0]][:1]
    w['W8 null = attempted and failed (the log line, then return null)'] = f8 + r8
    w['W9 the retire is called with the tenant of the minted key'] = ln(r"revokePriorConnectorKeys\(data\.connectorId, tenantId, apiKey\.id\)")
    ok4 = all(w[k] for k in w if not k.endswith('b')) and len(w['W4 the other active keys, same connector + tenant (SQL)']) == 2
    t.check('S4', ok4, 'WORDING TRACE at the head (clause -> CODE-ONLY line numbers in index.ts, MEASURED; the PR body\'s own line cites are %s): %s' % (P['claims']['trace_lines_body'][:60], json.dumps(w, sort_keys=True)))
    gb = grace_bucket(['<unset>', '0', '-5', 'abc', '', '600', '1.5', '2x'])
    desc_buckets = {'<unset>': 0, '0': 0, '600': 600}
    t.info('S5-GAP1', 'W-GAP-1 (grace): node-evaluated bucket of API_KEY_ROTATION_GRACE_SECONDS per index.ts :248-249 (value -> seconds used): %s | the description names only "unset or 0" for deactivation: negative, non-numeric and empty ALSO deactivate (0), and "1.5" / "2x" read 1 / 2 (parseInt) | the description\'s two named cases agree with the runtime: %s' % (gb, all(dict(gb)[k] == v for k, v in desc_buckets.items())))
    desc = dts or ''; sents = re.split(r'(?<=[.:])\s+', desc); idx = [i for i, x in enumerate(sents) if x.startswith('In that case')]
    prev = sents[idx[0] - 1] if idx and idx[0] > 0 else None
    t.info('S5-GAP2', 'W-GAP-2 (antecedent): the sentence "In that case the 201 response reports priorKeysRevoked..." follows %r ; the runtime reports priorKeysRevoked whenever rotate && connectorId (index.ts line(s) %s), not only for a positive grace — the gate rules whether "that case" reads as the whole rotate-with-connectorId condition or only the positive-grace sentence before it' % ((prev or '')[:150], w['W7 priorKeysRevoked in the 201 only when both']))
    resp = re.search(r'\n    ApiKeyCreateResponse:\n.*?\n    [A-Za-z0-9_]+:\n', yh, re.S); rtxt = resp.group(0) if resp else ''
    cons = git(repo, 'grep', '-n', 'priorKeysRevoked', head, '--', 'Blockchain/Dev/services', check=False)[1]
    consumers = sorted(set(x.split(':')[1] + ':' + x.split(':')[2] for x in cons.split('\n') if x.strip() and '__tests__' not in x and x.split(':')[1] != rt))
    t.info('S5-GAP3', 'W-GAP-3 (response schema): `priorKeysRevoked` occurs in the published ApiKeyCreateResponse block: %s (block %d chars; properties of data: %s) ; occurrences in the whole yaml: %d (the rotate description only) ; consumers outside index.ts and tests: %s' % (
        'priorKeysRevoked' in rtxt, len(rtxt), re.findall(r'(?m)^ {12}([a-zA-Z]+):$', rtxt), yh.count('priorKeysRevoked'), consumers))
    t.info('S5-GAP4', 'W-GAP-4 (count semantics): the DB path returns r.rowCount of the UPDATE (every matching active row, including one whose expiry does not move) — the description says only that the response "reports priorKeysRevoked": %s' % ln(r"return r\.rowCount \?\? retired"))
    env_hits = [x.split(':', 2)[1] for x in git(repo, 'grep', '-n', 'API_KEY_ROTATION_GRACE_SECONDS', head, '--', '.', ':!*.html', ':!Blockchain/Dev/docs/openapi/secuura-api.yaml', check=False)[1].split('\n') if x.strip()]
    t.info('S5-GAP4b', 'where API_KEY_ROTATION_GRACE_SECONDS is named at the head (git grep, html and the yaml excluded): %s (an integrator reads the variable in the published description; whether it is documented for an operator elsewhere is the gate\'s question)' % sorted(set(env_hits)))
    st = git(repo, 'grep', '-n', '-E', 'security/keys|rotate', head, '--', 'systemTest/schemathesis/schemathesis.toml', check=False)[1]
    cf = git(repo, 'grep', '-l', 'POST /api/security/keys', head, '--', 'systemTest/schemathesis', check=False)[1]
    t.info('S5-GAP5', 'W-GAP-5 (Schemathesis exposure, READ ONLY — never run): schemathesis.toml lines naming security/keys or rotate: %s | files naming `POST /api/security/keys` under systemTest/schemathesis: %s | the seat: UNMEASURED' % ([x.split(':', 2)[1] + ':' + x.split(':', 2)[2].strip()[:70] for x in st.split('\n') if x.strip()][:6], sorted(set(x.split(':', 1)[1] for x in cf.split('\n') if x.strip()))[:6]))
    tf = P['test_file']; ts_ = show(repo, head, tf)
    its = re.findall(r"\bit\('((?:[^'\\]|\\.)*)'", ts_); ex = re.search(r"const EXISTING = \[(.*?)\];", ts_, re.S)
    exl = sorted(re.findall(r"'([A-Za-z0-9_]+)'", ex.group(1))) if ex else []
    t.check('S6', len(its) == P['claims']['cells'] and exl == sorted(pb) and sum(1 for x in its if x.startswith('RED KS-1434')) == 4 and sum(1 for x in its if x.startswith('control KS-1434')) == 3,
            'test file %s: %d `it(` definitions (the seat claims %d): 4 RED (A1-A4) + 3 control (C1-C3) | its EXISTING list == the base yaml block\'s property names: %s (%s)' % (tf.split('/')[-1], len(its), P['claims']['cells'], exl == sorted(pb), exl))
    def importers(rev):
        out = git(repo, 'grep', '-n', 'security.openapi', rev, '--', 'Blockchain/Dev/services/security/src', check=False)[1].split('\n')
        out = [x.split(':', 1)[1] for x in out if x.strip()]; code_imp = []
        for x in out:
            f_, n_, l_ = x.split(':', 2)
            if '__tests__' in f_: continue
            if 'security.openapi' in code_only(show(repo, rev, f_)).split('\n')[int(n_) - 1]: code_imp.append(x)
        return out, code_imp
    ib, cb_ = importers(base); ih, ch_ = importers(head)
    t.check('S7', len(ib) == 4 and len(ih) == 5 and not cb_ and not ch_,
            'git grep `security.openapi` over services/security/src: BASE %d hit(s) (the body says 4: 2 tests, 2 comments — a BASE figure), HEAD %d (the 5th is the new test itself) ; CODE-ONLY importers outside tests: base %d head %d ; head hits %s' % (len(ib), len(ih), len(cb_), len(ch_), [x[:70] for x in ih]))
    docs(repo, head, base, t, P)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    a = 'x = 1;\n// c.catch(() => [])\nq`s`;\n'
    rep(code_only(a).count('catch') == 0, 'code_only: a comment mention is blanked')
    ad, rm = added_removed('a\nb\nc', 'a\nB\nc\nd'); rep(ad == ['B', 'd'] and rm == ['b'], 'added_removed: replace + insert')
    ok, _ = pure_insertion('a\nb\n', 'a\nNEW\nb\n'); rep(ok, 'pure_insertion: one inserted line passes')
    ok, _ = pure_insertion('a\nb\n', 'a\nNEW\nB\n'); rep(not ok, 'PLANTED altered base line FAILS pure_insertion')
    ok, _ = pure_insertion('a\nb\n', 'a\nN1\nb\nN2\n'); rep(not ok, 'PLANTED two separate insertions FAIL (one contiguous block only)')
    ok, _ = pure_insertion('a\nb\n', 'a\nb\n'); rep(not ok, 'PLANTED no change FAILS (nothing inserted)')
    rep(sh_code_only('a\n  # x\nb').split('\n') == ['a', '', 'b'], 'sh_code_only blanks full-line comments only')
    rep(blob_id(b'hello\n') == 'ce013625030ba8dba906f756967f9e9ca394464a', 'blob_id: the git blob id of "hello\\n" is ce013625030b (a known value)')
    rep(blob_id(b'hello\n ') != blob_id(b'hello\n'), 'blob_id: one added byte changes the id (the CONTROL of the re-derivations)')
    t_, ln_ = drop_line('a\n# KS-1456: x\nb', r'^# KS-1456:'); rep(t_ == 'a\nb' and ln_ == 2, 'drop_line removes exactly the one matching line and names it')
    try: drop_line('a\nx\nx', r'^x$'); rep(False, 'drop_line with 2 matches was ACCEPTED')
    except SystemExit: rep(True, 'ARM: drop_line with 2 matching lines -> refused')
    try: drop_line('a\nb', r'^zz$'); rep(False, 'drop_line with 0 matches was ACCEPTED')
    except SystemExit: rep(True, 'ARM: drop_line with 0 matching lines -> refused')
    ts_src = "rotate: z.boolean().optional().default(false).openapi({\n      description:\n        'When true and a ' +\n        'connectorId it\\'s ok. ' +\n        'End.',\n    }),"
    rep(ts_description(ts_src) == "When true and a connectorId it\\'s ok. End.", 'ts_description joins the string literals of the rotate property')
    rep(ts_description('nothing here') is None, 'ts_description: no rotate property reads None')
    blk = '\n    ApiKeyCreateRequest:\n      type: object\n      properties:\n        name:\n          type: string\n        rotate:\n          type: boolean\n          description: "a b\n            c d."\n      required:\n        - name\n    Next:\n      type: object\n'
    rep(yaml_props(yaml_block(blk)) == ['name', 'rotate'] and yaml_rotate_desc(yaml_block(blk)) == 'a b c d.', 'yaml_block / yaml_props / yaml_rotate_desc read a folded description and the property names')
    rep(yaml_block('no schema') == '', 'yaml_block: an absent schema reads empty')
    g = dict(grace_bucket(['<unset>', '0', '-5', 'abc', '600', '1.5']))
    rep(g['<unset>'] == 0 and g['0'] == 0 and g['-5'] == 0 and g['abc'] == 0 and g['600'] == 600 and g['1.5'] == 1, 'grace_bucket (node): unset / 0 / -5 / abc read 0; 600 reads 600; 1.5 reads 1')
    rep(test_cells('# CELL 1 x\n# CELL 2\n# CELL 3\n# CELL 4\nx # CELL 5') == 4, 'test_cells counts line-leading `# CELL n` markers only')
    try: req(['--repo', 'x', '--head', 'abc'], '--head', hex40=True); rep(False, 'short head ACCEPTED')
    except SystemExit: rep(True, 'REQUIRED-ARG ARM short --head -> refused')
    for foreign in (1441, 1443, 1446):
        try: PR(foreign); rep(False, '--pr %s ACCEPTED' % foreign)
        except SystemExit: rep(True, 'WRONG-PR ARM --pr %s (a previous gate\'s PR) -> refused' % foreign)
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
        return {'1447': run1447, '1448': run1448, '1449': run1449}[n](repo, head, base)
    except SystemExit as e:   # a wrong head / foreign PR's tree makes a helper refuse: that is a FAIL of the claims, not a crash
        print('FAIL C2-REFUSED %s' % e); return 1


if __name__ == '__main__':
    sys.exit(main())
