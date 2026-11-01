// Gate 98 probe: REAL createAdminRoutes on a REAL express listener (loopback), REAL requireAdmin/ADMIN_ROLES/mockBodyParser;
// replaced: verifyToken (auth context), query (DB), log, redisService stub.
import { describe, it, expect, afterAll } from 'vitest';
import express from 'express';
import fs from 'fs';
import type { AddressInfo } from 'net';
import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';

const OUT = process.env.PROBE_OUT as string;
const st = { thrown: undefined as { v: unknown } | undefined, queries: [] as any[], logs: [] as any[], unhandled: 0 };
process.on('unhandledRejection', () => { st.unhandled++; });
const revoked = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const getterErr = () => Object.create(Error.prototype, { message: { get() { throw new Error('g'); } } });
const deps = {
  authenticateToken: () => (_q: any, _r: any, n: any) => n(),
  verifyToken: (t: string) => ({ userId: 'u', email: 'e@x', role: t, verificationLevel: 'HIGH' }),
  isDbAvailable: () => false,
  redisService: {}, services: {},
  query: (text: string, params?: unknown[]) => { st.queries.push({ text: text.trim().slice(0, 40), params }); if (st.thrown) return Promise.reject(st.thrown.v); return Promise.resolve({ rows: [{ id: 'x' }], rowCount: 1 }); },
  log: (level: string, message: string, meta?: any) => { let m: string; try { m = JSON.stringify(meta); } catch { m = 'unserialisable'; } st.logs.push({ level, message, meta: m }); },
} as unknown as AdminRouteDeps;
const app = express(); app.use(createAdminRoutes(deps));
const srv = app.listen(0, '127.0.0.1');
const port = () => (srv.address() as AddressInfo).port;
const ID = 'd5800000-0000-4000-8000-000000000001';
const routes = [
  { n: 'GET users', m: 'GET', p: '/api/admin/identity/users' },
  { n: 'GET orgs', m: 'GET', p: '/api/admin/identity/organizations' },
  { n: 'PATCH level', m: 'PATCH', p: `/api/admin/identity/users/${ID}/level` },
];
const thrown: Array<[string, (() => unknown) | null]> = [['ok', null], ['Error', () => new Error('db boom 10.0.0.7')], ['string', () => 'plain'], ['revokedProxy', revoked], ['getterError', getterErr]];
async function call(r: typeof routes[0], role: string | null, body?: unknown) {
  st.queries.length = 0; st.logs.length = 0; const u0 = st.unhandled;
  const ac = new AbortController(); const to = setTimeout(() => ac.abort(), 1500);
  const headers: any = { 'content-type': 'application/json' }; if (role) headers.authorization = 'Bearer ' + role;
  let status: any, text: any;
  try { const res = await fetch(`http://127.0.0.1:${port()}${r.p}`, { method: r.m, headers, body: r.m === 'GET' ? undefined : JSON.stringify(body ?? { verificationLevel: 'HIGH' }), signal: ac.signal }); status = res.status; text = await res.text(); }
  catch { status = 'NO_RESPONSE'; text = null; }
  clearTimeout(to); await new Promise(r2 => setTimeout(r2, 50));
  return { status, text, queries: JSON.parse(JSON.stringify(st.queries)), logs: JSON.parse(JSON.stringify(st.logs)), unhandled: st.unhandled - u0 };
}
const rows: any[] = [];
describe('gate98 probe', () => {
  for (const r of routes) for (const [tn, mk] of thrown) {
    it(`${r.n} / ${tn}`, async () => { st.thrown = mk ? { v: mk() } : undefined; const o = await call(r, 'SYSTEM_ADMIN'); rows.push({ route: r.n, thrown: tn, ...o }); st.thrown = undefined; });
  }
  for (const r of routes) for (const role of [null, 'USER', 'ORG_ADMIN', 'ISSUER_ADMIN', 'SYSTEM_ADMIN']) {
    it(`auth ${r.n} / ${role}`, async () => { st.thrown = undefined; const o = await call(r, role); rows.push({ route: r.n, thrown: 'AUTH:' + role, ...o }); });
  }
  it('PATCH bad level 400 unchanged', async () => { const o = await call(routes[2], 'SYSTEM_ADMIN', { verificationLevel: 'NOPE' }); rows.push({ route: 'PATCH level', thrown: 'BADLEVEL', ...o }); });
  afterAll(() => { fs.writeFileSync(OUT, rows.map(x => JSON.stringify(x)).join('\n') + '\n'); srv.close(); });
});
