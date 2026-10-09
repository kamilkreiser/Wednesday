/**
 * KS-1264 - /revoke records its action_provenance row only after updateDocument.
 *
 * POST /api/documents/:id/revoke called handleOnBehalfOf, which validates onBehalfOf AND records the
 * provenance row, just before updateDocument. So when updateDocument threw, the answer was 500, the
 * revoke did not happen, and the row existed (batch gate N43-3, case C2: 500 and 1 row).
 * KS-1228 split the helper for /version, /share and /transfer-custody. /revoke now uses the same split:
 * checkOnBehalfOf where the call was, recordOnBehalfOf after updateDocument.
 *
 * Harness: the ks1213 suite's pattern. The real documentsRouter over an in-memory document store,
 * recordActionProvenance mocked and counted, resolveOnBehalfOf stubbed to null (no DB).
 */
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@127.0.0.1:1/test';
process.env.SIMULATE_ANCHORING = 'true';
// The revoke anchor goes to a refused loopback port, so it degrades to no anchor id (port 1 is a fetch bad port).
process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';

const store = new Map<string, any>();
const mockRecord = jest.fn(async (_rec: Record<string, unknown>) => undefined);
const mockUpdateDocument = jest.fn(async () => undefined);

jest.mock('../repositories/documentRepo', () => ({
  getDocument: jest.fn(async (id: string) => store.get(id) ?? null),
  listDocuments: jest.fn(async () => ({ items: [...store.values()], total: store.size })),
  saveDocument: jest.fn(async () => ({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true })),
  updateDocument: (...a: unknown[]) => mockUpdateDocument(...(a as [])),
  getSigningRequest: jest.fn(),
  saveSigningRequest: jest.fn(),
  deleteSigningRequest: jest.fn(),
  generateContentHash: jest.fn(() => 'a'.repeat(64)),
  seedDemoDocuments: jest.fn(async () => undefined),
  assertNoCycle: jest.fn(async () => undefined),
  getOrganizationExternalRef: jest.fn(async () => null),
}));
jest.mock('../repositories/certificationRepo', () => ({
  initRepo: jest.fn(async () => undefined),
  getCertification: jest.fn(),
  saveCertification: jest.fn(async () => undefined),
  listCertifications: jest.fn(),
  saveShare: jest.fn(),
  getSharesByCertification: jest.fn(),
  getLineageEvents: jest.fn(),
}));
jest.mock('../db', () => ({ prisma: { $queryRaw: jest.fn(), $executeRaw: jest.fn(), $executeRawUnsafe: jest.fn() } }));
jest.mock('../services/chargeEvents', () => ({ createChargeEvent: jest.fn(async () => ({ id: 'charge-1' })), getChargeEventsByCertification: jest.fn() }));
jest.mock('../utils/notificationClient', () => ({ notifyDocumentCertified: jest.fn(async () => undefined), notifyDocumentRevoked: jest.fn(async () => undefined), notifyDocumentShared: jest.fn(async () => undefined) }));
jest.mock('../repositories/shareRepo', () => ({ createShare: jest.fn() }));
jest.mock('../repositories/lifecycleEventRepo', () => ({ createLifecycleEvent: jest.fn(), setLifecycleEventAnchor: jest.fn(), listLifecycleEvents: jest.fn() }));
jest.mock('../events', () => ({ publishEvent: jest.fn(async () => undefined), EventTypes: { DOCUMENT_CREATED: 'document.created', DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred', DOCUMENT_VERSIONED: 'document.versioned', CERTIFICATION_ISSUED: 'certification.issued' } }));
jest.mock('../services/threadTokenClient', () => ({ mintAndRegisterThreadToken: jest.fn(async () => ({})) }));
jest.mock('../routes/verification', () => ({ registerInPlatformRegistry: jest.fn(async () => undefined) }));
jest.mock('../services/anchorStateSync', () => ({ pollAnchorUntilConfirmed: jest.fn(async () => undefined), reconcileDocumentAnchorState: jest.fn(async (d: any) => d) }));
jest.mock('../services/provenance', () => {
  const actual = jest.requireActual('../services/provenance');
  return {
    ...actual,
    recordActionProvenance: (rec: Record<string, unknown>) => mockRecord(rec),
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

const TENANT = 'a0000000-0000-4000-8000-000000000001';
const CONNECTOR = { userId: 'connector:ks1264-conn', role: 'connector', scopes: ['documents:write', 'documents:read'], organizationId: 'd0000000-0000-4000-8000-000000001264', tenantId: TENANT };
const OBO = { email: 'person.1264@example.com', displayName: 'Person 1264' };
const DOC_ID = 'doc-1264';

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
  store.set(DOC_ID, { id: DOC_ID, type: 'DOCUMENT', status: 'draft', owner: { id: CONNECTOR.userId }, data: { title: 'doc 1264' }, contentHash: 'sha256:' + 'a'.repeat(64), signatures: [], createdAt: '2026-09-19T00:00:00Z', updatedAt: '2026-09-19T00:00:00Z' });
  mockRecord.mockClear();
  mockUpdateDocument.mockReset();
  mockUpdateDocument.mockImplementation(async () => undefined);
});

/** POST /:id/revoke as the connector; returns the status, the error code, the updates made and the provenance rows recorded. */
async function revoke(body: Record<string, unknown>) {
  const res = await fetch(base + '/api/documents/' + DOC_ID + '/revoke', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(CONNECTOR) },
    body: JSON.stringify(body),
  });
  const j: any = await res.json().catch(() => null);
  // recordActionProvenance is fire-and-forget; let its microtask settle before counting.
  await new Promise((r) => setImmediate(r));
  return { status: res.status, code: j?.error?.code ?? null, updates: mockUpdateDocument.mock.calls.length, rows: mockRecord.mock.calls.map((c) => c[0]) };
}

describe('KS-1264 /revoke: the provenance row is recorded only after updateDocument', () => {
  it('control: a revoke that happens records exactly one row, as revoke', async () => {
    const r = await revoke({ reason: 'ks1264', onBehalfOf: OBO });
    expect([r.status, r.updates]).toEqual([200, 1]);
    expect(r.rows).toHaveLength(1);
    expect(r.rows[0]).toMatchObject({ documentId: DOC_ID, action: 'revoke', obo: OBO });
  });

  it('control: a bad onBehalfOf (null) is still refused 400 before the update, with no row', async () => {
    const r = await revoke({ reason: 'ks1264', onBehalfOf: null });
    expect([r.status, r.code, r.updates]).toEqual([400, 'BAD_REQUEST', 0]);
    expect(r.rows).toHaveLength(0);
  });

  it('🔴 KS-1264: updateDocument throws: 500, no row (the revoke did not happen)', async () => {
    mockUpdateDocument.mockImplementationOnce(async () => { throw new Error('ks1264 update failed'); });
    const r = await revoke({ reason: 'ks1264', onBehalfOf: OBO });
    expect([r.status, r.code]).toEqual([500, 'INTERNAL_ERROR']);
    expect(r.rows).toHaveLength(0);
  });
});
