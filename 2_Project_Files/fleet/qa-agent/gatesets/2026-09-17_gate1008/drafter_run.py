#!/usr/bin/env python3
"""drafter_run.py — tamper rows on the head tree of the drafter's --shared clone. Each row: porcelain asserted, anchor count 1 (str.count),
markers asserted, WHOLE api-gateway suite (JSON: numFailed / numPending / numFailedTestSuites / success), git checkout restore with sha256
asserted. Nothing outside the clone is written except vt_t_*.json and this script's stdout."""
import sys, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008')
from drafterlib import *
REL = 'Blockchain/Dev/services/api-gateway/src/routes/verification.ts'
F = T['head'] + '/' + REL
PRISTINE = sha(F); P('drafter_run', ts(), 'verification.ts head sha256', PRISTINE)
BASE_PORC = porcelain('head'); P('porcelain baseline', len(BASE_PORC))
CHECK = """        if (forwardStatus < 200 || forwardStatus >= 300) {
          res.status(502).json({ success: false, error: { code: 'ORIGINATE_FORWARD_FAILED', message: 'Approved, but the document could not be created in originate; the pending document was kept', status: forwardStatus } });
          return;
        }
"""
DEL = "        await redisService.deletePendingDocument(documentId);\n      }\n\n      res.json({\n        success: true,\n        instanceId: req.params.id,\n        status: 'approved',"
DEL_LINE = "        await redisService.deletePendingDocument(documentId);\n"
ROWS = [
 ('T0', None),
 ('S1_status_check_removed', [(CHECK, '', [('ORIGINATE_FORWARD_FAILED', 0)])]),
 ('S2_delete_moved_before_check', [(CHECK + DEL_LINE, DEL_LINE + CHECK, [('ORIGINATE_FORWARD_FAILED', 1)])]),
 ('S3_delete_removed', [(CHECK + DEL_LINE, CHECK, [('deletePendingDocument(documentId);', 1)])]),
 ('G1_CONTROL_AIM_4xx_counts_as_success', [('if (forwardStatus < 200 || forwardStatus >= 300) {', 'if (forwardStatus < 200 || forwardStatus >= 500) {', [('forwardStatus >= 500', 1)])]),
 ('G2_CONTROL_AIM_every_response_is_failure', [('resolveStatus(proxyRes.statusCode || 0);', 'resolveStatus(0);', [('resolveStatus(0);', 2)])]),
 ('G3_transport_error_counts_as_success', [("          resolveStatus(0);\n", "          resolveStatus(201);\n", [('resolveStatus(201);', 1)])]),
 ('G4_3xx_counts_as_success', [('if (forwardStatus < 200 || forwardStatus >= 300) {', 'if (forwardStatus < 200 || forwardStatus >= 400) {', [('forwardStatus >= 400', 1)])]),
 ('G5_resolve_on_end_not_headers', [("              resolveStatus(proxyRes.statusCode || 0);\n", '', []), ("              log('info', 'Workflow approved — document forwarded to originate', { documentId });\n", "              log('info', 'Workflow approved — document forwarded to originate', { documentId });\n              resolveStatus(proxyRes.statusCode || 0);\n", [('resolveStatus(proxyRes.statusCode || 0);', 1)])]),
 ('G6_502_body_echoes_originate_body', [("            proxyRes.on('end', () => {\n", "            proxyRes.on('end', () => {\n              (res as any).__qaBody = body;\n", []), ("status: forwardStatus } });", "status: forwardStatus, upstream: (res as any).__qaBody } });", [('upstream:', 1)])]),
 ('G7_inert_comment', [('        if (forwardStatus < 200 || forwardStatus >= 300) {', '        // qa inert comment\n        if (forwardStatus < 200 || forwardStatus >= 300) {', [('// qa inert comment', 1)])]),
 ('T0_after', None),
]
summary = []
for label, edits in ROWS:
    P('==', label, ts())
    assert porcelain('head') == BASE_PORC, 'porcelain moved before ' + label
    assert sha(F) == PRISTINE
    if edits:
        for old, new, markers in edits: edit(F, old, new, markers)
    r = vitest('t_' + label, 'head', 'gw')
    reds = sorted(k for k, v in r['cells'].items() if v['status'] == 'failed') if r else ['NO JSON']
    skipped = sorted(k for k, v in r['cells'].items() if v['status'] not in ('passed', 'failed')) if r else []
    summary.append({'row': label, 'rc': r and r['rc'], 'tests': r and r['tests'], 'passed': r and r['passed'], 'failed': r and r['failed'], 'pending': r and r['pending'], 'failed_suites': r and r['failed_suites'], 'success': r and r['success'], 'reds': [x[:200] for x in reds], 'skipped': skipped, 'first_msgs': [r['cells'][k]['msg'].split('\n')[0][:200] for k in reds] if r else []})
    if edits: restore('head', REL, PRISTINE)
assert porcelain('head') == BASE_PORC
json.dump(summary, open(GS + '/drafter_run_summary.json', 'w'), indent=1)
for s in summary: P('SUMMARY', s['row'], 'rc', s['rc'], 'tests', s['tests'], 'passed', s['passed'], 'failed', s['failed'], 'pending', s['pending'], 'failed_suites', s['failed_suites'], 'success', s['success'], '| reds', [x.split(' :: ')[-1][:90] for x in s['reds']], '| msgs', s['first_msgs'])
P('end', ts())
