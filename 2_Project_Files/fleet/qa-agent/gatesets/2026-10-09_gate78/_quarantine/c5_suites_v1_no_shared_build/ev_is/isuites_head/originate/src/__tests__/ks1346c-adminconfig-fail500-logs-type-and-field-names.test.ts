// KS-1346 part C (originate routes/adminConfig.ts): fail500 logged a NON-Error throw through String(),
// so a thrown plain object reached the log as [object Object] and its content was lost. The 500 BODY was
// already constant (KS-730); what this file pins is the LOG. Fifty admin-config sites go through the one
// fail500 helper; four GET routes are driven end to end, each by making its own prisma.$queryRaw reject,
// on a real loopback listener, exactly as the KS-730 part C cells do. Error and string throws must log
// exactly what they logged before.
// Kam ruled 2026-09-27 (card secuura-ks1346-logging-thrown-objects-leaks-secrets, option a): a non-Error,
// non-string throw is logged as its TYPE and FIELD NAMES only, never its values, so no secret reaches the log.
process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();
const mockLoggerError = jest.fn();

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
      const principal = { id: 'u-ks1346c', role: 'SYSTEM_ADMIN', tenantId: 't-ks1346c' };
      req._secuuraUser = principal; req.user = principal; req.tenantId = principal.tenantId;
      next();
    },
    requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  };
});

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    ...(jest.requireActual('@secuura/shared') as Record<string, unknown>),
    runWithPlatformScope: (fn: () => unknown) => fn(),
    queryWithTenantGuc: jest.fn(),
  }),
);

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { adminConfigRouter } from '../routes/adminConfig';

const DETAIL = 'ks1346c-private-detail';
const SECRET = 'ks1346c-secret-value';
const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
const ROUTES = [
  { label: 'GET /settings', path: '/settings', context: 'Admin config request failed (GET /api/admin/settings)' },
  { label: 'GET /document-types', path: '/document-types', context: 'Admin config request failed (GET /api/admin/document-types)' },
  { label: 'GET /workflows', path: '/workflows', context: 'Admin config request failed (GET /api/admin/workflows)' },
  { label: 'GET /organizations', path: '/organizations', context: 'Admin config request failed (GET /api/admin/organizations)' },
] as const;

const app = express();
app.use('/api/admin', express.json(), adminConfigRouter);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => server?.close());
beforeEach(() => jest.clearAllMocks());

async function callWithThrow(route: (typeof ROUTES)[number], thrown: unknown): Promise<{ status: number; text: string; calls: unknown[][] }> {
  mockLoggerError.mockClear();
  mockQueryRaw.mockRejectedValueOnce(thrown);
  const res = await fetch(baseUrl + '/api/admin' + route.path);
  return { status: res.status, text: await res.text(), calls: mockLoggerError.mock.calls };
}

describe('KS-1346 part C: adminConfig fail500 keeps a non-Error throw readable in the log', () => {
  it.each(ROUTES)('RED KS-1346 C1 $label: a thrown plain object is logged as its type and field names, once, under this route', async (route) => {
    const reply = await callWithThrow(route, { code: 'KS1346C_OBJECT', detail: DETAIL, password: SECRET });
    expect(reply.status).toBe(500);
    expect(reply.calls.length).toBe(1);
    const [context, meta] = reply.calls[0] as [string, { error: unknown }];
    expect(context).toBe(route.context);
    expect(meta.error).toBe('thrown Object with fields [code, detail, password]');
  });

  it.each(ROUTES)('control KS-1346 C6 $label: no VALUE of a thrown object reaches the log', async (route) => {
    const reply = await callWithThrow(route, { code: 'KS1346C_OBJECT', detail: DETAIL, password: SECRET });
    const logged = JSON.stringify(reply.calls);
    expect({ secret: logged.includes(SECRET), detail: logged.includes(DETAIL), code: logged.includes('KS1346C_OBJECT') }).toEqual({ secret: false, detail: false, code: false });
  });

  it.each(ROUTES)('control KS-1346 C2 $label: the 500 body stays the constant text for an object throw', async (route) => {
    const reply = await callWithThrow(route, { code: 'KS1346C_OBJECT', detail: DETAIL });
    expect({ status: reply.status, leaked: reply.text.includes(DETAIL) }).toEqual({ status: 500, leaked: false });
    expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
  });

  it('control KS-1346 C3: an Error throw still logs exactly its message', async () => {
    const reply = await callWithThrow(ROUTES[0], new Error(DETAIL));
    expect(reply.calls).toEqual([[ROUTES[0].context, { error: DETAIL }]]);
  });

  it('control KS-1346 C4: a string throw still logs exactly itself, not a quoted rendering', async () => {
    const reply = await callWithThrow(ROUTES[1], DETAIL);
    expect(reply.calls).toEqual([[ROUTES[1].context, { error: DETAIL }]]);
  });

  it('control KS-1346 C5: String() of the thrown object really is the lossy text, so C1 is not vacuous', () => {
    expect(String({ code: 'KS1346C_OBJECT', detail: DETAIL })).toBe('[object Object]');
  });
});
