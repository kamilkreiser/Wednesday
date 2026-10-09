/**
 * =============================================================================
 * RIGHTS-HOLDERS TENANT SCOPING — INTEGRATION TEST (KS-93 / KS-108)
 * =============================================================================
 * Proves the KS-93 fix end-to-end against a real Postgres, with the full
 * multi-tenancy stack stood up exactly as dev/demo run it:
 *
 *   - MULTI_TENANCY_ENABLED=true → originate's `withTenant()` uses the
 *     TenantPoolManager pg-pool transaction path (BEGIN; set_config; …; COMMIT)
 *     rather than the single-tenant Prisma fallback.
 *   - `extractTenantContext(manager)` resolves the `x-tenant-id` header — which
 *     is what the API gateway forwards after it has validated a super_admin's
 *     `X-Tenant-Override` (that client→gateway mapping lives in the gateway's
 *     auth middleware and is out of scope for this originate-level test).
 *   - the real `adminConfigRouter`, including `authenticate()` + `requireRole()`.
 *
 * KS-93 was: `GET /api/admin/rights-holders` with the tenant override (and no
 * `?organizationId=`) returned HTTP 400 `TENANT_SCOPE_REQUIRED` — a super_admin
 * had to dual-send header AND query param. KS-108 rewrote every rights_holders
 * handler around `resolveTenantId()` + `withTenant()`. These tests lock that in
 * and assert cross-tenant isolation on the shared table.
 *
 * DB-gated. This is an INTEGRATION suite kept out of the default `npm test`
 * (unit) run via its own jest config (`jest.integration.config.js` /
 * `npm run test:integration`). It is never silently skipped: with a database it
 * runs fully and fails loudly; without one the dedicated command throws a clear
 * setup error in beforeAll. Point it at a Postgres via TEST_DATABASE_URL
 * (default DB, holds rights_holders) + TEST_PLATFORM_DATABASE_URL (platform DB,
 * holds tenants/tenant_config); both fall back to the service's own
 * DATABASE_URL / PLATFORM_DATABASE_URL.
 * =============================================================================
 */

import http from 'http';
import { randomUUID } from 'crypto';
import { Client } from 'pg';
import jwt from 'jsonwebtoken';

// --- DB targets (resolved before any env-reading module is require()'d) ------
const DEFAULT_DB = process.env.TEST_DATABASE_URL || process.env.DATABASE_URL;
const PLATFORM_DB =
  process.env.TEST_PLATFORM_DATABASE_URL ||
  process.env.PLATFORM_DATABASE_URL ||
  (DEFAULT_DB ? DEFAULT_DB.replace(/\/[^/?]+(\?.*)?$/, '/secuura_platform$1') : undefined);

// --- Force the full multi-tenancy stack on, before requiring config/db ------
// config.ts throws at import if DATABASE_URL / JWT_SECRET are unset, and
// withTenant() only takes the TenantPoolManager path when MT is enabled.
const JWT_SECRET = process.env.JWT_SECRET || 'ks93-integration-secret';
if (DEFAULT_DB) {
  process.env.DATABASE_URL = DEFAULT_DB;
  process.env.PLATFORM_DATABASE_URL = PLATFORM_DB as string;
}
process.env.JWT_SECRET = JWT_SECRET;
// KS-184: originate verifies RS256-only. Generate a test keypair, publish the
// public key to the middleware (JWT_PUBLIC_KEY, read at module load) and keep
// the private key to sign the test tokens below. Set before requiring the app.
const { privateKey: _rsaPriv, publicKey: _rsaPub } = require('crypto').generateKeyPairSync('rsa', {
  modulusLength: 2048,
});
const JWT_PRIVATE_PEM = _rsaPriv.export({ type: 'pkcs8', format: 'pem' }).toString();
process.env.JWT_PUBLIC_KEY = Buffer.from(
  _rsaPub.export({ type: 'spki', format: 'pem' }).toString(),
).toString('base64');
process.env.MULTI_TENANCY_ENABLED = 'true';
if (process.env.NODE_ENV === 'production' || !process.env.NODE_ENV) {
  // never run this as 'production' (extractTenantContext would 400 on the
  // tenant-bound paths that legitimately omit x-tenant-id).
  process.env.NODE_ENV = 'test';
}

const RUN = randomUUID().slice(0, 8);
const emailFor = (t: 'a' | 'b') => `rh-${t}-${RUN}@ks93.test`;

interface ApiResult {
  status: number;
  body: any;
}

describe('rights_holders tenant scoping (KS-93 / KS-108) — full MT integration', () => {
  let server: http.Server;
  let baseUrl: string;
  let platformClient: Client;
  let defaultClient: Client;
  let disconnectDb: () => Promise<void>;

  const tenantA = randomUUID();
  const tenantB = randomUUID();
  let tokens: { superAdmin: string; orgAdminA: string; orgAdminNoOrg: string };

  async function api(
    method: string,
    path: string,
    opts: { token?: string; tenantId?: string; body?: unknown } = {},
  ): Promise<ApiResult> {
    const headers: Record<string, string> = { 'content-type': 'application/json' };
    if (opts.token) headers.authorization = `Bearer ${opts.token}`;
    if (opts.tenantId) headers['x-tenant-id'] = opts.tenantId;
    const res = await fetch(`${baseUrl}${path}`, {
      method,
      headers,
      body: opts.body === undefined ? undefined : JSON.stringify(opts.body),
    });
    const body = await res.json().catch(() => null);
    return { status: res.status, body };
  }

  const emails = (r: ApiResult): string[] =>
    (r.body?.rightsHolders ?? []).map((rh: { email: string }) => rh.email);

  beforeAll(async () => {
    if (!DEFAULT_DB) {
      throw new Error(
        'KS-93 integration suite requires a database. Set TEST_DATABASE_URL ' +
          '(default DB with rights_holders) and TEST_PLATFORM_DATABASE_URL ' +
          '(platform DB with tenants/tenant_config), or run with the service ' +
          'DATABASE_URL / PLATFORM_DATABASE_URL exported.',
      );
    }

    // Modules that read env at import-time — require AFTER the env is set above.
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const db = require('../db');
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const { adminConfigRouter } = require('../routes/adminConfig');
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const { extractTenantContext } = require('@secuura/shared');
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const express = require('express');

    disconnectDb = db.disconnectDb;

    await db.initDb();
    const manager = db.getTenantManager();
    if (!manager) {
      throw new Error(
        'TenantPoolManager not initialised — check MULTI_TENANCY_ENABLED and ' +
          'PLATFORM_DATABASE_URL. withTenant() would fall back to Prisma.',
      );
    }

    platformClient = new Client({ connectionString: PLATFORM_DB });
    defaultClient = new Client({ connectionString: DEFAULT_DB });
    await platformClient.connect();
    await defaultClient.connect();

    // Seed two tenants into the platform DB so refreshConfigs() loads them as
    // active and extractTenantContext resolves them cleanly. tenant_config
    // points at the same default DB (where rights_holders lives).
    const u = new URL(DEFAULT_DB);
    const dbName = u.pathname.replace(/^\//, '');
    const dbHost = u.hostname;
    const dbPort = parseInt(u.port || '5432', 10);
    for (const [id, slug] of [
      [tenantA, 'a'],
      [tenantB, 'b'],
    ] as const) {
      await platformClient.query(
        `INSERT INTO tenants (id, name, slug, status) VALUES ($1, $2, $3, 'active')
         ON CONFLICT (id) DO NOTHING`,
        [id, `KS93 Test ${slug.toUpperCase()}`, `ks93-${slug}-${id.slice(0, 8)}`],
      );
      await platformClient.query(
        `INSERT INTO tenant_config (tenant_id, db_name, db_host, db_port) VALUES ($1, $2, $3, $4)
         ON CONFLICT (tenant_id) DO NOTHING`,
        [id, dbName, dbHost, dbPort],
      );
    }
    await db.refreshTenantConfigs();

    // Minimal app == the production wiring for this router: json body parser,
    // the MT tenant-context middleware, then the real adminConfigRouter (which
    // mounts authenticate() + requireRole() itself).
    const app = express();
    app.use(express.json());
    app.use(extractTenantContext(manager));
    app.use('/api/admin', adminConfigRouter);

    server = http.createServer(app);
    await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
    const addr = server.address();
    baseUrl = `http://127.0.0.1:${typeof addr === 'object' && addr ? addr.port : 0}`;

    const sign = (payload: object): string => jwt.sign(payload, JWT_PRIVATE_PEM, { algorithm: 'RS256' });
    tokens = {
      // super_admin (SYSTEM_ADMIN) has NO organizationId → must scope via override.
      superAdmin: sign({ userId: 'ks93-sa', email: 'sa@ks93.test', role: 'SYSTEM_ADMIN', verificationLevel: 'full' }),
      // tenant-bound admin, org == tenantA.
      orgAdminA: sign({ userId: 'ks93-oa', email: 'oaa@ks93.test', role: 'ORG_ADMIN', organizationId: tenantA, verificationLevel: 'full' }),
      // tenant-bound role but no org on the JWT.
      orgAdminNoOrg: sign({ userId: 'ks93-no', email: 'noorg@ks93.test', role: 'ORG_ADMIN', verificationLevel: 'full' }),
    };
  }, 30000);

  afterAll(async () => {
    if (defaultClient) {
      await defaultClient.query(`DELETE FROM rights_holders WHERE organization_id = ANY($1::uuid[])`, [[tenantA, tenantB]]);
      await defaultClient.end();
    }
    if (platformClient) {
      await platformClient.query(`DELETE FROM tenant_config WHERE tenant_id = ANY($1::uuid[])`, [[tenantA, tenantB]]);
      await platformClient.query(`DELETE FROM tenants WHERE id = ANY($1::uuid[])`, [[tenantA, tenantB]]);
      await platformClient.end();
    }
    if (disconnectDb) await disconnectDb();
    if (server) await new Promise<void>((resolve) => server.close(() => resolve()));
  });

  // --- Criterion #2: create scoped by the override, no body.organizationId ---
  it('super_admin POST with x-tenant-id only (no body org) creates a holder scoped to that tenant', async () => {
    const a = await api('POST', '/api/admin/rights-holders', {
      token: tokens.superAdmin,
      tenantId: tenantA,
      body: { email: emailFor('a'), sendInvite: false },
    });
    expect(a.status).toBe(201);
    expect(a.body?.success).toBe(true);
    expect(a.body?.rightsHolder?.email).toBe(emailFor('a'));
    expect(a.body?.rightsHolder?.organizationId).toBe(tenantA);

    const b = await api('POST', '/api/admin/rights-holders', {
      token: tokens.superAdmin,
      tenantId: tenantB,
      body: { email: emailFor('b'), sendInvite: false },
    });
    expect(b.status).toBe(201);
    expect(b.body?.rightsHolder?.organizationId).toBe(tenantB);
  });

  // --- Criterion #1: list by override only, NOT 400, and scoped --------------
  it('super_admin GET list with x-tenant-id only returns 200 scoped (KS-93: was 400)', async () => {
    const a = await api('GET', '/api/admin/rights-holders', { token: tokens.superAdmin, tenantId: tenantA });
    expect(a.status).toBe(200);
    expect(emails(a)).toContain(emailFor('a'));
    expect(emails(a)).not.toContain(emailFor('b'));
    for (const rh of a.body.rightsHolders) expect(rh.organizationId).toBe(tenantA);
  });

  it('super_admin scoped to the other tenant sees only that tenant (cross-tenant isolation)', async () => {
    const b = await api('GET', '/api/admin/rights-holders', { token: tokens.superAdmin, tenantId: tenantB });
    expect(b.status).toBe(200);
    expect(emails(b)).toContain(emailFor('b'));
    expect(emails(b)).not.toContain(emailFor('a'));
  });

  // --- Criterion #3: existing ?organizationId= path still works --------------
  it('super_admin GET list with header + ?organizationId= still works (no regression, no dual-send 400)', async () => {
    const a = await api('GET', `/api/admin/rights-holders?organizationId=${tenantA}`, {
      token: tokens.superAdmin,
      tenantId: tenantA,
    });
    expect(a.status).toBe(200);
    expect(emails(a)).toContain(emailFor('a'));
    expect(emails(a)).not.toContain(emailFor('b'));
  });

  // --- tenant-bound admin: own org only, cannot override ---------------------
  it('tenant-bound admin sees only their own org and cannot escape it via the override header', async () => {
    const own = await api('GET', '/api/admin/rights-holders', { token: tokens.orgAdminA });
    expect(own.status).toBe(200);
    expect(emails(own)).toContain(emailFor('a'));
    expect(emails(own)).not.toContain(emailFor('b'));

    // Sending another tenant's id must NOT broaden a tenant-bound admin's scope.
    const spoof = await api('GET', '/api/admin/rights-holders', { token: tokens.orgAdminA, tenantId: tenantB });
    expect(spoof.status).toBe(200);
    expect(emails(spoof)).toContain(emailFor('a'));
    expect(emails(spoof)).not.toContain(emailFor('b'));
  });

  // --- Criterion #4: non-super-admin without an org → empty (not all) --------
  it('non-super-admin without an org gets an empty list, not a 400 and not all tenants', async () => {
    const r = await api('GET', '/api/admin/rights-holders', { token: tokens.orgAdminNoOrg });
    expect(r.status).toBe(200);
    expect(r.body?.rightsHolders).toEqual([]);
    expect(r.body?.total).toBe(0);
  });
});
