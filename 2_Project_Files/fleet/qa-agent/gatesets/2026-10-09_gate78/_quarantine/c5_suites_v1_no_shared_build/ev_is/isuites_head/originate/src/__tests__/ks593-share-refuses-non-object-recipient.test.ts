/**
 * KS-593 (not_a_server_error register) - POST /api/documents/:id/share answered a raw 500 for
 * `{"recipients":[null]}` (KS-593 register 2026-09-15: "POST /api/documents/{id}/share | 500 | {"recipients":[null]}").
 * The express-validator chain only checks that `recipients` is a non-empty array, and the up-front recipient
 * loop read `r.email` on each entry, so a null entry threw a TypeError inside the handler and the catch answered
 * 500 INTERNAL_ERROR. The loop now refuses a recipient that is not an object with the same 400 VALIDATION_ERROR
 * it gives one with neither an email nor a userId, before any share row is written.
 *
 * Harness: the ks1228 suite's pattern - the real documentsRouter over an in-memory document store; createShare
 * mocked and counted; withTenant hands the callback a recording client. No database, no network beyond 127.0.0.1.
 */
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@127.0.0.1:1/test';
process.env.SIMULATE_ANCHORING = 'true';
process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';

const store = new Map<string, any>();
const mockCreateShare = jest.fn(async (input: Record<string, unknown>, _db?: unknown) => ({
  id: 'share-593', recipientEmail: input.recipientEmail ?? null, recipientUserId: input.recipientUserId ?? null, shareType: input.shareType,
}));

jest.mock('../repositories/documentRepo', () => ({
  getDocument: jest.fn(async (id: string) => store.get(id) ?? null),
  listDocuments: jest.fn(async () => ({ items: [...store.values()], total: store.size })),
  saveDocument: jest.fn(async () => ({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true })),
  updateDocument: jest.fn(async () => undefined),
  getSigningRequest: jest.fn(),
  saveSigningRequest: jest.fn(),
  deleteSigningRequest: jest.fn(),
  generateContentHash: jest.fn(() => 'a'.repeat(64)),
  seedDemoDocuments: jest.fn(async () => undefined),
  assertNoCycle: jest.fn(async () => undefined),
  getOrganizationExternalRef: jest.fn(async () => null),
}));
jest.mock('../db', () => {
  const client = { $queryRaw: jest.fn(async () => []), $executeRaw: jest.fn(async () => 1), $executeRawUnsafe: jest.fn(), $queryRawUnsafe: jest.fn() };
  return { prisma: client, withTenant: async (_t: string, fn: (tx: unknown) => Promise<unknown>) => fn(client) };
});
jest.mock('../services/chargeEvents', () => ({ createChargeEvent: jest.fn(async () => ({ id: 'charge-1' })), getChargeEventsByCertification: jest.fn() }));
jest.mock('../utils/notificationClient', () => ({ notifyDocumentCertified: jest.fn(async () => undefined), notifyDocumentRevoked: jest.fn(async () => undefined), notifyDocumentShared: jest.fn(async () => undefined) }));
jest.mock('../repositories/shareRepo', () => ({ createShare: (...a: unknown[]) => mockCreateShare(...(a as [Record<string, unknown>])) }));
jest.mock('../repositories/lifecycleEventRepo', () => ({ createLifecycleEvent: jest.fn(), setLifecycleEventAnchor: jest.fn(), listLifecycleEvents: jest.fn() }));
jest.mock('../events', () => ({ publishEvent: jest.fn(async () => undefined), EventTypes: { DOCUMENT_CREATED: 'document.created', DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred', DOCUMENT_VERSIONED: 'document.versioned', CERTIFICATION_ISSUED: 'certification.issued' } }));
jest.mock('../services/threadTokenClient', () => ({ mintAndRegisterThreadToken: jest.fn(async () => ({})) }));
jest.mock('../routes/verification', () => ({ registerInPlatformRegistry: jest.fn(async () => undefined) }));
jest.mock('../services/anchorStateSync', () => ({ pollAnchorUntilConfirmed: jest.fn(async () => undefined), reconcileDocumentAnchorState: jest.fn(async (d: any) => d) }));
jest.mock('../services/provenance', () => {
  const actual = jest.requireActual('../services/provenance');
  return {
    ...actual,
    recordActionProvenance: jest.fn(async () => undefined),
    resolveOnBehalfOf: jest.fn(async () => null),
    getCreationProvenance: jest.fn(async () => null),
    wasCreatedByConnector: jest.fn(async () => false),
  };
});
jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    hasNulByte: jest.requireActual('@secuura/shared').hasNulByte,
    runWithTenantId: jest.requireActual('@secuura/shared').runWithTenantId,
    encryptField: jest.requireActual('@secuura/shared').encryptField,
    decryptField: jest.requireActual('@secuura/shared').decryptField,
    lookupHash: jest.requireActual('@secuura/shared').lookupHash,
  }),
);
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = JSON.parse(String(req.headers['x-probe-user'] || '{}'));
    next();
  },
}));
jest.mock('../utils/logger', () => ({ logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() } }));

import express from 'express';
import { documentsRouter } from '../routes/documents';

const TENANT = 'a0000000-0000-4000-8000-000000000593';
const CONNECTOR = {
  userId: 'connector:ks593-conn',
  role: 'connector',
  scopes: ['documents:read', 'documents:write', 'documents:share'],
  organizationId: 'd0000000-0000-4000-8000-000000000593',
  tenantId: TENANT,
};
const DOC_ID = 'doc-share-593';

const app = express();
app.use((req: any, _res, next) => { req.tenantId = TENANT; next(); });
app.use('/api/documents', express.json(), documentsRouter);
let base = '';
let server: ReturnType<typeof app.listen>;
beforeAll(async () => {
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  const a = server.address();
  base = 'http://127.0.0.1:' + String(typeof a === 'object' && a ? a.port : 0);
});
afterAll(() => { server?.close(); });
beforeEach(() => {
  store.clear();
  store.set(DOC_ID, { id: DOC_ID, type: 'DOCUMENT', status: 'draft', owner: { id: '11111111-2222-4333-8444-555555550593' }, data: { title: 'share' }, contentHash: 'sha256:' + 'a'.repeat(64), signatures: [], createdAt: '2026-10-05T00:00:00Z', updatedAt: '2026-10-05T00:00:00Z' });
  mockCreateShare.mockClear();
});

async function share(recipients: unknown): Promise<{ status: number; code: string | null; writes: number }> {
  const res = await fetch(`${base}/api/documents/${DOC_ID}/share`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(CONNECTOR) },
    body: JSON.stringify({ recipients }),
  });
  const j: any = await res.json().catch(() => null);
  return { status: res.status, code: j?.error?.code ?? null, writes: mockCreateShare.mock.calls.length };
}

describe('KS-593: POST /api/documents/:id/share refuses a recipient that is not an object with 400, not a raw 500', () => {
  it('RED KS-593 SN1: recipients [null] answers 400 VALIDATION_ERROR and writes no share', async () => {
    expect(await share([null])).toEqual({ status: 400, code: 'VALIDATION_ERROR', writes: 0 });
  });

  it('RED KS-593 SN2: a null after a valid recipient answers 400 and writes no share (validated up-front)', async () => {
    expect(await share([{ email: 'first.593@example.test' }, null])).toEqual({ status: 400, code: 'VALIDATION_ERROR', writes: 0 });
  });

  it('control KS-593 SNC1: a valid recipient is still shared (201, one write)', async () => {
    expect(await share([{ email: 'ok.593@example.test' }])).toEqual({ status: 201, code: null, writes: 1 });
  });

  it('control KS-593 SNC2: an object with neither email nor userId is still refused with 400 VALIDATION_ERROR', async () => {
    expect(await share([{ name: 'nobody' }])).toEqual({ status: 400, code: 'VALIDATION_ERROR', writes: 0 });
  });

  it('control KS-593 SNC3: a non-uuid userId is still refused with 400 VALIDATION_ERROR', async () => {
    expect(await share([{ userId: 'not-a-uuid' }])).toEqual({ status: 400, code: 'VALIDATION_ERROR', writes: 0 });
  });
});
