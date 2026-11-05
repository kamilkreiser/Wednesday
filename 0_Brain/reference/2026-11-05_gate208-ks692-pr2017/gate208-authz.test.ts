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

describe('gate208 Q2/Q4 authorization table', () => {
  for (const op of ['revoke', 'unrevoke'] as const) {
    for (const [credName, owner] of Object.entries(CREDS)) {
      for (const [callerName, caller] of Object.entries(CALLERS)) {
        it(`${op} ${credName} ${callerName}`, async () => {
          const list = await freshList();
          const cid = `https://secuura.io/credentials/g208-${op}-${credName}-${callerName}-${seq}`;
          const a = await call('POST', `/api/status/${list}/allocate`, ALLOCATOR, { credentialId: cid });
          expect(a.status).toBe(200);
          if (owner !== 'not_stored') await repo.store({ id: cid, type: ['VerifiableCredential'] } as any, owner);
          // pre-state for unrevoke: revoked, set directly on the manager (no route, so identical on base and head)
          const mgr = allocSpy.mock.instances[allocSpy.mock.instances.length - 1];
          const before = await call('GET', `/api/status/${list}/revoked`, ALLOCATOR);
          if (op === 'unrevoke') {
            mgr.revoke(cid, 'pre');
          }
          const pre = await call('GET', `/api/status/${list}/revoked`, ALLOCATOR);
          revokeSpy.mockClear(); unrevokeSpy.mockClear();
          const r = await call('POST', `/api/status/${list}/${op}`, caller, { credentialId: cid, reason: 'g208-r' });
          const writes = revokeSpy.mock.calls.length + unrevokeSpy.mock.calls.length;
          const post = await call('GET', `/api/status/${list}/revoked`, ALLOCATOR);
          // not-in-list control in the same list for the identical-404 comparison
          const ctl = await call('POST', `/api/status/${list}/${op}`, caller, { credentialId: 'https://secuura.io/credentials/g208-never-allocated', reason: 'g208-r' });
          rec({ kind: 'cell', op, cred: credName, caller: callerName, status: r.status, body: r.body, headers: r.headers, ms: r.ms,
            writes, stateChanged: pre.body !== post.body, before: before.body, pre: pre.body, post: post.body,
            ctlStatus: ctl.status, ctlBody: ctl.body, ctlHeaders: ctl.headers, ctlMs: ctl.ms });
        });
      }
    }
  }
});

describe('gate208 Q3 gate exemption path tricks (non-platform signed-in OWNER, creator of the credential, and anonymous)', () => {
  const tricks: Array<[string, string, string, Record<string, string>?]> = [
    ['plain revoke', 'POST', '/api/status/LIST/revoke'],
    ['plain unrevoke', 'POST', '/api/status/LIST/unrevoke'],
    ['trailing slash', 'POST', '/api/status/LIST/revoke/'],
    ['upper case REVOKE', 'POST', '/api/status/LIST/REVOKE'],
    ['mixed case UnRevoke', 'POST', '/api/status/LIST/UnRevoke'],
    ['query smuggle on allocate', 'POST', '/api/status/LIST/allocate?x=/a/revoke'],
    ['encoded slash in id (LIST%2Fx)', 'POST', '/api/status/LIST%2Fx/revoke'],
    ['encoded slash before revoke (LIST%2Frevoke)', 'POST', '/api/status/LIST%2Frevoke'],
    ['double slash before id', 'POST', '/api/status//LIST/revoke'],
    ['double slash before revoke', 'POST', '/api/status/LIST//revoke'],
    ['trailing extra segment', 'POST', '/api/status/LIST/revoke/extra'],
    ['two segments before', 'POST', '/api/status/a/LIST/revoke'],
    ['revoke on root (no id)', 'POST', '/api/status/revoke'],
    ['dot segment', 'POST', '/api/status/LIST/./revoke'],
    ['dotdot to allocate', 'POST', '/api/status/LIST/revoke/../allocate'],
    ['revokeX suffix', 'POST', '/api/status/LIST/revokeX'],
    ['encoded r (%72evoke)', 'POST', '/api/status/LIST/%72evoke'],
    ['matrix ;', 'POST', '/api/status/LIST/revoke;x'],
    ['allocate (different POST)', 'POST', '/api/status/LIST/allocate'],
    ['create list (different POST)', 'POST', '/api/status'],
    ['PUT revoke', 'PUT', '/api/status/LIST/revoke'],
    ['DELETE revoke', 'DELETE', '/api/status/LIST/revoke'],
    ['PATCH revoke', 'PATCH', '/api/status/LIST/revoke'],
    ['method override header to allocate', 'POST', '/api/status/LIST/allocate', { 'x-http-method-override': 'GET' }],
    ['method override header on revoke', 'POST', '/api/status/LIST/revoke', { 'x-http-method-override': 'GET' }],
  ];
  for (const [name, method, tpl, hdrs] of tricks) {
    for (const [cname, caller] of [['creator', CALLERS.creator], ['other_tenant_OWNER', CALLERS.other_tenant_OWNER], ['anonymous', undefined]] as const) {
      it(`${name} as ${cname}`, async () => {
        const list = await freshList();
        const cid = `https://secuura.io/credentials/g208-trick-${seq}`;
        expect((await call('POST', `/api/status/${list}/allocate`, ALLOCATOR, { credentialId: cid })).status).toBe(200);
        await repo.store({ id: cid, type: ['VerifiableCredential'] } as any, { userId: 'g208-alice', tenantId: T1 });
        revokeSpy.mockClear(); unrevokeSpy.mockClear();
        const listsBefore = await call('GET', '/api/status', ALLOCATOR);
        const r = await call(method, tpl.replace('LIST', list), caller, { credentialId: cid, id: `g208-created-${seq}` }, hdrs || {});
        const listsAfter = await call('GET', '/api/status', ALLOCATOR);
        rec({ kind: 'trick', name, caller: cname, method, path: tpl, status: r.status, body: r.body.slice(0, 200),
          writes: revokeSpy.mock.calls.length + unrevokeSpy.mock.calls.length, listsChanged: listsBefore.body !== listsAfter.body });
      });
    }
  }
});
