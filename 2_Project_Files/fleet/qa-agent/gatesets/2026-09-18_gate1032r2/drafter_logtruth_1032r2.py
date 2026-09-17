#!/usr/bin/env python3
"""drafter_logtruth_1032r2.py — F-2 over the branches probe rows (head / r1 / dev, NODE_ENV test): every product error/warn line on the approve path
('Verification approve…'): does it carry requestId, userId, targetLevel? count of lines matching the three round-1 false strings; approve rows at head
whose failure left NO line naming the request. Control: the same scan on r1 must find the round-1 strings."""
import json, re
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1032r2'
FALSE = re.compile(r'raising the verification level failed|was not raised|at an unchanged level', re.I)
for t in ('head', 'r1', 'dev'):
    rows = [r for r in json.load(open('%s/out/rows_branches_%s_test.json' % (GS, t)))['rows'] if r.get('kind') == 'approve']
    lines = [(r['id'], l) for r in rows for l in r['errorLines'] + r['warnLines'] if l['msg'].startswith('Verification approve')]
    missing = [(rid, l['msg'][:60], l['keys']) for rid, l in lines if not all(k in l['keys'] for k in ('requestId', 'userId', 'targetLevel'))]
    false = sorted({(rid, l['msg'][:70]) for rid, l in lines if FALSE.search(l['msg'])})
    silent = [r['id'] for r in rows if r['status'] != 200 and r['code'] and not any(l['msg'].startswith('Verification approve') and l.get('requestId') for l in r['errorLines'] + r['warnLines']) and not r['id'].startswith('C-')]
    print('%s: approve rows %d | approve lines %d | lines missing one of requestId/userId/targetLevel %d %s | lines with a round-1 false string %d %s | non-200 level-path rows with no line naming the request %d %s'
          % (t, len(rows), len(lines), len(missing), missing[:3], len(false), false[:3], len(silent), silent))
