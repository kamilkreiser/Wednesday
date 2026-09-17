#!/usr/bin/env python3
"""drafter_tamper_1032.py — #1032 (KS-1194) tamper table in the drafter clone's head worktree ONLY (cwd inside the clone).
The seat's 8 rows are re-derived EXACTLY from the seat's own runner (5_Project_History/2026-09-17_seatA-7th/ks1194/tamper_1194_r7.py, READ-ONLY: its ROWS
literal is parsed with ast and evaluated with only USERS + DEV_USERS bound; nothing of it is executed, its seat worktree is never entered). DEV_USERS = develop
0a2b1603f users.ts bytes from `git show` in the drafter clone. Then the drafter's X rows, aimed at what the 11 cells do not pin (the 503 wording, the log
payload, the restore target state, the response body). Each row: anchor count 1 (else VOID) + a changed sha, project tsc --noEmit -p . (rc != 0 -> VOID), the
WHOLE auth vitest at --testTimeout=60000 --hookTimeout=60000 (json), denominator asserted = T0's, reds per ks1194 cell split ASSERTION vs other, reds outside
the file, restore by bytes + sha256 + git diff --quiet HEAD. A 0-red X row gets the drafter probe run ON THE TAMPERED TREE (rows_probe_head_<row>.json)."""
import ast, json, subprocess, datetime, os, hashlib, re, sys
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1032'
SEAT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-17_seatA-7th/ks1194/tamper_1194_r7.py'
paths = json.load(open(GS + '/out/drafter_paths.json')); C = paths['C']; HT = paths['trees']['head']
DEV = 'Blockchain/Dev'; A = DEV + '/services/auth'; AD = HT + '/' + A
USERS = AD + '/src/routes/users.ts'
ONLY = set(sys.argv[1:])
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(): return subprocess.run(['uptime'], capture_output=True, text=True).stdout.split('load averages:')[-1].strip()
P('drafter_tamper_1032', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| head worktree HEAD', subprocess.run(['git', '-C', HT, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()[:9],
  '| porcelain', len(subprocess.run(['git', '-C', HT, 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines()))
DEV_USERS = subprocess.run(['git', '-C', C, 'show', '0a2b1603fe52f0f3b8152588af78bbeab0237be7:' + A + '/src/routes/users.ts'], capture_output=True).stdout
assert hashlib.sha1(b'blob %d\0' % len(DEV_USERS) + DEV_USERS).hexdigest().startswith('c723a68af')
seat_src = open(SEAT).read(); P('seat runner READ sha256', hashlib.sha256(seat_src.encode()).hexdigest()[:16], 'bytes', len(seat_src))
node = [n for n in ast.parse(seat_src).body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'ROWS'][0]
SEAT_ROWS = eval(compile(ast.Expression(node.value), 'seat-ROWS', 'eval'), {'__builtins__': {}}, {'USERS': USERS, 'DEV_USERS': DEV_USERS})
P('seat rows parsed', [(r[0], r[4]) for r in SEAT_ROWS])
ROWS = [dict(id=r[0], anchor=r[2], repl=r[3], pred=r[4], names=r[5], by='seat') for r in SEAT_ROWS]
THROW_APPROVE = "        throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');\n      }\n      logger.info('Verification request approved'"
X = [
 ('X-503-WORDING', THROW_APPROVE, "        throw new ServiceUnavailableError('Verification approve was not applied: the level update matched no row'); // QA-TAMPER\n      }\n      logger.info('Verification request approved'", 0, 'the approve 503 message asserts the forbidden stronger cause (helper docblock / F-929-2 wording)', ['A-UPD-ZERO', 'A-READBACK-INFRA']),
 ('X-SAVE-INFRA-AS-500', "    if (isInfrastructureDbError(err)) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');\n    throw err;\n  }\n  memVerificationRequests.set(req.id, req);", "    throw err; // QA-TAMPER\n  }\n  memVerificationRequests.set(req.id, req);", 3, 'an infrastructure save failure answers 500 instead of 503', ['S-INFRA']),
 ('X-LOG-NOUSERID', "            { requestId, userId: request.userId, error: restoreErr?.message },\n", "            { requestId }, // QA-TAMPER\n", 0, 'the double-failure log keeps requestId only (no userId, no cause)', ['A-DOUBLE']),
 ('X-LOG-RAISE-DROPPED', "        logger.error('Verification approve: raising the verification level failed', { requestId, userId: request.userId, error: err?.message });\n", "        void err; // QA-TAMPER\n", 0, 'the raise-failure log (the only line naming the request on a single failure) removed', ['A-UPD-INFRA', 'A-READBACK-INFRA']),
 ('X-RESTORE-KEEP-REVIEWEDAT', "          await saveVerificationRequest({ ...request, status: 'PENDING', reviewedAt: undefined, reviewedBy: undefined });\n", "          await saveVerificationRequest({ ...approved, status: 'PENDING', reviewedBy: undefined }); // QA-TAMPER\n", 0, 'the restored PENDING row keeps the approval reviewed_at', ['A-UPD-ZERO']),
 ('X-RESTORE-REJECTED', "          await saveVerificationRequest({ ...request, status: 'PENDING', reviewedAt: undefined, reviewedBy: undefined });\n", "          await saveVerificationRequest({ ...request, status: 'REJECTED', reviewedAt: undefined, reviewedBy: undefined }); // QA-TAMPER\n", 2, 'the restore target is REJECTED instead of PENDING', ['A-UPD-ZERO']),
 ('X-APPROVE-BODY-STALE', "      res.json({ success: true, message: 'Verification approved', data: approved });\n", "      res.json({ success: true, message: 'Verification approved', data: request }); // QA-TAMPER\n", 0, 'the 200 approve body carries the looked-up PENDING object', ['A-OK']),
 ('X-REJECT-BODY-STALE', "      res.json({ success: true, message: 'Verification rejected', data: rejected });\n", "      res.json({ success: true, message: 'Verification rejected', data: request }); // QA-TAMPER\n", 0, 'the 200 reject body carries the looked-up PENDING object', ['R-OK']),
]
for x in X: ROWS.append(dict(id=x[0], anchor=x[1], repl=x[2], pred=x[3], names=x[4], by='drafter', probe=x[5]))
orig = open(USERS, 'rb').read(); s0 = sha(USERS)
T0 = {}; table = []
for row in ROWS:
    if ONLY and row['id'] not in ONLY: continue
    rid = row['id']; t0 = now(); out = dict(id=rid, by=row['by'], pred=row['pred'], names=row['names'])
    if row['anchor'] == 'WHOLEFILE':
        open(USERS, 'wb').write(row['repl']); out['form'] = 'whole-file develop bytes'
    elif row['anchor'] is not None:
        n = orig.decode().count(row['anchor']); out['anchor_count'] = n
        if n != 1:
            out['VOID'] = 'anchor count %d' % n; table.append(out); P('ROW', rid, 'VOID anchor count', n); continue
        open(USERS, 'wb').write(orig.decode().replace(row['anchor'], row['repl']).encode()); out['form'] = 'anchored edit'
    out['changed'] = sha(USERS) != s0 if row['anchor'] is not None else 'n/a'
    try:
        tsc = subprocess.run([HT + '/' + DEV + '/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=AD, capture_output=True, text=True)
        out['tsc'] = tsc.returncode; out['tsc_tail'] = (tsc.stdout + tsc.stderr).strip()[:200]
        out['load'] = load(); jf = GS + '/out/tamper/%s.vitest.json' % rid; os.makedirs(GS + '/out/tamper', exist_ok=True)
        with open(GS + '/out/tamper/%s.vitest.stderr' % rid, 'w') as fe:
            subprocess.run([HT + '/' + DEV + '/node_modules/.bin/vitest', 'run', '--testTimeout=60000', '--hookTimeout=60000', '--reporter=json', '--outputFile=' + jf], cwd=AD, stdout=subprocess.PIPE, stderr=fe, text=True, env=dict(os.environ, CI='1'))
        j = json.load(open(jf)); out['den'] = (len(j['testResults']), j['numTotalTests'], j['numPendingTests'])
        if rid == 'T0': T0['den'] = out['den']
        out['den_eq_T0'] = out['den'] == T0.get('den')
        reds, other, outside = [], [], []
        for f in j['testResults']:
            if f['status'] != 'passed' and not f['assertionResults']: other.append('FILE-LOAD ' + f['name'].split('/')[-1])
            for a in f['assertionResults']:
                if a['status'] != 'failed': continue
                m = (a.get('failureMessages') or [''])[0]
                if 'ks1194' in f['name']:
                    (reds if m.startswith('AssertionError') else other).append(a['title'][:70] + ('' if m.startswith('AssertionError') else ' :: ' + m.splitlines()[0][:80]))
                else: outside.append(f['name'].split('/')[-1] + ' :: ' + a['title'][:50] + ' :: ' + m.splitlines()[0][:60] if m else '')
        out.update(reds=len(reds), red_cells=reds, other=other, outside=outside)
        if out['tsc'] != 0: out['VOID'] = 'tsc rc %d' % out['tsc']
        out['as_predicted'] = out['reds'] == row['pred'] and not other and not outside and out['den_eq_T0'] and 'VOID' not in out
        if row['by'] == 'drafter' and out['reds'] == 0 and 'VOID' not in out:
            pr = subprocess.run(['python3', GS + '/drafter_probe_1032.py', '_' + rid, 'head'], capture_output=True, text=True)
            open(GS + '/out/tamper/%s.probe.out' % rid, 'w').write(pr.stdout + pr.stderr)
            try:
                rs = {r['id']: r for r in json.load(open(GS + '/out/rows_probe_head_%s.json' % rid))}
                out['probe'] = {k: dict(status=rs[k]['status'], message=rs[k]['message'], dataStatus=rs[k]['dataStatus'], row=rs[k]['requestRow'], level=rs[k]['level'],
                                        errorLogs=[(l['msg'][:70], l['keys'], l['requestId']) for l in rs[k]['errorLogs'] if l['msg'] != 'Error occurred']) for k in row['probe']}
            except Exception as e:
                out['probe'] = 'unreadable %s' % type(e).__name__
    finally:
        open(USERS, 'wb').write(orig)
        out['restored'] = sha(USERS) == s0
        out['diff_quiet'] = subprocess.run(['git', '-C', HT, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode
    table.append(out)
    P('ROW', rid, '(%s)' % row['by'], t0, '->', now(), '| tsc', out.get('tsc'), '| den', out.get('den'), 'eq T0', out.get('den_eq_T0'), '| ks1194 reds', out.get('reds'), 'pred', row['pred'], 'AS PREDICTED' if out.get('as_predicted') else 'NOT AS PREDICTED',
      '| other', out.get('other'), '| outside', out.get('outside'), '| restored', out['restored'], 'diff --quiet', out['diff_quiet'], '| load', out.get('load'))
    for c in out.get('red_cells', []): P('     RED', c)
    if 'probe' in out: P('     PROBE ON TAMPERED TREE', json.dumps(out['probe'], ensure_ascii=False)[:900])
json.dump(table, open(GS + '/out/tamper_rows%s.json' % ('_' + '_'.join(sorted(ONLY)) if ONLY else ''), 'w'), indent=1, ensure_ascii=False)
P('seat rows as predicted', sum(1 for r in table if r['by'] == 'seat' and r.get('as_predicted')), '/', sum(1 for r in table if r['by'] == 'seat'),
  '| drafter rows as predicted', sum(1 for r in table if r['by'] == 'drafter' and r.get('as_predicted')), '/', sum(1 for r in table if r['by'] == 'drafter'),
  '| head worktree porcelain after', len(subprocess.run(['git', '-C', HT, 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines()), '| end', now())
