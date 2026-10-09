// KS-1160: POST /api/webhooks persists and echoes the RAW request url where PATCH persists the
// SSRF guard's NORMALISED one. The create handler consults validateWebhookUrl (webhooks.ts:219)
// and then DISCARDS its .url: :257 binds the raw url into the INSERT and :262 echoes it. The
// harness mirrors ks444-webhooks-create-description-guard.test.ts with ONE change inside the
// @secuura/shared mock: assertSafeOutboundUrl NORMALISES (trims), so the defect is observable.

const mockExecuteRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: jest.fn(),
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
    assertSafeOutboundUrl: jest.fn(async (raw: unknown) => ({ ok: true as const, url: String(raw).trim() })),
  }),
);

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { webhooksRouter } from '../routes/webhooks';

const shared = jest.requireMock('@secuura/shared') as { assertSafeOutboundUrl: jest.Mock };

const app = express();
app.use('/api/webhooks', express.json(), webhooksRouter);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});

afterAll(() => server?.close());
beforeEach(() => {
  mockExecuteRaw.mockReset();
  shared.assertSafeOutboundUrl.mockClear();
});

function createWebhook(body: unknown): Promise<Response> {
  return fetch(baseUrl + '/api/webhooks', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

const RAW = '  https://partner.example.com/hooks  ';
const NORMALISED = 'https://partner.example.com/hooks';

describe('KS-1160 POST /api/webhooks: url normalisation persistence', () => {
  it('RED KS-1160 A: POST persists the guard NORMALISED url, not the raw request string', async () => {
    mockExecuteRaw.mockResolvedValueOnce(1);
    const res = await createWebhook({ url: RAW, events: ['certification.issued'] });
    expect(res.status).toBe(201);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    const boundUrl = mockExecuteRaw.mock.calls[0][4];
    expect(boundUrl).toBe(NORMALISED);
  });

  it('RED KS-1160 B: the 201 body echoes the normalised url', async () => {
    mockExecuteRaw.mockResolvedValueOnce(1);
    const res = await createWebhook({ url: RAW, events: ['certification.issued'] });
    expect(res.status).toBe(201);
    const body = (await res.json()) as { webhook?: { url?: string } };
    expect(body.webhook?.url).toBe(NORMALISED);
  });

  it('control: the guard is consulted once with the raw request url, before and after', async () => {
    mockExecuteRaw.mockResolvedValueOnce(1);
    await createWebhook({ url: RAW, events: ['certification.issued'] });
    expect(shared.assertSafeOutboundUrl).toHaveBeenCalledTimes(1);
    expect(shared.assertSafeOutboundUrl).toHaveBeenCalledWith(RAW);
  });
});
