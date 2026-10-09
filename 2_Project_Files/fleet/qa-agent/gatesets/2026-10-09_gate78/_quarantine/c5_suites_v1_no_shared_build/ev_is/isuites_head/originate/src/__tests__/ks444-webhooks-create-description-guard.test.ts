/**
 * KS-444 — POST /api/webhooks: description must be a string.
 *
 * The create handler validated url + events but bound `description` into the
 * INSERT untyped — the sweep's negative_data_rejection sent `description: {}`
 * (the published WebhookCreateRequest declares an optional string) and it was
 * accepted with a 201, the object echoed back in the response. The handler now
 * rejects a non-string description at the boundary. Harness mirrors
 * ks445-webhook-patch-body-guard.test.ts.
 */

const mockExecuteRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: jest.fn(),
    $executeRaw: mockExecuteRaw,
    $executeRawUnsafe: jest.fn(),
  },
}));

jest.mock('../middleware/auth', () => ({
  // Auth is not under test — inject a stub caller for organization_id.
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: '11111111-2222-4333-8444-555555555555' };
    next();
  },
}));

// The create path encrypts the signing secret at rest (F-18); the crypto
// itself is not under test and needs no key material here. runWithTenantId
// (added by KS-458 while this suite was load-dead on the uuid-ESM class —
// revived in KS-466) just runs the callback: the GUC mechanics are covered by
// ks458-db-tenant-guc.test.ts.
//
// KS-927: `assertSafeOutboundUrl` MUST be in this factory. `webhooks.ts:170`
// calls it on the create path, and a `jest.mock` factory REPLACES the module —
// an export the factory omits is `undefined` at call time, not the real one. So
// both POSITIVE cells 500'd while the two negative ones stayed green, and the
// suite still printed two ticks. A guard suite running only its negative half
// cannot tell "the boundary rejects bad input" from "the route rejects
// everything" — which is the shape a coverage number reports as fine.
//
// Faithful to the real contract (`packages/shared/src/security/ssrf-guard.ts:358`):
// it is ASYNC and resolves `{ ok: true; url } | { ok: false; error }`. Returning
// ok for whatever it is handed is correct HERE and only here — this suite's
// subject is the DESCRIPTION type guard, not SSRF, and the SSRF behaviour has
// its own cells in `packages/shared/src/__tests__/ssrf-guard.test.ts`. A mock
// that answered ok:false would test the wrong boundary.
//
// NOT `jest.requireActual`: that pulls real DNS resolution into a unit test.
jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    encryptField: jest.fn(() => 'v1:mock-ciphertext'),
    decryptField: jest.fn(() => ''),
    runWithTenantId: jest.fn(async (_tenantId: unknown, fn: () => unknown) => fn()),
    assertSafeOutboundUrl: jest.fn(async (raw: unknown) => ({ ok: true as const, url: String(raw) })),
  }),
);

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import express from 'express';
import { webhooksRouter } from '../routes/webhooks';

// KS-487 (Peter's review of #720, 2026-08-31 / 2026-09-09, ask 1): a handle on the MOCKED guard so a
// 201 case can assert it was CONSULTED. Without this, deleting `assertSafeOutboundUrl` from
// `routes/webhooks.ts` leaves this suite green — the same wiring defect that killed both 201 cases
// on 2026-08-13 (#683) would be invisible again. `jest.requireMock` returns the factory's own object,
// so this line is unchanged if the factory is later built by a helper.
const shared = jest.requireMock('@secuura/shared') as { assertSafeOutboundUrl: jest.Mock };

const app = express();
app.use('/api/webhooks', express.json(), webhooksRouter);

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
beforeEach(() => jest.clearAllMocks());

/** Canonical error-envelope shape the routes emit (KS-367). */
interface ErrorEnvelope {
  success?: boolean;
  error?: { code?: string; message?: string };
}

/** Helper: POST a subscription body and return the response. */
function createWebhook(body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/webhooks`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

/** A spec-valid base body (public HTTPS url + one declared event). */
const VALID_BASE = { url: 'https://partner.example.com/hooks', events: ['certification.issued'] };

describe('KS-444 POST /api/webhooks — description type guard', () => {
  it('400s an object description (the sweep body) — DB untouched', async () => {
    const res = await createWebhook({ ...VALID_BASE, description: {} });
    expect(res.status).toBe(400);
    const body = (await res.json()) as ErrorEnvelope;
    expect(body.error?.code).toBe('BAD_REQUEST');
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  it('400s a null description — the published contract is an optional string, not nullable', async () => {
    const res = await createWebhook({ ...VALID_BASE, description: null });
    expect(res.status).toBe(400);
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  it('201s with a string description and stores the subscription', async () => {
    mockExecuteRaw.mockResolvedValueOnce(1);
    const res = await createWebhook({ ...VALID_BASE, description: 'partner integration' });
    expect(res.status).toBe(201);
    const body = (await res.json()) as { success?: boolean; webhook?: { description?: string } };
    expect(body.success).toBe(true);
    expect(body.webhook?.description).toBe('partner integration');
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    // KS-487 ask 1: the guard was consulted exactly once, with the URL this case posted.
    expect(shared.assertSafeOutboundUrl).toHaveBeenCalledTimes(1);
    expect(shared.assertSafeOutboundUrl).toHaveBeenCalledWith(VALID_BASE.url);
  });

  it('201s with description omitted (optional in the published contract)', async () => {
    mockExecuteRaw.mockResolvedValueOnce(1);
    const res = await createWebhook(VALID_BASE);
    expect(res.status).toBe(201);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    // KS-487 ask 1: consulted once here too — the omitted-description path still reaches the guard.
    expect(shared.assertSafeOutboundUrl).toHaveBeenCalledTimes(1);
  });
});
