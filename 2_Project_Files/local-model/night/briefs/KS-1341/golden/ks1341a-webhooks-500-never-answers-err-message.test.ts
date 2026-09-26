// KS-1341 part A (originate routes/webhooks.ts, GET / and POST /): seven catch blocks answered a 500
// whose body carried the thrown error's own text, with NO NODE_ENV guard, so it reached the client in
// every environment, production included (measured by the 2026-09-26 batch1280 gate). Part A adds the
// file's fail500 helper and converts the first two sites; parts B and C convert the other five.
// Harness copied from ks1160-webhooks-post-persists-normalised-url.test.ts; cell shape from ks730c.
//
// THE GET / TRAP. GET / chains .catch() onto its list query, so a REJECTED $queryRaw is swallowed into
// a 200 with an empty list and never reaches the catch under test. The GET / cell therefore makes
// $queryRaw THROW SYNCHRONOUSLY, and every red cell asserts the catch was REACHED (the logger received
// this route's context with the thrown text), not only that the body is clean. control A0 pins the
// swallowing branch so the trap cannot come back silently.
const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();
const mockLoggerError = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: mockQueryRaw,
    $executeRaw: mockExecuteRaw,
    $executeRawUnsafe: jest.fn(),
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

// THE FIXTURE IS LOAD-BEARING. It must not contain 'does not exist' (the KS-730 PR3 trap) and must
// carry no Postgres SQLSTATE token that utils/pgErrors.ts would classify, so no benign or 4xx branch
// can claim it. The last control below pins both properties.
const LEAK = 'connect ECONNREFUSED 10.0.4.17:5432 ks1341a-private-detail';
const NODE_ENVS = ['production', 'development', 'test', undefined];
const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
const CREATE_BODY = { url: 'https://partner.example.com/hooks', events: ['certification.issued'] };

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

// Each route is driven by making ITS OWN db call throw, so a cell cannot pass because another
// handler answered.
const ROUTES = [
  {
    label: 'GET /',
    method: 'GET',
    body: undefined,
    arm: () => mockQueryRaw.mockImplementationOnce(() => { throw new Error(LEAK); }),
    context: 'Webhook list failed (GET /api/webhooks)',
  },
  {
    label: 'POST /',
    method: 'POST',
    body: CREATE_BODY,
    arm: () => mockExecuteRaw.mockRejectedValueOnce(new Error(LEAK)),
    context: 'Webhook create failed (POST /api/webhooks)',
  },
];

async function call(route: (typeof ROUTES)[number], nodeEnv: string | undefined): Promise<{ status: number; text: string }> {
  setNodeEnv(nodeEnv);
  route.arm();
  const res = await fetch(baseUrl + '/api/webhooks', {
    method: route.method,
    headers: { 'content-type': 'application/json' },
    ...(route.body === undefined ? {} : { body: JSON.stringify(route.body) }),
  });
  return { status: res.status, text: await res.text() };
}

describe('KS-1341 part A: GET / and POST / never answer a 500 with the thrown text', () => {
  it.each(ROUTES)('RED KS-1341 A1 $label: the thrown message is not in the 500 body under production, development, test or unset', async (route) => {
    for (const nodeEnv of NODE_ENVS) {
      const reply = await call(route, nodeEnv);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      // REACHED, not merely clean: only fail500 logs this route's context with the thrown text.
      expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
    }
  });

  it.each(ROUTES)('RED KS-1341 A2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
    const reply = await call(route, 'production');
    expect(reply.status).toBe(500);
    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
  });

  it('control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch', async () => {
    // PRE-EXISTING behaviour this change must NOT alter, and the reason the GET / cell throws
    // synchronously: same route, same message, a rejected promise instead, a different answer.
    setNodeEnv('production');
    mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
    const res = await fetch(baseUrl + '/api/webhooks');
    expect(res.status).toBe(200);
    expect(JSON.parse(await res.text())).toEqual({ success: true, webhooks: [] });
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 A: a create that does NOT throw answers 201 and logs nothing', async () => {
    // Without this, every "not leaked" pass above is consistent with the router answering 500 always.
    setNodeEnv('production');
    mockExecuteRaw.mockResolvedValueOnce(1);
    const res = await fetch(baseUrl + '/api/webhooks', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(CREATE_BODY),
    });
    expect(res.status).toBe(201);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 A: an authored 400 keeps its own text and logs nothing', async () => {
    // The risk of a blanket helper is that it swallows messages a route MEANT to return.
    setNodeEnv('production');
    const res = await fetch(baseUrl + '/api/webhooks', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ url: 'https://partner.example.com/hooks' }),
    });
    expect(res.status).toBe(400);
    expect(JSON.parse(await res.text()).error.message).toBe('url and events (array) are required');
    expect(mockExecuteRaw).not.toHaveBeenCalled();
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 A: the LEAK string is the thrown text and dodges every benign branch', () => {
    // If LEAK were absent from the thrown error, every leaked: false above would hold trivially.
    expect(new Error(LEAK).message).toBe(LEAK);
    expect(LEAK.length).toBeGreaterThan(20);
    expect(LEAK).not.toContain('does not exist');
    expect(LEAK).not.toMatch(/\b(22P02|22001|22007|22008|22021|22P05|23502|23503|23505|23514|42804)\b/);
  });
});
