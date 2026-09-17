#!/usr/bin/env python3
"""drafter_tamper_1032r2.py [row ...] — #1032 ROUND 2 (KS-1194) tamper table in the drafter clone's head worktree ONLY (cwd inside the clone).
From ../2026-09-17_gate1032/drafter_tamper_1032.py, re-pinned. The seat's 11 rows are re-derived EXACTLY from the seat's own runner
(5_Project_History/2026-09-17_seatA-7th/ks1194-r2/tamper_1194_r2.py, READ-ONLY: its module-level string constants and its ROWS literal are parsed with ast
and evaluated with no builtins; nothing of it is executed; its seat worktree is never entered). DEV_BYTES = the round-1 users.ts at 5d55a72bd from
`git show` in the drafter clone (= the seat's DEV). Then the drafter's X2 rows on the NEW branches plus controls. Each row: anchor count 1 (else VOID), a
changed sha, project tsc --noEmit -p . (rc != 0 -> VOID), the WHOLE auth vitest (json; 60 s ceilings unless the row says default), denominator asserted =
T0's, reds split ASSERTION vs other and inside vs outside the two ks1194 files, restore by bytes + sha256 + git diff --quiet HEAD. A 0-red drafter row gets
the round-2 branches probe run ON THE TAMPERED TREE (out/rows_tamper-<row>_head_test.json) and the named rows are quoted."""
import ast, json, subprocess, datetime, os, hashlib, sys
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1032r2'
SEAT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-17_seatA-7th/ks1194-r2/tamper_1194_r2.py'
paths = json.load(open(GS + '/out/drafter_paths.json')); C = paths['C']; HT = paths['trees']['head']
DEV = 'Blockchain/Dev'; A = DEV + '/services/auth'; AD = HT + '/' + A
USERS = AD + '/src/routes/users.ts'
ONLY = set(sys.argv[1:])
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(): return subprocess.run(['uptime'], capture_output=True, text=True).stdout.split('load averages:')[-1].strip()
P('drafter_tamper_1032r2', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| head worktree HEAD', subprocess.run(['git', '-C', HT, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()[:9],
  '| porcelain', len(subprocess.run(['git', '-C', HT, 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines()))
DEV_BYTES = subprocess.run(['git', '-C', C, 'show', '5d55a72bd59dcac88a9b5bc59c9c387bfcbc1540:' + A + '/src/routes/users.ts'], capture_output=True).stdout
assert hashlib.sha1(b'blob %d\0' % len(DEV_BYTES) + DEV_BYTES).hexdigest().startswith('8299a2558')
seat_src = open(SEAT).read(); P('seat runner READ sha256', hashlib.sha256(seat_src.encode()).hexdigest()[:16], 'bytes', len(seat_src))
env = {}
for n in ast.parse(seat_src).body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ('READ', 'TARGETIF', 'UNREAD_THROW', 'CTX', 'CATCH', 'SWALLOW_A', 'MEMFIRST_A'):
        env[n.targets[0].id] = eval(compile(ast.Expression(n.value), 'seat-const', 'eval'), {'__builtins__': {}}, dict(env))
node = [n for n in ast.parse(seat_src).body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'ROWS'][0]
SEAT_ROWS = eval(compile(ast.Expression(node.value), 'seat-ROWS', 'eval'), {'__builtins__': {}}, env)
P('seat constants parsed', sorted(env), '| seat rows parsed', [(r[0], r[2], r[4]) for r in SEAT_ROWS], '| predicted reds total', sum(r[2] for r in SEAT_ROWS))
ROWS = [dict(id=r[0], edits=r[1], pred=r[2], names=r[3], t60=r[4], by='seat') for r in SEAT_ROWS]
# ---- drafter rows (anchors asserted count 1 against the head bytes before any run) ----
OTHER_THROW = "          throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');\n        } else {\n"
OTHER_LOG = "'Verification approve: the level update could not be confirmed and the level does not read the target level; restoring the request to PENDING',\n            { ...logCtx, levelNow, error: cause },\n"
RESTORE_CATCH = "          } catch (restoreErr: any) {\n            logger.error(\n              'Verification approve: the request could not be restored to PENDING; it may read APPROVED while the level does not read the target level',\n              { ...logCtx, levelNow, error: restoreErr?.message },\n            );\n          }\n"
TARGET_WARN = "          logger.warn(\n            'Verification approve: the level update could not be confirmed, but the level reads the target level; the approval stands',\n            { ...logCtx, levelNow, error: cause },\n          );\n"
TARGETIF = env['TARGETIF']; UNREAD_THROW = env['UNREAD_THROW']
X = [
 # on the NEW branches
 ('X2-OTHER-503-FORBIDDEN-CAUSE', [(OTHER_THROW, "          throw new ServiceUnavailableError('Verification approve was not applied: the level was not raised'); // QA-TAMPER\n        } else {\n")], 0, 'the other-level 503 asserts the stronger cause the helper docblock forbids', ['O-UPD-ZERO', 'O-READBACK-POOLTIMEOUT-REREAD-STALE']),
 ('X2-UNREADABLE-GENERIC-WORDING', [(UNREAD_THROW, "          throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry'); // QA-TAMPER\n")], 1, 'the unreadable 503 loses the "could not be confirmed" wording: the unreadable cell', None),
 ('X2-TARGET-ANSWERS-503', [(TARGET_WARN, TARGET_WARN + "          throw new ServiceUnavailableError('Verification approval could not be confirmed. Please retry — if you already succeeded, you may not need to.'); // QA-TAMPER\n")], 1, 'a target-level read keeps APPROVED but answers 503: landed-unconfirmed', None),
 ('X2-TARGET-WARN-DROPPED', [(TARGET_WARN, "          void cause; // QA-TAMPER\n")], 1, 'no line names the request when the approval stands: log-truth', None),
 ('X2-OTHER-NO-THROW', [(OTHER_THROW, "        } else { // QA-TAMPER no throw\n")], 2, 'other-level restores PENDING then falls through to 200 APPROVED: zero-row (r2) + null (r1 file)', None),
 ('X2-ANY-READABLE-STANDS', [(TARGETIF, "        if (levelNow !== null) { // QA-TAMPER\n")], 3, 'any readable level is treated as the target (no restore): zero-row, r1 null / throw cells', None),
 ('X2-OTHER-LOG-NO-LEVELNOW', [(OTHER_LOG, "'Verification approve: the level update could not be confirmed and the level does not read the target level; restoring the request to PENDING',\n            { ...logCtx, error: cause }, // QA-TAMPER\n")], 0, 'the other-level line loses the level it read (levelNow)', ['O-UPD-ZERO']),
 ('X2-RESTORE-LINE-DROPPED', [(RESTORE_CATCH, "          } catch (restoreErr: any) {\n            void restoreErr; // QA-TAMPER\n          }\n")], 1, 'residual (i) leaves no line: the reworded r1 double-failure cell', None),
 ('X2-UNREADABLE-NOTLANDED-RESTORES-WHEN-PREAUTH', [(UNREAD_THROW, "          if (raiseError && /timeout exceeded/.test(raiseError)) await saveVerificationRequest({ ...request, status: 'PENDING', reviewedAt: undefined, reviewedBy: undefined }); // QA-TAMPER\n" + UNREAD_THROW)], 0, 'a guessed restore when the RAISE itself timed out (no cell drives a failed pre-auth or UPDATE with an unreadable level)', ['U-NOTLANDED-PREAUTH-POOLTIMEOUT-REREAD-POOLTIMEOUT', 'U-LANDED-READBACK-POOLTIMEOUT-REREAD-POOLTIMEOUT']),
 # DRAFTER v2 (01:2x): the row above is INERT on the probe shapes (getUserByIdPreAuth / getUserById convert the pool error to ServiceUnavailableError, so raiseError never
 # matches /timeout exceeded/); kept as run, and this corrected form added: restore PENDING whenever the raise THREW and the level is unreadable.
 ('X2-UNREADABLE-RESTORES-ON-RAISE-ERROR', [(UNREAD_THROW, "          if (raiseError !== undefined) await saveVerificationRequest({ ...request, status: 'PENDING', reviewedAt: undefined, reviewedBy: undefined }); // QA-TAMPER\n" + UNREAD_THROW)], 1, 'the unreadable branch restores PENDING whenever the raise threw: the unreadable cell (landed + unreadable = F-1 again)', ['U-LANDED-READBACK-POOLTIMEOUT-REREAD-POOLTIMEOUT', 'U-NOTLANDED-PREAUTH-POOLTIMEOUT-REREAD-POOLTIMEOUT']),
 # carried from round 1 (still unpinned?)
 ('X-APPROVE-BODY-STALE', [("      res.json({ success: true, message: 'Verification approved', data: approved });\n", "      res.json({ success: true, message: 'Verification approved', data: request }); // QA-TAMPER\n")], 0, '(round-1 drafter row) the 200 approve body carries the looked-up PENDING object', ['B-OK']),
 # controls
 ('XC-APPROVED-SAVE-DROPPED', [("      await saveVerificationRequest(approved);\n", "      // QA-TAMPER control: the APPROVED save removed\n")], 4, 'CONTROL: the healthy approve never saves APPROVED (reds expected in both files)', None),
 ('XC-TI', [(TARGETIF, "        // QA-TAMPER control: inert\n" + TARGETIF)], 0, 'CONTROL: inert comment on the new branch', None),
]
head_text = open(USERS).read()
for x in X:
    for a, b in x[1]: assert head_text.count(a) == 1, (x[0], head_text.count(a))
    ROWS.append(dict(id=x[0], edits=x[1], pred=x[2], names=x[3], t60=True, by='drafter', probe=x[4]))
orig = open(USERS, 'rb').read(); s0 = sha(USERS)
T0 = {}; table = []
for row in ROWS:
    if ONLY and row['id'] not in ONLY and row['id'] != 'T0': continue
    rid = row['id']; t0 = now(); out = dict(id=rid, by=row['by'], pred=row['pred'], names=row['names'], t60=row['t60'])
    if row['edits'] == 'WHOLEFILE':
        open(USERS, 'wb').write(DEV_BYTES); out['form'] = 'whole-file round-1 bytes (5d55a72bd)'
    elif row['edits']:
        text = orig.decode(); counts = []
        for a, b in row['edits']:
            counts.append(text.count(a))
            if counts[-1] != 1: break
            text = text.replace(a, b)
        out['anchor_counts'] = counts
        if any(c != 1 for c in counts):
            out['VOID'] = 'anchor counts %s' % counts; table.append(out); P('ROW', rid, 'VOID anchor counts', counts); continue
        open(USERS, 'wb').write(text.encode()); out['form'] = 'anchored edit'
    out['changed'] = sha(USERS) != s0
    try:
        tsc = subprocess.run([HT + '/' + DEV + '/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=AD, capture_output=True, text=True)
        out['tsc'] = tsc.returncode; out['tsc_tail'] = (tsc.stdout + tsc.stderr).strip()[:200]
        out['load'] = load(); jf = GS + '/out/tamper/%s.vitest.json' % rid; os.makedirs(GS + '/out/tamper', exist_ok=True)
        with open(GS + '/out/tamper/%s.vitest.stderr' % rid, 'w') as fe:
            subprocess.run([HT + '/' + DEV + '/node_modules/.bin/vitest', 'run'] + (['--testTimeout=60000', '--hookTimeout=60000'] if row['t60'] else []) + ['--reporter=json', '--outputFile=' + jf], cwd=AD, stdout=subprocess.PIPE, stderr=fe, text=True, env=dict(os.environ, CI='1'))
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
                    (reds if m.startswith('AssertionError') else other).append(('r2 ' if 'raised-level' in f['name'] else 'r1 ') + a['title'][:80] + ('' if m.startswith('AssertionError') else ' :: ' + m.splitlines()[0][:80]))
                else: outside.append(f['name'].split('/')[-1] + ' :: ' + a['title'][:50] + ' :: ' + (m.splitlines()[0][:60] if m else ''))
        out.update(reds=len(reds), red_cells=reds, other=other, outside=outside)
        if out['tsc'] != 0: out['VOID'] = 'tsc rc %d' % out['tsc']
        out['as_predicted'] = out['reds'] == row['pred'] and not other and not outside and out['den_eq_T0'] and 'VOID' not in out
        if row['by'] == 'drafter' and out['reds'] == 0 and row.get('probe') and 'VOID' not in out:
            tag = 'tamper-' + rid
            pr = subprocess.run(['python3', GS + '/drafter_probe_1032r2.py', 'qa1032r2-drafter-probe.template.ts', tag, 'test', 'head'], capture_output=True, text=True)
            open(GS + '/out/tamper/%s.probe.out' % rid, 'w').write(pr.stdout + pr.stderr)
            try:
                rs = {r['id']: r for r in json.load(open(GS + '/out/rows_%s_head_test.json' % tag))['rows']}
                out['probe'] = {k: dict(status=rs[k]['status'], message=rs[k]['message'], row=(rs[k]['requestRow'] or {}).get('status'), level=rs[k]['level'],
                                        errorLines=[(l['msg'][:80], l['keys']) for l in rs[k]['errorLines']]) for k in row['probe']}
            except Exception as e:
                out['probe'] = 'unreadable %s %s' % (type(e).__name__, str(e)[:100])
    finally:
        open(USERS, 'wb').write(orig)
        out['restored'] = sha(USERS) == s0
        out['diff_quiet'] = subprocess.run(['git', '-C', HT, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode
    table.append(out)
    P('ROW', rid, '(%s)' % row['by'], t0, '->', now(), '| tsc', out.get('tsc'), '| den', out.get('den'), 'eq T0', out.get('den_eq_T0'), '| ks1194 reds', out.get('reds'), 'pred', row['pred'], 'AS PREDICTED' if out.get('as_predicted') else 'NOT AS PREDICTED',
      '| other', out.get('other'), '| outside', out.get('outside'), '| restored', out['restored'], 'diff --quiet', out['diff_quiet'], '| load', out.get('load'))
    for c in out.get('red_cells', []): P('     RED', c)
    if 'probe' in out: P('     PROBE ON TAMPERED TREE', json.dumps(out['probe'], ensure_ascii=False)[:1200])
json.dump(table, open(GS + '/out/tamper_rows%s.json' % ('_' + '_'.join(sorted(ONLY)) if ONLY else ''), 'w'), indent=1, ensure_ascii=False)
P('seat rows as predicted', sum(1 for r in table if r['by'] == 'seat' and r.get('as_predicted')), '/', sum(1 for r in table if r['by'] == 'seat'), '| seat reds', sum(r.get('reds', 0) for r in table if r['by'] == 'seat'),
  '| drafter rows as predicted', sum(1 for r in table if r['by'] == 'drafter' and r.get('as_predicted')), '/', sum(1 for r in table if r['by'] == 'drafter'),
  '| head worktree porcelain after', len(subprocess.run(['git', '-C', HT, 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines()), '| end', now())
