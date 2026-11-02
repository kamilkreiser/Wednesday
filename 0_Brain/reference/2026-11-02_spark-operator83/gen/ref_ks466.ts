/**
 * KS-466 §8 — malformed `{id}` path params on the document routes must be
 * rejected BEFORE any repository/DB work (reject-before-cast, the KS-451/
 * KS-367 pattern), answering 400 VALIDATION_ERROR instead of a raw 500.
 *
 * The published spec already constrains every `{id}` to SAFE_ID_PATTERN
 * (originate.openapi.ts idPathParams); the runtime guard is a router.param
 * hook on documentsRouter + publicDocumentsRouter, so every current and
 * future `:id` route is covered.
 *
 * Also pins the ticket's charset-LEGAL repro: an id that matches the pattern
 * but names no document (id `0`) stays a 404, never a 500.
 */

// routes/documents imports services/provenance -> db -> config, which demands
// DATABASE_URL at module load — same shim the other route suites here use
// (ks480-provenance.test.ts). Without it this suite fails to RUN (0 tests),
// which read as green in the suite count for weeks (BACKLOG 2026-08-06).
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

process.env.SIMULATE_ANCHORING = 'true';

const mockGetDocument = jest.fn();

jest.mock('../repositories/documentRepo', () => ({
  getDocument: mockGetDocument,
  listDocuments: jest.fn(),
  saveDocument: jest.fn(async (..._args: any[]) => ({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true })),
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
import { documentsRouter, publicDocumentsRouter } from '../routes/documents';

const app = express();
// Same mount order as index.ts: public router first, then the auth-gated one.
app.use('/api/documents', express.json(), publicDocumentsRouter);
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

/** The sweep's malformed id — the C1 control U+0084, percent-encoded. */
const BAD_ID = '%C2%84';

async function expect400NoRepoTouch(method: string, path: string, body?: unknown) {
  const res = await fetch(`${baseUrl}${path}`, {
    method,
    headers: { 'content-type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  expect(res.status).toBe(400);
  const payload = (await res.json()) as ErrorEnvelope;
  expect(payload.success).toBe(false);
  expect(payload.error?.code).toBe('VALIDATION_ERROR');
  expect(payload.error?.message).toContain('Invalid document id');
  expect(mockGetDocument).not.toHaveBeenCalled();
}

describe('KS-466 §8 — malformed {id} rejected before the repository', () => {
  it('GET /api/documents/{bad}', async () => {
    await expect400NoRepoTouch('GET', `/api/documents/${BAD_ID}`);
  });

  it('GET /api/documents/{bad}/lifecycle-events', async () => {
    await expect400NoRepoTouch('GET', `/api/documents/${BAD_ID}/lifecycle-events`);
  });

  it('POST /api/documents/{bad}/anchor', async () => {
    await expect400NoRepoTouch('POST', `/api/documents/${BAD_ID}/anchor`, {});
  });

  it('POST /api/documents/{bad}/revoke', async () => {
    await expect400NoRepoTouch('POST', `/api/documents/${BAD_ID}/revoke`, {});
  });

  it('POST /api/documents/{bad}/sign-cert', async () => {
    await expect400NoRepoTouch('POST', `/api/documents/${BAD_ID}/sign-cert`, {
      metadata: {},
      title: '',
      certId: 'e3e70682-c209-1cac-a29f-6fbed82c07cd',
    });
  });

  it('POST /api/documents/{bad}/version', async () => {
    await expect400NoRepoTouch('POST', `/api/documents/${BAD_ID}/version`, {
      action: 'watermark',
      newContentHash: '0'.repeat(64),
      metadata: {},
      title: '',
    });
  });

  it('GET /api/documents/{bad}/sig-json (public router) is guarded too', async () => {
    const res = await fetch(`${baseUrl}/api/documents/${BAD_ID}/sig-json`);
    expect(res.status).toBe(400);
    const payload = (await res.json()) as ErrorEnvelope;
    expect(payload.error?.code).toBe('VALIDATION_ERROR');
  });
});

describe('KS-466 §8 — charset-legal ids still flow to the handlers', () => {
  it('a real-shaped id reaches the repository (404 when absent, not 400/500)', async () => {
    mockGetDocument.mockResolvedValueOnce(null);
    const res = await fetch(`${baseUrl}/api/documents/doc-1777346021120-1e528170`);
    expect(res.status).toBe(404);
    expect(mockGetDocument).toHaveBeenCalledTimes(1);
  });

  it("the ticket's id `0` on POST /lifecycle-events is a 404, never a 500", async () => {
    mockGetDocument.mockResolvedValueOnce(null);
    const res = await fetch(`${baseUrl}/api/documents/0/lifecycle-events`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      // KS-537: mirrors the published spec example — which deliberately no
      // longer contains an email (the old subjectEmail example was copied
      // into real rows by this very test).
      body: JSON.stringify({ action: 'rights-unassign', payload: { rightsProfile: 'reviewer', reference: 'case-8891' } }),
    });
    expect(res.status).toBe(404);
    const payload = (await res.json()) as ErrorEnvelope;
    expect(payload.error?.code).toBe('NOT_FOUND');
  });
});
