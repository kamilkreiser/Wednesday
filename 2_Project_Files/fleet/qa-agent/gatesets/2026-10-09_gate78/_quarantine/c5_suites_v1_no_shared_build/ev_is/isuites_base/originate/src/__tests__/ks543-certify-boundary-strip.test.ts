/**
 * KS-543 (finding #3) — POST /api/certifications/issue must strip known
 * identity keys from the `data` blob BEFORE content-hashing it.
 *
 * The blob is content-hashed into the certification, so PII inside it is
 * STRUCTURALLY UNERASABLE — it can never be encrypted or pseudonymised
 * post-hoc without invalidating the certification's own hash. The route
 * already deletes the reserved `onBehalfOf` key for exactly this reason
 * (KS-480); this extends the same boundary hygiene to the identity keys S
 * used to send (`actorName` — "First Last (email)", dropped S-side in
 * PS-472) so no caller can hash identity into permanence. Strip, not
 * reject: a 400 would widen platform-wide 4xx behaviour (KS-472 rule).
 *
 * Mock surface mirrors ks444-certifications-issue-body-types.test.ts.
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
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    // KS-547: /issue now role-gates; ISSUER_ADMIN keeps these validation tests past the gate.
    req.user = { userId: '11111111-2222-4333-8444-555555555555', email: 'issuer@example.com', role: 'ISSUER_ADMIN' };
    next();
  },
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import crypto from 'crypto';
import express from 'express';
import { certificationsRouter } from '../routes/certifications';

/** The route's own content-hash algorithm (module-local in certifications.ts). */
function routeContentHash(data: Record<string, unknown>): string {
  const sorted = JSON.stringify(data, Object.keys(data).sort());
  return crypto.createHash('sha256').update(sorted).digest('hex');
}

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

function issue(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/certifications/issue`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

describe('KS-543 certify boundary strip — identity keys never reach the content hash', () => {
  it('strips actorName/actorEmail from data before hashing AND before persistence', async () => {
    const res = await issue({
      type: 'certificate',
      data: {
        grade: 'A',
        actorName: 'Subject Person (subject@example.com)',
        actorEmail: 'subject@example.com',
      },
    });
    expect(res.status).toBe(201);

    // The persisted certification's data blob must not carry the identity keys…
    expect(mockSaveCertification).toHaveBeenCalled();
    const saved = mockSaveCertification.mock.calls[0][0] as {
      data: Record<string, unknown>;
      contentHash: string;
    };
    expect(saved.data).not.toHaveProperty('actorName');
    expect(saved.data).not.toHaveProperty('actorEmail');
    expect(saved.data).not.toHaveProperty('onBehalfOf');
    expect(saved.data.grade).toBe('A');

    // …and the content hash must be computed over the STRIPPED blob (the
    // route hashes with its own sha256-of-sorted-JSON; recompute it here),
    // proving the identity keys were removed BEFORE hashing — i.e. they can
    // never be hashed into permanence.
    expect(saved.contentHash).toBe(routeContentHash({ grade: 'A' }));
    expect(saved.contentHash).not.toBe(
      routeContentHash({
        grade: 'A',
        actorName: 'Subject Person (subject@example.com)',
        actorEmail: 'subject@example.com',
      }),
    );
  });

  it('a payload without identity keys hashes exactly as sent (strip is a no-op)', async () => {
    const res = await issue({ type: 'certificate', data: { grade: 'B', reference: 'case-1' } });
    expect(res.status).toBe(201);
    const saved = mockSaveCertification.mock.calls[0][0] as { contentHash: string };
    expect(saved.contentHash).toBe(routeContentHash({ grade: 'B', reference: 'case-1' }));
  });
});

describe('KS-1124 F4: a certification whose anchoring failed is saved with status failed', () => {
  it('RED KS-1124 F4-1: an issue whose anchoring is unreachable saves status failed, not a statusless pending', async () => {
    const res = await issue({ type: 'certificate', data: { grade: 'F4' } });
    const bc = mockSaveCertification.mock.calls[0][0].blockchain;
    expect({ status: res.status, saves: mockSaveCertification.mock.calls.length, saved: bc.status, anchoringStatus: bc.anchoringStatus, anchorId: bc.anchorId }).toEqual({ status: 201, saves: 1, saved: 'failed', anchoringStatus: 'failed', anchorId: null });
  });

  it('RED KS-1124 F4-2: a recertify whose anchoring is unreachable saves status failed, not a statusless pending', async () => {
    jest.requireMock('../repositories/certificationRepo').getCertification.mockResolvedValueOnce({ id: 'cert-ks1124-f4', type: 'certificate', status: 'issued', issuer: { id: 'issuer-1' }, holder: { id: 'holder-1' } });
    const res = await fetch(baseUrl + '/api/certifications/cert-ks1124-f4/recertify', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ note: 'f4' }) });
    const bc = mockSaveCertification.mock.calls[0][0].blockchain;
    expect({ status: res.status, saves: mockSaveCertification.mock.calls.length, saved: bc.status, anchoringStatus: bc.anchoringStatus, anchorId: bc.anchorId }).toEqual({ status: 201, saves: 1, saved: 'failed', anchoringStatus: 'failed', anchorId: null });
  });

  it('control KS-1124 F4-3: an issue whose anchoring is accepted stays statusless pending-onchain with its anchor id', async () => {
    const stub = express().post('/api/anchors', (_req, r) => { r.status(202).json({ data: { id: 'anchor-ks1124-f4' } }); }).listen(0, '127.0.0.1');
    await new Promise((resolve) => stub.once('listening', resolve));
    process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:' + (stub.address() as { port: number }).port;
    try {
      const res = await issue({ type: 'certificate', data: { grade: 'F4' } });
      const bc = mockSaveCertification.mock.calls[0][0].blockchain;
      expect({ status: res.status, hasStatus: 'status' in bc, confidence: bc.confidence, anchoringStatus: bc.anchoringStatus, anchorId: bc.anchorId }).toEqual({ status: 201, hasStatus: false, confidence: 'pending-onchain', anchoringStatus: 'submitted', anchorId: 'anchor-ks1124-f4' });
    } finally {
      process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';
      stub.close();
    }
  });
});
