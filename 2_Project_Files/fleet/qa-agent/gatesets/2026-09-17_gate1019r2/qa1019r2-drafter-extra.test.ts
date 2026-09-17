/**
 * qa1019-gate-probe.test.ts — QA GATE probe for PR #1019 (KS-1187), round 1. NOT a product test: copied into THIS gate's clone, run SOLO,
 * quarantined by rename. Derived from (not identical to) the drafter's qa1019-drafter-probe.test.ts; additions: the W class widened
 * (every dot-segment-after-erasures spelling this gate derived by reading erasureDoorVerdict against express's matcher) and replicated x2
 * in-run, L10 refs, a no-email non-gdpr route, a req.url setter spy on a BARE app mounting createProxyRoutes, the grace spy over more shapes,
 * and an 'originate' stage: originate's REAL gdprRouter + REAL requireRole mounted in-process as the upstream (its gdprService and logger
 * mocked, its authenticate() mocked to decode the forwarded Bearer WITHOUT verifying) so the W class is routed by the upstream's own router.
 * The REAL index.ts app in-process; `../db` mocked; every *_SERVICE_URL = ONE loopback recorder with a hit counter (JWKS fetches are
 * counted apart and are NOT hits). Tokens: THROWAWAY RS256 JWTs (vitest.setup.ts __TEST_JWT_PRIVATE_PEM), email as generateConnectorToken
 * mints it, a FRESH userId per request (except the limiter stage). Stages via QA_STAGES. Rows -> QA_OUT. Every listener binds 127.0.0.1:0
 * and is closed in finally/afterAll.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import express from 'express';
import jwt from 'jsonwebtoken';
import { randomUUID } from 'crypto';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

vi.mock('../db', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
});
// originate stage only (these modules are not imported by the gateway)
const ORIG_CALLS: any[] = [];
vi.mock('../../../originate/src/services/gdprService', () => {
  const rec = (name: string) => async (...args: any[]) => { ORIG_CALLS.push({ fn: name, args: args.map((a) => (typeof a === 'string' ? a : typeof a)) }); return { qa: 'recorded', fn: name }; };
  // QA-FIX-NAMEDMOCK: a Proxy namespace exposed no named exports (first run hung); every gdpr.* the router references, named
  class ConnectorErasureCrossOrgError extends Error {} class ConnectorErasureUnresolvableError extends Error {}
  const o: Record<string, any> = { ConnectorErasureCrossOrgError, ConnectorErasureUnresolvableError };
  for (const k of ['createDSR', 'enforceRetention', 'executeErasure', 'executeErasureByExternalRef', 'exportUserData', 'getDeletionLog', 'getDSR', 'getErasureStatusByExternalRef', 'getPendingDSRs', 'getRetentionPolicies', 'getUserConsents', 'getUserDSRs', 'hasValidConsent', 'recordConsent', 'updateDSRStatus', 'withdrawConsent']) o[k] = rec(k);
  return o;
});
vi.mock('../../../originate/src/utils/logger', () => ({ logger: { info: () => {}, warn: () => {}, error: () => {}, debug: () => {} }, default: { info: () => {}, warn: () => {}, error: () => {}, debug: () => {} } }));
vi.mock('../../../originate/src/middleware/auth', async (orig) => {
  const real = (await orig()) as Record<string, any>;
  return { ...real, authenticate: () => (req: any, res: any, next: any) => {
    const h = String(req.headers.authorization || ''); if (!h.startsWith('Bearer ')) return res.status(401).json({ qaOriginateAuth: 'none' });
    const u = jwt.decode(h.slice(7)) as any; req._secuuraUser = u; req.user = u; next(); } };
});

const STAGES = (process.env.QA_STAGES || 'verdict,test,prod,mount').split(',');
const OUT: any = { mount: [], stages: STAGES, verdict: [], test: [], grace: [], prod: [], limiter: [], noemail: [], urlspy: [], originate: [], originateRoutes: [], jwksFetches: 0 };
const seen: string[] = [];
let recorder: http.Server | undefined;
let recorderUrl = '';

function listen(server: http.Server): Promise<string> {
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(`http://127.0.0.1:${(server.address() as any).port}`)));
}
async function closeServer(server: http.Server | undefined) {
  if (!server) return;
  (server as any).closeAllConnections?.();
  await new Promise<void>((r) => server.close(() => r()));
}
function token(o: { scopes?: string[]; email?: boolean; userId?: string; role?: string; authMethod?: string }): string {
  const p: any = { userId: o.userId || 'connector:' + randomUUID(), role: o.role || 'connector', authMethod: o.authMethod || 'api_key', type: 'connector', scopes: o.scopes || [],
    tenantId: 'a0000000-0000-4000-8000-000000000001', organizationId: 'd0000000-0000-4000-8000-00000000118d', verificationLevel: 'api_key' };
  if (o.role === 'user') { delete p.type; p.verificationLevel = 'BASIC'; }
  if (o.email !== false) p.email = o.role === 'user' ? 'qa-user@secuura.invalid' : 'connector@secuura.io';
  return 'Bearer ' + jwt.sign(p, process.env.__TEST_JWT_PRIVATE_PEM as string, { algorithm: 'RS256', expiresIn: '10m' });
}
const TOK: Record<string, () => string | null> = {
  noscope: () => token({ scopes: ['documents:read'] }),
  scope: () => token({ scopes: ['subjects:erase'] }),
  noemail_noscope: () => token({ scopes: ['documents:read'], email: false }),
  noemail_scope: () => token({ scopes: ['subjects:erase'], email: false }),
  user: () => token({ role: 'user', authMethod: 'email', scopes: [] }),
  none: () => null,
};
let lastErrLines: string[] = [];
function send(base: string, method: string, path: string, auth: string | null): Promise<any> {
  return new Promise((resolve) => {
    const t = new URL(base); const before = seen.length; const oc = ORIG_CALLS.length; const el = lastErrLines.length;
    const body = method === 'GET' ? undefined : '{"externalRef":"qa-gate-ref"}';
    const headers: Record<string, string> = {};
    if (auth) headers.authorization = auth;
    if (body !== undefined) { headers['content-type'] = 'application/json'; headers['content-length'] = String(Buffer.byteLength(body)); }
    const req = http.request({ hostname: t.hostname, port: t.port, path, method, agent: false, headers }, (res) => {
      const c: Buffer[] = [];
      res.on('data', (d) => c.push(d));
      res.on('end', () => {
        const txt = Buffer.concat(c).toString(); let code: string | null = null; let msg: string | null = null; let upstreamBody: any = null;
        try { const j = JSON.parse(txt); code = j?.error?.code ?? null; msg = (j?.error?.message ?? null) && String(j.error.message).slice(0, 120); if (j?.recorder || j?.qa || j?.h || j?.qaOriginate) upstreamBody = j; } catch { /* non-JSON body: code stays null */ }
        setTimeout(() => resolve({ status: res.statusCode, code, msg, hits: seen.slice(before), location: res.headers.location ?? null,
          rlRemaining: res.headers['x-ratelimit-remaining'] ?? null, originateCalls: ORIG_CALLS.slice(oc), upstreamBody,
          headerErr: lastErrLines.slice(el).filter((l) => /x-user-email/i.test(l)).length }), 60);
      });
    });
    req.setTimeout(8000, () => { req.destroy(new Error('QA-CLIENT-TIMEOUT 8s')); }); // QA-FIX-CLIENTTIMEOUT: a hang is a row, not a stalled stage
    req.on('error', (e) => resolve({ status: -1, code: 'CLIENT_ERROR', msg: String(e).slice(0, 120), hits: seen.slice(before), originateCalls: ORIG_CALLS.slice(oc) }));
    if (body !== undefined) req.end(body); else req.end();
  });
}
async function bootApp(env: Record<string, string>) {
  vi.resetModules();
  for (const [k, v] of Object.entries(env)) vi.stubEnv(k, v);
  delete process.env.JWT_JWKS_URL;
  const app = (await import('../index')).default;
  const server = http.createServer(app as any);
  return { server, url: await listen(server) };
}
const SVC = ['ORIGINATE_SERVICE_URL', 'AUTH_SERVICE_URL', 'SECURITY_SERVICE_URL', 'ANCHORING_SERVICE_URL', 'VERIFICATION_SERVICE_URL', 'NOTIFICATION_SERVICE_URL'];

type Shape = { id: string; cls: string; method: string; sub: string; abs?: string; toks: string[]; reps?: number };
const D = ['noscope', 'scope'];
const WT = ['noscope', 'scope', 'user', 'noemail_noscope'];
const SHAPES: Shape[] = [
  // qa1019r2 DRAFTER EXTRA: dot / param / encoding spellings AFTER the door that round 1's census did not send, and dotted references (L-shapes)
  { id: 'X01 erasures/%2e', cls: 'X-dot', method: 'GET', sub: '/erasures/%2e', toks: D },
  { id: 'X02 erasures/abc/%2e%2e', cls: 'X-dot', method: 'GET', sub: '/erasures/abc/%2e%2e', toks: D },
  { id: 'X03 erasures/..%3bx', cls: 'X-ref', method: 'GET', sub: '/erasures/..%3bx', toks: D },
  { id: 'X04 erasures/%2e%2e;x=1', cls: 'X-dot', method: 'GET', sub: '/erasures/%2e%2e;x=1', toks: D },
  { id: 'X05 Erasures/%2e', cls: 'X-dot', method: 'GET', sub: '/Erasures/%2e', toks: D },
  { id: 'X06 ./erasures/..', cls: 'X-dot', method: 'GET', sub: '/./erasures/..', toks: D },
  { id: 'X07 erasures/./abc', cls: 'X-dot', method: 'GET', sub: '/erasures/./abc', toks: D },
  { id: 'X08 erasures/abc/.', cls: 'X-dot', method: 'GET', sub: '/erasures/abc/.', toks: D },
  { id: 'X09 erasures/...', cls: 'X-ref', method: 'GET', sub: '/erasures/...', toks: D },
  { id: 'X10 erasures/%2e%2e%2e', cls: 'X-ref', method: 'GET', sub: '/erasures/%2e%2e%2e', toks: D },
  { id: 'X11 erasures/.ref', cls: 'X-ref', method: 'GET', sub: '/erasures/.ref', toks: D },
  { id: 'X12 erasures/a.b', cls: 'X-ref', method: 'GET', sub: '/erasures/a.b', toks: D },
  { id: 'X13 erasures/abc.', cls: 'X-ref', method: 'GET', sub: '/erasures/abc.', toks: D },
  { id: 'X14 erasures/ref..v2', cls: 'X-ref', method: 'GET', sub: '/erasures/ref..v2', toks: D },
  { id: 'X15 erasures/%2E', cls: 'X-dot', method: 'GET', sub: '/erasures/%2E', toks: D },
  { id: 'X16 erasures/..%00', cls: 'X-ref', method: 'GET', sub: '/erasures/..%00', toks: D },
  { id: 'X17 erasures/%252e%252e', cls: 'X-ref', method: 'GET', sub: '/erasures/%252e%252e', toks: D },
  { id: 'X18 erasures/.. POST', cls: 'X-dot', method: 'POST', sub: '/erasures/..', toks: D },
  { id: 'X19 erasures/..?x=/erasures', cls: 'X-dot', method: 'GET', sub: '/erasures/..?x=/erasures', toks: D },
  { id: 'X20 erasures/..#frag', cls: 'X-dot', method: 'GET', sub: '/erasures/..#frag', toks: D },
  { id: 'X21 consent/../erasures/..', cls: 'X-dot', method: 'GET', sub: '/consent/../erasures/..', toks: D },
  { id: 'X22 consent/..', cls: 'X-notdoor-dot', method: 'GET', sub: '/consent/..', toks: D },
  { id: 'X23 dsr/./pending', cls: 'X-notdoor-dot', method: 'GET', sub: '/dsr/./pending', toks: D },
];

beforeAll(async () => {
  const w2 = process.stderr.write.bind(process.stderr); const w1 = process.stdout.write.bind(process.stdout);
  (process.stderr as any).write = (ch: any, ...a: any[]) => { lastErrLines.push(String(ch)); return w2(ch, ...a); };
  (process.stdout as any).write = (ch: any, ...a: any[]) => { lastErrLines.push(String(ch)); return w1(ch, ...a); };
  for (const k of ['warn', 'error', 'log'] as const) { const o = (console as any)[k].bind(console); (console as any)[k] = (...a: any[]) => { lastErrLines.push(a.map((x) => { try { return typeof x === 'string' ? x : JSON.stringify(x); } catch { return String(x); } }).join(' ')); o(...a); }; }
  recorder = http.createServer((req, res) => { req.resume(); req.on('end', () => { if ((req.url || '').startsWith('/.well-known/')) { OUT.jwksFetches += 1; } else { seen.push(`${req.method} ${req.url}`); } res.writeHead(200, { 'content-type': 'application/json' }); res.end('{"recorder":true}'); }); });
  recorderUrl = await listen(recorder);
  const src = readFileSync(join(__dirname, '..', '..', '..', 'originate', 'src', 'routes', 'gdpr.ts'), 'utf8');
  OUT.originateRoutes = [...src.matchAll(/gdprRouter\.(get|post|put|patch|delete)\(\s*'([^']+)'/g)].map((m) => [m[1].toUpperCase(), m[2]]);
  OUT.originateRouteControl = (src.match(/gdprRouter\.(get|post|put|patch|delete)\(/g) || []).length;
});
afterAll(async () => {
  await closeServer(recorder);
  vi.unstubAllEnvs();
  writeFileSync(process.env.QA_OUT as string, JSON.stringify(OUT, null, 1));
});

async function runMatrix(url: string, prefix: string, rows: any[]) {
  for (const s of SHAPES) {
    const path = (s.abs ? s.abs : '') + prefix + s.sub;
    for (let rep = 1; rep <= (s.reps || 1); rep++) {
      for (const t of s.toks) rows.push({ id: s.id, cls: s.cls, rep, method: s.method, target: path, tok: t, ...(await send(url, s.method, path, TOK[t]())) });
    }
  }
  for (const [m, p] of OUT.originateRoutes as Array<[string, string]>) {
    const filled = p.replace(/:[A-Za-z]+/g, 'u-1');
    for (const t of D) rows.push({ id: 'O ' + m + ' ' + p, cls: p.startsWith('/erasures') ? 'originate-door-route' : 'originate-route', rep: 1, method: m, target: prefix + filled, tok: t, ...(await send(url, m, prefix + filled, TOK[t]())) });
  }
}
const testEnv = (flag: string) => { const e: Record<string, string> = { NODE_ENV: 'test', GATEWAY_VOUCH_SECRET: '', SUBJECTS_ERASE_SCOPE_ENFORCED: flag, UNHANDLED_REJECTION_MODE: 'survive' }; for (const k of SVC) e[k] = recorderUrl; return e; };
const prodEnv = () => { const e: Record<string, string> = { NODE_ENV: 'production', CSRF_SECRET: 'qa1019-gate-stub-not-a-secret', DATABASE_URL: 'postgres://qa:qa@127.0.0.1:1/qa', REDIS_URL: 'redis://127.0.0.1:1',
  ENABLE_TEST_TOKENS: '', ENABLE_MOCK_ENDPOINTS: '', GATEWAY_VOUCH_SECRET: '', SUBJECTS_ERASE_SCOPE_ENFORCED: 'true', UNHANDLED_REJECTION_MODE: 'survive' }; for (const k of SVC) e[k] = recorderUrl; return e; };

describe('qa1019 gate probe', () => {
  it('verdict: erasureDoorVerdict over every sub-path (trees that export it)', async () => {
    if (!STAGES.includes('verdict')) return;
    const mod: any = await import('../routes/proxy');
    OUT.verdictExported = typeof mod.erasureDoorVerdict;
    if (typeof mod.erasureDoorVerdict !== 'function') return;
    const subs = new Set<string>();
    for (const s of SHAPES) subs.add((s.abs ? s.abs : '') + s.sub);
    for (const [, p] of OUT.originateRoutes) subs.add(p.replace(/:[A-Za-z]+/g, 'u-1'));
    for (const p of subs) OUT.verdict.push({ sub: p, ci: mod.erasureDoorVerdict(p, false), cs: mod.erasureDoorVerdict(p, true) });
    expect(OUT.verdict.length).toBeGreaterThan(30); // qa1019r2: 23 extra shapes + 17 routes
  });

  it('test mode ENFORCED: the matrix', async () => {
    if (!STAGES.includes('test')) return;
    const g = await bootApp(testEnv('true'));
    try {
      await runMatrix(g.url, '/api/gdpr', OUT.test);
      for (const [id, m, sub, abs] of [['V1 abs POST', 'POST', '/erasures', 'http://127.0.0.1'], ['V1 %65', 'POST', '/%65rasures', ''], ['V1 W01', 'GET', '/erasures/..', ''], ['V1 origin', 'POST', '/erasures', '']] as string[][]) {
        for (const t of ['noscope', 'scope']) { const path = abs + '/api/v1/gdpr' + sub; OUT.test.push({ id, cls: 'v1-in-test', rep: 1, method: m, target: path, tok: t, ...(await send(g.url, m, path, TOK[t]())) }); }
      }
    } finally { await closeServer(g.server); }
    expect(OUT.test.length).toBe(88); // qa1019r2: 46 shape rows + 34 route rows + 8 V1
  }, 180000);

  it('grace (flag unset): a role-only connector, logger spy on THIS registry', async () => {
    if (!STAGES.includes('grace')) return;
    const g = await bootApp(testEnv(''));
    try {
      const lg: any = (await import('../utils/logger')).logger;
      const spy = vi.spyOn(lg, 'warn');
      const ids = ['D01 origin POST', 'D02 origin GET ref', 'D03 abs POST', 'D04 abs GET ref', 'D10 %65rasures', 'D15 ERASURES', 'D13 erasures;x=1', 'U01 %zzrasures',
        'W01 erasures/.. GET', 'W02 erasures/%2e%2e GET', 'W03 erasures/..;x GET', 'W04 erasures/%2e%2e%2fabc GET', 'W07 abs erasures/.. GET', 'N01 %63onsent/check'];
      for (const s of SHAPES.filter((x) => ids.includes(x.id))) {
        const path = (s.abs || '') + '/api/gdpr' + s.sub;
        const c0 = spy.mock.calls.length;
        const r = await send(g.url, s.method, path, TOK.noscope());
        const calls = spy.mock.calls.slice(c0).filter((c: any[]) => String(c[0]).includes('grace is ON'));
        OUT.grace.push({ id: s.id, method: s.method, target: path, tok: 'noscope', ...r, graceSpyCalls: calls.length, graceRoute: calls.map((c: any[]) => c[1]?.route) });
      }
      spy.mockRestore();
    } finally { await closeServer(g.server); }
    expect(OUT.grace.length).toBe(14);
  }, 60000);

  it('production: the matrix under /api/v1 plus unversioned 307 rows', async () => {
    if (!STAGES.includes('prod')) return;
    const g = await bootApp(prodEnv());
    try {
      await runMatrix(g.url, '/api/v1/gdpr', OUT.prod);
      for (const [id, m, p] of [['P307 origin', 'POST', '/api/gdpr/erasures'], ['P307 abs', 'POST', 'http://127.0.0.1/api/gdpr/erasures'], ['P307 %65', 'POST', '/api/gdpr/%65rasures'], ['P307 W01', 'GET', '/api/gdpr/erasures/..']]) {
        for (const t of ['noscope', 'scope']) OUT.prod.push({ id, cls: 'unversioned', rep: 1, method: m, target: p, tok: t, ...(await send(g.url, m, p, TOK[t]())) });
      }
    } finally { await closeServer(g.server); }
    expect(OUT.prod.length).toBe(88); // qa1019r2: 46 + 34 + 8 P307
  }, 180000);

  it('limiter: ONE userId api_key principal across door shapes', async () => {
    if (!STAGES.includes('limiter')) return;
    const g = await bootApp(testEnv('true'));
    const uid = 'connector:' + randomUUID();
    try {
      for (const [id, m, p, sc] of [
        ['L1 origin admitted', 'POST', '/api/gdpr/erasures', true], ['L2 abs admitted', 'POST', 'http://127.0.0.1/api/gdpr/erasures', true],
        ['L3 %65 admitted', 'POST', '/api/gdpr/%65rasures', true], ['L4 abs refused 403', 'POST', 'http://127.0.0.1/api/gdpr/erasures', false],
        ['L5 400 NON_CANONICAL', 'POST', '/api/gdpr/%zzrasures', true], ['L6 non-door consent', 'GET', '/api/gdpr/consent/check', true],
        ['L7 W01 erasures/..', 'GET', '/api/gdpr/erasures/..', false], ['L8 origin refused 403', 'POST', '/api/gdpr/erasures', false]] as Array<[string, string, string, boolean]>) {
        OUT.limiter.push({ id, method: m, target: p, ...(await send(g.url, m, p, token({ userId: uid, scopes: sc ? ['subjects:erase'] : ['documents:read'] }))) });
      }
    } finally { await closeServer(g.server); }
    expect(OUT.limiter.length).toBe(8);
  }, 60000);

  it('noemail: the x-user-email class on gdpr and a non-gdpr proxied route, test and production', async () => {
    if (!STAGES.includes('noemail')) return;
    for (const mode of ['test', 'production']) {
      const g = await bootApp(mode === 'test' ? testEnv('true') : prodEnv());
      const pre = mode === 'test' ? '/api' : '/api/v1';
      try {
        for (const [id, m, sub, abs] of [['NE gdpr door origin', 'POST', '/gdpr/erasures', ''], ['NE gdpr door abs', 'POST', '/gdpr/erasures', 'http://127.0.0.1'],
          ['NE gdpr consent', 'GET', '/gdpr/consent/check', ''], ['NE anchors GET', 'GET', '/anchors/document/qa-doc-1', ''], ['NE documents GET', 'GET', '/documents', '']] as string[][]) {
          for (const t of ['noemail_noscope', 'noemail_scope', 'scope']) { const path = abs + pre + sub; OUT.noemail.push({ mode, id, method: m, target: path, tok: t, ...(await send(g.url, m, path, TOK[t]())) }); }
        }
      } finally { await closeServer(g.server); }
    }
    expect(OUT.noemail.length).toBe(30);
  }, 90000);

  it('urlspy: req.url setter spy on a BARE app mounting createProxyRoutes (no index.ts edit)', async () => {
    if (!STAGES.includes('urlspy')) return;
    const g0 = await bootApp(testEnv('true')); await closeServer(g0.server); // same registry: index.ts ran configureAuth; env stubbed
    const { createProxyRoutes }: any = await import('../routes/proxy');
    const { services }: any = await import('../config/services');
    const { authenticateToken }: any = await import('../middleware/auth');
    const bare = express();
    bare.use((req: any, res: any, next: any) => {
      let v = req.url; const writes: string[] = [];
      Object.defineProperty(req, 'url', { configurable: true, enumerable: true, get: () => v, set: (x) => { writes.push(String(x)); v = x; } });
      res.on('finish', () => { req.__qaFinal = { finalUrl: v, writes }; OUT.urlspy.push({ target: req.originalUrl, method: req.method, status: res.statusCode, finalUrl: v, writes }); });
      next();
    });
    bare.use(createProxyRoutes({ services, authenticateToken, log: () => {} }));
    const srv = http.createServer(bare); const url = await listen(srv);
    try {
      for (const [m, p, t] of [['POST', '/api/gdpr/erasures', 'scope'], ['POST', 'http://127.0.0.1/api/gdpr/erasures', 'scope'], ['POST', '/api/gdpr/%65rasures', 'scope'],
        ['POST', '/api/gdpr/erasures?x=1', 'scope'], ['POST', '/api/gdpr//erasures', 'scope'], ['POST', '/api/gdpr/erasures', 'noscope'], ['POST', '/api/gdpr/%65rasures', 'noscope'],
        ['POST', '/api/gdpr/%zzrasures', 'scope'], ['GET', '/api/gdpr/consent/check', 'scope'], ['GET', '/api/gdpr/erasures/..', 'noscope']]) {
        const r = await send(url, m, p, TOK[t]());
        OUT.urlspy.push({ probe: true, method: m, target: p, tok: t, status: r.status, code: r.code, hits: r.hits });
      }
    } finally { await closeServer(srv); }
    expect(OUT.urlspy.filter((x: any) => x.probe).length).toBe(10);
  }, 60000);

  it('originate: the REAL originate gdprRouter + requireRole as the upstream (service/logger mocked, Bearer decoded unverified)', async () => {
    if (!STAGES.includes('originate')) return;
    const { gdprRouter }: any = await import('../../../originate/src/routes/gdpr');
    const oapp = express(); oapp.use(express.json()); oapp.use('/api/gdpr', gdprRouter); oapp.use((req: any, res: any) => { seen.push(`${req.method} ${req.url} [originate-404]`); res.status(404).json({ qaOriginate: '404' }); });
    const osrv = http.createServer((req, res) => { if ((req.url || '').startsWith('/.well-known/')) { OUT.jwksFetches += 1; return void http.request(recorderUrl + req.url, (r2) => { res.writeHead(r2.statusCode || 200, r2.headers); r2.pipe(res); }).end(); } seen.push(`${req.method} ${req.url}`); (oapp as any)(req, res); });
    const ourl = await listen(osrv);
    const env = testEnv('true'); env.ORIGINATE_SERVICE_URL = ourl;
    for (const mode of ['test', 'production']) {
      const e = mode === 'test' ? env : { ...prodEnv(), ORIGINATE_SERVICE_URL: ourl };
      const g = await bootApp(e);
      const pre = mode === 'test' ? '/api/gdpr' : '/api/v1/gdpr';
      try {
        for (const [id, m, sub] of [['OC origin GET abc', 'GET', '/erasures/abc'], ['OC X01 %2e', 'GET', '/erasures/%2e'], ['OC X03 ..%3bx', 'GET', '/erasures/..%3bx'], ['OC X07 ./abc', 'GET', '/erasures/./abc'], ['OC X09 ...', 'GET', '/erasures/...'], ['OC X11 .ref', 'GET', '/erasures/.ref'], ['OC X12 a.b', 'GET', '/erasures/a.b'], ['OC X13 abc.', 'GET', '/erasures/abc.'], ['OC X16 ..%00', 'GET', '/erasures/..%00'], ['OC X17 %252e%252e', 'GET', '/erasures/%252e%252e'], ['OC X20 ..#frag', 'GET', '/erasures/..#frag'], ['OC W01 ..', 'GET', '/erasures/..'], ['OC W02 %2e%2e', 'GET', '/erasures/%2e%2e'], ['OC W03 ..;x', 'GET', '/erasures/..;x'],
          ['OC W04 %2e%2e%2fabc', 'GET', '/erasures/%2e%2e%2fabc'], ['OC W05 .%2e', 'GET', '/erasures/.%2e'], ['OC W10 ../', 'GET', '/erasures/../'], ['OC W12 %2e%2e%2fconsent', 'GET', '/erasures/%2e%2e%2fconsent'],
          ['OC W14 ERASURES/..', 'GET', '/ERASURES/..'], ['OC CTRL %65rasures POST', 'POST', '/%65rasures'], ['OC CTRL consent/check', 'GET', '/consent/check']] as string[][]) {
          for (const rep of [1, 2]) for (const t of ['noscope', 'scope', 'user']) OUT.originate.push({ mode, id, rep, method: m, target: pre + sub, tok: t, ...(await send(g.url, m, pre + sub, TOK[t]())) });
        }
      } finally { await closeServer(g.server); }
    }
    await closeServer(osrv);
    expect(OUT.originate.length).toBe(252); // qa1019r2: 21 shapes x 2 reps x 3 toks x 2 modes
  }, 400000);
});

describe('qa1019r2 drafter extra: MOUNT-PREFIX spellings (the /api/gdpr mount itself spelled oddly) — test and production', () => {
  it('mount', async () => {
    if (!STAGES.includes('mount')) return;
    const T = ['/api/./gdpr/erasures/..', '/api/x/../gdpr/erasures/abc', '/API/GDPR/erasures/..', '/API/GDPR/ERASURES/abc', '/api/gdpr;x/erasures/..', '/api/%67dpr/erasures/abc',
      '/api/gdpr/./erasures/abc', '/api//gdpr/erasures/..', '/api/x/%2e%2e/gdpr/erasures/abc', '/api/gdpr%2ferasures/abc', '/api/gdpr/erasures/abc', '/api/gdpr/erasures/..'];
    for (const mode of ['test', 'production']) {
      const g = await bootApp(mode === 'test' ? testEnv('true') : prodEnv());
      try {
        for (const t0 of T) {
          const t = mode === 'test' ? t0 : t0.replace(/^\/api\//i, (m) => m + 'v1/');
          for (const tok of ['noscope', 'scope']) OUT.mount.push({ mode, id: 'M ' + t0, method: 'GET', target: t, tok, ...(await send(g.url, 'GET', t, TOK[tok]())) });
        }
      } finally { await closeServer(g.server); }
    }
    expect(OUT.mount.length).toBe(48);
  }, 120000);
});
