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

// ============================================================================
// GATE 81 probes (QA, not part of the PR). Same harness as the author's allowlist file.
// ============================================================================
const G = 'G81SMUGGLEDzq9x4';
describe('G81 allowlist bypass probes (callback)', () => {
  const cases: Array<[string, () => unknown]> = [
    ['adapter text + LF + token', () => new Error(`GitHub token exchange failed (HTTP 400)\n${G}`)],
    ['token + LF + adapter text', () => new Error(`${G}\nGitHub token exchange failed (HTTP 400)`)],
    ['adapter text + CRLF + token', () => new Error(`GitHub token exchange failed (HTTP 400)\r\n${G}`)],
    ['adapter text + U+2028 + token', () => new Error(`GitHub token exchange failed (HTTP 400) ${G}`)],
    ['adapter text + U+2029 + token', () => new Error(`GitHub token exchange failed (HTTP 400) ${G}`)],
    ['profile text + LF + token', () => new Error(`Failed to fetch GitHub user profile\n${G}`)],
    ['profile text (HTTP) + LF + token', () => new Error(`Failed to fetch Google user profile (HTTP 401)\n${G}`)],
    ['adapter text with trailing LF only', () => new Error(`GitHub token exchange failed (HTTP 400)\n`)],
    ['adapter text, status widened with token', () => new Error(`GitHub token exchange failed (HTTP 400 ${G})`)],
    ['adapter text, 4-digit status', () => new Error(`GitHub token exchange failed (HTTP 4001)`)],
    ['adapter text, Arabic-Indic digits', () => new Error(`GitHub token exchange failed (HTTP ٤٠٠)`)],
    ['adapter text, NUL + token', () => new Error(`GitHub token exchange failed (HTTP 400)\u0000${G}`)],
  ];
  it.each(cases)('G81 %s -> 400 constant, token nowhere', async (_l, make) => {
    const r = await callback(make);
    expect.soft([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', CONSTANT]);
    expect.soft(r.raw).not.toContain(G);
    expect.soft(allLogs()).not.toContain(G);
  });
  it('G81 a TypeError named by a 65-char identifier logs "unnamed"; a 64-char one logs the name', async () => {
    const e1 = new TypeError('x'); e1.name = 'A'.repeat(65);
    await callback(() => e1);
    expect(warnsNamed(CALLBACK_WARN)).toEqual([{ provider: 'github', errorName: 'unnamed' }]);
    for (const fn of Object.values(silentLogger)) fn.mockClear();
    const e2 = new TypeError('x'); e2.name = 'A'.repeat(64);
    await callback(() => e2);
    expect(warnsNamed(CALLBACK_WARN)).toEqual([{ provider: 'github', errorName: 'A'.repeat(64) }]);
  });
  it('G81 name with an embedded LF is "unnamed"', async () => {
    const e = new Error('x'); e.name = `TypeError\n${G}`;
    await callback(() => e);
    expect(warnsNamed(CALLBACK_WARN)).toEqual([{ provider: 'github', errorName: 'unnamed' }]);
    expect(allLogs()).not.toContain(G);
  });
  it('G81 adapter-text PIN run twice in a row both pass (no lastIndex state)', async () => {
    for (let i = 0; i < 3; i++) {
      const r = await callback(() => new Error('GitHub token exchange failed (HTTP 400)'));
      expect(r.message).toBe('OAuth authentication failed: GitHub token exchange failed (HTTP 400)');
    }
  });
});
describe('G81 F3 link probes', () => {
  it('G81 link: adapter text + LF + token -> 500 generic, token in no log line', async () => {
    const r = await link(() => new Error(`GitHub token exchange failed (HTTP 400)\n${G}`));
    expect.soft([r.status, r.code, r.message]).toEqual([500, 'INTERNAL_ERROR', 'An unexpected error occurred']);
    expect.soft(r.raw).not.toContain(G);
    expect.soft(allLogs()).not.toContain(G);
  });
  it('G81 link: plain Error carrying the token -> 500 generic, token in no log line, body byte-identical to a base TypeError 500', async () => {
    const r = await link(() => new Error(G));
    expect.soft(r.status).toBe(500);
    expect.soft(r.raw).toBe('{"success":false,"error":{"code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}');
    expect.soft(allLogs()).not.toContain(G);
  });
  it('G81 link: a SyntaxError quoting provider bytes -> token in no log line', async () => {
    const r = await link(() => new SyntaxError(`Unexpected token '<', "<html>${G}"... is not valid JSON`));
    expect.soft(r.status).toBe(500);
    expect.soft(allLogs()).not.toContain(G);
  });
  it('G81 link: thrown string -> 500, string not in log', async () => {
    const r = await link(() => `raw-${G}`);
    expect.soft(r.status).toBe(500);
    expect.soft(allLogs()).not.toContain(G);
  });
  it('G81 link: hostile Proxy stays a 500', async () => {
    const hostile = new Proxy(new Error('hostile'), { get(t, p) { if (p === 'name' || p === 'message') throw new Error('trap'); return Reflect.get(t, p); } });
    const r = await link(() => hostile);
    expect([r.status, r.code]).toEqual([500, 'INTERNAL_ERROR']);
  });
});
