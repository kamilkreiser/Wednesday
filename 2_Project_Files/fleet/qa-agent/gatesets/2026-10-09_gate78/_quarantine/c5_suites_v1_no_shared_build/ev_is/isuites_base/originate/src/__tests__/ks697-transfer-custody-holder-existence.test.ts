/**
 * KS-697 — POST /api/documents/:id/transfer-custody accepted a NON-EXISTENT
 * `newHolderId`, returned 201 and minted an anchor, while `newHolderEmail` for
 * the same operation correctly answered 404 RECIPIENT_NOT_FOUND.
 *
 * Root cause (one, not two): the id path assigned `resolvedHolderId = newHolderId`
 * and never looked the holder up. `custody_events.to_holder_id` carries no foreign
 * key — only `document_id` does — so any well-formed uuid inserted, and a non-uuid
 * threw Postgres 22P02 at the `::uuid` cast, was swallowed by the handler's outer
 * catch, and surfaced as a raw 500. Both symptoms are that one missing lookup.
 *
 * What this pins:
 *   - unknown holder uuid  -> 404 RECIPIENT_NOT_FOUND, and NO custody row, and
 *     critically NO ANCHOR. The anchor is the part that cannot be un-minted.
 *   - non-uuid holder      -> 400 VALIDATION_ERROR (was 500)
 *   - EXISTING holder      -> 201. This is the positive control and it is the
 *     assertion that actually earns the others: without it, a fix that 404s
 *     everything would pass every other test in this file.
 *   - email path unknown   -> still 404 (unchanged; it was already correct)
 *
 * The existence check runs on the request's db handle, which since KS-458 carries
 * the RLS tenant GUC. `users` is FORCE RLS fail-closed, so a holder in another
 * tenant is invisible to the query and falls out as the same 404 — matching auth's
 * deliberate /lookup stance where "no such user" and "in another tenant" are made
 * indistinguishable. Tenant behaviour is asserted below via the db mock.
 */

// routes/documents imports services/provenance -> db -> config, which demands
// DATABASE_URL at module load (see ks466/ks480). Without it this suite fails to
// RUN, which reads as green in the suite count rather than as a failure.
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
process.env.SIMULATE_ANCHORING = 'true';

const TENANT_ID = '3fa85f64-5717-4562-b3fc-2c963f66afa6';
const REAL_HOLDER_ID = '7c9e6679-7425-40de-944b-e07fc1f90ae7';
const UNKNOWN_HOLDER_ID = '11111111-2222-4333-8444-555555555555';
const OTHER_TENANT_HOLDER_ID = '99999999-8888-4777-8666-555555555555';
const DOC_ID = 'doc-0000000000000-5eeded0c';

const mockGetDocument = jest.fn();
const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn(async (..._args: any[]) => 1);
jest.mock('../repositories/documentRepo', () => ({
  getDocument: mockGetDocument,
  listDocuments: jest.fn(),
  saveDocument: jest.fn(async () => ({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true })),
  updateDocument: jest.fn(async () => undefined),
  getSigningRequest: jest.fn(),
  saveSigningRequest: jest.fn(),
  deleteSigningRequest: jest.fn(),
  generateContentHash: jest.fn(() => 'a'.repeat(64)),
  seedDemoDocuments: jest.fn(async () => undefined),
  assertNoCycle: jest.fn(async () => undefined),
}));

jest.mock('../db', () => {
  const client = {
    $queryRaw: (...args: any[]) => mockQueryRaw(...args),
    $executeRaw: (...args: any[]) => mockExecuteRaw(...args),
    $queryRawUnsafe: jest.fn(),
    $executeRawUnsafe: jest.fn(),
  };
  // KS-1263: /share and /transfer-custody run their writes inside withTenant(). The callback gets
  // the SAME client this suite already observes, so the existing assertions still see them. A mock
  // cannot roll back; the behavioural rollback cell is OWED at the tier-1 gate (real Postgres).
  return { prisma: client, withTenant: async (_t: string, fn: (tx: unknown) => Promise<unknown>) => fn(client) };
});

jest.mock('../repositories/shareRepo', () => ({ createShare: jest.fn() }));
jest.mock('../repositories/lifecycleEventRepo', () => ({
  createLifecycleEvent: jest.fn(),
  setLifecycleEventAnchor: jest.fn(),
  listLifecycleEvents: jest.fn(),
}));
jest.mock('../events', () => ({
  publishEvent: jest.fn(async () => undefined),
  EventTypes: { DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred' },
}));
jest.mock('../services/threadTokenClient', () => ({ mintAndRegisterThreadToken: jest.fn(async () => ({})) }));
jest.mock('../routes/verification', () => ({ registerInPlatformRegistry: jest.fn(async () => undefined) }));
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee', role: 'SYSTEM_ADMIN', tenantId: TENANT_ID };
    next();
  },
}));
jest.mock('../middleware/rbac', () => ({ isAllowedByRoleOrScope: () => true }));
jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import express from 'express';
import { documentsRouter, publicDocumentsRouter } from '../routes/documents';

const app = express();
app.use((req: any, _res, next) => {
  req.user = { userId: 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee', role: 'SYSTEM_ADMIN', tenantId: TENANT_ID };
  req.tenantId = TENANT_ID;
  next();
});
app.use('/api/documents', express.json(), publicDocumentsRouter);
app.use('/api/documents', express.json(), documentsRouter);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;

/**
 * `emitLifecycleAnchor` is module-local to routes/documents, so there is no
 * jest.mock seam for it. Its real seam is the outbound POST to the anchoring
 * service — which is the better thing to assert anyway: it proves no anchor
 * request ever left this process, rather than that a mock went uncalled.
 */
const realFetch = global.fetch;
let anchorCalls: string[] = [];
let lookupStatus = 404;

function installFetchSpy() {
  anchorCalls = [];
  lookupStatus = 404;
  global.fetch = (async (url: any, init?: any) => {
    const u = String(url);
    if (u.includes('/api/anchors')) {
      anchorCalls.push(u);
      return { ok: true, status: 201, json: async () => ({ data: { id: 'anchor_x', txHash: null, status: 'submitted' } }) } as any;
    }
    if (u.includes('/api/users/lookup')) {
      return { ok: lookupStatus === 200, status: lookupStatus, json: async () => ({ data: { userId: REAL_HOLDER_ID } }) } as any;
    }
    return realFetch(url, init);
  }) as any;
}

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});
afterAll(() => {
  global.fetch = realFetch;
  server?.close();
});

/**
 * The db mock stands in for the tenant-scoped `users` read and the custody INSERT.
 * `knownHolders` is the set the "database" contains for this tenant — anything not
 * in it comes back empty, which is exactly what FORCE RLS does to a cross-tenant
 * row on the real database.
 */
function primeDb(knownHolders: string[]) {
  mockQueryRaw.mockReset();
  mockQueryRaw.mockImplementation(async (strings: TemplateStringsArray, ...values: any[]) => {
    const sql = Array.isArray(strings) ? strings.join('?') : String(strings);
    if (/FROM\s+users/i.test(sql)) {
      const wanted = String(values[0]);
      return knownHolders.includes(wanted) ? [{ ok: 1 }] : [];
    }
    if (/INSERT\s+INTO\s+custody_events/i.test(sql)) {
      return [{ id: 'ce111111-2222-4333-8444-555555555555' }];
    }
    return [];
  });
}

function custodyInsertCount(): number {
  return mockQueryRaw.mock.calls.filter((c: any[]) => {
    const s = Array.isArray(c[0]) ? c[0].join('?') : String(c[0]);
    return /INSERT\s+INTO\s+custody_events/i.test(s);
  }).length;
}

beforeEach(() => {
  jest.clearAllMocks();
  installFetchSpy();
  mockGetDocument.mockResolvedValue({
    id: DOC_ID,
    contentHash: 'a'.repeat(64),
    owner: { id: '12121212-3434-4545-8656-767676767676' },
  });
  primeDb([REAL_HOLDER_ID]);
});

async function transfer(body: unknown) {
  const res = await fetch(`${baseUrl}/api/documents/${DOC_ID}/transfer-custody`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: 'Bearer test-token' },
    body: JSON.stringify(body),
  });
  return { status: res.status, payload: (await res.json()) as any };
}

describe('KS-697 — a non-existent newHolderId must not become custody', () => {
  it("the ticket's first invented uuid is a 404, not a 201", async () => {
    const { status, payload } = await transfer({ newHolderId: UNKNOWN_HOLDER_ID });
    expect(status).toBe(404);
    expect(payload.success).toBe(false);
    expect(payload.error?.code).toBe('RECIPIENT_NOT_FOUND');
  });

  it('writes NO custody row and — the part that cannot be undone — mints NO anchor', async () => {
    await transfer({ newHolderId: UNKNOWN_HOLDER_ID });
    expect(custodyInsertCount()).toBe(0);
    expect(anchorCalls).toHaveLength(0);
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  it("the ticket's SECOND invented uuid behaves the same — it was never a one-off", async () => {
    const { status } = await transfer({ newHolderId: OTHER_TENANT_HOLDER_ID });
    expect(status).toBe(404);
    expect(custodyInsertCount()).toBe(0);
  });

  it('a holder the tenant cannot see (other tenant, hidden by RLS) is the same 404, never a 403', async () => {
    // The negative response must not distinguish "no such user" from "exists
    // elsewhere" — that distinction is itself cross-tenant disclosure, and auth's
    // /lookup deliberately refuses to make it.
    primeDb([REAL_HOLDER_ID]); // OTHER_TENANT_HOLDER_ID invisible, as RLS would render it
    const { status, payload } = await transfer({ newHolderId: OTHER_TENANT_HOLDER_ID });
    expect(status).toBe(404);
    expect(payload.error?.code).toBe('RECIPIENT_NOT_FOUND');
    expect(status).not.toBe(403);
  });
});

describe('KS-697 — a malformed newHolderId is the caller\'s fault, not a server error', () => {
  it.each([
    ['not-a-uuid', 'a bare string'],
    ['', 'empty string'],
    ['11111111-2222-4333-8444-55555555555', 'one char short of a uuid'],
  ])('%s (%s) -> 400 VALIDATION_ERROR, never 500', async (bad: string, _label: string) => {
    const { status, payload } = await transfer({ newHolderId: bad });
    expect(status).toBe(400);
    expect(payload.error?.code).toBe('VALIDATION_ERROR');
    expect(custodyInsertCount()).toBe(0);
  });

  it.each([
    [123, 'a number'],
    [[], 'an array'],
    [{}, 'an object'],
  ])('a non-string %s (%s) -> 400, never 500', async (bad: unknown, _label: string) => {
    const { status } = await transfer({ newHolderId: bad });
    expect(status).toBe(400);
    expect(custodyInsertCount()).toBe(0);
  });

  it('never reaches the ::uuid cast — no DB work happens at all on a malformed id', async () => {
    await transfer({ newHolderId: 'not-a-uuid' });
    expect(mockGetDocument).not.toHaveBeenCalled();
    expect(mockQueryRaw).not.toHaveBeenCalled();
  });
});

// =============================================================================
// THE POSITIVE CONTROL
// =============================================================================
// Everything above passes trivially if the fix simply refuses every transfer.
// This block is what makes the suite discriminating rather than merely green.
describe('KS-697 — the positive control: a REAL holder still transfers', () => {
  it('an existing same-tenant holder is 201, writes the custody row and mints the anchor', async () => {
    const { status, payload } = await transfer({ newHolderId: REAL_HOLDER_ID });
    expect(status).toBe(201);
    expect(payload.transfer?.toHolderId).toBe(REAL_HOLDER_ID);
    expect(custodyInsertCount()).toBe(1);
    expect(anchorCalls).toHaveLength(1);
  });

  it('the existence check is tenant-scoped in the SQL, not only by RLS', async () => {
    await transfer({ newHolderId: REAL_HOLDER_ID });
    const userQuery = mockQueryRaw.mock.calls.find((c: any[]) => {
      const s = Array.isArray(c[0]) ? c[0].join('?') : String(c[0]);
      return /FROM\s+users/i.test(s);
    });
    expect(userQuery).toBeDefined();
    const sql = (userQuery![0] as TemplateStringsArray).join('?');
    expect(sql).toMatch(/tenant_id/i);
    expect(userQuery!.slice(1)).toContain(TENANT_ID);
  });

  it('the document owner is flipped to the new holder', async () => {
    await transfer({ newHolderId: REAL_HOLDER_ID });
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });
});

describe('KS-697 — the email path, which was already correct, is unchanged', () => {
  it('an unknown email is still 404 RECIPIENT_NOT_FOUND', async () => {
    lookupStatus = 404;
    const { status, payload } = await transfer({ newHolderEmail: 'nobody-xyz@example.invalid' });
    expect(status).toBe(404);
    expect(payload.error?.code).toBe('RECIPIENT_NOT_FOUND');
    expect(custodyInsertCount()).toBe(0);
  });

  it('supplying neither id nor email is still a 400', async () => {
    const { status, payload } = await transfer({});
    expect(status).toBe(400);
    expect(payload.error?.code).toBe('VALIDATION_ERROR');
  });

  it('supplying both is still a 400', async () => {
    const { status } = await transfer({ newHolderId: REAL_HOLDER_ID, newHolderEmail: 'a@b.com' });
    expect(status).toBe(400);
  });
});
