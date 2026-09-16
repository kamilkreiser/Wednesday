/**
 * =============================================================================
 * KS-871 round 2 (QA gate F-1011-5 on PR #1011) — audit rows through the REAL
 * gateway app, in test AND production mode
 * =============================================================================
 * The Part A / Part B files drive `createAuditMiddleware` + `createProxyRoutes`
 * in isolation. The tier-1 gate on #1011 round 1 measured three things they cannot
 * see, because only the real app has index.ts's version redirect and `/api/v1`
 * strip mounted ABOVE the audit middleware (index.ts:530 / :561 / :570):
 *   F-1011-1  under NODE_ENV=production every refused erasure arrives as
 *             /api/v1/gdpr/erasures after the 307, and a path read from
 *             `req.originalUrl` audits it as `v1.erasures`;
 *   F-1011-2  the same source rewrote ADMITTED non-gdpr rows (`/api/v1/logs` →
 *             `v1.create`);
 *   F-1011-5  no cell pinned a non-gdpr row, a `/api/v1/` row or production mode
 *             (tampers G-NONGDPR / G-V1 / G-D3 were 0 red).
 *
 * This file imports the REAL app exported by index.ts (its `require.main` guard
 * keeps it from listening; the ks1165 real-app pattern), with `../db` mocked so
 * `isDbAvailable()` is true and `query` records the audit INSERT. Rows are matched
 * by a unique User-Agent, never by timing. Harness shape: the gate's
 * `qa1011-census.test.ts` (report 2026-09-17-ks871-1011-0a1f8900c-tier1-r1).
 * =============================================================================
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import jwt from 'jsonwebtoken';
import type { AddressInfo } from 'net';

const rec = vi.hoisted(() => ({ calls: [] as Array<{ sql: string; params: unknown[] }> }));
vi.mock('../db', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  return {
    ...real,
    isDbAvailable: () => true,
    query: async (sql: string, params: unknown[] = []) => {
      rec.calls.push({ sql, params });
      return { rows: [], rowCount: 0 };
    },
  };
});

interface AuditRow { action: unknown; resourceType: unknown; path: unknown }

/** The audit INSERT whose user_agent (param 7) is `ua`, read back as action / resource_type / details.path. */
function rowFor(ua: string): AuditRow | undefined {
  const call = rec.calls.find((c) => /INSERT INTO audit_logs/.test(c.sql) && c.params[7] === ua);
  if (!call) return undefined;
  const details = JSON.parse(String(call.params[8])) as { path?: unknown };
  return { action: call.params[3], resourceType: call.params[4], path: details.path };
}

/** One assertion per field, so a failure names the field and both values. */
function expectRow(row: AuditRow | undefined, want: AuditRow, label: string): void {
  expect(row, `${label}: an audit row was written`).toBeDefined();
  expect(row?.action, `${label}: action`).toBe(want.action);
  expect(row?.resourceType, `${label}: resource_type`).toBe(want.resourceType);
  expect(row?.path, `${label}: details.path`).toBe(want.path);
}

async function waitForRow(ua: string, timeoutMs = 3000): Promise<AuditRow | undefined> {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    const row = rowFor(ua);
    if (row) return row;
    await new Promise((r) => setTimeout(r, 25));
  }
  return undefined;
}

const seen: string[] = [];
let recorder: http.Server | undefined;
let recorderUrl = '';

async function listen(server: http.Server): Promise<string> {
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
  return `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}

function post(base: string, path: string, headers: Record<string, string>): Promise<{ status: number; location: string | undefined }> {
  return new Promise((resolve, reject) => {
    const target = new URL(base);
    const body = '{}';
    const req = http.request(
      { hostname: target.hostname, port: target.port, path, method: 'POST', agent: false,
        headers: { 'content-type': 'application/json', 'content-length': String(Buffer.byteLength(body)), ...headers } },
      (res) => { res.resume(); res.on('end', () => resolve({ status: res.statusCode ?? 0, location: res.headers.location })); },
    );
    req.on('error', reject);
    req.end(body);
  });
}

/** A connector WITHOUT `subjects:erase`, signed with vitest.setup.ts's in-process RS256 key. */
function connectorToken(): string {
  return 'Bearer ' + jwt.sign(
    { userId: 'c0000000-0000-4000-8000-00000000000c', role: 'connector', authMethod: 'api_key', scopes: ['documents:read'],
      tenantId: 'a0000000-0000-4000-8000-000000000001', organizationId: 'd0000000-0000-4000-8000-00000000000d', verificationLevel: 'BASIC' },
    process.env.__TEST_JWT_PRIVATE_PEM as string,
    { algorithm: 'RS256', expiresIn: '10m' },
  );
}

async function bootApp(): Promise<{ server: http.Server; url: string }> {
  vi.resetModules();
  const app = (await import('../index')).default;
  const server = http.createServer(app as http.RequestListener);
  return { server, url: await listen(server) };
}

async function closeServer(server: http.Server | undefined): Promise<void> {
  if (!server) return;
  server.closeAllConnections();
  await new Promise<void>((r) => server.close(() => r()));
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

describe('KS-871 real app, NODE_ENV=test — an admitted non-gdpr row is canonical in every spelling', () => {
  let gateway: { server: http.Server; url: string } | undefined;

  beforeAll(async () => {
    vi.stubEnv('ORIGINATE_SERVICE_URL', recorderUrl);
    vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
    gateway = await bootApp();
  }, 60000);

  afterAll(async () => { await closeServer(gateway?.server); });

  it('KS-871 real app — POST /api/logs is audited logs.create / log at /api/logs (resource_type is singular, audit.ts deriveAction)', async () => {
    const ua = 'ks871-real-app-logs';
    const res = await post(gateway!.url, '/api/logs', { 'user-agent': ua });
    expect(res.status).toBe(204);
    expectRow(await waitForRow(ua), { action: 'logs.create', resourceType: 'log', path: '/api/logs' }, 'the audit row for POST /api/logs');
  });

  it('🔴 KS-871 real app — POST /api/v1/logs is audited as the SAME canonical row, not v1.create', async () => {
    const ua = 'ks871-real-app-v1-logs';
    const res = await post(gateway!.url, '/api/v1/logs', { 'user-agent': ua });
    expect(res.status).toBe(204);
    expectRow(await waitForRow(ua), { action: 'logs.create', resourceType: 'log', path: '/api/logs' }, 'the audit row for POST /api/v1/logs');
  });
});

describe('KS-871 real app, NODE_ENV=production — a refused erasure after the 307 is audited canonically', () => {
  let gateway: { server: http.Server; url: string } | undefined;

  beforeAll(async () => {
    // Production boot needs these (the gate's census_run.py): a stub CSRF secret and
    // DB / Redis URLs pointed at a closed loopback port. `../db` is mocked above.
    vi.stubEnv('NODE_ENV', 'production');
    vi.stubEnv('CSRF_SECRET', 'ks871-stub-csrf-not-a-real-secret');
    vi.stubEnv('DATABASE_URL', 'postgres://ks871:ks871@127.0.0.1:1/ks871');
    vi.stubEnv('REDIS_URL', 'redis://127.0.0.1:1');
    vi.stubEnv('ENABLE_TEST_TOKENS', '');
    vi.stubEnv('ENABLE_MOCK_ENDPOINTS', '');
    vi.stubEnv('ORIGINATE_SERVICE_URL', recorderUrl);
    vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
    vi.stubEnv('SUBJECTS_ERASE_SCOPE_ENFORCED', 'true');
    gateway = await bootApp();
  }, 60000);

  afterAll(async () => { await closeServer(gateway?.server); });

  it('🔴 KS-871 real app, production — a refused POST /api/gdpr/erasures is audited gdpr.create at /api/gdpr/erasures, not v1.erasures', async () => {
    const auth = connectorToken();
    const first = await post(gateway!.url, '/api/gdpr/erasures', { 'user-agent': 'ks871-prod-307', authorization: auth });
    expect(first.status, 'production redirects the unversioned path').toBe(307);
    expect(first.location).toBe('/api/v1/gdpr/erasures');

    const ua = 'ks871-prod-erasure-refused';
    const hitsBefore = seen.length;
    const refused = await post(gateway!.url, first.location as string, { 'user-agent': ua, authorization: auth });
    expect(refused.status, 'the door refuses a connector without subjects:erase').toBe(403);
    expect(seen.length - hitsBefore, 'nothing reached originate, so the 403 is the door').toBe(0);
    expectRow(await waitForRow(ua), { action: 'gdpr.create', resourceType: 'gdpr', path: '/api/gdpr/erasures' }, 'the audit row for the refused erasure');
  });
});
