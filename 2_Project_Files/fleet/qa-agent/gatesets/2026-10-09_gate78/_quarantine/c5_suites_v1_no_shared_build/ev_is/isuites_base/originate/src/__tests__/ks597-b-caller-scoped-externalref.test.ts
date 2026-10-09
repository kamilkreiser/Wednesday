/**
 * =============================================================================
 * KS-597 option B — organizationUuid may name the ACTING Organisation by its K
 * id OR by its own Platform S externalRef, and nothing else
 * =============================================================================
 * Kam's ruling, 2026-09-11 (card `secuura-ks597-bind-compares-two-id-spaces-now-deployed`,
 * option B): K resolves S's externalRef, then compares. His 2026-09-07 bind stays.
 *
 * Stuart's measurement on KS-597 (2026-09-10): a Platform S connector sends its
 * own Organisation GUID — the value it registered as `externalRef` — while the
 * caller's org is K's `organizations.id`. The bind compared the two raw, so every
 * S originate was refused (144 refusals in 45 minutes on his stack).
 *
 * The rule is CALLER-SCOPED, never a global lookup by ref: the only
 * organisation read is the caller's own, by id and request tenant. `externalRef`
 * carries no unique index (register-connector keys idempotency on a lockless
 * check-then-insert), so resolving the CLAIM would pick an organisation by chance
 * when two share a ref. Resolving the CALLER cannot (row 6).
 *
 * One cell per row of the s180 resolution table, plus Wednesday's (b)-(d):
 *   1 no claim · 2 caller's K id · 3 caller's own ref · 4 another org · 5 nothing
 *   6 shared ref · 7 org-less caller · 8 malformed · 9 read throws · 10 issuer ≠ key
 * The org read is mocked here; the real read under originate's real role and
 * tenant GUC is `ks597-b-caller-org-externalref.integration.test.ts`.
 * =============================================================================
 */

process.env.SIMULATE_ANCHORING = 'true';
// routes/documents imports services/provenance -> db -> config, which demands
// DATABASE_URL at module load — same shim as the sibling suites.
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const DB_ID = '99999999-9999-4999-8999-999999999999';
const mockSaveDocument = jest.fn(async (..._args: any[]) => ({ dbId: DB_ID, inserted: true }));
const mockGetDocument = jest.fn(async (..._args: any[]) => null as any);
// Keyed by organisation id: what `organizations.metadata->>'externalRef'` holds
// for that org in the request tenant. A key the map does not hold reads as no row.
let storedRefs: Record<string, string | null> = {};
const mockGetOrganizationExternalRef = jest.fn(async (orgId: string, _tenantId: string, _db?: unknown) =>
  (orgId in storedRefs ? storedRefs[orgId] : null));

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
  getOrganizationExternalRef: mockGetOrganizationExternalRef,
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

const TENANT = 'dddddddd-0000-4000-8000-00000000000d';
// The acting principal and its tenant are what this suite varies. The tenant is
// set the way `extractTenantContext` leaves it (`req.tenantId`), so the cells can
// prove the read is scoped to the REQUEST's tenant rather than to a default.
let currentUser: Record<string, unknown> = {};
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = currentUser;
    req.tenantId = TENANT;
    next();
  },
}));

jest.mock('../middleware/rbac', () => ({ isAllowedByRoleOrScope: () => true }));
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
    // KS-860: loopback only — never `app.listen(0, cb)`, which binds all interfaces.
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => server?.close());

const USER_ID = '11111111-2222-4333-8444-555555555555';
// K `organizations.id` values — what the key's JWT carries as `organizationId`.
const ORG_A = 'aaaaaaaa-0000-4000-8000-00000000000a';
const ORG_B = 'bbbbbbbb-0000-4000-8000-00000000000b';
// Platform S Organisation GUIDs — what register-connector stored as `externalRef`.
const REF_A = 'c0ffee00-1111-4111-8111-0000000000a1';
const REF_B = 'c0ffee00-2222-4222-8222-0000000000b2';
const HASH = 'b'.repeat(64);

beforeEach(() => {
  jest.clearAllMocks();
  mockSaveDocument.mockImplementation(async (..._args: any[]) => ({ dbId: DB_ID, inserted: true }));
  mockGetDocument.mockResolvedValue(null);
  storedRefs = { [ORG_A]: REF_A, [ORG_B]: REF_B };
  currentUser = { userId: USER_ID, role: 'connector', organizationId: ORG_A };
});

function createDocument(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/documents`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

/** The options the route handed `saveDocument` — the column and the metadata claim. */
function savedOpts(): { issuerOrganizationId?: unknown; sIdentity?: { organizationUuid?: string } } {
  expect(mockSaveDocument).toHaveBeenCalledTimes(1);
  return mockSaveDocument.mock.calls[0][3] as any;
}

async function expectBindRefusal(res: Response): Promise<void> {
  expect(res.status).toBe(403);
  const body: any = await res.json();
  expect(body.error.code).toBe('FORBIDDEN');
  // Same wire message as the 2026-09-07 bind — an S-side matcher on it must not break.
  expect(body.error.message).toBe('organizationUuid differs from the acting Organisation');
  expect(mockSaveDocument).not.toHaveBeenCalled();
}

describe('KS-597 option B — organizationUuid names the acting Organisation by K id or by its own externalRef', () => {
  it('row 1: no claim is unchanged — accepted, nothing bound, and no organisation read', async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH });
    expect(res.status).toBe(201);
    expect(savedOpts().issuerOrganizationId).toBeNull();
    expect(mockGetOrganizationExternalRef).not.toHaveBeenCalled();
  });

  it("row 2: the caller's own K organizations.id is accepted and bound WITHOUT an organisation read", async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: ORG_A });
    expect(res.status).toBe(201);
    expect(savedOpts().issuerOrganizationId).toBe(ORG_A);
    expect(mockGetOrganizationExternalRef).not.toHaveBeenCalled();
  });

  // Wednesday (c): the column holds what K could bind, the metadata holds what S sent.
  it("row 3: the caller Organisation's own S externalRef is accepted — the column gets the caller's K id, the metadata keeps S's GUID", async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: REF_A });
    expect(res.status).toBe(201);
    const opts = savedOpts();
    expect(opts.issuerOrganizationId).toBe(ORG_A);
    expect(opts.sIdentity?.organizationUuid).toBe(REF_A);
  });

  it("row 3: the read is caller-scoped — once, with the CALLER's id and the REQUEST's tenant, never with the claim", async () => {
    await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: REF_A });
    expect(mockGetOrganizationExternalRef).toHaveBeenCalledTimes(1);
    const [orgId, tenantId] = mockGetOrganizationExternalRef.mock.calls[0];
    expect(orgId).toBe(ORG_A);
    expect(tenantId).toBe(TENANT);
  });

  // Wednesday (d): S's GUIDs are case-free identifiers; both sides go through the
  // shared normaliseOrgId (QA F-4), so case is never an identity difference.
  it('(d) an UPPER-case claim matches a lower-case stored externalRef', async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: REF_A.toUpperCase() });
    expect(res.status).toBe(201);
    expect(savedOpts().issuerOrganizationId).toBe(ORG_A);
  });

  it('(d) a lower-case claim matches an UPPER-case stored externalRef', async () => {
    storedRefs = { [ORG_A]: REF_A.toUpperCase() };
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: REF_A });
    expect(res.status).toBe(201);
    expect(savedOpts().issuerOrganizationId).toBe(ORG_A);
  });

  it("row 4: ANOTHER Organisation's K id is refused — same code and message, nothing written", async () => {
    await expectBindRefusal(await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: ORG_B }));
  });

  it("row 4: ANOTHER Organisation's externalRef is refused — same code and message, nothing written", async () => {
    await expectBindRefusal(await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: REF_B }));
  });

  // 403 and not 404: a 404 would tell a key which refs exist — the reason
  // register-connector's guardrail 4 answers a cross-tenant ref with a uniform code.
  it('row 5: a claim that identifies no Organisation is refused with the SAME 403, not a 404', async () => {
    const unknown = 'eeeeeeee-5555-4555-8555-555555555555';
    await expectBindRefusal(await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: unknown }));
  });

  it('row 5: a caller Organisation with no externalRef on record refuses every claim that is not its K id', async () => {
    storedRefs = { [ORG_A]: null };
    await expectBindRefusal(await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: REF_A }));
  });

  // Two orgs sharing a ref: each key binds to ITS OWN org. A resolver keyed on
  // the claim would return one row for both calls and attribute one of them wrongly.
  it('row 6: two Organisations sharing one externalRef each bind to their OWN Organisation, never the other', async () => {
    const SHARED = 'c0ffee00-6666-4666-8666-000000000066';
    storedRefs = { [ORG_A]: SHARED, [ORG_B]: SHARED };

    currentUser = { userId: USER_ID, role: 'connector', organizationId: ORG_A };
    const resA = await createDocument({ title: 'Doc A', contentHash: HASH, organizationUuid: SHARED });
    currentUser = { userId: USER_ID, role: 'connector', organizationId: ORG_B };
    const resB = await createDocument({ title: 'Doc B', contentHash: 'c'.repeat(64), organizationUuid: SHARED });

    expect(resA.status).toBe(201);
    expect(resB.status).toBe(201);
    expect(mockSaveDocument).toHaveBeenCalledTimes(2);
    expect((mockSaveDocument.mock.calls[0][3] as any).issuerOrganizationId).toBe(ORG_A);
    expect((mockSaveDocument.mock.calls[1][3] as any).issuerOrganizationId).toBe(ORG_B);
    expect(mockGetOrganizationExternalRef.mock.calls.map((c) => c[0])).toEqual([ORG_A, ORG_B]);
  });

  it.each([
    ['absent', undefined],
    ["the gateway's empty string", ''],
  ])('row 7: an org-less caller (%s) is not refused, not attributed, and reads no organisation', async (_label, org) => {
    currentUser = { userId: USER_ID, role: 'connector', ...(org === undefined ? {} : { organizationId: org }) };
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: REF_A });
    expect(res.status).toBe(201);
    expect(savedOpts().issuerOrganizationId).toBeNull();
    expect(mockGetOrganizationExternalRef).not.toHaveBeenCalled();
  });

  it('row 8: a malformed claim is 400 before any organisation read', async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: 'not-a-uuid' });
    expect(res.status).toBe(400);
    expect(mockGetOrganizationExternalRef).not.toHaveBeenCalled();
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  // Wednesday (b): a failed read must never become a 201 — and must not be
  // disguised as the bind's 403 either, which would tell S its org is wrong.
  it('row 9: when the caller-organisation read THROWS the request fails with 500 and nothing is written', async () => {
    mockGetOrganizationExternalRef.mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: REF_A });
    expect(res.status).toBe(500);
    const body: any = await res.json();
    expect(body.error.code).toBe('INTERNAL_ERROR');
    expect(mockGetOrganizationExternalRef).toHaveBeenCalledTimes(1);
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  // Stuart's cost #1 (KS-597, 2026-09-10 07:43Z): S signs with the document
  // OWNER's key but may name the ISSUER's organisation. B compares against the
  // caller, so that divergence stays refused — exactly as it was under the raw bind.
  it("row 10: the ISSUER's externalRef on the OWNER's key is refused under B, as it was before", async () => {
    await expectBindRefusal(await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: REF_B }));
    expect(mockGetOrganizationExternalRef.mock.calls.map((c) => c[0])).toEqual([ORG_A]);
  });
});
