/**
 * KS-1228 — a REFUSED request writes no action_provenance row.
 *
 * `/:id/version`, `/:id/share` and `/:id/transfer-custody` called `handleOnBehalfOf` near the top of the
 * handler. For a connector sending `onBehalfOf` that validates the field AND records the provenance row
 * (an INSERT INTO action_provenance for the document id), BEFORE the refusals that follow. So a refused
 * request left a row for an action that never happened (the #1031 gate, finding D1). `action_provenance`
 * .document_id is deliberately not a foreign key, so nothing downstream rejects the row.
 *
 * Now the field is still validated where it was (a bad `onBehalfOf` refuses first, as before), and the
 * row is recorded only once the action has happened. `/revoke` already did this (KS-566).
 * `POST /api/certifications/issue` had the same defect in a narrower form. It recorded the row before the
 * lineage 422, the production anchoring 503 and the save-time 400/503s, though after the KS-1213 type
 * guard (the only refusal the ticket measured there). Measured at develop 8b9c3f022: its 422 wrote 1 row.
 *
 * Harness: the ks1213 suite's pattern. The real documentsRouter and certificationsRouter over one
 * in-memory document store; `recordActionProvenance` mocked and counted; `resolveOnBehalfOf` stubbed
 * (no DB), returning null unless a cell sets a resolved user.
 */
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@127.0.0.1:1/test';
process.env.SIMULATE_ANCHORING = 'true';
// Lifecycle anchors (share / transfer-custody) and the issue anchor go to a closed port: both paths
// degrade to "no anchor id" by design, so the domain write still completes.
// KS-1266: port 2, not port 1 — port 1 is on the Fetch-spec bad-port list and undici refuses
// it before any socket opens, so the "closed port" above was not what produced the failure.
process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';

const store = new Map<string, any>();
const mockRecord = jest.fn(async (_rec: Record<string, unknown>) => undefined);
// KS-1263: recorders for the STRUCTURAL property — one transaction per request, both writes inside it.
const mockWithTenantCalls: string[] = [];
const mockTxWrites: string[] = [];
let mockResolvedUserId: string | null = null;
const mockAssertNoCycle = jest.fn(async () => undefined);
const mockSaveCertification = jest.fn(async () => undefined);
// KS-1263: the second parameter is the db client `/share` passes; the real createShare has taken it
// since KS-458. The stub declared only the first, so a cell could not assert WHICH client was used.
const mockCreateShare = jest.fn(async (input: Record<string, unknown>, _db?: unknown) => ({
  id: 'share-1228', recipientEmail: input.recipientEmail ?? null, recipientUserId: input.recipientUserId ?? null, shareType: input.shareType,
}));
let mockHolderRows: Array<{ ok: number }> = [{ ok: 1 }];
const mockQueryRaw = jest.fn(async (strings: TemplateStringsArray) => {
  const sql = strings.join('?');
  if (sql.includes('FROM users')) return mockHolderRows;
  if (sql.includes('INSERT INTO custody_events')) return [{ id: 'evt-1228' }];
  return [];
});

jest.mock('../repositories/documentRepo', () => ({
  getDocument: jest.fn(async (id: string) => store.get(id) ?? null),
  listDocuments: jest.fn(async () => ({ items: [...store.values()], total: store.size })),
  saveDocument: jest.fn(async (record: any) => {
    store.set(record.id, JSON.parse(JSON.stringify(record)));
    return { dbId: '99999999-9999-4999-8999-999999999999', inserted: true };
  }),
  updateDocument: jest.fn(async () => undefined),
  getSigningRequest: jest.fn(),
  saveSigningRequest: jest.fn(),
  deleteSigningRequest: jest.fn(),
  generateContentHash: jest.fn(() => 'a'.repeat(64)),
  seedDemoDocuments: jest.fn(async () => undefined),
  assertNoCycle: (...a: unknown[]) => mockAssertNoCycle(...(a as [])),
  getOrganizationExternalRef: jest.fn(async () => null),
}));
jest.mock('../repositories/certificationRepo', () => ({
  initRepo: jest.fn(async () => undefined),
  getCertification: jest.fn(),
  saveCertification: (...a: unknown[]) => mockSaveCertification(...(a as [])),
  listCertifications: jest.fn(),
  saveShare: jest.fn(),
  getSharesByCertification: jest.fn(),
  getLineageEvents: jest.fn(),
}));
jest.mock('../db', () => {
  const client = {
    $queryRaw: (...a: unknown[]) => mockQueryRaw(...(a as [TemplateStringsArray])),
    $executeRaw: jest.fn(async () => 1),
    $executeRawUnsafe: jest.fn(),
    $queryRawUnsafe: jest.fn(),
  };
  // KS-1263: /share and /transfer-custody run their writes inside withTenant(). The callback gets
  // the SAME client this suite already observes, so the existing assertions still see them. A mock
  // cannot roll back; the behavioural rollback cell is OWED at the tier-1 gate (real Postgres).
  const txClient = {
    // KS-1263: the client withTenant hands its callback. Every write through it is recorded, so a cell
    // can assert BOTH writes landed inside the ONE transaction rather than beside it.
    $queryRaw: (...a: unknown[]) => { mockTxWrites.push('queryRaw'); return client.$queryRaw(...(a as [TemplateStringsArray])); },
    $executeRaw: async (..._a: unknown[]) => { mockTxWrites.push('executeRaw'); return 1; },
    $queryRawUnsafe: jest.fn(),
    $executeRawUnsafe: jest.fn(),
  };
  return {
    prisma: client,
    // KS-1263 G-S2: the mock EXPORTS the client withTenant hands out, so a cell can assert the
    // identity of what `/share` passed rather than only that the two calls agreed. Without this,
    // passing the MODULE client to every recipient satisfies `tx1 === tx0` and the cell stays green
    // while every write has left the transaction. Measured: the gate's tamper passed 29/29.
    __txClient: txClient,
    withTenant: async (t: string, fn: (tx: unknown) => Promise<unknown>) => {
      mockWithTenantCalls.push(t);
      return fn(txClient);
    },
  };
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
    recordActionProvenance: (rec: Record<string, unknown>) => mockRecord(rec),
    resolveOnBehalfOf: jest.fn(async () => mockResolvedUserId),
    getCreationProvenance: jest.fn(async () => null),
    wasCreatedByConnector: jest.fn(async () => false),
  };
});
// KS-1061: through makeSharedMock. The routes' own shared imports stay real.
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
import { certificationsRouter } from '../routes/certifications';

const TENANT = 'a0000000-0000-4000-8000-000000000001';
const CONNECTOR = {
  userId: 'connector:ks1228-conn',
  role: 'connector',
  scopes: ['documents:write', 'documents:read', 'documents:share', 'documents:transfer-custody', 'certifications:write'],
  organizationId: 'd0000000-0000-4000-8000-000000001228',
  tenantId: TENANT,
};
const OBO = { email: 'person.1228@example.com', displayName: 'Person 1228' };
const SOURCE_ID = 'doc-src-1228';
const OWNER = '11111111-2222-4333-8444-555555551228';
const HOLDER = '22222222-3333-4444-8555-666666661228';
const RESOLVED = '33333333-4444-4555-8666-777777771228';
const HASH = 'b'.repeat(64);

const app = express();
app.use((req: any, _res, next) => { req.tenantId = TENANT; next(); });
app.use('/api/documents', express.json(), documentsRouter);
app.use('/api/certifications', express.json(), certificationsRouter);
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
  store.set(SOURCE_ID, { id: SOURCE_ID, type: 'DOCUMENT', status: 'draft', owner: { id: OWNER }, data: { title: 'src' }, contentHash: 'sha256:' + 'a'.repeat(64), signatures: [], createdAt: '2026-09-18T00:00:00Z', updatedAt: '2026-09-18T00:00:00Z' });
  mockRecord.mockClear();
  mockWithTenantCalls.length = 0;
  mockTxWrites.length = 0;
  mockCreateShare.mockClear();
  mockAssertNoCycle.mockReset();
  mockAssertNoCycle.mockImplementation(async () => undefined);
  mockSaveCertification.mockReset();
  mockSaveCertification.mockImplementation(async () => undefined);
  mockResolvedUserId = null;
  mockHolderRows = [{ ok: 1 }];
});

const cycle = () => { throw Object.assign(new Error('cycle'), { code: 'LINEAGE_CYCLE' }); };

/** POST as the connector; returns the status, the error code and the provenance rows recorded. */
async function probe(path: string, body: Record<string, unknown>) {
  const res = await fetch(base + path, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(CONNECTOR) },
    body: JSON.stringify(body),
  });
  const j: any = await res.json().catch(() => null);
  // recordActionProvenance is fire-and-forget; let its microtask settle before counting.
  await new Promise((r) => setImmediate(r));
  return { status: res.status, code: j?.error?.code ?? null, rows: mockRecord.mock.calls.map((c) => c[0]) };
}

const version = (extra: Record<string, unknown> = {}, id = SOURCE_ID) =>
  probe(`/api/documents/${id}/version`, { action: 'watermark', newContentHash: HASH, onBehalfOf: OBO, ...extra });
const share = (extra: Record<string, unknown> = {}, id = SOURCE_ID) =>
  probe(`/api/documents/${id}/share`, { recipients: [{ email: 'recipient.1228@example.com' }], onBehalfOf: OBO, ...extra });
const transfer = (extra: Record<string, unknown> = {}, id = SOURCE_ID) =>
  probe(`/api/documents/${id}/transfer-custody`, { newHolderId: HOLDER, onBehalfOf: OBO, ...extra });
const issue = (extra: Record<string, unknown> = {}) =>
  probe('/api/certifications/issue', { type: 'verification_certificate', data: { title: 'cert 1228' }, onBehalfOf: OBO, ...extra });

describe('KS-1228 — a refused request writes no action_provenance row', () => {
  describe('/:id/version', () => {
    it('🔴 a bad content hash: 400, no row', async () => {
      const r = await version({ newContentHash: 'not-a-hash' });
      expect([r.status, r.code]).toEqual([400, 'VALIDATION_ERROR']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 an unknown document: 404, no row', async () => {
      const r = await version({}, 'doc-missing-1228');
      expect([r.status, r.code]).toEqual([404, 'NOT_FOUND']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 the KS-1213 type guard (metadata.documentType differs): 400, no row', async () => {
      const r = await version({ metadata: { documentType: 'PROPERTY_DEED' } });
      expect([r.status, r.code]).toEqual([400, 'BAD_REQUEST']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 a lineage cycle: 422, no row', async () => {
      mockAssertNoCycle.mockImplementation(async () => cycle());
      const r = await version();
      expect([r.status, r.code]).toEqual([422, 'LINEAGE_CYCLE']);
      expect(r.rows).toHaveLength(0);
    });
    it('KS-1267: saveDocument throws: 500, no row (the row is recorded only after the save)', async () => {
      jest.requireMock('../repositories/documentRepo').saveDocument.mockImplementationOnce(async () => { throw new Error('ks1267 save failed'); });
      const r = await version();
      expect([r.status, r.code]).toEqual([500, 'INTERNAL_ERROR']);
      expect(r.rows).toHaveLength(0);
    });
    it('control: a version that is created records exactly one row, for the source, as version:watermark', async () => {
      const r = await version();
      expect(r.status).toBe(201);
      expect(r.rows).toHaveLength(1);
      expect(r.rows[0]).toMatchObject({ documentId: SOURCE_ID, action: 'version:watermark', obo: OBO });
    });
  });

  describe('/:id/share', () => {
    it('🔴 an unknown document: 404, no row', async () => {
      const r = await share({}, 'doc-missing-1228');
      expect([r.status, r.code]).toEqual([404, 'NOT_FOUND']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 a recipient userId that is not a uuid: 400, no row', async () => {
      const r = await share({ recipients: [{ userId: 'not-a-uuid' }] });
      expect([r.status, r.code]).toEqual([400, 'VALIDATION_ERROR']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 the target vanishes at share time (SHARE_TARGET_NOT_FOUND): 404, no row', async () => {
      mockCreateShare.mockImplementationOnce(async () => { throw Object.assign(new Error('gone'), { code: 'SHARE_TARGET_NOT_FOUND' }); });
      const r = await share();
      expect([r.status, r.code]).toEqual([404, 'NOT_FOUND']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 an unstorable field at share time (SQLSTATE 22007): 400, no row', async () => {
      mockCreateShare.mockImplementationOnce(async () => { throw Object.assign(new Error('invalid datetime'), { code: '22007' }); });
      const r = await share({ expiresAt: 'not-a-date' });
      expect([r.status, r.code]).toEqual([400, 'VALIDATION_ERROR']);
      expect(r.rows).toHaveLength(0);
    });
    it('control: a share that is created records exactly one row, and the resolved person is still the sharer', async () => {
      mockResolvedUserId = RESOLVED;
      const r = await share();
      expect(r.status).toBe(201);
      expect(r.rows).toHaveLength(1);
      expect(r.rows[0]).toMatchObject({ documentId: SOURCE_ID, action: 'share', obo: OBO, resolvedUserId: RESOLVED });
      expect(mockCreateShare).toHaveBeenCalledTimes(1);
      expect(mockCreateShare.mock.calls[0][0]).toMatchObject({ sharedById: RESOLVED });
    });
  });

  describe('KS-1263 — the multi-write is ONE transaction (structural)', () => {
    // The BEHAVIOURAL property (a refusal at recipient k > 1 rolls the earlier rows back) cannot be
    // proved here: this suite mocks `../db`, and a mock cannot ROLL BACK. That cell is written for the
    // integration config and is OWED at the tier-1 gate against a real Postgres. What IS provable here
    // is the structure the rollback depends on — one withTenant call per request, with both writes
    // inside it. Splitting the writes into two withTenant calls reds these two cells.
    it('🔴 KS-1263 G-S1 /transfer-custody: ONE withTenant, and BOTH writes run on the client it hands out', async () => {
      const r = await transfer();
      expect(r.status).toBe(201);
      expect(mockWithTenantCalls).toHaveLength(1);
      // the custody INSERT (queryRaw … RETURNING id) and the owner flip (executeRaw), both on the tx
      expect(mockTxWrites).toEqual(['queryRaw', 'executeRaw']);
    });
    it('🔴 KS-1263 G-S2 /share: ONE withTenant, and every recipient is written on the SAME tx client', async () => {
      const r = await share({ recipients: [{ email: 'a@example.test' }, { email: 'b@example.test' }] });
      expect(r.status).toBe(201);
      expect(mockWithTenantCalls).toHaveLength(1);
      expect(mockCreateShare).toHaveBeenCalledTimes(2);
      const tx0 = mockCreateShare.mock.calls[0][1];
      const tx1 = mockCreateShare.mock.calls[1][1];
      expect(tx0).toBeDefined();
      expect(tx1).toBe(tx0);
      // KS-1263 G-S2 (round 2): AGREEMENT IS NOT IDENTITY. `tx1 === tx0` holds just as well when
      // `/share` passes the module client to both recipients — and then neither write is in the
      // transaction and the rollback this ticket exists for cannot happen. Name the client.
      const dbMock = require('../db');
      expect(tx0).toBe(dbMock.__txClient);
      expect(tx0).not.toBe(dbMock.prisma);
    });
  });

  describe('/:id/transfer-custody', () => {
    it('🔴 no holder named: 400, no row', async () => {
      const r = await transfer({ newHolderId: undefined });
      expect([r.status, r.code]).toEqual([400, 'VALIDATION_ERROR']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 a holder id that is not a uuid: 400, no row', async () => {
      const r = await transfer({ newHolderId: 'not-a-uuid' });
      expect([r.status, r.code]).toEqual([400, 'VALIDATION_ERROR']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 an unknown document: 404, no row', async () => {
      const r = await transfer({}, 'doc-missing-1228');
      expect([r.status, r.code]).toEqual([404, 'NOT_FOUND']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 an unknown holder: 404, no row', async () => {
      mockHolderRows = [];
      const r = await transfer();
      expect([r.status, r.code]).toEqual([404, 'RECIPIENT_NOT_FOUND']);
      expect(r.rows).toHaveLength(0);
    });
    it('control: a transfer that is recorded records exactly one row, as transfer-custody', async () => {
      const r = await transfer();
      expect(r.status).toBe(201);
      expect(r.rows).toHaveLength(1);
      expect(r.rows[0]).toMatchObject({ documentId: SOURCE_ID, action: 'transfer-custody', obo: OBO });
    });
  });

  describe('a bad onBehalfOf still refuses first, before any other check (the order KS-480 set)', () => {
    it.each([
      ['version', () => version({ onBehalfOf: null, newContentHash: 'not-a-hash' })],
      ['share', () => share({ onBehalfOf: null }, 'doc-missing-1228')],
      ['transfer', () => transfer({ onBehalfOf: null }, 'doc-missing-1228')],
    ] as const)('%s: onBehalfOf null wins over the later refusal: 400 BAD_REQUEST, no row', async (_name, call) => {
      const r = await call();
      expect([r.status, r.code]).toEqual([400, 'BAD_REQUEST']);
      expect(r.rows).toHaveLength(0);
    });
  });

  describe('POST /api/certifications/issue', () => {
    it('the KS-1213 type guard refuses before the row is recorded: 400, no row', async () => {
      const r = await issue({ parentDocumentId: SOURCE_ID, data: { title: 'cert 1228', documentType: 'PROPERTY_DEED' } });
      expect([r.status, r.code]).toEqual([400, 'BAD_REQUEST']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 a lineage cycle: 422, no row', async () => {
      mockAssertNoCycle.mockImplementation(async () => cycle());
      const r = await issue({ parentDocumentId: SOURCE_ID });
      expect([r.status, r.code]).toEqual([422, 'LINEAGE_CYCLE']);
      expect(r.rows).toHaveLength(0);
    });
    it('🔴 production with anchoring unreachable: 503, no row', async () => {
      // certifications.ts reads NODE_ENV at request time for this refusal only; anchoring is a closed port.
      const prior = process.env.NODE_ENV;
      process.env.NODE_ENV = 'production';
      try {
        const r = await issue();
        expect([r.status, r.code]).toEqual([503, 'SERVICE_UNAVAILABLE']);
        expect(r.rows).toHaveLength(0);
      } finally {
        process.env.NODE_ENV = prior;
      }
    });
    // The save-time refusals: saveCertification throws, and the handler's catch maps the error.
    it.each([
      ['a holder that does not exist (FK on owner_user_id)', new Error('insert violates foreign key constraint "documents_owner_user_id_fkey"'), 400, 'BAD_REQUEST'],
      ['another missing reference (FK)', new Error('insert violates foreign key constraint "documents_tenant_id_fkey"'), 400, 'BAD_REQUEST'],
      ['an unstorable value (SQLSTATE 22P05)', Object.assign(new Error('unsupported Unicode escape sequence'), { code: '22P05' }), 400, 'BAD_REQUEST'],
      ['a transient dependency failure (Prisma P2024)', Object.assign(new Error('Timed out fetching a new connection from the connection pool'), { code: 'P2024' }), 503, 'SERVICE_UNAVAILABLE'],
    ] as const)('🔴 refused at save time, %s: no row', async (_name, err, status, code) => {
      mockSaveCertification.mockImplementation(async () => { throw err; });
      const r = await issue();
      expect([r.status, r.code]).toEqual([status, code]);
      expect(r.rows).toHaveLength(0);
    });
    it('control: an issued certification records exactly one row, as certify', async () => {
      const r = await issue();
      expect(r.status).toBe(201);
      expect(r.rows).toHaveLength(1);
      expect(r.rows[0]).toMatchObject({ action: 'certify', obo: OBO });
    });
  });
});
