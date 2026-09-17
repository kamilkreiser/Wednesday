#!/usr/bin/env python3
"""drafter_tamper_1034.py [ROW ...] — the #1034 tamper table on the WHOLE api-gateway suite at HEAD fd81a75f0 in the drafter clone (vitest 4.1.11 via
node .../node_modules/vitest/vitest.mjs; --testTimeout=60000 --hookTimeout=60000 unless the row says default).
SEAT ROWS: parsed from the seat runner's ROWS literal (Blockchain/5_Project_History/2026-09-17_seatA-7th/ks1215/build/tamper_1215_r2.py, READ-ONLY, sha256
printed) by a restricted AST evaluator (string constants, names bound to earlier string constants, +, slices, len(<const>)): the runner is NEVER executed
(it hard-codes the seat worktree). The seat's WHOLEFILE row swaps auth.ts to develop 27e53ec3a's bytes, read from the drafter clone.
DRAFTER ROWS: aimed at what the 16 cells do not pin (a partial strip, a differently-cased delete, the delete gated on `required`, an empty string
instead of a delete, an onProxyReq re-add from rawAuthorization, a hand-forwarded route reading rawAuthorization, and platform.ts's authHeaders
without rawAuthorization (a fix shape: does any cell depend on it?)).
Every row: every anchor count asserted 1 against HEAD bytes (else VOID, nothing written) + a marker asserted landed; project `tsc --noEmit -p .` rc
(non-zero = VOID); denominator asserted = T0 (files, tests, pending 0); reds split AssertionError vs other, per file; restore by bytes, blob sha asserted,
`git diff --quiet HEAD`. Load beside every row. Never rm; stderr kept per row under out/tamper/."""
import ast, hashlib, json, os, re, subprocess, sys, datetime, time
GSD = os.path.dirname(os.path.abspath(__file__)); OUTD = GSD + '/out/tamper'; os.makedirs(OUTD, exist_ok=True)
PA = json.load(open(GSD + '/drafter_paths.json')); T = PA['trees']; C = PA['C']; SHA = PA['sha']
WT = T['head']; GWREL = 'Blockchain/Dev/services/api-gateway'; GW = WT + '/' + GWREL
AUREL = 'src/middleware/auth.ts'; PXREL = 'src/routes/proxy.ts'; PFREL = 'src/routes/platform.ts'
SEAT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-17_seatA-7th/ks1215/build/tamper_1215_r2.py'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return '%.1f/%.1f/%.1f' % os.getloadavg()
def blob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
src = open(SEAT, 'rb').read(); P('seat runner sha256', hashlib.sha256(src).hexdigest()[:16], 'bytes', len(src), '(READ as text, never executed)')
tree = ast.parse(src.decode())
env = {}
def ev(n):
    if isinstance(n, ast.Constant): return n.value
    if isinstance(n, ast.Name):
        if n.id in env: return env[n.id]
        raise ValueError('name ' + n.id)
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add): return ev(n.left) + ev(n.right)
    if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub): return -ev(n.operand)
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'len' and len(n.args) == 1: return len(ev(n.args[0]))
    if isinstance(n, ast.Subscript):
        base = ev(n.value); s = n.slice
        if isinstance(s, ast.Slice): return base[(ev(s.lower) if s.lower else None):(ev(s.upper) if s.upper else None)]
        return base[ev(s)]
    if isinstance(n, (ast.List, ast.Tuple)): return [ev(x) for x in n.elts] if isinstance(n, ast.List) else tuple(ev(x) for x in n.elts)
    raise ValueError('node ' + type(n).__name__)
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name in ('TOPDEL', 'TOPDEL_OFF', 'AWAIT', 'SETBLOCK', 'ROWS'):
            env[name] = ev(node.value)
SEAT_ROWS = env['ROWS']; P('seat ROWS parsed:', [(r[0], r[2], r[4]) for r in SEAT_ROWS])
HEAD_AU = open(GW + '/' + AUREL).read(); HEAD_PX = open(GW + '/' + PXREL).read(); HEAD_PF = open(GW + '/' + PFREL).read()
DEL = "      delete req.headers.authorization;\n"
PXA = "      if (req.headers.authorization) {\n        proxyReq.setHeader('Authorization', req.headers.authorization);\n      }\n"
SIG = "          headers: { 'Authorization': req.headers.authorization || '' },\n        });\n        const body = await upstream.json().catch(() => ({}));\n        return res.status(upstream.status).json(body);"
PFA = "    const auth = (req as any).rawAuthorization || req.headers.authorization;\n"
ROWS = []
for rid, edits, pred, names, t60 in SEAT_ROWS:
    ROWS.append(dict(id=rid, origin='seat', file=AUREL, edits=edits, pred=pred, form=names, t60=t60))
ROWS += [
  dict(id='X-DELETE-CASED', origin='drafter', file=AUREL, edits=[(DEL, "      delete (req.headers as Record<string, unknown>)['Authorization']; // qa1034-tamper X-DELETE-CASED\n")], pred=9, t60=True,
       form="delete the differently-cased key 'Authorization' (Node lowercases inbound names): a CONTROL that must red the 9"),
  dict(id='X-BEARER-PREFIX-ONLY', origin='drafter', file=AUREL, edits=[(DEL, "      if (req.headers.authorization?.startsWith('Bearer ')) delete req.headers.authorization; // qa1034-tamper X-BEARER-PREFIX-ONLY\n")], pred=None, t60=True,
       form="a PARTIAL strip: only an exact 'Bearer ' scheme is dropped ('bearer <jwt>', 'BEARER <jwt>', 'Basic …' stay)"),
  dict(id='X-REQUIRED-ONLY', origin='drafter', file=AUREL, edits=[(DEL, "      if (required) delete req.headers.authorization; // qa1034-tamper X-REQUIRED-ONLY\n")], pred=5, t60=True,
       form='the delete gated on required mounts only (optional mounts keep the caller header): a CONTROL'),
  dict(id='X-EMPTY-NOT-DELETE', origin='drafter', file=AUREL, edits=[(DEL, "      req.headers.authorization = ''; // qa1034-tamper X-EMPTY-NOT-DELETE\n")], pred=None, t60=True,
       form="the header set to '' instead of deleted"),
  dict(id='X-ONPROXYREQ-RAW', origin='drafter', file=PXREL, edits=[(PXA, PXA + "      if ((req as any).rawAuthorization) proxyReq.setHeader('Authorization', (req as any).rawAuthorization); // qa1034-tamper X-ONPROXYREQ-RAW\n")], pred=None, t60=True,
       form="http-proxy-middleware onProxyReq re-adds the entry-captured rawAuthorization after the connector branch dropped it"),
  dict(id='X-FETCH-RAW', origin='drafter', file=PXREL, edits=[(SIG, SIG.replace("'Authorization': req.headers.authorization || ''", "'Authorization': (req as any).rawAuthorization || req.headers.authorization || '' /* qa1034-tamper X-FETCH-RAW */"))], pred=None, t60=True,
       form="the hand-forwarded GET /api/signatories reads rawAuthorization (the platform.ts authHeaders pattern)"),
  dict(id='X-PLATFORM-NO-RAW', origin='drafter', file=PFREL, edits=[(PFA, "    const auth = req.headers.authorization; // qa1034-tamper X-PLATFORM-NO-RAW (a fix shape)\n")], pred=None, t60=True,
       form="platform.ts authHeaders stops preferring rawAuthorization (a FIX SHAPE for the register-connector forward): does any cell depend on rawAuthorization?"),
]
ONLY = set(sys.argv[1:])
DEV_AU = subprocess.run(['git', '-C', C, 'show', SHA['dev'] + ':' + GWREL + '/' + AUREL], capture_output=True).stdout
assert len(DEV_AU) > 1000
# pre-assert every anchor against HEAD bytes
for r in ROWS:
    base = {AUREL: HEAD_AU, PXREL: HEAD_PX, PFREL: HEAD_PF}[r['file']]
    if isinstance(r['edits'], list) and r['edits']:
        r['anchor_counts_head'] = [base.count(a) for a, b in r['edits']]
P('anchor pre-assert against HEAD:', [(r['id'], r.get('anchor_counts_head')) for r in ROWS])
def tsc(): return subprocess.run([WT + '/Blockchain/Dev/node_modules/typescript/bin/tsc', '--noEmit', '-p', '.'], cwd=GW, capture_output=True, text=True)
def vitest(rid, t60):
    jf = OUTD + '/%s.vitest.json' % rid; env = dict(os.environ); env.pop('NODE_ENV', None)
    p = subprocess.run(['node', WT + '/Blockchain/Dev/node_modules/vitest/vitest.mjs', 'run', '--reporter=json', '--outputFile=' + jf] + (['--testTimeout=60000', '--hookTimeout=60000'] if t60 else []), cwd=GW, capture_output=True, text=True, env=env)
    open(OUTD + '/%s.vitest.stderr' % rid, 'w').write(p.stderr)
    return p.returncode, json.load(open(jf))
table = []; T0 = None
for r in ROWS:
    if ONLY and r['id'] not in ONLY and r['id'] != 'T0': continue
    f = GW + '/' + r['file']; orig = open(f, 'rb').read(); oblob = blob(orig)
    row = {k: v for k, v in r.items() if k != 'edits'}; row['load_before'] = load(); row['t_start'] = now()
    try:
        if r['edits'] == 'WHOLEFILE':
            open(f, 'wb').write(DEV_AU); row['landed'] = blob(open(f, 'rb').read()) == blob(DEV_AU) != oblob; row['swapped_to'] = blob(DEV_AU)[:9]
        elif r['edits']:
            text = orig.decode(); counts = []
            for a, b in r['edits']:
                n = text.count(a); counts.append(n)
                if n != 1: break
                text = text.replace(a, b)
            row['anchors'] = counts
            if any(c != 1 for c in counts):
                row['VOID'] = 'anchor counts %s' % counts; table.append(row); P('ROW', json.dumps(row)); continue
            open(f, 'wb').write(text.encode())
            row['landed'] = blob(open(f, 'rb').read()) != oblob and (('qa1034-tamper' in text) or r['origin'] == 'seat')
        else:
            row['landed'] = True
        assert row['landed'], ('tamper did not land', r['id'])
        tp = tsc(); row['tsc_rc'] = tp.returncode
        if tp.returncode != 0: row['VOID'] = 'tsc rc %d' % tp.returncode; row['tsc_out'] = (tp.stdout + tp.stderr)[:400]
        t0 = time.time(); rc, j = vitest(r['id'], r['t60']); row['secs'] = round(time.time() - t0, 1); row['vitest_rc'] = rc
        row.update(files=len(j['testResults']), tests=j['numTotalTests'], pending=j['numPendingTests'])
        if r['id'] == 'T0': T0 = (row['files'], row['tests'])
        row['denominator_ok'] = (row['files'], row['tests'], row['pending']) == (T0[0], T0[1], 0) if T0 else None
        reds, other = [], []
        for s in j['testResults']:
            if s['status'] != 'passed' and not s['assertionResults']: other.append('FILE-LOAD ' + s['name'].split('/')[-1] + ': ' + (s.get('message') or '')[:160])
            for a in s['assertionResults']:
                if a['status'] == 'failed':
                    msg = (a.get('failureMessages') or [''])[0]
                    (reds if msg.startswith('AssertionError') else other).append(s['name'].split('/')[-1][:48] + ' :: ' + a['title'][:90] + ' :: ' + (msg.splitlines()[0][:120] if msg else ''))
        row['reds'] = len(reds); row['red_cells'] = reds; row['non_assertion'] = other
        row['reds_outside_ks1215'] = sum('ks1215' not in x.split(' :: ')[0] for x in reds)
        row['as_predicted'] = (r['pred'] is None) or (len(reds) == r['pred'] and not other)
    finally:
        open(f, 'wb').write(orig)
        row['restored_blob_equal'] = blob(open(f, 'rb').read()) == oblob
        row['git_diff_quiet'] = subprocess.run(['git', '-C', WT, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode == 0
        row['load_after'] = load()
    table.append(row)
    P('ROW', json.dumps({k: v for k, v in row.items() if k != 'red_cells'}))
    for x in row.get('red_cells', []): P('   RED', x)
    json.dump(table, open(OUTD + '/tamper_table.json', 'w'), indent=1)
P('porcelain at end:', repr(subprocess.run(['git', '-C', WT, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout))
P('seat rows as predicted:', [(r['id'], r.get('reds'), r.get('as_predicted')) for r in table if r['origin'] == 'seat'])
