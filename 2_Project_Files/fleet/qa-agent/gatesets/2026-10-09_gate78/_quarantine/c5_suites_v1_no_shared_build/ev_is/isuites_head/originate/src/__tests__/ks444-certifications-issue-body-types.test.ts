/**
 * KS-444 — POST /api/certifications/issue: enforce the remaining published
 * CertificationIssueRequest field types.
 *
 * The validator chain covered type/data/holderEmail/parentDocumentId but not
 * documentId or metadata — the sweep's negative_data_rejection sent
 * `metadata: [null, null]` (the published contract declares a JSON object)
 * and it was accepted with a 201. The chain now types documentId (optional
 * string) and metadata (optional object). Mock surface mirrors
 * ks445-certifications-issue-unstorable-payload.test.ts.
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

/** Canonical error-envelope shape the routes emit (KS-367). */
interface ErrorEnvelope {
  success?: boolean;
  error?: { code?: string; message?: string };
}

/** Helper: POST /issue with a JSON body and return the response. */
function issue(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/certifications/issue`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

describe('KS-444 POST /api/certifications/issue — body type enforcement', () => {
  it('400s an array metadata (the sweep body) — repo untouched', async () => {
    const res = await issue({
      type: 'educational_degree',
      data: {},
      documentId: '',
      metadata: [null, null],
      parentDocumentId: '',
    });
    expect(res.status).toBe(400);
    const body = (await res.json()) as ErrorEnvelope;
    expect(body.error?.code).toBe('VALIDATION_ERROR');
    expect(mockSaveCertification).not.toHaveBeenCalled();
  });

  it('400s a non-string documentId', async () => {
    const res = await issue({ type: 'educational_degree', data: {}, documentId: { nested: true } });
    expect(res.status).toBe(400);
    expect(mockSaveCertification).not.toHaveBeenCalled();
  });

  it('201s the spec-minimal request (type + data) and reaches the repo', async () => {
    mockSaveCertification.mockResolvedValueOnce(undefined);
    const res = await issue({ type: 'educational_degree', data: {} });
    expect(res.status).toBe(201);
    expect(mockSaveCertification).toHaveBeenCalledTimes(1);
  });

  it('still accepts an object metadata alongside the required fields', async () => {
    mockSaveCertification.mockResolvedValueOnce(undefined);
    const res = await issue({ type: 'certificate', data: { degree: 'BSc' }, metadata: { batch: 7 } });
    expect(res.status).toBe(201);
    expect(mockSaveCertification).toHaveBeenCalledTimes(1);
  });
});
