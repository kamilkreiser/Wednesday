/**
 * GATE 208 (QA, KS-692 PR 2017): independent authorization table + gate-exemption path tricks.
 * Real express app over real HTTP (127.0.0.1, ephemeral port): express.json, a stand-in for jwtAuthenticate that
 * puts the principal from the x-gate-user header on req.user (absent header = anonymous), the REAL statusRoutes at
 * /api/status, the index.ts 404 fallback shape, the REAL errorHandler. Only storage is doubled: ../db reports
 * unavailable, so credentialRepo uses its in-memory store + owner map (the fallback path the product also runs).
 * Writes are counted with spies on StatusListManager.prototype.revoke/unrevoke (the only status mutations).
 * Output: one JSON line per cell to process.env.GATE_OUT.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import fs from 'fs';
import http from 'http';
import type { AddressInfo } from 'net';

const dbMock = vi.hoisted(() => ({ isDbAvailable: () => false, query: async () => ({ rows: [] }) }));
vi.mock('../db', () => ({ isDbAvailable: () => dbMock.isDbAvailable(), query: () => dbMock.query() }));
const loggerMock = vi.hoisted(() => ({ info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() }));
vi.mock('../utils/logger', () => ({ logger: loggerMock }));

const OUT = process.env.GATE_OUT || '/dev/null';
const rec = (o: unknown) => fs.appendFileSync(OUT, JSON.stringify(o) + '\n');

const T1 = 'g208-t1';
const T2 = 'g208-t2';
const who = (userId: string, tenantId: string | undefined, role: string) => ({ userId, ...(tenantId ? { tenantId } : {}), role, email: `${userId}@g208.test` });
const CALLERS: Record<string, any> = {
  anonymous: undefined,
  creator: who('g208-alice', T1, 'OWNER'),
  same_tenant_noncreator_OWNER: who('g208-bob', T1, 'OWNER'),
  same_tenant_ISSUER_ADMIN: who('g208-ia1', T1, 'ISSUER_ADMIN'),
  same_tenant_ORG_ADMIN: who('g208-oa1', T1, 'ORG_ADMIN'),
  other_tenant_OWNER: who('g208-carol', T2, 'OWNER'),
  other_tenant_ISSUER_ADMIN: who('g208-ia2', T2, 'ISSUER_ADMIN'),
  SYSTEM_ADMIN_own_tenant: who('g208-sa1', T1, 'SYSTEM_ADMIN'),
  SYSTEM_ADMIN_other_tenant: who('g208-sa2', T2, 'SYSTEM_ADMIN'),
  SUPER_ADMIN_own_tenant: who('g208-su1', T1, 'SUPER_ADMIN'),
  legacy_super_admin_own_tenant: who('g208-lsu1', T1, 'super_admin'),
};
const ALLOCATOR = who('g208-allocator', T2, 'SYSTEM_ADMIN');
// owner-less-with-tenant credential belongs to T1 (the "own tenant" of the SYSTEM_ADMIN_own_tenant caller)
const CREDS: Record<string, { userId: string | null; tenantId: string | null } | 'not_stored'> = {
  owned_by_creator: { userId: 'g208-alice', tenantId: T1 },
  ownerless_with_tenant: { userId: null, tenantId: T1 },
  ownerless_without_tenant: { userId: null, tenantId: null },
  not_stored: 'not_stored',
};

let server: http.Server;
let base = '';
let mgrProto: any;
let revokeSpy: any;
let unrevokeSpy: any;
let allocSpy: any;
let repo: any;

type Rep = { status: number; body: string; headers: Record<string, string>; ms: number };
function call(method: string, path: string, user: any, body?: unknown, extraHeaders: Record<string, string> = {}): Promise<Rep> {
  return new Promise((resolve, reject) => {
    const data = body === undefined ? undefined : JSON.stringify(body);
    const t0 = Date.now();
    const req = http.request(base + path, {
      method,
      headers: {
        ...(data ? { 'content-type': 'application/json', 'content-length': String(Buffer.byteLength(data)) } : {}),
        ...(user ? { 'x-gate-user': JSON.stringify(user) } : {}),
        ...extraHeaders,
      },
    }, (res) => {
      let b = '';
      res.on('data', (c) => (b += c));
      res.on('end', () => {
        const h: Record<string, string> = {};
        for (const [k, v] of Object.entries(res.headers)) if (k !== 'date') h[k] = String(v);
        resolve({ status: res.statusCode || 0, body: b, headers: h, ms: Date.now() - t0 });
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

let seq = 0;
async function freshList(): Promise<string> {
  const id = `g208-list-${++seq}`;
  const r = await call('POST', '/api/status', ALLOCATOR, { id });
  expect(r.status).toBe(201);
  return id;
}

beforeAll(async () => {
  const express = (await import('express')).default;
  const { statusRoutes } = await import('../routes/status');
  const { errorHandler } = await import('../middleware/errorHandler');
  repo = await import('../repositories/credentialRepo');
  const vc: any = await import('@secuura/shared/vc');
  mgrProto = vc.StatusListManager.prototype;
  revokeSpy = vi.spyOn(mgrProto, 'revoke');
  unrevokeSpy = vi.spyOn(mgrProto, 'unrevoke');
  allocSpy = vi.spyOn(mgrProto, 'allocateIndex');
  const app = express();
  app.use(express.json());
  app.use('/api', (req: any, _res: any, next: any) => {
    const h = req.headers['x-gate-user'];
    if (h) req.user = JSON.parse(String(h));
    next();
  });
  app.use('/api/status', statusRoutes);
  app.use((req: any, res: any) => res.status(404).json({ error: 'Not Found', path: req.path }));
  app.use(errorHandler);
  server = app.listen(0, '127.0.0.1');
  await new Promise((r) => server.once('listening', r));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}, 180000);
afterAll(async () => { if (server) await new Promise((r) => server.close(r)); });

describe('gate208 Q6 systemTest bodies', () => {
  for (const [path, body] of [['/api/status/default/revoke', { index: 0, reason: 'KS-588 probe' }], ['/api/status/default/unrevoke', { index: 0 }], ['/api/status/default/allocate', {}], ['/api/status', { id: 'ks588-probe-list', purpose: 'revocation' }]] as const) {
    it(path, async () => {
      const r = await call('POST', path, CALLERS.same_tenant_ISSUER_ADMIN, body);
      rec({ kind: 'q6', path, body, status: r.status, resp: r.body });
    });
  }
});
