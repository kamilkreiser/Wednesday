#!/usr/bin/env python3
"""drafter_run.py — #1012 drafter: WHOLE api-gateway suite on base and head, then tamper rows on head (the seat's TU/TR/TUR shapes + the gate's own:
CONTROL-aimed, service-token forward, limit sent), project tsc rc per row (non-compiling = VOID), anchor count 1, sha-asserted restore. Never rm."""
import sys, subprocess, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1012')
from drafterlib import *
A = 'Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts'
def tsc_project(tree):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', 'services/api-gateway'], cwd=T[tree] + '/Blockchain/Dev', capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip().splitlines()[:6]
P('drafter_run', ts())
if '--rows-only' not in sys.argv:
  for t in ('base', 'head'):
    rc, _ = tsc_project(t); P('project tsc', t, 'rc', rc); vitest('gw_suite_' + t, t, 'gw')
ap = T['head'] + '/' + A; PRIS = sha(ap); base_porc = len(porcelain('head'))
URL_NEW = '`${SECURITY_SERVICE_URL}/api/audit?${queryParams.toString()}`,'
READ_NEW = 'entries = (data as any)?.data?.logs ?? (data as any)?.logs ?? [];'
ROWS = [
 ('Q_T0', []),
 ('Q_TU_url_back', [(URL_NEW, '`${SECURITY_SERVICE_URL}/api/audit/logs?${queryParams.toString()}`,')]),
 ('Q_TR_read_back', [(READ_NEW, 'entries = (data as any)?.data || (data as any)?.logs || [];')]),
 ('Q_CTL_catch_503', [("      res.status(502).json({", "      res.status(503).json({")]),
 ('Q_SVC_forwards_a_service_token', [("if (authHeader) headers['Authorization'] = authHeader;", "if (authHeader) headers['Authorization'] = 'Bearer qa-service-identity';")]),
 ('Q_NO_AUTH_forwarded', [("if (authHeader) headers['Authorization'] = authHeader;", "void authHeader;")]),
 ('Q_LIMIT_sent', [("      to: formattedTo,\n      type,\n    });", "      to: formattedTo,\n      type,\n      limit: '100000',\n    });")]),
 ('Q_ADMIN_gate_open', [("if (!adminRoles.includes(user.role)) {", "if (false && !adminRoles.includes(user.role)) {")]),
 ('Q_T0_after', []),
]
summary = []
for label, edits in ROWS:
    assert len(porcelain('head')) == base_porc
    for old, new in edits: edit(ap, old, new, markers=[(new, 1)])
    rc_tsc, tsc_lines = tsc_project('head')
    r = vitest('t_' + label, 'head', 'gw')
    if edits: restore('head', A, PRIS)
    reds = [k for k, v in (r or {}).get('cells', {}).items() if v['status'] != 'passed']
    row = {'label': label, 'tsc_rc': rc_tsc, 'tsc_head': tsc_lines, 'VOID': rc_tsc != 0, 'tests': (r or {}).get('tests'), 'failed': (r or {}).get('failed'), 'pending': (r or {}).get('pending'), 'success': (r or {}).get('success'), 'reds': reds, 'msgs': [(r['cells'][k]['msg'].split('\n')[0][:200]) for k in reds]}
    summary.append(row); P('ROW', label, 'tsc rc', rc_tsc, 'VOID' if rc_tsc else '', 'tests', row['tests'], 'failed', row['failed'], 'pending', row['pending'])
    for k, m in zip(reds, row['msgs']): P('     RED', k.split(' :: ')[-1][:120], '|', m)
json.dump(summary, open(GS + '/drafter_run_summary.json', 'w'), indent=1)
assert len(porcelain('head')) == base_porc
P('end', ts())
