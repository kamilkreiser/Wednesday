/**
 * =============================================================================
 * KS-423 — contract-drift alignments: route-side negative_data_rejection fixes
 * =============================================================================
 * Two of the six KS-423 coverage-phase findings are route-behaviour fixes in
 * this service; these tests pin them:
 *   - GET /api/system-errors must 400 on an UNKNOWN query param (the strict()
 *     schema) instead of silently stripping it and answering 200.
 *   - GET /api/webhooks/{id}/deliveries must 400 on an id violating the spec's
 *     SAFE_ID_PATTERN instead of the ::uuid cast's .catch masking it as an
 *     empty 200.
 * Both are exercised over HTTP against the mounted routers (mocked DB/tracking
 * layers), mirroring exactly what schemathesis's coverage phase sends.
 * =============================================================================
 */

// NODE_ENV=development keeps the system-errors GET open (no auth middleware),
// matching the dev posture the schemathesis sweep runs against.
process.env.NODE_ENV = 'development';

const mockGetRecentErrors = jest.fn();
const mockQueryRaw = jest.fn();

jest.mock('../services/errorTrackingService', () => ({
  trackError: jest.fn(),
  getRecentErrors: mockGetRecentErrors,
  getErrorStats: jest.fn(),
  resolveError: jest.fn(),
  resolveErrorsByService: jest.fn(),
}));

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw },
}));

jest.mock('../middleware/auth', () => ({
  // Auth is not under test — pass everything through.
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import express from 'express';
import { systemErrorsRouter } from '../routes/systemErrors';
import { webhooksRouter } from '../routes/webhooks';

const app = express();
app.use('/api/system-errors', systemErrorsRouter);
app.use('/api/webhooks', webhooksRouter);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => {
  server?.close();
});

beforeEach(() => {
  jest.clearAllMocks();
  mockGetRecentErrors.mockResolvedValue({ errors: [], total: 0 });
});

describe('GET /api/system-errors — strict query validation (KS-423)', () => {
  it('rejects an unknown query parameter with 400', async () => {
    // The schemathesis negative_data_rejection probe: junk param must 4xx.
    const res = await fetch(`${baseUrl}/api/system-errors?limit=1&x-schemathesis-unknown-property=42`);
    expect(res.status).toBe(400);
    const body = (await res.json()) as { error?: { code?: string } };
    expect(body.error?.code).toBe('BAD_REQUEST');
  });

  it('still accepts the full declared parameter set', async () => {
    const res = await fetch(`${baseUrl}/api/system-errors?service=auth&severity=error&resolved=false&limit=10&offset=0`);
    expect(res.status).toBe(200);
    expect(mockGetRecentErrors).toHaveBeenCalledTimes(1);
  });
});

describe('GET /api/webhooks/{id}/deliveries — declared id pattern enforced (KS-423)', () => {
  it('rejects an id violating SAFE_ID_PATTERN with 400 (was a masked empty 200)', async () => {
    // %C2%84 decodes to a control character — outside the declared charset.
    const res = await fetch(`${baseUrl}/api/webhooks/%C2%84/deliveries`);
    expect(res.status).toBe(400);
    const body = (await res.json()) as { error?: { code?: string } };
    expect(body.error?.code).toBe('BAD_REQUEST');
    // The DB must never see the malformed id.
    expect(mockQueryRaw).not.toHaveBeenCalled();
  });

  it('accepts a pattern-conforming id and returns the delivery envelope', async () => {
    mockQueryRaw.mockReturnValueOnce({ catch: () => [] });
    const res = await fetch(`${baseUrl}/api/webhooks/wh_12345/deliveries`);
    expect(res.status).toBe(200);
    const body = (await res.json()) as { success?: boolean; deliveries?: unknown[] };
    expect(body.success).toBe(true);
  });
});
