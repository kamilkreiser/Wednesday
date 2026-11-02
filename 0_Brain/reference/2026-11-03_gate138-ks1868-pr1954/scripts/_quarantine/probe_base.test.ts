// Gate 138 probe: REAL createAdminRoutes (real requireAdmin, mockBodyParser) on a REAL express listener with the REAL gateway errorHandler
// mounted after it and the REAL winston logger (wired exactly like index.ts: log = winstonLogger.log). Replaced: verifyToken (role = bearer token),
// query (stateful stub, records every statement), redisService (small stub), global fetch (the thrown value). Client uses the original fetch.
import { describe, it, afterAll } from 'vitest';
import express from 'express';
import fs from 'fs';
import Transport from 'winston-transport';
import type { AddressInfo } from 'net';
import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';
import { errorHandler } from '../middleware/errorHandler';
import { logger as winstonLogger } from '../utils/logger';

const OUT = process.env.PROBE_OUT as string;
const origFetch = globalThis.fetch;
const st = { thrown: undefined as { v: unknown } | undefined, scope: 'all' as 'all' | 'count' | 'main', queries: [] as any[], emitted: [] as any[], logThrew: 0, unhandled: 0, redisWrites: 0, fetchCalls: 0, seedInserts: 0 };
process.on('unhandledRejection', () => { st.unhandled++; });

class Cap extends Transport { log(info: any, cb: () => void) { let m: string; try { m = JSON.stringify({ level: info.level, message: info.message, error: info.error }); } catch { m = 'UNSERIALISABLE'; } st.emitted.push(m); cb(); } }
winstonLogger.add(new Cap({ level: 'debug' }));
if (!process.env.PROBE_REAL_CONSOLE) winstonLogger.transports.forEach((t) => { if (!(t instanceof Cap)) t.silent = true; });

const revoked = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const getterErr = () => Object.create(Error.prototype, { message: { get() { throw new Error('g'); } } });
const msgOf = (mk: () => unknown) => Object.create(Error.prototype, { message: { get() { return mk(); } } });
const THROWN: Array<[string, (() => unknown) | null]> = [
  ['ok', null],
  ['ordinaryError', () => new Error('db boom 10.0.0.7')],
  ['revokedProxy', revoked],
  ['getterThrows', getterErr],
  ['msgRevokedProxy', () => msgOf(revoked)],
  ['msgSymbol', () => msgOf(() => Symbol('s'))],
  ['msgToStringThrows', () => msgOf(() => ({ toString() { throw new Error('ts'); } }))],
  ['msgNullProto', () => msgOf(() => Object.create(null))],
  ['msgPlainObject', () => msgOf(() => ({ a: 1 }))],
  ['undefinedThrown', () => undefined],
  ['nullThrown', () => null],
  ['emptyObject', () => ({})],
  ['number42', () => 42],
  ['plainString', () => 'plain string 10.0.0.7'],
  ['objWithMessage', () => ({ message: 'plain msg 10.0.0.7' })],
  ['errMsgNumber', () => msgOf(() => 12345)],
  ['errMsgEmpty', () => new Error('')],
  ['errMsgUndefined', () => msgOf(() => undefined)],
  ['symbolThrown', () => Symbol('thrown')],
];

const integ = { id: 'int-1', integrationType: 'blockchain', provider: 'blockfrost', config: { projectId: 'pid', network: 'preprod' } };
const deps = {
  authenticateToken: () => (_q: any, _r: any, n: any) => n(),
  verifyToken: (t: string) => ({ userId: 'u', email: 'e@x', role: t, verificationLevel: 'HIGH' }),
  isDbAvailable: () => true,
  redisService: { getIntegration: async () => integ, setIntegration: async () => { st.redisWrites++; } },
  services: { auth: { url: 'http://auth.invalid:4003' } },
  query: (text: string, params?: unknown[]) => {
    const t = text.trim();
    st.queries.push({ text: t.slice(0, 45).replace(/\s+/g, ' '), n: (params || []).length });
    if (/^INSERT INTO (organizations|users)/.test(t) && st.scope === 'count') st.seedInserts++;
    const isCount = /^SELECT COUNT/.test(t);
    if (st.thrown && (st.scope === 'all' || (st.scope === 'count' && isCount) || (st.scope === 'main' && !isCount))) return Promise.reject(st.thrown.v);
    if (isCount) return Promise.resolve({ rows: [{ cnt: '5' }], rowCount: 1 });
    return Promise.resolve({ rows: [], rowCount: 1 });
  },
  log: (level: string, message: string, meta?: object) => { try { winstonLogger.log(level, message, meta as any); } catch (e) { st.logThrew++; throw e; } },
} as unknown as AdminRouteDeps;

const app = express();
app.use(createAdminRoutes(deps));
app.use(errorHandler);
const srv = app.listen(0, '127.0.0.1');
const port = () => (srv.address() as AddressInfo).port;
const ID = 'd5800000-0000-4000-8000-000000000002';
type Rt = { n: string; m: string; p: string; body?: unknown; scope?: 'all' | 'count' | 'main'; fetchThrows?: boolean };
const routes: Rt[] = [
  { n: 'POST org', m: 'POST', p: '/api/users/admin/organizations', body: { name: 'Acme', type: 'Organization', status: 'active' } },
  { n: 'PUT org', m: 'PUT', p: `/api/users/admin/organizations/${ID}`, body: { name: 'Acme2' } },
  { n: 'DELETE org', m: 'DELETE', p: `/api/users/admin/organizations/${ID}` },
  { n: 'PATCH forward', m: 'PATCH', p: `/api/users/admin/${ID}`, body: { role: 'USER' }, fetchThrows: true },
  { n: 'GET audit export', m: 'GET', p: '/api/security/audit/export' },
  { n: 'POST integ test', m: 'POST', p: '/api/admin/integrations/int-1/test', body: {}, fetchThrows: true },
  { n: 'PATCH identity level', m: 'PATCH', p: `/api/admin/identity/users/${ID}/level`, body: { verificationLevel: 'HIGH' } },
  { n: 'GET identity users (main)', m: 'GET', p: '/api/admin/identity/users', scope: 'main' },
  { n: 'GET identity orgs (main)', m: 'GET', p: '/api/admin/identity/organizations', scope: 'main' },
  { n: 'GET identity users (seed)', m: 'GET', p: '/api/admin/identity/users', scope: 'count' },
  { n: 'GET identity orgs (seed)', m: 'GET', p: '/api/admin/identity/organizations', scope: 'count' },
];
async function call(r: Rt, role: string | null, thrown: { v: unknown } | undefined) {
  st.queries.length = 0; st.emitted.length = 0; st.logThrew = 0; st.redisWrites = 0; st.fetchCalls = 0; st.seedInserts = 0; const u0 = st.unhandled;
  st.thrown = thrown; st.scope = r.scope || 'all';
  globalThis.fetch = (r.fetchThrows ? ((..._a: unknown[]) => { st.fetchCalls++; return thrown ? Promise.reject(thrown.v) : Promise.resolve({ ok: true, status: 200, json: async () => ({ url: 'stub', version: '1' }) }); }) : origFetch) as typeof fetch;
  const ac = new AbortController(); const to = setTimeout(() => ac.abort(), 1500);
  const headers: Record<string, string> = { 'content-type': 'application/json' }; if (role) headers.authorization = 'Bearer ' + role;
  let status: any, text: any;
  try { const res = await origFetch(`http://127.0.0.1:${port()}${r.p}`, { method: r.m, headers, body: r.m === 'GET' || r.m === 'DELETE' ? undefined : JSON.stringify(r.body ?? {}), signal: ac.signal }); status = res.status; text = (await res.text()).slice(0, 300); }
  catch { status = 'NO_RESPONSE'; text = null; }
  clearTimeout(to); await new Promise((r2) => setTimeout(r2, 60));
  globalThis.fetch = origFetch; st.thrown = undefined;
  return { status, text, queries: JSON.parse(JSON.stringify(st.queries)), emitted: [...st.emitted], logThrew: st.logThrew, unhandled: st.unhandled - u0, redisWrites: st.redisWrites, fetchCalls: st.fetchCalls, seedInserts: st.seedInserts };
}
const rows: any[] = [];
describe('gate138 probe', () => {
  for (const r of routes) for (const [tn, mk] of THROWN) {
    it(`${r.n} / ${tn}`, async () => { const o = await call(r, 'SYSTEM_ADMIN', mk ? { v: mk() } : undefined); rows.push({ route: r.n, thrown: tn, ...o }); });
  }
  for (const r of routes) for (const role of [null, 'USER', 'ORG_ADMIN', 'SYSTEM_ADMIN']) {
    it(`auth ${r.n} / ${role}`, async () => { const o = await call(r, role, undefined); rows.push({ route: r.n, thrown: 'AUTH:' + role, ...o }); });
  }
  afterAll(() => { fs.writeFileSync(OUT, rows.map((x) => JSON.stringify(x)).join('\n') + '\n'); srv.close(); });
});
