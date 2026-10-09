#!/usr/bin/env python3
"""c3_cells_gate81.py — the RUN instruments for gate81: the vitest cells / whole suites / tsc / probes / tamper rows for #1443, #1445, #1446 (in YOUR
worktree), #1444's relink guard (suite arms, a 32-probe WIDEN matrix, tamper rows, siblings), and the COMPOSITION of all four (audit-export.ts in both
orders in a temp index with the tree recorded; the two platform-k HTML docs in several orders with html_docs_matrix on each composed tree). Every write
path is checked lexically AND by realpath and refused under !CODING. Carried in shape from c3_cells_gate80.py; [g81] rebuilt.

  setup     --clone CL --head H --wt WT [--log DIR]          `git worktree add --detach` in YOUR clone; in WT/Blockchain/Dev `npm ci --ignore-scripts`
            and `npm run build --workspace=packages/shared` (dist/index.js ASSERTED). Refuses a WT that exists. (X1)
  cells     --pkg api-gateway|transfer --route R --tests T [--whole] --wt WT --clone CL --base B --head1443 H --head1446 H --head1445 H --out DIR
            materialises a STATE in WT: ROUTE files (api-gateway: base | 1443 | 1446 | composedAB | composedBA; transfer: base | 1445) and TEST files
            (none | 1443 | 1446 | both | 1445), each plant ASSERTED LANDED (sha); runs vitest ONCE (the new test files, or --whole the package), reads the
            per-cell JSON, RESTORES every touched path by sha (an originally-absent path is MOVED to the out dir's quarantine, never deleted).
            PREDICTIONS (the seats' figures, never evidence): see PRED. A suite that fails to LOAD is load_failed, never a count.
  tsc       --pkg P --route R --wt WT ...                    `tsc --noEmit -p services/<pkg>/tsconfig.json` rc in that STATE (the program EXCLUDES src/__tests__).
  probe     --pkg api-gateway|transfer --block 1443|1446|1445 --route R ...   appends a probe block to a COPY of that PR's own test file in WT, runs
            it with G81_PROBE_OUT, MOVES the copy out (quarantine), asserts the plants restored. FACTS, never a verdict.
  tamper    --pr 1443|1445|1446 --wt WT ... --out DIR [--only T1,T2]   HEAD row (all green), CONTROL no-op row, then the tamper rows of that PR: anchor
            EXACTLY ONCE, LANDED, run the PR's test file, read which cells RED, RESTORE (sha). LOAD failure = TAMPER-INVALID. ALL-GREEN = a tamper no cell catches.
  suite1444 --wt44 WT --clone CL --head H --base B --out DIR  #1444 in a worktree (no installs): the suite with (head script) / (BASE script planted) /
            (head script minus the ruled deviation guard) = the seat's 112/0, 108/4, 111/1; siblings at base and head; html_docs_matrix; `run-shell-suites.sh --list`.
  widen1444 --clone CL --head H --base B --scratch S --out DIR   32 probe Dockerfiles (+ extras) through the BASE guard and the HEAD guard, `bash <guard> <dir>`
            as the suite does: CONTROL / NEWLY-ACCEPTED / STILL-REFUSED / NEWLY-REFUSED / UNEXPECTED vs the kit's own expectation; names the `../node_modules` row.
  tamper1444 --wt44 WT --clone CL --head H --out DIR         T1 regex prefix reverted, T2 USER drop reverted, T3 deviation guard removed, T4 prefix over-widened.
  compose   --clone CL --base B --head1443 H --head1444 H --head1445 H --head1446 H --scratch S --out DIR   audit-export.ts in BOTH orders (merge-file,
            clean/conflict, the composed blob equal in both orders), a TEMP INDEX tree per order A / B / C (full tree and the code-only tree, recorded), `git
            merge-tree --write-tree` per pair (clone only), the survival of #1443's fail500 line and #1446's catch in the composed file.
  docs      (same args)  the two docs in orders A B C: textual merge-file (conflict at the same base line is the expected finding), KEEP-BOTH in each order, each
            fragment present once, flow numbers, `html_docs_matrix` on every composed tree (+ base and single-PR trees + a drops-a-block CONTROL).
  --selftest
rc 0 / 1 (a FAIL: plant not landed, restore failed, HEAD row not green, CONTROL red, a LOAD failure where a count was expected, a probe class UNEXPECTED,
a composition that does not compose) / 2 refused. NOT RUN is reported by name and is never a pass."""
import difflib, hashlib, json, os, re, shutil, signal, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate81 import K, PR, git, git_bytes, blob, req, opt, wgit, must_be_outside, extract, resolvable

HERE = os.path.dirname(os.path.abspath(__file__))
P43, P44, P45, P46 = PR(1443), PR(1444), PR(1445), PR(1446)
DD = K['dev_dir']; AG = 'Blockchain/Dev/services/api-gateway/'; TR = 'Blockchain/Dev/services/transfer/'
DOCS = list(K['known_develop_overlap']); AUDIT = list(K['known_code_overlap'])[0]
AG_ROUTES = P43['route_files']                                   # notifications, batch, audit-export
AG_TESTS = {'1443': P43['test_file'], '1446': P46['test_file']}
TR_ROUTE = P45['route_files'][0]; TR_TEST = P45['test_file']
PRED = {
    ('api-gateway', 'base', '1443'): '9 failed / 6 passed of 15 (G1 G2 G3 x3 routes red; GC1 GC2 green)',
    ('api-gateway', '1443', '1443'): '15/15 green', ('api-gateway', 'base', '1446'): '6 failed / 3 passed of 9 (X1 x3, X2, X3, X4 red; XC1-XC3 green)',
    ('api-gateway', '1446', '1446'): '9/9 green', ('transfer', 'base', '1445'): '4 failed / 2 passed of 6 (T1 x3, T2 red; TC1 TC2 green)',
    ('transfer', '1445', '1445'): '6/6 green', ('api-gateway', 'composedAB', 'both'): '24/24 green (15 + 9)', ('api-gateway', 'composedBA', 'both'): '24/24 green (15 + 9)',
    ('api-gateway', '1443', '1446'): 'PREDICTION (kit builder): #1446 cells against #1443\'s routes only: audit-export.ts at 1443 has NO 502 fix -> X1 x3, X2, X3, X4 red',
}
WHOLE_PRED = {('api-gateway', 'base'): '94 files / 845 tests (#1446 body: measured)', ('api-gateway', '1443'): '95 / 860 (#1443 body: measured)', ('api-gateway', '1446'): '95 / 854 (#1446 body: measured)',
              ('api-gateway', 'composedAB'): '96 / 869 (kit builder: 845 + 15 + 9)', ('transfer', 'base'): '79 tests (#1445 body)', ('transfer', '1445'): '85 tests (#1445 body)'}


def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def w(path, data):
    must_be_outside(path, 'write'); os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(data if isinstance(data, bytes) else data.encode('utf-8'))


def write_checked(wt, rel, data):
    p = os.path.join(wt, rel); must_be_outside(p, 'write'); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(data)
    if sha(open(p, 'rb').read()) != sha(data): raise SystemExit('PLANT NOT LANDED: %s' % rel)
    return p


def run(cmd, cwd=None, env=None, timeout=900, stdin=None):
    """-> (rc, out, err, timed_out). The child runs in its OWN process group; a timeout kills the group."""
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    p = subprocess.Popen(cmd, cwd=cwd, env=e, stdin=(subprocess.PIPE if stdin is not None else subprocess.DEVNULL), stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        o, er = p.communicate(input=(stdin.encode() if stdin is not None else None), timeout=timeout); to = False
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL); o, er = p.communicate(); to = True
    return p.returncode, o.decode('utf-8', 'replace'), er.decode('utf-8', 'replace'), to


def cgit(clone, args, env=None, inp=None):
    """plumbing in the KIT CLONE only (refuses a clone under !CODING); never the shared checkout."""
    must_be_outside(clone, 'git %s' % args[0])
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    p = subprocess.run(['git', '-C', clone] + list(args), capture_output=True, env=e, input=inp)
    return p.returncode, p.stdout, p.stderr.decode('utf-8', 'replace')


# ---------------- vitest ----------------
def cell_key(title, seen):
    k = title.split(': ', 1)[0].replace("'", '')[:70]   # vitest renders a `$label` placeholder QUOTED: the quotes are not part of the cell's name
    n = seen.get(k, 0); seen[k] = n + 1
    return k if n == 0 else '%s #%d' % (k, n + 1)


def read_vitest(json_path):
    if not os.path.isfile(json_path): return {'load_failed': True, 'tests': 0, 'passed': 0, 'failed': 0, 'skipped': 0, 'suites': 0, 'failed_suites': 0, 'cells': {}, 'message': 'NO JSON WRITTEN', 'fail_msgs': {}, 'load_failed_suites': []}
    d = json.load(open(json_path)); tr = d.get('testResults') or []
    ar = [(r, a) for r in tr for a in r.get('assertionResults') or []]
    lf = [r.get('name', '?') for r in tr if 'Test suite failed to run' in (r.get('message') or '') or (not r.get('assertionResults') and r.get('status') == 'failed')]
    seen = {}; cells = {}; msgs = {}
    for r, a in ar:
        k = cell_key(a['title'], seen); cells[k] = a['status']
        if a['status'] == 'failed': msgs[k] = ' '.join((a.get('failureMessages') or [''])[0].split())[:260]
    return {'load_failed': bool(lf) or not ar, 'load_failed_suites': lf, 'tests': len(ar), 'passed': sum(1 for _, a in ar if a['status'] == 'passed'),
            'failed': sum(1 for _, a in ar if a['status'] == 'failed'), 'skipped': sum(1 for _, a in ar if a['status'] in ('pending', 'todo', 'skipped')),
            'suites': len(tr), 'failed_suites': sum(1 for r in tr if r.get('status') == 'failed'), 'cells': cells, 'fail_msgs': msgs,
            'message': ' | '.join((r.get('message') or '')[:200] for r in tr if r.get('message'))}


def vitest(wt, pkg, rels, json_path, env_extra=None, timeout=1500):
    pd = os.path.join(wt, 'Blockchain/Dev/services', pkg); vt = os.path.join(wt, DD, 'node_modules', 'vitest', 'vitest.mjs')
    cmd = ['node', vt, 'run', '--reporter=json', '--outputFile=' + json_path] + [os.path.relpath(os.path.join(wt, r), pd) for r in rels]
    return run(cmd, cwd=pd, env=env_extra, timeout=timeout)


def porcelain(wt):
    return subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=all', '--', '.', ':!Blockchain/Dev/**/node_modules', ':!Blockchain/Dev/packages/shared/dist'],
                          capture_output=True, text=True).stdout.strip()


def apply_edits(src, edits):
    """returns the tampered text; refuses unless each anchor occurs EXACTLY ONCE in the (progressively edited) file."""
    out = src
    for a, b in edits:
        n = out.count(a)
        if n != 1: raise SystemExit('ANCHOR %r occurs %d time(s) (want 1) — the tamper is NOT applied' % (a[:70], n))
        out = out.replace(a, b)
    return out


def landed(before, after, edits):
    return sha(before.encode()) != sha(after.encode()) and all(b in after for _, b in edits if b)


# ---------------- setup ----------------
def setup(clone, head, wt, logd):
    must_be_outside(wt, 'worktree'); must_be_outside(clone, 'clone')
    if os.path.exists(wt): print('REFUSED: %s exists (a fresh worktree each time)' % wt); return 2
    logd = logd or os.path.dirname(wt.rstrip('/')); os.makedirs(logd, exist_ok=True)
    rc, o, e = wgit(clone, 'worktree', 'add', '--detach', wt, head)
    print('%s worktree add rc %d %s' % (now(), rc, e.strip()[-120:]))
    if rc: return 1
    dev = os.path.join(wt, DD)
    for name, cmd in (('ci', ['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund']), ('build_shared', ['npm', 'run', 'build', '--workspace=packages/shared'])):
        rc, o, e, to = run(cmd, cwd=dev, timeout=1500)
        w(os.path.join(logd, 'setup_%s.out' % name), o); w(os.path.join(logd, 'setup_%s.err' % name), e)
        print('%s %s rc %d%s (%s)' % (now(), ' '.join(cmd), rc, ' TIMEOUT' if to else '', os.path.join(logd, 'setup_%s.out' % name)))
        if rc: return 1
    ok = os.path.isfile(os.path.join(dev, 'packages', 'shared', 'dist', 'index.js'))
    print('ASSERT packages/shared/dist/index.js present: %s | porcelain after setup %r' % (ok, porcelain(wt)[:160]))
    return 0 if ok else 1


# ---------------- composition ----------------
def insertion(basetxt, headtxt):
    la, lb = basetxt.split('\n'), headtxt.split('\n')
    ops = [x for x in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if x[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'insert': raise SystemExit('not a pure insertion: %s' % ops[:3])
    _, i1, _, j1, j2 = ops[0]; return i1, lb[j1:j2]


def compose_keep_both(basetxt, frags):
    """frags: [(base_position, fragment_lines)] IN THE ORDER TO PLACE THEM, all inserted at the same base position; refuses differing positions."""
    la = basetxt.split('\n'); pos = {p for p, _ in frags}
    if len(pos) != 1: raise SystemExit('fragments insert at different base positions %s: not a keep-both at one point' % sorted(pos))
    i = pos.pop(); ins = [l for _, f in frags for l in f]
    return '\n'.join(la[:i] + ins + la[i:])


def flow_numbers(txt): return [int(x) for x in re.findall(r'<h2>(\d+)\.', txt)]


def merge_file(cur, basef, other):
    rc, o, e, to = run(['git', 'merge-file', '-p', '-L', 'ours', '-L', 'base', '-L', 'theirs', cur, basef, other], timeout=60)
    return rc, o   # rc = number of conflicts (>0), 0 clean, <0 error


def heads_of(A):
    return dict((n, req(A, '--head' + n, True)) for n in ('1443', '1444', '1445', '1446'))


def compose_audit(clone, base, heads, order, scratch):
    """audit-export.ts merged IN `order` (a list of PR numbers touching it): sequential 3-way merge-file. -> (bytes, [conflicts per step])."""
    b = git_bytes(clone, base, AUDIT); d = os.path.join(scratch, 'audit_' + ''.join(order)); basef = os.path.join(d, 'base.ts'); w(basef, b)
    cur = b; steps = []
    for n in order:
        theirs = git_bytes(clone, heads[n], AUDIT); tf = os.path.join(d, 'pr%s.ts' % n); w(tf, theirs); cf = os.path.join(d, 'cur_before_%s.ts' % n); w(cf, cur)
        rc, o = merge_file(cf, basef, tf); steps.append((n, rc))
        if rc != 0: raise SystemExit('audit-export.ts merge of #%s onto %s: %d conflict hunk(s)' % (n, '+'.join(order[:order.index(n)]) or 'base', rc))
        cur = o.encode('utf-8')
    return cur, steps


def compose_tree(clone, base, heads, order, scratch, tag):
    """a TEMP INDEX tree of the whole composition in `order`: every PR's exclusive paths from its head, audit-export.ts merged, the docs keep-both in
    `order`. -> dict(full, nodocs, audit_blob, docs_texts). Writes objects into the KIT CLONE only."""
    idx = os.path.join(scratch, 'idx_%s_%d' % (tag, int(time.time() * 1000))); env = {'GIT_INDEX_FILE': idx}
    must_be_outside(idx, 'temp index')
    rc, o, e = cgit(clone, ['read-tree', base], env=env)
    if rc: raise SystemExit('read-tree: ' + e)
    def put(path, data, mode='100644'):
        rc, o, e = cgit(clone, ['hash-object', '-w', '--stdin'], inp=data);
        if rc: raise SystemExit('hash-object: ' + e)
        bid = o.decode().strip(); rc, o, e = cgit(clone, ['update-index', '--add', '--cacheinfo', '%s,%s,%s' % (mode, bid, path)], env=env)
        if rc: raise SystemExit('update-index: ' + e)
        return bid
    audit_order = [n for n in order if AUDIT in PR(n)['numstat']]
    audit_bytes, _ = compose_audit(clone, base, heads, audit_order, scratch)
    for n in order:
        for path in PR(n)['numstat']:
            if path in DOCS or path == AUDIT: continue
            put(path, git_bytes(clone, heads[n], path), PR(n)['modes'][path])
    ab = put(AUDIT, audit_bytes)
    docs_texts = {}
    for d in DOCS:
        bt = git_bytes(clone, base, d).decode('utf-8')
        fr = [insertion(bt, git_bytes(clone, heads[n], d).decode('utf-8')) for n in order]
        docs_texts[d] = compose_keep_both(bt, fr); put(d, docs_texts[d].encode('utf-8'))
    rc, o, e = cgit(clone, ['write-tree'], env=env)
    if rc: raise SystemExit('write-tree: ' + e)
    full = o.decode().strip()
    # code-only tree: the same index with the docs reset to base
    for d in DOCS:
        bid = cgit(clone, ['rev-parse', '%s:%s' % (base, d)])[1].decode().strip(); cgit(clone, ['update-index', '--cacheinfo', '100644,%s,%s' % (bid, d)], env=env)
    rc, o, e = cgit(clone, ['write-tree'], env=env); nodocs = o.decode().strip()
    return dict(full=full, nodocs=nodocs, audit_blob=ab, audit_bytes=audit_bytes, docs=docs_texts)


def compose_cmd(clone, base, heads, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    A, B_, C_ = K['compose_orders']['A'], K['compose_orders']['B'], K['compose_orders']['C']
    print('%s COMPOSITION, audit-export.ts: #1443 edits fail500 (~:25), #1446 edits the 502 catch (~:171); base blob %s' % (now(), blob(clone, base, AUDIT)[-12:]))
    res = {}
    for lab, order in (('1443 then 1446', ['1443', '1446']), ('1446 then 1443', ['1446', '1443'])):
        try:
            b, steps = compose_audit(clone, base, heads, order, scratch); res[lab] = b
            print('  ORDER %-16s textual 3-way merge-file: CLEAN (conflict hunks per step %s) -> composed blob sha256/16 %s, %d bytes' % (lab, steps, sha(b)[:16], len(b)))
        except SystemExit as e:
            print('  ORDER %-16s %s' % (lab, e)); rc_all = 1
    if len(res) == 2:
        same = res['1443 then 1446'] == res['1446 then 1443']
        print('  the composed audit-export.ts is BYTE-IDENTICAL in both orders: %s' % same); rc_all |= 0 if same else 1
        txt = res['1443 then 1446'].decode('utf-8')
        f1443 = P43['route_files'][2]; l43 = [l for l in txt.split('\n') if 'logger.error(context' in l and 'thrown ' in l]
        l46 = [l for l in txt.split('\n') if "logger.error('Audit export could not reach the security service" in l and 'thrown ' in l]
        c502 = "message: 'Failed to reach security service'," in txt and '${err.message}' not in re.sub(r'//[^\n]*', '', txt)
        n43 = txt.split('\n').index(l43[0]) + 1 if l43 else -1; n46 = txt.split('\n').index(l46[0]) + 1 if l46 else -1
        surv = len(l43) == 1 and len(l46) == 1 and c502 and PRECEDENCE_OK(txt)
        print('  SURVIVAL in the composed file: #1443 fail500 ruled logger line at :%d (count %d, "String(err)" left in fail500: %s) | #1446 catch logger line at :%d (count %d) + the constant 502 message and no `${err.message}` code: %s | lines apart %d' % (
            n43, len(l43), 'String(err)' in re.sub(r'//[^\n]*', '', txt), n46, len(l46), c502, n46 - n43))
        print('  CONTROL: the base file reads fail500 String(err) = %s and the old template message = %s (the instrument can see the OLD text)' % (
            'String(err)' in git_bytes(clone, base, AUDIT).decode(), '${err.message}' in git_bytes(clone, base, AUDIT).decode()))
        rc_all |= 0 if surv else 1
        w(os.path.join(out, 'composed_audit-export.ts.txt'), res['1443 then 1446'])
    trees = {}
    for tag, order in (('A', A), ('B', B_), ('C', C_)):
        try:
            t = compose_tree(clone, base, heads, order, scratch, tag); trees[tag] = t
            print('  TEMP-INDEX TREE order %s (%s): FULL %s | CODE-ONLY (docs reset to base) %s | audit blob %s' % (tag, ' -> '.join('#' + n for n in order), t['full'], t['nodocs'], t['audit_blob'][:12]))
        except SystemExit as e:
            print('  TEMP-INDEX TREE order %s: %s' % (tag, e)); rc_all = 1
    if len(trees) == 3:
        same = len({t['nodocs'] for t in trees.values()}) == 1; diff_full = len({t['full'] for t in trees.values()})
        print('  CODE-ONLY tree IDENTICAL across orders A / B / C: %s (%s) | FULL trees differ only by the docs order: %d distinct of 3' % (same, trees['A']['nodocs'][:12], diff_full)); rc_all |= 0 if same else 1
    json.dump(dict((k, dict(full=v['full'], nodocs=v['nodocs'], audit_blob=v['audit_blob'])) for k, v in trees.items()), open(os.path.join(out, 'compose_trees.json'), 'w'), indent=1)
    # whole-tree pairwise merge simulation in the CLONE (merge-tree --write-tree), conflicts BY PATH
    pairs = [('1443', '1446'), ('1443', '1445'), ('1443', '1444'), ('1444', '1445'), ('1444', '1446'), ('1445', '1446')]
    for a, b in pairs:
        rc, o, e = cgit(clone, ['merge-tree', '--write-tree', '--name-only', '--merge-base=' + base, heads[a], heads[b]])
        lines = o.decode('utf-8', 'replace').strip().split('\n'); tree = lines[0] if lines else ''
        conf = [l for l in lines[1:] if l.strip() and not l.startswith('Auto-merging') and not l.startswith('CONFLICT')]
        print('  merge-tree --write-tree #%s + #%s: rc %d (1 = conflicts; anything else is an ERROR) tree %s | conflicted paths %s' % (a, b, rc, tree[:12], sorted(set(conf)) or 'none'))
        if rc not in (0, 1): rc_all = 1
    return rc_all


def PRECEDENCE_OK(txt):
    i = txt.find("logger.error('Audit export could not reach"); j = txt.find('res.status(502)', i)
    return 0 <= i < j


def docs_cmd(clone, base, heads, develop, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    orders = [(t, K['compose_orders'][t]) for t in ('A', 'B', 'C')]
    texts = {}
    for d in DOCS:
        b = git_bytes(clone, base, d).decode('utf-8'); dv = git_bytes(clone, develop, d).decode('utf-8'); nm = os.path.basename(d)
        ins = dict((n, insertion(b, git_bytes(clone, heads[n], d).decode('utf-8'))) for n in heads)
        print('%s %s: insertion position (base line) per PR %s | same position for all four: %s | develop tail flow numbers %s, next free %s' % (
            now(), nm, dict((n, v[0] + 1) for n, v in ins.items()), len({v[0] for v in ins.values()}) == 1, flow_numbers(dv)[-3:], (max(flow_numbers(dv)) + 1) if flow_numbers(dv) else 'n/a'))
        sd = os.path.join(scratch, 'docs_' + nm[:12]); os.makedirs(sd, exist_ok=True); w(os.path.join(sd, 'base.html'), b)
        for n in heads: w(os.path.join(sd, n + '.html'), git_bytes(clone, heads[n], d))
        for tag, order in orders:
            # textual merge, step by step, in this order: the text so far is the merge seat's KEEP-BOTH resolution of the steps before (an unresolved
            # marker text would make every later step conflict for the wrong reason)
            steps = []
            for k in range(1, len(order)):
                so_far = compose_keep_both(b, [ins[n] for n in order[:k]]); cf = os.path.join(sd, 'sofar_%s_%d.html' % (tag, k)); w(cf, so_far)
                rc, o = merge_file(cf, os.path.join(sd, 'base.html'), os.path.join(sd, order[k] + '.html')); steps.append((order[k], rc if rc >= 0 else 'ERR'))
                w(os.path.join(out, 'merge_%s_%s_step%s.txt' % (tag, nm[:10], order[k])), o)
            print('  ORDER %s (%s) textual merge-file, each step onto the KEEP-BOTH of the steps before (PR, conflict hunks): %s  [a conflict at the SAME base line is the expected finding: the keep-both is the merge seat\'s job; the marker texts are under predictions/]' % (tag, ' -> '.join('#' + n for n in order), steps))
            res = compose_keep_both(b, [ins[n] for n in order]); texts[(tag, d)] = res
            w(os.path.join(sd, 'composed_%s.html' % tag), res)
            fn = flow_numbers(res) if d == DOCS[0] else None
            once = all(res.count('\n'.join(ins[n][1])) == 1 for n in order)
            print('     KEEP-BOTH %s: each of the four fragments present once: %s%s' % (tag, once, (' | flow numbers in the composed tail %s (in file order)' % fn[-6:]) if fn else ''))
            if not once: rc_all = 1
            if d == DOCS[0]:
                want = [K['docs_composition']['flow_numbers'][n] for n in order]
                tail = [x for x in fn if x in want]
                print('     placement order %s -> file order of the four flow numbers %s' % (want, tail))
    SHELL_PATHS = ['systemTest', 'Blockchain/Dev/scripts', '.githooks'] + DOCS
    def tree(rev, dest):
        if not os.path.exists(dest): extract(clone, rev, SHELL_PATHS, dest)
        return dest
    mx = K['docs_composition']['matrix_suite']; results = {}
    for lab, rev, comp in [('base tree (control)', base, None)] + [('#%s head tree' % n, heads[n], None) for n in heads] + [('COMPOSED order %s' % t, base, t) for t, _ in orders]:
        td = os.path.join(scratch, 'mx_' + re.sub(r'\W+', '_', lab)[:18]); tree(rev, td)
        if comp:
            for d in DOCS: w(os.path.join(td, d), texts[(comp, d)])
        rc, o, e, to = run(['/bin/bash', os.path.join(td, mx)], cwd=td, timeout=300)
        m = re.search(r'(\d+) passed, (\d+) failed', o + e); c = (int(m.group(1)), int(m.group(2))) if m else None
        inval = 'is missing' in (o + e)
        w(os.path.join(out, 'matrix_%s.out' % re.sub(r'\W+', '_', lab)[:18]), o); w(os.path.join(out, 'matrix_%s.err' % re.sub(r'\W+', '_', lab)[:18]), e)
        print('%s html_docs_matrix on %-26s rc %d%s counts %s%s' % (now(), lab, rc, ' TIMEOUT' if to else '', c, '  TREE-INVALID (a doc is missing: not a measurement)' if inval else ''))
        results[lab] = (rc, c, inval)
        if inval: rc_all = 1
    ok_orders = [lab for lab, (rc, c, inv) in results.items() if lab.startswith('COMPOSED') and rc == 0 and c and c[1] == 0 and not inv]
    print('COMPOSED orders with html_docs_matrix 0 failed: %s (PASS condition: order A + at least ONE other)' % ok_orders)
    if 'COMPOSED order A' not in ok_orders or len(ok_orders) < 2: rc_all = 1
    # CONTROL: a composition that DROPS a block must be caught
    b0 = git_bytes(clone, base, DOCS[0]).decode(); drop = compose_keep_both(b0, [insertion(b0, git_bytes(clone, heads[n], DOCS[0]).decode()) for n in ('1443', '1446', '1445')])
    print('CONTROL: a composition WITHOUT #1444 reads flow number 50 present = %s (must be False: the all-four-blocks check can fail)' % (50 in flow_numbers(drop)))
    rc_all |= 1 if 50 in flow_numbers(drop) else 0
    return rc_all


# ---------------- STATE (vitest legs) ----------------
def state_writes(pkg, route, tests, clone, base, heads, scratch):
    """-> {relpath: bytes|None}: the variable paths of `pkg` in the requested state (None = the path must be ABSENT)."""
    wr = {}
    if pkg == 'api-gateway':
        notif, batch, audit = AG_ROUTES
        if route not in ('base', '1443', '1446', 'composedAB', 'composedBA'): raise SystemExit('REFUSED: --route %r for api-gateway (base|1443|1446|composedAB|composedBA)' % route)
        if route.startswith('composed'):
            order = ['1443', '1446'] if route == 'composedAB' else ['1446', '1443']
            b, _ = compose_audit(clone, base, heads, order, scratch)
            wr[notif] = git_bytes(clone, heads['1443'], notif); wr[batch] = git_bytes(clone, heads['1443'], batch); wr[audit] = b
        else:
            src = {'base': lambda p: base, '1443': lambda p: heads['1443'], '1446': lambda p: heads['1446'] if p == audit else base}[route]
            for p in AG_ROUTES: wr[p] = git_bytes(clone, src(p), p)
        want = {'none': [], '1443': ['1443'], '1446': ['1446'], 'both': ['1443', '1446']}
        if tests not in want: raise SystemExit('REFUSED: --tests %r for api-gateway (none|1443|1446|both)' % tests)
        for n, tf in AG_TESTS.items(): wr[tf] = git_bytes(clone, heads[n], tf) if n in want[tests] else None
    elif pkg == 'transfer':
        if route not in ('base', '1445'): raise SystemExit('REFUSED: --route %r for transfer (base|1445)' % route)
        if tests not in ('none', '1445'): raise SystemExit('REFUSED: --tests %r for transfer (none|1445)' % tests)
        wr[TR_ROUTE] = git_bytes(clone, base if route == 'base' else heads['1445'], TR_ROUTE)
        wr[TR_TEST] = git_bytes(clone, heads['1445'], TR_TEST) if tests == '1445' else None
    else:
        raise SystemExit('REFUSED: --pkg %r (api-gateway|transfer)' % pkg)
    return wr


def apply_state(wt, wr, qdir):
    """plants `wr` in WT; returns the restore record {path: original bytes|None}. Every plant ASSERTED LANDED."""
    rec = {}
    for rel, data in wr.items():
        p = os.path.join(wt, rel); must_be_outside(p, 'write')
        rec[rel] = open(p, 'rb').read() if os.path.isfile(p) else None
        if data is None:
            if os.path.isfile(p):
                os.makedirs(qdir, exist_ok=True); shutil.move(p, os.path.join(qdir, 'removed_%s_%d' % (os.path.basename(rel), int(time.time() * 1000))))
            if os.path.isfile(p): raise SystemExit('REMOVE NOT LANDED: %s' % rel)
        else:
            write_checked(wt, rel, data)
    return rec


def restore_state(wt, rec, qdir):
    bad = []
    for rel, data in rec.items():
        p = os.path.join(wt, rel)
        if data is None:
            if os.path.isfile(p):
                os.makedirs(qdir, exist_ok=True); shutil.move(p, os.path.join(qdir, 'planted_%s_%d' % (os.path.basename(rel), int(time.time() * 1000))))
            if os.path.isfile(p): bad.append(rel)
        else:
            write_checked(wt, rel, data)
            if sha(open(p, 'rb').read()) != sha(data): bad.append(rel)
    return bad


def test_rels(pkg, tests):
    if pkg == 'transfer': return [TR_TEST] if tests == '1445' else []
    return [AG_TESTS[n] for n in ({'1443': ['1443'], '1446': ['1446'], 'both': ['1443', '1446']}.get(tests, []))]


def cells_cmd(pkg, route, tests, whole, wt, clone, base, heads, scratch, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); qd = os.path.join(out, 'quarantine')
    wr = state_writes(pkg, route, tests, clone, base, heads, scratch)
    rec = apply_state(wt, wr, qd)
    for rel, data in wr.items(): print('PLANT LANDED %-44s %s' % (rel.split('/')[-1], ('sha256/16 ' + sha(data)[:16]) if data is not None else 'ABSENT (moved to quarantine)'))
    jp = os.path.join(out, '%s_route%s_tests%s_%s.json' % (pkg, route, tests, 'whole' if whole else 'file'))
    rels = [] if whole else test_rels(pkg, tests)
    if not whole and not rels: restore_state(wt, rec, qd); print('REFUSED: no test file in state --tests %s to run (use --whole)' % tests); return 2
    rc, o, e, to = vitest(wt, pkg, rels, jp, timeout=1800 if whole else 900); w(jp.replace('.json', '.out'), o); w(jp.replace('.json', '.err'), e)
    r = read_vitest(jp); bad = restore_state(wt, rec, qd)
    print('%s vitest %s rc %d%s | LOAD-FAILED %s | suites %d | tests %d passed %d failed %d skipped %d | restored by sha: %s | porcelain %r' % (
        now(), 'WHOLE ' + pkg if whole else 'on %d file(s)' % len(rels), rc, ' TIMEOUT' if to else '', r['load_failed'], r['suites'], r['tests'], r['passed'], r['failed'], r['skipped'], not bad, porcelain(wt)[:100]))
    if not whole:
        for k, v in sorted(r['cells'].items()): print('  %-8s %s%s' % (v.upper(), k, ('  :: ' + r['fail_msgs'][k][:200]) if k in r['fail_msgs'] else ''))
    else:
        for k, v in r['cells'].items():
            if v == 'failed': print('  RED %s' % k)
    key = (pkg, route, tests)
    print('PREDICTION %s: %s -- measured passed %d of %d tests, reds %s' % (key if not whole else (pkg, route, 'WHOLE'), (WHOLE_PRED.get((pkg, route)) if whole else PRED.get(key, 'none recorded')), r['passed'], r['tests'], sorted(k for k, v in r['cells'].items() if v == 'failed') if not whole else '(listed above)'))
    return 1 if (r['load_failed'] or bad) else 0


def tsc_cmd(pkg, route, wt, clone, base, heads, scratch, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); qd = os.path.join(out, 'quarantine')
    tests = {'api-gateway': {'base': 'none', '1443': '1443', '1446': '1446'}.get(route, 'both'), 'transfer': 'none' if route == 'base' else '1445'}[pkg]
    wr = state_writes(pkg, route, tests, clone, base, heads, scratch); rec = apply_state(wt, wr, qd)
    tsc = os.path.join(wt, DD, 'node_modules', '.bin', 'tsc'); pd = os.path.join(wt, 'Blockchain/Dev/services', pkg)
    rc, o, e, to = run(['node', tsc, '--noEmit', '-p', os.path.join(pd, 'tsconfig.json')], cwd=pd, timeout=900)
    bad = restore_state(wt, rec, qd)
    w(os.path.join(out, 'tsc_%s_%s.out' % (pkg, route)), o); w(os.path.join(out, 'tsc_%s_%s.err' % (pkg, route)), e)
    ex = run(['node', tsc, '--noEmit', '-p', os.path.join(pd, 'tsconfig.json'), '--listFilesOnly'], cwd=pd, timeout=300)[1]
    n_test = len([l for l in ex.split('\n') if '/__tests__/' in l])
    print('%s tsc --noEmit -p services/%s/tsconfig.json in state route=%s tests=%s: rc %d%s (stdout %d B, stderr %d B) | files in the program under src/__tests__: %d (the program %s the new tests) | restored %s' % (
        now(), pkg, route, tests, rc, ' TIMEOUT' if to else '', len(o), len(e), n_test, 'EXCLUDES' if n_test == 0 else 'INCLUDES', not bad))
    return 0 if (rc == 0 and not bad) else 1


# ---------------- probes ----------------
def probe_cmd(pkg, block, route, wt, clone, base, heads, scratch, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); qd = os.path.join(out, 'quarantine')
    if pkg == 'transfer':
        tests = '1445'; fn = os.path.join(HERE, 'probe_block_gate81.ts.txt'); tf = TR_TEST; blk = open(fn, encoding='utf-8').read()
    else:
        tests = 'both'; fn = os.path.join(HERE, 'probe_apigw_gate81.ts.txt'); tf = AG_TESTS[block]
        txt = open(fn, encoding='utf-8').read(); m = re.search(r'//@@ BLOCK %s\n(.*?)//@@ END %s\n' % (block, block), txt, re.S)
        if not m: raise SystemExit('REFUSED: probe block %s absent from %s' % (block, fn))
        blk = m.group(1)
    wr = state_writes(pkg, route, tests, clone, base, heads, scratch); rec = apply_state(wt, wr, qd)
    for rel, data in wr.items():
        if data is not None: print('PLANT LANDED %-44s sha256/16 %s' % (rel.split('/')[-1], sha(data)[:16]))
    src = open(os.path.join(wt, tf), encoding='utf-8').read()
    prel = os.path.join(os.path.dirname(tf), 'gate81-probe-%s.test.ts' % block)
    facts = os.path.join(out, 'probe_facts_%s_route%s.jsonl' % (block, route))
    if os.path.exists(facts): os.rename(facts, facts + '.prev.%d' % int(time.time()))
    write_checked(wt, prel, (src + '\n' + blk).encode('utf-8'))
    jp = os.path.join(out, 'probe_%s_route%s.json' % (block, route))
    rc, o, e, to = vitest(wt, pkg, [prel], jp, env_extra={'G81_PROBE_OUT': facts}); w(jp.replace('.json', '.out'), o); w(jp.replace('.json', '.err'), e)
    r = read_vitest(jp)
    qdir = os.path.join(out, 'quarantine_probe'); os.makedirs(qdir, exist_ok=True); shutil.move(os.path.join(wt, prel), os.path.join(qdir, 'gate81-probe-%s_route%s.test.ts' % (block, route)))
    bad = restore_state(wt, rec, qd); pc = porcelain(wt)
    print('%s probe vitest rc %d%s | LOAD-FAILED %s | tests %d passed %d failed %d | the probe copy moved to %s | restored %s | porcelain clean: %s' % (now(), rc, ' TIMEOUT' if to else '', r['load_failed'], r['tests'], r['passed'], r['failed'], qdir, not bad, pc == ''))
    ran = 0
    for l in open(facts) if os.path.isfile(facts) else []:
        d = json.loads(l); ran += 1
        print('  %s' % json.dumps(d, sort_keys=True)[:330])
    print('PROBE facts recorded: %d record(s) in %s (FACTS; the gate rules)' % (ran, facts))
    return 0 if (not r['load_failed'] and ran >= 3 and not bad and pc == '') else 1


# ---------------- tamper rows (#1443 / #1445 / #1446) ----------------
E_OBJ = "'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']'"
TAMPER = {
 '1443': dict(pkg='api-gateway', file=AG_ROUTES[1], route='1443', tests='1443', rows=[
    ('T1', 'revert ONE route (batch.ts) to the pre-ruling String(err)', [("err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? " + E_OBJ + " : 'thrown ' + typeof err", 'err instanceof Error ? err.message : String(err)')], ['RED KS-1346 G1 batch POST /certifications', 'RED KS-1346 G2 batch POST /certifications', 'RED KS-1346 G3 batch POST /certifications']),
    ('T2', 'drop the thrown-string branch (a string then falls to the object branch)', [("typeof err === 'string' ? err : ", '')], ['control KS-1346 GC2 batch POST /certifications']),
    ('T3', 'the object branch logs VALUES (JSON.stringify) instead of field names', [("'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']'", 'JSON.stringify(err)')], ['RED KS-1346 G1 batch POST /certifications', 'RED KS-1346 G2 batch POST /certifications', 'control KS-1346 GC1 batch POST /certifications']),
    ('T4', 'drop the `err !== null` guard (a thrown null then dereferences null INSIDE fail500)', [(" && err !== null", '')], []),
    ('T5', 'the class name is a constant `Object` (a class instance loses its name)', [("Object.getPrototypeOf(err)?.constructor?.name ?? 'object'", "'Object'")], ['RED KS-1346 G2 batch POST /certifications']),
    ('T6', 'fail500 answers err.message in the 500 body (this file\'s cells check the body only for a thrown OBJECT, which has no .message)', [("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });", "res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: String((err as any)?.message ?? 'Internal server error') } });")], [])]),
 '1446': dict(pkg='api-gateway', file=AUDIT, route='1446', tests='1446', rows=[
    ('Y1', 'remove the logger.error call from the 502 catch', [(None, None)], ['RED KS-1410 X2', 'RED KS-1410 X4']),
    ('Y2', 'the new log line uses the PRE-ruling String(err) (the payload\'s own state)', [("{ error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? " + E_OBJ + " : 'thrown ' + typeof err });\n      res.status(502)", "{ error: err instanceof Error ? err.message : String(err) });\n      res.status(502)")], ['RED KS-1410 X4']),
    ('Y3', 'the 502 message is the template `${err.message}` again', [("message: 'Failed to reach security service',", "message: `Failed to reach security service: ${err.message}`,")], ['RED KS-1410 X1 NODE_ENV=production', 'RED KS-1410 X1 NODE_ENV=development', 'RED KS-1410 X1 NODE_ENV=test', 'RED KS-1410 X3', 'RED KS-1410 X4']),
    ('Y4', 'the 502 message is a DIFFERENT constant (the cells are loose about wording)', [("message: 'Failed to reach security service',", "message: 'Bad gateway',")], []),
    ('Y5', 'the log line carries the thrown VALUE via JSON.stringify for objects', [("'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });\n      res.status(502)", "JSON.stringify(err) : 'thrown ' + typeof err });\n      res.status(502)")], ['RED KS-1410 X4']),
    ('Y6', 'the 502 status becomes 500', [("res.status(502).json({\n        success: false,\n        error: {\n          code: 'BAD_GATEWAY',\n          // KS-1410: a constant message.", "res.status(500).json({\n        success: false,\n        error: {\n          code: 'BAD_GATEWAY',\n          // KS-1410: a constant message.")], ['RED KS-1410 X1 NODE_ENV=production', 'RED KS-1410 X1 NODE_ENV=development', 'RED KS-1410 X1 NODE_ENV=test', 'RED KS-1410 X2', 'RED KS-1410 X4'])]),
 '1445': dict(pkg='transfer', file=TR_ROUTE, route='1445', tests='1445', rows=[
    ('Z1', 'remove the logger.error call', [("logger.error('Process expired delegations failed (POST /api/delegations/admin/process-expired)', { error: error.message });\n", '')], ['RED KS-1410 T2']),
    ('Z2', 'the 500 body answers error.message again', [("message: 'Internal server error' } });\n    }\n    next(error);", "message: error.message } });\n    }\n    next(error);")], ['RED KS-1410 T1 NODE_ENV=production', 'RED KS-1410 T1 NODE_ENV=development', 'RED KS-1410 T1 NODE_ENV=test']),
    ('Z3', 'the log carries String(error) instead of error.message', [("{ error: error.message });\n      return res.status(500)", "{ error: String(error) });\n      return res.status(500)")], ['RED KS-1410 T2']),
    ('Z4', 'the status becomes 503', [("return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });", "return res.status(503).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });")], ['RED KS-1410 T1 NODE_ENV=production', 'RED KS-1410 T1 NODE_ENV=development', 'RED KS-1410 T1 NODE_ENV=test', 'RED KS-1410 T2']),
    ('Z5', 'the instanceof guard becomes `true` (a NON-Error throw is now logged as .message and answered 500)', [("if (error instanceof Error) {\n      // KS-1410", "if (true) {\n      // KS-1410")], []),
    ('Z6', 'next(error) removed (a non-Error throw would leave the request hanging)', [("    }\n    next(error);\n  }\n});\n\nexport { router as delegationRoutes };", "    }\n  }\n});\n\nexport { router as delegationRoutes };")], [])]),
}


def tamper_cmd(pr, wt, clone, base, heads, scratch, out, only):
    T = TAMPER[pr]; must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); qd = os.path.join(out, 'quarantine'); rc_all = 0
    wr = state_writes(T['pkg'], T['route'], T['tests'], clone, base, heads, scratch); rec = apply_state(wt, wr, qd)
    rels = test_rels(T['pkg'], T['tests']) if pr != '1443' else [AG_TESTS['1443']]
    head_src = git_bytes(clone, heads[pr], T['file']).decode('utf-8')
    # the working file is whatever the state planted (a composed/ route state is not used here: the PR's own head file)
    write_checked(wt, T['file'], head_src.encode('utf-8'))
    rows = [('HEAD', 'no change (all green)', None, []), ('CONTROL', 'a no-op comment appended (all green)', 'NOOP', [])] + [(a, b, c, d) for a, b, c, d in T['rows']]
    for tid, name, edits, pred in rows:
        if only and tid not in only and tid not in ('HEAD', 'CONTROL'): continue
        try:
            if edits is None: new = head_src
            elif edits == 'NOOP': new = head_src + '\n// gate81-noop\n'
            elif edits == [(None, None)]:   # Y1: remove the whole logger.error statement of the 502 catch
                m = re.search(r"\n[ \t]*logger\.error\('Audit export could not reach the security service[^\n]*\n", head_src)
                if not m or len(re.findall(r"logger\.error\('Audit export could not reach", head_src)) != 1: raise SystemExit('ANCHOR logger.error(502) occurs != 1 — the tamper is NOT applied')
                new = head_src[:m.start()] + '\n' + head_src[m.end():]
            else: new = apply_edits(head_src, edits)
        except SystemExit as e:
            print('%s %-8s TAMPER-INVALID: %s' % (now(), tid, e)); rc_all = 1; continue
        ok_land = (new == head_src) if edits is None else (new != head_src and (edits == 'NOOP' or edits == [(None, None)] or all(b in new for _, b in edits if b)))
        write_checked(wt, T['file'], new.encode('utf-8'))
        jp = os.path.join(out, 'tamper_%s_%s.json' % (pr, tid)); r_rc, o, e, to = vitest(wt, T['pkg'], rels, jp); w(jp.replace('.json', '.out'), o); w(jp.replace('.json', '.err'), e)
        r = read_vitest(jp); reds = sorted(k for k, v in r['cells'].items() if v == 'failed')
        write_checked(wt, T['file'], head_src.encode('utf-8')); back = sha(open(os.path.join(wt, T['file']), 'rb').read()) == sha(head_src.encode())
        if r['load_failed']: verdict = 'TAMPER-INVALID (suite failed to LOAD: %s)' % r['message'][:120]; rc_all = 1
        elif tid == 'HEAD': verdict = 'OK all green' if not reds else 'FAIL: HEAD row has reds %s' % reds; rc_all |= 0 if not reds else 1
        elif tid == 'CONTROL': verdict = 'OK all green (harness quiet)' if not reds else 'FAIL: the no-op reds %s: the harness is noisy' % reds; rc_all |= 0 if not reds else 1
        else: verdict = ('ALL-GREEN: NO CELL CATCHES THIS TAMPER (a finding to rule)' if not reds else 'caught by %d cell(s)' % len(reds)) + ' | kit-builder prediction %s: %s' % (pred or 'ALL-GREEN', 'MATCH' if sorted(pred) == reds else 'DIFFER')
        print('%s %-8s %-78s landed %s restored %s | tests %d failed %d | %s' % (now(), tid, name[:78], ok_land, back, r['tests'], r['failed'], verdict))
        for k in reds: print('      RED %s :: %s' % (k, r['fail_msgs'].get(k, '')[:180]))
        if not ok_land or not back: rc_all = 1
    bad = restore_state(wt, rec, qd)
    print('porcelain after the tamper rows: %r | state restored: %s' % (porcelain(wt)[:120], not bad)); return rc_all | (1 if bad else 0)


# ---------------- #1444: the relink guard ----------------
G44 = P44['gate_script']; S44 = P44['suite']; GUARD = 'if (u !~ /^:/) sub(/:.*$/, "", u)'


def pcounts(text):
    m = re.search(r'(\d+) passed, (\d+) failed', text); return (int(m.group(1)), int(m.group(2))) if m else None


def run_sh(bash, script, cwd, timeout=300):
    rc, o, e, to = run([bash, script], cwd=cwd, timeout=timeout); return rc, o, e, to, pcounts(o + e)


def suite1444(wt44, clone, head, base, out):
    must_be_outside(wt44, 'worktree'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    if not os.path.isdir(os.path.join(wt44, 'Blockchain')): print('REFUSED: %s is not a worktree of the kit clone (git worktree add --detach it at the #1444 head first)' % wt44); return 2
    got = subprocess.run(['git', '-C', wt44, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    if got != head: print('REFUSED: the worktree is at %s, not --head %s' % (got[:12], head[:12])); return 2
    g_head = git_bytes(clone, head, G44); g_base = git_bytes(clone, base, G44); gp = os.path.join(wt44, G44); suite = os.path.join(wt44, S44)
    assert sha(open(gp, 'rb').read()) == sha(g_head)
    txt = g_head.decode('utf-8'); nr = apply_edits(txt, [(GUARD, 'sub(/:.*$/, "", u)')])   # the payload WITHOUT the ruled deviation
    arms = [('A', 'head script, head suite', g_head, (112, 0), 0), ('B', 'BASE script planted, head suite', g_base, (108, 4), 1), ('C', 'head script MINUS the ruled deviation guard (the payload\'s state)', nr.encode(), (111, 1), 1)]
    mode = os.stat(gp).st_mode
    for aid, lab, data, want, wrc in arms:
        write_checked(wt44, G44, data); os.chmod(gp, mode)
        rc, o, e, to, c = run_sh('/bin/bash', suite, wt44)
        w(os.path.join(out, 'suite1444_%s.out' % aid), o); w(os.path.join(out, 'suite1444_%s.err' % aid), e)
        reds = [l.strip() for l in o.split('\n') if 'FAIL' in l and l.strip().startswith('FAIL')]
        print('%s ARM %s (%s): rc %d%s counts %s (the PR body says %s, rc %s) | plant sha256/16 %s' % (now(), aid, lab, rc, ' TIMEOUT' if to else '', c, want, wrc, sha(data)[:16]))
        for l in reds[:6]: print('      RED %s' % l[:170])
        if aid == 'A' and (c != want or rc != 0): rc_all = 1
        if aid != 'A' and rc == 0: rc_all = 1
    write_checked(wt44, G44, g_head); os.chmod(gp, mode)
    print('restored by sha: %s | mode %s | porcelain %r' % (sha(open(gp, 'rb').read()) == sha(g_head), oct(os.stat(gp).st_mode & 0o777), porcelain(wt44)[:100]))
    # siblings, base script vs head script
    sibs = P44.get('claims', {}); names = ['check_shared_relink_case.test.sh', 'check_shared_relink_tooling_tokens.test.sh', 'preflight_deps.test.sh']
    for rev, data in (('base', g_base), ('head', g_head)):
        write_checked(wt44, G44, data); os.chmod(gp, mode)
        for nm in names:
            sp = os.path.join(wt44, 'Blockchain/Dev/scripts/__tests__', nm)
            rc, o, e, to, c = run_sh('/bin/bash', sp, wt44); w(os.path.join(out, 'sibling_%s_%s.out' % (rev, nm)), o); w(os.path.join(out, 'sibling_%s_%s.err' % (rev, nm)), e)
            print('%s SIBLING %-4s %-48s rc %d%s counts %s' % (now(), rev, nm, rc, ' TIMEOUT' if to else '', c))
    write_checked(wt44, G44, g_head); os.chmod(gp, mode)
    rc, o, e, to, c = run_sh('/bin/bash', os.path.join(wt44, K['docs_composition']['matrix_suite']), wt44)
    print('%s html_docs_matrix at the head tree: rc %d counts %s (the PR body says 12/0)' % (now(), rc, c))
    rc, o, e, to = run(['/bin/bash', os.path.join(wt44, 'Blockchain/Dev/scripts/run-shell-suites.sh'), '--list'], cwd=wt44)
    n = len([l for l in o.split('\n') if l.strip()]); print('%s run-shell-suites.sh --list at the head: rc %d, %d suite line(s) (the PR body says the count stays 73); check_shared_relink listed: %s' % (now(), rc, n, 'check_shared_relink.test.sh' in o))
    print('Homebrew bash: %s' % ('present' if os.path.isfile('/opt/homebrew/bin/bash') else 'NOT PRESENT: that leg is NOT RUN (/bin/bash 3.2 only)'))
    return rc_all


def tamper1444(wt44, clone, head, out):
    must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    g_head = git_bytes(clone, head, G44).decode('utf-8'); gp = os.path.join(wt44, G44); mode = os.stat(gp).st_mode; suite = os.path.join(wt44, S44)
    RX_NEW = r'([^ \t]*\/)?node_modules'; RX_OLD = r'(\/[^ \t]*\/)?node_modules'
    rows = [('HEAD', 'no change (112/0)', None, (112, 0)), ('CONTROL', 'a no-op awk comment appended', 'NOOP', (112, 0)),
            ('T1', 'revert the destination prefix group to the base (leading slash required)', [(RX_NEW, RX_OLD)], 'F-C cells red'),
            ('T2', 'revert the USER drop to the base (compare the whole value)', [('sub(/[ \\t].*$/, "", u); ' + GUARD, 'sub(/[ \\t].*$/, "", u)')], 'F-E cells red'),
            ('T3', 'remove ONLY the ruled deviation guard', [(GUARD, 'sub(/:.*$/, "", u)')], 'the F-E pin red (111/1)'),
            ('T4', 'OVER-WIDEN the prefix group so `xnode_modules/@secuura/shared` also passes', [(RX_NEW, r'([^ \t]*)node_modules')], 'no cell may be expected to catch it: ALL-GREEN is the finding')]
    for tid, name, edits, pred in rows:
        try:
            if edits is None: new = g_head
            elif edits == 'NOOP': new = g_head + '\n# gate81-noop\n'
            else: new = apply_edits(g_head, edits)
        except SystemExit as e:
            print('%s %-8s TAMPER-INVALID: %s' % (now(), tid, e)); rc_all = 1; continue
        write_checked(wt44, G44, new.encode('utf-8')); os.chmod(gp, mode)
        rc, o, e, to, c = run_sh('/bin/bash', suite, wt44)
        reds = [l.strip()[:120] for l in o.split('\n') if l.strip().startswith('FAIL')]
        write_checked(wt44, G44, g_head.encode('utf-8')); os.chmod(gp, mode); back = sha(open(gp, 'rb').read()) == sha(g_head.encode())
        if c is None: verdict = 'TAMPER-INVALID (no count: the suite did not run)'; rc_all = 1
        elif tid in ('HEAD', 'CONTROL'): verdict = 'OK' if c == pred and rc == 0 else 'FAIL: %s' % (c,); rc_all |= 0 if c == pred and rc == 0 else 1
        else: verdict = ('ALL-GREEN: NO CELL CATCHES THIS TAMPER (a finding to rule)' if c[1] == 0 else 'caught: %d failed' % c[1]) + ' | kit-builder prediction: %s' % pred
        print('%s %-8s %-78s restored %s | rc %d counts %s | %s' % (now(), tid, name[:78], back, rc, c, verdict))
        for l in reds[:5]: print('      %s' % l)
        if not back: rc_all = 1
    print('porcelain after the tamper rows: %r' % porcelain(wt44)[:100]); return rc_all


# the kit's OWN 32 probes (+ extras). Every final stage opens with the same shared-builder / builder / final head the suite's cells use.
HEADDF = 'FROM node:24-alpine AS shared-builder\nRUN npm ci --ignore-scripts\nFROM node:24-alpine AS builder\nCOPY --from=shared-builder /shared /shared\nRUN npm ci --ignore-scripts\nFROM node:24-alpine'
R1 = 'RUN npm ci --ignore-scripts --omit=dev\nCOPY --from=shared-builder /shared /shared'
def _dest(label, line, cls): return (cls, label, R1 + '\n' + line + '\nUSER secuura')
def _user(label, val, cls): return (cls, label, 'USER %s\n%s\nRUN ln -s /shared node_modules/@secuura/shared\nUSER secuura' % (val, R1))
PROBES = [
 _dest('dest node_modules/@secuura/shared', 'RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared', 'CONTROL'),
 _dest('dest /app/node_modules/... (absolute)', 'RUN ln -s /shared /app/node_modules/@secuura/shared', 'CONTROL'),
 _dest('dest /tmp/node_modules/... (absolute, WRONG dir)', 'RUN ln -s /shared /tmp/node_modules/@secuura/shared', 'CONTROL'),
 _user('USER root', 'root', 'CONTROL'), _user('USER 0', '0', 'CONTROL'),
 _dest('dest ./node_modules/...', 'RUN ln -s /shared ./node_modules/@secuura/shared', 'NEWLY-ACCEPTED'),
 _dest('dest app/node_modules/...', 'RUN ln -s /shared app/node_modules/@secuura/shared', 'NEWLY-ACCEPTED'),
 _dest('dest ../node_modules/... (the PARENT of WORKDIR: the MEASURED GAP)', 'RUN ln -s /shared ../node_modules/@secuura/shared', 'NEWLY-ACCEPTED'),
 _dest('dest ${APP}/node_modules/... (brace variable prefix)', 'RUN ln -s /shared ${APP}/node_modules/@secuura/shared', 'NEWLY-ACCEPTED'),
 _dest('dest a/b/c/node_modules/... (deep relative)', 'RUN ln -s /shared a/b/c/node_modules/@secuura/shared', 'NEWLY-ACCEPTED'),
 _user('USER root:root', 'root:root', 'NEWLY-ACCEPTED'), _user('USER 0:0', '0:0', 'NEWLY-ACCEPTED'), _user('USER root:1000', 'root:1000', 'NEWLY-ACCEPTED'), _user('USER 0:secuura', '0:secuura', 'NEWLY-ACCEPTED'),
 _dest('dest ./node_modules/@secuura/shared2', 'RUN ln -s /shared ./node_modules/@secuura/shared2', 'STILL-REFUSED'),
 _dest('dest ./node_modules/@secuura/shared/x', 'RUN ln -s /shared ./node_modules/@secuura/shared/x', 'STILL-REFUSED'),
 _dest('dest ./node_modules/@secuura/other', 'RUN ln -s /shared ./node_modules/@secuura/other', 'STILL-REFUSED'),
 _dest('source /sharedx, relative dest', 'RUN ln -s /sharedx ./node_modules/@secuura/shared', 'STILL-REFUSED'),
 _dest('source /shared/sub, relative dest', 'RUN ln -s /shared/sub ./node_modules/@secuura/shared', 'STILL-REFUSED'),
 _dest('source `shared` (relative source), relative dest', 'RUN ln -s shared ./node_modules/@secuura/shared', 'STILL-REFUSED'),
 _dest('HARD link (no -s), relative dest', 'RUN ln /shared ./node_modules/@secuura/shared', 'STILL-REFUSED'),
 ('STILL-REFUSED', 'relative link BEFORE the last node_modules write', 'COPY --from=shared-builder /shared /shared\nRUN ln -s /shared ./node_modules/@secuura/shared\nRUN npm ci --ignore-scripts --omit=dev\nUSER secuura'),
 ('STILL-REFUSED', 'relative link AFTER USER secuura', R1 + '\nUSER secuura\nRUN ln -s /shared ./node_modules/@secuura/shared'),
 ('STILL-REFUSED', 'no re-link at all', R1 + '\nUSER secuura'),
 _user('USER secuura:root (non-root user, root group)', 'secuura:root', 'STILL-REFUSED'), _user('USER 1000:0', '1000:0', 'STILL-REFUSED'), _user('USER node:node', 'node:node', 'STILL-REFUSED'),
 _user('USER :root (EMPTY user part: the ruled deviation)', ':root', 'STILL-REFUSED'), _user('USER :0 (EMPTY user part)', ':0', 'STILL-REFUSED'),
 _user('USER rootless:root', 'rootless:root', 'STILL-REFUSED'), _user('USER root0:root', 'root0:root', 'STILL-REFUSED'), _user('USER secuura', 'secuura', 'STILL-REFUSED'),
]
EXTRAS = [   # FACTS, no expectation
 _dest('EXTRA dest ../../node_modules/...', 'RUN ln -s /shared ../../node_modules/@secuura/shared', 'FACT'),
 _dest('EXTRA dest ./x/../node_modules/...', 'RUN ln -s /shared ./x/../node_modules/@secuura/shared', 'FACT'),
 _user('EXTRA USER root: (trailing colon, empty group)', 'root:', 'FACT'), _user('EXTRA USER 0: (trailing colon)', '0:', 'FACT'),
 _dest('EXTRA dest /node_modules/... (filesystem root)', 'RUN ln -s /shared /node_modules/@secuura/shared', 'FACT'),
]


def widen1444(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True)
    gb = os.path.join(scratch, 'guard_base.sh'); gh_ = os.path.join(scratch, 'guard_head.sh'); w(gb, git_bytes(clone, base, G44)); w(gh_, git_bytes(clone, head, G44))
    wd = os.path.join(scratch, 'widen_%d' % int(time.time())); counts = {}; unexpected = []; rows = []
    for idx, (cls, label, body) in enumerate(PROBES + EXTRAS, 1):
        d = os.path.join(wd, 'p%02d' % idx); os.makedirs(os.path.join(d, 'services/thing')); w(os.path.join(d, 'services/thing/Dockerfile'), HEADDF + '\n' + body + '\n')
        rb = run(['/bin/bash', gb, d], timeout=60); ra = run(['/bin/bash', gh_, d], timeout=60)
        if rb[3] or ra[3]: got = 'TIMEOUT'
        elif rb[0] == 0 and ra[0] == 0: got = 'CONTROL'
        elif rb[0] != 0 and ra[0] == 0: got = 'NEWLY-ACCEPTED'
        elif rb[0] != 0 and ra[0] != 0: got = 'STILL-REFUSED'
        else: got = 'NEWLY-REFUSED'
        exp = '' if cls == 'FACT' else cls
        v = 'FACT' if cls == 'FACT' else ('OK' if got == cls else 'UNEXPECTED')
        if v == 'UNEXPECTED': unexpected.append(label)
        if cls != 'FACT': counts[got] = counts.get(got, 0) + 1
        why = re.search(r'(re-link invariant[^\n]{0,90}|final stage has NO[^\n]{0,60})', ra[1] + ra[2])
        rows.append((v, got, rb[0], ra[0], label))
        print('%-10s %-15s base=%s head=%s  %-70s %s' % (v, got, rb[0], ra[0], label[:70], (why.group(1)[:70] if why else '')))
    seat = K['relink']['seat_matrix']
    mine = dict(control=counts.get('CONTROL', 0), newly_accepted=counts.get('NEWLY-ACCEPTED', 0), still_refused=counts.get('STILL-REFUSED', 0), newly_refused=counts.get('NEWLY-REFUSED', 0), unexpected=len(unexpected))
    print('WIDEN MATRIX (the kit\'s own %d probes): %s | the SEAT\'s matrix (PR body / READY): %s | equal: %s' % (len(PROBES), mine, seat, mine == seat))
    gap = [r for r in rows if '../node_modules' in r[4] and 'EXTRA' not in r[4]]
    tmpc = [r for r in rows if '/tmp/node_modules' in r[4]]
    print('THE MEASURED GAP: `ln -s /shared ../node_modules/@secuura/shared` reads %s (base rc %s -> head rc %s): the guard does not check that the destination is the stage\'s OWN node_modules; the control `/tmp/node_modules` reads %s (already accepted at BASE)' % (
        gap[0][1], gap[0][2], gap[0][3], tmpc[0][1]))
    print('DOCKER: whether Docker builds `USER :root` (or runs it as root) is UNMEASURED: no Docker here, and the probes exercise the guard\'s parser only.')
    return 0 if (not unexpected and len(PROBES) == 32) else 1


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    try: apply_edits('a b a', [('a', 'x')]); rep(False, 'a 2-occurrence anchor was ACCEPTED')
    except SystemExit: rep(True, 'ARM: anchor occurring twice -> refused (tamper not applied)')
    try: apply_edits('a b', [('zz', 'x')]); rep(False, 'an absent anchor was ACCEPTED')
    except SystemExit: rep(True, 'ARM: anchor absent -> refused')
    t = apply_edits('one two', [('two', 'TWO')]); rep(t == 'one TWO' and landed('one two', t, [('two', 'TWO')]), 'a single-occurrence edit applies and reads LANDED')
    rep(not landed('x', 'x', [('a', 'b')]), 'PLANTED no-change reads NOT LANDED')
    j = {'testResults': [{'name': 'a', 'status': 'passed', 'assertionResults': [{'title': 'RED KS-1346 G1 batch POST /certifications: x', 'status': 'passed'}, {'title': 'RED KS-1410 X4: y', 'status': 'failed', 'failureMessages': ['boom\n at x']}]},
                         {'name': 'b', 'status': 'failed', 'assertionResults': [], 'message': 'Test suite failed to run'}]}
    p = os.path.join(HERE, '_scratch', 'selftest_vitest.json'); w(p, json.dumps(j)); r = read_vitest(p)
    rep(r['load_failed'] and r['tests'] == 2 and r['failed'] == 1 and r['cells'].get('RED KS-1410 X4') == 'failed' and 'RED KS-1346 G1 batch POST /certifications' in r['cells'], 'vitest reader: a suite that failed to LOAD is load_failed (never a count); cell keys read')
    w(p, json.dumps({'testResults': [{'name': 'a', 'status': 'passed', 'assertionResults': [{'title': 'ok', 'status': 'passed'}]}]})); rep(not read_vitest(p)['load_failed'], 'vitest reader: a clean file is not load_failed')
    rep(read_vitest(os.path.join(HERE, '_scratch', 'does-not-exist.json'))['load_failed'], 'vitest reader: NO JSON WRITTEN reads load_failed (never a green)')
    seen = {}; rep(cell_key('control KS-1346 GC1 a: x', {}) == 'control KS-1346 GC1 a', 'cell keys: the key is the title up to the first colon'); k1 = cell_key('RED KS-1 X1: a', seen); k2 = cell_key('RED KS-1 X1: b', seen); rep(k1 != k2, 'cell keys: two titles with the same prefix get distinct keys')
    rep(pcounts('x\n  112 passed, 0 failed, 0 skipped\n') == (112, 0) and pcounts('nothing') is None, 'pcounts reads "N passed, M failed" and nothing else')
    base = 'x\n</body>\n'
    ia, fa = insertion(base, 'x\nH45\n</body>\n'); ib, fb = insertion(base, 'x\nH46\n</body>\n'); ic, fc = insertion(base, 'x\nH50\n</body>\n')
    rep(ia == ib == ic == 1 and compose_keep_both(base, [(ia, fa), (ib, fb), (ic, fc)]) == 'x\nH45\nH46\nH50\n</body>\n', 'compose_keep_both: three same-position insertions compose in the given order, each present once')
    rep(compose_keep_both(base, [(ic, fc), (ib, fb), (ia, fa)]) == 'x\nH50\nH46\nH45\n</body>\n', 'compose_keep_both: the REVERSE placement is a different, equally complete text')
    rep(compose_keep_both(base, [(ia, fa)]).count('H46') == 0, 'CONTROL: a composition keeping one block reads the others ABSENT (the all-blocks check can fail)')
    try: compose_keep_both(base, [(1, ['a']), (2, ['b'])]); rep(False, 'fragments at different positions were ACCEPTED')
    except SystemExit: rep(True, 'ARM: fragments at different base positions -> refused')
    try: insertion(base, 'y\n</body>\n'); rep(False, 'a non-insertion was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a replaced base line is not a pure insertion -> refused')
    rep(flow_numbers('<h2>45. a</h2><h2>46. b</h2><h2>50. c</h2>') == [45, 46, 50], 'flow_numbers reads <h2>NN.</h2> headings')
    d = os.path.join(HERE, '_scratch', 'selftest_a'); w(os.path.join(d, 'x'), 'one\ntwo\nthree\n'); w(os.path.join(d, 'y'), 'one\ntwo\nthree\nfour\n'); w(os.path.join(d, 'z'), 'zero\ntwo\nthree\n')
    rc, o = merge_file(os.path.join(d, 'y'), os.path.join(d, 'x'), os.path.join(d, 'z'))
    rep(rc == 0 and o.startswith('zero') and o.rstrip().endswith('four'), 'merge_file: a clean 3-way merge reads rc 0 (the reader of the conflict count works)')
    w(os.path.join(d, 'q'), 'one\nTWO\nthree\n'); w(os.path.join(d, 'r'), 'one\ntwo!\nthree\n')
    rc, o = merge_file(os.path.join(d, 'q'), os.path.join(d, 'x'), os.path.join(d, 'r'))
    rep(rc == 1 and ('<' * 7 + ' ours') in o, 'merge_file: PLANTED same-line edits read rc 1 with a conflict marker (the instrument can see a conflict)')
    rc, o, e, to = run(['sh', '-c', 'cat >/dev/null'], timeout=2, stdin=None); rep(rc == 0 and not to, 'run(): a child with stdin /dev/null returns')
    pre = time.time(); rc, o, e, to = run(['sh', '-c', 'sleep 30'], timeout=1); rep(to and time.time() - pre < 6, 'run(): a hanging child is killed by process group at the timeout (TIMEOUT reported)')
    try: must_be_outside('/Volumes/DevMASTER/!CODING/x/y', 'write'); rep(False, 'a write under !CODING was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a write path under !CODING -> refused (lexical)')
    try: extract('/nonexistent-repo', 'abc', ['x'], '/Volumes/DevMASTER/!CODING/zz'); rep(False, 'extract into !CODING was ACCEPTED')
    except SystemExit: rep(True, 'ARM: extract into a !CODING dest -> refused before any write')
    try: cgit('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files', ['write-tree']); rep(False, 'plumbing in the shared checkout was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a plumbing write verb against a clone under !CODING (the shared checkout) -> refused before it runs')
    try: state_writes('api-gateway', 'main', 'none', 'x', 'y', {}, 'z'); rep(False, '--route main was ACCEPTED')
    except SystemExit: rep(True, 'ARM: --route main -> refused')
    try: state_writes('transfer', 'base', 'both', 'x', 'y', {}, 'z'); rep(False, 'transfer --tests both was ACCEPTED')
    except SystemExit: rep(True, 'ARM: transfer --tests both -> refused')
    rep(len(PROBES) == 32 and sum(1 for p_ in PROBES if p_[0] == 'CONTROL') == 5 and sum(1 for p_ in PROBES if p_[0] == 'NEWLY-ACCEPTED') == 9 and sum(1 for p_ in PROBES if p_[0] == 'STILL-REFUSED') == 18, 'the kit\'s probe set is 32 = 5 CONTROL + 9 NEWLY-ACCEPTED + 18 STILL-REFUSED (its own expectation, to be MEASURED)')
    for pr, T in TAMPER.items():
        ok = all(len(rows_) == 4 for rows_ in T['rows'])
        rep(ok, '#%s tamper table: %d rows, each (id, name, edits, predicted reds)' % (pr, len(T['rows'])))
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        cmd = A[0]
        if cmd == 'setup': return setup(req(A, '--clone'), req(A, '--head', True), req(A, '--wt'), opt(A, '--log'))
        if cmd in ('cells', 'tsc', 'probe', 'tamper'):
            wt, cl, bs, out = req(A, '--wt'), req(A, '--clone'), req(A, '--base', True), req(A, '--out')
            sc = opt(A, '--scratch') or os.path.join(out, 'scratch')
            heads = dict((n, req(A, '--head' + n, True)) for n in ('1443', '1445', '1446')) if cmd != 'tamper' else dict((n, opt(A, '--head' + n)) for n in ('1443', '1445', '1446'))
            if cmd == 'tamper':
                pr = req(A, '--pr')
                if pr not in TAMPER: raise SystemExit('REFUSED: --pr %r has no tamper table (1443|1445|1446)' % pr)
                heads[pr] = req(A, '--head' + pr, True)
                return tamper_cmd(pr, wt, cl, bs, heads, sc, out, (opt(A, '--only') or '').split(',') if opt(A, '--only') else None)
            pkg, route = req(A, '--pkg'), req(A, '--route')
            if cmd == 'cells': return cells_cmd(pkg, route, req(A, '--tests'), '--whole' in A, wt, cl, bs, heads, sc, out)
            if cmd == 'tsc': return tsc_cmd(pkg, route, wt, cl, bs, heads, sc, out)
            return probe_cmd(pkg, req(A, '--block'), route, wt, cl, bs, heads, sc, out)
        if cmd == 'suite1444': return suite1444(req(A, '--wt44'), req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--out'))
        if cmd == 'tamper1444': return tamper1444(req(A, '--wt44'), req(A, '--clone'), req(A, '--head', True), req(A, '--out'))
        if cmd == 'widen1444': return widen1444(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'compose': return compose_cmd(req(A, '--clone'), req(A, '--base', True), heads_of(A), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'docs': return docs_cmd(req(A, '--clone'), req(A, '--base', True), heads_of(A), req(A, '--develop', True), req(A, '--scratch'), req(A, '--out'))
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
