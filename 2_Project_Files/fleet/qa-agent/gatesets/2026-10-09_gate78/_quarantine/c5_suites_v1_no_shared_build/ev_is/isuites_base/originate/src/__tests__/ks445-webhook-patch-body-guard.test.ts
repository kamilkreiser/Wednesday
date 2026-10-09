/**
 * KS-445 — PATCH /api/webhooks/:id body guard.
 *
 * The update handler bound body fields straight into the raw UPDATE via
 * $executeRawUnsafe. A fuzzer body of the wrong type — `events` as a string
 * (svc_webhooks.events is text[]) or `isActive` as a string (boolean column) —
 * made Postgres throw `42804 datatype mismatch`, which fell through to a raw
 * 500 (KS-440 sweep evidence). The published WebhookUpdateRequest contract
 * declares those field types, so the handler now enforces them at the boundary
 * (400 VALIDATION_ERROR) and maps any residual cast failure via extractPgCode.
 */

const mockExecuteRawUnsafe = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: jest.fn(),
    $executeRaw: jest.fn(),
    $executeRawUnsafe: mockExecuteRawUnsafe,
  },
}));

jest.mock('../middleware/auth', () => ({
  // Auth is not under test — pass everything through.
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import express from 'express';
import { webhooksRouter } from '../routes/webhooks';

const app = express();
app.use('/api/webhooks', express.json(), webhooksRouter);

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

/** A usable webhook id — the KS-431 :id guard requires a canonical UUID. */
const WEBHOOK_ID = 'a1b2c3d4-5678-4abc-9def-0123456789ab';

/** Helper: PATCH the webhook with a JSON body and return the response. */
function patchWebhook(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/webhooks/${WEBHOOK_ID}`, {
    method: 'PATCH',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

/** Canonical error-envelope shape the routes emit (KS-367). */
interface ErrorEnvelope {
  success?: boolean;
  error?: { code?: string; message?: string };
}

/** Helper: parse the response body as the canonical error envelope. */
async function jsonOf(res: Response): Promise<ErrorEnvelope> {
  return (await res.json()) as ErrorEnvelope;
}

describe('KS-445 PATCH /api/webhooks/:id body guard', () => {
  it('400s when events is a string instead of an array (the 42804 class) — DB untouched', async () => {
    // A single event as a bare string binds text against the text[] column → 42804 pre-fix.
    const res = await patchWebhook({ events: 'certification.issued' });
    expect(res.status).toBe(400);
    const body = await jsonOf(res);
    expect(body).toMatchObject({ success: false, error: { code: 'VALIDATION_ERROR' } });
    expect(mockExecuteRawUnsafe).not.toHaveBeenCalled();
  });

  it('400s when isActive is a string instead of a boolean — DB untouched', async () => {
    // "true" (string) bound against the boolean is_active column → 42804 pre-fix.
    const res = await patchWebhook({ isActive: 'true' });
    expect(res.status).toBe(400);
    const body = await jsonOf(res);
    expect(body.error?.code).toBe('VALIDATION_ERROR');
    expect(mockExecuteRawUnsafe).not.toHaveBeenCalled();
  });

  it('400s when events contains a value outside the published event enum', async () => {
    // The spec's WebhookUpdateRequest declares events as WebhookEvent[] — junk members are spec-invalid.
    const res = await patchWebhook({ events: ['certification.issued', 'not.a.real.event'] });
    expect(res.status).toBe(400);
    const body = await jsonOf(res);
    expect(body.error?.code).toBe('VALIDATION_ERROR');
    expect(mockExecuteRawUnsafe).not.toHaveBeenCalled();
  });

  it('200s a spec-shaped update (events array + boolean isActive + string description)', async () => {
    mockExecuteRawUnsafe.mockResolvedValueOnce(1);
    const res = await patchWebhook({
      events: ['document.created', 'document.anchored'],
      isActive: false,
      description: 'updated by test',
    });
    expect(res.status).toBe(200);
    expect(await res.json()).toMatchObject({ success: true });
    expect(mockExecuteRawUnsafe).toHaveBeenCalledTimes(1);
  });

  it('ignores unknown extra keys (spec is passthrough) rather than rejecting them', async () => {
    mockExecuteRawUnsafe.mockResolvedValueOnce(1);
    // Extra keys are permitted by the published schema (.passthrough()) and ignored by the handler.
    const res = await patchWebhook({ isActive: true, somethingExtra: 'ignored' });
    expect(res.status).toBe(200);
  });

  it('maps a residual Postgres 42804 (Prisma-wrapped) to 400, never a raw 500', async () => {
    // Prisma wraps pg errors: its own code is P2010, the SQLSTATE lives in meta.code.
    mockExecuteRawUnsafe.mockRejectedValueOnce(
      Object.assign(new Error('Raw query failed. Code: `42804`. Message: `datatype mismatch`'), {
        code: 'P2010',
        meta: { code: '42804' },
      }),
    );
    const res = await patchWebhook({ isActive: true });
    expect(res.status).toBe(400);
    const body = await jsonOf(res);
    expect(body).toMatchObject({ success: false, error: { code: 'VALIDATION_ERROR' } });
  });

  it('keeps 500 for genuinely unclassified failures', async () => {
    // A non-Postgres failure (e.g. connection drop) is still an honest 500.
    mockExecuteRawUnsafe.mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
    const res = await patchWebhook({ isActive: true });
    expect(res.status).toBe(500);
  });
});
