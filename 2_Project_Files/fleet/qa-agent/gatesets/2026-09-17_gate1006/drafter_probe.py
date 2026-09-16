#!/usr/bin/env python3
"""drafter_probe.py — place qa1006-drafter-probe.test.ts in each tree's demo-service __tests__, run it SOLO, move it out by rename
(quarantine, never rm), assert porcelain back to baseline. Rows -> probe_rows_<tree>.json; then a base-vs-head table."""
import sys, os, json, shutil
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1006')
from drafterlib import *
REL = 'Blockchain/Dev/services/demo-service/src/__tests__/qa1006-drafter-probe.test.ts'
Q = W + '/_quarantine'; os.makedirs(Q, exist_ok=True)
P('drafter_probe start', ts())
for t in ('base', 'head'):
    before = porcelain(t)
    dst = T[t] + '/' + REL; shutil.copyfile(GS + '/qa1006-drafter-probe.test.ts', dst)
    out = GS + '/probe_rows_%s.json' % t
    r = vitest('probe_' + t, t, 'demo', files=['src/__tests__/qa1006-drafter-probe.test.ts'], env_extra={'QA_OUT': out})
    os.rename(dst, Q + '/qa1006-drafter-probe.%s.test.ts' % t)
    after = porcelain(t); P('porcelain restored', t, after == before)
rows = {t: json.load(open(GS + '/probe_rows_%s.json' % t)) for t in ('base', 'head')}
def key(r): return (r['id'], r['env'])
bi = {key(r): r for r in rows['base']}
P('\n== E/K rows: base (develop 40fe4db69, no handler) -> head (86fe59e6b)')
for r in rows['head']:
    if not r['id'][0] in 'EK': continue
    b = bi.get(key(r), {})
    P('%-62s %-11s | base %s %-28s html=%s stack=%s path=%s | head %s %-31s html=%s stack=%s path=%s csp=%s | head body: %s' % (
        r['id'][:62], r['env'], b.get('status'), str(b.get('ctype'))[:28], b.get('html'), b.get('stack'), b.get('abs_path'),
        r['status'], str(r['ctype'])[:31], r['html'], r['stack'], r['abs_path'], str(r['csp'])[:24], r['body_head'][:150].replace('\n', ' ')))
P('\n== H rows (head tree): express finalhandler vs the exported errorHandler, synthetic errors')
for r in rows['head']:
    if r['id'][0] != 'H': continue
    P('%-58s %-11s | %s %-31s | html=%s stack=%s | allow=%s | body: %s' % (r['id'][:58], r['env'], r['status'], str(r['ctype'])[:31], r['html'], r['stack'], 'allow' in r['header_names'], r['body_head'][:120].replace('\n', ' ')))
P('drafter_probe end', ts())
