// KS-730 part A (originate routes/systemErrors.ts): a thrown error must
// ROUND 2 OF THIS FILE (Seat B 29th): #1182 covered the two unauthenticated ingest routes. The FOUR
// admin routes in the same router still returned `err.message` outside production, and none of them
// logged it — so deleting the ternary alone would have destroyed the diagnostic. All six now go
// through one local `fail500` helper, and the four new cells below are the other four routes in the
// same shape as A1-A4. Measured across the three files this ticket enumerates: 0 of 65 sites logged.
// never reach the 500 body in ANY NODE_ENV (the KS-727 doctrine), and its message must be logged server-side
// instead of being lost. The two routes are unauthenticated ingest paths; the router is mounted on a real
// loopback listener and driven with fetch (no auth stub needed - the mocked middleware is a pass-through).
const mockTrackError = jest.fn();
const mockLoggerError = jest.fn();
// KS-730 round 2: named so a throw can be aimed at ONE admin route at a time. Without these the four
// new cells could not tell which handler answered, and a shared jest.fn() would let one route's throw
// be credited to another's cell.
const mockGetErrorStats = jest.fn();
const mockGetRecentErrors = jest.fn();
const mockResolveError = jest.fn();
const mockResolveErrorsByService = jest.fn();

jest.mock('../services/errorTrackingService', () => ({
  trackError: mockTrackError,
  resolveErrorsByService: mockResolveErrorsByService,
  getErrorStats: mockGetErrorStats,
  getRecentErrors: mockGetRecentErrors,
  resolveError: mockResolveError,
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { systemErrorsRouter } from '../routes/systemErrors';

const LEAK = 'relation system_errors does not exist ks730-private-detail';
const NODE_ENVS = ['development', 'demo', 'test', undefined];
const INGEST_BODY = { service: 'ks730-svc', message: 'ks730 reported error' };
const CLIENT_BODY = { error: 'ks730 render error', source: 'ks730-frontend' };
const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
const ORIGINAL_NODE_ENV = process.env.NODE_ENV;

const app = express();
app.use('/api/system-errors', express.json(), systemErrorsRouter);
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
afterEach(() => setNodeEnv(ORIGINAL_NODE_ENV));

function setNodeEnv(value: string | undefined): void {
  if (value === undefined) delete process.env.NODE_ENV;
  else process.env.NODE_ENV = value;
}

async function post(path: string, body: object, nodeEnv: string | undefined, throwInService: boolean): Promise<{ status: number; text: string }> {
  setNodeEnv(nodeEnv);
  if (throwInService) mockTrackError.mockRejectedValueOnce(new Error(LEAK));
  const res = await fetch(baseUrl + '/api/system-errors' + path, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  return { status: res.status, text: await res.text() };
}

describe('KS-730 part A: the system-errors ingest routes never answer a 500 with err.message', () => {
  it('RED KS-730 A1: POST /ingest: the thrown message is not in the 500 body under development, demo, test or unset', async () => {
    for (const nodeEnv of NODE_ENVS) {
      const reply = await post('/ingest', INGEST_BODY, nodeEnv, true);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
    }
  });

  it('RED KS-730 A2: POST /client-errors: the thrown message is not in the 500 body under development, demo, test or unset', async () => {
    for (const nodeEnv of NODE_ENVS) {
      const reply = await post('/client-errors', CLIENT_BODY, nodeEnv, true);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
    }
  });

  it('RED KS-730 A3: POST /ingest: the thrown message is logged once, server-side', async () => {
    const reply = await post('/ingest', INGEST_BODY, 'development', true);
    expect(reply.status).toBe(500);
    expect(mockLoggerError.mock.calls).toEqual([['System error ingest failed', { error: LEAK }]]);
  });

  it('RED KS-730 A4: POST /client-errors: the thrown message is logged once, server-side', async () => {
    const reply = await post('/client-errors', CLIENT_BODY, 'development', true);
    expect(reply.status).toBe(500);
    expect(mockLoggerError.mock.calls).toEqual([['Client error ingest failed', { error: LEAK }]]);
  });

  it('control: under production both routes already answer the constant text, and the service was reached', async () => {
    const ingest = await post('/ingest', INGEST_BODY, 'production', true);
    const client = await post('/client-errors', CLIENT_BODY, 'production', true);
    expect([ingest.status, client.status]).toEqual([500, 500]);
    expect([JSON.parse(ingest.text), JSON.parse(client.text)]).toEqual([CONSTANT_BODY, CONSTANT_BODY]);
    expect(mockTrackError).toHaveBeenCalledTimes(2);
  });

  it('control: a 400 keeps its own authored message, and a 201 logs nothing', async () => {
    const refused = await post('/ingest', {}, 'development', false);
    expect(refused.status).toBe(400);
    expect(JSON.parse(refused.text).error.message).toBe('service and message are required');
    const accepted = await post('/client-errors', CLIENT_BODY, 'development', false);
    expect(accepted.status).toBe(201);
    expect(mockTrackError).toHaveBeenCalledTimes(1);
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  // ── KS-730 round 2: the FOUR ADMIN ROUTES in the same router ──────────────────────────────────
  // Each is driven by making ITS OWN service call throw, so a cell cannot pass because a different
  // handler answered. The table is the route, its HTTP verb, the service that throws, and the log
  // context `fail500` is expected to write.
  const ADMIN_ROUTES = [
    { label: 'GET /stats', method: 'GET', path: '/stats', mock: mockGetErrorStats, context: 'Error statistics read failed (GET /api/system-errors/stats)' },
    { label: 'GET /', method: 'GET', path: '/', mock: mockGetRecentErrors, context: 'Error list read failed (GET /api/system-errors)' },
    { label: 'PATCH /:errorId/resolve', method: 'PATCH', path: '/err-ks730/resolve', mock: mockResolveError, context: 'Error resolve failed (PATCH /api/system-errors/:errorId/resolve)' },
    { label: 'POST /resolve-by-service', method: 'POST', path: '/resolve-by-service', mock: mockResolveErrorsByService, context: 'Bulk error resolve failed (POST /api/system-errors/resolve-by-service)' },
  ] as const;

  async function callAdmin(route: (typeof ADMIN_ROUTES)[number], nodeEnv: string | undefined, throwInService: boolean): Promise<{ status: number; text: string }> {
    setNodeEnv(nodeEnv);
    if (throwInService) route.mock.mockRejectedValueOnce(new Error(LEAK));
    else route.mock.mockResolvedValueOnce({ ok: true });
    const res = await fetch(baseUrl + '/api/system-errors' + route.path, {
      method: route.method,
      headers: { 'content-type': 'application/json' },
      ...(route.method === 'GET' ? {} : { body: JSON.stringify({ service: 'ks730-svc' }) }),
    });
    return { status: res.status, text: await res.text() };
  }

  it.each(ADMIN_ROUTES)('RED KS-730 A5 $label: the thrown message is not in the 500 body under development, demo, test or unset', async (route) => {
    for (const nodeEnv of NODE_ENVS) {
      const reply = await callAdmin(route, nodeEnv, true);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
    }
  });

  it.each(ADMIN_ROUTES)('RED KS-730 A6 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
    const reply = await callAdmin(route, 'development', true);
    expect(reply.status).toBe(500);
    // The context is asserted as a VALUE, not merely "something was logged": a helper that logged a
    // constant string would satisfy a looser check and make every route's log indistinguishable.
    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
  });

  it('control KS-730: under production the four admin routes already answered the constant text', async () => {
    // So the four cells above are about the NON-production environments, which is where the leak was.
    for (const route of ADMIN_ROUTES) {
      const reply = await callAdmin(route, 'production', true);
      expect({ label: route.label, status: reply.status, body: JSON.parse(reply.text) })
        .toEqual({ label: route.label, status: 500, body: CONSTANT_BODY });
    }
  });

  it('control KS-730: a typed CLIENT error keeps its own authored text — the helper did not flatten every error', async () => {
    // The risk of a blanket helper is that it swallows messages a route MEANT to return. PATCH with a
    // missing body is a 400 the route authors itself, and it must still say what it says.
    setNodeEnv('development');
    const res = await fetch(baseUrl + '/api/system-errors/resolve-by-service', {
      method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({}),
    });
    const text = await res.text();
    expect(res.status).toBeGreaterThanOrEqual(400);
    expect(res.status).toBeLessThan(500);
    expect(text).not.toContain('Internal server error');
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-730: the LEAK string really is the thrown text, so a "not leaked" pass is not vacuous', () => {
    // If LEAK were absent from the thrown error, every `leaked: false` above would hold trivially.
    expect(new Error(LEAK).message).toBe(LEAK);
    expect(LEAK.length).toBeGreaterThan(20);
  });
});
