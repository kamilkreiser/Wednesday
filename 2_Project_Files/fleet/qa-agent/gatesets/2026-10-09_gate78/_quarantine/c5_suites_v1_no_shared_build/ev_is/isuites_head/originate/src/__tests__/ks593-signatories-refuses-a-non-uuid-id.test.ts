// KS-593 (not_a_server_error register; the ninth operation, GET /api/signatories, measured 2026-08-28):
// `?organizationId=abc` passed the route's validator (isString + notEmpty only) and reached
// `s.organization_id = ${organizationId}::uuid`, where Postgres refuses it (22P02) and the catch answers
// 500 INTERNAL_ERROR. GET /api/signatories/check casts organizationId AND userId the same way. The fix adds
// isUUID() to those three validators, so a malformed id is a 400 from the route's own validationResult
// branch and no query runs. Harness: the real signatoriesRouter on a loopback listener, prisma mocked,
// authenticate() stubbed. No database, no network beyond 127.0.0.1.
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw },
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: 'u-ks593-sig', email: 'sig@example.test', role: 'ORG_ADMIN' };
    next();
  },
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { signatoriesRouter } from '../routes/signatories';

const ORG = 'a0000000-0000-4000-8000-000000000001';
const USER = 'b0000000-0000-4000-8000-000000000002';

const app = express();
app.use('/api/signatories', express.json(), signatoriesRouter);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';

beforeAll(async () => {
  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', () => resolve()); });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => {
  server?.close();
});
beforeEach(() => {
  jest.clearAllMocks();
  mockQueryRaw.mockResolvedValue([]);
});

async function get(pathAndQuery: string): Promise<{ status: number; body: any }> {
  const res = await fetch(baseUrl + '/api/signatories' + pathAndQuery);
  return { status: res.status, body: await res.json() };
}

describe('KS-593: the signatory list and check routes refuse a non-UUID id with 400 before any query runs', () => {
  it('RED KS-593 SG1: GET /api/signatories?organizationId=abc answers 400 and runs no query', async () => {
    const r = await get('/?organizationId=abc');
    expect(r.status).toBe(400);
    expect(r.body.success).toBe(false);
    expect(mockQueryRaw).not.toHaveBeenCalled();
  });

  it('RED KS-593 SG2: GET /api/signatories/check with a non-UUID organizationId answers 400 and runs no query', async () => {
    const r = await get('/check?organizationId=abc&userId=' + USER);
    expect(r.status).toBe(400);
    expect(mockQueryRaw).not.toHaveBeenCalled();
  });

  it('RED KS-593 SG3: GET /api/signatories/check with a non-UUID userId answers 400 and runs no query', async () => {
    const r = await get('/check?organizationId=' + ORG + '&userId=abc');
    expect(r.status).toBe(400);
    expect(mockQueryRaw).not.toHaveBeenCalled();
  });

  it('control KS-593 SGC1: a well-formed organizationId still lists (200) and runs the query once', async () => {
    const r = await get('/?organizationId=' + ORG);
    expect(r.status).toBe(200);
    expect(r.body).toEqual({ success: true, signatories: [], total: 0 });
    expect(mockQueryRaw).toHaveBeenCalledTimes(1);
  });

  it('control KS-593 SGC2: a well-formed check still answers 200 authorised false when no row matches', async () => {
    const r = await get('/check?organizationId=' + ORG + '&userId=' + USER);
    expect(r.status).toBe(200);
    expect(r.body).toEqual({ success: true, authorised: false });
    expect(mockQueryRaw).toHaveBeenCalledTimes(1);
  });

  it('control KS-593 SGC3: a missing organizationId is still refused with 400', async () => {
    const r = await get('/');
    expect(r.status).toBe(400);
    expect(mockQueryRaw).not.toHaveBeenCalled();
  });
});
