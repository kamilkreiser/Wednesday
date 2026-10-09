/**
 * KS-739 — POST /api/documents/:id/transfer-custody mapped a 401/403 from
 * `GET /api/users/lookup` to 502 BAD_GATEWAY.
 *
 * KS-536 wrote the rule and implemented two codes of it. Its comment says:
 *
 *   "A 4xx from the lookup is the caller's fault and must surface as 400; only
 *    a genuine upstream failure (5xx / unreachable) is a 502."
 *
 * — a statement about the whole 4xx class. The code enumerated 404, then
 * 400/422, then sent EVERYTHING else to 502. So 401 and 403 (and 405, 409, 410,
 * 429) became "upstream gateway failure". Platform S saw exactly that on
 * PS-681: a refusal of its own connector credential, presented as K being down.
 * A 5xx is not something a caller can branch on, so `PostLifecycleAsync`
 * degraded to flat `/api/anchors` and `waitForLifecycleEvent` burned its 90 s.
 *
 * The lookup is called with the CALLER'S `Authorization` header, so a 401/403
 * from it IS the caller's own credential failing — which is what makes
 * surfacing it as a 4xx honest rather than blame-shifting.
 *
 * What this pins:
 *   - 401 and 403 pass through with their own status and a message naming the
 *     missing credential/scope — the two codes the ticket was filed for.
 *   - 409, 410, 429 pass through too. These are the cells that prove the fix is
 *     a CLASS rule and not four enumerated codes; enumerating 401/403 would
 *     leave these at 502 and re-create this ticket on the next code auth grows.
 *   - 404 and 400/422 keep their existing specific answers. Regression guards:
 *     the class branch sits BELOW them and must not swallow them.
 *   - 500/502/503 STILL yield 502 BAD_GATEWAY. This is the positive control the
 *     ticket demands: without it, a fix that passed every status through would
 *     pass every other cell in this file while destroying the gateway branch.
 *   - a resolvable email still transfers (201). Without this control, a fix that
 *     refused everything would look green.
 *   - no refusal path mints an anchor or writes a custody row.
 */

// routes/documents imports services/provenance -> db -> config, which demands
// DATABASE_URL at module load (see ks466/ks480/ks697). Without it this suite
// fails to RUN, which reads as green in the suite count rather than as a failure.
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
process.env.SIMULATE_ANCHORING = 'true';

const TENANT_ID = '3fa85f64-5717-4562-b3fc-2c963f66afa6';
const REAL_HOLDER_ID = '7c9e6679-7425-40de-944b-e07fc1f90ae7';
const DOC_ID = 'doc-0000000000000-5eeded0c';
const RECIPIENT_EMAIL = 'recipient@example.com';

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

const realFetch = global.fetch;
let anchorCalls: string[] = [];
let lookupStatus = 200;
let lookupBody: unknown = { data: { userId: REAL_HOLDER_ID } };

/**
 * The outbound POST to anchoring is the real seam for `emitLifecycleAnchor`
 * (module-local, no jest.mock seam). Asserting on it proves no anchor request
 * ever left this process, which is stronger than a mock going uncalled.
 */
function installFetchSpy() {
  anchorCalls = [];
  global.fetch = (async (url: any, init?: any) => {
    const u = String(url);
    if (u.includes('/api/anchors')) {
      anchorCalls.push(u);
      return { ok: true, status: 201, json: async () => ({ data: { id: 'anchor_x', txHash: null, status: 'submitted' } }) } as any;
    }
    if (u.includes('/api/users/lookup')) {
      return {
        ok: lookupStatus >= 200 && lookupStatus < 300,
        status: lookupStatus,
        json: async () => lookupBody,
      } as any;
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
  lookupStatus = 200;
  lookupBody = { data: { userId: REAL_HOLDER_ID } };
  installFetchSpy();
  mockGetDocument.mockResolvedValue({
    id: DOC_ID,
    contentHash: 'a'.repeat(64),
    owner: { id: '12121212-3434-4545-8656-767676767676' },
  });
  primeDb([REAL_HOLDER_ID]);
});

async function transferByEmail() {
  const res = await fetch(`${baseUrl}/api/documents/${DOC_ID}/transfer-custody`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: 'Bearer test-token' },
    body: JSON.stringify({ newHolderEmail: RECIPIENT_EMAIL }),
  });
  return { status: res.status, payload: (await res.json()) as any };
}

describe('KS-739 — an auth refusal from users/lookup is the caller\'s fault, not a 502', () => {
  it('401 surfaces as 401, never 502, and the message says to re-authenticate', async () => {
    lookupStatus = 401;
    lookupBody = { success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } };
    const { status, payload } = await transferByEmail();
    expect(status).toBe(401);
    expect(status).not.toBe(502);
    expect(payload.success).toBe(false);
    expect(payload.error?.code).toBe('UNAUTHORIZED');
    expect(payload.error?.message).toMatch(/re-authenticate/i);
  });

  it('403 surfaces as 403, never 502, and the message NAMES the missing scope', async () => {
    // The whole cost of this defect was diagnosis time: "Could not resolve
    // recipient email via users/lookup" told Platform S nothing it could act on.
    lookupStatus = 403;
    lookupBody = { success: false, error: { code: 'FORBIDDEN', message: 'users:read scope or an allowed role is required' } };
    const { status, payload } = await transferByEmail();
    expect(status).toBe(403);
    expect(status).not.toBe(502);
    expect(payload.error?.code).toBe('FORBIDDEN');
    expect(payload.error?.message).toContain('users:read');
  });

  it('the upstream message is carried through, not replaced', async () => {
    lookupStatus = 403;
    lookupBody = { success: false, error: { code: 'FORBIDDEN', message: 'users:read scope or an allowed role is required' } };
    const { payload } = await transferByEmail();
    expect(payload.error?.message).toContain('Upstream said: users:read scope or an allowed role is required');
  });

  it('a 4xx with no parseable body still answers that 4xx, with a typed fallback code', async () => {
    lookupStatus = 403;
    lookupBody = null;
    const { status, payload } = await transferByEmail();
    expect(status).toBe(403);
    expect(payload.error?.code).toBe('RECIPIENT_LOOKUP_FAILED');
    expect(payload.error?.message).toMatch(/users:read/);
  });

  it.each([[409], [410], [429]])(
    '%i passes through too — the fix is the 4xx CLASS, not four enumerated codes',
    async (code: number) => {
      // These are the cells that fail if someone "fixes" this by adding
      // `|| status === 401 || status === 403` to the enumeration.
      lookupStatus = code;
      lookupBody = { success: false, error: { code: 'UPSTREAM', message: `upstream said ${code}` } };
      const { status, payload } = await transferByEmail();
      expect(status).toBe(code);
      expect(status).not.toBe(502);
      expect(payload.error?.message).toContain(`upstream said ${code}`);
    },
  );

  it('KS-739 F1: a 403 whose body is not JSON (json() rejects) still answers 403 RECIPIENT_LOOKUP_FAILED, never 502', async () => {
    global.fetch = (async (url: any, init?: any) => {
      const u = String(url);
      if (u.includes('/api/users/lookup')) {
        return { ok: false, status: 403, json: async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); } } as any;
      }
      return realFetch(url, init);
    }) as any;
    const { status, payload } = await transferByEmail();
    expect([status, payload.error?.code]).toEqual([403, 'RECIPIENT_LOOKUP_FAILED']);
    expect(payload.error?.message).toMatch(/users:read/);
  });
  it('RED KS-739 N66-1: a 401 and a 429 whose body is not JSON (json() rejects) still answer that 4xx RECIPIENT_LOOKUP_FAILED, never 502', async () => {
    const notJson = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 401, json: notJson } as any) : realFetch(url, init))) as any;
    const a = await transferByEmail();
    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 429, json: notJson } as any) : realFetch(url, init))) as any;
    const b = await transferByEmail();
    expect([a.status, a.payload.error?.code, b.status, b.payload.error?.code]).toEqual([401, 'RECIPIENT_LOOKUP_FAILED', 429, 'RECIPIENT_LOOKUP_FAILED']);
  });
  it('RED KS-739 N75-1: a 404 whose body is not JSON (json() rejects) is still the typed RECIPIENT_NOT_FOUND, never 502', async () => {
    const notJson404 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 404, json: notJson404 } as any) : realFetch(url, init))) as any;
    const r404 = await transferByEmail();
    expect([r404.status, r404.payload.error?.code]).toEqual([404, 'RECIPIENT_NOT_FOUND']);
  });
  it('RED KS-739 N75-1: a 500 whose body is not JSON (json() rejects) is still 502 BAD_GATEWAY from the upstream branch, not the catch', async () => {
    const notJson500 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 500, json: notJson500 } as any) : realFetch(url, init))) as any;
    const r500 = await transferByEmail();
    expect([r500.status, r500.payload.error?.code, r500.payload.error?.message]).toEqual([502, 'BAD_GATEWAY', 'Could not resolve recipient email via users/lookup']);
  });
  it('RED KS-739 N82-1: a 400 whose body is not JSON (json() rejects) is still 400 VALIDATION_ERROR, never 502', async () => {
    const notJson400 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 400, json: notJson400 } as any) : realFetch(url, init))) as any;
    const r400 = await transferByEmail();
    expect([r400.status, r400.payload.error?.code]).toEqual([400, 'VALIDATION_ERROR']);
  });
  it('RED KS-739 N82-1: a 503 whose body is not JSON (json() rejects) is still 502 BAD_GATEWAY from the upstream branch, not the catch', async () => {
    const notJson503 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 503, json: notJson503 } as any) : realFetch(url, init))) as any;
    const r503 = await transferByEmail();
    expect([r503.status, r503.payload.error?.code, r503.payload.error?.message]).toEqual([502, 'BAD_GATEWAY', 'Could not resolve recipient email via users/lookup']);
  });
  it('RED KS-739 N89-1: a 422 whose body is not JSON (json() rejects) is still 400 VALIDATION_ERROR, never 502', async () => {
    const notJson422 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 422, json: notJson422 } as any) : realFetch(url, init))) as any;
    const r422 = await transferByEmail();
    expect([r422.status, r422.payload.error?.code]).toEqual([400, 'VALIDATION_ERROR']);
  });
  it('RED KS-739 N89-1: a 502 whose body is not JSON (json() rejects) is still 502 BAD_GATEWAY from the upstream branch, not the catch', async () => {
    const notJson502 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 502, json: notJson502 } as any) : realFetch(url, init))) as any;
    const r502 = await transferByEmail();
    expect([r502.status, r502.payload.error?.code, r502.payload.error?.message]).toEqual([502, 'BAD_GATEWAY', 'Could not resolve recipient email via users/lookup']);
  });
  it('RED KS-739 N89-1: a 504 whose body is not JSON (json() rejects) is still 502 BAD_GATEWAY from the upstream branch, not the catch', async () => {
    const notJson504 = async () => { throw new SyntaxError('Unexpected token < in JSON at position 0'); };
    global.fetch = (async (url: any, init?: any) => (String(url).includes('/api/users/lookup') ? ({ ok: false, status: 504, json: notJson504 } as any) : realFetch(url, init))) as any;
    const r504 = await transferByEmail();
    expect([r504.status, r504.payload.error?.code, r504.payload.error?.message]).toEqual([502, 'BAD_GATEWAY', 'Could not resolve recipient email via users/lookup']);
  });
  it('no anchor is minted and no custody row is written on a 403', async () => {
    lookupStatus = 403;
    lookupBody = { success: false, error: { code: 'FORBIDDEN', message: 'nope' } };
    await transferByEmail();
    expect(anchorCalls).toHaveLength(0);
    expect(custodyInsertCount()).toBe(0);
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });
});

describe('KS-739 — the answers that must NOT change', () => {
  it('404 is still the typed RECIPIENT_NOT_FOUND with its invite path (KS-74)', async () => {
    lookupStatus = 404;
    lookupBody = { success: false, error: { code: 'USER_NOT_FOUND', message: 'no such user' } };
    const { status, payload } = await transferByEmail();
    expect(status).toBe(404);
    expect(payload.error?.code).toBe('RECIPIENT_NOT_FOUND');
    expect(payload.error?.message).toContain('KS-74');
  });

  it.each([[400], [422]])('%i is still flattened to 400 VALIDATION_ERROR about the email (KS-536)', async (code: number) => {
    lookupStatus = code;
    lookupBody = { success: false, error: { code: 'BAD_REQUEST', message: 'malformed' } };
    const { status, payload } = await transferByEmail();
    expect(status).toBe(400);
    expect(payload.error?.code).toBe('VALIDATION_ERROR');
    expect(payload.error?.message).toContain('newHolderEmail');
  });
});

describe('KS-739 — POSITIVE CONTROL: the gateway branch must survive', () => {
  it.each([[500], [502], [503]])(
    '%i is a GENUINE upstream failure and must still be 502 BAD_GATEWAY',
    async (code: number) => {
      // Without this, a fix that passed every status straight through would pass
      // every other cell in this file while deleting the reason 502 exists.
      lookupStatus = code;
      lookupBody = { success: false, error: { code: 'INTERNAL_ERROR', message: 'boom' } };
      const { status, payload } = await transferByEmail();
      expect(status).toBe(502);
      expect(payload.error?.code).toBe('BAD_GATEWAY');
      expect(payload.error?.message).toContain('users/lookup');
    },
  );

  it('an UNREACHABLE auth service is still 502, from the catch, with its own message', async () => {
    global.fetch = (async (url: any, init?: any) => {
      const u = String(url);
      if (u.includes('/api/users/lookup')) throw new Error('ECONNREFUSED');
      if (u.includes('/api/anchors')) { anchorCalls.push(u); return { ok: true, status: 201, json: async () => ({ data: {} }) } as any; }
      return realFetch(url, init);
    }) as any;
    const { status, payload } = await transferByEmail();
    expect(status).toBe(502);
    expect(payload.error?.message).toContain('Recipient lookup service unavailable');
  });
});

describe('KS-739 — POSITIVE CONTROL: a resolvable recipient still transfers', () => {
  it('200 from the lookup still completes the transfer', async () => {
    // Without this, a fix that refused every status would look green above.
    lookupStatus = 200;
    lookupBody = { data: { userId: REAL_HOLDER_ID } };
    const { status } = await transferByEmail();
    expect([200, 201]).toContain(status);
    expect(custodyInsertCount()).toBe(1);
  });
});
