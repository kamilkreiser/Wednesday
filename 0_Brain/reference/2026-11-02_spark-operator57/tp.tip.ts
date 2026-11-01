import express from 'express';
import { z } from 'zod';
import { tenantIdParamGuard } from './tenantIdParam.js';
import pg from 'pg';
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { createHash, randomBytes } from 'node:crypto';
import { authenticate as jwtAuthenticate, enforceProductionConfig, errorHandler, pgSslConfig, rejectNulBytes } from '@secuura/shared';
import { requestMeteringKey, type MeteringKey } from './meteringKey.js';

// Production startup guard — refuse to start with dev defaults in production
enforceProductionConfig('tenant-provisioning', {
  requiredEnvVars: ['DATABASE_URL', 'PLATFORM_DATABASE_URL'],
  forbiddenValues: {},
  requireRealProviders: true,
});

const app = express();
app.use(express.json({ limit: '1mb' }));
app.use(rejectNulBytes()); // KS-471: no U+0000 may pass the boundary (raw-500 / persist class)

const PORT = parseInt(process.env.PORT || '4022', 10);

const PLATFORM_DB_URL = process.env.PLATFORM_DATABASE_URL;
if (!PLATFORM_DB_URL) throw new Error('PLATFORM_DATABASE_URL environment variable is required');

// Derive PG connection details from PLATFORM_DATABASE_URL (preferred) or DATABASE_URL
// PLATFORM_DATABASE_URL always points to the real PostgreSQL server — not PgBouncer —
// which is required because tenant creation uses CREATE DATABASE (admin-level op).
const _dbUrl = new URL(PLATFORM_DB_URL);
const _fallbackUrl = process.env.DATABASE_URL ? new URL(process.env.DATABASE_URL) : null;
const PG_USER = process.env.POSTGRES_USER || _dbUrl.username || _fallbackUrl?.username || 'secuura';
const PG_PASSWORD = process.env.POSTGRES_PASSWORD || _dbUrl.password || _fallbackUrl?.password || 'secuura_dev_password';
const PG_HOST = process.env.POSTGRES_HOST || _dbUrl.hostname || _fallbackUrl?.hostname || 'postgres';
const PG_PORT = parseInt(process.env.POSTGRES_PORT || _dbUrl.port || _fallbackUrl?.port || '5432', 10);

const TOKENISATION_URL = process.env.TOKENISATION_URL || 'http://tokenisation:4021';
// KS-1240: the longest tenant creation waits for the tokenisation service to generate a tenant key. The fetch
// carried no timeout, so a service that accepted the connection and never answered held the request open after
// the tenant row was inserted. On expiry the fetch (or the body read) rejects into the handler's existing
// try/catch, the same path an unreachable service already takes.
// The only route to this handler is the gateway's POST /api/platform/tenants, which gives up at
// PLATFORM_UPSTREAM_TIMEOUT_MS (default 8000, api-gateway routes/platform.ts) and answers 504. The two bounded
// fetches run one after the other, so this bound plus METERING_KEY_FETCH_TIMEOUT_MS plus the writes must fit
// inside that deadline, or the caller is told 504 while the tenant is still being completed.
const KEY_GENERATION_FETCH_TIMEOUT_MS = 3_000;
// KS-1240, Kam's ruling on decision card secuura-ks1240-key-fail-answer-measured-1028 (option b): when the tenant's vault key
// is not confirmed, tenant creation still answers 201 (the tenant is active), but the answer says so: `keyPending: true` and
// this message. `keyPending` is false when the key service confirmed the key; the message is then absent.
const KEY_PENDING_MESSAGE =
  'The tenant was created, but its vault key was not confirmed: the key service did not return a key. No vault key hash is recorded for this tenant.';
// KS-336: the security service owns connector API keys (svc_api_keys, in the app
// DB — a different DB from the platform tables this service writes). We mint the
// per-tenant metering key over HTTP, not via platformQuery. Default matches the
// local-stack service name + port (security listens on 4008); Azure sets the
// internal FQDN via env.
const SECURITY_SERVICE_URL = process.env.SECURITY_SERVICE_URL || 'http://security:4008';

const INIT_SCRIPTS_DIR = process.env.INIT_SCRIPTS_DIR || '/app/init-scripts';

const platformPool = new pg.Pool({ connectionString: PLATFORM_DB_URL, max: 5 });

async function platformQuery<T extends pg.QueryResultRow = any>(
  text: string,
  params?: unknown[],
): Promise<pg.QueryResult<T>> {
  return platformPool.query<T>(text, params);
}

// -------------------------------------------------------------------------
// Helper: create a database and run init scripts
// -------------------------------------------------------------------------

const VALID_DB_NAME = /^[a-z][a-z0-9_]{0,62}$/;

async function createTenantDatabase(dbName: string): Promise<void> {
  if (!VALID_DB_NAME.test(dbName)) {
    throw new Error(`Invalid database name: ${dbName}`);
  }
  const adminPool = new pg.Pool({
    user: PG_USER,
    password: PG_PASSWORD,
    host: PG_HOST,
    port: PG_PORT,
    database: 'postgres',
    max: 2,
    ssl: pgSslConfig(PG_HOST),
  });

  try {
    const exists = await adminPool.query(
      `SELECT 1 FROM pg_database WHERE datname = $1`,
      [dbName],
    );
    if (exists.rowCount === 0) {
      await adminPool.query(`CREATE DATABASE "${dbName}" OWNER "${PG_USER}"`);
    }
  } finally {
    await adminPool.end();
  }

  const tenantPool = new pg.Pool({
    user: PG_USER,
    password: PG_PASSWORD,
    host: PG_HOST,
    port: PG_PORT,
    database: dbName,
    max: 2,
  });

  try {
    let scripts: string[] = [];
    try {
      scripts = readdirSync(INIT_SCRIPTS_DIR)
        .filter((f) => f.endsWith('.sql'))
        .sort();
    } catch {
      console.warn(`[provisioning] Init scripts dir not found: ${INIT_SCRIPTS_DIR}`);
    }

    for (const script of scripts) {
      const sql = readFileSync(join(INIT_SCRIPTS_DIR, script), 'utf-8');
      try {
        await tenantPool.query(sql);
        console.log(`[provisioning] Executed ${script} on ${dbName}`);
      } catch (err) {
        console.warn(`[provisioning] Script ${script} on ${dbName} had errors:`, (err as Error).message);
      }
    }
  } finally {
    await tenantPool.end();
  }
}

// -------------------------------------------------------------------------
// Helper: generate a key via the tokenisation service
// -------------------------------------------------------------------------

async function requestKeyGeneration(tenantId: string, tenantSlug: string, authHeader?: string) {
  // KS-175: forward the calling platform-admin's bearer token. generate-key now
  // requires a platform-level role (SYSTEM_ADMIN/SUPER_ADMIN/...), and tenant
  // creation is always driven by an authenticated platform-admin, so the real
  // admin identity authorises — and is audited on — the new tenant's key. A
  // tenant-scoped user hitting generate-key directly is rejected with 403.
  const res = await fetch(`${TOKENISATION_URL}/api/generate-key`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(authHeader ? { Authorization: authHeader } : {}),
    },
    body: JSON.stringify({ tenantId, tenantSlug }),
    signal: AbortSignal.timeout(KEY_GENERATION_FETCH_TIMEOUT_MS),
  });
  return res.json() as Promise<{
    success: boolean;
    keyFile: Record<string, unknown>;
    keyHash: string;
    error?: { code?: unknown; message?: unknown };
  }>;
}

/** A log-safe account of a key service answer that was not `success: true`: its error code and message only, capped. Nothing else it sent (a hash, a key file) is copied. */
function describeKeyRefusal(answer: { error?: { code?: unknown; message?: unknown } }): string {
  const code = typeof answer.error?.code === 'string' ? answer.error.code : 'no error code';
  const message = typeof answer.error?.message === 'string' ? ` ${answer.error.message}` : '';
  return `${code}${message}`.slice(0, 200);
}

// -------------------------------------------------------------------------
// GET /health
// -------------------------------------------------------------------------

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'tenant-provisioning', version: '1.0.0' });
});

// Pen-test H2 — every /api/* route below this point JWT-verifies the
// bearer token via @secuura/shared's `authenticate()`. Without this,
// downstream services trusted the gateway-injected x-user-* headers,
// which an attacker reaching a service directly (intra-cluster, leaked
// internal endpoint, etc.) could forge.
app.use('/api', jwtAuthenticate());

// -------------------------------------------------------------------------
// POST /api/tenants  — create a new tenant
// -------------------------------------------------------------------------

// F-DEV-TENANT-CRUFT fix (2026-04-29): refuse slugs that are obvious
// test cruft or that contain literal `undefined`/`null`. Without this,
// a shell script with an unset env var (`co-${ENV}`) creates tenants
// named `co-undefined` etc. — Dev had 6 such cruft tenants.
const TENANT_SLUG_BLOCKLIST = /(^|-)(undefined|null)(-|$)|^test(-?[0-9]+)?$|^test-bug/i;
const createTenantSchema = z.object({
  name: z.string().trim().min(1).max(255),
  slug: z
    .string()
    .min(2)
    .max(100)
    .regex(/^[a-z0-9-]+$/)
    .refine((s) => !TENANT_SLUG_BLOCKLIST.test(s), {
      message:
        'Tenant slug looks like test cruft (matches `test-?\\d+`, `test-bug…`, or contains `undefined`/`null`). ' +
        'If this is a real tenant, pick a different slug. If a script is generating slugs from env vars, ensure they are set.',
    }),
  domain: z.string().trim().optional(),
  industry: z.string().trim().optional(),
  country: z.string().trim().optional(),
  test_url: z.string().url().optional().or(z.literal('')),
  live_url: z.string().url().optional().or(z.literal('')),
  contacts: z.array(z.object({
    name: z.string().trim(),
    email: z.string().trim().email(),
    phone: z.string().trim().optional(),
    role: z.string().optional(),
    isPrimary: z.boolean().optional(),
  })).optional(),
});

app.post('/api/tenants', async (req, res) => {
  // KS-211: track the inserted tenant id so a provisioning failure (CREATE
  // DATABASE / key-gen / a later INSERT) rolls back instead of leaving an
  // orphan 'provisioning' tenant (which then blocks retries / pollutes the
  // tenant list). The catch also logs the real cause — it was a silent 500.
  let provisionedTenantId: string | undefined;
  try {
    const body = createTenantSchema.parse(req.body);
    const dbName = `secuura_tenant_${body.slug.replace(/-/g, '_')}`;

    const existing = await platformQuery(
      `SELECT id FROM tenants WHERE slug = $1`,
      [body.slug],
    );
    if (existing.rowCount && existing.rowCount > 0) {
      res.status(409).json({ success: false, error: { code: 'CONFLICT', message: `Tenant with slug "${body.slug}" already exists` } });
      return;
    }

    const tenantResult = await platformQuery<{ id: string }>(
      `INSERT INTO tenants (name, slug, status, domain, industry, country, test_url, live_url)
       VALUES ($1, $2, 'provisioning', $3, $4, $5, $6, $7)
       RETURNING id`,
      [body.name, body.slug, body.domain || null, body.industry || null, body.country || null, body.test_url || null, body.live_url || null],
    );
    const tenantId = tenantResult.rows[0].id;
    provisionedTenantId = tenantId;

    if (body.contacts) {
      for (const c of body.contacts) {
        await platformQuery(
          `INSERT INTO tenant_contacts (tenant_id, name, email, phone, role, is_primary)
           VALUES ($1, $2, $3, $4, $5, $6)`,
          [tenantId, c.name, c.email, c.phone || null, c.role || 'admin', c.isPrimary ?? false],
        );
      }
    }

    // KS-211: per-tenant DATABASE provisioning is gated OFF by default. New
    // tenants use the shared app DB (consistent with existing tenants + the
    // current RLS-inert reality). Building real per-tenant-DB isolation (admin
    // CREATE DATABASE + the connection budget) is KS-160's job — set
    // PROVISION_PER_TENANT_DB=true once that path is ready.
    //
    // Point tenant_config at the shared app DB *via the runtime path* (DATABASE_URL
    // → pgbouncer on Azure), so a trafficked tenant multiplexes through pgbouncer
    // instead of opening a direct connection (KS-207), and the row satisfies the
    // NOT NULL tenant_config schema (local init-platform; Azure's migration is
    // nullable, but non-null is safe for both).
    const provisionPerTenantDb = process.env.PROVISION_PER_TENANT_DB === 'true';
    const appDbUrl = (() => {
      try { return new URL(process.env.DATABASE_URL || ''); } catch { return null; }
    })();
    let cfgDbName: string = appDbUrl?.pathname.replace(/^\//, '') || 'secuura';
    let cfgDbHost: string = appDbUrl?.hostname || PG_HOST;
    let cfgDbPort: number = appDbUrl?.port ? parseInt(appDbUrl.port, 10) : PG_PORT;
    if (provisionPerTenantDb) {
      await createTenantDatabase(dbName);
      cfgDbName = dbName;
      cfgDbHost = PG_HOST;
      cfgDbPort = PG_PORT;
    }

    let keyFile: Record<string, unknown> | null = null;
    let keyHash = '';
    // KS-1240 (option b): true on every path where the key service did not confirm a key, so the 201 can say so.
    let keyPending = false;
    try {
      const keyResult = await requestKeyGeneration(tenantId, body.slug, req.headers.authorization);
      if (keyResult.success) {
        keyFile = keyResult.keyFile;
        keyHash = keyResult.keyHash;
      } else {
        keyPending = true;
        console.warn('[provisioning] Key generation answered not-ok, tenant created with keyPending:', describeKeyRefusal(keyResult), { tenantId, slug: body.slug });
      }
    } catch (err) {
      keyPending = true;
      console.warn('[provisioning] Key generation failed, will need manual generation:', (err as Error).message, { tenantId, slug: body.slug });
    }

    await platformQuery(
      `INSERT INTO tenant_config (tenant_id, db_name, db_host, db_port, vault_key_hash)
       VALUES ($1, $2, $3, $4, $5)`,
      [tenantId, cfgDbName, cfgDbHost, cfgDbPort, keyHash || null],
    );

    await platformQuery(
      `UPDATE tenants SET status = 'active' WHERE id = $1`,
      [tenantId],
    );

    await platformQuery(
      `INSERT INTO platform_audit_log (action, target_type, target_id, details)
       VALUES ('tenant_created', 'tenant', $1, $2)`,
      [tenantId, JSON.stringify({ name: body.name, slug: body.slug, dbName })],
    );

    // KS-336: mint the tenant's Platform-S metering key (Option A onboarding) and
    // return it once, alongside the vault keyFile, so S receives it at signup
    // without holding admin creds. Fail-soft — a mint failure must NOT fail
    // provisioning (the tenant is already active); it can be minted later.
    // Mirrors the keyFile try/catch above.
    let meteringApiKey: MeteringKey | null = null;
    try {
      meteringApiKey = await requestMeteringKey(SECURITY_SERVICE_URL, tenantId, body.slug, req.headers.authorization);
    } catch (err) {
      console.warn('[provisioning] metering key mint failed, will need manual generation:', (err as Error).message);
    }

    res.status(201).json({
      success: true,
      tenant: { id: tenantId, name: body.name, slug: body.slug, status: 'active', dbName: cfgDbName },
      keyFile,
      meteringApiKey,
      keyPending,
      ...(keyPending ? { keyPendingMessage: KEY_PENDING_MESSAGE } : {}),
    });
  } catch (err: unknown) {
    if (err instanceof z.ZodError) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: err.errors } });
      return;
    }
    const message = err instanceof Error ? err.message : String(err);
    // KS-211: surface the real cause — this was a silent 500 (the message was
    // returned to the client but never logged server-side, so it was invisible
    // in Log Analytics). Likely cause on Azure: tenant-provisioning connects to
    // the platform DB as the least-privilege secuura_app role (from
    // PLATFORM_DATABASE_URL), which cannot write the platform tables / CREATE
    // DATABASE — a platform-admin write service needs an admin connection.
    console.error('[provisioning] POST /api/tenants failed:', message, err instanceof Error ? err.stack : '');
    // Roll back a partially-created tenant so it doesn't orphan or block retries.
    if (provisionedTenantId) {
      try {
        await platformQuery(`DELETE FROM tenant_config WHERE tenant_id = $1`, [provisionedTenantId]);
        await platformQuery(`DELETE FROM tenant_contacts WHERE tenant_id = $1`, [provisionedTenantId]);
        await platformQuery(`DELETE FROM tenants WHERE id = $1`, [provisionedTenantId]);
        console.error(`[provisioning] rolled back partially-created tenant ${provisionedTenantId}`);
      } catch (cleanupErr) {
        console.error('[provisioning] cleanup of partial tenant failed:', (cleanupErr as Error).message);
      }
    }
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
  }
});

// -------------------------------------------------------------------------
// GET /api/tenants  — list all tenants
// -------------------------------------------------------------------------

app.get('/api/tenants', async (_req, res) => {
  try {
    const result = await platformQuery(
      `SELECT t.*, tc.db_name, tc.db_host, tc.db_port
       FROM tenants t
       LEFT JOIN tenant_config tc ON tc.tenant_id = t.id
       ORDER BY t.created_at DESC`,
    );
    res.json({ success: true, tenants: result.rows, total: result.rowCount });
  } catch (err: unknown) {
    // Return 400 for validation errors, 500 for everything else
    if (err instanceof z.ZodError) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: err.errors } });
      return;
    }
    const message = err instanceof Error ? err.message : String(err);
    console.error('[provisioning] GET /api/tenants failed:', message);
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

// -------------------------------------------------------------------------
// :id param guard — KS-497 (see src/tenantIdParam.ts for the rationale)
// -------------------------------------------------------------------------
app.param('id', tenantIdParamGuard);

// -------------------------------------------------------------------------
// GET /api/tenants/:id
// -------------------------------------------------------------------------

app.get('/api/tenants/:id', async (req, res) => {
  try {
    const tenant = await platformQuery(
      `SELECT t.*, tc.db_name, tc.db_host, tc.db_port, tc.token_location_type, tc.token_location_path
       FROM tenants t
       LEFT JOIN tenant_config tc ON tc.tenant_id = t.id
       WHERE t.id = $1`,
      [req.params.id],
    );
    if (tenant.rowCount === 0) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Tenant not found' } });
      return;
    }

    const contacts = await platformQuery(
      `SELECT * FROM tenant_contacts WHERE tenant_id = $1`,
      [req.params.id],
    );

    res.json({
      success: true,
      tenant: tenant.rows[0],
      contacts: contacts.rows,
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error('[provisioning] GET /api/tenants/:id failed:', message);
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

// -------------------------------------------------------------------------
// PATCH /api/tenants/:id/status  — suspend / activate / archive
// -------------------------------------------------------------------------

// KS-1860: the statuses each target may be reached from, in the order docs/MULTI-TENANCY.md draws
// (provisioning -> active -> suspended -> archived, and reactivation from suspended). Any other move, archived ->
// active included, answers 409.
// KS-1861: archived -> suspended is allowed too, so an archive is reversible through the API (Kam, 2026-11-01 10:05:44
// AEDT, card secuura-ks1861-archive-from-which-status-1101: "b — As (a), and archived can go back to suspended").
const STATUS_REACHABLE_FROM: Record<string, string[]> = {
  active: ['provisioning', 'suspended'],
  suspended: ['active', 'archived'],
  archived: ['suspended'],
};

app.patch('/api/tenants/:id/status', async (req, res) => {
  try {
    const { status } = req.body;
    if (!['active', 'suspended', 'archived'].includes(status)) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid status' } });
      return;
    }

    // One conditional statement, so the check and the write cannot be split by a concurrent change.
    const updated = await platformQuery(
      `UPDATE tenants SET status = $1, updated_at = now() WHERE id = $2 AND status = ANY($3::text[])`,
      [status, req.params.id, STATUS_REACHABLE_FROM[status]],
    );
    if (!updated.rowCount) {
      const current = await platformQuery<{ status: string }>(
        `SELECT status FROM tenants WHERE id = $1`,
        [req.params.id],
      );
      if (current.rowCount === 0) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Tenant not found' } });
        return;
      }
      res.status(409).json({
        success: false,
        error: { code: 'CONFLICT', message: `Cannot change tenant status from ${current.rows[0].status} to ${status}` },
      });
      return;
    }

    await platformQuery(
      `INSERT INTO platform_audit_log (action, target_type, target_id, details)
       VALUES ('tenant_status_changed', 'tenant', $1, $2)`,
      [req.params.id, JSON.stringify({ status })],
    );

    res.json({ success: true, status });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error('[provisioning] PATCH /api/tenants/:id/status failed:', message);
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

// -------------------------------------------------------------------------
// PATCH /api/tenants/:id  — update tenant fields
// -------------------------------------------------------------------------

const updateTenantSchema = z.object({
  name: z.string().trim().min(1).max(255).optional(),
  domain: z.string().trim().optional(),
  industry: z.string().trim().optional(),
  country: z.string().trim().optional(),
  test_url: z.string().url().optional().or(z.literal('')).or(z.null()),
  live_url: z.string().url().optional().or(z.literal('')).or(z.null()),
});

app.patch('/api/tenants/:id', async (req, res) => {
  try {
    const body = updateTenantSchema.parse(req.body);
    const sets: string[] = [];
    const vals: unknown[] = [];
    let idx = 1;

    for (const [key, value] of Object.entries(body)) {
      if (value !== undefined) {
        sets.push(`${key} = $${idx}`);
        vals.push(value === '' ? null : value);
        idx++;
      }
    }

    if (sets.length === 0) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'No fields to update' } });
      return;
    }

    sets.push(`updated_at = now()`);
    vals.push(req.params.id);

    await platformQuery(
      `UPDATE tenants SET ${sets.join(', ')} WHERE id = $${idx}`,
      vals,
    );

    await platformQuery(
      `INSERT INTO platform_audit_log (action, target_type, target_id, details)
       VALUES ('tenant_updated', 'tenant', $1, $2)`,
      [req.params.id, JSON.stringify(body)],
    );

    res.json({ success: true });
  } catch (err: unknown) {
    // KS-497: a body failing updateTenantSchema threw a ZodError that fell
    // into the generic handler → raw 500. Map it to the declared 400, the
    // same shape the list route already uses.
    if (err instanceof z.ZodError) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: err.errors } });
      return;
    }
    const message = err instanceof Error ? err.message : String(err);
    console.error('[provisioning] PATCH /api/tenants/:id failed:', message);
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

// -------------------------------------------------------------------------
// DELETE /api/tenants/:id  — archive (requires confirmation)
// -------------------------------------------------------------------------

// KS-1861 (Kam, card secuura-ks1861-what-tenant-delete-means-1031, a: "Archive, not erase"): DELETE sets the tenant's
// status to archived and keeps every row. Nothing is deleted and no database is dropped, whatever
// PROVISION_PER_TENANT_DB says; erasure is not built.
const ARCHIVABLE_FROM = ['provisioning', 'active', 'suspended'];

app.delete('/api/tenants/:id', async (req, res) => {
  try {
    const { confirm } = req.body || {};
    if (confirm !== true) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Set "confirm": true in the request body to delete' } });
      return;
    }

    const tenant = await platformQuery<{ slug: string; status: string }>(
      `SELECT slug, status FROM tenants WHERE id = $1`,
      [req.params.id],
    );
    if (tenant.rowCount === 0) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Tenant not found' } });
      return;
    }
    const { slug, status: previousStatus } = tenant.rows[0];
    if (!ARCHIVABLE_FROM.includes(previousStatus)) {
      const message = previousStatus === 'archived' ? 'Tenant is already archived' : `Cannot archive a tenant whose status is ${previousStatus}`;
      res.status(409).json({ success: false, error: { code: 'CONFLICT', message } });
      return;
    }

    // The status change and its audit row commit together, or neither does. The update only matches the status read
    // above, so a concurrent change answers 409 instead of being overwritten.
    let archived = false;
    const client = await platformPool.connect();
    try {
      await client.query('BEGIN');
      const updated = await client.query(
        `UPDATE tenants SET status = 'archived', updated_at = now() WHERE id = $1 AND status = $2`,
        [req.params.id, previousStatus],
      );
      if (updated.rowCount) {
        await client.query(
          `INSERT INTO platform_audit_log (action, target_type, target_id, details)
           VALUES ('tenant_archived', 'tenant', $1, $2)`,
          [req.params.id, JSON.stringify({ slug, previousStatus, erased: false })],
        );
        archived = true;
      }
      await client.query(archived ? 'COMMIT' : 'ROLLBACK');
    } catch (err) {
      await client.query('ROLLBACK').catch((rollbackErr: unknown) => {
        console.error('[provisioning] DELETE /api/tenants/:id rollback failed:', rollbackErr instanceof Error ? rollbackErr.message : String(rollbackErr));
      });
      throw err;
    } finally {
      client.release();
    }
    if (!archived) {
      res.status(409).json({ success: false, error: { code: 'CONFLICT', message: 'Tenant status changed while archiving; nothing was changed' } });
      return;
    }

    res.json({
      success: true,
      deleted: false,
      archived: true,
      status: 'archived',
      message: 'Tenant archived. No data was removed: every row is kept and no database is dropped.',
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    // Ruling 1 (KS-1861): the audit log records a failed attempt too. Its own failure is logged, never silent.
    await platformQuery(
      `INSERT INTO platform_audit_log (action, target_type, target_id, details)
       VALUES ('tenant_archive_failed', 'tenant', $1, $2)`,
      [req.params.id, JSON.stringify({ erased: false })],
    ).catch((auditErr: unknown) => {
      console.error('[provisioning] DELETE /api/tenants/:id could not audit the failure:', auditErr instanceof Error ? auditErr.message : String(auditErr));
    });
    console.error('[provisioning] DELETE /api/tenants/:id failed:', message);
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

// -------------------------------------------------------------------------
// GET /api/audit-log  — platform audit log
// -------------------------------------------------------------------------

app.get('/api/audit-log', async (req, res) => {
  try {
    const limit = Math.min(parseInt(req.query.limit as string) || 50, 200);
    const offset = parseInt(req.query.offset as string) || 0;
    const result = await platformQuery(
      `SELECT * FROM platform_audit_log ORDER BY created_at DESC, id DESC LIMIT $1 OFFSET $2`,
      [limit, offset],
    );
    const countResult = await platformQuery(`SELECT COUNT(*) as total FROM platform_audit_log`);
    res.json({ success: true, entries: result.rows, total: parseInt(countResult.rows[0].total) });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error('[provisioning] GET /api/audit-log failed:', message);
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

// -------------------------------------------------------------------------
// START
// -------------------------------------------------------------------------

try {
  await platformPool.query('SELECT 1');
  console.log('[provisioning] Platform DB connected');
} catch {
  console.warn('[provisioning] Platform DB not available — will retry on first request');
}

// KS-111: final AppError-aware handler — thrown AppErrors (and unknowns) get the
// canonical {success,error} JSON + correct status instead of Express's HTML 500.
app.use(errorHandler);

const server = app.listen(PORT, () => {

  console.log(`[provisioning] Listening on port ${PORT}`);
});
// KS-252: hold keep-alive sockets longer than any upstream proxy's idle
// window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
// sockets; Node's 5 s default close races their reuse -> ECONNRESET and
// 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;
