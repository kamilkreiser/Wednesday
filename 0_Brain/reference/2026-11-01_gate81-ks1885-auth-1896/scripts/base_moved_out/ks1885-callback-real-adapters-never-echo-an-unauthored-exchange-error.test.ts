/**
 * =============================================================================
 * KS-1885 — the social sign-in callback answers a constant for any exchange error our own code did not write
 * =============================================================================
 * `GET /api/auth/social/:provider/callback` put the exchange error's message into its 400 unless it was a SyntaxError
 * (KS 1791). A provider token answer whose `access_token` holds a newline makes `fetch` throw a TypeError that QUOTES
 * the whole `Bearer <token>` header (github, google, linkedin, microsoft_personal: F1), and a JSON `null` answer echoed
 * V8's internal text (all six adapters: F2). The error handler also logs the message, so the token reached the log too.
 *
 * Now an AppError's text and the adapters' own exact texts pass; everything else answers the KS 1791 constant
 * `OAuth authentication failed: the provider answer could not be read`, with the status unchanged (400). The log names
 * the provider and an identifier-shaped error name only.
 *
 * Harness (the ks1240b shape): the REAL adapter classes through the REAL routes. Each adapter's provider URL is
 * rewritten to one in-process stub HTTP server on 127.0.0.1, and the real `fetch` runs with the adapter's own init,
 * so the header TypeError is the runtime's own. No real provider and no external network. The logger is captured.
 *
 * Cells marked RED fail at the untouched base; CONTROL and PIN cells pass at the base by design (facebook carries the
 * token in the URL query, the SyntaxError path, the adapters' own texts, the success path) and must still pass.
 * =============================================================================
 */
import { describe, it, expect, beforeAll, beforeEach, afterAll, vi } from 'vitest';
import http from 'node:http';
import express from 'express';
import type { AddressInfo } from 'node:net';
import { FacebookProvider } from '../providers/social/facebook';
import type { SocialProvider } from '../providers/social/types';

const { silentLogger, redisStore, CONFIG } = vi.hoisted(() => ({
  silentLogger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() },
  redisStore: new Map<string, string>(),
  CONFIG: { clientId: 'cid-ks1885', clientSecret: 'secret-ks1885', callbackUrl: 'https://app.test/cb', enabled: true },
}));
vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));
vi.mock('../services/session', () => ({
  createSession: vi.fn(async () => ({ id: 'sess-ks1885' })),
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
  generateTokenPair: vi.fn(() => ({ accessToken: 'MINTED_KS1885', refreshToken: 'MINTED_KS1885_R', expiresIn: 900 })),
  verifyAccessToken: vi.fn(() => ({})),
}));
const passthrough = () => (_r: unknown, _s: unknown, n: () => void) => n();
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
  const classes: Record<string, new (c: typeof CONFIG) => SocialProvider> = {
    github: real.GitHubProvider as never, google: real.GoogleProvider as never, linkedin: real.LinkedInProvider as never,
    apple: real.AppleProvider as never, facebook: real.FacebookProvider as never, microsoft_personal: real.MicrosoftPersonalProvider as never,
  };
  class RealProvidersFactory {
    get(name: string) { return classes[name] ? new classes[name](CONFIG) : undefined; }
    getEnabled() { return Object.keys(classes); }
    has(n: string) { return n in classes; }
    isValidProvider(n: string) { return n in classes; }
  }
  return { ...real, SocialProviderFactory: RealProvidersFactory };
});

// A made-up marker, never a real token. It sits on both sides of the newline so either half would be seen.
const SENTINEL = 'KS1885SENTINELq7w2e9';
const NEWLINE_TOKEN = `tok-${SENTINEL}\n${SENTINEL}`;
const PROVIDER_MARKER = 'KS1885PROVIDERBYTESx4';
const CONSTANT = 'OAuth authentication failed: the provider answer could not be read';

type Family = { name: string; label: string; token: string; profile?: string };
const FAMILIES: Family[] = [
  { name: 'github', label: 'GitHub', token: 'github.com/login/oauth/access_token', profile: 'api.github.com/user' },
  { name: 'google', label: 'Google', token: 'oauth2.googleapis.com/token', profile: 'www.googleapis.com/oauth2/v2/userinfo' },
  { name: 'linkedin', label: 'LinkedIn', token: 'www.linkedin.com/oauth/v2/accessToken', profile: 'api.linkedin.com/v2/userinfo' },
  { name: 'microsoft_personal', label: 'Microsoft', token: 'login.microsoftonline.com/consumers/oauth2/v2.0/token', profile: 'graph.microsoft.com/v1.0/me' },
  { name: 'facebook', label: 'Facebook', token: 'graph.facebook.com/v19.0/oauth/access_token', profile: 'graph.facebook.com/v19.0/me' },
  { name: 'apple', label: 'Apple', token: 'appleid.apple.com/auth/token' },
];
const BEARER = FAMILIES.filter((f) => ['github', 'google', 'linkedin', 'microsoft_personal'].includes(f.name));
const WITH_PROFILE = FAMILIES.filter((f) => f.profile);
// What each adapter throws when its profile call is answered 401 (read from the adapters at develop d7691f35).
const PROFILE_REFUSED: Record<string, string> = {
  github: 'Failed to fetch GitHub user profile',
  google: 'Failed to fetch Google user profile (HTTP 401)',
  linkedin: 'Failed to fetch LinkedIn user profile',
  microsoft_personal: 'Failed to fetch Microsoft user profile (HTTP 401)',
  facebook: 'Failed to fetch Facebook user profile',
};

type Mode = 'ok' | 'newlineToken' | 'nullBody' | 'html200' | 'empty200' | 'unauth' | 'appleBadIdToken';
const mode: Record<string, Mode> = {};
const realFetch = globalThis.fetch;
const appleIdToken = `h.${Buffer.from(JSON.stringify({ sub: 'apple-1', email: 'a@ks1885.test', email_verified: true })).toString('base64')}.s`;
const OK_BODY: Record<string, unknown> = {
  'github.com/login/oauth/access_token': { access_token: 'tok' },
  'api.github.com/user': { id: 1, email: '', name: 'K S', login: 'ks' },
  'api.github.com/user/emails': [{ email: 'g@ks1885.test', primary: true, verified: true }],
  'oauth2.googleapis.com/token': { access_token: 'tok' },
  'www.googleapis.com/oauth2/v2/userinfo': { id: 'g-1', email: 'g@ks1885.test', verified_email: true },
  'www.linkedin.com/oauth/v2/accessToken': { access_token: 'tok' },
  'api.linkedin.com/v2/userinfo': { sub: 'l-1', email: 'l@ks1885.test', email_verified: true },
  'appleid.apple.com/auth/token': { id_token: appleIdToken },
  'graph.facebook.com/v19.0/oauth/access_token': { access_token: 'tok' },
  'graph.facebook.com/v19.0/me': { id: 'f-1', email: 'f@ks1885.test' },
  'login.microsoftonline.com/consumers/oauth2/v2.0/token': { access_token: 'tok' },
  'graph.microsoft.com/v1.0/me': { id: 'm-1', mail: 'm@ks1885.test' },
};

let stub: http.Server | undefined;
let stubUrl = '';
let app: http.Server | undefined;
let appUrl = '';

async function listen(server: http.Server): Promise<string> {
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
  return `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}
async function closeServer(server: http.Server | undefined): Promise<void> {
  if (!server) return;
  server.closeAllConnections();
  await new Promise<void>((r) => server.close(() => r()));
}

beforeAll(async () => {
  stub = http.createServer((req, res) => {
    req.resume();
    req.on('end', () => {
      const key = (req.url || '').slice(1).split('?')[0];
      const m = mode[key] ?? 'ok';
      const json = (status: number, body: string) => { res.writeHead(status, { 'content-type': 'application/json' }); res.end(body); };
      if (m === 'newlineToken') return json(200, JSON.stringify({ access_token: NEWLINE_TOKEN }));
      if (m === 'nullBody') return json(200, 'null');
      if (m === 'empty200') return json(200, '{}');
      if (m === 'unauth') return json(401, JSON.stringify({ message: 'Bad credentials' }));
      if (m === 'html200') { res.writeHead(200, { 'content-type': 'text/html' }); res.end(`<html>${PROVIDER_MARKER}</html>`); return; }
      if (m === 'appleBadIdToken') return json(200, JSON.stringify({ id_token: `h.${Buffer.from(`<html>${PROVIDER_MARKER}`).toString('base64')}.s` }));
      json(200, JSON.stringify(OK_BODY[key] ?? {}));
    });
  });
  stubUrl = await listen(stub);
  vi.spyOn(globalThis, 'fetch').mockImplementation(((input: string | URL | Request, init?: RequestInit) => {
    const u = new URL(String(input));
    return realFetch(`${stubUrl}/${u.host}${u.pathname}${u.search}`, init);
  }) as typeof fetch);

  const { authRoutes } = await import('../routes/auth');
  const { errorHandler } = await import('../middleware/errorHandler');
  const ex = express();
  ex.use(express.json());
  ex.use('/api/auth', authRoutes);
  ex.use(errorHandler);
  app = http.createServer(ex as http.RequestListener);
  appUrl = await listen(app);
}, 60000);

afterAll(async () => {
  vi.restoreAllMocks();
  await closeServer(app);
  await closeServer(stub);
});

beforeEach(() => {
  for (const k of Object.keys(mode)) delete mode[k];
  redisStore.clear();
  for (const fn of Object.values(silentLogger)) fn.mockClear();
});

type Res = { status: number; code: string | null; message: string | null; raw: string };
function call(p: string): Promise<Res> {
  return new Promise((resolve, reject) => {
    const target = new URL(appUrl);
    const req = http.request({ hostname: target.hostname, port: target.port, path: p, method: 'GET', agent: false }, (res) => {
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
    req.end();
  });
}

/** Run one sign-in for a provider: mint a real state through the initiate route, then hit the callback with it. */
async function signIn(provider: string): Promise<Res> {
  const init = await call(`/api/auth/social/${provider}`);
  const state = JSON.parse(init.raw).state as string;
  return call(`/api/auth/social/${provider}/callback?code=c-ks1885&state=${encodeURIComponent(state)}`);
}

/** Every logger call at every level, serialised, so a marker anywhere in any argument is found. */
const allLogs = (): string => JSON.stringify(Object.fromEntries(Object.entries(silentLogger).map(([k, fn]) => [k, fn.mock.calls])));
const exchangeWarns = () => silentLogger.warn.mock.calls.filter((c) => c[0] === 'Social callback: the provider code exchange failed');

describe('KS-1885 F1: a newline in access_token never puts the token in the 400 or in the log', () => {
  it.each(BEARER)('RED $name: the Bearer-header TypeError answers the constant, and no response byte or log line carries the token', async (f) => {
    mode[f.token] = 'newlineToken';
    const r = await signIn(f.name);
    // Soft: at the base every one of these fails and is reported, which shows each can see the leak.
    expect.soft([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', CONSTANT]);
    expect.soft(r.raw, 'the token is not anywhere in the serialised body').not.toContain(SENTINEL);
    expect.soft(allLogs(), 'the token is not in any log line, at any level').not.toContain(SENTINEL);
    expect.soft(exchangeWarns().map((c) => c[1]), 'one warn names the provider and the class only').toEqual([{ provider: f.name, errorName: 'TypeError' }]);
  });

  it('CONTROL facebook: the token rides in the URL query, the runtime strips the newline, so the exchange resolves and nothing echoes', async () => {
    const fb = FAMILIES.find((f) => f.name === 'facebook')!;
    mode[fb.token] = 'newlineToken';
    const profile = await new FacebookProvider(CONFIG).exchangeCode('c-ks1885');
    expect(profile.providerId).toBe('f-1');
    const r = await signIn('facebook');
    expect(r.raw).not.toContain(SENTINEL);
    expect(r.status).toBe(200);
  });
});

describe('KS-1885 F2: a JSON null token answer answers the constant, not the runtime\'s internal text', () => {
  it.each(FAMILIES)('RED $name: null token answer -> 400 with the constant', async (f) => {
    mode[f.token] = 'nullBody';
    const r = await signIn(f.name);
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', CONSTANT]);
    expect(r.raw).not.toContain('Cannot read properties');
  });
});

describe('KS-1885 F4: the later stages are pinned too (the KS 1791 constant held there at the base already)', () => {
  it.each(WITH_PROFILE)('PIN $name: a non-JSON 200 at the profile stage answers the constant and none of the provider\'s bytes', async (f) => {
    mode[f.profile!] = 'html200';
    const r = await signIn(f.name);
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', CONSTANT]);
    expect(r.raw).not.toContain(PROVIDER_MARKER);
  });

  it('PIN github: a non-JSON 200 at the emails call answers the constant and none of the provider\'s bytes', async () => {
    mode['api.github.com/user/emails'] = 'html200';
    const r = await signIn('github');
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', CONSTANT]);
    expect(r.raw).not.toContain(PROVIDER_MARKER);
  });

  it('PIN apple: an id_token whose payload is not JSON answers the constant and none of its bytes', async () => {
    mode['appleid.apple.com/auth/token'] = 'appleBadIdToken';
    const r = await signIn('apple');
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', CONSTANT]);
    expect(r.raw).not.toContain(PROVIDER_MARKER);
  });
});

describe('KS-1885: the adapters\' own texts still reach the client unchanged, and so does a success', () => {
  it.each(WITH_PROFILE)('PIN $name: a 200 token answer with no access token keeps the adapter\'s own text', async (f) => {
    mode[f.token] = 'empty200';
    const r = await signIn(f.name);
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', `OAuth authentication failed: ${f.label} token exchange failed (no access token)`]);
  });

  it.each(WITH_PROFILE)('PIN $name: a refused profile call keeps the adapter\'s own text', async (f) => {
    mode[f.profile!] = 'unauth';
    const r = await signIn(f.name);
    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', `OAuth authentication failed: ${PROFILE_REFUSED[f.name]}`]);
  });

  it('CONTROL github: a normal sign-in still answers 200 and mints', async () => {
    const r = await signIn('github');
    expect(r.status).toBe(200);
    expect(r.raw).toContain('MINTED_KS1885');
  });
});
