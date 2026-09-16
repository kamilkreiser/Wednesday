#!/usr/bin/env python3
"""drafter_run.py — #1013 (KS-999) tamper rows on the HEAD tree, WHOLE auth suite per row, project tsc rc per row, anchors str.count == 1,
sha-asserted restore via git checkout in the scratch clone, porcelain asserted. Seat rows T0/TA/TL/TC/TI/T0after (the seat's anchors) + drafter rows."""
import sys, subprocess, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1013')
from drafterlib import *
UR = 'Blockchain/Dev/services/auth/src/repositories/userRepo.ts'
EH = 'Blockchain/Dev/services/auth/src/middleware/errorHandler.ts'
AWAIT = "    if (result.rows.length > 0) return await fromRow(result.rows[0]); // KS-999: await so the catch classifies infra failures inside fromRow\n"
LOGC = "    logger.error('DB getUserById failed', { error: err?.message, code: err?.code });\n    if (isInfrastructureDbError(err)) {\n"
DEK = "  const dek = needsDek ? await subjectDeks.getDek(row.id) : null;\n"
E503 = "    super(message, 503, 'SERVICE_UNAVAILABLE');\n"
ROWS = [
 ('T0', 'seat', UR, []),
 ('TA', 'seat: await removed', UR, [(AWAIT, "    if (result.rows.length > 0) return fromRow(result.rows[0]); // TA tamper\n")]),
 ('TL', 'seat: catch no longer logs', UR, [(LOGC, "    if (isInfrastructureDbError(err)) {\n")]),
 ('TC', 'seat: classifier disabled', UR, [(LOGC, "    logger.error('DB getUserById failed', { error: err?.message, code: err?.code });\n    if (false && isInfrastructureDbError(err)) {\n")]),
 ('TI', 'seat: inert comment', UR, [(AWAIT, AWAIT.rstrip('\n') + ' // inert tamper\n')]),
 ('Q-SWALLOW', 'drafter: awaits but swallows a fromRow failure (returns null)', UR, [(AWAIT, "    if (result.rows.length > 0) return await fromRow(result.rows[0]).catch(() => null); // Q-SWALLOW\n")]),
 ('Q-500', 'drafter: maps any fromRow failure to a plain Error (a 500)', UR, [(AWAIT, "    if (result.rows.length > 0) return await fromRow(result.rows[0]).catch(() => { throw new Error('QA subject key read failed'); }); // Q-500\n")]),
 ('Q-CTL-NODEK', 'drafter CONTROL-aimed: fromRow never reads the DEK', UR, [(DEK, "  const dek = needsDek && false ? await subjectDeks.getDek(row.id) : null;\n")]),
 ('Q-DECRYPT-503', 'drafter: a decrypt (plaintext cutoff) failure classified as 503', UR, [(LOGC, "    logger.error('DB getUserById failed', { error: err?.message, code: err?.code });\n    if (isInfrastructureDbError(err) || /migration incomplete/.test(String(err?.message))) {\n")]),
 ('Q-LOG-LEAK', 'drafter: the catch logs the stack and the user id', UR, [(LOGC, "    logger.error('DB getUserById failed', { error: err?.message, code: err?.code, stack: err?.stack, userId: id });\n    if (isInfrastructureDbError(err)) {\n")]),
 ('Q-EH-503-AS-500', 'drafter caller-side: ServiceUnavailableError answers 500', EH, [(E503, "    super(message, 500, 'SERVICE_UNAVAILABLE');\n")]),
 ('T0after', 'seat', UR, []),
]
tp = T['head']
# first run died on its own marker assertion AFTER landing TL (outside the try) -> restore both files from the clone before anything
for rel0 in (UR, EH): subprocess.run(['git', '-C', tp, 'checkout', '--', rel0], check=True)
for rid, d, rel, edits in ROWS:
    s = open(tp + '/' + rel).read()
    for a, _ in edits:
        assert s.count(a) == 1, '%s anchor count %d' % (rid, s.count(a))
P('drafter_run start', ts(), 'anchors all count 1; porcelain', porcelain('head'))
summary = []
for rid, d, rel, edits in ROWS:
    path = tp + '/' + rel; pristine = sha(path); s = open(path).read()
    for a, r in edits: s = s.replace(a, r, 1)
    try:
        if edits:
            open(path, 'w').write(s); assert sha(path) != pristine
            for a, r in edits: assert open(path).read().count(r) >= 1 and open(path).read().count(a) == (1 if a in r else 0), 'MARKER'
        P('\n' + ts(), rid, '|', d, '| landed' if edits else '| no edit')
        rc_tsc, out_tsc = tsc_project('head')
        P('   project tsc rc', rc_tsc, out_tsc.strip()[-400:])
        r = vitest('t_' + rid, 'head', 'auth')
    finally:
        subprocess.run(['git', '-C', tp, 'checkout', '--', rel], check=True)
        assert sha(path) == pristine, 'RESTORE FAILED'
    P('   restored sha-identical; porcelain', porcelain('head'))
    reds = [k for k, v in (r or {}).get('cells', {}).items() if v['status'] == 'failed']
    summary.append({'row': rid, 'desc': d, 'tsc_rc': rc_tsc, 'VOID': rc_tsc != 0, 'cells_run': r and r['tests'] - (r['pending'] or 0), 'tests': r and r['tests'], 'failed': r and r['failed'], 'pending': r and r['pending'], 'success': r and r['success'], 'reds': reds})
json.dump(summary, open(GS + '/drafter_run_summary.json', 'w'), indent=1)
P('drafter_run end', ts())
