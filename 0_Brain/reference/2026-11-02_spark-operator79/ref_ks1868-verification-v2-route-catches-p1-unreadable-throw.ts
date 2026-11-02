// KS-1868 (originate routes/verificationV2.ts, POST /api/v2/verification/verify and POST /api/v2/verification/verify-file): both route catch blocks logged
// `error instanceof Error ? error.message : String(error)` themselves and then answered the constant 500. When the thrown value cannot be read (a revoked Proxy makes
// `instanceof` throw; an Error whose `message` getter throws), that read threw INSIDE the catch: the handler's promise rejected and the request got NO answer. Both catches
// now read the value inside their own try and log the constant reason `unreadable thrown value`. The database stand-in rejects with the thrown value on a real loopback
// listener; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();
const mockLoggerError = jest.fn();

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw },
  getTenantManager: () => null,
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
    queryWithTenantGuc: jest.fn(),
  }),
);

jest.mock('../repositories/documentRepo', () => ({
  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
  updateDocument: jest.fn().mockResolvedValue(undefined),
  MAX_LINEAGE_DEPTH: 10,
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { verificationV2Router } from '../routes/verificationV2';

const CONSTANT_BODY_VERIFY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Verification failed' } };
const CONSTANT_BODY_FILE = { success: false, error: { code: 'INTERNAL_ERROR', message: 'File verification failed' } };
const UNREADABLE = 'unreadable thrown value';
const HASH = 'f'.repeat(64);

const ROUTES = [
  { route: 'POST /verify', path: '/verify', context: 'v2 verification error', constant: CONSTANT_BODY_VERIFY, file: false },
  { route: 'POST /verify-file', path: '/verify-file', context: 'v2 file verification error', constant: CONSTANT_BODY_FILE, file: true },
];

const app = express();
app.use(express.json());
app.use('/api/v2/verification', verificationV2Router);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => server?.close());
beforeEach(() => jest.clearAllMocks());

async function callWithThrow(c: (typeof ROUTES)[number], thrown: unknown): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
  mockQueryRaw.mockRejectedValueOnce(thrown);
  try {
    const res = await fetch(baseUrl + '/api/v2/verification' + c.path, {
      method: 'POST',
      headers: { 'content-type': c.file ? 'application/octet-stream' : 'application/json' },
      body: c.file ? Buffer.from('ks1868 file bytes') : JSON.stringify({ hash: HASH }),
      signal: AbortSignal.timeout(1500),
    });
    return { status: res.status, body: await res.json() };
  } catch {
    return { status: 'NO ANSWER', body: null };
  }
}

function revokedProxy(): object {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
}

function throwingMessageError(): Error {
  const e = new Error('ks1868 hidden');
  Object.defineProperty(e, 'message', {
    get() {
      throw new Error('ks1868 message getter');
    },
  });
  return e;
}

describe.each(ROUTES)('KS-1868 $route catch reads the thrown value safely', (c) => {
  it(`RED ks1868 R1 ${c.route}: a revoked Proxy thrown by the database is logged as a constant reason and answered with the constant 500`, async () => {
    const reply = await callWithThrow(c, revokedProxy());
    expect(reply).toEqual({ status: 500, body: c.constant });
    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
  });

  it(`RED ks1868 R2 ${c.route}: an Error whose message getter throws is logged as a constant reason and answered with the constant 500`, async () => {
    const reply = await callWithThrow(c, throwingMessageError());
    expect(reply).toEqual({ status: 500, body: c.constant });
    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
  });

  it(`control ks1868 C1 ${c.route}: an ordinary Error logs its own message and the answer is the constant 500 without it`, async () => {
    const reply = await callWithThrow(c, new Error('ks1868 ordinary'));
    expect(reply).toEqual({ status: 500, body: c.constant });
    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
  });

  it(`control ks1868 C2 ${c.route}: a thrown string is logged as itself, as before`, async () => {
    const reply = await callWithThrow(c, 'ks1868 plain string');
    expect(reply).toEqual({ status: 500, body: c.constant });
    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 plain string' }]]);
  });
});
