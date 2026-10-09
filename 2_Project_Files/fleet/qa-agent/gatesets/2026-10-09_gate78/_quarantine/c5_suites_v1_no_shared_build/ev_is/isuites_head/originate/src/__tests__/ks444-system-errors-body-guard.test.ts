/**
 * KS-444 — /api/system-errors write-route body guards.
 *
 * The three write routes truthy-checked (or didn't check) their bodies, so
 * spec-violating shapes were accepted (verified live 2026-07-13):
 *   - POST /ingest stored `metadata` sent as an array → 201
 *   - POST /client-errors stored `source: {}` → 201
 *   - POST /resolve-by-service answered 200 to `service: {}`
 * The handlers now validate against the published request schemas
 * (originate.openapi.ts) and 400 with the KS-267-style envelope. The ingest
 * severity enum is the platform's real domain (warning/error/critical — the
 * errorTrackingService union + the KS-267 list filter), which the spec was
 * corrected to in the same change.
 */

const mockTrackError = jest.fn();
const mockResolveErrorsByService = jest.fn();

jest.mock('../services/errorTrackingService', () => ({
  trackError: mockTrackError,
  resolveErrorsByService: mockResolveErrorsByService,
  getErrorStats: jest.fn(),
  getRecentErrors: jest.fn(),
  resolveError: jest.fn(),
}));

jest.mock('../middleware/auth', () => ({
  // Auth/RBAC are not under test — pass everything through.
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));

import express from 'express';
import { systemErrorsRouter } from '../routes/systemErrors';

const app = express();
app.use('/api/system-errors', express.json(), systemErrorsRouter);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => server?.close());
beforeEach(() => jest.clearAllMocks());

/** Helper: POST a JSON body to a system-errors subpath and return the response. */
function post(path: string, body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/system-errors${path}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

/** Canonical error-envelope shape the routes emit (KS-367). */
interface ErrorEnvelope {
  success?: boolean;
  error?: { code?: string; message?: string };
}

describe('KS-444 POST /api/system-errors/ingest body guard', () => {
  it('400s when metadata is an array instead of a record (the sweep body) — nothing tracked', async () => {
    const res = await post('/ingest', { service: 's', message: 'm', metadata: [null, null] });
    expect(res.status).toBe(400);
    const body = (await res.json()) as ErrorEnvelope;
    expect(body).toMatchObject({ success: false, error: { code: 'BAD_REQUEST' } });
    expect(mockTrackError).not.toHaveBeenCalled();
  });

  it('400s when severity is outside the platform union (warning/error/critical)', async () => {
    const res = await post('/ingest', { service: 's', message: 'm', severity: 'debug' });
    expect(res.status).toBe(400);
    expect(mockTrackError).not.toHaveBeenCalled();
  });

  it('400s when service or message is missing (spec marks both required)', async () => {
    expect((await post('/ingest', { message: 'm' })).status).toBe(400);
    expect((await post('/ingest', { service: 's' })).status).toBe(400);
    expect(mockTrackError).not.toHaveBeenCalled();
  });

  it('201s a spec-shaped body and forwards it to trackError', async () => {
    mockTrackError.mockResolvedValueOnce(undefined);
    const res = await post('/ingest', {
      service: 'auth', message: 'boom', severity: 'critical', metadata: { requestId: 'r1' },
    });
    expect(res.status).toBe(201);
    expect(mockTrackError).toHaveBeenCalledWith(expect.objectContaining({
      service: 'auth', message: 'boom', severity: 'critical', metadata: { requestId: 'r1' },
    }));
  });
});

describe('KS-444 POST /api/system-errors/client-errors body guard', () => {
  it('400s when source is an object instead of a string (the sweep body) — nothing tracked', async () => {
    const res = await post('/client-errors', { error: 'e', source: {} });
    expect(res.status).toBe(400);
    const body = (await res.json()) as ErrorEnvelope;
    expect(body.error?.code).toBe('BAD_REQUEST');
    expect(mockTrackError).not.toHaveBeenCalled();
  });

  it('201s the React ErrorBoundary payload — undeclared extras pass (schema is non-strict)', async () => {
    mockTrackError.mockResolvedValueOnce(undefined);
    // Mirrors frontend/*/src/components/ErrorBoundary.tsx: extra type/message/
    // stack/timestamp fields beyond the published ClientErrorIngestRequest.
    const res = await post('/client-errors', {
      type: 'react_error_boundary', source: 'admin', message: 'render blew up',
      stack: 'Error: x', componentStack: 'at App', url: 'https://a/admin', timestamp: 'now',
    });
    expect(res.status).toBe(201);
    expect(mockTrackError).toHaveBeenCalledWith(expect.objectContaining({ service: 'admin' }));
  });
});

describe('KS-444 POST /api/system-errors/resolve-by-service body guard', () => {
  it('400s when service is an object instead of a string (the sweep body) — nothing resolved', async () => {
    const res = await post('/resolve-by-service', { service: {} });
    expect(res.status).toBe(400);
    const body = (await res.json()) as ErrorEnvelope;
    expect(body.error?.code).toBe('BAD_REQUEST');
    expect(mockResolveErrorsByService).not.toHaveBeenCalled();
  });

  it('200s a spec-shaped body and returns the resolve count', async () => {
    mockResolveErrorsByService.mockResolvedValueOnce(3);
    const res = await post('/resolve-by-service', { service: 'auth' });
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ success: true, resolved: 3 });
    expect(mockResolveErrorsByService).toHaveBeenCalledWith('auth');
  });
});
