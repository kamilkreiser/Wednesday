#!/usr/bin/env python3
"""drafter_sample.py — #1011 ROUND 2 drafter SAMPLE on the head tree of the drafter's own clone (PREDICTIONS for the gate, not its measurements).
Rows: T0 whole api-gateway suite (denominator); on the real-app file ks871-real-app-canonical-audit-rows.test.ts alone: F0 none, R1 (round-1 source
restored in audit.ts), NORESET (vi.resetModules() removed from bootApp), NOPRODENV (stubEnv NODE_ENV production removed); a WITNESS probe = a copy of
the real-app file that also records whether each response carries X-CSRF-Token (set only when index.ts was EVALUATED with NODE_ENV != test,
index.ts:387) — run as-is and with vi.resetModules() removed. Anchored edits (count 1, markers), project tsc rc per product row, restore sha-identical,
probe files quarantined by rename. Never rm."""
import sys, os, json, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafterlib import *
G = T['head']; GWD = G + '/' + PKG['gw']; AUD = GWD + '/src/middleware/audit.ts'; RA = GWD + '/src/__tests__/ks871-real-app-canonical-audit-rows.test.ts'
RA_REL = PKG['gw'] + '/src/__tests__/ks871-real-app-canonical-audit-rows.test.ts'; AUD_REL = PKG['gw'] + '/src/middleware/audit.ts'
def tsc():
    p = subprocess.run([G + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=GWD, capture_output=True, text=True); return p.returncode, (p.stdout + p.stderr)[:300]
P('drafter_sample start', ts(), 'porcelain', porcelain('head'))
pa, pr = sha(AUD), sha(RA); P('pristine audit.ts', pa[:12], 'real-app', pr[:12])
rows = []
def row(name, files, pred):
    rc, out = tsc(); r = vitest('r2_' + name, 'head', 'gw', files=files)
    rows.append(dict(row=name, tsc_rc=rc, files=r['files'], tests=r['tests'], failed=r['failed'], pending=r['pending'], predicted=pred,
                     reds=[(k.split(' :: ')[-1][:90], v['msg'].split('\n')[0][:160]) for k, v in r['cells'].items() if v['status'] == 'failed']))
    P('ROW', json.dumps(rows[-1])[:900])
row('T0_whole_suite', (), 'seat: 50 files / 417 pass')
F = ('src/__tests__/ks871-real-app-canonical-audit-rows.test.ts',)
row('F0_realapp', F, 'seat: 3/3 green')
edit(AUD, "    const auditPath = req.path;\n", "    const auditPath = req.originalUrl.split('?')[0];\n", [("req.originalUrl.split('?')[0]", 1)])
edit(AUD, "  const segments = path.replace(/\\/+$/, '').split('/').filter(Boolean);\n", "  const segments = req.originalUrl.split('?')[0].replace(/\\/+$/, '').split('/').filter(Boolean); void path;\n", [("req.originalUrl.split('?')[0]", 2)])
row('R1_round1_source', F, 'seat R1: 2 red (v1 logs, production erasure)')
restore('head', AUD_REL, pa)
edit(RA, "  vi.resetModules();\n", "  /* QA-DRAFTER-NORESET */\n", [('QA-DRAFTER-NORESET', 1), ('vi.resetModules', 0)])
row('NORESET_realapp', F, 'drafter: 0 red — the 307 is request-time (versioning.ts:47) so nothing pins that index.ts re-evaluated under production')
restore('head', RA_REL, pr)
edit(RA, "    vi.stubEnv('NODE_ENV', 'production');\n", "    /* QA-DRAFTER-NOPRODENV */\n", [('QA-DRAFTER-NOPRODENV', 1), ("'NODE_ENV'", 0)])
row('NOPRODENV_realapp', F, 'drafter: 1 red (the 307 assertion)')
restore('head', RA_REL, pr)
# WITNESS probe: copy of the real-app file; post() also returns whether X-CSRF-Token is present; each production/test response appended to a JSON file.
s = open(RA).read(); OUT = W + '/witness_%s.json'
def mk(tag, noreset):
    t = s
    old = "(res) => { res.resume(); res.on('end', () => resolve({ status: res.statusCode ?? 0, location: res.headers.location })); },"
    assert t.count(old) == 1
    t = t.replace(old, "(res) => { res.resume(); res.on('end', () => { require('fs').appendFileSync(process.env.QA_WITNESS as string, JSON.stringify({ path, ua: headers['user-agent'], status: res.statusCode, csrfHeader: res.headers['x-csrf-token'] !== undefined, nodeEnvAtRequest: process.env.NODE_ENV }) + '\\n'); resolve({ status: res.statusCode ?? 0, location: res.headers.location }); }); },")
    if noreset:
        assert t.count("  vi.resetModules();\n") == 1; t = t.replace("  vi.resetModules();\n", "  /* QA-DRAFTER-NORESET */\n")
    p = GWD + '/src/__tests__/qa1011r2-drafter-witness-%s.test.ts' % tag; open(p, 'w').write(t); return p
for tag, nr in (('reset', False), ('noreset', True)):
    p = mk(tag, nr); wf = OUT % tag; open(wf, 'w').close()
    r = vitest('r2_WITNESS_' + tag, 'head', 'gw', files=('src/__tests__/' + os.path.basename(p),), env_extra={'QA_WITNESS': wf})
    lines = [json.loads(x) for x in open(wf).read().splitlines() if x.strip()]
    P('WITNESS', tag, 'failed', r['failed'], 'tests', r['tests']); [P('   ', x) for x in lines]
    rows.append(dict(row='WITNESS_' + tag, failed=r['failed'], tests=r['tests'], responses=lines))
    os.makedirs(W + '/_quarantine', exist_ok=True); os.rename(p, W + '/_quarantine/' + os.path.basename(p))
json.dump(rows, open(GS + '/drafter_sample_rows.json', 'w'), indent=1)
P('porcelain end', porcelain('head'), '| audit sha', sha(AUD)[:12], '| real-app sha', sha(RA)[:12])
P('drafter_sample end', ts())
