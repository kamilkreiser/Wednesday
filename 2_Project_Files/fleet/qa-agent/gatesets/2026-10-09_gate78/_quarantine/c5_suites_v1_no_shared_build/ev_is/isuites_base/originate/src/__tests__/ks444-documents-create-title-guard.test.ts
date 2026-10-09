/**
 * KS-444 — POST /api/documents: title is required and field types are enforced
 * (closes the KS-440 validation hole).
 *
 * The published DocumentCreateRequest declares `title` REQUIRED (plus
 * documentType: string, data: object), but the handler accepted any body that
 * carried a `data` object — the sweep's negative_data_rejection created an
 * untitled document with a 201. The handler now requires a title (top-level
 * per the spec, or `data.title` for the still-supported legacy `{type, data}`
 * shape) and rejects wrong-typed title/documentType/data.
 *
 * SIMULATE_ANCHORING short-circuits the auto-anchor scope so the harness
 * never reaches for the anchoring service.
 */

// routes/documents imports services/provenance -> db -> config, which demands
// DATABASE_URL at module load — same shim the other route suites here use
// (ks480-provenance.test.ts). Without it this suite fails to RUN (0 tests),
// which read as green in the suite count for weeks (BACKLOG 2026-08-06).
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

process.env.SIMULATE_ANCHORING = 'true';

// KS-1266: keep this unit file off the network. Left at its default, ANCHORING_SERVICE_URL
// resolves the host `anchoring` by DNS and opens a TCP connection to :4005, so the result
// depends on the host's resolver. Port 2, NOT port 1: port 1 is on the Fetch-spec bad-port
// list and undici refuses it before any socket opens, so it never produces the
// ECONNREFUSED the cell is written for. 127.0.0.1:2 does.
process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';

// KS-596: saveDocument now returns { dbId, inserted } — the create route
// reads dbId for the response's documentUuid.
const mockSaveDocument = jest.fn(async (..._args: any[]) => ({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true }));

jest.mock('../repositories/documentRepo', () => ({
  getDocument: jest.fn(),
  listDocuments: jest.fn(),
  saveDocument: mockSaveDocument,
  updateDocument: jest.fn(async () => undefined),
  getSigningRequest: jest.fn(),
  saveSigningRequest: jest.fn(),
  deleteSigningRequest: jest.fn(),
  generateContentHash: jest.fn(() => 'a'.repeat(64)),
  seedDemoDocuments: jest.fn(async () => undefined),
  assertNoCycle: jest.fn(async () => undefined),
}));

jest.mock('../repositories/shareRepo', () => ({
  createShare: jest.fn(),
}));

jest.mock('../repositories/lifecycleEventRepo', () => ({
  createLifecycleEvent: jest.fn(),
  setLifecycleEventAnchor: jest.fn(),
  listLifecycleEvents: jest.fn(),
}));

jest.mock('../events', () => ({
  publishEvent: jest.fn(async () => undefined),
  EventTypes: {
    DOCUMENT_CREATED: 'document.created',
    DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred',
    DOCUMENT_VERSIONED: 'document.versioned',
  },
}));

jest.mock('../services/threadTokenClient', () => ({
  mintAndRegisterThreadToken: jest.fn(async () => ({})),
}));

// The fire-and-forget cross-tenant registry call requires routes/verification
// at request time — stub it so the harness never loads the real module.
jest.mock('../routes/verification', () => ({
  registerInPlatformRegistry: jest.fn(async () => undefined),
}));

jest.mock('../middleware/auth', () => ({
  // Auth is not under test — inject a stub issuer-admin caller.
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: '11111111-2222-4333-8444-555555555555', role: 'ISSUER_ADMIN' };
    next();
  },
}));

jest.mock('../middleware/rbac', () => ({
  // RBAC is not under test — allow document writes.
  isAllowedByRoleOrScope: () => true,
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import express from 'express';
import { documentsRouter } from '../routes/documents';

const app = express();
app.use('/api/documents', express.json(), documentsRouter);

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

/** Helper: POST a document body and return the response. */
function createDocument(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/documents`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

describe('KS-444 POST /api/documents — title required (KS-440 hole)', () => {
  it('400s a body with a data object but no title anywhere (the sweep body) — repo untouched', async () => {
    const res = await createDocument({
      documentType: 'PROPERTY_DEED',
      data: { propertyAddress: '42 Plinth Lane, London EC1A 1BB, UK', titleNumber: 'TGL123456' },
    });
    expect(res.status).toBe(400);
    const body = (await res.json()) as ErrorEnvelope;
    expect(body.error?.code).toBe('BAD_REQUEST');
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  it('400s an empty body', async () => {
    const res = await createDocument({});
    expect(res.status).toBe(400);
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  it('201s the spec-minimal request (title only) and stores the document', async () => {
    mockSaveDocument.mockResolvedValueOnce({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true });
    const res = await createDocument({ title: 'Property Deed — 42 Plinth Lane' });
    expect(res.status).toBe(201);
    expect(mockSaveDocument).toHaveBeenCalledTimes(1);
  });

  it('still accepts the legacy {type, data} shape when data carries the title (back-compat pin)', async () => {
    mockSaveDocument.mockResolvedValueOnce({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true });
    const res = await createDocument({ type: 'DOCUMENT', data: { title: 'Legacy-shaped doc' } });
    expect(res.status).toBe(201);
    expect(mockSaveDocument).toHaveBeenCalledTimes(1);
  });
});

describe('KS-444 POST /api/documents — published field types enforced', () => {
  it('400s a non-string title', async () => {
    const res = await createDocument({ title: { nested: true } });
    expect(res.status).toBe(400);
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  it('400s a non-string documentType', async () => {
    const res = await createDocument({ title: 'Deed', documentType: 42 });
    expect(res.status).toBe(400);
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  it('400s an array data blob — the published contract declares an object', async () => {
    const res = await createDocument({ title: 'Deed', data: [1, 2, 3] });
    expect(res.status).toBe(400);
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });
});
