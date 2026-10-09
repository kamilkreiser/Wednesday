/**
 * KS-1206 - the originate admin API-key mint refuses a rateLimit outside 1..10000.
 *
 * POST /api/admin/api-keys stored d.rateLimit || 1000 with no bounds, so a key minted with rateLimit -1
 * answered 429 on every request once the per-key limiter fired (KS-1195). The security service bounds
 * the same field on its own create path to an integer from 1 to 10000. This mint now does the same and
 * answers 400 BAD_REQUEST before the INSERT. An absent rateLimit still gets the 1000 default.
 *
 * Harness: the ks764 suite's pattern. The real adminConfigRouter and the real requireRole,
 * authenticate stubbed, the database stubbed ($queryRaw is the INSERT ... RETURNING, counted).
 */
process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw, $executeRaw: jest.fn() },
  refreshTenantConfigs: jest.fn(),
  withTenant: (_t: unknown, fn: () => unknown) => fn(),
  getTenantManager: () => null,
}));
jest.mock('../middleware/auth', () => {
  const actual = jest.requireActual('../middleware/auth');
  return {
    ...actual,
    authenticate: () => (req: any, _res: unknown, next: () => void) => {
      const principal = JSON.parse(String(req.headers['x-test-principal'] || '{}'));
      req._secuuraUser = principal;
      req.user = principal;
      if (principal.tenantId) req.tenantId = principal.tenantId;
      next();
    },
  };
});
jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    ...(jest.requireActual('@secuura/shared') as Record<string, unknown>),
    runWithPlatformScope: (fn: () => unknown) => fn(),
    queryWithTenantGuc: jest.fn(),
  }),
);

import express from 'express';
import { adminConfigRouter } from '../routes/adminConfig';

const TENANT = 'a0000000-0000-4000-8000-000000001206';
const PLATFORM = { userId: 'u1206', role: 'super_admin', tenantId: TENANT };

const app = express();
app.use(express.json());
app.use('/api/admin', adminConfigRouter);
let base = '';
let server: ReturnType<typeof app.listen>;
beforeAll(async () => {
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  const a = server.address();
  base = 'http://127.0.0.1:' + String(typeof a === 'object' && a ? a.port : 0);
});
afterAll(() => { server?.close(); });
beforeEach(() => {
  mockQueryRaw.mockReset();
  mockQueryRaw.mockResolvedValue([{ id: 'key_1206', key_prefix: 'sk_120600000', name: 'ks1206', scopes: ['read'], rate_limit: 1000, is_active: true, expires_at: null, created_at: '2026-09-19T00:00:00Z' }]);
});

/** POST /api/admin/api-keys as the platform admin; returns the status, the error code and how many INSERTs ran. */
async function mint(body: Record<string, unknown>) {
  const res = await fetch(base + '/api/admin/api-keys', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-test-principal': JSON.stringify(PLATFORM) },
    body: JSON.stringify(body),
  });
  const j: any = await res.json().catch(() => null);
  return { status: res.status, code: j?.error?.code ?? null, inserts: mockQueryRaw.mock.calls.length };
}

describe('KS-1206 the admin API-key mint bounds rateLimit to an integer from 1 to 10000', () => {
  it('control: no rateLimit still mints with the default, one INSERT', async () => {
    const r = await mint({ name: 'ks1206' });
    expect([r.status, r.inserts]).toEqual([201, 1]);
  });

  it('control: rateLimit 10000, the upper bound, still mints, one INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: 10000 });
    expect([r.status, r.inserts]).toEqual([201, 1]);
  });

  it('control: a missing name is still refused 400 with no INSERT', async () => {
    const r = await mint({ rateLimit: 100 });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });

  it('🔴 KS-1206: rateLimit -1 is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: -1 });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });

  it('🔴 KS-1206: rateLimit 10001, above the bound, is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: 10001 });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });

  it('🔴 KS-1206: a string rateLimit is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: 'abc' });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N61-1: rateLimit null is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: null });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N61-1: rateLimit 0 is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: 0 });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N61-1: a fractional rateLimit (1.5) is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: 1.5 });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N61-1: a numeric-string rateLimit (100 as a string) is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: '100' });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N61-1: rateLimit 1, the lower bound, still mints, one INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: 1 });
    expect([r.status, r.inserts]).toEqual([201, 1]);
  });
  it('RED KS-1206 N72-1: rateLimit false is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: false });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N72-1: an empty-string rateLimit is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: '' });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N72-1: rateLimit true is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: true });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N72-1: an array rateLimit is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: [] });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N72-1: an object rateLimit is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: {} });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N81-1: rateLimit Infinity (1e999 in the raw JSON body) is refused 400 before the INSERT', async () => {
    const inf = await fetch(base + '/api/admin/api-keys', { method: 'POST', headers: { 'content-type': 'application/json', 'x-test-principal': JSON.stringify(PLATFORM) }, body: '{"name":"ks1206","rateLimit":1e999}' });
    const infBody: any = await inf.json().catch(() => null);
    expect([inf.status, infBody?.error?.code ?? null, mockQueryRaw.mock.calls.length]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N81-1: a space-padded numeric-string rateLimit (" 100") is refused 400 before the INSERT', async () => {
    const r = await mint({ name: 'ks1206', rateLimit: ' 100' });
    expect([r.status, r.code, r.inserts]).toEqual([400, 'BAD_REQUEST', 0]);
  });
  it('RED KS-1206 N81-1: rateLimit -0 (-0 in the raw JSON body) is refused 400 before the INSERT', async () => {
    const negz = await fetch(base + '/api/admin/api-keys', { method: 'POST', headers: { 'content-type': 'application/json', 'x-test-principal': JSON.stringify(PLATFORM) }, body: '{"name":"ks1206","rateLimit":-0}' });
    const negzBody: any = await negz.json().catch(() => null);
    expect([negz.status, negzBody?.error?.code ?? null, mockQueryRaw.mock.calls.length]).toEqual([400, 'BAD_REQUEST', 0]);
  });
});
