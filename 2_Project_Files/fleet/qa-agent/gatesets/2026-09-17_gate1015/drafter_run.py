#!/usr/bin/env python3
"""drafter_run.py — #1015 (KS-1018) tamper rows on the HEAD tree (scratch clone), WHOLE auth suite per row, project tsc rc per row, every anchor
str.count == 1 asserted, the replacement asserted present, sha-asserted restore via git checkout in the scratch clone, porcelain asserted.
Seat rows T0/T1/T2/T3/TL/TW/TK/TI use the seat's own anchors (a15-ks1018/tamper1018.py); D-* rows are the drafter's."""
import sys, subprocess, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1015')
from drafterlib import *
US = 'Blockchain/Dev/services/auth/src/routes/users.ts'
EH = 'Blockchain/Dev/services/auth/src/middleware/errorHandler.ts'
RT = "      if (isInfrastructureDbError(err)) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');\n"
def log(fn, extra=''): return "      logger.error('DB %s failed', { error: err?.message, code: err?.code%s });\n" % (fn, extra)
GET, FIND, LIST = 'getVerificationRequest', 'findPendingVerificationRequest', 'listUserVerificationRequests'
WIDE = "      if (err) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');\n"
NARROW = "      if (isInfrastructureDbError(err) && err?.code) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');\n"
ROWS = [
 ('T0', 'seat: none', US, []),
 ('T1', 'seat: getVerificationRequest rethrow removed', US, [(log(GET) + RT, log(GET))]),
 ('T2', 'seat: findPendingVerificationRequest rethrow removed', US, [(log(FIND) + RT, log(FIND))]),
 ('T3', 'seat: listUserVerificationRequests rethrow removed', US, [(log(LIST) + RT, log(LIST))]),
 ('TL', 'seat: list log line removed', US, [(log(LIST), '')]),
 ('TW', 'seat: list rethrow widened to every error', US, [(log(LIST) + RT, log(LIST) + WIDE)]),
 ('TK', 'seat: userId added to the list log meta', US, [(log(LIST), log(LIST, ', userId'))]),
 ('TI', 'seat: inert comment', US, [(log(GET), '      // inert tamper\n' + log(GET))]),
 ('D-TW-GET', 'drafter: getVerificationRequest rethrow widened to every error (review has no non-infra control)', US, [(log(GET) + RT, log(GET) + WIDE)]),
 ('D-TW-FIND', 'drafter: findPending rethrow widened to every error', US, [(log(FIND) + RT, log(FIND) + WIDE)]),
 ('D-TL-GET', 'drafter: getVerificationRequest log line removed', US, [(log(GET), '')]),
 ('D-TK-FIND', 'drafter: userId added to the findPending log meta', US, [(log(FIND), log(FIND, ', userId'))]),
 ('D-NARROW', 'drafter: all three rethrows narrowed to errors that carry a code (message-form pool timeouts fall through)', US, [(log(f) + RT, log(f) + NARROW) for f in (GET, FIND, LIST)]),
 ('D-CTL-NOMEM', 'drafter CONTROL-aimed: a non-infra error no longer falls through to the in-memory map (return null / [] from the catch)', US,
   [(log(GET) + RT, log(GET) + RT + '      return null;\n'), (log(FIND) + RT, log(FIND) + RT + '      return null;\n'), (log(LIST) + RT, log(LIST) + RT + '      return [];\n')]),
 ('D-CF-POST', 'drafter caller fail-open: POST /me/verification maps the pending-read error to no pending request', US,
   [("    const existingRequest = await findPendingVerificationRequest(user.id);\n", "    const existingRequest = await findPendingVerificationRequest(user.id).catch(() => null);\n")]),
 ('D-CF-LIST', 'drafter caller fail-open: GET /me/verification maps the list-read error to an empty list', US,
   [("    const requests = await listUserVerificationRequests(user.id);\n", "    const requests = await listUserVerificationRequests(user.id).catch(() => [] as never[]);\n")]),
 ('D-CF-REVIEW', 'drafter caller fail-open: review maps the get-read error to not found', US,
   [("    const request = await getVerificationRequest(requestId);\n", "    const request = await getVerificationRequest(requestId).catch(() => null);\n")]),
 ('D-EH-503-AS-500', 'drafter caller side: ServiceUnavailableError answers 500', EH, [("    super(message, 503, 'SERVICE_UNAVAILABLE');\n", "    super(message, 500, 'SERVICE_UNAVAILABLE');\n")]),
 ('T0-after', 'seat: none', US, []),
]
tp = T['head']
for rid, d, rel, edits in ROWS:
    s = open(tp + '/' + rel).read()
    for a, _ in edits: assert s.count(a) == 1, '%s anchor count %d' % (rid, s.count(a))
P('drafter_run start', ts(), 'anchors all count 1; porcelain', porcelain('head'))
summary = []
for rid, d, rel, edits in ROWS:
    path = tp + '/' + rel; pristine = sha(path); s = open(path).read()
    for a, r in edits:
        s = s.replace(a, r, 1)
    rc_tsc, r = None, None
    try:
        if edits:
            open(path, 'w').write(s); assert sha(path) != pristine, 'NOT LANDED'
            now = open(path).read()
            for a, r_ in edits:
                if r_: assert r_ in now, 'MARKER ABSENT ' + rid
            P('\n' + ts(), rid, '|', d, '| landed (sha changed, every replacement present)')
        else:
            P('\n' + ts(), rid, '|', d, '| no edit')
        rc_tsc, out_tsc = tsc_project('head')
        P('   project tsc rc', rc_tsc, out_tsc.strip()[-400:])
        r = vitest('t_' + rid, 'head', 'auth')
    finally:
        subprocess.run(['git', '-C', tp, 'checkout', '--', rel], check=True)
        assert sha(path) == pristine, 'RESTORE FAILED'
    P('   restored sha-identical; porcelain', porcelain('head'))
    reds = [k for k, v in (r or {}).get('cells', {}).items() if v['status'] == 'failed']
    summary.append({'row': rid, 'desc': d, 'tsc_rc': rc_tsc, 'VOID': rc_tsc != 0, 'cells_run': r and r['tests'] - (r['pending'] or 0), 'tests': r and r['tests'], 'failed': r and r['failed'], 'pending': r and r['pending'], 'failed_suites': r and r['failed_suites'], 'success': r and r['success'], 'reds': reds})
json.dump(summary, open(GS + '/drafter_run_summary.json', 'w'), indent=1)
P('\nSUMMARY')
for x in summary: P('%-16s tsc %s VOID %s tests %s run %s failed %s pending %s' % (x['row'], x['tsc_rc'], x['VOID'], x['tests'], x['cells_run'], x['failed'], x['pending']))
P('drafter_run end', ts())
