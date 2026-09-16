#!/usr/bin/env python3
"""drafter_probe.py — place qa1008-drafter-probe.test.ts into each clone tree (base, head), run it SOLO, collect rows, then MOVE the probe
out of the tree into the drafter workdir (quarantine by rename; never rm). Porcelain asserted back to baseline."""
import sys, os, shutil, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008')
from drafterlib import *
REL = 'Blockchain/Dev/services/api-gateway/src/__tests__/qa1008-drafter-probe.test.ts'
P('drafter_probe', ts())
for t in ('base', 'head'):
    base_porc = len(porcelain(t))
    dst = T[t] + '/' + REL
    shutil.copyfile(GS + '/qa1008-drafter-probe.test.ts', dst)
    out = GS + '/probe_rows_%s.json' % t
    r = vitest('probe_' + t, t, 'gw', files=['src/__tests__/qa1008-drafter-probe.test.ts'], env_extra={'PROBE_OUT': out})
    q = W + '/_quarantine_probe_%s_%s.test.ts' % (t, datetime.datetime.now().strftime('%H%M%S'))
    os.rename(dst, q); P('   probe moved out of tree ->', q)
    assert len(porcelain(t)) == base_porc, 'porcelain did not return to baseline'
    P('   stderr tail:', (r or {}).get('stderr_tail', '')[-800:].replace('\n', ' | '))
    rows = json.load(open(out))
    for row in rows: P('  ROW', t, json.dumps(row)[:700])
P('end', ts())
