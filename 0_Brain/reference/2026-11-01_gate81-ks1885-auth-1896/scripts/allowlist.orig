/**
 * =============================================================================
 * KS-1885 — the exchange-error allowlist is exact, on the callback and on POST /social/link
 * =============================================================================
 * The callback (`GET /api/auth/social/:provider/callback`) passes an exchange error's text to the client only when our
 * own code wrote it: an AppError, or exactly one of the adapters' own texts (two anchored patterns). Everything else
 * answers `OAuth authentication failed: the provider answer could not be read`, status unchanged (400). The log names
 * the provider and an identifier-shaped error name, never the message.
 *
 * `POST /social/link` (F3) answers exactly what it answered before (500 INTERNAL_ERROR, or the AppError's own status),
 * but the error handler logs `err.message` and `err.stack`, so a raw exchange error put the token in the error log.
 * Our own texts are rethrown as they are; anything else is logged by name and replaced by a neutral Error.
 *
 * Harness: a fake provider whose exchangeCode throws the value a cell chooses, through the REAL routes and the REAL
 * error handler. No network. The logger is captured. RED cells fail at the untouched base; PIN and CONTROL cells pass
 * at the base by design and must still pass.
 * =============================================================================
 */
import { describe, it, expect, beforeAll, beforeEach, afterAll, vi } from 'vitest';
import http from 'node:http';
import express from 'express';
import type { AddressInfo } from 'node:net';

const { silentLogger, redisStore, thrower } = vi.hoisted(() => ({
  silentLogger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() },
  redisStore: new Map<string, string>(),
  thrower: { make: (): unknown => new Error('unset') },
}));
vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));
vi.mock('../services/session', () => ({
  createSession: vi.fn(async () => ({ id: 'sess-ks1885b' })),
  getRedisClient: vi.fn(() => ({
    setex: async (k: string, _ttl: number, v: string) => { redisStore.set(k, v); return 'OK'; },
    getdel: async (k: string) => { const v = redisStore.get(k) ?? null; redisStore.delete(k); return v; },
  })),
  validateSession: vi.fn(async () => true),
  updateSessionActivity: vi.fn(async () => undefined),
}));
vi.mock('../repositories/userRepo', () => ({
  getUserBySocialId: vi.fn(async () => null),
  getUserByEmail: vi.fn(async () => null),
  getUserById: vi.fn(async () => null),
  updateUser: vi.fn(async () => undefined),
  createUser: vi.fn(async (u: Record<string, unknown>) => u),
  getPlatformAdmin: vi.fn(async () => null),
  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
  seedDemoUsers: vi.fn(async () => undefined),
}));
vi.mock('../services/jwt', () => ({
  generateTokenPair: vi.fn(() => ({ accessToken: 'MINTED_KS1885B', refreshToken: 'MINTED_KS1885B_R', expiresIn: 900 })),
  verifyAccessToken: vi.fn(() => ({})),
}));
const passthrough = () => (req: { user?: unknown }, _s: unknown, n: () => void) => { req.user = { userId: 'user-ks1885b' }; n(); };
vi.mock('../middleware/authenticate', () => ({
  authenticate: passthrough,
  authenticateAccessOrConnector: passthrough,
  requireRole: passthrough,
  requireVerificationLevel: passthrough,
  requireOwnership: passthrough,
  requireSameOrganization: passthrough,
}));
vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [] })) }));
vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
vi.mock('../providers/social', async (importOriginal) => {
  const real = await importOriginal<Record<string, unknown>>();
  const NAMES = ['github', 'google', 'linkedin', 'apple', 'facebook', 'microsoft_personal'];
  const fake = {
    getAuthUrl: (state: string) => `https://provider.test/auth?state=${state}`,
    exchangeCode: async () => { throw thrower.make(); },
  };
  class FakeFactory {
    get(name: string) { return NAMES.includes(name) ? fake : undefined; }
    getEnabled() { return NAMES; }
    has(n: string) { return NAMES.includes(n); }
    isValidProvider(n: string) { return NAMES.includes(n); }
  }
  return { ...real, SocialProviderFactory: FakeFactory };
});

const SENTINEL = 'KS1885SENTINELb3n8m1';
const CONSTANT = 'OAuth authentication failed: the provider answer could not be read';
const LABELS = ['Apple', 'Facebook', 'GitHub', 'Google', 'LinkedIn', 'Microsoft'];
const PROFILE_LABELS = ['Facebook', 'GitHub', 'Google', 'LinkedIn', 'Microsoft'];
// Every text the adapters write themselves, in the shapes they write them (read from providers/social at develop d7691f35).
const ADAPTER_TEXTS = [
  ...LABELS.flatMap((l) => [`${l} token exchange failed (HTTP 400)`, `${l} token exchange failed (HTTP 502)`, `${l} token exchange failed (no access token)`]),
  ...PROFILE_LABELS.flatMap((l) => [`Failed to fetch ${l} user profile`, `Failed to fetch ${l} user profile (HTTP 401)`]),
];

let errorHandlerModule: typeof import('../middleware/errorHandler');
let app: http.Server | undefined;
let appUrl = '';

beforeAll(async () => {
  const { authRoutes } = await import('../routes/auth');
  errorHandlerModule = await import('../middleware/errorHandler');
  const ex = express();
  ex.use(express.json());
  ex.use('/api/auth', authRoutes);
  ex.use(errorHandlerModule.errorHandler);
  app = http.createServer(ex as http.RequestListener);
  await new Promise<void>((resolve) => app!.listen(0, '127.0.0.1', () => resolve()));
  appUrl = `http://127.0.0.1:${(app.address() as AddressInfo).port}`;
}, 60000);

afterAll(async () => {
  if (!app) return;
  app.closeAllConnections();
  await new Promise<void>((r) => app!.close(() => r()));
});

beforeEach(() => {
  redisStore.clear();
  for (const fn of Object.values(silentLogger)) fn.mockClear();
});

type Res = { status: number; code: string | null; message: string | null; raw: string };
function call(method: 'GET' | 'POST', p: string, body?: unknown): Promise<Res> {
  return new Promise((resolve, reject) => {
    const target = new URL(appUrl);
    const payload = body === undefined ? undefined : JSON.stringify(body);
    const req = http.request({ hostname: target.hostname, port: target.port, path: p, method, agent: false,
      headers: payload ? { 'content-type': 'application/json', 'content-length': String(Buffer.byteLength(payload)) } : {} }, (res) => {
      const c: Buffer[] = [];
      res.on('data', (d) => c.push(d));
      res.on('end', () => {
        const raw = Buffer.concat(c).toString();
        let code: string | null = null; let message: string | null = null;
        try { const e = JSON.parse(raw)?.error; code = e?.code ?? null; message = e?.message ?? null; } catch { /* not JSON: raw is still asserted on */ }
        resolve({ status: res.statusCode ?? 0, code, message, raw });
      });
    });
    req.on('error', reject);
    if (payload) req.write(payload);
    req.end();
  });
}

async function callback(make: () => unknown): Promise<Res> {
  thrower.make = make;
  const init = await call('GET', '/api/auth/social/github');
  const state = JSON.parse(init.raw).state as string;
  return call('GET', `/api/auth/social/github/callback?code=c-ks1885b&state=${encodeURIComponent(state)}`);
}
async function link(make: () => unknown): Promise<Res> {
  thrower.make = make;
  return call('POST', '/api/auth/social/link', { provider: 'github', code: 'c-ks1885b' });
}
const allLogs = (): string => JSON.stringify(Object.fromEntries(Object.entries(silentLogger).map(([k, fn]) => [k, fn.mock.calls])));
const warnsNamed = (msg: string) => silentLogger.warn.mock.calls.filter((c) => c[0] === msg).map((c) => c[1]);
const CALLBACK_WARN = 'Social callback: the provider code exchange failed';
const LINK_WARN = 'Social link: the provider code exchange failed';

describe('KS-1885 callback: a text our code did not write never reaches the client or the log', () => {
  const cases: Array<[string, () => unknown]> = [
    ['a TypeError quoting a Bearer header with the token in it', () => new TypeError(`Headers.append: "Bearer tok-${SENTINEL}\n${SENTINEL}" is an invalid header value.`)],
    ['an adapter text with the token appended (the $ anchor)', () => new Error(`GitHub token exchange failed (HTTP 400) ${SENTINEL}`)],
    ['an adapter text with the token in front (the ^ anchor)', () => new Error(`${SENTINEL} GitHub token exchange failed (HTTP 400)`)],
    ['a plain Error carrying only the token', () => new Error(SENTINEL)],
    ['a thrown object with a message property', () => ({ message: SENTINEL })],
    // Not a string, but String() of it IS an adapter text: only the typeof check keeps it out of the allowlist.
    ['a message that is not a string but reads as an adapter text', () => ({ message: ['GitHub token exchange failed (HTTP 400)'] })],
  ];
  it.each(cases)('RED %s: 400 with the constant, no token in the body, no token in any log line', async (_label, make) => {
    const r = await callback(make);
    // Soft: every failing assertion is reported, so a red at the base shows which of them saw the leak.
    expect.soft([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', CONSTANT]);
    expect.soft(r.raw).not.toContain(SENTINEL);
    expect.soft(allLogs()).not.toContain(SENTINEL);
  });

  it('RED a thrown string answers the constant (it answered "invalid authorization code" before; the status is unchanged)', async () => {
    const r = await callback(() => 'a thrown string');
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', CONSTANT]);
  });

  it('RED an Error with an EMPTY message answers the constant (it answered "invalid authorization code" before; the status is unchanged)', async () => {
    const r = await callback(() => new Error(''));
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', CONSTANT]);
  });

  it('RED the warn names the class only: an identifier-shaped name is logged, a name that is not is logged as "unnamed"', async () => {
    await callback(() => new TypeError(SENTINEL));
    expect(warnsNamed(CALLBACK_WARN)).toEqual([{ provider: 'github', errorName: 'TypeError' }]);
    for (const fn of Object.values(silentLogger)) fn.mockClear();
    const odd = new Error(SENTINEL);
    odd.name = `${SENTINEL} with a space`;
    const r = await callback(() => odd);
    expect(r.message).toBe(CONSTANT);
    expect(warnsNamed(CALLBACK_WARN)).toEqual([{ provider: 'github', errorName: 'unnamed' }]);
    expect(allLogs()).not.toContain(SENTINEL);
    // A name that is not a string, though String() of it is identifier-shaped: only the typeof check logs it as "unnamed".
    for (const fn of Object.values(silentLogger)) fn.mockClear();
    const odder = new Error('x');
    (odder as unknown as { name: unknown }).name = [SENTINEL];
    await callback(() => odder);
    expect(warnsNamed(CALLBACK_WARN)).toEqual([{ provider: 'github', errorName: 'unnamed' }]);
    expect(allLogs()).not.toContain(SENTINEL);
  });
});

describe('KS-1885 callback: what passed before still passes', () => {
  it('PIN a SyntaxError (KS 1791) still answers the constant and none of its text', async () => {
    const r = await callback(() => new SyntaxError(`Unexpected token '<', "<html>${SENTINEL}"... is not valid JSON`));
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', CONSTANT]);
    expect(r.raw).not.toContain(SENTINEL);
  });

  it('PIN an AppError keeps its own text (the adapters\' timeout text), still as a 400', async () => {
    const text = 'GitHub did not answer in time; please try again.';
    const r = await callback(() => new errorHandlerModule.ServiceUnavailableError(text));
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', `OAuth authentication failed: ${text}`]);
  });

  it.each(ADAPTER_TEXTS)('PIN the adapter text "%s" still reaches the client unchanged', async (text) => {
    const r = await callback(() => new Error(text));
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', `OAuth authentication failed: ${text}`]);
  });

  it('CONTROL a thrown value whose own property reads throw still answers 500, as before (no hang, no status change)', async () => {
    const hostile = new Proxy(new Error('hostile'), { get(t, p) { if (p === 'name' || p === 'message') throw new Error('trap'); return Reflect.get(t, p); } });
    const r = await callback(() => hostile);
    expect([r.status, r.code, r.message]).toEqual([500, 'INTERNAL_ERROR', 'An unexpected error occurred']);
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    const r2 = await callback(() => proxy);
    expect([r2.status, r2.code, r2.message]).toEqual([500, 'INTERNAL_ERROR', 'An unexpected error occurred']);
  });
});

describe('KS-1885 F3: POST /social/link answers exactly as before, and its log no longer carries the exchange error\'s text', () => {
  it('RED a TypeError carrying the token: 500 INTERNAL_ERROR with the generic text, and no token in any log line', async () => {
    const r = await link(() => new TypeError(`Headers.append: "Bearer tok-${SENTINEL}\n${SENTINEL}" is an invalid header value.`));
    expect.soft([r.status, r.code, r.message]).toEqual([500, 'INTERNAL_ERROR', 'An unexpected error occurred']);
    expect.soft(r.raw).not.toContain(SENTINEL);
    expect.soft(allLogs()).not.toContain(SENTINEL);
    expect.soft(warnsNamed(LINK_WARN)).toEqual([{ provider: 'github', errorName: 'TypeError' }]);
  });

  it('PIN an AppError still answers its own status and text (503)', async () => {
    const text = 'GitHub could not be reached; please try again.';
    const r = await link(() => new errorHandlerModule.ServiceUnavailableError(text));
    expect([r.status, r.code, r.message]).toEqual([503, 'SERVICE_UNAVAILABLE', text]);
  });

  it('PIN an adapter text still answers 500 INTERNAL_ERROR, and the text stays in the error log for an operator', async () => {
    const text = 'GitHub token exchange failed (HTTP 400)';
    const r = await link(() => new Error(text));
    expect([r.status, r.code, r.message]).toEqual([500, 'INTERNAL_ERROR', 'An unexpected error occurred']);
    expect(JSON.stringify(silentLogger.error.mock.calls)).toContain(text);
  });
});
