/**
 * =============================================================================
 * KS-597 — the issuing organisation is BOUND to the acting Organisation
 * =============================================================================
 * Kam's ruling, 2026-09-07: "Bind the issuer to the actor — 403 on a mismatch,
 * exactly as `onBehalfOf` already does."
 *
 * `organizationUuid` is attribution the CALLER supplies. Before this, a
 * mismatched claim folded to NULL inside the repository and the request still
 * succeeded; a claim for another org in the same tenant was written and
 * attributed. It is now refused at the route.
 *
 * "Exactly as onBehalfOf already does" is load-bearing and is what the case
 * split below mirrors — `resolveOnBehalfOf` (services/provenance.ts:101-145):
 *   - both orgs present and different            -> 403        (:131)
 *   - caller has NO Organisation                 -> no 403, no attribution (:109)
 *   - both sides normalised through normaliseOrgId, one shared implementation,
 *     so a case-only difference is NOT a different org (:128-129, QA F-4)
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
  // KS-597 option B: a claim that is not the caller's K id is checked against the
  // caller Organisation's own externalRef. These cells carry none, so every
  // mismatched claim still refuses; option B's own cells live in
  // ks597-b-caller-scoped-externalref.test.ts.
  getOrganizationExternalRef: jest.fn(async () => null),
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

// The acting principal is what this suite varies, so the mock reads a mutable
// value rather than pinning one. `organizationId` is OPTIONAL on the JWT
// payload (middleware/auth.ts:19) and the gateway maps a missing connector org
// to '' (api-gateway middleware/auth.ts:232) — both absent shapes are exercised.
let currentUser: Record<string, unknown> = {};
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = currentUser;
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
const ORG_A = 'aaaaaaaa-0000-4000-8000-00000000000a';
const ORG_B = 'bbbbbbbb-0000-4000-8000-00000000000b';
const HASH = 'b'.repeat(64);

beforeEach(() => {
  jest.clearAllMocks();
  mockSaveDocument.mockImplementation(async (..._args: any[]) => ({ dbId: DB_ID, inserted: true }));
  mockGetDocument.mockResolvedValue(null);
  currentUser = { userId: USER_ID, role: 'ISSUER_ADMIN', organizationId: ORG_A };
});

function createDocument(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/documents`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

/** The `issuerOrganizationId` opt the route handed the repository. */
function savedIssuerOrg(): unknown {
  expect(mockSaveDocument).toHaveBeenCalled();
  const opts = mockSaveDocument.mock.calls[0][3] as any;
  return opts?.issuerOrganizationId;
}

describe('KS-597 — a mismatched organizationUuid is refused, not folded to NULL', () => {
  it('403s when the claimed organizationUuid belongs to a DIFFERENT Organisation', async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: ORG_B });
    expect(res.status).toBe(403);
    const body: any = await res.json();
    expect(body.error.code).toBe('FORBIDDEN');
    // KS-978 F-2: the message said "belongs to a different Organisation", which is
    // NARROWER than the predicate. The test is `claimedOrgId !== callerOrgId` --
    // inequality, not membership -- so a well-formed UUID belonging to NO
    // Organisation is refused identically. The wire now says what it does.
    expect(body.error.message).toMatch(/differs from the acting Organisation/);
  });

  it('refuses BEFORE the write — a rejected registration must not reach the repository', async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: ORG_B });
    expect(res.status).toBe(403);
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });

  it('binds the claim when it matches the acting Organisation', async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: ORG_A });
    expect(res.status).toBeLessThan(400);
    expect(savedIssuerOrg()).toBe(ORG_A);
  });

  // provenance.ts:128-129 / QA F-4: both sides go through `normaliseOrgId`, so a
  // case-only difference is the SAME org. A raw string compare here would 403 a
  // caller acting inside its own Organisation — the exact defect the sibling
  // resolver was repaired for, and the reason this uses the shared normaliser
  // rather than a private copy.
  it('does NOT 403 on a case-only difference — the shared normaliser decides', async () => {
    currentUser = { userId: USER_ID, role: 'ISSUER_ADMIN', organizationId: ORG_A.toUpperCase() };
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: ORG_A });
    expect(res.status).toBeLessThan(400);
    expect(savedIssuerOrg()).toBe(ORG_A);
  });

  // provenance.ts:109 gives the reason: an org-less caller "has no Organisation
  // to validate against", so resolving "would attribute to ANY matching tenant
  // user" (the "not in a *different* org" phrasing belongs to :136, the org-less
  // SUBJECT, not the org-less caller). So the org-less caller is
  // not refused — but nothing can be bound to it either, so the claim is not
  // attributed. Reachable: migration 018 drops NOT NULL on
  // svc_api_keys.organization_id outright; the originate admin endpoint issuing
  // org-less keys is the migration's stated reason, not a per-key condition.
  it('does NOT 403 an org-less caller, and does NOT attribute its claim either', async () => {
    currentUser = { userId: USER_ID, role: 'ISSUER_ADMIN' };
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: ORG_B });
    expect(res.status).toBeLessThan(400);
    expect(savedIssuerOrg()).toBeNull();
  });

  it("treats the gateway's empty-string org exactly as an absent one", async () => {
    currentUser = { userId: USER_ID, role: 'ISSUER_ADMIN', organizationId: '' };
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: ORG_B });
    expect(res.status).toBeLessThan(400);
    expect(savedIssuerOrg()).toBeNull();
  });

  it('leaves a registration with NO organizationUuid untouched — this adds a refusal, not a requirement', async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH });
    expect(res.status).toBeLessThan(400);
    expect(savedIssuerOrg()).toBeNull();
  });

  it('still 400s a malformed organizationUuid before the org comparison is reached', async () => {
    const res = await createDocument({ title: 'Doc', contentHash: HASH, organizationUuid: 'not-a-uuid' });
    expect(res.status).toBe(400);
    expect(mockSaveDocument).not.toHaveBeenCalled();
  });
});
