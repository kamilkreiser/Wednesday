#!/usr/bin/env python3
"""drafter_probe_1032r2.py <template-basename> <tag> <NODE_ENV test|production> [trees...] — place GS/src/<template> OUTSIDE services/auth at
<tree>/Blockchain/Dev/qa_probe_1032r2/ (every mock / import path ABSOLUTE via __AUTH__), with a scratch vitest config beside it (root = the probe dir,
include = the probe only, auth's vitest.setup.ts and the @secuura/shared/utils/logger alias absolute, test.env NODE_ENV as given), run it per tree,
write out/rows_<tag>_<tree>_<env>.json, print a compact table per row (head vs r1 vs dev). Then PROVE the probe is outside both auth collectors:
`vitest list --filesOnly` lists 0 qa_probe (control: ks1194 listed at head) and `tsc -p . --listFilesOnly` lists 0 qa_probe (control users.ts).
From ../2026-09-17_gate1032/drafter_probe_1032.py, re-pinned. cwd inside the clone only; never rm."""
import json, subprocess, datetime, os, sys, hashlib
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1032r2'
paths = json.load(open(GS + '/out/drafter_paths.json'))
DEV = 'Blockchain/Dev'; A = DEV + '/services/auth'
TPL, TAG, NODE_ENV = sys.argv[1], sys.argv[2], sys.argv[3]
TREES = sys.argv[4:] or ['head', 'r1', 'dev']
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return subprocess.run(['uptime'], capture_output=True, text=True).stdout.split('load averages:')[-1].strip()
tpl = open(GS + '/src/' + TPL).read()
P('drafter_probe_1032r2', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| template', TPL, 'sha256', hashlib.sha256(tpl.encode()).hexdigest()[:16], '| __AUTH__ x', tpl.count('__AUTH__'), '| NODE_ENV', NODE_ENV, '| load', load())
rows = {}
for name in TREES:
    tree = paths['trees'][name]; auth = tree + '/' + A; pd = tree + '/' + DEV + '/qa_probe_1032r2'
    os.makedirs(pd, exist_ok=True)
    src = tpl.replace('__AUTH__', auth); assert '__AUTH__' not in src
    pf = 'qa1032r2-%s.test.ts' % TAG
    open(pd + '/' + pf, 'w').write(src)
    cfg = pd + '/vitest.qa1032r2-%s-%s.config.mts' % (TAG, NODE_ENV)
    open(cfg, 'w').write("import { defineConfig } from 'vitest/config';\nexport default defineConfig({\n  root: %r,\n  resolve: { alias: { '@secuura/shared/utils/logger': %r } },\n  test: { globals: true, environment: 'node', include: [%r], setupFiles: [%r], env: { NODE_ENV: %r }, testTimeout: 60000, hookTimeout: 60000 },\n});\n"
                         % (pd, tree + '/' + DEV + '/packages/shared/dist/utils/logger.js', pf, auth + '/vitest.setup.ts', NODE_ENV))
    out = GS + '/out/rows_%s_%s_%s.json' % (TAG, name, NODE_ENV); rep = GS + '/out/probe_vitest_%s_%s_%s.json' % (TAG, name, NODE_ENV)
    t0 = now()
    with open(GS + '/out/probe_%s_%s_%s.stderr' % (TAG, name, NODE_ENV), 'w') as fe:
        p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/vitest', 'run', '--config', cfg, '--reporter=json', '--outputFile=' + rep], cwd=pd, stdout=subprocess.PIPE, stderr=fe, text=True, env=dict(os.environ, CI="1", QA1032R2_ROWS_OUT=out))
    try:
        j = json.load(open(rep))
        P('probe', name, NODE_ENV, t0, '->', now(), 'rc', p.returncode, '| files', len(j['testResults']), 'tests', j['numTotalTests'], 'failed', j['numFailedTests'],
          [(a['title'], (a.get('failureMessages') or [''])[0][:300]) for s in j['testResults'] for a in s['assertionResults'] if a['status'] != 'passed'][:5], [s.get('message', '')[:400] for s in j['testResults'] if s['status'] != 'passed'][:2])
        d = json.load(open(out)); P('   probe saw NODE_ENV', d.get('nodeEnv'), '| listener', open(out + '.listen').read())
        rows[name] = {r['id']: r for r in d['rows']}
    except Exception as e:
        P('probe', name, 'rc', p.returncode, 'unreadable', type(e).__name__, str(e)[:200], '| stdout tail', p.stdout[-1200:])
def lines(r, k):
    return ['%s{%s}' % (l['msg'][:95], ','.join(l['keys'])) for l in r.get(k, [])]
def compact(r):
    if not r: return 'MISSING'
    if r.get('kind') == 'follow-up':
        f = r['first']
        return 'first %s %s row=%s level=%s || ' % (f['status'], f['message'][:50], (f['requestRow'] or {}).get('status'), f['level']) + ' || '.join(
            '%s: %s' % (s['step'], ' '.join('%s=%s' % (k, s.get(k)) for k in ('status', 'code', 'message', 'dataStatus', 'currentLevel', 'requests', 'rows', 'newRequestId', 'level') if k in s)) + (' row=%s' % (s.get('requestRow') or {}).get('status') if 'requestRow' in s else '') for s in r['steps'])
    if 'requestRow' not in r: return json.dumps({k: r.get(k) for k in ('status', 'message', 'afterApprove', 'thenReject')})  # pool-routing rows
    rq = r['requestRow'] or {}
    return '%s %s "%s" data=%s | row=%s/by=%s/at=%s | level=%s\n        seq=%s\n        error=%s\n        warn=%s' % (
        r['status'], r['code'], r['message'][:70], r['dataStatus'], rq.get('status'), rq.get('reviewed_by'), rq.get('reviewed_at'), r['level'], ' > '.join(r['seq']), lines(r, 'errorLines'), lines(r, 'warnLines'))
order = TREES
if rows:
    first = rows.get('head') or next(iter(rows.values()))
    for rid, r in first.items():
        P('ROW', rid, '| expect(head READ):', r.get('expect', '-'))
        for name in order:
            if name in rows: P('   %-4s: %s' % (name, compact(rows[name].get(rid))))
for name in TREES:
    tree = paths['trees'][name]; auth = tree + '/' + A
    p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/vitest', 'list', '--filesOnly'], cwd=auth, capture_output=True, text=True, env=dict(os.environ, CI='1'))
    L = p.stdout.splitlines()
    P('COLLECTOR vitest list', name, 'rc', p.returncode, 'files', len(L), '| qa_probe listed', sum('qa_probe' in x for x in L), '| control ks1194 listed', sum('ks1194' in x for x in L), '| stderr', p.stderr.strip()[:160])
    p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.', '--listFilesOnly'], cwd=auth, capture_output=True, text=True)
    L = p.stdout.splitlines()
    P('COLLECTOR tsc -p . --listFilesOnly', name, 'files', len(L), '| qa_probe', sum('qa_probe' in x for x in L), '| control routes/users.ts', sum(x.endswith('src/routes/users.ts') for x in L))
P('drafter_probe_1032r2 end', now(), 'load', load())
