// KS-1346 part A (originate routes/systemErrors.ts): fail500 logged a NON-Error throw through String(),
// so a thrown plain object reached the log as [object Object] and its content was lost. The 500 BODY was
// already constant (KS-730); what this file pins is the LOG. The four admin routes go through fail500, so
// each is driven by making ITS OWN service call reject, on a real loopback listener, exactly as the KS-730
// part A cells do. Error and string throws must log exactly what they logged before.
const mockLoggerError = jest.fn();
const mockGetErrorStats = jest.fn();
const mockGetRecentErrors = jest.fn();
const mockResolveError = jest.fn();
const mockResolveErrorsByService = jest.fn();

jest.mock('../services/errorTrackingService', () => ({
  trackError: jest.fn(),
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

const DETAIL = 'ks1346-private-detail';
const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
const ROUTES = [
  { label: 'GET /stats', method: 'GET', path: '/stats', mock: mockGetErrorStats, context: 'Error statistics read failed (GET /api/system-errors/stats)' },
  { label: 'GET /', method: 'GET', path: '/', mock: mockGetRecentErrors, context: 'Error list read failed (GET /api/system-errors)' },
  { label: 'PATCH /:errorId/resolve', method: 'PATCH', path: '/err-ks1346/resolve', mock: mockResolveError, context: 'Error resolve failed (PATCH /api/system-errors/:errorId/resolve)' },
  { label: 'POST /resolve-by-service', method: 'POST', path: '/resolve-by-service', mock: mockResolveErrorsByService, context: 'Bulk error resolve failed (POST /api/system-errors/resolve-by-service)' },
] as const;

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

async function callWithThrow(route: (typeof ROUTES)[number], thrown: unknown): Promise<{ status: number; text: string; calls: unknown[][] }> {
  mockLoggerError.mockClear();
  route.mock.mockRejectedValueOnce(thrown);
  const res = await fetch(baseUrl + '/api/system-errors' + route.path, {
    method: route.method,
    headers: { 'content-type': 'application/json' },
    ...(route.method === 'GET' ? {} : { body: JSON.stringify({ service: 'ks1346-svc' }) }),
  });
  return { status: res.status, text: await res.text(), calls: mockLoggerError.mock.calls };
}

describe('KS-1346 part A: systemErrors fail500 keeps a non-Error throw readable in the log', () => {
  it.each(ROUTES)('RED KS-1346 A1 $label: a thrown plain object is logged with its content, once, under this route', async (route) => {
    const reply = await callWithThrow(route, { code: 'KS1346_OBJECT', detail: DETAIL });
    expect(reply.status).toBe(500);
    expect(reply.calls.length).toBe(1);
    const [context, meta] = reply.calls[0] as [string, { error: unknown }];
    expect(context).toBe(route.context);
    expect(typeof meta.error).toBe('string');
    expect({ hasDetail: String(meta.error).includes(DETAIL), hasCode: String(meta.error).includes('KS1346_OBJECT') }).toEqual({ hasDetail: true, hasCode: true });
  });

  it.each(ROUTES)('control KS-1346 A2 $label: the 500 body stays the constant text for an object throw', async (route) => {
    const reply = await callWithThrow(route, { code: 'KS1346_OBJECT', detail: DETAIL });
    expect({ status: reply.status, leaked: reply.text.includes(DETAIL) }).toEqual({ status: 500, leaked: false });
    expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
  });

  it('control KS-1346 A3: an Error throw still logs exactly its message', async () => {
    const reply = await callWithThrow(ROUTES[0], new Error(DETAIL));
    expect(reply.calls).toEqual([[ROUTES[0].context, { error: DETAIL }]]);
  });

  it('control KS-1346 A4: a string throw still logs exactly itself, not a quoted rendering', async () => {
    const reply = await callWithThrow(ROUTES[1], DETAIL);
    expect(reply.calls).toEqual([[ROUTES[1].context, { error: DETAIL }]]);
  });

  it('control KS-1346 A5: String() of the thrown object really is the lossy text, so A1 is not vacuous', () => {
    expect(String({ code: 'KS1346_OBJECT', detail: DETAIL })).toBe('[object Object]');
  });
});
