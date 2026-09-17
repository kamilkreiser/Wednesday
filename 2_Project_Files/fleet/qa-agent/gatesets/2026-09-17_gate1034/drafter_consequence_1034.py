#!/usr/bin/env python3
"""drafter_consequence_1034.py — the RUNTIME consequence of the tamper rows that leave the whole suite green (and of the fix-shape row), on the real app.
A MINI probe is derived from src/qa1034-drafter-probe.template.ts by asserted substitutions (each anchor count 1): routes = GET /api/credentials (http-proxy,
optional), GET /api/signatories (hand-forwarded fetch, required), POST /api/platform/organizations/register-connector (platform.ts authHeaders); keys OK /
REFUSED; callers LIVE, REVOKED and the same JWTs with a lower-case `bearer ` scheme; test mode /api only. Arms on the HEAD worktree: BASE (untampered),
X-BEARER-PREFIX-ONLY, X-FETCH-RAW, X-PLATFORM-NO-RAW — each tamper applied by the same anchors as drafter_tamper_1034.py (count 1 asserted), restored by
bytes + blob sha + git diff --quiet. The probe dir lives at <tree>/Blockchain/Dev/qa_probe_1034c/ and is MOVED to _quarantine after each arm."""
import json, os, subprocess, datetime, hashlib, shutil
GSD = os.path.dirname(os.path.abspath(__file__)); OUTD = GSD + '/out'
PA = json.load(open(GSD + '/drafter_paths.json')); W = PA['W']; T = PA['trees']
WT = T['head']; GWREL = 'Blockchain/Dev/services/api-gateway'; GW = WT + '/' + GWREL
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def blob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
tpl = open(GSD + '/src/qa1034-drafter-probe.template.ts').read()
SUBS = [
 ("const KEYS = ['NOKEY', 'JUNK', 'OK', 'REFUSED', 'DROPPED', 'NONJSON'];\nconst CALLERS = ['NONE', 'LIVE', 'REVOKED'];", "const KEYS = ['OK', 'REFUSED'];\nconst CALLERS = ['LIVE', 'REVOKED', 'LIVE_LOWER', 'REVOKED_LOWER'];"),
 ("function callerHeader(c: string): Record<string, string> { return c === 'NONE' ? {} : { authorization: userJwt(c === 'LIVE' ? 'qa1034-live' : 'qa1034-revoked') }; }",
  "function callerHeader(c: string): Record<string, string> { if (c === 'NONE') return {}; const j = userJwt(c.startsWith('LIVE') ? 'qa1034-live' : 'qa1034-revoked'); return { authorization: c.endsWith('_LOWER') ? j.replace(/^Bearer /, 'bearer ') : j }; }"),
]
mini = tpl
for a, b in SUBS:
    assert mini.count(a) == 1, (a[:60], mini.count(a)); mini = mini.replace(a, b)
i = mini.index("describe('qa1034 drafter probe', () => {")
mini = mini[:i] + """describe('qa1034 drafter consequence probe', () => {
  it('test mode /api: 3 routes x OK/REFUSED x 4 callers', async () => {
    const g = await bootApp(testEnv());
    const pick = ROUTES.filter((r) => ['/api/credentials', '/api/signatories', '/api/platform/organizations/register-connector'].includes(r.path));
    try { await matrix(g.url, 'test', '/api', pick); } finally { await closeServer(g.server); }
    expect(OUT.rows.length).toBe(24);
  }, 300000);
});
"""
DEL = "      delete req.headers.authorization;\n"
SIG = "          headers: { 'Authorization': req.headers.authorization || '' },\n        });\n        const body = await upstream.json().catch(() => ({}));\n        return res.status(upstream.status).json(body);"
PFA = "    const auth = (req as any).rawAuthorization || req.headers.authorization;\n"
ARMS = [('BASE', None, None, None),
        ('X-BEARER-PREFIX-ONLY', 'src/middleware/auth.ts', DEL, "      if (req.headers.authorization?.startsWith('Bearer ')) delete req.headers.authorization; // qa1034-tamper X-BEARER-PREFIX-ONLY\n"),
        ('X-FETCH-RAW', 'src/routes/proxy.ts', SIG, SIG.replace("'Authorization': req.headers.authorization || ''", "'Authorization': (req as any).rawAuthorization || req.headers.authorization || '' /* qa1034-tamper X-FETCH-RAW */")),
        ('X-PLATFORM-NO-RAW', 'src/routes/platform.ts', PFA, "    const auth = req.headers.authorization; // qa1034-tamper X-PLATFORM-NO-RAW (a fix shape)\n")]
summary = {}
for arm, rel, a, b in ARMS:
    f = GW + '/' + rel if rel else None; orig = open(f, 'rb').read() if f else None
    D = WT + '/Blockchain/Dev/qa_probe_1034c'; os.makedirs(D); pf = D + '/qa1034c.test.ts'; open(pf, 'w').write(mini.replace('__GW_SRC__', GW + '/src'))
    cfg = D + '/vitest.qa1034c.config.mts'
    open(cfg, 'w').write("import { defineConfig } from 'vitest/config';\nexport default defineConfig({ root: %r, test: { globals: true, environment: 'node', setupFiles: [%r], include: [%r], dir: %r } });\n" % (GW, GW + '/vitest.setup.ts', pf, D))
    try:
        if f:
            t = orig.decode(); assert t.count(a) == 1, (arm, t.count(a)); open(f, 'w').write(t.replace(a, b)); assert 'qa1034-tamper' in open(f).read()
        out = OUTD + '/consequence_%s.json' % arm; env = dict(os.environ); env.pop('NODE_ENV', None); env.update(QA_OUT=out, QA_ROUTES=OUTD + '/mounts_head.json')
        p = subprocess.run(['node', WT + '/Blockchain/Dev/node_modules/vitest/vitest.mjs', 'run', '--config', cfg], cwd=GW, capture_output=True, text=True, env=env)
        open(OUTD + '/consequence_%s.stderr' % arm, 'w').write(p.stderr + '\n--stdout tail--\n' + p.stdout[-3000:])
        rows = json.load(open(out))['rows']
        summary[arm] = [(r['route'].split(' ')[1].split('/')[-1], r['key'], r['caller'], r['status'], [(h['url'].split('/')[-1][:12], h['cls'], h['eqCaller']) for h in r['fwd']]) for r in rows]
        P(arm, 'vitest rc', p.returncode, '| rows', len(rows), '| cells forwarding the caller Authorization', sum(any(h['eqCaller'] for h in r['fwd']) for r in rows),
          '| by route', dict((k, sum(1 for r in rows if r['route'].endswith(k) and any(h['eqCaller'] for h in r['fwd']))) for k in ('credentials', 'signatories', 'register-connector')),
          '| by caller', dict((c, sum(1 for r in rows if r['caller'] == c and any(h['eqCaller'] for h in r['fwd']))) for c in ('LIVE', 'REVOKED', 'LIVE_LOWER', 'REVOKED_LOWER')))
        for row in summary[arm]: P('    ', row)
    finally:
        if f:
            open(f, 'wb').write(orig); P('   restored blob equal', blob(open(f, 'rb').read()) == blob(orig), '| git diff --quiet', subprocess.run(['git', '-C', WT, 'diff', '--quiet', 'HEAD']).returncode == 0)
        q = W + '/_quarantine'; os.makedirs(q, exist_ok=True); shutil.move(D, q + '/qa_probe_1034c.%s.%s' % (arm, datetime.datetime.now().strftime('%H%M%S%f')))
P('porcelain', repr(subprocess.run(['git', '-C', WT, 'status', '--porcelain', '--untracked-files=all'], capture_output=True, text=True).stdout[:300]))
