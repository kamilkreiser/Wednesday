#!/usr/bin/env python3
"""drafter_probe_1032.py [tag trees...] — place src/qa1032-drafter-probe.template.ts OUTSIDE services/auth at <tree>/Blockchain/Dev/qa_probe_1032/ (every mock /
import path ABSOLUTE via __AUTH__), with a scratch vitest config beside it (root = the probe dir, include = the probe only, auth's vitest.setup.ts and the
@secuura/shared/utils/logger alias as absolute paths), run it on develop and head, write rows_probe_<tree>.json, print develop vs head per row.
Then PROVE the probe is outside both auth collectors: `vitest list` from auth lists 0 qa_probe (control: the ks1194 test listed at head) and
`tsc -p . --listFilesOnly` lists 0 qa_probe (control: routes/users.ts listed). cwd inside the clone only; never rm."""
import json, subprocess, datetime, os, sys, hashlib
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1032'
paths = json.load(open(GS + '/out/drafter_paths.json'))
DEV = 'Blockchain/Dev'; A = DEV + '/services/auth'
TAG = sys.argv[1] if len(sys.argv) > 1 else ''
TREES = sys.argv[2:] or ['dev', 'head']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
tpl = open(GS + '/src/qa1032-drafter-probe.template.ts').read()
P('drafter_probe_1032', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| template sha256', hashlib.sha256(tpl.encode()).hexdigest()[:16], '| __AUTH__ occurrences', tpl.count('__AUTH__'))
rows = {}
for name in TREES:
    tree = paths['trees'][name]; auth = tree + '/' + A; pd = tree + '/' + DEV + '/qa_probe_1032'
    os.makedirs(pd, exist_ok=True)
    src = tpl.replace('__AUTH__', auth); assert '__AUTH__' not in src
    open(pd + '/qa1032-drafter-probe.test.ts', 'w').write(src)
    cfg = pd + '/vitest.qa1032.config.mts'
    open(cfg, 'w').write("import { defineConfig } from 'vitest/config';\nexport default defineConfig({\n  root: %r,\n  resolve: { alias: { '@secuura/shared/utils/logger': %r } },\n  test: { globals: true, environment: 'node', include: ['qa1032-drafter-probe.test.ts'], setupFiles: [%r] },\n});\n"
                         % (pd, tree + '/' + DEV + '/packages/shared/dist/utils/logger.js', auth + '/vitest.setup.ts'))
    out = GS + '/out/rows_probe_%s%s.json' % (name, TAG); rep = GS + '/out/probe_vitest_%s%s.json' % (name, TAG)
    t0 = now()
    with open(GS + '/out/probe_%s%s.stderr' % (name, TAG), 'w') as fe:
        p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/vitest', 'run', '--config', cfg, '--reporter=json', '--outputFile=' + rep], cwd=pd, stdout=subprocess.PIPE, stderr=fe, text=True, env=dict(os.environ, CI='1', QA1032_ROWS_OUT=out))
    try:
        j = json.load(open(rep)); P('probe', name, t0, '->', now(), 'rc', p.returncode, '| files', len(j['testResults']), 'tests', j['numTotalTests'], 'failed', j['numFailedTests'],
                                   [ (a['title'], (a.get('failureMessages') or [''])[0][:200]) for s in j['testResults'] for a in s['assertionResults'] if a['status'] != 'passed'][:5], [s.get('message', '')[:300] for s in j['testResults'] if s['status'] != 'passed'][:2])
        rows[name] = {r['id']: r for r in json.load(open(out))}
    except Exception as e:
        P('probe', name, 'rc', p.returncode, 'unreadable', type(e).__name__, str(e)[:200], '| stdout tail', p.stdout[-800:])
def brief(r):
    if not r: return 'MISSING'
    rq = r['requestRow']
    return '%s %s code=%s data=%s | row=%s rows=%d | level=%s | seq=%s | errlogs=%d%s' % (
        r['status'], 'ok' if r['success'] else 'fail', r['code'], r['dataStatus'], (rq['status'] + '/by=' + ('set' if rq['reviewed_by'] else 'null') + '/at=' + str(rq['reviewed_at'])) if rq else None,
        r['requestRows'], r['level'], ','.join(r['seq']), len(r['errorLogs']), (' mem=%s' % r.get('listedFromMemory')) if 'listedFromMemory' in r else '')
if len(rows) == 2:
    for rid in rows['head']:
        P('ROW', rid.ljust(26), '\n    develop:', brief(rows['dev'].get(rid)), '\n    head   :', brief(rows['head'].get(rid)))
        for l in rows['head'][rid]['errorLogs']: P('      head error log:', l['msg'][:150], '| keys', l['keys'], '| requestId', l['requestId'])
elif rows:
    for name, rs in rows.items():
        for rid, r in rs.items(): P('ROW', name, rid.ljust(26), brief(r))
# collectors
for name in TREES:
    tree = paths['trees'][name]; auth = tree + '/' + A
    p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/vitest', 'list', '--filesOnly'], cwd=auth, capture_output=True, text=True, env=dict(os.environ, CI='1'))
    L = p.stdout.splitlines()
    P('COLLECTOR vitest list', name, 'rc', p.returncode, 'files', len(L), '| qa_probe listed', sum('qa_probe' in x for x in L), '| control ks1194 listed', sum('ks1194' in x for x in L), '| stderr', p.stderr.strip()[:160])
    p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.', '--listFilesOnly'], cwd=auth, capture_output=True, text=True)
    L = p.stdout.splitlines()
    P('COLLECTOR tsc -p . --listFilesOnly', name, 'files', len(L), '| qa_probe', sum('qa_probe' in x for x in L), '| control routes/users.ts', sum(x.endswith('src/routes/users.ts') for x in L))
P('drafter_probe_1032 end', now())
