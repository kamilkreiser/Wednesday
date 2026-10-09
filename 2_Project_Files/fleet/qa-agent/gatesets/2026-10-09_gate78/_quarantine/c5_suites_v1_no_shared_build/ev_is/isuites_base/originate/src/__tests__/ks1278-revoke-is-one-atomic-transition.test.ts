/**
 * KS-1278 - POST /api/documents/:id/revoke decided "already revoked" on a READ and then ran an unconditional
 * UPDATE, so two overlapping revokes could both pass the read: 200 + 200, two updates, two provenance rows and two
 * anchor calls (batch gate N60-2, measured in-process). The fix moves the decision INTO the UPDATE: the revoke's
 * write refuses a row that is already revoked, and a revoke whose write changed no row answers the same 400 and
 * records nothing.
 *
 * Harness: the ks1264 suite's route harness, but with the REAL documentRepo over a mocked prisma (the ks521 shape),
 * so one request drives both product files. "The other revoke won" is planted as $executeRaw resolving 0 rows.
 */
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@127.0.0.1:1/test';
process.env.SIMULATE_ANCHORING = 'true';
// The revoke anchor goes to a refused loopback port, so it degrades to no anchor id (port 1 is a fetch bad port).
process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();
const mockRecord = jest.fn(async (_rec: Record<string, unknown>) => undefined);

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw, $executeRawUnsafe: jest.fn() },
  getTenantManager: jest.fn(() => null),
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
import { updateDocument } from '../repositories/documentRepo';

const TENANT = 'a0000000-0000-4000-8000-000000000001';
const CONNECTOR = { userId: 'connector:ks1278-conn', role: 'connector', scopes: ['documents:write', 'documents:read'], organizationId: 'd0000000-0000-4000-8000-000000001278', tenantId: TENANT };
const OBO = { email: 'person.1278@example.com', displayName: 'Person 1278' };
const DOC_ID = 'doc-1278';

/** A documents row as getDocument's SELECT projects it (the ks521 shape), owned by the connector, not revoked. */
function dbRow(status = 'draft'): Record<string, unknown> {
  return {
    id: '2539dc16-c5f1-4d8c-b7e4-2d3ff3551278',
    external_id: DOC_ID,
    document_type: 'general',
    status,
    owner_user_id: CONNECTOR.userId,
    title: 'KS-1278 doc',
    description: null,
    content_hash: 'sha256:' + 'a'.repeat(64),
    metadata: {},
    certification_metadata: {},
    created_at: new Date('2026-09-19T00:00:00.000Z'),
    updated_at: new Date('2026-09-19T00:00:00.000Z'),
  };
}

/** The revoke UPDATE among $executeRaw's calls (the one binding status 'revoked'). */
function revokeUpdateCall(): unknown[] | undefined {
  return mockExecuteRaw.mock.calls.find((c) => (c[0] as readonly string[]).join('?').includes('UPDATE documents SET') && c.slice(1).includes('revoked'));
}

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
  mockQueryRaw.mockReset();
  mockExecuteRaw.mockReset();
  mockRecord.mockClear();
  mockQueryRaw.mockImplementation(async () => [dbRow('draft')]);
  // KS-1278 round 2 (N-1393-2): emitLifecycleAnchor is module-local to routes/documents.ts
  // (:1261) and cannot be jest.mock'd, so its ONE observable is the POST it makes to
  // ANCHORING_SERVICE_URL + '/api/anchors'. Count only those; revoke() itself uses fetch.
  anchorFetches = 0;
  global.fetch = (async (input: unknown, init?: unknown) => {
    const url = typeof input === 'string' ? input : String((input as { url?: string })?.url ?? input);
    if (url.includes('/api/anchors')) anchorFetches += 1;
    return (realFetch as (a: unknown, b?: unknown) => Promise<Response>)(input, init);
  }) as unknown as typeof fetch;
});
afterAll(() => { global.fetch = realFetch; });

/**
 * KS-1278 round 2: a DRIVER SIMULATOR, not a constant.
 *
 * The existing cells drive `mockExecuteRaw.mockResolvedValue(n)`, which is right for them: they
 * plant "the other revoke won". The UUID-addressed cell below cannot use a constant -- the whole
 * question is whether the UPDATE's KEY resolves the row the read resolved, so a constant 1 is green
 * at both ends and a constant 0 is red at both. Neither measures the fix.
 *
 * So these two helpers answer as Postgres would for this one statement, given one fixture row and
 * the id the request addressed. They assert on the RESULT (status / rows), never on my SQL text;
 * the text is read only to learn WHICH COLUMN the statement keys on, which is the behaviour under
 * test. If the statement keys on neither shape the simulator KNOWS, it THROWS rather than returning
 * a default -- a mock that silently falls back is how a cell like this rots into a vacuous pass.
 */
function queryRawResolver(addressedId: string, row: Record<string, unknown>) {
  return async (strings: readonly string[], ..._vals: unknown[]) => {
    const sql = (strings as readonly string[]).join('?');
    if (!sql.includes('FROM documents')) return [];
    // getDocument tries external_id first (:238-:243), then the pkey (:244-:251). Anchor the uuid
    // probe on `WHERE id = ?::uuid`: a bare /id = \?::uuid/ also matches `tenant_id = ?::uuid`.
    if (/WHERE external_id = \?/.test(sql)) return addressedId === row.external_id ? [row] : [];
    if (/WHERE id = \?::uuid/.test(sql)) return addressedId === row.id ? [row] : [];
    return [];
  };
}

function executeRawSimulator(addressedId: string, row: Record<string, unknown>) {
  return async (strings: readonly string[], ..._vals: unknown[]) => {
    const sql = (strings as readonly string[]).join('?');
    if (!sql.includes('UPDATE documents SET')) return 1;
    const keysOnResolvedRow = sql.includes('WHERE id = COALESCE');
    const keysOnExternalId = /WHERE external_id = \?/.test(sql);
    if (keysOnResolvedRow === keysOnExternalId) {
      throw new Error('ks1278 simulator: the revoke UPDATE keys on neither shape this cell knows; ' +
        'the cell would otherwise pass vacuously. SQL was: ' + sql);
    }
    const isUuidShaped = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(addressedId);
    const resolved = keysOnResolvedRow
      // the COALESCE mirrors getDocument: external_id arm, then the pkey arm
      ? addressedId === row.external_id || (isUuidShaped && addressedId === row.id)
      : addressedId === row.external_id;
    return resolved ? 1 : 0;
  };
}

/** KS-1278 round 2: fetches emitLifecycleAnchor makes (documents.ts:1261 POSTs /api/anchors). */
let anchorFetches = 0;
const realFetch: typeof fetch = global.fetch;

/** POST /:id/revoke as the connector; returns the status, the error code and the provenance rows recorded. */
async function revoke(addressed: string = DOC_ID) {
  const res = await fetch(base + '/api/documents/' + addressed + '/revoke', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(CONNECTOR) },
    body: JSON.stringify({ reason: 'ks1278', onBehalfOf: OBO }),
  });
  const j: any = await res.json().catch(() => null);
  // recordActionProvenance is fire-and-forget; let its microtask settle before counting.
  await new Promise((r) => setImmediate(r));
  return { status: res.status, code: j?.error?.code ?? null, rows: mockRecord.mock.calls.length };
}

describe('KS-1278 /revoke is one atomic transition', () => {
  it('RED KS-1278 R1: a revoke whose UPDATE changed no row (another revoke won the race) answers 400 and records nothing', async () => {
    mockExecuteRaw.mockResolvedValue(0);
    const r = await revoke();
    // N-1393-2: "records nothing" was pinned by the provenance count alone, so the anchor half of
    // the claim was pinned by no cell at all. G8 (emitLifecycleAnchor moved onto the loser path,
    // before the null check) left all four cells GREEN at round 1. anchorFetches closes that.
    expect([r.status, r.code, r.rows, anchorFetches]).toEqual([400, 'BAD_REQUEST', 0, 0]);
  });

  it('RED KS-1278 R2: the revoke UPDATE itself refuses a row that is already revoked', async () => {
    mockExecuteRaw.mockResolvedValue(1);
    await revoke();
    const call = revokeUpdateCall();
    const sql = call ? (call[0] as readonly string[]).join('?') : '';
    // N-1393-2, round 2 follow-up. The two earlier forms of this assertion were both too weak, and
    // the tamper matrix is what showed it:
    //   * 'sql.includes("status IS DISTINCT FROM")' alone survives T5, which PREFIXES "TRUE OR " to
    //     the clause and makes the guard vacuous while leaving that substring intact.
    //   * 'bound.includes("revoked")' survives G7 (ifStatusIsNot: 'draft'), because this UPDATE
    //     binds 'revoked' THREE times and one of them is the SET clause's NEW STATUS, not the
    //     guard. Membership cannot tell those apart. Measured, not reasoned: the bound list is
    //     [false,'revoked',<metadata>,<certMeta>,'doc-1278',<tenant>,null,<tenant>,<tenant>,
    //      'revoked','revoked'].
    // So pin BOTH halves precisely: the guard clause by EXACT text (a prefix breaks it), and the
    // guard's own parameters BY POSITION. The two guard bindings are the LAST TWO in every variant
    // of this statement -- guarded and unguarded alike the guard is the final clause -- which is
    // why slice(-2) is used rather than the literal indices 9 and 10 that a changed SET list
    // would shift.
    const GUARD_SQL = 'AND (?::text IS NULL OR status IS DISTINCT FROM ?::text)';
    const guardBindings = call ? call.slice(1).slice(-2) : [];
    expect([call !== undefined, sql.includes(GUARD_SQL), guardBindings])
      .toEqual([true, true, ['revoked', 'revoked']]);
  });

  it('control KS-1278 C1: the revoke that changes the row answers 200 and records exactly one row', async () => {
    mockExecuteRaw.mockResolvedValue(1);
    const r = await revoke();
    expect([r.status, r.rows]).toEqual([200, 1]);
  });

  it('control KS-1278 C2: an ordinary update (no guard asked for) still returns the record when the driver reports 0 rows', async () => {
    mockExecuteRaw.mockResolvedValueOnce(0);
    const updated = await updateDocument(DOC_ID, TENANT, { status: 'signed' });
    expect(updated?.status).toBe('signed');
  });

  it('RED KS-1278 N1: a SEQUENTIAL revoke addressed by the platform documentUuid revokes the document - 200, status written, exactly one provenance row', async () => {
    // gate65 N-1393-1. getDocument resolves this id by the pkey fallback (documentRepo.ts:244-:251)
    // and the API hands clients that pkey as `documentUuid` (:172) -- but the guarded UPDATE keyed
    // on external_id, which is 'doc-1278' here, so it matched 0 rows and the route answered 400
    // "already revoked" for a document nobody had revoked. No race is involved.
    // RED at 4a1620588819 (400 / 0 rows), GREEN at this head.
    const row = dbRow('draft');
    const uuid = String(row.id);
    mockQueryRaw.mockImplementation(queryRawResolver(uuid, row));
    mockExecuteRaw.mockImplementation(executeRawSimulator(uuid, row));
    const r = await revoke(uuid);
    expect([r.status, r.code, r.rows]).toEqual([200, null, 1]);
  });

  it('control KS-1278 N2: a guarded revoke addressed by a NON-UUID external id still revokes - 200, one row, GREEN at both ends', async () => {
    // Wednesday's ANSWER 2026-10-05T22:14:59Z made this a condition of the fix: `${x}::uuid` on a
    // non-UUID string RAISES 22P02, so the resolver must bind null instead of casting (the
    // isValidUuid guard mirroring documentRepo.ts:244). This cell is GREEN at the base too -- it
    // does not prove the fix, it proves the fix broke nothing for the ordinary address form.
    const row = dbRow('draft');
    mockQueryRaw.mockImplementation(queryRawResolver(DOC_ID, row));
    mockExecuteRaw.mockImplementation(executeRawSimulator(DOC_ID, row));
    const r = await revoke(DOC_ID);
    expect([r.status, r.code, r.rows]).toEqual([200, null, 1]);
  });

  it('control KS-1278 N3: an UNGUARDED updateDocument still keys on external_id - the other 12 production callers are untouched', async () => {
    // The blast-radius control. 13 production updateDocument( callers; exactly ONE passes
    // ifStatusIsNot (routes/documents.ts:2398). This cell is what a tamper applying the new key to
    // EVERY path has to redden, and it is green at both ends by design.
    mockExecuteRaw.mockResolvedValue(1);
    await updateDocument(DOC_ID, TENANT, { status: 'signed' });
    const call = mockExecuteRaw.mock.calls.find((c) => (c[0] as readonly string[]).join('?').includes('UPDATE documents SET'));
    const sql = call ? (call[0] as readonly string[]).join('?') : '';
    expect([call !== undefined, /WHERE external_id = \?/.test(sql), sql.includes('WHERE id = COALESCE')])
      .toEqual([true, true, false]);
  });
});
