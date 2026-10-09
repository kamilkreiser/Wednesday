/**
 * KS-445 — POST /api/certifications/issue: unstorable payloads answer 400, not 500.
 *
 * The spec's free-form `data` object permits values Postgres cannot store —
 * the 2026-07-13 sweep sent garbage-unicode keys whose jsonb write raised
 * SQLSTATE 22P05 (unsupported Unicode escape sequence), which fell past the
 * FK/transient classifiers to the blanket 500. The catch now maps the
 * unstorable-input SQLSTATE family via extractPgCode → 400 BAD_REQUEST.
 *
 * Mock surface mirrors ks445-webhook-patch-body-guard.test.ts (express +
 * fetch harness, auth passed through with a stub user).
 */

// KS-1266: keep this unit file off the network. Left at its default, ANCHORING_SERVICE_URL
// resolves the host `anchoring` by DNS and opens a TCP connection to :4005, so the result
// depends on the host's resolver. Port 2, NOT port 1: port 1 is on the Fetch-spec bad-port
// list and undici refuses it before any socket opens, so it never produces the
// ECONNREFUSED the cell is written for. 127.0.0.1:2 does.
process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';

const mockSaveCertification = jest.fn();

jest.mock('../repositories/certificationRepo', () => ({
  initRepo: jest.fn(async () => undefined),
  getCertification: jest.fn(),
  saveCertification: mockSaveCertification,
  listCertifications: jest.fn(),
  saveShare: jest.fn(),
  getSharesByCertification: jest.fn(),
  getLineageEvents: jest.fn(),
}));

jest.mock('../db', () => ({
  prisma: { $queryRaw: jest.fn(), $executeRaw: jest.fn(), $executeRawUnsafe: jest.fn() },
}));

jest.mock('../services/chargeEvents', () => ({
  createChargeEvent: jest.fn(async () => ({ id: 'charge-1' })),
  getChargeEventsByCertification: jest.fn(),
}));

jest.mock('../utils/notificationClient', () => ({
  notifyDocumentCertified: jest.fn(async () => undefined),
  notifyDocumentRevoked: jest.fn(async () => undefined),
  notifyDocumentShared: jest.fn(async () => undefined),
}));

jest.mock('../events', () => ({
  publishEvent: jest.fn(async () => undefined),
  EventTypes: { CERTIFICATION_ISSUED: 'certification.issued' },
}));

jest.mock('../repositories/documentRepo', () => ({
  saveDocument: jest.fn(async () => undefined),
  assertNoCycle: jest.fn(async () => undefined),
  generateContentHash: jest.fn(() => 'hash'),
}));

jest.mock('../middleware/auth', () => ({
  // Auth is not under test — inject a stub issuer.
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    // KS-547: /issue now role-gates; ISSUER_ADMIN keeps these validation tests past the gate.
    req.user = { userId: '11111111-2222-4333-8444-555555555555', email: 'issuer@example.com', role: 'ISSUER_ADMIN' };
    next();
  },
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import express from 'express';
import { certificationsRouter } from '../routes/certifications';

const app = express();
app.use('/api/certifications', express.json(), certificationsRouter);

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

/** Helper: POST /issue with a JSON body and return the response. */
function issue(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/certifications/issue`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

describe('KS-445 POST /api/certifications/issue — unstorable payload classes', () => {
  it('maps a 22P05 jsonb rejection (NUL escape in `data`) to 400 BAD_REQUEST', async () => {
    // Prisma-wrapped shape: SQLSTATE on meta.code, P-code on code.
    mockSaveCertification.mockRejectedValueOnce(
      Object.assign(new Error('Raw query failed. Code: `22P05`. unsupported Unicode escape sequence'), {
        code: 'P2010',
        meta: { code: '22P05' },
      }),
    );
    const res = await issue({ type: 'certificate', data: { poisoned: 'x' } });
    expect(res.status).toBe(400);
    const body = (await res.json()) as { success: boolean; error: { code: string } };
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('maps a 22021 invalid-byte-sequence rejection the same way', async () => {
    mockSaveCertification.mockRejectedValueOnce(
      Object.assign(new Error('invalid byte sequence for encoding "UTF8": 0x00'), { code: '22021' }),
    );
    expect((await issue({ type: 'certificate', data: { k: 'v' } })).status).toBe(400);
  });

  it('keeps the KS-203 transient mapping: pool timeout still answers 503', async () => {
    mockSaveCertification.mockRejectedValueOnce(Object.assign(new Error('pool timeout'), { code: 'P2024' }));
    expect((await issue({ type: 'certificate', data: { k: 'v' } })).status).toBe(503);
  });

  it('still 500s a genuine unclassified fault', async () => {
    mockSaveCertification.mockRejectedValueOnce(new Error('unexpected null pointer somewhere internal'));
    expect((await issue({ type: 'certificate', data: { k: 'v' } })).status).toBe(500);
  });
});
