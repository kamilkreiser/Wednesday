/**
 * =============================================================================
 * KS-1187 — the erasure door judges the canonical gdpr path
 * =============================================================================
 * The `/api/gdpr` wrapper collapsed `//` across the WHOLE req.url. Inside that
 * mount an absolute-form target keeps its `scheme://authority`, so
 * `http://h/erasures` became `http:/h/erasures`, the `/erasures` door never
 * matched, and the catch-all forwarded the erasure to originate for a connector
 * without `subjects:erase` (tier-1 QA gate on #1011, F-1011-4). Spellings such
 * as a percent-escaped letter, a dot segment or a `;param` passed the door the
 * same way (the #1011 round-2 gate).
 *
 * The wrapper now asks `erasureDoorVerdict` (routes/proxy.ts), the ONE function
 * these cells also use, whether the canonical path names the door, and refuses
 * a path it cannot canonicalise when that decides the door. Real-app cells use
 * the ks871 pattern: the app exported by index.ts, `../db` mocked, a recording
 * originate, connector Bearer tokens signed with vitest.setup.ts's RS256 key.
 *
 * Round 2 (tier-1 gate NO GO on #1019, F-1019-1): resolving `..` popped the door
 * segment, so `/erasures/..` was judged "not the door" and forwarded, while the
 * upstream routes the RAW path to `/erasures/:externalRef` with the reference
 * `..`. A `.` or `..` segment after a path that names the door is now refused.
 * Bare-app cells mount `createProxyRoutes` with a recording `authenticateToken`:
 * one pins that the case rule is read from the door's router (F-1019-2), one that
 * `req.url` is restored for the layer after the door (F-1019-3).
 * =============================================================================
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import express from 'express';
import type { NextFunction, Request, RequestHandler, Response } from 'express';
import jwt from 'jsonwebtoken';
import type { AddressInfo } from 'net';
import { erasureDoorVerdict } from '../routes/proxy';

vi.mock('../db', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
});

const seen: string[] = [];
let recorder: http.Server | undefined;
let recorderUrl = '';

async function listen(server: http.Server): Promise<string> {
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
  return `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}
async function closeServer(server: http.Server | undefined): Promise<void> {
  if (!server) return;
  server.closeAllConnections();
  await new Promise<void>((r) => server.close(() => r()));
}

type Res = { status: number; code: string | null; hits: string[] };
/** Sends `path` verbatim as the request target (absolute-form included) and returns the upstream lines it caused. */
function send(base: string, method: string, path: string, authorization: string): Promise<Res> {
  return new Promise((resolve, reject) => {
    const target = new URL(base);
    const before = seen.length;
    const body = method === 'GET' ? undefined : '{}';
    const headers: Record<string, string> = { authorization };
    if (body !== undefined) { headers['content-type'] = 'application/json'; headers['content-length'] = String(Buffer.byteLength(body)); }
    const req = http.request({ hostname: target.hostname, port: target.port, path, method, agent: false, headers }, (res) => {
      const c: Buffer[] = [];
      res.on('data', (d) => c.push(d));
      res.on('end', () => {
        let code: string | null = null;
        try { code = JSON.parse(Buffer.concat(c).toString())?.error?.code ?? null; } catch { /* non-JSON: code stays null */ }
        // Give a forwarded request time to land before reading the recorder.
        setTimeout(() => resolve({ status: res.statusCode ?? 0, code, hits: seen.slice(before) }), 50);
      });
    });
    req.on('error', reject);
    if (body !== undefined) req.end(body); else req.end();
  });
}

function connector(scopes: string[]): string {
  return 'Bearer ' + jwt.sign(
    // email as generateConnectorToken mints it: without it the proxy cannot set x-user-email and answers 500 (the KS-744 class).
    { userId: 'c0000000-0000-4000-8000-00000000118c', email: 'connector@secuura.io', role: 'connector', authMethod: 'api_key', scopes,
      tenantId: 'a0000000-0000-4000-8000-000000000001', organizationId: 'd0000000-0000-4000-8000-00000000118d', verificationLevel: 'BASIC' },
    process.env.__TEST_JWT_PRIVATE_PEM as string,
    { algorithm: 'RS256', expiresIn: '10m' },
  );
}
const WITHOUT_SCOPE = () => connector(['documents:read']);
const WITH_SCOPE = () => connector(['subjects:erase']);

async function bootApp(): Promise<{ server: http.Server; url: string }> {
  vi.resetModules();
  const app = (await import('../index')).default;
  const server = http.createServer(app as http.RequestListener);
  return { server, url: await listen(server) };
}

beforeAll(async () => {
  recorder = http.createServer((req, res) => {
    req.resume();
    req.on('end', () => {
      seen.push(`${req.method} ${req.url}`);
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end('{"recorder":true}');
    });
  });
  recorderUrl = await listen(recorder);
});

afterAll(async () => {
  await closeServer(recorder);
  vi.unstubAllEnvs();
});

describe('KS-1187: erasureDoorVerdict, the one canonicaliser', () => {
  const door = ['/erasures', '/erasures/abc', '/ERASURES', '/%65rasures', '/./erasures', '/erasures;x=1', '/x/../erasures', 'http://h/erasures', 'http://h/erasures/abc?x=1'];
  const notDoor = ['/consent/check', '/%63onsent/check', '/consent/%zz', '/', '/erasure/u-1'];
  const undetermined = ['/%zzrasures', '/../erasures', '/consent/../../erasures'];
  // Round 2: a dot segment once the path names the door. Resolving it would judge
  // a path express does not route (the upstream sees `/erasures/:externalRef`).
  const dotAfterDoor = [
    '/erasures/..', '/erasures/%2e%2e', '/erasures/.%2e', '/erasures/%2E%2E', '/erasures/..;x',
    '/erasures/%2e%2e%2fabc', '/erasures/../', '/erasures/.', '/erasures/abc/..', '/ERASURES/..',
    '/x/../erasures/..', 'http://h/erasures/..',
  ];
  // Controls: a dot INSIDE a segment is part of a reference, not a dot segment.
  const doorWithDots = ['/erasures/%2e%2e%3bx', '/erasures/..ref', '/erasures/a.b', '/erasures/abc.'];

  it.each(door)('names the door: %s', (p) => {
    expect(erasureDoorVerdict(p, false).verdict).toBe('door');
  });
  it.each(notDoor)('plainly not the door, forwarded as before: %s', (p) => {
    expect(erasureDoorVerdict(p, false).verdict).toBe('not-door');
  });
  it.each(undetermined)('cannot be canonicalised where it decides the door: %s', (p) => {
    expect(erasureDoorVerdict(p, false).verdict).toBe('undetermined');
  });
  it.each(dotAfterDoor)('🔴 a dot segment after the door is refused, never resolved to "not the door": %s', (p) => {
    expect(erasureDoorVerdict(p, false)).toEqual({ verdict: 'undetermined', canonicalPath: null });
  });
  it.each(doorWithDots)('control: a dot inside a reference is still the door: %s', (p) => {
    expect(erasureDoorVerdict(p, false).verdict).toBe('door');
  });
  it('honours a case-sensitive router: /ERASURES is not the door when case matters', () => {
    expect(erasureDoorVerdict('/ERASURES', true).verdict).toBe('not-door');
  });
  it('the dot rule uses the same case rule: under a case-sensitive router /ERASURES/.. is not the door, /erasures/.. is refused', () => {
    expect(erasureDoorVerdict('/ERASURES/..', true).verdict).toBe('not-door');
    expect(erasureDoorVerdict('/erasures/..', true).verdict).toBe('undetermined');
  });
  it('hands the door a canonical path', () => {
    expect(erasureDoorVerdict('http://h/x/..//%65rasures;v=2/abc?q=1', false)).toEqual({ verdict: 'door', canonicalPath: '/erasures/abc' });
  });
});

describe('KS-1187 real app, NODE_ENV=test — the door judges every spelling', () => {
  let gateway: { server: http.Server; url: string } | undefined;

  beforeAll(async () => {
    vi.stubEnv('NODE_ENV', 'test');
    vi.stubEnv('ORIGINATE_SERVICE_URL', recorderUrl);
    vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
    vi.stubEnv('SUBJECTS_ERASE_SCOPE_ENFORCED', 'true');
    delete process.env.JWT_JWKS_URL;
    gateway = await bootApp();
  }, 60000);

  afterAll(async () => { await closeServer(gateway?.server); });

  const refused: Array<[string, string, string]> = [
    ['absolute-form POST', 'POST', 'http://127.0.0.1/api/gdpr/erasures'],
    ['absolute-form status read', 'GET', 'http://127.0.0.1/api/gdpr/erasures/abc'],
    ['absolute-form, any host', 'POST', 'http://qa-anything.invalid/api/gdpr/erasures'],
    ['absolute-form v1', 'POST', 'http://127.0.0.1/api/v1/gdpr/erasures'],
    ['a percent-escaped letter', 'POST', '/api/gdpr/%65rasures'],
    ['a dot segment', 'POST', '/api/gdpr/./erasures'],
    ['a ;param', 'POST', '/api/gdpr/erasures;x=1'],
    ['v1 with a percent-escaped letter', 'POST', '/api/v1/gdpr/%65rasures'],
    ['a climbing dot segment', 'POST', '/api/gdpr/x/../erasures'],
    ['upper case (how the router compares)', 'POST', '/api/gdpr/ERASURES'],
  ];
  it.each(refused)('🔴 %s without subjects:erase is refused 403 at the door, nothing forwarded', async (_label, method, path) => {
    const r = await send(gateway!.url, method, path, WITHOUT_SCOPE());
    expect([r.status, r.hits]).toEqual([403, []]);
  });

  it.each([
    ['an undecodable escape where the door is decided', 'POST', '/api/gdpr/%zzrasures'],
    ['a dot segment that climbs out of the mount', 'POST', '/api/gdpr/../gdpr/erasures'],
  ])('🔴 %s is refused 400 NON_CANONICAL_PATH, nothing forwarded', async (_label, method, path) => {
    const r = await send(gateway!.url, method, path, WITH_SCOPE());
    expect([r.status, r.code, r.hits]).toEqual([400, 'NON_CANONICAL_PATH', []]);
  });

  // Round 2, F-1019-1: at the round-1 head each of these was 200 with one upstream hit.
  it.each([
    '/api/gdpr/erasures/..',
    '/api/gdpr/erasures/%2e%2e',
    '/api/gdpr/erasures/.%2e',
    '/api/gdpr/erasures/..;x',
    '/api/gdpr/erasures/%2e%2e%2fabc',
  ])('🔴 a dot segment after the door, GET %s without subjects:erase, is refused 400 NON_CANONICAL_PATH, nothing forwarded', async (path) => {
    const r = await send(gateway!.url, 'GET', path, WITHOUT_SCOPE());
    expect([r.status, r.code, r.hits]).toEqual([400, 'NON_CANONICAL_PATH', []]);
  });

  it('control (the gate\'s W18): an escaped `;` keeps the dots inside one reference, so it is the door and refused 403', async () => {
    const r = await send(gateway!.url, 'GET', '/api/gdpr/erasures/%2e%2e%3bx', WITHOUT_SCOPE());
    expect([r.status, r.hits]).toEqual([403, []]);
  });

  it('control: origin-form without subjects:erase is still refused 403, nothing forwarded', async () => {
    const r = await send(gateway!.url, 'POST', '/api/gdpr/erasures', WITHOUT_SCOPE());
    expect([r.status, r.hits]).toEqual([403, []]);
  });

  it('control: a connector WITH subjects:erase is admitted, origin-form and absolute-form, forwarded as sent', async () => {
    const origin = await send(gateway!.url, 'POST', '/api/gdpr/erasures', WITH_SCOPE());
    const absolute = await send(gateway!.url, 'POST', 'http://127.0.0.1/api/gdpr/erasures', WITH_SCOPE());
    const spelled = await send(gateway!.url, 'POST', '/api/gdpr/%65rasures', WITH_SCOPE());
    expect([origin.status, origin.hits]).toEqual([200, ['POST /api/gdpr/erasures']]);
    expect([absolute.status, absolute.hits]).toEqual([200, ['POST /api/gdpr/erasures']]);
    // req.url is restored before forwarding: the upstream sees what the caller sent.
    expect([spelled.status, spelled.hits]).toEqual([200, ['POST /api/gdpr/%65rasures']]);
  });

  it.each([
    ['a plain non-erasure gdpr read', '/api/gdpr/consent/check'],
    ['an odd but decodable non-erasure spelling', '/api/gdpr/%63onsent/check'],
    ['a malformed escape on a path that plainly is not the door', '/api/gdpr/consent/%zz'],
  ])('control (Tightening A): %s is forwarded unchanged', async (_label, path) => {
    const r = await send(gateway!.url, 'GET', path, WITHOUT_SCOPE());
    expect([r.status, r.hits]).toEqual([200, [`GET ${path}`]]);
  });
});

describe('KS-1187 real app, NODE_ENV=production — the v1 absolute-form targets', () => {
  let gateway: { server: http.Server; url: string } | undefined;

  beforeAll(async () => {
    vi.stubEnv('NODE_ENV', 'production');
    vi.stubEnv('CSRF_SECRET', 'ks1187-stub-csrf-not-a-real-secret');
    vi.stubEnv('DATABASE_URL', 'postgres://ks1187:ks1187@127.0.0.1:1/ks1187');
    vi.stubEnv('REDIS_URL', 'redis://127.0.0.1:1');
    vi.stubEnv('ENABLE_TEST_TOKENS', '');
    vi.stubEnv('ENABLE_MOCK_ENDPOINTS', '');
    vi.stubEnv('ORIGINATE_SERVICE_URL', recorderUrl);
    vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
    vi.stubEnv('SUBJECTS_ERASE_SCOPE_ENFORCED', 'true');
    gateway = await bootApp();
  }, 60000);

  afterAll(async () => { await closeServer(gateway?.server); });

  it.each([
    ['POST', 'http://127.0.0.1/api/v1/gdpr/erasures'],
    ['GET', 'http://127.0.0.1/api/v1/gdpr/erasures/abc'],
  ])('🔴 production: %s %s without subjects:erase is refused 403, nothing forwarded', async (method, path) => {
    const r = await send(gateway!.url, method, path, WITHOUT_SCOPE());
    expect([r.status, r.hits]).toEqual([403, []]);
  });

  // Round 2, F-1019-1, production spellings (the v1 prefix; an unversioned path is redirected first).
  it.each([
    '/api/v1/gdpr/erasures/..',
    '/api/v1/gdpr/erasures/%2e%2e',
    '/api/v1/gdpr/erasures/.%2e',
    '/api/v1/gdpr/erasures/..;x',
    '/api/v1/gdpr/erasures/%2e%2e%2fabc',
  ])('🔴 production: a dot segment after the door, GET %s without subjects:erase, is refused 400 NON_CANONICAL_PATH, nothing forwarded', async (path) => {
    const r = await send(gateway!.url, 'GET', path, WITHOUT_SCOPE());
    expect([r.status, r.code, r.hits]).toEqual([400, 'NON_CANONICAL_PATH', []]);
  });

  it('control, production: the same v1 absolute-form POST WITH subjects:erase is admitted and forwarded', async () => {
    const r = await send(gateway!.url, 'POST', 'http://127.0.0.1/api/v1/gdpr/erasures', WITH_SCOPE());
    expect(r.status).toBe(200);
    expect(r.hits.length).toBe(1);
  });
});

/**
 * Bare-app cells: `createProxyRoutes` mounted alone, with an `authenticateToken`
 * that records what each layer sees and admits a fixed connector. The real app
 * cannot show either property below, because the upstream path is derived from
 * `req.originalUrl` whatever `req.url` holds, and the door's router is built inside
 * the factory.
 */
type Seen = { baseUrl: string; url: string };
async function bareProxyApp(scopes: string[], layers: Seen[]): Promise<{ server: http.Server; url: string }> {
  vi.stubEnv('NODE_ENV', 'test');
  vi.stubEnv('ORIGINATE_SERVICE_URL', recorderUrl);
  vi.stubEnv('SUBJECTS_ERASE_SCOPE_ENFORCED', 'true');
  const { createProxyRoutes } = await import('../routes/proxy');
  const { services } = await import('../config/services');
  const authenticateToken = (): RequestHandler => (req: Request, _res: Response, next: NextFunction) => {
    layers.push({ baseUrl: req.baseUrl, url: req.url });
    (req as any).user = {
      userId: 'c0000000-0000-4000-8000-00000000118c', email: 'connector@secuura.io', role: 'connector',
      authMethod: 'api_key', scopes, tenantId: 'a0000000-0000-4000-8000-000000000001',
    };
    req.headers['x-user-id'] = 'c0000000-0000-4000-8000-00000000118c';
    req.headers['x-user-email'] = 'connector@secuura.io';
    req.headers['x-user-role'] = 'connector';
    next();
  };
  const app = express();
  app.use(createProxyRoutes({ services, authenticateToken, log: () => {} }));
  const server = http.createServer(app);
  return { server, url: await listen(server) };
}

describe('KS-1187 round 2, F-1019-3: req.url is restored for the layer after the door', () => {
  let bare: { server: http.Server; url: string } | undefined;
  const layers: Seen[] = [];

  beforeAll(async () => {
    vi.resetModules();
    bare = await bareProxyApp(['subjects:erase'], layers);
  }, 60000);
  afterAll(async () => { await closeServer(bare?.server); });

  it('🔴 an admitted spelled erasure reaches the catch-all with the caller\'s own sub-path, not the canonical one', async () => {
    layers.length = 0;
    const r = await send(bare!.url, 'POST', '/api/gdpr/%65rasures', 'Bearer not-read-by-this-harness');
    // The door's chain sees the canonical path (baseUrl /api/gdpr/erasures); the catch-all
    // proxy mount after it must see what the caller sent. Without the restore it sees `/erasures`.
    const catchAll = layers.filter((l) => l.baseUrl === '/api/gdpr');
    expect([r.status, r.hits]).toEqual([200, ['POST /api/gdpr/%65rasures']]);
    expect(layers.some((l) => l.baseUrl === '/api/gdpr/erasures'), 'CONTROL: the door\'s own chain ran').toBe(true);
    expect(catchAll).toEqual([{ baseUrl: '/api/gdpr', url: '/%65rasures' }]);
  });
});

describe('KS-1187 round 2, F-1019-2: the case rule is read from the door\'s own router', () => {
  let bare: { server: http.Server; url: string } | undefined;
  const layers: Seen[] = [];

  beforeAll(async () => {
    vi.resetModules();
    // Every Router the factory builds, the door's included, is case-sensitive here.
    vi.doMock('express', async (importOriginal) => {
      const real = (await importOriginal()) as any;
      const base = real.default ?? real;
      const Router = (options?: Record<string, unknown>) => base.Router({ ...(options ?? {}), caseSensitive: true });
      // A new default object, so the real express module is never mutated.
      const wrapped = Object.assign((...args: unknown[]) => base(...args), base, { Router });
      return { ...real, Router, default: wrapped };
    });
    bare = await bareProxyApp(['documents:read'], layers);
  }, 60000);
  afterAll(async () => {
    await closeServer(bare?.server);
    vi.doUnmock('express');
    vi.resetModules();
  });

  it('control: the dot rule is live in this app: GET /api/gdpr/erasures/.. is refused 400, nothing forwarded', async () => {
    const r = await send(bare!.url, 'GET', '/api/gdpr/erasures/..', 'Bearer not-read-by-this-harness');
    expect([r.status, r.code, r.hits]).toEqual([400, 'NON_CANONICAL_PATH', []]);
  });

  it('🔴 with a case-sensitive door router, GET /api/gdpr/ERASURES/.. is not judged as the door (a constant `false` would refuse it)', async () => {
    // This pins that the wrapper passes the router's own option, not that a
    // case-sensitive gateway beside a case-insensitive upstream would be safe:
    // under such a router `/ERASURES` is not the door at all (Tightening B).
    const r = await send(bare!.url, 'GET', '/api/gdpr/ERASURES/..', 'Bearer not-read-by-this-harness');
    expect([r.status, r.code, r.hits]).toEqual([200, null, ['GET /api/gdpr/ERASURES/..']]);
  });
});
