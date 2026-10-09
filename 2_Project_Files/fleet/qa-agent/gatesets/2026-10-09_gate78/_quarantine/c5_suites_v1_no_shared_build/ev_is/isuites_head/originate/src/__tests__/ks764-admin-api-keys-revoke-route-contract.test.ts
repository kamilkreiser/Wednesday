/**
 * =============================================================================
 * KS-764 — DELETE /api/admin/api-keys/:id, the SECOND revoke surface, on the wire
 * =============================================================================
 * PETER'S MAJOR 2 (#799 review, 2026-09-03), in his words: *"The originate route
 * has no test of any kind. The new pre-flight SELECT (adminConfig.ts:1002), the
 * 403 branch, and — importantly — a permitted revoke still returning
 * `success: true` through the added SELECT are covered only by a regex over
 * source text. The source guard proves the field is passed; it can't prove a 403
 * reaches the client or that the happy path survived."*
 *
 * ONE CORRECTION TO THE FINDING, and it does not weaken it. His sweep said
 * *"nothing in `services/originate/src/__tests__/` references api-keys"*. One
 * file does — `rightsHolders.tenant-scope.integration.test.ts:125` mounts the
 * real `adminConfigRouter`. It is excluded from the default run by
 * `jest.config.js:8` (`\.integration\.test\.ts$`), it is about rights-holder
 * tenant scoping, and it asserts nothing about revoke authorisation. So the
 * substance is exactly right — this route's authorisation has no unit coverage —
 * and the literal claim is off by one file that jest does not execute.
 *
 * WHAT IS REAL HERE AND WHAT IS NOT — the mock surface is the risk on this file,
 * so it is declared rather than left to be discovered:
 *   - REAL: `adminConfigRouter` itself, its `express.json()` pipeline, the
 *     pre-flight SELECT, `decideKeyRevoke` from `@secuura/shared`, and
 *     `requireRole` — pulled through `jest.requireActual`, so the role gate that
 *     admits ORG_ADMIN is the product's own and not a stand-in.
 *   - STUBBED: `authenticate()` only, because the real one verifies an RS256
 *     token against a public key or the auth service. The stub sets the
 *     principal under BOTH `_secuuraUser` and `user`, which is precisely what
 *     the real `setUser` (middleware/auth.ts:69) does — `requireRole` reads the
 *     first, the route reads the second, and a stub setting one would silently
 *     disable half the chain.
 *   - STUBBED, and declared because it is NOT what `authenticate()` does: the
 *     stub also sets `req.tenantId` from the principal's `tenantId`. The real
 *     `authenticate()` never touches `req.tenantId`; in production it is set by
 *     `extractTenantContext` (@secuura/shared, from the gateway-resolved
 *     `x-tenant-id` header). So a principal with NO `tenantId` leaves
 *     `req.tenantId` unset here and the route falls back to its default-tenant
 *     literal — the row still resolves, and the policy refuses the CALLER for
 *     having no tenant of its own. That is the shape the no-tenant case below
 *     exercises.
 *   - STUBBED: the database. `$queryRaw` returns the key row under test and
 *     `$executeRaw` records the UPDATE, so the happy path's write is observable
 *     rather than assumed.
 *   - OBSERVED, not replaced: `logger.warn` is spied and calls through. The
 *     route's 403 body is generic by KS-764's own design (four causes, one
 *     message), so the refusal's ARM is visible only in the log's `reason` —
 *     the spy is how the no-tenant case names the arm it is pinning.
 *
 * THE CONTROL THAT MATTERS MOST is `decideKeyRevoke` NOT being a mock. Mocking
 * `@secuura/shared` wholesale is the obvious way to write this file and it would
 * replace the subject with a stub, leaving a green suite that tests nothing.
 * `jest.isMockFunction` is asserted on it directly, below.
 *
 * SAME TENANT THROUGHOUT — the defect is a sibling ORGANISATION inside one
 * tenant. ORG_ADMIN is the caller because it is the role that genuinely reaches
 * this router (`adminConfig.ts:38` admits SYSTEM_ADMIN + ORG_ADMIN) and is
 * org-bounded, which is the combination Peter re-derived as reachable.
 * =============================================================================
 */

process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw },
  refreshTenantConfigs: jest.fn(),
  withTenant: (_t: unknown, fn: () => unknown) => fn(),
  getTenantManager: () => null,
}));

// Only `authenticate` is replaced. `requireRole` is the real implementation.
jest.mock('../middleware/auth', () => {
  const actual = jest.requireActual('../middleware/auth');
  return {
    ...actual,
    authenticate: () => (req: any, _res: unknown, next: () => void) => {
      const principal = req.headers['x-test-principal']
        ? JSON.parse(req.headers['x-test-principal'] as string)
        : undefined;
      if (principal) {
        // Mirrors middleware/auth.ts setUser() exactly — both fields, always.
        req._secuuraUser = principal;
        req.user = principal;
        if (principal.tenantId) req.tenantId = principal.tenantId;
      }
      next();
    },
  };
});

// `runWithPlatformScope` / `queryWithTenantGuc` need the DB; `decideKeyRevoke`
// is the SUBJECT and is passed through untouched.
jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    ...(jest.requireActual('@secuura/shared') as Record<string, unknown>),
    runWithPlatformScope: (fn: () => unknown) => fn(),
    queryWithTenantGuc: jest.fn(),
    decideKeyRevoke: (jest.requireActual('@secuura/shared') as Record<string, unknown>).decideKeyRevoke,
  }),
);

import express from 'express';
import * as shared from '@secuura/shared';
import { adminConfigRouter } from '../routes/adminConfig';
import { logger } from '../utils/logger';

const TENANT_A = 'a0000000-0000-4000-8000-0000000000aa';
const ORG_A = '11111111-1111-4111-8111-111111111111';
const ORG_B = '22222222-2222-4222-8222-222222222222';
const KEY_ID = '33333333-3333-4333-8333-333333333333';

/** ORG_ADMIN in organisation A — admitted by requireRole, and org-bounded. */
const ADMIN_ORG_A = { userId: 'u1', role: 'ORG_ADMIN', tenantId: TENANT_A, organizationId: ORG_A };
/** ORG_ADMIN with a tenant but NO organisation claim — Peter's case 4. */
const ADMIN_NO_ORG = { userId: 'u2', role: 'ORG_ADMIN', tenantId: TENANT_A };
/** Platform role: requireRole normalises super_admin -> SYSTEM_ADMIN. */
const PLATFORM = { userId: 'u3', role: 'super_admin', tenantId: TENANT_A };
/** A role the router does NOT admit — proves the role gate is live. */
const VIEWER = { userId: 'u4', role: 'VIEWER', tenantId: TENANT_A };
/**
 * ORG_ADMIN naming its organisation but carrying NO tenant claim — the one
 * refusal this PR introduces on this route (`403 caller has no tenant`). The
 * auth service signs tenantId conditionally (generateAccessToken in jwt.ts),
 * so this is a token
 * shape that exists, not a hypothetical.
 */
const ADMIN_NO_TENANT = { userId: 'u5', role: 'ORG_ADMIN', organizationId: ORG_A };

const app = express();
app.use(express.json());
app.use('/api/admin', adminConfigRouter);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    // Loopback, explicitly. A function in argument 2 is the CALLBACK, so the
    // host is unset and the socket binds `::` — every interface — which the
    // packages/shared test-listener guard reds. Host second, callback last.
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => {
  server?.close();
});

beforeEach(() => {
  mockQueryRaw.mockReset();
  mockExecuteRaw.mockReset();
  mockExecuteRaw.mockResolvedValue(1);
});

/** The pre-flight SELECT returns one key row owned by `organizationId`. */
function keyOwnedBy(organizationId: string | null): void {
  mockQueryRaw.mockResolvedValue([
    { id: KEY_ID, tenant_id: TENANT_A, organization_id: organizationId },
  ]);
}

async function revoke(principal: object | null): Promise<{ status: number; body: any }> {
  const res = await fetch(`${baseUrl}/api/admin/api-keys/${KEY_ID}`, {
    method: 'DELETE',
    headers: principal ? { 'x-test-principal': JSON.stringify(principal) } : {},
  });
  return { status: res.status, body: await res.json() };
}

describe('KS-764 / Peter Major 2 — the originate revoke surface, on the wire', () => {
  it('CONTROL: decideKeyRevoke is the REAL implementation, not a jest mock', () => {
    // FIRST: the export must EXIST. The two lines below it pass when it does
    // not — `jest.isMockFunction(undefined)` is `false` and `undefined ===
    // undefined` — which is exactly the stale-`packages/shared/dist` state this
    // repo has already had ("decideKeyRevoke is not a function", 22 failures,
    // BACKLOG.md). A control that is green against an absent subject is not a
    // control; this line is what makes the other two mean something.
    expect(typeof shared.decideKeyRevoke).toBe('function');
    // Without this the whole file could be green against a stub. `toBe(false)`
    // on isMockFunction is the direct statement; the identity check proves the
    // spread did not shadow it with something else that merely is not a mock.
    expect(jest.isMockFunction(shared.decideKeyRevoke)).toBe(false);
    expect(shared.decideKeyRevoke).toBe(
      jest.requireActual<typeof shared>('@secuura/shared').decideKeyRevoke,
    );
  });

  it('CONTROL: an unauthenticated caller is refused 401 by the real role gate', async () => {
    keyOwnedBy(ORG_A);
    const { status } = await revoke(null);
    expect(status).toBe(401);
    // The handler was never reached, so the pre-flight SELECT never ran.
    expect(mockQueryRaw).not.toHaveBeenCalled();
  });

  it('CONTROL: a role the router does not admit is refused BEFORE the handler', async () => {
    // Distinguishes requireRole's 403 from the route's own 403: different
    // message, and the SELECT never runs. Without this the organisation arm's
    // refusals could not be told apart from the role gate's.
    keyOwnedBy(ORG_A);
    const { status, body } = await revoke(VIEWER);
    expect(status).toBe(403);
    expect(body.error?.message).toBe('Insufficient permissions');
    expect(mockQueryRaw).not.toHaveBeenCalled();
  });

  it('CASE 1 — same organisation: the revoke succeeds AND the UPDATE runs', async () => {
    // Peter named this one explicitly: the happy path must survive the added
    // SELECT. Asserting the status alone would not show the write happened.
    keyOwnedBy(ORG_A);
    const { status, body } = await revoke(ADMIN_ORG_A);
    expect(status).toBe(200);
    expect(body.success).toBe(true);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });

  it('CASE 2 — cross organisation, SAME tenant: 403 and NO write (the finding)', async () => {
    keyOwnedBy(ORG_B);
    const { status, body } = await revoke(ADMIN_ORG_A);
    expect(status).toBe(403);
    expect(body.error?.code).toBe('FORBIDDEN');
    expect(body.error?.message).toBe('Not authorised to revoke this key');
    // The refusal must be BEFORE the UPDATE. A 403 returned after the row was
    // already deactivated would read identically to the caller and still have
    // destroyed a sibling organisation's key.
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  it('CASE 3 — an ORG-LESS KEY stays revocable by its tenant’s admin (Kam’s ruling)', async () => {
    keyOwnedBy(null);
    const { status, body } = await revoke(ADMIN_ORG_A);
    expect(status).toBe(200);
    expect(body.success).toBe(true);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });

  it('CASE 4 — an ORG-LESS CALLER is refused on an org-owned key, and nothing is written', async () => {
    keyOwnedBy(ORG_A);
    const { status, body } = await revoke(ADMIN_NO_ORG);
    expect(status).toBe(403);
    expect(body.error?.code).toBe('FORBIDDEN');
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  it('CASE 5 — a TENANT-LESS CALLER is refused on an org-owned key (`caller has no tenant`), and nothing is written', async () => {
    // The refusal this PR introduces on this route: before KS-764 it made no
    // tenant comparison at all, so a principal with no tenant claim was never
    // refused here. Same organisation on both sides, so the organisation arm
    // would ALLOW — only the tenant floor can produce this 403. The body is
    // generic by design; the arm is named in the refusal log's `reason`.
    const warn = jest.spyOn(logger, 'warn');
    try {
      keyOwnedBy(ORG_A);
      const { status, body } = await revoke(ADMIN_NO_TENANT);
      expect(status).toBe(403);
      expect(body.error?.code).toBe('FORBIDDEN');
      // The row resolved (the SELECT ran) — the refusal is the policy's, not an
      // empty read's.
      expect(mockQueryRaw).toHaveBeenCalledTimes(1);
      expect(warn).toHaveBeenCalledWith(
        'API key revoke refused',
        expect.objectContaining({ reason: 'caller has no tenant' }),
      );
      expect(mockExecuteRaw).not.toHaveBeenCalled();
    } finally {
      warn.mockRestore();
    }
  });

  it('CONTROL: the PLATFORM bypass survives on this surface too', async () => {
    keyOwnedBy(ORG_B);
    const { status, body } = await revoke(PLATFORM);
    expect(status).toBe(200);
    expect(body.success).toBe(true);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });

  it('CONTROL: a key the tenant-scoped SELECT cannot see is reported missing, not refused', async () => {
    // Proves the 403s above come from the decision and not from an empty read.
    mockQueryRaw.mockResolvedValue([]);
    const { status, body } = await revoke(ADMIN_ORG_A);
    expect(status).toBe(200);
    expect(body.success).toBe(false);
    expect(body.message).toBe('Not found');
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });
});
