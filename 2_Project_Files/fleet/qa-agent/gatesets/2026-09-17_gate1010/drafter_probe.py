#!/usr/bin/env python3
"""drafter_probe.py — place qa1010-drafter-probe.test.ts into each clone tree, run it SOLO, collect rows, MOVE it out (quarantine by rename; never rm). Porcelain asserted back to baseline."""
import sys, os, shutil, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1010')
from drafterlib import *
REL = 'Blockchain/Dev/services/api-gateway/src/__tests__/qa1010-drafter-probe.test.ts'
P('drafter_probe', ts())
for t in sys.argv[1:]:
    base_porc = len(porcelain(t)); dst = T[t] + '/' + REL
    shutil.copyfile(GS + '/qa1010-drafter-probe.test.ts', dst)
    out = GS + '/probe_rows_%s.json' % t
    r = vitest('probe_' + t, t, 'gw', files=['src/__tests__/qa1010-drafter-probe.test.ts'], env_extra={'PROBE_OUT': out, 'PROBE_TREE': t, 'PROBE_DEFAULT': '1' if t == 'head' else '0'})
    q = W + '/_quarantine_probe_%s_%s.test.ts' % (t, datetime.datetime.now().strftime('%H%M%S'))
    os.rename(dst, q); P('   probe moved out of tree ->', q)
    assert len(porcelain(t)) == base_porc, 'porcelain did not return to baseline'
    P('   stderr tail:', (r or {}).get('stderr_tail', '')[-600:].replace('\n', ' | '))
    for row in json.load(open(out)):
        c = row.pop('censusAfter', None); P('  ROW', json.dumps(row)[:900]); P('     census', c)
P('end', ts())
