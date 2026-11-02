/**
 * =============================================================================
 * KS-1470 — a connector JWT presented as a Bearer is refused at the front door,
 * not only inside `authenticateToken`
 * =============================================================================
 * KS-1198 refuses a verified `type: 'connector'` JWT presented as `Authorization:
 * Bearer`, but only inside `authenticateToken`. A mount that does not use it still
 * forwards the header to the upstream verbatim (`/api/verification`, `/api/v2/verification`,
 * `/api/presentations/verify`, `/api/documents/:id/sig-json`, `/api/auth/*`, `/api/sessions`,
 * the gateway-internal `/originate/` mount). The upstreams' shared `authenticate()` verifies the
 * signature only, so there the connector JWT is an ordinary principal and skips the gates only the
 * `x-api-key` branch sets up.
 *
 * Exploiting it needs a signed connector JWT, which only the gateway mints from a validated key and
 * nothing client-side holds: a defence-in-depth gap on the same class as KS-1198, not an open door.
 *
 * The fix is ONE earlier point that every mount passes through, with the same 401 body and the same
 * structured warning as KS-1198. The trigger is unchanged: the SIGNED `type` claim, checked only after
 * the signature verifies. The gateway's own `x-api-key` flow sets `Authorization: Bearer <connector JWT>`
 * itself AFTER that point, so it must keep working.
 *
 * What is measured here is the real app over HTTP against one recording upstream. The question asked of
 * every request is the one that matters: did the upstream receive the connector JWT the caller sent? Each
 * request carries its OWN token, so a leak is attributed to the mount that made it.
 * =============================================================================
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import jwt from 'jsonwebtoken';
import { generateKeyPairSync } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { AddressInfo } from 'node:net';
import { parse as parseYaml } from 'yaml';

// The real app boots over HTTP below. Its DB is a stub, as in the KS-1215 production recipe: the audit
// middleware and a few gateway-local routes read it, and neither is under test here.
vi.mock('../db', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
});

const EXPECTED_CELLS = 20;
let CELLS_RUN = 0;

const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
const TENANT = 'a0000000-0000-4000-8000-000000001470';
const VALID_KEY = 'sk_ks1470_valid_key_000001';
const SPEC = resolve(__dirname, '../../../../docs/openapi/secuura-api.yaml');

type Hit = { method: string; url: string; authorization: string | null };
const hits: Hit[] = [];
const MINTED: string[] = [];
/** Every connector JWT this file has handed a caller, token -> the request it was made for. */
const issued = new Map<string, string>();
let seq = 0;

function sign(claims: Record<string, unknown>, key: string = PRIV): string {
  return jwt.sign(
    { userId: 'u-ks1470', email: 'u@ks1470.test', role: 'ISSUER', tenantId: TENANT, verificationLevel: 'BASIC', ...claims },
    key,
    { algorithm: 'RS256', expiresIn: '10m' },
  );
}
/** A signed connector JWT of the shape auth mints, UNIQUE per call so a leak names the request that made it. */
function connectorJwt(label: string, extra: Record<string, unknown> = {}): string {
  seq += 1;
  const token = sign({
    userId: `connector:ks1470-${seq}`, email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key',
    type: 'connector', scopes: ['documents:write'], organizationId: 'org-ks1470', ...extra,
  });
  issued.set(token, label);
  return token;
}
const humanBearer = (): string => 'Bearer ' + sign({});
const tokenOf = (h: Hit): string | null => (h.authorization?.startsWith('Bearer ') ? h.authorization.slice('Bearer '.length) : null);

function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
}
async function listen(server: http.Server): Promise<string> {
  await new Promise<void>((resolveListen) => server.listen(0, '127.0.0.1', () => resolveListen()));
  return `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}
async function closeServer(server: http.Server | undefined): Promise<void> {
  if (!server) return;
  server.closeAllConnections();
  await new Promise<void>((r) => server.close(() => r()));
}

/** One upstream for every service: key validation, the connector-token exchange, and a recorder for everything else. */
function createUpstream(): http.Server {
  return http.createServer(async (req, res) => {
    const body = await readBody(req);
    const json = (status: number, payload: unknown) => { res.writeHead(status, { 'content-type': 'application/json' }); res.end(JSON.stringify(payload)); };
    const url = req.url || '';
    if (url === '/api/keys/validate') {
      const ok = (JSON.parse(body || '{}') as { key?: string }).key === VALID_KEY;
      return json(200, ok
        ? { data: { valid: true, connectorId: 'ks1470-conn', scopes: ['documents:read', 'documents:write'], organizationId: 'org-ks1470', tenantId: TENANT, rateLimit: 1000, rateLimitWindow: 60 } }
        : { data: { valid: false } });
    }
    if (url === '/internal/connector-token') {
      if ((JSON.parse(body || '{}') as { apiKey?: string }).apiKey !== VALID_KEY) return json(401, { success: false });
      const token = sign({ userId: 'connector:ks1470-minted', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector' });
      MINTED.push(token);
      return json(200, { success: true, data: { token, expiresIn: 600 } });
    }
    if (url.startsWith('/.well-known/')) return json(404, {});
    hits.push({ method: req.method || '', url, authorization: (req.headers.authorization as string | undefined) ?? null });
    return json(200, { success: true, data: { recorder: true } });
  });
}

const SERVICES = ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM',
  'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET'];

type Warn = unknown[];
const warns: Warn[] = [];
async function bootApp(upstreamUrl: string): Promise<{ server: http.Server; url: string }> {
  for (const name of SERVICES) vi.stubEnv(`${name}_SERVICE_URL`, upstreamUrl);
  vi.stubEnv('TENANT_PROVISIONING_URL', upstreamUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  delete process.env.JWT_JWKS_URL;
  vi.resetModules();
  // The logger is imported AFTER the reset and BEFORE the app, so the spy sits on the instance the app uses.
  const { logger } = await import('../utils/logger');
  vi.spyOn(logger, 'warn').mockImplementation(((...a: unknown[]) => { warns.push(a); return logger; }) as never);
  vi.spyOn(console, 'warn').mockImplementation(() => undefined);
  vi.spyOn(console, 'error').mockImplementation(() => undefined);
  const app = (await import('../index')).default;
  const server = http.createServer(app as http.RequestListener);
  return { server, url: await listen(server) };
}

type Res = { status: number; code: string | null; message: string; location: string | null };
function send(base: string, method: string, path: string, headers: Record<string, string> = {}): Promise<Res> {
  return new Promise((resolveSend, reject) => {
    const target = new URL(base);
    const withBody = method === 'POST' || method === 'PUT' || method === 'PATCH';
    const payload = withBody ? '{}' : '';
    const h: Record<string, string> = withBody ? { 'content-type': 'application/json', 'content-length': String(Buffer.byteLength(payload)), ...headers } : { ...headers };
    const req = http.request({ hostname: target.hostname, port: target.port, path, method, agent: false, headers: h }, (res) => {
      const c: Buffer[] = [];
      res.on('data', (d: Buffer) => c.push(d));
      res.on('end', () => {
        let code: string | null = null; let message = '';
        try { const j = JSON.parse(Buffer.concat(c).toString()); code = j?.error?.code ?? null; message = String(j?.error?.message ?? ''); } catch { /* non-JSON body */ }
        resolveSend({ status: res.statusCode ?? 0, code, message, location: (res.headers.location as string | undefined) ?? null });
      });
    });
    req.setTimeout(20000, () => req.destroy(new Error(`no response from ${method} ${path} within 20 s`)));
    req.on('error', reject);
    req.end(payload);
  });
}
const settle = (ms = 150) => new Promise<void>((r) => setTimeout(r, ms));

/** The connector refusal, exactly as KS-1198 answers it. */
const isRefusal = (r: Res): boolean => r.status === 401 && r.code === 'UNAUTHORIZED' && r.message.includes('x-api-key');

/** Send ONE request that carries a fresh connector JWT as its Bearer; report what the caller got and what the upstream saw of it. */
async function sendConnector(base: string, method: string, path: string, extraHeaders: Record<string, string> = {}): Promise<{ res: Res; forwarded: Hit[]; token: string }> {
  const label = `${method} ${path}`;
  const token = connectorJwt(label);
  const mark = hits.length;
  const res = await send(base, method, path, { authorization: 'Bearer ' + token, ...extraHeaders });
  await settle(60);
  return { res, forwarded: hits.slice(mark).filter((h) => tokenOf(h) === token), token };
}

async function pool<T, R>(items: T[], size: number, fn: (t: T) => Promise<R>): Promise<R[]> {
  const out: R[] = new Array(items.length);
  let next = 0;
  await Promise.all(Array.from({ length: size }, async () => {
    for (;;) { const n = next++; if (n >= items.length) return; out[n] = await fn(items[n]); }
  }));
  return out;
}

type Op = { method: string; path: string };
/** Every operation the published spec declares, with each `{param}` filled. */
function specOps(): Op[] {
  const spec = parseYaml(readFileSync(SPEC, 'utf8')) as { paths: Record<string, Record<string, unknown>> };
  const ops: Op[] = [];
  for (const [p, item] of Object.entries(spec.paths)) {
    for (const m of Object.keys(item)) {
      if (['get', 'post', 'put', 'patch', 'delete'].includes(m)) ops.push({ method: m.toUpperCase(), path: p.replace(/\{[^}]+\}/g, 'ks1470') });
    }
  }
  return ops;
}
/** Mounts the spec does not list: the gateway-internal originate mount, a webhook, the demo and download surfaces, health. */
const UNSPEC_MOUNTS: Op[] = [
  { method: 'POST', path: '/originate/api/documents' },
  { method: 'GET', path: '/originate/api/documents/ks1470' },
  { method: 'POST', path: '/webhooks/stripe' },
  { method: 'GET', path: '/demo-api/ks1470' },
  { method: 'POST', path: '/api/logs' },
  { method: 'GET', path: '/api/downloads/ks1470' },
  { method: 'GET', path: '/health' },
];
/** The mounts the Opus gate on #1470 measured forwarding a connector Bearer, plus the gateway-internal one. */
const NAMED_MOUNTS: Array<[string, Op]> = [
  ['/api/v2/verification', { method: 'POST', path: '/api/v2/verification/verify' }],
  ['/api/verification', { method: 'POST', path: '/api/verification/verify' }],
  ['/api/presentations/verify', { method: 'POST', path: '/api/presentations/verify' }],
  ['/api/documents/:id/sig-json', { method: 'GET', path: '/api/documents/ks1470/sig-json' }],
  ['/api/auth/*', { method: 'POST', path: '/api/auth/logout' }],
  ['/api/sessions', { method: 'GET', path: '/api/sessions' }],
  ['/originate/ (gateway-internal)', { method: 'POST', path: '/originate/api/documents' }],
];

let upstream: http.Server | undefined;
let upstreamUrl = '';
beforeAll(async () => {
  expect(PRIV, 'vitest.setup.ts provisioned a throwaway RS256 private key').toBeTruthy();
  upstream = createUpstream();
  upstreamUrl = await listen(upstream);
});
afterAll(async () => { await closeServer(upstream); vi.restoreAllMocks(); vi.unstubAllEnvs(); });

const refusalWarns = (): Warn[] => warns.filter((w) => JSON.stringify(w).includes('CONNECTOR_JWT_AS_BEARER_REFUSED'));

describe('KS-1470 the real app, NODE_ENV=test — a connector JWT as a Bearer never reaches an upstream', () => {
  let gateway: { server: http.Server; url: string } | undefined;
  beforeAll(async () => {
    vi.stubEnv('NODE_ENV', 'test');
    gateway = await bootApp(upstreamUrl);
  }, 60000);
  afterAll(async () => { await closeServer(gateway?.server); });

  it('RED KS-1470 A — EVERY operation the spec declares, and the mounts it does not list, answers a connector Bearer with the 401 refusal and forwards NOTHING', async () => {
    CELLS_RUN += 1;
    const ops = [...specOps(), ...UNSPEC_MOUNTS];
    expect(ops.length, 'CONTROL: the corpus is the real spec (346 operations) plus the unlisted mounts, not an empty list').toBeGreaterThan(340);
    const mark = hits.length;
    const results = await pool(ops, 8, async (op) => {
      const label = `${op.method} ${op.path}`;
      const token = connectorJwt(label);
      const res = await send(gateway!.url, op.method, op.path, { authorization: 'Bearer ' + token });
      return { label, res };
    });
    await settle(400);
    const leaked = hits.slice(mark).filter((h) => { const t = tokenOf(h); return t !== null && issued.has(t); })
      .map((h) => `${issued.get(tokenOf(h) as string)} -> upstream saw it on ${h.method} ${h.url}`).sort();
    const notRefused = results.filter((r) => !isRefusal(r.res)).map((r) => `${r.label} -> ${r.res.status} ${r.res.code ?? ''}`).sort();
    // The offenders go in the assertion MESSAGE: vitest truncates a long array or string it formats itself ("…(47)").
    expect(leaked.length, `${leaked.length} request(s) delivered the caller's connector JWT to an upstream:\n${leaked.join('\n')}`).toBe(0);
    expect(notRefused.length, `${notRefused.length} request(s) were not refused with the connector 401:\n${notRefused.join('\n')}`).toBe(0);
  }, 120000);

  for (const [name, op] of NAMED_MOUNTS) {
    it(`RED KS-1470 B — ${name}: ${op.method} ${op.path} refuses a connector Bearer 401 and the upstream never sees it`, async () => {
      CELLS_RUN += 1;
      const { res, forwarded } = await sendConnector(gateway!.url, op.method, op.path);
      expect([res.status, res.code, res.message.includes('x-api-key'), forwarded.length]).toEqual([401, 'UNAUTHORIZED', true, 0]);
    });
  }

  it('RED KS-1470 C — a VALID x-api-key beside a connector Bearer is refused too: the key does not make the Bearer harmless on a mount that never validates it', async () => {
    CELLS_RUN += 1;
    const sig = await sendConnector(gateway!.url, 'GET', '/api/documents/ks1470/sig-json', { 'x-api-key': VALID_KEY });
    const req = await sendConnector(gateway!.url, 'GET', '/api/credentials/ks1470', { 'x-api-key': VALID_KEY });
    expect([sig.res.status, sig.forwarded.length, req.res.status, req.forwarded.length]).toEqual([401, 0, 401, 0]);
    expect(isRefusal(sig.res) && isRefusal(req.res)).toBe(true);
  });

  it('RED KS-1470 D — the path spelling does not matter: upper-case, /api/v1/ and mixed-case spellings of an unauthenticated mount are refused too', async () => {
    CELLS_RUN += 1;
    const spellings = ['/API/documents/ks1470/sig-json', '/api/v1/documents/ks1470/sig-json', '/API/V1/documents/ks1470/sig-json', '/api/documents/ks1470/sig-json/'];
    const got = [];
    for (const p of spellings) { const r = await sendConnector(gateway!.url, 'GET', p); got.push([p, r.res.status, r.forwarded.length]); }
    expect(JSON.stringify(got), `each spelling as [path, status, upstream hits]: ${JSON.stringify(got)}`).toBe(JSON.stringify(spellings.map((p) => [p, 401, 0])));
  });

  it('RED KS-1470 E — each refusal logs ONE structured warning that names x-api-key, the connector, the method and the full path, and never the token', async () => {
    CELLS_RUN += 1;
    warns.length = 0;
    const { token } = await sendConnector(gateway!.url, 'GET', '/api/documents/ks1470/sig-json');
    const first = refusalWarns();
    expect(first, 'one warning for one refusal').toHaveLength(1);
    const line = JSON.stringify(first[0]);
    expect(line).toContain('x-api-key');
    expect(line).toContain(`connector:ks1470-${seq}`);
    expect(line).toContain('/api/documents/ks1470/sig-json');
    expect(line).toContain('GET');
    expect(line, 'the credential itself is never logged').not.toContain(token);
    await sendConnector(gateway!.url, 'GET', '/api/documents/ks1470/sig-json');
    expect(refusalWarns(), 'a second refusal logs a second warning').toHaveLength(2);
  });

  it('GREEN KS-1470 F — on a mount that DOES use authenticateToken the refusal is still logged exactly ONCE (the front door answers; the inner check is not reached to log it again)', async () => {
    CELLS_RUN += 1;
    warns.length = 0;
    const { res } = await sendConnector(gateway!.url, 'GET', '/api/credentials/ks1470');
    expect(isRefusal(res)).toBe(true);
    expect(refusalWarns()).toHaveLength(1);
  });

  it('GREEN KS-1470 G — an ordinary human token is NOT refused on any named mount, and it reaches the upstream on the mounts that forward (the observation channel works)', async () => {
    CELLS_RUN += 1;
    warns.length = 0;
    const bearer = humanBearer();
    const refused: string[] = [];
    const reached: string[] = [];
    for (const [name, op] of NAMED_MOUNTS) {
      const mark = hits.length;
      const r = await send(gateway!.url, op.method, op.path, { authorization: bearer });
      await settle(60);
      if (isRefusal(r)) refused.push(name);
      if (hits.slice(mark).some((h) => h.authorization === bearer)) reached.push(name);
    }
    expect(refused, 'a human token is never refused by the connector check').toEqual([]);
    expect(refusalWarns()).toHaveLength(0);
    expect(reached.length, 'CONTROL: the recorder does see a Bearer when one is forwarded, so a 0 above means refused, not unobserved').toBeGreaterThanOrEqual(3);
  });

  it('GREEN KS-1470 H — the gateway\'s own x-api-key flow is unaffected: a valid key is exchanged and the upstream receives the connector JWT the GATEWAY minted', async () => {
    CELLS_RUN += 1;
    warns.length = 0;
    const mark = hits.length;
    const r = await send(gateway!.url, 'GET', '/api/credentials/ks1470-own-flow', { 'x-api-key': VALID_KEY });
    await settle(100);
    const got = hits.slice(mark).filter((h) => h.url === '/api/credentials/ks1470-own-flow');
    expect(r.status).toBe(200);
    // The gateway caches the minted Bearer per key (8 min), so an earlier cell may have done the exchange: assert on what reached the upstream.
    expect(MINTED.length, 'CONTROL: the gateway has minted a connector JWT from the key').toBeGreaterThan(0);
    expect(got).toHaveLength(1);
    expect(MINTED, 'the Bearer the upstream received is one the GATEWAY minted').toContain(tokenOf(got[0]));
    expect(issued.has(tokenOf(got[0]) as string), 'and it is not one a caller sent').toBe(false);
    expect((jwt.decode(tokenOf(got[0]) as string) as { type?: string }).type).toBe('connector');
    expect(refusalWarns(), 'the gateway\'s own Bearer is never logged as a refused one').toHaveLength(0);
  });

  it('GREEN KS-1470 I — the trigger is the SIGNED type claim, not the role: a role:connector token with no type claim is not refused', async () => {
    CELLS_RUN += 1;
    const mark = hits.length;
    const bearer = 'Bearer ' + sign({ role: 'connector', userId: 'connector:ks1470-notype' });
    const r = await send(gateway!.url, 'GET', '/api/documents/ks1470/sig-json', { authorization: bearer });
    await settle(60);
    expect([r.status, isRefusal(r), hits.slice(mark).filter((h) => h.authorization === bearer).length]).toEqual([200, false, 1]);
  });

  it('GREEN KS-1470 J — a type:connector token with a BAD signature is not acted on: not refused as a connector JWT, not logged as one', async () => {
    CELLS_RUN += 1;
    warns.length = 0;
    const { privateKey } = generateKeyPairSync('rsa', { modulusLength: 2048 });
    const forged = jwt.sign({ userId: 'connector:ks1470-forged', role: 'connector', type: 'connector', tenantId: TENANT }, privateKey.export({ type: 'pkcs1', format: 'pem' }) as string, { algorithm: 'RS256', expiresIn: '10m' });
    const r = await send(gateway!.url, 'GET', '/api/documents/ks1470/sig-json', { authorization: 'Bearer ' + forged });
    expect(isRefusal(r), 'only a token whose signature verified is treated as a connector credential').toBe(false);
    expect(refusalWarns()).toHaveLength(0);
  });

  // KS-1503 Minor 1: cell J asserts only "not the connector refusal", so it passes whether an unverifiable Bearer is forwarded,
  // answered 401, or answered 500. If the front door's `catch` ever rethrew, every forged, expired or malformed Bearer would
  // answer 500 on every route and J would stay green. The next two cells say what the Bearer DOES get; the third keeps the
  // guard itself pinned. The forged and expired tokens below carry type:connector on purpose: that is the claim the guard acts on.
  const unverifiable = {
    forged: (): string => {
      const { privateKey } = generateKeyPairSync('rsa', { modulusLength: 2048 });
      return jwt.sign({ userId: 'connector:ks1503-forged', role: 'connector', type: 'connector', tenantId: TENANT }, privateKey.export({ type: 'pkcs1', format: 'pem' }) as string, { algorithm: 'RS256', expiresIn: '10m' });
    },
    expired: (): string =>
      jwt.sign({ userId: 'connector:ks1503-expired', role: 'connector', type: 'connector', tenantId: TENANT, exp: Math.floor(Date.now() / 1000) - 3600 }, PRIV, { algorithm: 'RS256' }),
  };

  it('RED KS-1503 M1 - a type:connector token with a BAD signature goes on to the mount that forwards it: 200 and ONE upstream hit, not a 500', async () => {
    CELLS_RUN += 1;
    const bearer = 'Bearer ' + unverifiable.forged();
    const mark = hits.length;
    const r = await send(gateway!.url, 'GET', '/api/documents/ks1503/sig-json', { authorization: bearer });
    await settle(60);
    expect([r.status, isRefusal(r), hits.slice(mark).filter((h) => h.authorization === bearer).length]).toEqual([200, false, 1]);
  });

  it('RED KS-1503 M2 - an EXPIRED type:connector token (good signature) goes on the same way: 200 and ONE upstream hit, not a 500', async () => {
    CELLS_RUN += 1;
    const bearer = 'Bearer ' + unverifiable.expired();
    const mark = hits.length;
    const r = await send(gateway!.url, 'GET', '/api/documents/ks1503/sig-json', { authorization: bearer });
    await settle(60);
    expect([r.status, isRefusal(r), hits.slice(mark).filter((h) => h.authorization === bearer).length]).toEqual([200, false, 1]);
  });

  it('CONTROL KS-1503 M3 - a type:connector token with a GOOD signature is still refused 401 with the connector refusal and 0 upstream hits (the guard itself is unchanged)', async () => {
    CELLS_RUN += 1;
    const { res, forwarded } = await sendConnector(gateway!.url, 'GET', '/api/documents/ks1503/sig-json');
    expect([res.status, isRefusal(res), forwarded.length]).toEqual([401, true, 0]);
  });
});

describe('KS-1470 the real app, NODE_ENV=production — the same refusal, with the 307 and CSRF live', () => {
  let gateway: { server: http.Server; url: string } | undefined;
  beforeAll(async () => {
    // The ks871 production recipe: a stub CSRF secret and DB / Redis URLs on a closed loopback port (`../db` is mocked above).
    vi.stubEnv('NODE_ENV', 'production');
    vi.stubEnv('CSRF_SECRET', 'ks1470-stub-csrf-not-a-real-secret');
    vi.stubEnv('DATABASE_URL', 'postgres://ks1470:ks1470@127.0.0.1:1/ks1470');
    vi.stubEnv('REDIS_URL', 'redis://127.0.0.1:1');
    vi.stubEnv('ENABLE_TEST_TOKENS', '');
    vi.stubEnv('ENABLE_MOCK_ENDPOINTS', '');
    gateway = await bootApp(upstreamUrl);
  }, 60000);
  afterAll(async () => { await closeServer(gateway?.server); vi.unstubAllEnvs(); });

  it('RED KS-1470 K — production: the unversioned path still 307s (the mode is live), and on /api/v1/ a connector Bearer is refused 401 on a GET and a POST with 0 upstream hits', async () => {
    CELLS_RUN += 1;
    const unversioned = await sendConnector(gateway!.url, 'GET', '/api/documents/ks1470/sig-json');
    expect([unversioned.res.status, unversioned.forwarded.length], 'CONTROL: production mode is live, the unversioned path redirects and forwards nothing').toEqual([307, 0]);
    const get = await sendConnector(gateway!.url, 'GET', '/api/v1/documents/ks1470/sig-json');
    const post = await sendConnector(gateway!.url, 'POST', '/api/v1/verification/verify');
    expect([get.res.status, get.forwarded.length, post.res.status, post.forwarded.length]).toEqual([401, 0, 401, 0]);
    expect(isRefusal(get.res) && isRefusal(post.res)).toBe(true);
  });
});

describe('KS-1470 completeness', () => {
  it('KS-1470 COMPLETENESS — every graded cell above actually ran', () => { expect(CELLS_RUN).toBe(EXPECTED_CELLS); });
});
