/**
 * KS-444 — PATCH /api/gdpr/dsr/:dsrId + POST /api/gdpr/consent/withdraw
 * body guards.
 *
 * Both handlers only truthy-checked their bodies, so a spec-violating value
 * passed straight through to the service layer — the sweep's
 * negative_data_rejection sent `processedBy: {}` (PATCH) and `userId: {}`
 * (withdraw) and both were accepted with a 200. The routes now enforce the
 * published request contracts (DSRUpdateRequest / ConsentWithdrawRequest in
 * originate.openapi.ts) via the same Zod-mirror pattern as the KS-445 consent
 * and dsr create guards. Harness mirrors ks445-gdpr-write-guards.test.ts.
 */

const mockUpdateDSRStatus = jest.fn();
const mockWithdrawConsent = jest.fn();

jest.mock('../services/gdprService', () => ({
  updateDSRStatus: mockUpdateDSRStatus,
  withdrawConsent: mockWithdrawConsent,
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

/** A well-formed DSR id for the PATCH path param. */
const DSR_ID = 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee';

/** A well-formed subject UUID for withdraw bodies. */
const USER_ID = '11111111-2222-4333-8444-555555555555';

/** Canonical error-envelope shape the routes emit (KS-367). */
interface ErrorEnvelope {
  success?: boolean;
  error?: { code?: string; message?: string };
}

/** Helper: send a JSON request to a gdpr route and return the response. */
function send(method: string, path: string, body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/gdpr/${path}`, {
    method,
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

/** Helper: parse the response body as the canonical error envelope. */
async function jsonOf(res: Response): Promise<ErrorEnvelope> {
  return (await res.json()) as ErrorEnvelope;
}

describe('KS-444 PATCH /api/gdpr/dsr/:dsrId body guard', () => {
  it('keeps the friendly 400 when status/processedBy are missing (pre-existing behaviour)', async () => {
    const res = await send('PATCH', `dsr/${DSR_ID}`, { notes: 'no status here' });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('BAD_REQUEST');
    expect(mockUpdateDSRStatus).not.toHaveBeenCalled();
  });

  it('400s a wrong-typed processedBy (the sweep sent `{}`) — service untouched', async () => {
    const res = await send('PATCH', `dsr/${DSR_ID}`, { status: 'pending', processedBy: {}, notes: '' });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('VALIDATION_ERROR');
    expect(mockUpdateDSRStatus).not.toHaveBeenCalled();
  });

  it('400s a status outside the published vocabulary', async () => {
    const res = await send('PATCH', `dsr/${DSR_ID}`, { status: 'demolished', processedBy: USER_ID });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('VALIDATION_ERROR');
    expect(mockUpdateDSRStatus).not.toHaveBeenCalled();
  });

  it("accepts the runtime vocabulary the spec now publishes ('processing')", async () => {
    // KS-444 also corrected the published enum: the platform stores
    // 'processing'/'denied'/'extended' (data_subject_requests CHECK), not the
    // drifted 'in_progress'/'rejected'.
    mockUpdateDSRStatus.mockResolvedValueOnce(true);
    const res = await send('PATCH', `dsr/${DSR_ID}`, { status: 'processing', processedBy: USER_ID });
    expect(res.status).toBe(200);
    expect(mockUpdateDSRStatus).toHaveBeenCalledWith(DSR_ID, 'processing', USER_ID, undefined);
  });

  it('200s a spec-shaped update and forwards notes to the service', async () => {
    mockUpdateDSRStatus.mockResolvedValueOnce(true);
    const res = await send('PATCH', `dsr/${DSR_ID}`, { status: 'completed', processedBy: USER_ID, notes: 'done' });
    expect(res.status).toBe(200);
    expect(mockUpdateDSRStatus).toHaveBeenCalledWith(DSR_ID, 'completed', USER_ID, 'done');
  });
});

describe('KS-444 POST /api/gdpr/consent/withdraw body guard', () => {
  it('keeps the friendly 400 when userId/purpose are missing (pre-existing behaviour)', async () => {
    const res = await send('POST', 'consent/withdraw', { purpose: 'marketing' });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('BAD_REQUEST');
    expect(mockWithdrawConsent).not.toHaveBeenCalled();
  });

  it('400s a wrong-typed userId (the sweep sent `{}`) — service untouched', async () => {
    const res = await send('POST', 'consent/withdraw', { userId: {}, purpose: 'marketing' });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('VALIDATION_ERROR');
    expect(mockWithdrawConsent).not.toHaveBeenCalled();
  });

  it('400s a purpose outside the published ConsentPurpose enum', async () => {
    const res = await send('POST', 'consent/withdraw', { userId: USER_ID, purpose: 'totally-made-up' });
    expect(res.status).toBe(400);
    expect((await jsonOf(res)).error?.code).toBe('VALIDATION_ERROR');
    expect(mockWithdrawConsent).not.toHaveBeenCalled();
  });

  it('200s a spec-shaped withdraw and reaches the service', async () => {
    mockWithdrawConsent.mockResolvedValueOnce(true);
    const res = await send('POST', 'consent/withdraw', { userId: USER_ID, purpose: 'marketing' });
    expect(res.status).toBe(200);
    expect(mockWithdrawConsent).toHaveBeenCalledWith(USER_ID, 'marketing');
  });
});
