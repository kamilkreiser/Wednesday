/**
 * =============================================================================
 * KS-1195 — the per-key rate limiter fires in the assembled gateway
 * =============================================================================
 * `enforceClientRateLimit` (KS-164/170/616) reads `req.user`, which only
 * `authenticateToken` sets. It was `app.use()`d in index.ts ahead of every
 * `authenticateToken`, so it never saw a user: a key validated at 2 requests per
 * 60 s answered 201 five times with no `X-RateLimit-Limit` (tier-1 QA gate on
 * PR #1014, finding F-2). It now runs as the continuation of each
 * `authenticateToken` branch that sets `req.user`, counts a request once, and the
 * dead app-level mount is gone.
 *
 * Real-app cells import the app exported by index.ts (its `require.main` guard
 * keeps it from listening; the ks1165/ks871 real-app pattern) with every upstream
 * pointed at one recording stub. There is no Redis here, so the limiter counts in
 * the in-memory degrade path. Placement cells mount the REAL `authenticateToken`
 * on a bare express app. Harness shape: the gate's `qa1014-gate-census.test.ts`
 * (report 2026-09-17-ks1176-1014-616c766a5-tier1-r1).
 * =============================================================================
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import express from 'express';
import jwt from 'jsonwebtoken';
import type { AddressInfo } from 'net';

const PRIV = process.env.__TEST_JWT_PRIVATE_PEM || '';

// Each key has its own connectorId, so each cell has its own counter.
const KEYS: Record<string, Record<string, unknown>> = {
  sk_ks1195_docs_00001: { connectorId: 'ks1195-docs', scopes: ['documents:write'], organizationId: 'org-ks1195', tenantId: 't-ks1195', rateLimit: 2, rateLimitWindow: 60 },
  sk_ks1195_anchors_01: { connectorId: 'ks1195-anchors', scopes: ['anchors:read'], organizationId: 'org-ks1195', tenantId: 't-ks1195-anchors', rateLimit: 2, rateLimitWindow: 60 },
  sk_ks1195_twice_0001: { connectorId: 'ks1195-twice', scopes: [], tenantId: 't-ks1195', rateLimit: 2, rateLimitWindow: 60 },
  sk_ks1195_tenant_001: { connectorId: 'ks1195-tenant', scopes: [], tenantId: 't-ks1195-als', rateLimit: 50, rateLimitWindow: 60 },
};

type Rec = { method: string; url: string; headers: http.IncomingHttpHeaders; body: string };
const seen: Rec[] = [];
const logged: string[] = [];

function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
}

type Res = { status: number; code: string | null; headers: http.IncomingHttpHeaders; json: any };
function send(base: string, method: string, path: string, headers: Record<string, string>, body?: string): Promise<Res> {
  return new Promise((resolve, reject) => {
    const u = new URL(base);
    const h: Record<string, string> = { ...headers };
    if (body !== undefined) { h['content-type'] = 'application/json'; h['content-length'] = String(Buffer.byteLength(body)); }
    const req = http.request({ hostname: u.hostname, port: u.port, path, method, headers: h, agent: false }, (res) => {
      const c: Buffer[] = []; res.on('data', (d) => c.push(d));
      res.on('end', () => {
        let json: any = null;
        try { json = JSON.parse(Buffer.concat(c).toString()); } catch { /* non-JSON body: json stays null */ }
        resolve({ status: res.statusCode || 0, code: json?.error?.code ?? null, headers: res.headers, json });
      });
    });
    req.on('error', reject);
    if (body !== undefined) req.end(body); else req.end();
  });
}

async function listen(s: http.Server): Promise<string> {
  await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
  return `http://127.0.0.1:${(s.address() as AddressInfo).port}`;
}
async function close(s?: http.Server): Promise<void> {
  if (!s) return;
  (s as any).closeAllConnections?.();
  await new Promise<void>((r) => s.close(() => r()));
}

let stub: http.Server; let stubUrl = '';
let gw: http.Server; let gwUrl = '';
let bare: http.Server; let bareUrl = '';
let redis: any;
const handlerHits: Record<string, number> = { twice: 0 };

beforeAll(async () => {
  expect(PRIV.length, 'vitest.setup.ts provisioned a throwaway RS256 private key').toBeGreaterThan(100);
  stub = http.createServer(async (req, res) => {
    const body = await readBody(req);
    seen.push({ method: req.method || '', url: req.url || '', headers: { ...req.headers }, body });
    const j = (s: number, o: unknown) => { res.writeHead(s, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); };
    if (req.url === '/api/keys/validate') {
      const m = KEYS[JSON.parse(body || '{}').key];
      return j(200, m ? { data: { valid: true, ...m } } : { data: { valid: false } });
    }
    if (req.url === '/internal/connector-token') {
      const m = KEYS[JSON.parse(body || '{}').apiKey];
      if (!m) return j(401, { success: false });
      const token = jwt.sign({ userId: `connector:${String(m.connectorId)}`, email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', tenantId: m.tenantId, scopes: m.scopes }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
      return j(200, { success: true, data: { token, expiresIn: 600 } });
    }
    if (req.url === '/.well-known/jwks.json') return j(404, {});
    if (req.method === 'POST' && req.url === '/api/documents') return j(201, { success: true, data: { id: 'doc-ks1195' } });
    if (req.method === 'GET' && (req.url || '').startsWith('/api/anchors/')) return j(200, { success: true, data: [] });
    return j(404, { success: false });
  });
  stubUrl = await listen(stub);

  vi.resetModules();
  vi.stubEnv('NODE_ENV', 'test');
  vi.stubEnv('ENABLE_TEST_TOKENS', 'true');
  vi.stubEnv('ORIGINATE_SERVICE_URL', stubUrl);
  vi.stubEnv('SECURITY_SERVICE_URL', stubUrl);
  vi.stubEnv('AUTH_SERVICE_URL', stubUrl);
  vi.stubEnv('ANCHORING_SERVICE_URL', stubUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  delete process.env.JWT_JWKS_URL;

  const app = (await import('../index')).default;
  redis = await import('../services/redis');
  const auth = await import('../middleware/auth');
  const shared = await import('@secuura/shared');
  const { logger } = await import('../utils/logger');
  for (const level of ['error', 'warn'] as const) {
    vi.spyOn(logger, level).mockImplementation(((...a: unknown[]) => { logged.push(a.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))).join(' ')); return logger; }) as any);
  }
  vi.spyOn(console, 'error').mockImplementation((...a: unknown[]) => { logged.push(a.map(String).join(' ')); });

  gw = http.createServer(app as http.RequestListener);
  gwUrl = await listen(gw);

  const b = express();
  b.get('/twice', auth.authenticateToken(true), auth.authenticateToken(true), (_q, s) => { handlerHits.twice += 1; s.status(200).json({ ok: true }); });
  b.get('/tenant', auth.authenticateToken(true), (_q, s) => { s.status(200).json({ tenant: shared.currentTenantId() ?? null }); });
  bare = http.createServer(b);
  bareUrl = await listen(bare);
}, 60000);

afterAll(async () => {
  await close(gw);
  await close(bare);
  await close(stub);
  vi.restoreAllMocks();
  vi.unstubAllEnvs();
}, 30000);

const docsPosted = (marker: string) => seen.filter((r) => r.method === 'POST' && r.url === '/api/documents' && r.body.includes(marker)).length;
const anchorsFetched = (marker: string) => seen.filter((r) => r.method === 'GET' && r.url.startsWith(`/api/anchors/${marker}`)).length;

describe('KS-1195: the per-key limiter in the REAL app', () => {
  const r1: Res[] = [];
  const r2: Res[] = [];

  it('R1 / A3: a key at 2 per 60 s creating documents is refused 429 from request 3, with Redis unavailable', async () => {
    expect(redis.isRedisAvailable(), 'precondition: no Redis, so this is the in-memory degrade path').toBe(false);
    for (let i = 0; i < 5; i++) {
      r1.push(await send(gwUrl, 'POST', '/api/documents', { 'x-api-key': 'sk_ks1195_docs_00001' }, JSON.stringify({ title: `ks1195-r1-${i}` })));
    }
    expect(r1.map((r) => r.status)).toEqual([201, 201, 429, 429, 429]);
    expect(r1.map((r) => r.headers['x-ratelimit-limit'])).toEqual(['2', '2', '2', '2', '2']);
    expect(r1.slice(2).map((r) => r.code)).toEqual(['RATE_LIMIT_EXCEEDED', 'RATE_LIMIT_EXCEEDED', 'RATE_LIMIT_EXCEEDED']);
    expect(r1[2].headers['retry-after']).toBeDefined();
    expect(logged.some((l) => l.includes('DEGRADED') && l.includes('redis-not-ready')), 'the limiter counted in the in-memory degrade path').toBe(true);
  });

  it('A1: a refused create answers once and never reaches the handler (2 upstream creates, no double send)', () => {
    expect(r1.length, 'R1 ran first').toBe(5);
    expect(docsPosted('ks1195-r1-')).toBe(2);
    expect(logged.filter((l) => /ERR_HTTP_HEADERS_SENT|headers after they are sent/i.test(l))).toEqual([]);
  });

  it('R2: the same ceiling holds on a proxied family (GET /api/anchors), and a refused read is not forwarded', async () => {
    for (let i = 0; i < 5; i++) {
      r2.push(await send(gwUrl, 'GET', `/api/anchors/ks1195-r2-${i}`, { 'x-api-key': 'sk_ks1195_anchors_01' }));
    }
    expect(r2.map((r) => r.status)).toEqual([200, 200, 429, 429, 429]);
    expect(r2.map((r) => r.headers['x-ratelimit-limit'])).toEqual(['2', '2', '2', '2', '2']);
    expect(anchorsFetched('ks1195-r2-')).toBe(2);
    expect(logged.filter((l) => /ERR_HTTP_HEADERS_SENT|headers after they are sent/i.test(l))).toEqual([]);
  });

  it("A2: an allowed proxied request still carries the key's tenant to the upstream", () => {
    // Independent of how many R2 requests were allowed, so it reads the same before and after KS-1195.
    const forwarded = seen.filter((r) => r.method === 'GET' && r.url.startsWith('/api/anchors/ks1195-r2-'));
    expect(forwarded.length, 'R2 ran first and forwarded at least one read').toBeGreaterThan(0);
    expect(new Set(forwarded.map((r) => r.headers['x-tenant-id']))).toEqual(new Set(['t-ks1195-anchors']));
  });

  it('control: a JWT caller is not governed by the per-key limiter (5 of 5 forwarded, no X-RateLimit-Limit)', async () => {
    const token = jwt.sign({ userId: 'u-ks1195', email: 'ks1195@example.test', role: 'issuer', authMethod: 'email', tenantId: 't-ks1195-jwt', verificationLevel: 'standard' }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
    const rs: Res[] = [];
    for (let i = 0; i < 5; i++) rs.push(await send(gwUrl, 'GET', `/api/anchors/ks1195-jwt-${i}`, { authorization: `Bearer ${token}` }));
    expect(rs.map((r) => r.status)).toEqual([200, 200, 200, 200, 200]);
    expect(rs.map((r) => r.headers['x-ratelimit-limit'] ?? null)).toEqual([null, null, null, null, null]);
    expect(anchorsFetched('ks1195-jwt-')).toBe(5);
  });

  it('control: no credential and an unknown key are still 401, and neither is forwarded', async () => {
    const none = await send(gwUrl, 'GET', '/api/anchors/ks1195-none', {});
    const unknown = await send(gwUrl, 'GET', '/api/anchors/ks1195-unknown', { 'x-api-key': 'sk_ks1195_not_a_key_' });
    expect([none.status, unknown.status]).toEqual([401, 401]);
    expect(anchorsFetched('ks1195-none') + anchorsFetched('ks1195-unknown')).toBe(0);
  });
});

describe('KS-1195: placement inside the real authenticateToken', () => {
  it('R3: a chain that authenticates twice counts the request once (2 allowed, then 429)', async () => {
    const rs: Res[] = [];
    for (let i = 0; i < 3; i++) rs.push(await send(bareUrl, 'GET', '/twice', { 'x-api-key': 'sk_ks1195_twice_0001' }));
    expect(rs.map((r) => r.status)).toEqual([200, 200, 429]);
    expect(handlerHits.twice).toBe(2);
  });

  it("A2: the handler after the limiter still runs inside the key's tenant context", async () => {
    const r = await send(bareUrl, 'GET', '/tenant', { 'x-api-key': 'sk_ks1195_tenant_001' });
    expect(r.status).toBe(200);
    expect(r.json).toEqual({ tenant: 't-ks1195-als' });
  });
});
