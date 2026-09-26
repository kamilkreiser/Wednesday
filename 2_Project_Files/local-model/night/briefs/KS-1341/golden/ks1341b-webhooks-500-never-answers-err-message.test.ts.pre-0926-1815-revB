// KS-1341 part B (originate routes/webhooks.ts, PATCH /:id, DELETE /:id, POST /:id/rotate-secret):
// the three write routes answered a 500 whose body carried the thrown error's own text in every
// NODE_ENV. The 2026-09-26 gate MEASURED two of them in production: DELETE /:id returned the thrown
// text, and rotate-secret returned the field-encryption layer's internal configuration message.
// Part A added the fail500 helper; this part converts these three catch blocks to it and changes
// NOTHING on the secret path (generation, encryption, storage, the one-time return) - the last
// rotate-secret control pins that path end to end.
// Harness copied from ks1160-webhooks-post-persists-normalised-url.test.ts; cell shape from ks730c.
const mockExecuteRaw = jest.fn();
const mockExecuteRawUnsafe = jest.fn();
const mockLoggerError = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: jest.fn(),
    $executeRaw: mockExecuteRaw,
    $executeRawUnsafe: mockExecuteRawUnsafe,
  },
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: '11111111-2222-4333-8444-555555555555' };
    next();
  },
}));

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    encryptField: jest.fn(() => 'v1:mock-ciphertext'),
    decryptField: jest.fn(() => ''),
    runWithTenantId: jest.fn(async (_tenantId: unknown, fn: () => unknown) => fn()),
    assertSafeOutboundUrl: jest.fn(async (raw: unknown) => ({ ok: true as const, url: String(raw) })),
  }),
);

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { webhooksRouter } from '../routes/webhooks';

const shared = jest.requireMock('@secuura/shared') as { encryptField: jest.Mock };

// THE FIXTURE IS LOAD-BEARING. It must not contain 'does not exist' (the KS-730 PR3 trap) and must
// carry no Postgres SQLSTATE token: PATCH's catch sends a classified SQLSTATE to an honest 400
// BEFORE the 500 line, so a LEAK carrying one would never reach the site under test.
const LEAK = 'PII encryption is not initialised: call registerKey() first ks1341b-private-detail';
const NODE_ENVS = ['production', 'development', 'test', undefined];
const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
const WEBHOOK_ID = 'a1b2c3d4-5678-4abc-9def-0123456789ab';

const app = express();
app.use('/api/webhooks', express.json(), webhooksRouter);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => {
  if (ORIGINAL_NODE_ENV === undefined) delete process.env.NODE_ENV;
  else process.env.NODE_ENV = ORIGINAL_NODE_ENV;
  server?.close();
});
beforeEach(() => jest.clearAllMocks());

function setNodeEnv(v: string | undefined): void {
  if (v === undefined) delete process.env.NODE_ENV;
  else process.env.NODE_ENV = v;
}

// Each route is driven by making ITS OWN call throw, so a cell cannot pass because another handler
// answered. rotate-secret throws from encryptField, the shape the gate measured in production.
const ROUTES = [
  {
    label: 'PATCH /:id',
    method: 'PATCH',
    path: '/' + WEBHOOK_ID,
    body: { description: 'ks1341b' },
    arm: () => mockExecuteRawUnsafe.mockRejectedValueOnce(new Error(LEAK)),
    context: 'Webhook update failed (PATCH /api/webhooks/:id)',
  },
  {
    label: 'DELETE /:id',
    method: 'DELETE',
    path: '/' + WEBHOOK_ID,
    body: undefined,
    arm: () => mockExecuteRaw.mockRejectedValueOnce(new Error(LEAK)),
    context: 'Webhook delete failed (DELETE /api/webhooks/:id)',
  },
  {
    label: 'POST /:id/rotate-secret',
    method: 'POST',
    path: '/' + WEBHOOK_ID + '/rotate-secret',
    body: undefined,
    arm: () => shared.encryptField.mockImplementationOnce(() => { throw new Error(LEAK); }),
    context: 'Webhook secret rotation failed (POST /api/webhooks/:id/rotate-secret)',
  },
];

async function call(route: (typeof ROUTES)[number], nodeEnv: string | undefined): Promise<{ status: number; text: string }> {
  setNodeEnv(nodeEnv);
  route.arm();
  const res = await fetch(baseUrl + '/api/webhooks' + route.path, {
    method: route.method,
    headers: { 'content-type': 'application/json' },
    ...(route.body === undefined ? {} : { body: JSON.stringify(route.body) }),
  });
  return { status: res.status, text: await res.text() };
}

describe('KS-1341 part B: PATCH, DELETE and rotate-secret never answer a 500 with the thrown text', () => {
  it.each(ROUTES)('RED KS-1341 B1 $label: the thrown message is not in the 500 body under production, development, test or unset', async (route) => {
    for (const nodeEnv of NODE_ENVS) {
      const reply = await call(route, nodeEnv);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      // REACHED, not merely clean: only fail500 logs this route's context with the thrown text.
      expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
    }
  });

  it.each(ROUTES)('RED KS-1341 B2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
    const reply = await call(route, 'production');
    expect(reply.status).toBe(500);
    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
  });

  it('control KS-1341 B0: a classified Postgres cast failure on PATCH still answers 400 and never reaches fail500', async () => {
    // PRE-EXISTING KS-445 branch this change must NOT alter (same error shape as ks445's own cell).
    setNodeEnv('production');
    mockExecuteRawUnsafe.mockRejectedValueOnce(
      Object.assign(new Error('Raw query failed. Code: `42804`. Message: `datatype mismatch`'), {
        code: 'P2010',
        meta: { code: '42804' },
      }),
    );
    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID, {
      method: 'PATCH',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ isActive: true }),
    });
    expect(res.status).toBe(400);
    expect(JSON.parse(await res.text()).error.code).toBe('VALIDATION_ERROR');
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 B: a rotate-secret that does NOT throw still encrypts, stores and returns the new secret once', async () => {
    // The secret path is OUT of scope and must be byte-for-byte unchanged: a fresh whsec_ secret,
    // encrypted with this row's AAD, stored, returned in the 200 body, and nothing logged.
    setNodeEnv('production');
    mockExecuteRaw.mockResolvedValueOnce(1);
    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID + '/rotate-secret', { method: 'POST' });
    expect(res.status).toBe(200);
    const body = JSON.parse(await res.text());
    expect(body.success).toBe(true);
    expect(body.secret).toMatch(/^whsec_[0-9a-f]{48}$/);
    expect(shared.encryptField).toHaveBeenCalledWith(body.secret, 'svc_webhooks.secret.' + WEBHOOK_ID);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 B: a DELETE that does NOT throw answers 200 and logs nothing', async () => {
    // Without this, every "not leaked" pass above is consistent with the router answering 500 always.
    setNodeEnv('production');
    mockExecuteRaw.mockResolvedValueOnce(1);
    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID, { method: 'DELETE' });
    expect(res.status).toBe(200);
    expect(JSON.parse(await res.text())).toEqual({ success: true });
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 B: an authored 400 keeps its own text and logs nothing', async () => {
    // A pattern-malformed id is refused by the KS-431 guard with its own message, before any query.
    setNodeEnv('production');
    const res = await fetch(baseUrl + '/api/webhooks/bad%20id', { method: 'DELETE' });
    expect(res.status).toBe(400);
    expect(JSON.parse(await res.text()).error.message).toBe('Invalid webhook id format');
    expect(mockExecuteRaw).not.toHaveBeenCalled();
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 B: the LEAK string is the thrown text and dodges every benign branch', () => {
    // If LEAK were absent from the thrown error, every leaked: false above would hold trivially.
    expect(new Error(LEAK).message).toBe(LEAK);
    expect(LEAK.length).toBeGreaterThan(20);
    expect(LEAK).not.toContain('does not exist');
    expect(LEAK).not.toMatch(/\b(22P02|22001|22007|22008|22021|22P05|23502|23503|23505|23514|42804)\b/);
  });
});
