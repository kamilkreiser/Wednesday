/**
 * KS-451 — POST /api/documents rejects a NUL byte (U+0000) in free-text fields.
 *
 * A NUL inside `title` (or `description`, or the legacy `data.{title,description}`)
 * passed the KS-444 `typeof === 'string'` type guard (a NUL is a valid JS
 * string) and reached Postgres unfiltered — `sanitizeString` only HTML-escapes,
 * it does not strip NUL — so the driver threw
 * `invalid byte sequence for encoding "UTF8": 0x00` → a raw 500. The handler
 * now rejects a NUL in any persisted free-text field → 400, before the DB call.
 *
 * SIMULATE_ANCHORING short-circuits the auto-anchor scope so the harness never
 * reaches for the anchoring service.
 */

// routes/documents imports services/provenance -> db -> config, which demands
// DATABASE_URL at module load — same shim the other route suites here use
// (ks480-provenance.test.ts). Without it this suite fails to RUN (0 tests),
// which read as green in the suite count for weeks (BACKLOG 2026-08-06).
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

process.env.SIMULATE_ANCHORING = 'true';

const NUL = '\u0000';

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

jest.mock('../repositories/shareRepo', () => ({ createShare: jest.fn() }));

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

interface ErrorEnvelope {
  success?: boolean;
  error?: { code?: string; message?: string };
}

function createDocument(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/documents`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

describe('KS-451 POST /api/documents — NUL byte rejection', () => {
  it('400s a NUL byte in the top-level title — repo untouched (was raw 500)', async () => {
    const res = await createDocument({ title: `x${NUL}y`, documentType: 'DOCUMENT', data: {} });
    expect(res.status).toBe(400);
    const body = (await res.json()) as ErrorEnvelope;
    expect(body.error?.code).toBe('BAD_REQUEST');
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  it('400s a NUL byte in description', async () => {
    const res = await createDocument({ title: 'Clean', description: `bad${NUL}desc` });
    expect(res.status).toBe(400);
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  it('400s a NUL byte in the legacy data.title shape', async () => {
    const res = await createDocument({ type: 'DOCUMENT', data: { title: `legacy${NUL}` } });
    expect(res.status).toBe(400);
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  it('still 201s a clean title (no false positives)', async () => {
    mockSaveDocument.mockResolvedValueOnce({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true });
    const res = await createDocument({ title: 'A perfectly clean title' });
    expect(res.status).toBe(201);
    expect(mockSaveDocument).toHaveBeenCalledTimes(1);
  });
});
