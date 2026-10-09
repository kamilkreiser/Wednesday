/**
 * KS-547 (KS-540 F-2) — POST /api/certifications/issue role gate.
 *
 * /issue was the one document-write verb with zero role/scope checks: the
 * gateway's requireScope short-circuits for JWT humans, and the handler
 * mounted authenticate() only — any authenticated user could certify. It now
 * gates on DOCUMENT_WRITE_ROLES + the `certifications:write` scope via
 * isAllowedByRoleOrScope, the same pattern as document create/version/share.
 *
 * The gate sits between authentication and body validation, so a caller that
 * passes it with an invalid body gets 400 VALIDATION_ERROR — that is how these
 * tests prove gate passage without mocking the whole happy path. Mock surface
 * mirrors ks444-certifications-issue-body-types.test.ts.
 */

jest.mock('../repositories/certificationRepo', () => ({
  initRepo: jest.fn(async () => undefined),
  getCertification: jest.fn(),
  saveCertification: jest.fn(),
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

// Mutable per-test caller — the mock factory reads it on every request.
let testUser: Record<string, unknown> | null = null;

jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = testUser;
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
beforeEach(() => {
  jest.clearAllMocks();
  testUser = null;
});

interface ErrorEnvelope {
  success?: boolean;
  error?: { code?: string; message?: string };
}

/** POST /issue with a deliberately invalid body (missing type/data). */
function issue(): Promise<Response> {
  return fetch(`${baseUrl}/api/certifications/issue`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({}),
  });
}

const BASE = { userId: '11111111-2222-4333-8444-555555555555', email: 'caller@example.com' };

describe('KS-547 — /certifications/issue role gate', () => {
  it.each(['OWNER', 'VERIFIER'])('403s a %s JWT caller (FORBIDDEN, before validation)', async (role) => {
    testUser = { ...BASE, role };
    const res = await issue();
    expect(res.status).toBe(403);
    const body = (await res.json()) as ErrorEnvelope;
    expect(body.success).toBe(false);
    expect(body.error?.code).toBe('FORBIDDEN');
  });

  it('403s a role-less authenticated caller', async () => {
    testUser = { ...BASE };
    const res = await issue();
    expect(res.status).toBe(403);
  });

  it.each(['ISSUER_ADMIN', 'ORG_ADMIN', 'SYSTEM_ADMIN', 'SUPER_ADMIN'])(
    'passes the gate for %s (invalid body reaches validation → 400)',
    async (role) => {
      testUser = { ...BASE, role };
      const res = await issue();
      expect(res.status).toBe(400);
      const body = (await res.json()) as ErrorEnvelope;
      expect(body.error?.code).toBe('VALIDATION_ERROR');
    },
  );

  it('passes the gate for a connector carrying certifications:write (KS-71 scope path)', async () => {
    testUser = { ...BASE, role: 'connector', scopes: ['certifications:write'] };
    const res = await issue();
    expect(res.status).toBe(400); // past the gate, failed body validation
  });

  it('403s a connector without the certifications:write scope', async () => {
    testUser = { ...BASE, role: 'connector', scopes: ['documents:write', 'certifications:read'] };
    const res = await issue();
    expect(res.status).toBe(403);
  });
});
