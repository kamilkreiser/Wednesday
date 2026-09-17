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

const STAGES = (process.env.QA_STAGES || 'verdict,test,grace,prod,limiter,noemail,urlspy').split(',');
const OUT: any = { stages: STAGES, verdict: [], test: [], grace: [], prod: [], limiter: [], noemail: [], urlspy: [], originate: [], originateRoutes: [], jwksFetches: 0 };
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
  { id: 'D01 origin POST', cls: 'door', method: 'POST', sub: '/erasures', toks: [...D, 'user', 'none', 'noemail_noscope', 'noemail_scope'] },
  { id: 'D02 origin GET ref', cls: 'door', method: 'GET', sub: '/erasures/abc', toks: [...D, 'user', 'none', 'noemail_noscope', 'noemail_scope'] },
  { id: 'D03 abs POST', cls: 'door', method: 'POST', sub: '/erasures', abs: 'http://127.0.0.1', toks: [...D, 'user', 'none', 'noemail_noscope', 'noemail_scope'] },
  { id: 'D04 abs GET ref', cls: 'door', method: 'GET', sub: '/erasures/abc', abs: 'http://127.0.0.1', toks: [...D, 'user', 'noemail_noscope'] },
  { id: 'D05 abs any host', cls: 'door', method: 'POST', sub: '/erasures', abs: 'http://qa-anything.invalid', toks: D },
  { id: 'D07 abs HTTP upper scheme', cls: 'door', method: 'POST', sub: '/erasures', abs: 'HTTP://127.0.0.1', toks: D },
  { id: 'D08 abs https:443', cls: 'door', method: 'POST', sub: '/erasures', abs: 'https://127.0.0.1:443', toks: D },
  { id: 'D09 abs userinfo', cls: 'door', method: 'POST', sub: '/erasures', abs: 'http://u@127.0.0.1', toks: D },
  { id: 'D31 abs erasures#f', cls: 'door', method: 'POST', sub: '/erasures#f', abs: 'http://127.0.0.1', toks: D },
  { id: 'D32 abs GET ref #f', cls: 'door', method: 'GET', sub: '/erasures/abc#f', abs: 'http://qa-anything.invalid', toks: D },
  { id: 'D10 %65rasures', cls: 'door', method: 'POST', sub: '/%65rasures', toks: D },
  { id: 'D11 %45RASURES', cls: 'door', method: 'POST', sub: '/%45RASURES', toks: D },
  { id: 'D12 ./erasures', cls: 'door', method: 'POST', sub: '/./erasures', toks: D },
  { id: 'D13 erasures;x=1', cls: 'door', method: 'POST', sub: '/erasures;x=1', toks: D },
  { id: 'D14 erasures/', cls: 'door', method: 'POST', sub: '/erasures/', toks: D },
  { id: 'D15 ERASURES', cls: 'door', method: 'POST', sub: '/ERASURES', toks: D },
  { id: 'D16 Erasures', cls: 'door', method: 'POST', sub: '/Erasures', toks: D },
  { id: 'D17 x/../erasures', cls: 'door', method: 'POST', sub: '/x/../erasures', toks: D },
  { id: 'D18 //erasures', cls: 'door', method: 'POST', sub: '//erasures', toks: D },
  { id: 'D19 erasures?x=1', cls: 'door', method: 'POST', sub: '/erasures?x=1', toks: D },
  { id: 'D20 %2e/erasures', cls: 'door', method: 'POST', sub: '/%2e/erasures', toks: D },
  { id: 'D21 x/%2e%2e/erasures', cls: 'door', method: 'POST', sub: '/x/%2e%2e/erasures', toks: D },
  { id: 'D22 erasures%2fabc GET', cls: 'door', method: 'GET', sub: '/erasures%2fabc', toks: D },
  { id: 'D23 %2ferasures', cls: 'door', method: 'POST', sub: '/%2ferasures', toks: D },
  { id: 'D24 ;p/erasures', cls: 'door', method: 'POST', sub: '/;p/erasures', toks: D },
  { id: 'D26 abs %65rasures', cls: 'door', method: 'POST', sub: '/%65rasures', abs: 'http://127.0.0.1', toks: D },
  { id: 'D27 abs ./erasures', cls: 'door', method: 'POST', sub: '/./erasures', abs: 'http://127.0.0.1', toks: D },
  { id: 'D28 abs x/../erasures', cls: 'door', method: 'POST', sub: '/x/../erasures', abs: 'http://127.0.0.1', toks: D },
  { id: 'D29 erasures/%zz GET', cls: 'door', method: 'GET', sub: '/erasures/%zz', toks: D },
  { id: 'D30 erasures/abc;x GET', cls: 'door', method: 'GET', sub: '/erasures/abc;x', toks: D },
  { id: 'D33 ERASURES/abc GET', cls: 'door', method: 'GET', sub: '/ERASURES/abc', toks: D },
  { id: 'D34 erasures/. GET', cls: 'door', method: 'GET', sub: '/erasures/.', toks: D },
  { id: 'D35 erasures/abc/.. GET', cls: 'door', method: 'GET', sub: '/erasures/abc/..', toks: D },
  // L10 legitimate refs WITH the scope (and the refusal without)
  { id: 'L10a erasures/ref.v2 GET', cls: 'door', method: 'GET', sub: '/erasures/ref.v2', toks: D },
  { id: 'L10b erasures/ref%20x GET', cls: 'door', method: 'GET', sub: '/erasures/ref%20x', toks: D },
  { id: 'L10c erasures/u-1 GET', cls: 'door', method: 'GET', sub: '/erasures/c0ffee00-0000-4000-8000-000000000001', toks: D },
  { id: 'L10d erasures/..ref GET', cls: 'door', method: 'GET', sub: '/erasures/..ref', toks: D },
  // undetermined
  { id: 'U01 %zzrasures', cls: 'undetermined', method: 'POST', sub: '/%zzrasures', toks: [...D, 'none'] },
  { id: 'U02 ../gdpr/erasures', cls: 'undetermined', method: 'POST', sub: '/../gdpr/erasures', toks: D },
  { id: 'U03 consent/../../erasures', cls: 'undetermined', method: 'POST', sub: '/consent/../../erasures', toks: D },
  { id: 'U04 %E9rasures', cls: 'undetermined', method: 'POST', sub: '/%E9rasures', toks: D },
  { id: 'U05 abs %zzrasures', cls: 'undetermined', method: 'POST', sub: '/%zzrasures', abs: 'http://127.0.0.1', toks: D },
  { id: 'U06 %zz alone GET', cls: 'undetermined', method: 'GET', sub: '/%zz', toks: D },
  { id: 'U07 /.. GET', cls: 'undetermined', method: 'GET', sub: '/..', toks: D },
  { id: 'U08 erasures/../%zz GET', cls: 'undetermined', method: 'GET', sub: '/erasures/../%zz', toks: D },
  { id: 'U09 erasures/%2e%2e%2f%2e%2e%2fconsent GET', cls: 'undetermined', method: 'GET', sub: '/erasures/%2e%2e%2f%2e%2e%2fconsent', toks: D },
  // W class: raw first segment names the door; the canonical verdict pops it; express matches /erasures/:externalRef on the RAW path. x2 in-run.
  { id: 'W01 erasures/.. GET', cls: 'W', method: 'GET', sub: '/erasures/..', toks: WT, reps: 2 },
  { id: 'W02 erasures/%2e%2e GET', cls: 'W', method: 'GET', sub: '/erasures/%2e%2e', toks: WT, reps: 2 },
  { id: 'W03 erasures/..;x GET', cls: 'W', method: 'GET', sub: '/erasures/..;x', toks: WT, reps: 2 },
  { id: 'W04 erasures/%2e%2e%2fabc GET', cls: 'W', method: 'GET', sub: '/erasures/%2e%2e%2fabc', toks: WT, reps: 2 },
  { id: 'W05 erasures/.%2e GET', cls: 'W', method: 'GET', sub: '/erasures/.%2e', toks: WT, reps: 2 },
  { id: 'W08 erasures/%2E%2E GET', cls: 'W', method: 'GET', sub: '/erasures/%2E%2E', toks: WT, reps: 2 },
  { id: 'W09 erasures/%2e. GET', cls: 'W', method: 'GET', sub: '/erasures/%2e.', toks: WT, reps: 2 },
  { id: 'W10 erasures/../ GET (trailing slash)', cls: 'W', method: 'GET', sub: '/erasures/../', toks: WT, reps: 2 },
  { id: 'W11 erasures/..%2f GET', cls: 'W', method: 'GET', sub: '/erasures/..%2f', toks: WT, reps: 2 },
  { id: 'W12 erasures/%2e%2e%2fconsent GET', cls: 'W', method: 'GET', sub: '/erasures/%2e%2e%2fconsent', toks: WT, reps: 2 },
  { id: 'W13 erasures/.%2e;x GET', cls: 'W', method: 'GET', sub: '/erasures/.%2e;x', toks: WT, reps: 2 },
  { id: 'W14 ERASURES/.. GET', cls: 'W', method: 'GET', sub: '/ERASURES/..', toks: WT, reps: 2 },
  { id: 'W15 //erasures/.. GET', cls: 'W', method: 'GET', sub: '//erasures/..', toks: WT, reps: 2 },
  { id: 'W16 erasures//.. GET', cls: 'W', method: 'GET', sub: '/erasures//..', toks: WT, reps: 2 },
  { id: 'W17 erasures/..?x=1 GET', cls: 'W', method: 'GET', sub: '/erasures/..?x=1', toks: WT, reps: 2 },
  { id: 'W18 erasures/%2e%2e%3bx GET', cls: 'W', method: 'GET', sub: '/erasures/%2e%2e%3bx', toks: WT, reps: 2 },
  { id: 'W06 erasures/.. POST', cls: 'W', method: 'POST', sub: '/erasures/..', toks: D },
  { id: 'W07 abs erasures/.. GET', cls: 'W', method: 'GET', sub: '/erasures/..', abs: 'http://127.0.0.1', toks: WT, reps: 2 },
  // non-door spellings (Tightening A)
  { id: 'N01 %63onsent/check', cls: 'not-door', method: 'GET', sub: '/%63onsent/check', toks: D },
  { id: 'N02 consent/%zz', cls: 'not-door', method: 'GET', sub: '/consent/%zz', toks: D },
  { id: 'N03 CONSENT/check', cls: 'not-door', method: 'GET', sub: '/CONSENT/check', toks: D },
  { id: 'N04 consent//check', cls: 'not-door', method: 'GET', sub: '/consent//check', toks: D },
  { id: 'N05 erasuresX', cls: 'not-door', method: 'POST', sub: '/erasuresX', toks: D },
  { id: 'N06 erasures.json', cls: 'not-door', method: 'POST', sub: '/erasures.json', toks: D },
  { id: 'N07 erasures%3bx=1', cls: 'not-door', method: 'POST', sub: '/erasures%3bx=1', toks: D },
  { id: 'N08 abs consent/check?next=/erasures', cls: 'not-door', method: 'GET', sub: '/consent/check?next=/erasures', abs: 'http://127.0.0.1', toks: D },
  { id: 'N09 consent/check?x=%zz', cls: 'not-door', method: 'GET', sub: '/consent/check?x=%zz', toks: D },
  { id: 'N10 bare mount', cls: 'not-door', method: 'GET', sub: '', toks: D },
  { id: 'N11 consent/%E9', cls: 'not-door', method: 'GET', sub: '/consent/%E9', toks: D },
  { id: 'N12 erasure/u-1 (admin, singular)', cls: 'not-door', method: 'POST', sub: '/erasure/u-1', toks: D },
  { id: 'N13 consent/check?q=//x', cls: 'not-door', method: 'GET', sub: '/consent/check?q=//x', toks: D },
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
    expect(OUT.verdict.length).toBeGreaterThan(60);
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
    expect(OUT.test.length).toBeGreaterThan(200);
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
    expect(OUT.prod.length).toBeGreaterThan(200);
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
        for (const [id, m, sub] of [['OC origin GET abc', 'GET', '/erasures/abc'], ['OC W01 ..', 'GET', '/erasures/..'], ['OC W02 %2e%2e', 'GET', '/erasures/%2e%2e'], ['OC W03 ..;x', 'GET', '/erasures/..;x'],
          ['OC W04 %2e%2e%2fabc', 'GET', '/erasures/%2e%2e%2fabc'], ['OC W05 .%2e', 'GET', '/erasures/.%2e'], ['OC W10 ../', 'GET', '/erasures/../'], ['OC W12 %2e%2e%2fconsent', 'GET', '/erasures/%2e%2e%2fconsent'],
          ['OC W14 ERASURES/..', 'GET', '/ERASURES/..'], ['OC CTRL %65rasures POST', 'POST', '/%65rasures'], ['OC CTRL consent/check', 'GET', '/consent/check']] as string[][]) {
          for (const rep of [1, 2]) for (const t of ['noscope', 'scope', 'user']) OUT.originate.push({ mode, id, rep, method: m, target: pre + sub, tok: t, ...(await send(g.url, m, pre + sub, TOK[t]())) });
        }
      } finally { await closeServer(g.server); }
    }
    await closeServer(osrv);
    expect(OUT.originate.length).toBe(132);
  }, 400000);
});
