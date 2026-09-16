#!/usr/bin/env python3
"""drafter_suites.py — #1011 (KS-871) drafter: whole api-gateway suite on base d067725ff and head 0a1f8900c (merged tree = head tree:
develop d067725ff is the head's parent, api-gateway tree hash identical — asserted in drafter_setup.out); service tsc -p . rc and an
INCLUDING program (extends ./tsconfig.json, include src/**/*; placed for the run, moved out by rename) base vs head, NEW/GONE by full
diagnostic line and the error lines in the three touched files; eslint on the three head files; and the GATE'S OWN three tamper rows on
head (anchor count 1, tsc rc per row, WHOLE suite, denominator asserted, restore sha-asserted). Predictions FIXED here before the run."""
import sys, os, json, re, subprocess
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1011')
from drafterlib import *
GWR = 'Blockchain/Dev/services/api-gateway'; AUD = GWR + '/src/middleware/audit.ts'
TOUCHED = ('middleware/audit.ts', 'ks871-audit-path-captured-at-entry', 'ks871-the-audit-log-records-req-path')
INC = '{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}\n'
os.makedirs(W + '/_quarantine', exist_ok=True)
def tsc_p(tree):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=T[tree] + '/' + GWR, capture_output=True, text=True); return p.returncode, p.stdout + p.stderr
def including(tree):
    cfg = T[tree] + '/' + GWR + '/tsconfig.qa-including.json'; open(cfg, 'w').write(INC)
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', 'tsconfig.qa-including.json'], cwd=T[tree] + '/' + GWR, capture_output=True, text=True)
    os.rename(cfg, W + '/_quarantine/tsconfig.qa-including.%s.%d.json' % (tree, len(os.listdir(W + '/_quarantine'))))
    return p.returncode, p.stdout + p.stderr
def porc(tree): return [l for l in porcelain(tree) if not l.rstrip('/').endswith('node_modules')]
P('drafter_suites start', ts())
S = {}
for t in ('base', 'head'):
    assert porc(t) == [], porc(t)
    S[t] = vitest('gw_suite_' + t, t, 'gw')
    rc, o = tsc_p(t); P('   tsc -p . tree', t, 'rc', rc, 'error lines', o.count('error TS'))
E = {}
for t in ('base', 'head'):
    rc, o = including(t); lines = [l for l in o.splitlines() if 'error TS' in l]; E[t] = lines
    open(GS + '/tsc_including_%s.out' % t, 'w').write(o)
    P('including tsc tree', t, 'rc', rc, 'error lines', len(lines), '| in touched files', len([l for l in lines if any(x in l for x in TOUCHED)]), '| files with errors', len({l.split('(')[0] for l in lines}))
new = [l for l in E['head'] if l not in E['base']]; gone = [l for l in E['base'] if l not in E['head']]
P('including base -> head: NEW %d GONE %d' % (len(new), len(gone))); [P('   +', l[:170]) for l in new]; [P('   -', l[:170]) for l in gone]
p = subprocess.run([T['head'] + '/Blockchain/Dev/node_modules/.bin/eslint', '-f', 'json', *[T['head'] + '/' + GWR + '/src/' + f for f in ('middleware/audit.ts', '__tests__/ks871-audit-path-captured-at-entry.test.ts', '__tests__/ks871-the-audit-log-records-req-path.test.ts')]], cwd=T['head'] + '/Blockchain/Dev', capture_output=True, text=True)
try:
    for f in json.loads(p.stdout): P('eslint head', f['filePath'].split('/src/')[-1], 'errors', f['errorCount'], 'warnings', f['warningCount'])
except Exception: P('eslint NO JSON rc', p.returncode, p.stderr[-400:])
DEN = (S['head']['files'], S['head']['tests']); P('denominator head', DEN, '| base', (S['base']['files'], S['base']['tests']))
def cell(sub):
    m = [k for k in S['head']['cells'] if sub(k)]; assert len(m) == 1, m; return m[0]
A_RED = cell(lambda k: 'ks871-audit-path-captured' in k and 'full path, not the trimmed' in k)
A_CTL = cell(lambda k: 'ks871-audit-path-captured' in k and 'CONTROL' in k)
PATHLINE = "            path: auditPath, // KS-871: was req.path, the trimmed remainder for a refused request\n"
SECTION = "  const section = segments[1] || 'unknown';\n"
ROWS = [
 ('G_CTRL_admitted_path_wrong', [(AUD, PATHLINE, "            path: res.statusCode < 400 ? '/qa-tampered' : auditPath,\n", [('qa-tampered', 1)])], {A_CTL}),
 ('G_NONGDPR_logs_action_renamed', [(AUD, SECTION, "  const section = segments[1] === 'logs' ? 'qa-logs' : (segments[1] || 'unknown');\n", [('qa-logs', 1)])], set()),
 ('G_ADMITTED_ONLY_path', [(AUD, PATHLINE, "            path: res.statusCode < 400 ? auditPath : req.path,\n", [('? auditPath : req.path', 1)])], {A_RED}),
]
pristine = sha(T['head'] + '/' + AUD)
summary = []
for label, edits, predicted in ROWS:
    P('== ROW', label, ts(), '| PREDICTED reds', len(predicted), sorted(x.split(' :: ')[-1][:70] for x in predicted))
    assert porc('head') == [], porc('head')
    for f, old, new, markers in edits: edit(T['head'] + '/' + f, old, new, markers)
    trc, _ = tsc_p('head')
    r = vitest('t_' + label, 'head', 'gw')
    reds = set(k for k, v in r['cells'].items() if v['status'] != 'passed')
    den = (r['files'], r['tests'])
    P('   tsc rc', trc, '| denominator', den, 'asserted', den == DEN, '| failed', r['failed'], 'pending', r['pending'], '| reds', len(reds), '| MATCHES PREDICTION', reds == predicted)
    restore('head', AUD, pristine)
    summary.append(dict(row=label, tsc_rc=trc, den=den, den_ok=den == DEN, failed=r['failed'], pending=r['pending'], reds=sorted(reds), predicted=sorted(predicted), match=reds == predicted))
json.dump(summary, open(GS + '/drafter_suites_summary.json', 'w'), indent=1, ensure_ascii=False)
P('porcelain head', porc('head'), 'base', porc('base'))
P('drafter_suites end', ts())
