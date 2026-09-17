#!/usr/bin/env python3
"""drafter_tamper.py [ROW ...] — #1019 ROUND 2 drafter tamper table on the HEAD tree (82f09c8bd) of the drafter's own clone. The seat's 8 rows re-derived in the
seat's EXACT forms (tamper_r2.py, read only) + the drafter's G rows the seat did not write. Per row: anchor count == 1 (else VOID), marker (sha changed), project
`tsc --noEmit -p .` rc (non-zero = VOID), the WHOLE api-gateway suite (denominator asserted 55 / 524, pending 0; 0-cell or load failure = INVALID), reds classified
AssertionError vs other, restore by bytes (sha256 equal) + `git diff --quiet HEAD`. T0 before and after. Rows -> tamper_rows.json; raw vitest JSON -> workdir."""
import hashlib, json, os, subprocess, sys, datetime
GSD = os.path.dirname(os.path.abspath(__file__))
PA = json.load(open(GSD + '/drafter_paths.json')); W = PA['W']; WT = PA['trees']['head']
GW = WT + '/Blockchain/Dev/services/api-gateway'; PX = GW + '/src/routes/proxy.ts'; SV = GW + '/src/config/services.ts'
BIN = WT + '/Blockchain/Dev/node_modules/.bin/'
DOT = "        if (namesDoor(segments[0])) return { verdict: 'undetermined', canonicalPath: null };\n"
CS = "const erasureDoorCaseSensitive = Boolean((erasureDoor as unknown as { caseSensitive?: boolean }).caseSensitive);"
ROWS = [
 ('T0', None, None, None, 0, 'seat', 'no edit'),
 ('QWFIX', PX, DOT, '', 24, 'seat', 'the fix removed'),
 ('GHARDFALSE', PX, CS, CS.replace('Boolean((erasureDoor', 'Boolean(false && (erasureDoor'), 1, 'seat', 'F-1019-2 router cell'),
 ('GNORESTORE', PX, '      req.url = original;\n', '      req.url = req.url || original;\n', 2, 'seat', 'F-1019-3 cell + ks843 source pin'),
 ('GONLYDOTDOT', PX, DOT, DOT.replace('if (namesDoor', "if (segment === '..' && namesDoor"), 1, 'seat', 'verdict /erasures/.'),
 ('GCASEFOLD', PX, DOT, "        if (typeof segments[0] === 'string' && segments[0].toLowerCase() === 'erasures') return { verdict: 'undetermined', canonicalPath: null };\n", 2, 'seat', 'verdict case-rule + F-1019-2 router cell'),
 ('GWIDE', PX, DOT, "        if (segment === '.' || segment === '..') return { verdict: 'undetermined', canonicalPath: null };\n", 7, 'seat', 'Tightening-A dot controls + F-1019-2 router cell'),
 ('TI', PX, '  const namesDoor = (segment: string | null | undefined): boolean =>\n', '  // tamper TI: inert comment\n  const namesDoor = (segment: string | null | undefined): boolean =>\n', 0, 'seat', 'inert'),
 # drafter rows the seat did not write
 ('G-READOUTER', PX, CS, CS.replace('(erasureDoor as unknown as', '(router as unknown as'), 0, 'drafter', 'the case rule read from the FACTORY router, not the door router: the doMock makes every Router case-sensitive, so predicted invisible'),
 ('G-HARDTRUE', PX, CS, CS.replace('Boolean((erasureDoor', 'Boolean(true || (erasureDoor'), 3, 'drafter', 'round-1 form: ks1187 real-app upper case + ks843-path-bypass F-9 ENFORCING + GRACE'),
 ('G-RESTORE-UNDONE', PX, '      req.url = original;\n      next(err as Error | undefined);\n', '      req.url = original;\n      if (!err) req.url = canonicalPath as string;\n      next(err as Error | undefined);\n', 1, 'drafter', 'the restore line kept (ks843 text pin green), then undone: only the F-1019-3 behavioural cell can see it'),
 ('G-RESTORE-PARAMS', PX, '      req.url = original;\n', "      req.url = original.replace(/;[^/?]*/g, '');\n", 1, 'drafter', 'a restore wrong only for ;param spellings: the F-1019-3 cell sends %65rasures (no ;), predicted green; the ks843 text pin reds'),
 ('G-NODETECT', SV, '    /(\\.\\.\\/)/, // Path traversal\n', '    /(\\.\\.\\/)(?!)/, // Path traversal (QA tamper: never matches)\n', None, 'drafter', 'security.ts suspicious-path detector neutered for ../ (Q4: is the ordering load-bearing?)'),
 ('T0-after', None, None, None, 0, 'seat', 'no edit, after'),
]
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def P(*a): print(' '.join(str(x) for x in a), flush=True)
ONLY = set(sys.argv[1:])
P('drafter_tamper', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| tree', WT, '| HEAD', subprocess.run(['git', '-C', WT, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip())
out = []
for rid, path, anchor, repl, pred, by, names in ROWS:
    if ONLY and rid not in ONLY: continue
    row = dict(id=rid, predicted=pred, predicted_by=by, names=names)
    por = subprocess.run(['git', '-C', WT, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout
    row['porcelain_before'] = len(por.splitlines())
    orig = open(path, 'rb').read() if path else None; osha = sha(path) if path else None
    if anchor is not None:
        n = orig.decode().count(anchor); row['anchor_count'] = n
        if n != 1: row['VOID'] = 'anchor count %d' % n; out.append(row); P(json.dumps(row)); continue
        open(path, 'wb').write(orig.decode().replace(anchor, repl).encode()); row['marker'] = sha(path) != osha
    try:
        p = subprocess.run([BIN + 'tsc', '--noEmit', '-p', '.'], cwd=GW, capture_output=True, text=True); row['tsc_rc'] = p.returncode
        if p.returncode: row['tsc_head'] = (p.stdout + p.stderr)[:400]
        jf = W + '/tamper_%s.json' % rid; env = dict(os.environ); env.pop('NODE_ENV', None)
        v = subprocess.run([BIN + 'vitest', 'run', '--reporter=json', '--outputFile=' + jf], cwd=GW, capture_output=True, text=True, env=env)
        open(W + '/tamper_%s.stderr.txt' % rid, 'w').write(v.stderr)
        d = json.load(open(jf))
        row.update(files=len(d['testResults']), tests=d['numTotalTests'], failed=d['numFailedTests'], pending=d['numPendingTests'])
        row['denominator_ok'] = (row['files'], row['tests']) == (55, 524) and row['pending'] == 0
        reds, other = [], []
        for f in d['testResults']:
            if f['status'] != 'passed' and not f['assertionResults']: other.append('FILE-LOAD ' + f['name'].split('/')[-1] + ': ' + (f.get('message') or '')[:160])
            for t in f['assertionResults']:
                if t['status'] == 'failed':
                    msg = (t.get('failureMessages') or [''])[0]; item = f['name'].split('/')[-1] + ' :: ' + t['title'][:150]
                    (reds if msg.startswith('AssertionError') else other).append(item + ('' if msg.startswith('AssertionError') else ' :: ' + msg.splitlines()[0][:160]))
        row['reds'] = len(reds); row['red_cells'] = reds; row['non_assertion'] = other
        row['as_predicted'] = (pred is None) or (len(reds) == pred and not other)
        row['VALID'] = row['tests'] > 0 and row['tsc_rc'] == 0
    finally:
        if path:
            open(path, 'wb').write(orig); row['restored_sha_equal'] = sha(path) == osha
        row['git_diff_quiet'] = subprocess.run(['git', '-C', WT, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode == 0
    out.append(row)
    P(ts(), json.dumps({k: v for k, v in row.items() if k != 'red_cells'}))
    for r in row.get('red_cells', []): P('   RED', r)
json.dump(out, open(GSD + '/tamper_rows%s.json' % ('' if not ONLY else '_' + '_'.join(sorted(ONLY))), 'w'), indent=1)
P('ALL AS PREDICTED (rows with a prediction):', all(r.get('as_predicted') for r in out if r.get('predicted') is not None), '| end', ts())
