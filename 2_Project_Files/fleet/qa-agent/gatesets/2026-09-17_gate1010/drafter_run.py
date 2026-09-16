#!/usr/bin/env python3
"""drafter_run.py — #1010 drafter tamper rows (gate's OWN, beyond the seat's T0-T11) on the WHOLE api-gateway suite at head, project tsc rc per row
(a non-compiling tamper is VOID), anchor count 1, sha-asserted restore; then the INCLUDING tsc program on base / head / merged (inclusion by --listFilesOnly,
planted positive control on head). Config placed for the run and moved out by rename. Never rm."""
import sys, os, subprocess, json, re
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1010')
from drafterlib import *
V = 'Blockchain/Dev/services/api-gateway/src/routes/verification.ts'
K = 'Blockchain/Dev/services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts'
def tsc_project(tree):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', 'services/api-gateway'], cwd=T[tree] + '/Blockchain/Dev', capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip().splitlines()[:6]
P('drafter_run', ts())
vp = T['head'] + '/' + V; VPRIS = sha(vp); P('head verification.ts sha256', VPRIS[:16]); base_porc = len(porcelain('head'))
ROWS = [
 ('Q_T0', []),
 ('Q_CTL_201_counts_as_failure', [('if (forwardStatus < 200 || forwardStatus >= 300) {', 'if (forwardStatus < 200 || forwardStatus >= 201) {')]),
 ('Q_LATE_bound_fires_1400ms_late', [('proxyReq.setTimeout(originateForwardTimeoutMs, () => {', 'proxyReq.setTimeout(originateForwardTimeoutMs + 1_400, () => {')]),
 ('Q_LATE_bound_fires_1600ms_late', [('proxyReq.setTimeout(originateForwardTimeoutMs, () => {', 'proxyReq.setTimeout(originateForwardTimeoutMs + 1_600, () => {')]),
 ('Q_LATE_default_16s', [('export const ORIGINATE_FORWARD_TIMEOUT_MS = 15_000;', 'export const ORIGINATE_FORWARD_TIMEOUT_MS = 16_000;')]),
 ('Q_LATE_default_29999', [('export const ORIGINATE_FORWARD_TIMEOUT_MS = 15_000;', 'export const ORIGINATE_FORWARD_TIMEOUT_MS = 29_999;')]),
 ('Q_DEFAULT_destructure_0', [('originateForwardTimeoutMs = ORIGINATE_FORWARD_TIMEOUT_MS,', 'originateForwardTimeoutMs = 0,')]),
 ('Q_DELETE_on_timeout', [('          proxyReq.setTimeout(originateForwardTimeoutMs, () => {\n', '          proxyReq.setTimeout(originateForwardTimeoutMs, () => {\n            void redisService.deletePendingDocument(documentId);\n')]),
 ('Q_ERROR_listener_resolves_201', [("proxyRes.on('error', () => resolveStatus(0));", "proxyRes.on('error', () => resolveStatus(201));")]),
 ('Q_T0_after', []),
]
summary = []
for label, edits in ROWS:
    assert len(porcelain('head')) == base_porc
    for old, new in edits: edit(vp, old, new, markers=[(new, 1)])
    rc_tsc, tsc_lines = tsc_project('head')
    r = vitest('t_' + label, 'head', 'gw')
    if edits: restore('head', V, VPRIS)
    reds = [k for k, v in (r or {}).get('cells', {}).items() if v['status'] != 'passed']
    row = {'label': label, 'tsc_rc': rc_tsc, 'tsc_head': tsc_lines, 'VOID': rc_tsc != 0, 'tests': (r or {}).get('tests'), 'failed': (r or {}).get('failed'), 'pending': (r or {}).get('pending'), 'success': (r or {}).get('success'), 'reds': reds, 'msgs': [(r['cells'][k]['msg'].split('\n')[0][:200]) for k in reds]}
    summary.append(row); P('ROW', label, 'tsc rc', rc_tsc, 'VOID' if rc_tsc else '', 'tests', row['tests'], 'failed', row['failed'], 'pending', row['pending'])
    for k, m in zip(reds, row['msgs']): P('     RED', k.split(' :: ')[-1][:120], '|', m)
json.dump(summary, open(GS + '/drafter_run_summary.json', 'w'), indent=1)
P('--- including tsc', ts())
CFG = {"extends": "./tsconfig.json", "compilerOptions": {"noEmit": True}, "include": ["src/**/*.ts"], "exclude": []}
def including(tree, tag):
    d = T[tree] + '/Blockchain/Dev/services/api-gateway'; cfg = d + '/tsconfig.qa-including.json'
    open(cfg, 'w').write(json.dumps(CFG))
    tscb = T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc'
    lf = subprocess.run([tscb, '-p', 'tsconfig.qa-including.json', '--listFilesOnly'], cwd=d, capture_output=True, text=True).stdout.splitlines()
    p = subprocess.run([tscb, '-p', 'tsconfig.qa-including.json'], cwd=d, capture_output=True, text=True)
    os.rename(cfg, W + '/_quarantine_including_%s_%s.json' % (tag, datetime.datetime.now().strftime('%H%M%S%f')))
    lines = [l for l in (p.stdout + p.stderr).splitlines() if re.search(r'error TS\d+', l)]
    open(GS + '/tsc_including_%s.out' % tag, 'w').write(p.stdout + p.stderr)
    nt = sum(1 for l in lf if '/src/__tests__/' in l and '/node_modules/' not in l); ks = sum(1 for l in lf if 'ks1087-workflow' in l)
    by = {}
    for l in lines:
        f = l.split('(')[0].split('/')[-1]; by[f] = by.get(f, 0) + 1
    P('INCLUDING', tag, 'rc', p.returncode, 'error lines', len(lines), '__tests__ files listed', nt, 'ks1087 listed', ks, 'by file', by)
    return set(re.sub(r'\(\d+,\d+\)', '', l) for l in lines), lines
sb, lb = including('base', 'base'); sh, lh = including('head', 'head'); sm, lm = including('merged', 'merged')
P('NEW head vs base (line-number-free):', sorted(sh - sb)); P('GONE head vs base:', sorted(sb - sh))
P('NEW merged vs head:', sorted(sm - sh))
kp = T['head'] + '/' + K; KPRIS = sha(kp)
edit(kp, "const DOC_ID = 'doc-ks1087';", "const DOC_ID = 'doc-ks1087';\nfunction qaPlant(): void { const QA_UNUSED_PLANT = 1; }", markers=[('QA_UNUSED_PLANT', 1)])
sp, lp = including('head', 'head_planted'); restore('head', K, KPRIS)
P('positive control NEW lines:', [l for l in lp if 'ks1087' in l])
assert len(porcelain('head')) == base_porc
P('end', ts())
