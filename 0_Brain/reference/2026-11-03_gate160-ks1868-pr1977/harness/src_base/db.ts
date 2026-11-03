/**
 * =============================================================================
 * DATABASE CLIENT — Auth Service
 * =============================================================================
 * Lightweight PostgreSQL connection using the `pg` library.
 * Falls back gracefully if the database is unavailable, allowing the service
 * to function in degraded mode with in-memory storage.
 * =============================================================================
 */

import { Pool, PoolClient, QueryResult, QueryResultRow } from 'pg';
import { applyTenantGuc, queryWithTenantGuc, runWithTenantId } from '@secuura/shared';
import { logger } from './utils/logger';

let pool: Pool | null = null;
let dbAvailable = false;

export function getPool(): Pool {
  if (!pool) {
    const databaseUrl = process.env.DATABASE_URL;
    if (!databaseUrl) {
      logger.warn('DATABASE_URL not set — running with in-memory storage only');
      throw new Error('DATABASE_URL not configured');
    }
    // KS-254: pool size and acquisition timeout are env-tunable, and the
    // acquisition timeout defaults to 2 s (was 5 s) so a login that can't get
    // a connection fails fast — KS-253's classifier turns that into a 503 —
    // instead of queueing behind the pool. Pool max stays 10 by default:
    // auth sits behind pgbouncer, and fanning per-instance pools out past
    // the fronting pgbouncer's ceiling is the KS-213 failure mode.
    const poolMax = parseInt(process.env.AUTH_DB_POOL_MAX ?? '', 10) || 10;
    const connectTimeoutMs = parseInt(process.env.AUTH_DB_CONNECT_TIMEOUT_MS ?? '', 10) || 2000;
    pool = new Pool({
      connectionString: databaseUrl,
      max: poolMax,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: connectTimeoutMs,
    });

    pool.on('error', (err: Error) => {
      logger.error('DB pool unexpected error', { error: err.message });
    });
  }
  return pool;
}

export async function query<T extends QueryResultRow = QueryResultRow>(
  text: string,
  params?: unknown[],
  tenantId?: string,
): Promise<QueryResult<T>> {
  // If multi-tenancy is enabled and a tenantId is provided, use the tenant pool
  if (tenantId && tenantManager) {
    try {
      const tenantPool = tenantManager.getPool(tenantId);
      return tenantPool.query(text, params) as Promise<QueryResult<T>>;
    } catch {
      // Fall back to default pool
    }
  }
  // KS-458: an explicit tenantId (callers that know the target row's tenant,
  // e.g. writes after a pre-auth lookup) overrides the request ALS context;
  // otherwise the wrapper reads the ALS seeded by tenantGucContext(). Either
  // way the GUC is bundled into the same transaction as the statement, which
  // fail-closed RLS requires.
  if (tenantId) {
    return runWithTenantId(tenantId, () => queryWithTenantGuc<T>(getPool(), text, params));
  }
  return queryWithTenantGuc<T>(getPool(), text, params);
}

export async function getClient(): Promise<PoolClient> {
  return getPool().connect();
}

export async function transaction<T>(fn: (client: PoolClient) => Promise<T>): Promise<T> {
  const client = await getClient();
  try {
    await client.query('BEGIN');
    // KS-458: fail-closed RLS — the tenant GUC must live inside this
    // transaction for the callback's statements to see tenant rows.
    await applyTenantGuc(client);
    const result = await fn(client);
    await client.query('COMMIT');
    return result;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

/** Ensure required columns exist on the users table (idempotent migration) */
async function ensureUserColumns(): Promise<void> {
  // KS-110: these columns are now owned by the migration path
  // (migrations/030_auth_user_columns.sql), applied by the api-gateway as the
  // table owner. The runtime connects as the least-privilege `secuura_app` role
  // (KS-109), which can't ALTER `users` (owner-only) — attempting it just throws
  // "must be owner" and is swallowed below. Skip cleanly when we lack CREATE on
  // schema public (i.e. the non-owner runtime role).
  try {
    const probe = await getPool().query("SELECT has_schema_privilege(current_user, 'public', 'CREATE') AS ok");
    if (!((probe.rows?.[0] as any)?.ok)) {
      logger.info('Skipping runtime user-column DDL — least-privilege role; migration path owns it (KS-110)');
      return;
    }
  } catch {
    // Probe failed — fall through to the original best-effort behaviour.
  }
  const migrations = [
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS display_name VARCHAR(200)',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(50)',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_verified BOOLEAN DEFAULT FALSE',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_backup_codes TEXT[]',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS wallet_address VARCHAR(255)',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_method VARCHAR(20) DEFAULT \'email\'',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMP WITH TIME ZONE',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS organization_id UUID',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR(255)',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS linkedin_id VARCHAR(255)',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS facebook_id VARCHAR(255)',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS apple_id VARCHAR(255)',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS github_id VARCHAR(255)',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS microsoft_personal_id VARCHAR(255)',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS tenant_id UUID',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS tenant_slug VARCHAR(100)',
    // Audit 1.3 phase 2: phone_number is now stored as AES-GCM ciphertext
    // (`v1:iv:tag:ciphertext`, ~120-200 chars depending on plaintext length).
    // Widen from VARCHAR(50) to TEXT so the ciphertext fits. Pre-existing
    // plaintext values stay intact and are upgraded on next user update.
    'ALTER TABLE users ALTER COLUMN phone_number TYPE TEXT',
    // Audit 1.3 phase 3: same treatment for the name columns.
    'ALTER TABLE users ALTER COLUMN first_name TYPE TEXT',
    'ALTER TABLE users ALTER COLUMN last_name TYPE TEXT',
    'ALTER TABLE users ALTER COLUMN display_name TYPE TEXT',
    // Audit 1.3 phase 4a: encrypt email AND add HMAC lookup column.
    // Email becomes ciphertext (~140 chars) so widen + drop UNIQUE on it
    // (encryption is non-deterministic, the constraint can't enforce
    // anything useful any more). Lookup queries use the new
    // email_lookup_hash column which IS deterministic and indexed.
    'ALTER TABLE users ALTER COLUMN email TYPE TEXT',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS email_lookup_hash VARCHAR(64)',
    // Drop old UNIQUE on email (the constraint name is the auto-generated
    // pg default — try both common variants).
    'ALTER TABLE users DROP CONSTRAINT IF EXISTS users_email_key',
    'ALTER TABLE users DROP CONSTRAINT IF EXISTS users_email_unique',
    // New uniqueness invariant lives on the hash column. CONCURRENTLY isn't
    // an option inside a transaction; the dev DB is small enough that a
    // brief lock is fine.
    'CREATE UNIQUE INDEX IF NOT EXISTS users_email_lookup_hash_uniq ON users(email_lookup_hash) WHERE email_lookup_hash IS NOT NULL',
    'CREATE INDEX IF NOT EXISTS users_email_lookup_hash_idx ON users(email_lookup_hash)',
  ];

  for (const sql of migrations) {
    try {
      await getPool().query(sql);
    } catch (err: any) {
      // Ignore errors (e.g., table doesn't exist yet, or constraint issues)
      logger.debug('Column migration skipped', { sql: sql.substring(0, 60), error: err?.message });
    }
  }
  logger.info('User column migrations applied');
}

// =============================================================================
// AVAILABILITY PROBE + BACKGROUND RETRY (KS-377)
// =============================================================================
// A failed probe at boot must never latch the service into degraded mode for
// its lifetime: losing the compose/ACA start race against Postgres used to
// leave a healthy-looking service whose writes 202'd but never persisted.
// Every DB-gated code path re-reads isDbAvailable() per call, so flipping the
// flag when a background re-probe succeeds is almost all recovery takes —
// plus re-running ensureUserColumns(), the one-shot boot work the lost race
// skipped (best-effort user-column DDL, KS-110).

const DB_RETRY_INITIAL_MS = 1_000;
const DB_RETRY_MAX_MS = 30_000;
let retryDelayMs = DB_RETRY_INITIAL_MS;
let retryAttempts = 0;
let retryTimer: ReturnType<typeof setTimeout> | null = null;

async function probeDb(): Promise<{ ok: boolean; error?: string }> {
  try {
    const result = await query<{ ok: number }>('SELECT 1 AS ok');
    dbAvailable = result.rows[0]?.ok === 1;
    return { ok: dbAvailable };
  } catch (err: any) {
    dbAvailable = false;
    return { ok: false, error: err?.message };
  }
}

function scheduleRetry(): void {
  if (retryTimer || dbAvailable) return;
  retryTimer = setTimeout(async () => {
    retryTimer = null;
    retryAttempts += 1;
    const probe = await probeDb();
    if (probe.ok) {
      // The boot success path runs ensureUserColumns(); a recovery must too,
      // or a lost boot race silently skips the best-effort user-column DDL
      // (KS-110) until a manual restart.
      await ensureUserColumns();
      logger.info('Database connection established (recovered after retry)', {
        attempts: retryAttempts,
      });
      retryAttempts = 0;
      retryDelayMs = DB_RETRY_INITIAL_MS;
    } else {
      retryDelayMs = Math.min(retryDelayMs * 2, DB_RETRY_MAX_MS);
      logger.warn('Database still unavailable — will retry', {
        error: probe.error,
        attempt: retryAttempts,
        nextRetryMs: retryDelayMs,
      });
      scheduleRetry();
    }
  }, retryDelayMs);
  // A pending probe must never hold the process open (shutdown, tests).
  retryTimer.unref?.();
}

/**
 * Test the database connection and set the availability flag.
 * On failure, keeps re-probing in the background with capped backoff (KS-377)
 * instead of latching degraded mode until a manual restart.
 */
export async function initDb(): Promise<boolean> {
  if (!process.env.DATABASE_URL) {
    // Missing config, not a boot race — retrying can never succeed.
    logger.warn('DATABASE_URL not set — running with in-memory storage only');
    return false;
  }
  const probe = await probeDb();
  if (probe.ok) {
    logger.info('Database connection established');
    await ensureUserColumns();
  } else {
    logger.warn('Database unavailable — using in-memory fallback until it comes up, retrying in background (KS-377)', {
      error: probe.error,
      nextRetryMs: retryDelayMs,
    });
    scheduleRetry();
  }
  return dbAvailable;
}

export function isDbAvailable(): boolean {
  return dbAvailable;
}

export async function closeDb(): Promise<void> {
  if (retryTimer) {
    clearTimeout(retryTimer);
    retryTimer = null;
  }
  if (pool) {
    await pool.end();
    pool = null;
    dbAvailable = false;
    logger.info('Database connection closed');
  }
}

// =============================================================================
// MULTI-TENANCY SUPPORT
// =============================================================================
// When MULTI_TENANCY_ENABLED=true, provides tenant-aware pool routing.
// When false (default), all functions use the existing default pool.

let TenantPoolManager: any;
try { TenantPoolManager = require('@secuura/shared').TenantPoolManager; } catch { /* shared package not available */ }

let tenantManager: any = null;

export function getTenantManager(): any {
  return tenantManager;
}

export async function initTenantManager(): Promise<void> {
  if (process.env.MULTI_TENANCY_ENABLED !== 'true') return;
  const platformUrl = process.env.PLATFORM_DATABASE_URL;
  if (!platformUrl) return;
  const dbUrl = process.env.DATABASE_URL || '';
  if (!TenantPoolManager) return;
  tenantManager = new TenantPoolManager({
    platformDatabaseUrl: platformUrl,
    defaultDatabaseUrl: dbUrl,
  });
  await tenantManager.init();
}

export function getTenantPool(tenantId?: string): any {
  if (!tenantManager || !tenantId) return null;
  return tenantManager.getPool(tenantId);
}
