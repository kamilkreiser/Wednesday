/**
 * =============================================================================
 * KS-596 (architecture P1) — optional S-supplied identifiers on registration
 * =============================================================================
 * POST /api/documents accepts three OPTIONAL fields: documentUuid (v4),
 * userUuid, organizationUuid. documentUuid becomes the registration's
 * external_id; when absent K mints its legacy id exactly as before.
 *
 * Ruled idempotency (Kam 2026-08-10 via v1.3, ruling b — duplicate bytes are
 * TWO registrations distinguished by UUID):
 *   - re-POST of a seen documentUuid + SAME contentHash → 200 with the
 *     existing registration (idempotent; a retry can never mint a phantom);
 *   - same documentUuid + DIFFERENT bytes → 409 (surfaces an S-side
 *     duplicate-UUID bug rather than masking it — S-pack §3.2/§5.1).
 *
 * Phase B: every registration response returns BOTH the legacy id and
 * documentUuid, so S can migrate reads independently of writes.
 * =============================================================================
 */

process.env.SIMULATE_ANCHORING = 'true';
// routes/documents imports services/provenance -> db -> config, which demands
// DATABASE_URL at module load — same shim as the sibling suites.
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const DB_ID = '99999999-9999-4999-8999-999999999999';
const mockSaveDocument = jest.fn(async (..._args: any[]) => ({ dbId: DB_ID, inserted: true }));
const mockGetDocument = jest.fn(async (..._args: any[]) => null as any);

jest.mock('../repositories/documentRepo', () => ({
  getDocument: mockGetDocument,
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
beforeEach(() => {
  jest.clearAllMocks();
  mockSaveDocument.mockImplementation(async (..._args: any[]) => ({ dbId: DB_ID, inserted: true }));
  mockGetDocument.mockResolvedValue(null);
});

const V4 = '2f5b1a3c-9d4e-4f6a-8b7c-1d2e3f4a5b6c';
const HASH = 'b'.repeat(64);

function createDocument(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/documents`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

describe('KS-596 — field validation', () => {
  it('400s a non-v4 documentUuid', async () => {
    const res = await createDocument({ title: 'Doc', documentUuid: '2f5b1a3c-9d4e-1f6a-8b7c-1d2e3f4a5b6c' }); // v1 nibble
    expect(res.status).toBe(400);
    const body: any = await res.json();
    expect(body.error.message).toMatch(/documentUuid/);
  });

  it('400s a malformed userUuid / organizationUuid', async () => {
    const r1 = await createDocument({ title: 'Doc', userUuid: 'not-a-uuid' });
    expect(r1.status).toBe(400);
    const r2 = await createDocument({ title: 'Doc', organizationUuid: 42 });
    expect(r2.status).toBe(400);
  });
});

describe('KS-596 — minting unchanged when documentUuid absent', () => {
  it('mints the legacy doc-<ts>-<rand> id and returns the DB uuid as documentUuid', async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH });
    expect(res.status).toBe(201);
    const body: any = await res.json();
    expect(body.id).toMatch(/^doc-\d+-[0-9a-f]{8}$/);
    expect(body.documentUuid).toBe(DB_ID);
  });
});

describe('KS-596 — S-supplied documentUuid', () => {
  it('becomes the registration id; response carries both identifiers; insert skips the upsert', async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH, documentUuid: V4.toUpperCase(), userUuid: V4, organizationUuid: V4 });
    expect(res.status).toBe(201);
    const body: any = await res.json();
    expect(body.id).toBe(V4); // lowercased
    expect(body.documentUuid).toBe(V4);
    const [doc, , , opts] = mockSaveDocument.mock.calls[0] as any[];
    expect(doc.id).toBe(V4);
    // The legacy ON CONFLICT DO UPDATE would silently MERGE a duplicate
    // documentUuid — the S-supplied path must skip it.
    expect(opts.conflictMode).toBe('skip');
    expect(opts.sIdentity).toEqual({ userUuid: V4, organizationUuid: V4 });
  });

  it('re-POST with the SAME contentHash returns 200 with the existing registration and writes nothing', async () => {
    mockGetDocument.mockResolvedValue({
      id: V4, documentUuid: V4, type: 'DOCUMENT', status: 'anchored',
      contentHash: `sha256:${HASH.toUpperCase()}`, // P5 hygiene gap: prefix + case must not defeat equality
      blockchain: { txHash: 'c'.repeat(64), blockHeight: 1 },
      createdAt: '2026-08-01T00:00:00.000Z', data: {}, signatures: [], owner: { id: 'x' },
    });
    const res = await createDocument({ title: 'Doc', contentHash: HASH, documentUuid: V4 });
    expect(res.status).toBe(200);
    const body: any = await res.json();
    expect(body.id).toBe(V4);
    expect(body.documentUuid).toBe(V4);
    expect(body.txHash).toBe('c'.repeat(64));
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  it('re-POST with DIFFERENT bytes is 409', async () => {
    mockGetDocument.mockResolvedValue({
      id: V4, documentUuid: V4, type: 'DOCUMENT', status: 'anchored',
      contentHash: 'd'.repeat(64),
      createdAt: '2026-08-01T00:00:00.000Z', data: {}, signatures: [], owner: { id: 'x' },
    });
    const res = await createDocument({ title: 'Doc', contentHash: HASH, documentUuid: V4 });
    expect(res.status).toBe(409);
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  it('a documentUuid shadowing ANOTHER document\'s internal uuid is refused even on a hash match', async () => {
    // getDocument also resolves by pkey uuid; if the match is not on
    // external_id, registering would shadow that document's uuid lookups.
    mockGetDocument.mockResolvedValue({
      id: 'doc-1754000000000-abcdef12', documentUuid: V4, type: 'DOCUMENT', status: 'anchored',
      contentHash: HASH,
      createdAt: '2026-08-01T00:00:00.000Z', data: {}, signatures: [], owner: { id: 'x' },
    });
    const res = await createDocument({ title: 'Doc', contentHash: HASH, documentUuid: V4 });
    expect(res.status).toBe(409);
  });

  it('a lost insert race re-checks and answers 200 for same bytes', async () => {
    mockGetDocument
      .mockResolvedValueOnce(null) // pre-check: not there yet
      .mockResolvedValueOnce({     // post-race re-check: the winner's row
        id: V4, documentUuid: V4, type: 'DOCUMENT', status: 'draft',
        contentHash: HASH,
        createdAt: '2026-08-01T00:00:00.000Z', data: {}, signatures: [], owner: { id: 'x' },
      });
    mockSaveDocument.mockResolvedValueOnce({ dbId: DB_ID, inserted: false });
    const res = await createDocument({ title: 'Doc', contentHash: HASH, documentUuid: V4 });
    expect(res.status).toBe(200);
    const body: any = await res.json();
    expect(body.id).toBe(V4);
  });
});
