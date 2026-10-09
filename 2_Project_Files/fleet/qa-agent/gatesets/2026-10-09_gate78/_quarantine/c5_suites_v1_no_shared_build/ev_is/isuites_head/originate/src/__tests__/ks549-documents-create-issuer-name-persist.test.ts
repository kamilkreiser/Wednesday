/**
 * KS-549 — POST /api/documents: a top-level `issuerName` is persisted into
 * the document's data blob.
 *
 * It was previously only forwarded to the anchoring request body, so
 * connector-originated documents (S sends issuerName top-level per PS-496)
 * resolved `issuer: null` on every verify — all fallback sources
 * (certMeta/meta/organisation join) were empty. The route now persists it
 * (same top-level-field pattern as recipientEmail / H22), which the verify
 * chains' `meta.issuerName` fallback resolves.
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

jest.mock('../routes/verification', () => ({
  registerInPlatformRegistry: jest.fn(async () => undefined),
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: '11111111-2222-4333-8444-555555555555', role: 'ISSUER_ADMIN' };
    next();
  },
}));

jest.mock('../middleware/rbac', () => ({
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

function createDocument(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/documents`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

describe('KS-549 POST /api/documents — top-level issuerName persists into data', () => {
  it('stores a top-level issuerName in the saved document data blob', async () => {
    const res = await createDocument({
      title: 'Grad Cert in Systems Engineering',
      documentType: 'CERTIFICATE',
      issuerName: 'Flinders University',
      data: { title: 'Grad Cert in Systems Engineering' },
    });
    expect(res.status).toBe(201);
    expect(mockSaveDocument).toHaveBeenCalledTimes(1);
    const saved = mockSaveDocument.mock.calls[0][0];
    expect(saved.data.issuerName).toBe('Flinders University');
  });

  it('does not overwrite an issuerName already present inside data', async () => {
    const res = await createDocument({
      title: 'Doc',
      documentType: 'CERTIFICATE',
      issuerName: 'Top Level Org',
      data: { title: 'Doc', issuerName: 'Nested Org' },
    });
    expect(res.status).toBe(201);
    const saved = mockSaveDocument.mock.calls[0][0];
    expect(saved.data.issuerName).toBe('Nested Org');
  });

  it('never persists an email-shaped issuerName (E-01 guard parity)', async () => {
    const res = await createDocument({
      title: 'Doc',
      documentType: 'CERTIFICATE',
      issuerName: 'someone@example.com',
      data: { title: 'Doc' },
    });
    // KS-1265: the E-01 guard now refuses BEFORE the save. A refused create writes nothing:
    // 400, and saveDocument is never called (at the old tip it was called once, then 400).
    expect(res.status).toBe(400);
    expect(mockSaveDocument).toHaveBeenCalledTimes(0);
  });

  it('omits issuerName entirely when the caller does not send one', async () => {
    const res = await createDocument({
      title: 'Doc',
      documentType: 'CERTIFICATE',
      data: { title: 'Doc' },
    });
    expect(res.status).toBe(201);
    const saved = mockSaveDocument.mock.calls[0][0];
    expect(saved.data.issuerName).toBeUndefined();
  });
});
