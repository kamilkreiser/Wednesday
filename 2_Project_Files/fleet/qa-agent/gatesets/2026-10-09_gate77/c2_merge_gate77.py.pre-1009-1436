#!/usr/bin/env python3
"""c2_merge_gate77.py — gate77's MERGEABILITY, COLLISION and LANDING-CHAIN instrument (six rows + the pending #1427). Writes ONLY into YOUR
scratch clone (objects, SIM commits; never a ref) and the --out dir; lib_gate77.wgit refuses any write verb under !CODING.

  clean   --repo <clone> --develop <40-hex>                    per row: merge-tree vs develop -> conflict set; rc 1 if any CODE path conflicts
  collide --repo <clone> --develop <40-hex>                    the cross-PR collision table (rows + pending #1427 + develop's advance);
                                                               rc 1 if two rows share a CODE path (they must then be sequenced AND re-gated)
  chain   --repo <clone> --develop <40-hex> --order a,b,..  --out <fresh dir> [--drop n,..] [--expect-final <tree>]
                                                               the sequential docs-only KEEP-BOTH landing, one SIM merge-in M + SIM squash per
                                                               step; '1427' may lead the order (the pending gate76 row). Every row must be in
                                                               --order unless named in --drop (a row that has LANDED, or is NO GO). rc 1 on any failure.
  selftest --repo <clone> --develop <40-hex> --out <fresh dir> every planted arm must FAIL; the real chain and the gate76 calibration must PASS.

THE KEEP-BOTH RULE (gate73 Q-UNION, binding): each row's doc change must be ONE pure insertion immediately before `</body>` (vs raise_base);
the composed doc = the current doc with that block inserted before its `</body>`. NEVER `git merge-file --union` (reported as an INSTRUMENT
only: it is how a closing tag gets dropped). Read-back per doc per step: the current sequence is the PREFIX, the own number/key appears ONCE
and LAST, every flow number / cheat key UNIQUE, whole-doc tag balance == the current doc's, the block alone balanced, and new-minus-block ==
current byte for byte. Code paths: develop's blob must still equal raise_base's (else RE-GATE, refused), then the head's blob is taken.
CROSS-CHECK: `git merge-tree --write-tree <cur> <head>` must conflict on docs only and agree with the composed tree on every non-doc path.
"""
import json, os, re, subprocess, sys
import lib_gate77 as L
from lib_gate77 import K, ROWS, RAISE_BASE, DOCS, git, git_bytes, wgit, opt, obj_at, mode_at, changed_paths, refuse_absent, Tally

SIM_ENV = {'GIT_AUTHOR_NAME': 'gate77 SIM', 'GIT_AUTHOR_EMAIL': 'sim@gate77.invalid', 'GIT_COMMITTER_NAME': 'gate77 SIM',
           'GIT_COMMITTER_EMAIL': 'sim@gate77.invalid', 'GIT_AUTHOR_DATE': '2026-10-09T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-09T00:00:00Z'}


def row_info(n):
    if n in ROWS:
        R = ROWS[n]; return dict(pr=n, head=R['head_expected'], own_flow=R['flow_number'], own_key=R['cheat_key'])
    for p in K['pending_before_gate']:
        if p['pr'] == n: return dict(pr=n, head=p['head'], own_flow=p['flow_number'], own_key=p['cheat_key'])
    raise SystemExit('c2: REFUSED — unknown row %r' % n)


def merge_tree(repo, a, b):
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', '--no-messages', a, b)
    lines = [l for l in o.split('\n') if l]
    return rc, (lines[0] if lines else ''), sorted(lines[1:])


def readback(path, cur, new, blk, own):
    """[] when the composed doc reads back clean, else the list of failures."""
    bad = []; b = ''.join(blk)
    try:
        cs, ns_ = L.seq_of(path, cur), L.seq_of(path, new); bs = L.seq_of(path, b)
    except ValueError as e:
        return ['reader refused: %s' % e]
    if ns_[:len(cs)] != cs: bad.append('current sequence is not the prefix')
    if ns_[len(cs):] != [own]: bad.append('new entries %s != [own %s] (own must appear once and LAST)' % (ns_[len(cs):], own))
    if bs != [own]: bad.append('the block itself carries %s, want exactly [%s]' % (bs, own))
    if len(set(ns_)) != len(ns_): bad.append('sequence NOT UNIQUE: duplicates %s' % sorted({x for x in ns_ if ns_.count(x) > 1}))
    if L.tag_balance(new) != L.tag_balance(cur): bad.append('whole-doc tag balance %s != current %s' % (L.tag_balance(new), L.tag_balance(cur)))
    if L.tag_balance(b): bad.append('the block alone is unbalanced: %s' % L.tag_balance(b))
    if new.replace(b, '', 1) != cur: bad.append('new-minus-block != current byte for byte')
    return bad


def hash_blob(repo, data):
    if not L.outside_forbidden(repo): raise SystemExit('c2: REFUSED hash-object -w inside %s' % L.FORBIDDEN)
    p = subprocess.run(['git', '-C', repo, 'hash-object', '-w', '--stdin'], input=data, capture_output=True)
    if p.returncode != 0: raise SystemExit('c2: hash-object rc %d' % p.returncode)
    return p.stdout.decode().strip()


def build_tree(repo, onto, entries, idx):
    env = dict(SIM_ENV, GIT_INDEX_FILE=idx)
    rc, _, e = wgit(repo, 'read-tree', onto, env=env)
    if rc: raise SystemExit('c2: read-tree rc %d %s' % (rc, e))
    for path, (mode, sha) in entries.items():
        if sha is None: rc, _, e = wgit(repo, 'update-index', '--force-remove', '--', path, env=env)
        else: rc, _, e = wgit(repo, 'update-index', '--add', '--cacheinfo', '%s,%s,%s' % (mode, sha, path), env=env)
        if rc: raise SystemExit('c2: update-index rc %d %s' % (rc, e))
    rc, o, e = wgit(repo, 'write-tree', env=env)
    if rc: raise SystemExit('c2: write-tree rc %d %s' % (rc, e))
    return o.strip()


def commit_tree(repo, tree, parents, msg):
    args = ['commit-tree', tree] + sum([['-p', p] for p in parents], []) + ['-m', msg]
    rc, o, e = wgit(repo, *args, env=SIM_ENV)
    if rc: raise SystemExit('c2: commit-tree rc %d %s' % (rc, e))
    return o.strip()


def ls_nondoc(repo, tree):
    return {l.split('\t', 1)[1]: l.split('\t', 1)[0] for l in git(repo, 'ls-tree', '-r', tree).split('\n') if l and l.split('\t', 1)[1] not in L.DOC_PATHS}


def step(repo, cur, n, out, i, T):
    info = row_info(n); h = info['head']; tag = '#%s step %d' % (n, i)
    paths = changed_paths(repo, RAISE_BASE, h); code = [p for p in paths if p not in L.DOC_PATHS]
    moved = [p for p in code if obj_at(repo, cur, p) != obj_at(repo, RAISE_BASE, p)]
    if moved:
        T.check('CODE-UNMOVED', False, '%s: develop-so-far moved this row\'s CODE path(s) %s since raise_base — RE-GATE, refused' % (tag, moved))
        return None
    T.check('CODE-UNMOVED', True, '%s: %d code path(s), each still == raise_base at %s' % (tag, len(code), cur[:12]))
    entries = {p: ((mode_at(repo, h, p), obj_at(repo, h, p)) if obj_at(repo, h, p) else ('', None)) for p in code}
    docs = {}
    for key, path in (('flow', DOCS['flow']), ('cheat', DOCS['cheat'])):
        base_t = git_bytes(repo, RAISE_BASE, path).decode('utf-8'); head_t = git_bytes(repo, h, path).decode('utf-8')
        cur_t = git_bytes(repo, cur, path).decode('utf-8')
        try:
            blk = L.block_of(base_t, head_t)
        except ValueError as e:
            T.check('BLOCK-' + key, False, '%s %s: %s' % (tag, key, e)); return None
        new_t = L.compose(cur_t, blk)
        bad = readback(path, cur_t, new_t, blk, info['own_flow'] if key == 'flow' else info['own_key'])
        T.check('READBACK-' + key, not bad, '%s %s: block %d lines, sequence %s -> +%s, tag balance %s%s' % (
            tag, key, len(blk), len(L.seq_of(path, cur_t)), info['own_flow'] if key == 'flow' else info['own_key'],
            L.tag_balance(new_t) or 'balanced', (' | FAIL ' + '; '.join(bad)) if bad else ''))
        # the --union INSTRUMENT (never picked): what would a union merge do to tag balance?
        fs = []
        for nm, t in (('cur', cur_t), ('base', base_t), ('head', head_t)):
            p = os.path.join(out, '_u_%s_%s' % (key, nm)); open(p, 'w', encoding='utf-8').write(t); fs.append(p)
        u = subprocess.run(['git', 'merge-file', '-p', '--union'] + fs, capture_output=True).stdout.decode('utf-8', 'replace')
        T.info('UNION-' + key, '%s %s: `merge-file --union` would give tag balance %s (keep-both gives %s) — instrument only, NEVER picked' % (
            tag, key, L.tag_balance(u) or 'balanced', L.tag_balance(new_t) or 'balanced'))
        sha = hash_blob(repo, new_t.encode('utf-8'))
        fn = os.path.join(out, '%d_%s_%s.html' % (i, n, key)); open(fn, 'wb').write(new_t.encode('utf-8'))
        entries[path] = (mode_at(repo, cur, path), sha); docs[key] = dict(blob=sha, file=fn)
    tree = build_tree(repo, cur, entries, os.path.join(out, '_idx_%d' % i))
    rc, mt, conf = merge_tree(repo, cur, h)
    agree = ls_nondoc(repo, mt) == ls_nondoc(repo, tree)
    T.check('XCHECK', set(conf) <= set(L.DOC_PATHS) and agree, '%s: merge-tree %s %s rc %d conflicted %s; non-doc paths agree with the composed tree: %s' % (
        tag, cur[:12], h[:12], rc, [p.split('/')[-1][:24] for p in conf] or 'none', agree))
    M = commit_tree(repo, tree, [h, cur], 'SIM gate77 docs-only keep-both merge-in for #%s (never pushed)' % n)
    S = commit_tree(repo, tree, [cur], 'SIM gate77 squash of #%s (never pushed)' % n)
    ours = changed_paths(repo, h, M); dev = changed_paths(repo, cur, M)
    hook = any(p.startswith('Blockchain/Dev/') for p in ours)
    print('STEP %d #%s onto %s: tree %s | SIM M %s (parents [head %s, cur %s]) | push delta OURS..M %d paths%s, DEV..M %d paths | needs merge-in: %s' % (
        i, n, cur[:12], tree, M[:12], h[:12], cur[:12], len(ours), ' (Blockchain/Dev present: FULL preflight in-hook)' if hook else '', len(dev),
        'YES (docs conflict)' if rc else 'NO'))
    return dict(pr=n, head=h, onto=cur, tree=tree, M=M, S=S, merge_in_needed=bool(rc), conflicted=conf, ours_m_paths=len(ours),
                dev_m_paths=len(dev), full_preflight_in_hook=hook, docs=docs)


def chain(repo, dev, order, out, T, expect_final=None):
    os.makedirs(out, exist_ok=True); cur = dev; steps = []
    for i, n in enumerate(order, 1):
        s = step(repo, cur, n, out, i, T)
        if s is None: print('CHAIN REFUSED at step %d (#%s)' % (i, n)); return None
        steps.append(s); cur = s['S']
    # ONE-PASS: every block onto develop's docs in order + every code blob, in ONE tree -> must equal the chain's last tree
    entries = {}
    for key, path in (('flow', DOCS['flow']), ('cheat', DOCS['cheat'])):
        t = git_bytes(repo, dev, path).decode('utf-8')
        for n in order:
            h = row_info(n)['head']
            t = L.compose(t, L.block_of(git_bytes(repo, RAISE_BASE, path).decode('utf-8'), git_bytes(repo, h, path).decode('utf-8')))
        entries[path] = (mode_at(repo, dev, path), hash_blob(repo, t.encode('utf-8')))
    for n in order:
        h = row_info(n)['head']
        for p in changed_paths(repo, RAISE_BASE, h):
            if p not in L.DOC_PATHS: entries[p] = (mode_at(repo, h, p), obj_at(repo, h, p))
    one = build_tree(repo, dev, entries, os.path.join(out, '_idx_onepass'))
    T.check('ONEPASS', one == steps[-1]['tree'], 'one-pass composition %s == chain final %s' % (one[:12], steps[-1]['tree'][:12]))
    if expect_final: T.check('EXPECT-FINAL', steps[-1]['tree'] == expect_final, 'final %s == expected %s' % (steps[-1]['tree'], expect_final))
    print('FINAL tree %s (order %s onto develop %s)' % (steps[-1]['tree'], ','.join(order), dev[:12]))
    json.dump(dict(develop=dev, order=order, steps=steps, final_tree=steps[-1]['tree']), open(os.path.join(out, 'chain.json'), 'w'), indent=1)
    return steps


def collide(repo, dev, T, extra=None):
    sets = {n: changed_paths(repo, RAISE_BASE, R['head_expected']) for n, R in ROWS.items()}
    for p in K['pending_before_gate']: sets['%s(pending)' % p['pr']] = changed_paths(repo, RAISE_BASE, p['head'])
    sets['develop-advance'] = changed_paths(repo, RAISE_BASE, dev)
    if extra: sets.update(extra)
    by = {}
    for n, ps in sets.items():
        for p in ps: by.setdefault(p, []).append(n)
    print('COLLISION TABLE (paths touched by more than one of: six rows, pending #1427, develop since raise_base):')
    shared = {p: ns for p, ns in by.items() if len(ns) > 1}
    for p, ns in sorted(shared.items()): print('  %-100s %s' % (p, ' '.join(ns)))
    rows_only = [n for n in sets if n in ROWS or (extra and n in extra)]
    for p in K['pending_before_gate']:
        code = [x for x in changed_paths(repo, RAISE_BASE, p['head']) if x not in L.DOC_PATHS]
        landed = bool(code) and all(obj_at(repo, dev, x) == obj_at(repo, p['head'], x) for x in code)
        print('  #%s (pending): %s' % (p['pr'], 'LANDED on develop %s (every code blob == its head\'s): its overlap with develop-advance is expected' % dev[:12]
                                       if landed else 'NOT landed on develop %s' % dev[:12]))
    # a CODE collision matters only when a gate77 ROW is party to it (pending-vs-develop overlap is #1427 landing, not this gate's)
    code_hits = {p: ns for p, ns in shared.items() if p not in L.DOC_PATHS and any(n in rows_only for n in ns)}
    T.check('DOCS-SHARED', all(set(rows_only) <= set(by.get(d, [])) for d in L.DOC_PATHS),
            'both platform docs are touched by EVERY row (%d rows): every row needs a docs keep-both merge-in after the first lander' % len(rows_only))
    T.check('CODE-DISJOINT', not code_hits, 'code paths shared between rows / pending / develop advance: %s' % (code_hits or 'none'))
    return code_hits


def clean(repo, dev, T):
    for n, R in ROWS.items():
        rc, t, conf = merge_tree(repo, dev, R['head_expected'])
        code = [p for p in conf if p not in L.DOC_PATHS]
        T.check('CLEAN-' + n, not code, '#%s vs develop %s: merge-tree rc %d tree %s conflicted %s -> %s' % (
            n, dev[:12], rc, t[:12], [p.split('/')[-1][:30] for p in conf] or 'none',
            'MERGES CLEANLY' if rc == 0 else ('docs-only conflict: needs a keep-both merge-in' if not code else 'CODE CONFLICT: RE-GATE')))


def selftest(repo, dev, out):
    arms = []
    def arm(name, fired): arms.append((name, fired)); print('ARM %-34s %s' % (name, 'FIRED' if fired else 'DID NOT FIRE'))
    base = '<html>\n<body>\n<h2>1. a</h2>\n<table><tr><td>x</td></tr></table>\n</body>\n</html>\n'
    blk = ['<h2>2. b</h2>\n', '<table><tr><td>y</td></tr></table>\n']
    head_ok = base.replace('</body>', ''.join(blk) + '</body>')
    try: L.block_of(base, head_ok); ok_ctl = True
    except ValueError: ok_ctl = False
    print('CONTROL block_of on a clean insertion: %s' % ('ok' if ok_ctl else 'REFUSED (instrument broken)'))
    try: L.block_of(base, head_ok.replace('<h2>1. a</h2>', '<h2>1. A</h2>')); arm('S1 not-one-insertion', False)
    except ValueError: arm('S1 not-one-insertion', True)
    try: L.block_of(base, base.replace('<html>\n', '<html>\n' + ''.join(blk))); arm('S2 insertion-not-before-body', False)
    except ValueError: arm('S2 insertion-not-before-body', True)
    F = DOCS['flow']
    dup = ['<h2>1. dup</h2>\n']
    arm('S3 duplicate-flow-number', bool(readback(F, base, L.compose(base, dup), dup, 1)))
    unb = ['<h2>2. b</h2>\n', '<table><tr><td>y</tr></table>\n']
    arm('S4 unbalanced-block (</td> dropped)', bool(readback(F, base, L.compose(base, unb), unb, 2)))
    arm('S4b CONTROL clean block reads back clean', not readback(F, base, L.compose(base, blk), blk, 2))
    # S5/S6: a SIM develop that edits #1431's stack_guard.sh -> chain must refuse (RE-GATE) and clean must report a CODE conflict
    p = 'Blockchain/Dev/scripts/stack_guard.sh'
    data = git_bytes(repo, dev, p) + b'\n# gate77 SELFTEST plant: a develop-side edit of a row code path\n'
    t = build_tree(repo, dev, {p: (mode_at(repo, dev, p), hash_blob(repo, data))}, os.path.join(out, '_idx_s5'))
    simdev = commit_tree(repo, t, [dev], 'SIM gate77 selftest develop touching stack_guard.sh (never pushed)')
    T5 = Tally(); r = chain(repo, simdev, ['1431'], os.path.join(out, 's5'), T5)
    arm('S5 chain refuses a moved code path', r is None and 'CODE-UNMOVED' in T5.fails)
    T6 = Tally(); clean(repo, simdev, T6)
    # stack_guard.sh appended at develop and changed at #1431 in a different hunk may merge cleanly; P7/CODE-UNMOVED is the binding
    # check. The clean arm uses a plant ON the line #1431 edits, so the merge must conflict:
    data2 = git_bytes(repo, dev, p).replace(b'2>/dev/null | grep -v "^${project}|" | sort -u || true', b'2>/dev/null | grep -v "^${project}|" | sort -r || true', 1)
    t2 = build_tree(repo, dev, {p: (mode_at(repo, dev, p), hash_blob(repo, data2))}, os.path.join(out, '_idx_s6'))
    simdev2 = commit_tree(repo, t2, [dev], 'SIM gate77 selftest develop editing #1431\'s own line (never pushed)')
    T6 = Tally(); clean(repo, simdev2, T6)
    arm('S6 clean reports a CODE conflict', 'CLEAN-1431' in T6.fails and data2 != git_bytes(repo, dev, p))
    T7 = Tally(); collide(repo, dev, T7, extra={'9999(planted)': [p]})
    arm('S7 collide reports a shared code path', 'CODE-DISJOINT' in T7.fails)
    # positive controls
    T8 = Tally(); r = chain(repo, dev, ['1427'], os.path.join(out, 'calib'), T8, expect_final=K['pending_before_gate'][0]['predicted_tree_on_develop_at_draft'])
    cal = r is not None and not T8.fails
    print('POSITIVE CONTROL gate76 calibration: #1427 alone onto develop %s == gate76 predicted 57c9b5eaec95: %s' % (dev[:12], cal))
    T9 = Tally(); r = chain(repo, dev, ['1427'] + K['merge_order_default'], os.path.join(out, 'real'), T9)
    real = r is not None and not T9.fails
    print('POSITIVE CONTROL real chain 1427 + default order: %s' % real)
    allf = all(f for _, f in arms) and ok_ctl
    print('SELFTEST arms fired %d/%d | block_of control %s | calibration %s | real chain %s' % (sum(f for _, f in arms), len(arms), ok_ctl, cal, real))
    return 0 if allf and cal and real else 1


def main():
    A = sys.argv; mode = A[1] if len(A) > 1 else ''; repo = opt(A, '--repo'); dev = opt(A, '--develop'); out = opt(A, '--out')
    if mode not in ('clean', 'collide', 'chain', 'selftest') or not repo or not dev or not re.fullmatch(r'[0-9a-f]{40}', dev):
        print(__doc__); return 9
    if not L.outside_forbidden(repo): print('REFUSED: --repo %s is under %s — use YOUR scratch clone' % (repo, L.FORBIDDEN)); return 16
    if out and not L.outside_forbidden(out): print('REFUSED: --out %s is under %s' % (out, L.FORBIDDEN)); return 16
    need = [('develop', dev), ('raise_base', RAISE_BASE)] + [('#' + n, R['head_expected']) for n, R in ROWS.items()] + \
           [('#%s (pending)' % p['pr'], p['head']) for p in K['pending_before_gate']]
    if refuse_absent(repo, need): return 2
    T = Tally()
    if mode == 'clean': clean(repo, dev, T)
    elif mode == 'collide': collide(repo, dev, T)
    elif mode == 'selftest':
        if not out or (os.path.exists(out) and os.listdir(out)): print('REFUSED: --out must be a FRESH (absent or empty) dir'); return 9
        os.makedirs(out, exist_ok=True); return selftest(repo, dev, out)
    else:
        order = (opt(A, '--order') or '').split(',')
        if not out or (os.path.exists(out) and os.listdir(out)): print('REFUSED: --out must be a FRESH (absent or empty) dir'); return 9
        if not order or order == [''] or len(set(order)) != len(order): print('REFUSED: --order must list distinct rows'); return 9
        drop = [d for d in (opt(A, '--drop') or '').split(',') if d]
        if any(d not in ROWS for d in drop) or set(drop) & set(order): print('REFUSED: --drop must name rows of this kit that are NOT in --order'); return 9
        want = sorted(set(ROWS) - set(drop))
        if sorted(o for o in order if o in ROWS) != want:
            print('REFUSED: --order must carry every row not named in --drop (%s); a row leaves the chain only BY NAME (--drop <n>: landed already, or NO GO)' % ','.join(want)); return 9
        if drop: print('DROPPED BY NAME: %s (landed already, or NO GO) — every later step is re-predicted without it' % ','.join(drop))
        if chain(repo, dev, order, out, T, opt(A, '--expect-final')) is None: T.end(); return 1
    return T.end()


if __name__ == '__main__':
    sys.exit(main())
