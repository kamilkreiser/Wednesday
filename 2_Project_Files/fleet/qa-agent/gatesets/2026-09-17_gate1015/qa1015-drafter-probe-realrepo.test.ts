/**
 * qa1015-drafter-probe-realrepo — DRAFTER probe: REAL userRoutes + REAL userRepo + REAL errorHandler over 127.0.0.1:0, db.query rejecting
 * EVERY statement (F-all: a total outage), subjectDeks stubbed with a hit witness. Records the three routes' status/body per tree.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import express from 'express';
import fs from 'node:fs';
const st = vi.hoisted(() => ({ caller: { userId: 'aaaaaaaa-2222-4222-8222-aaaaaaaaaaaa', role: 'USER', tenantId: 'tenant-default' } as Record<string, string>, sql: [] as string[], dek: 0 }));
vi.mock('../middleware/authenticate', () => {
  const inject = () => (req: any, _res: any, next: any) => { req.user = { ...st.caller }; next(); };
  return { authenticate: inject, authenticateAccessOrConnector: inject };
});
vi.mock('../db', () => ({ isDbAvailable: () => true, query: vi.fn(async (sql: string) => { st.sql.push(String(sql).replace(/\s+/g, ' ').slice(0, 60)); throw Object.assign(new Error('connect ECONNREFUSED 127.0.0.1:5432'), { code: 'ECONNREFUSED' }); }), getPool: vi.fn(), transaction: vi.fn() }));
vi.mock('../services/subjectDeks', () => ({ subjectDeks: { getDek: vi.fn(async () => { st.dek++; return null; }) } }));
vi.mock('../services/session', () => ({ revokeAllUserSessions: vi.fn(async () => 0) }));
vi.mock('../utils/logger', () => ({ logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() } }));
import { userRoutes } from '../routes/users';
import { errorHandler } from '../middleware/errorHandler';
let server: Server; let base = ''; const rows: unknown[] = [];
beforeAll(async () => { const app = express(); app.use(express.json()); app.use('/', userRoutes); app.use(errorHandler);
  await new Promise<void>(r => { server = app.listen(0, '127.0.0.1', () => { base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`; r(); }); }); });
afterAll(async () => { await new Promise<void>(r => server.close(() => r())); fs.writeFileSync(process.env.QA_PROBE_OUT as string, JSON.stringify(rows, null, 1)); });
async function call(scn: string, method: string, path: string, body?: unknown) {
  st.sql.length = 0;
  const res = await fetch(base + path, { method, headers: body ? { 'Content-Type': 'application/json' } : {}, body: body ? JSON.stringify(body) : undefined });
  rows.push({ scn, status: res.status, body: (await res.text()).slice(0, 200), sql: [...st.sql], dek: st.dek });
}
describe('qa1015 real-repo F-all', () => { it('records', async () => {
  await call('GET /me/verification F-all (USER)', 'GET', '/me/verification');
  await call('POST /me/verification F-all (USER)', 'POST', '/me/verification', { targetLevel: 'ENHANCED' });
  st.caller = { userId: 'bbbbbbbb-2222-4222-8222-bbbbbbbbbbbb', role: 'SYSTEM_ADMIN', tenantId: 'tenant-default' };
  await call('review F-all (SYSTEM_ADMIN)', 'POST', '/verification/vr-x/review', { action: 'approve' });
  st.caller = { userId: 'bbbbbbbb-2222-4222-8222-bbbbbbbbbbbb', role: 'ORG_ADMIN', tenantId: 'tenant-default' };
  await call('review F-all (ORG_ADMIN)', 'POST', '/verification/vr-x/review', { action: 'approve' });
  expect(rows.length).toBe(4);
}); });
