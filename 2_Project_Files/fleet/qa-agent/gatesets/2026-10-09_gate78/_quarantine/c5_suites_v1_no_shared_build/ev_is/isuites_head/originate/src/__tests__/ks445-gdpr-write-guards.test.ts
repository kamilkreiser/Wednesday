/**
 * KS-445 — POST /api/gdpr/consent + POST /api/gdpr/dsr write-path guards.
 *
 * Both handlers only truthy-checked their bodies, then bound the values into
 * raw SQL (`${userId}::uuid` casts, VARCHAR / CHECK / FK constraints in
 * consent_records / data_subject_requests). Fuzzer-shaped bodies surfaced as
 * raw Postgres failures re-thrown generically → 500 INTERNAL_ERROR. The routes
 * now (1) validate the body against the published request schema → 400,
 * (2) 404 a non-UUID userId up front (uuid FK column — cannot reference a real
 * user), and (3) map SQLSTATE-tagged service errors (FK 23503 → 404,
 * 22001/23514 → 400). Same harness pattern as ks431-gdpr-export-id-guard.
 */

const mockRecordConsent = jest.fn();
const mockCreateDSR = jest.fn();

jest.mock('../services/gdprService', () => ({
  recordConsent: mockRecordConsent,
  createDSR: mockCreateDSR,
}));

jest.mock('../middleware/auth', () => ({
  // Auth/authz are not under test — pass everything through.
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireSelfOrRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  hasAnyRole: () => true,
}));

import express from 'express';
import { gdprRouter } from '../routes/gdpr';

const app = express();
app.use('/api/gdpr', express.json(), gdprRouter);

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

/** A well-formed subject UUID accepted by the route-level UUID pre-check. */
const USER_ID = '11111111-2222-4333-8444-555555555555';

/** Helper: POST a JSON body to a gdpr route and return the response. */
function post(path: string, body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/gdpr/${path}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

/** Build an Error tagged the way gdprService.wrapDbError tags re-thrown DB failures. */
function taggedDbError(message: string, pgCode: string): Error {
  return Object.assign(new Error(message), { pgCode });
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

describe('KS-445 POST /api/gdpr/consent', () => {
  it('404s a non-UUID userId without touching the service (the 22P02 → 500 class)', async () => {
    const res = await post('consent', { userId: '0', purpose: 'marketing' });
    expect(res.status).toBe(404);
    expect((await jsonOf(res)).error?.code).toBe('NOT_FOUND');
    expect(mockRecordConsent).not.toHaveBeenCalled();
  });

  it('400s a purpose outside the published ConsentPurpose enum', async () => {
    // The spec constrains purpose to the 8-value enum; junk purpose is spec-invalid.
    const res = await post('consent', { userId: USER_ID, purpose: 'totally-made-up' });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('VALIDATION_ERROR');
    expect(mockRecordConsent).not.toHaveBeenCalled();
  });

  it('400s a wrong-typed expiresInDays (string) — spec declares integer', async () => {
    const res = await post('consent', { userId: USER_ID, purpose: 'marketing', expiresInDays: '30' });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('VALIDATION_ERROR');
  });

  it('400s a spec-legal but unrepresentable expiresInDays (JS Date overflow → serialisation throw)', async () => {
    // 1e15 days is a positive integer (spec-legal) but exceeds the max JS Date of 8.64e15 ms.
    const res = await post('consent', { userId: USER_ID, purpose: 'marketing', expiresInDays: 1e15 });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('VALIDATION_ERROR');
    expect(mockRecordConsent).not.toHaveBeenCalled();
  });

  it('201s a spec-shaped request and reaches the service', async () => {
    mockRecordConsent.mockResolvedValueOnce({ id: 'c-1', userId: USER_ID, purpose: 'marketing' });
    const res = await post('consent', { userId: USER_ID, purpose: 'marketing', expiresInDays: 30 });
    expect(res.status).toBe(201);
    expect(mockRecordConsent).toHaveBeenCalledWith(USER_ID, 'marketing', expect.any(Object));
  });

  it('404s when the service reports FK 23503 (valid UUID, nonexistent user)', async () => {
    mockRecordConsent.mockRejectedValueOnce(taggedDbError('Failed to record consent', '23503'));
    const res = await post('consent', { userId: USER_ID, purpose: 'marketing' });
    expect(res.status).toBe(404);
    expect((await jsonOf(res)).error?.code).toBe('NOT_FOUND');
  });

  it('400s when the service reports 22001 (spec-legal value too long for its column, e.g. version)', async () => {
    // The spec leaves `version` an unbounded string; consent_records.version is VARCHAR(20).
    mockRecordConsent.mockRejectedValueOnce(taggedDbError('Failed to record consent', '22001'));
    const res = await post('consent', { userId: USER_ID, purpose: 'marketing', version: 'x'.repeat(30) });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('VALIDATION_ERROR');
  });

  it('400s when the service reports CHECK 23514 (spec-legal source outside explicit/implicit)', async () => {
    mockRecordConsent.mockRejectedValueOnce(taggedDbError('Failed to record consent', '23514'));
    const res = await post('consent', { userId: USER_ID, purpose: 'marketing', source: 'carrier-pigeon' });
    expect(res.status).toBe(400);
  });

  it('keeps 500 for genuinely unclassified service failures', async () => {
    mockRecordConsent.mockRejectedValueOnce(new Error('Failed to record consent'));
    const res = await post('consent', { userId: USER_ID, purpose: 'marketing' });
    expect(res.status).toBe(500);
  });
});

describe('KS-445 POST /api/gdpr/dsr', () => {
  it('404s a non-UUID userId without touching the service (the 22P02 → 500 class)', async () => {
    const res = await post('dsr', { type: 'access', userId: 'not-a-uuid', email: 'a@b.co' });
    expect(res.status).toBe(404);
    expect((await jsonOf(res)).error?.code).toBe('NOT_FOUND');
    expect(mockCreateDSR).not.toHaveBeenCalled();
  });

  it('400s a malformed email — the spec declares format: email', async () => {
    const res = await post('dsr', { type: 'access', userId: USER_ID, email: 'not-an-email' });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('VALIDATION_ERROR');
    expect(mockCreateDSR).not.toHaveBeenCalled();
  });

  it('keeps the friendly 400 for an unknown DSR type (pre-existing behaviour)', async () => {
    const res = await post('dsr', { type: 'demolition', userId: USER_ID, email: 'a@b.co' });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('BAD_REQUEST');
  });

  it('201s a spec-shaped request and reaches the service', async () => {
    mockCreateDSR.mockResolvedValueOnce({ id: 'dsr-1', type: 'access', userId: USER_ID });
    const res = await post('dsr', { type: 'access', userId: USER_ID, email: 'subject@example.com', notes: 'please' });
    expect(res.status).toBe(201);
    expect(mockCreateDSR).toHaveBeenCalledWith('access', USER_ID, 'subject@example.com', 'please');
  });

  it('404s when the service reports FK 23503 (valid UUID, nonexistent user)', async () => {
    mockCreateDSR.mockRejectedValueOnce(taggedDbError('Failed to create data subject request', '23503'));
    const res = await post('dsr', { type: 'access', userId: USER_ID, email: 'subject@example.com' });
    expect(res.status).toBe(404);
  });

  it('400s when the service reports 22001 (stored ciphertext exceeds the email VARCHAR(255))', async () => {
    mockCreateDSR.mockRejectedValueOnce(taggedDbError('Failed to create data subject request', '22001'));
    const res = await post('dsr', { type: 'access', userId: USER_ID, email: 'subject@example.com' });
    expect(res.status).toBe(400);
  });
});
