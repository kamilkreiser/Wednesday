#!/usr/bin/env python3
r"""c3_guard_gate75.py — the RED-PROOF instrument for gate75 (#1426 KS-1450: the leg-14 guard's provenance exemption).
Written new by the gate75 drafter (gate74's c3 drove a vitest suite; this kit's subject is a SHELL GUARD, so the arms are file tampers
of the guard, the baseline and planted new files, each run through the guard itself).

Usage:
  c3_guard_gate75.py leg14 --wt <REAL worktree> --expect-tree <40-hex> [--out <json>]
  c3_guard_gate75.py arms  --wt <REAL worktree of the HEAD> --expect-tree <40-hex> --quarantine <dir OUTSIDE the wt> --out <json>
                           [--only A1,A4,...]
  c3_guard_gate75.py --selftest

RULES THIS TOOL ENFORCES (each a refusal, never a warning):
  - the worktree is a REAL git work tree (the guard refuses a non-work-tree, and an ARCHIVE gives a FALSE red: gate74 §0.5);
  - HEAD^{tree} == --expect-tree (a verdict is valid only at its tree);
  - it is NOT under /Volumes/DevMASTER/!CODING (never a builder's or the shared checkout's tree);
  - `git status --porcelain --untracked-files=all` is EMPTY before every arm;
  - TAMPER LANDED: every replace asserts its anchor count == 1 before, the new form present and the old absent after; every new file
    asserts it did not exist and is NOT gitignored (an ignored plant is invisible to the guard: a false green);
  - RESTORE TO THE HEAD STATE, NEVER THE BASE: before an arm, each file it touches is saved as BYTES and asserted == its blob at HEAD
    (`git hash-object` vs `ls-tree HEAD`); after, the saved bytes are written back and the same equality re-asserted, and planted new
    files are MOVED to --quarantine (never deleted). R 16th's arms runner restored with `git checkout --`, which reverted its own fix and
    silently measured the pristine tip: this tool never runs checkout/restore/reset.
  - `git status --porcelain --untracked-files=all` is EMPTY after every arm.
  - A red is only a detection when it is the WANTED cell: every arm declares which cell(s) must FAIL and which must stay ok; a red from
    a different cell (a LOADFAIL, a broken plant) is reported as UNEXPECTED, never counted as a pass.
rc: 0 every arm == its want / 1 any arm != want / 2 refused (preconditions) / 3 a restore could not be proved (STOP; inspect by hand)."""
import hashlib, json, os, re, shutil, stat, subprocess, sys, tempfile, time

GUARD = 'systemTest/__tests__/no_hardcoded_slot_literals.test.sh'
BASELINE = 'systemTest/schemathesis/config/schemathesis-baseline.json'
FORBIDDEN = '/Volumes/DevMASTER/!CODING'
SUMMARY_RX = re.compile(r'^no_hardcoded_slot_literals: (\d+) passed, (\d+) failed\s*$', re.M)
CELL_RX = re.compile(r'^(ok|FAIL) {1,3}(.*)$', re.M)
# A cell is named by a substring of its ok/FAIL line. These are the guard's own words at dd31aa0c (read them before trusting them).
CELLS = {
    'SETSIZE': ('forbidden set',),
    'SCANNED': ('files under:', 'the scan is not reaching'),
    'SCAN': ('no unmarked slot', 'unmarked slot 2..'),
    'POS54': ('planted literals are reported', 'planted ', ),
    'NEG': ("slot 1's base", 'false positives in negative.ts'),
    'BARE': ('a marker with no reason', "bare 'slot-literal-ok:'"),
    'IGNORED': ('GITIGNORED cache', 'gitignored cache file'),
    'UNTRACKED': ('UNTRACKED (not ignored)', 'untracked source file'),
    'NOGIT': ('not a git work tree', 'non-git directory'),
    'MEMB': ('provenance exemption:', 'provenance exemption covered', 'jq is required'),
    'MEMB_CTL': ('lone provenance-shaped string in ANOTHER array', 'membership check cannot', 'could not build the planted-control'),
}
CELL_ORDER = ['SETSIZE', 'SCANNED', 'SCAN', 'POS54', 'NEG', 'BARE', 'IGNORED', 'UNTRACKED', 'NOGIT', 'MEMB', 'MEMB_CTL']

# The run ids at $generated.from_runs[5]/[6] at dd31aa0c (lines 10/11). A4v/N4v reuse a REAL member value on purpose.
REAL_ID = 'pre-merge-ks-1445-2026-10-07T14-01-26Z-slot2'
MARK = "slot-literal-ok: names the sweep's slot, not a target"

# ---- the arms: (id, what, edits, want) ----------------------------------------------------------------------------------------------
# edit kinds: ('replace', path, old, new) | ('newfile', path, text) | ('env', 'jq-shim-127') | ('env', 'jq-absent')
# want: {'rc': 0|1, 'fail': [cells that MUST fail], 'named': [substrings the output must carry], 'verdict': 'RED'|'GREEN'|'GREEN-NAMED-LIMITATION'|'GREEN-GAP'}
ARMS = [
    ('A0', 'untampered head', [], {'rc': 0, 'fail': [], 'verdict': 'GREEN'}),
    ('A1', 'slot value in a DIFFERENT KEY of the baseline ($generated.generated)',
     [('replace', BASELINE, '    "generated": "2026-08-19",\n', '    "generated": "2026-08-19-slot2",\n')],
     {'rc': 1, 'fail': ['SCAN'], 'named': ['schemathesis-baseline.json:13:'], 'verdict': 'RED'}),
    ('A2', 'from_runs id of a NON-(full|pre-merge) shape (line 10 re-prefixed nightly-)',
     [('replace', BASELINE, '      "pre-merge-ks-1445-2026-10-07T14-01-26Z-slot2",\n', '      "nightly-ks-1445-2026-10-07T14-01-26Z-slot2",\n')],
     {'rc': 1, 'fail': ['SCAN'], 'named': ['schemathesis-baseline.json:10:'], 'verdict': 'RED'}),
    ('A3', 'literal appended to an ORDINARY tracked systemTest file (scripts/run-k6.sh)',
     [('append', 'systemTest/scripts/run-k6.sh', '# gate75 arm A3: actors-slot2.json\n')],
     {'rc': 1, 'fail': ['SCAN'], 'named': ['scripts/run-k6.sh:'], 'verdict': 'RED'}),
    ('A4', 'lone provenance-shaped NOVEL id in a NEW array under $generated (caught by the membership cell ONLY)',
     [('replace', BASELINE, '    ],\n    "generated": "2026-08-19",\n',
       '    ],\n    "gate75_arm_a4_runs": [\n      "pre-merge-gate75-arm-a4-slot2"\n    ],\n    "generated": "2026-08-19",\n')],
     {'rc': 1, 'fail': ['MEMB'], 'named': ['pre-merge-gate75-arm-a4-slot2'], 'verdict': 'RED'}),
    ('A4v', 'the SAME shape but a REAL from_runs VALUE in a new array (membership is by VALUE, not by position)',
     [('replace', BASELINE, '    ],\n    "generated": "2026-08-19",\n',
       '    ],\n    "gate75_arm_a4v_runs": [\n      "%s"\n    ],\n    "generated": "2026-08-19",\n' % REAL_ID)],
     {'rc': 0, 'fail': [], 'verdict': 'GREEN-GAP'}),
    ('A5', 'bare marker (EMPTY reason) inside a quoted value at :859 (the ruled NAMED LIMITATION, KS-1451)',
     [('replace_nth', BASELINE, ' ' + MARK + '",\n', ' slot-literal-ok:",\n', 2)],
     {'rc': 0, 'fail': [], 'verdict': 'GREEN-NAMED-LIMITATION'}),
    ('A6', 'marker REMOVED from :859',
     [('replace_nth', BASELINE, ' ' + MARK + '",\n', '",\n', 2)],
     {'rc': 1, 'fail': ['SCAN'], 'named': ['schemathesis-baseline.json:859:'], 'verdict': 'RED'}),
    ('A7', 'the exemption STAGE removed from scan()',
     [('replace', GUARD, ' \\\n    | grep -vE "$PROVENANCE_LINE_RE" || true\n}', ' || true\n}')],
     {'rc': 1, 'fail': ['SCAN'], 'named': ['schemathesis-baseline.json:10:', 'schemathesis-baseline.json:11:', '(2 lines)'], 'verdict': 'RED'}),
    ('A8', 'jq broken: a PATH shim that exits 127', [('env', 'jq-shim-127')],
     {'rc': 1, 'fail': ['MEMB', 'MEMB_CTL'], 'verdict': 'RED'}),
    ('A8b', 'jq ABSENT from PATH (every other PATH tool symlinked)', [('env', 'jq-absent')],
     {'rc': 1, 'fail': ['MEMB'], 'named': ['jq is required'], 'verdict': 'RED'}),
    ('N1', 'slot literal in a NEW harness file the guard has never seen (untracked, not ignored)',
     [('newfile', 'systemTest/playwright/tests/gate75-arm-n1-planted.spec.ts', "export const actors = 'actors-slot3.json';\n")],
     {'rc': 1, 'fail': ['SCAN'], 'named': ['gate75-arm-n1-planted.spec.ts:1:'], 'verdict': 'RED'}),
    ('N2', 'lone provenance-shaped NOVEL id in a new array INSIDE AN ACCEPTED ENTRY (not $generated), slot 3',
     [('replace', BASELINE, '      "ticket": "KS-1448",\n',
       '      "gate75_arm_n2_runs": [\n        "full-gate75-arm-n2-slot3"\n      ],\n      "ticket": "KS-1448",\n')],
     {'rc': 1, 'fail': ['MEMB'], 'named': ['full-gate75-arm-n2-slot3'], 'verdict': 'RED'}),
    ('N3', 'slot literal in ANOTHER key of the baseline (an entry\'s "ticket")',
     [('replace', BASELINE, '      "ticket": "KS-1448",\n', '      "ticket": "KS-1448-slot4",\n')],
     {'rc': 1, 'fail': ['SCAN'], 'named': ['"ticket": "KS-1448-slot4"'], 'verdict': 'RED'}),
    ('N4', 'a NEW file at another root whose path ENDS in /schemathesis/config/schemathesis-baseline.json, NOVEL id',
     [('newfile', 'systemTest/fixtures/schemathesis/config/schemathesis-baseline.json', '{\n  "x": [\n    "pre-merge-gate75-arm-n4-slot2"\n  ]\n}\n')],
     {'rc': 1, 'fail': ['MEMB'], 'named': ['fixtures/schemathesis/config/schemathesis-baseline.json'], 'verdict': 'RED'}),
    ('N4v', 'the same suffix-path NEW file holding a REAL from_runs VALUE (the line filter is a PATH SUFFIX, not one file)',
     [('newfile', 'systemTest/fixtures/schemathesis/config/schemathesis-baseline.json', '{\n  "x": [\n    "%s"\n  ]\n}\n' % REAL_ID)],
     {'rc': 0, 'fail': [], 'verdict': 'GREEN-GAP'}),
]


def opt(A, k, d=None):
    return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d


def g(wt, *a, inp=None):
    p = subprocess.run(['git', '-C', wt] + list(a), capture_output=True, input=inp)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def under_forbidden(p):
    for q in (os.path.abspath(p), os.path.realpath(p)):
        if q == FORBIDDEN or q.startswith(FORBIDDEN + '/'): return True
    return False


def blob_at_head(wt, path):
    rc, o, _ = g(wt, 'ls-tree', 'HEAD', '--', path)
    f = o.split()
    return f[2] if rc == 0 and len(f) >= 3 else ''


def hash_obj(wt, path):
    rc, o, e = g(wt, 'hash-object', '--', path)
    return o.strip() if rc == 0 else 'ERR:' + e.strip()[:80]


def porcelain(wt):
    return g(wt, 'status', '--porcelain', '--untracked-files=all')[1]


def parse(out):
    """ONE parser for every tree and every arm: the summary line and each cell's ok/FAIL."""
    m = SUMMARY_RX.findall(out)
    cells, unknown = {}, []
    for st, msg in CELL_RX.findall(out):
        hit = [c for c in CELL_ORDER if any(s in msg for s in CELLS[c])]
        # MEMB_CTL's ok line also contains 'provenance' words; resolve the two KS-1450 cells by their most specific needle first.
        if 'MEMB_CTL' in hit and 'MEMB' in hit: hit = ['MEMB_CTL']
        if 'POS54' in hit and len(hit) > 1: hit = ['POS54']
        if len(hit) != 1: unknown.append('%s %s' % (st, msg[:80])); continue
        if hit[0] in cells: unknown.append('DUPLICATE %s' % hit[0])
        cells[hit[0]] = st
    return {'summary': [list(map(int, x)) for x in m], 'cells': cells, 'unknown': unknown,
            'passed': int(m[-1][0]) if m else None, 'failed': int(m[-1][1]) if m else None}


def run_guard(wt, env=None):
    t0 = time.time()
    e = dict(os.environ); e.update(env or {})
    p = subprocess.run(['bash', os.path.join(wt, GUARD)], capture_output=True, env=e, cwd=wt)
    out, err = p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')
    return p.returncode, out, err, round(time.time() - t0, 1)


def preconditions(wt, tree):
    why = []
    if under_forbidden(wt): why.append('the worktree %s is under %s (use YOUR OWN scratch clone)' % (wt, FORBIDDEN))
    rc, o, _ = g(wt, 'rev-parse', '--is-inside-work-tree')
    if rc != 0 or o.strip() != 'true': why.append('%s is NOT a git work tree (an archive gives a FALSE red)' % wt)
    rc, o, _ = g(wt, 'rev-parse', 'HEAD^{tree}')
    if o.strip() != tree: why.append('HEAD^{tree} %s != --expect-tree %s' % (o.strip()[:12], tree[:12]))
    if porcelain(wt): why.append('the worktree is NOT clean before the run: %r' % porcelain(wt)[:200])
    if not os.path.isfile(os.path.join(wt, GUARD)): why.append('the guard %s is absent' % GUARD)
    return why


def mk_env(kind, scratch):
    d = tempfile.mkdtemp(prefix='g75_%s_' % kind, dir=scratch)
    if kind == 'jq-shim-127':
        p = os.path.join(d, 'jq'); open(p, 'w').write('#!/bin/sh\nexit 127\n'); os.chmod(p, 0o755)
        return {'PATH': d + ':' + os.environ['PATH']}, d, 'shim %s/jq exits 127; `command -v jq` -> %s' % (d, p)
    if kind == 'jq-absent':
        n = 0
        for pd in os.environ['PATH'].split(':'):
            if not os.path.isdir(pd): continue
            for name in os.listdir(pd):
                src = os.path.join(pd, name)
                if name == 'jq' or os.path.exists(os.path.join(d, name)): continue
                if os.path.isfile(src) and os.access(src, os.X_OK): os.symlink(src, os.path.join(d, name)); n += 1
        probe = subprocess.run(['/bin/sh', '-c', 'command -v jq; echo rc=$?'], capture_output=True, env={'PATH': d}).stdout.decode()
        ctl = subprocess.run(['/bin/sh', '-c', 'command -v grep; echo rc=$?'], capture_output=True, env={'PATH': d}).stdout.decode()
        return {'PATH': d}, d, '%d tools symlinked into %s, jq excluded: `command -v jq` -> %r | CONTROL `command -v grep` -> %r' % (
            n, d, probe.strip(), ctl.strip())
    raise SystemExit('unknown env kind %s' % kind)


def arm(wt, aid, what, edits, want, qdir, scratch):
    rec = {'id': aid, 'what': what, 'want': want, 'landed': [], 'restored': [], 'notes': []}
    if porcelain(wt): rec['error'] = 'worktree not clean before the arm'; return rec, 2
    saved, planted, env = {}, [], None
    try:
        for ed in edits:
            k = ed[0]
            if k in ('replace', 'replace_nth', 'append'):
                path = ed[1]; full = os.path.join(wt, path)
                if path not in saved:
                    b = open(full, 'rb').read(); h = blob_at_head(wt, path); ho = hash_obj(wt, path)
                    if not h or ho != h: rec['error'] = 'PRE: %s on disk %s != HEAD blob %s' % (path, ho[:12], h[:12]); return rec, 2
                    saved[path] = b
                txt = open(full, encoding='utf-8').read()
                if k == 'append':
                    new = txt + ed[2]; ok = new.endswith(ed[2]) and new.count(ed[2]) == 1
                    rec['landed'].append('%s: appended %r; present once %s' % (path, ed[2].strip(), ok))
                elif k == 'replace':
                    old, nw = ed[2], ed[3]; c = txt.count(old)
                    if c != 1: rec['error'] = 'ANCHOR %s count %d (want 1)' % (path, c); return rec, 2
                    new = txt.replace(old, nw, 1); ok = nw in new and (old not in new or old in nw)
                    rec['landed'].append('%s: anchor count 1; new form present %s; old absent %s' % (path, nw in new, old not in new))
                else:
                    old, nw, nth = ed[2], ed[3], ed[4]; idx = [m.start() for m in re.finditer(re.escape(old), txt)]
                    if len(idx) < nth: rec['error'] = 'ANCHOR %s occurrences %d < nth %d' % (path, len(idx), nth); return rec, 2
                    s = idx[nth - 1]; new = txt[:s] + nw + txt[s + len(old):]
                    ln = txt.count('\n', 0, s) + 1; ok = new.count(old) == len(idx) - 1
                    rec['landed'].append('%s: occurrence %d of %d (line %d) replaced; remaining %d (want %d)' % (
                        path, nth, len(idx), ln, new.count(old), len(idx) - 1))
                    rec['line'] = ln
                if not ok: rec['error'] = 'TAMPER DID NOT LAND in %s' % path; open(full, 'w', encoding='utf-8').write(txt); return rec, 2
                open(full, 'w', encoding='utf-8').write(new)
            elif k == 'newfile':
                path, text = ed[1], ed[2]; full = os.path.join(wt, path)
                if os.path.exists(full): rec['error'] = 'NEWFILE %s already exists' % path; return rec, 2
                os.makedirs(os.path.dirname(full), exist_ok=True); open(full, 'w', encoding='utf-8').write(text); planted.append(path)
                ign = g(wt, 'check-ignore', '-q', '--', path)[0]
                ctl = g(wt, 'check-ignore', '-q', '--', 'systemTest/fixtures/generated/x.json')[0]
                rec['landed'].append('%s: created %d B; check-ignore rc %d (want 1 = NOT ignored) | CONTROL fixtures/generated/x.json rc %d (want 0)' % (
                    path, len(text.encode()), ign, ctl))
                if ign != 1 or ctl != 0: rec['error'] = 'the plant %s is IGNORED (or the control failed): a false green' % path
            elif k == 'env':
                env, d, note = mk_env(ed[1], scratch); rec['landed'].append(note); planted_env = d
        if 'error' in rec: raise RuntimeError(rec['error'])
        rc, out, err, secs = run_guard(wt, env)
        P = parse(out)
        rec.update({'rc': rc, 'secs': secs, 'passed': P['passed'], 'failed': P['failed'], 'cells': P['cells'], 'unknown_lines': P['unknown'],
                    'fail_lines': [l for l in out.split('\n') if l.startswith('FAIL ')],
                    'named_lines': [l.strip() for l in out.split('\n') if l.startswith('       ')][:12], 'stderr_tail': err.strip().split('\n')[-3:] if err.strip() else []})
        rec['_stdout'] = out; rec['_stderr'] = err
    except Exception as ex:  # noqa
        rec.setdefault('error', 'EXCEPTION %r' % ex)
    finally:
        for path, b in saved.items():
            open(os.path.join(wt, path), 'wb').write(b)
            h, ho = blob_at_head(wt, path), hash_obj(wt, path)
            rec['restored'].append('%s restored from SAVED BYTES: hash-object %s == HEAD blob %s: %s' % (path, ho[:12], h[:12], ho == h))
        for path in planted:
            src = os.path.join(wt, path); dst = os.path.join(qdir, aid, path); os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst); rec['restored'].append('%s MOVED to quarantine %s (never deleted)' % (path, dst))
            # an emptied planted directory chain is left in place: git does not list empty directories, so porcelain stays clean
        pc = porcelain(wt); rec['porcelain_after'] = pc
        rec['restore_ok'] = all(s.endswith('True') for s in rec['restored'] if 'hash-object' in s) and pc == ''
    if not rec['restore_ok']: return rec, 3
    if 'error' in rec: return rec, 2
    cells = rec['cells']; w = want
    want_fail = set(w.get('fail', []))
    got_fail = {c for c, s in cells.items() if s == 'FAIL'}
    missing_cells = [c for c in CELL_ORDER if c not in cells and not (c == 'MEMB_CTL' and aid == 'A8b')]
    named_ok = all(any(n in l for l in rec['_stdout'].split('\n')) for n in w.get('named', []))
    rec['got_fail_cells'] = sorted(got_fail)
    rec['missing_cells'] = missing_cells
    ok = rc == w['rc'] and got_fail == want_fail and named_ok and not rec['unknown_lines'] and not missing_cells
    if aid == 'A0': ok = ok and rec['passed'] == 11 and rec['failed'] == 0
    rec['match'] = ok
    rec['verdict_got'] = ('GREEN' if rc == 0 else 'RED') + ('' if ok else ' (!= want)')
    return rec, 0 if ok else 1


def do_arms(wt, tree, qdir, outp, only):
    why = preconditions(wt, tree)
    if under_forbidden(qdir) or os.path.realpath(qdir).startswith(os.path.realpath(wt) + '/'):
        why.append('--quarantine %s must be OUTSIDE the worktree and outside %s' % (qdir, FORBIDDEN))
    if why:
        for w in why: print('REFUSED: ' + w)
        return 2
    os.makedirs(qdir, exist_ok=True); scratch = tempfile.mkdtemp(prefix='g75_env_', dir=qdir)
    print('ARMS at %s tree %s | %s' % (wt, tree[:12], time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
    res, worst = [], 0
    for aid, what, edits, want in ARMS:
        if only and aid not in only: continue
        rec, rc = arm(wt, aid, what, edits, want, qdir, scratch)
        worst = max(worst, rc) if rc != 3 else 3
        print('%s %-4s want %-23s got rc %s %s/%s FAIL-cells %s | %s' % (
            'MATCH' if rec.get('match') else ('STOP ' if rc == 3 else 'DIFF '), aid, want['verdict'], rec.get('rc'), rec.get('passed'),
            rec.get('failed'), rec.get('got_fail_cells'), what))
        for s in rec['landed']: print('      landed: ' + s)
        for s in rec.get('fail_lines', []): print('      ' + s[:200])
        for s in rec.get('named_lines', [])[:4]: print('        ' + s[:200])
        for s in rec['restored']: print('      restore: ' + s)
        print('      porcelain after: %r | restore_ok %s%s' % (rec.get('porcelain_after'), rec.get('restore_ok'),
                                                            (' | ERROR ' + rec['error']) if 'error' in rec else ''))
        if rec.get('unknown_lines') or rec.get('missing_cells'):
            print('      PARSER: unknown %s missing %s' % (rec.get('unknown_lines'), rec.get('missing_cells')))
        res.append(rec)
        if rc == 3: print('STOP: a restore could not be proved; inspect %s by hand before anything else' % wt); break
    if outp:
        os.makedirs(os.path.dirname(os.path.abspath(outp)), exist_ok=True)
        for r in res:
            base = os.path.splitext(outp)[0] + '.%s' % r['id']
            open(base + '.stdout', 'w').write(r.pop('_stdout', '')); open(base + '.stderr', 'w').write(r.pop('_stderr', ''))
        json.dump({'wt': wt, 'tree': tree, 'arms': res}, open(outp, 'w'), indent=1)
    n_match = sum(1 for r in res if r.get('match'))
    print('ARMS %d/%d MATCH their want | final porcelain %r' % (n_match, len(res), porcelain(wt)))
    return 0 if worst == 0 and n_match == len(res) else (3 if worst == 3 else 1)


def do_leg14(wt, tree, outp):
    why = preconditions(wt, tree)
    if why:
        for w in why: print('REFUSED: ' + w)
        return 2
    rc, out, err, secs = run_guard(wt); P = parse(out)
    print('LEG14 tree %s rc %d | %s passed / %s failed | %ss | %s' % (tree[:12], rc, P['passed'], P['failed'], secs,
                                                                   time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
    for c in CELL_ORDER: print('  %-9s %s' % (c, P['cells'].get(c, 'ABSENT')))
    for l in out.split('\n'):
        if l.startswith('       '): print('    ' + l.strip()[:200])
    if P['unknown']: print('  PARSER unknown lines: %s' % P['unknown'])
    print('  stderr lines %d; porcelain after %r' % (len(err.strip().split('\n')) if err.strip() else 0, porcelain(wt)))
    if outp:
        open(outp + '.stdout', 'w').write(out); open(outp + '.stderr', 'w').write(err)
        json.dump({'tree': tree, 'rc': rc, **P}, open(outp, 'w'), indent=1)
    return 0 if P['passed'] is not None else 1


CAPTURED_DEV = """ok   forbidden set: 45 patterns = 3 slots x (11 port families + 4 name shapes)
ok   scanned 1206 files under: fixtures __tests__ scripts run-in-slot.sh performance playwright akto schemathesis api-explorer
FAIL unmarked slot 2..4 values (8 lines) — derive them from support/slot-expect.sh, or mark 'slot-literal-ok: <reason>'
ok   CONTROL: all 54 planted literals are reported
ok   CONTROL: slot 1's base, a port above the ceiling, a longer number, 'slot1'/'unslotted' and a marked line are not reported
ok   CONTROL: a marker with no reason does not exempt the line
ok   CONTROL: a slot value in a GITIGNORED cache file is not reported
ok   CONTROL: an UNTRACKED (not ignored) file is still scanned
ok   CONTROL: a directory that is not a git work tree is REFUSED, not scanned some other way

no_hardcoded_slot_literals: 8 passed, 1 failed
"""
CAPTURED_HEAD_TAIL = """ok   provenance exemption: 2 exempted line(s), all of them $generated.from_runs members
ok   CONTROL: a lone provenance-shaped string in ANOTHER array is exempted by the line filter (3) and CAUGHT by the membership check (1)
"""


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    P = parse(CAPTURED_DEV)
    rep(P['passed'] == 8 and P['failed'] == 1, 'develop capture: 8 passed / 1 failed parsed')
    rep(P['cells'].get('SCAN') == 'FAIL' and len(P['cells']) == 9 and not P['unknown'], 'develop capture: SCAN is the ONE FAIL of 9 cells, no unknown line')
    head = CAPTURED_DEV.replace('FAIL unmarked slot 2..4 values (8 lines) — derive them from support/slot-expect.sh, or mark \'slot-literal-ok: <reason>\'',
                                'ok   no unmarked slot 2..4 value in fixtures __tests__').replace('\nno_hardcoded', CAPTURED_HEAD_TAIL + '\nno_hardcoded').replace('8 passed, 1 failed', '11 passed, 0 failed')
    P = parse(head)
    rep(P['passed'] == 11 and set(P['cells'].values()) == {'ok'} and len(P['cells']) == 11, 'head capture: 11 cells all ok, MEMB and MEMB_CTL told apart')
    P = parse(head.replace('ok   provenance exemption: 2', 'FAIL provenance exemption covered 1 line(s) that are NOT'))
    rep(P['cells'].get('MEMB') == 'FAIL' and P['cells'].get('MEMB_CTL') == 'ok', 'PLANTED membership FAIL lands on MEMB, not MEMB_CTL')
    P = parse('')
    rep(P['passed'] is None and not P['cells'], 'PLANTED empty output (a LOADFAIL): no summary, 0 cells — never a pass')
    P = parse(CAPTURED_DEV + 'ok   something nobody declared\n')
    rep(P['unknown'] == ['ok something nobody declared'] or len(P['unknown']) == 1, 'PLANTED undeclared cell line is reported UNKNOWN')
    rep(under_forbidden('/Volumes/DevMASTER/!CODING/Secuura/x') and not under_forbidden('/private/tmp/x'), 'the !CODING refusal fires on a planted path, not on scratch')
    ids = [a[0] for a in ARMS]
    rep(len(ids) == len(set(ids)) == 16, 'ARMS: 16 unique ids (A0-A8b, N1-N4v)')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A or A[0] not in ('leg14', 'arms'): print(__doc__); return 2
    wt, tree = opt(A, '--wt'), opt(A, '--expect-tree')
    if not wt or not tree or not re.fullmatch(r'[0-9a-f]{40}', tree): print('REFUSED: --wt and a FULL 40-hex --expect-tree are required'); return 2
    if A[0] == 'leg14': return do_leg14(os.path.abspath(wt), tree, opt(A, '--out'))
    q = opt(A, '--quarantine'); outp = opt(A, '--out')
    if not q or not outp: print('REFUSED: arms needs --quarantine <dir outside the wt> and --out <json>'); return 2
    only = set((opt(A, '--only') or '').split(',')) - {''}
    return do_arms(os.path.abspath(wt), tree, os.path.abspath(q), outp, only)


if __name__ == '__main__':
    sys.exit(main())
