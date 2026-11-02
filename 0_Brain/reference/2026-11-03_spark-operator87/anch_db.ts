/**
 * =============================================================================
 * DATABASE CLIENT — Anchoring Service
 * =============================================================================
 * Lightweight PostgreSQL connection using the `pg` library.
 * Falls back gracefully if the database is unavailable, allowing the service
 * to function in degraded mode with in-memory storage.
 * =============================================================================
 */

import { Pool, PoolClient, QueryResult, QueryResultRow } from 'pg';

let pool: Pool | null = null;
let dbAvailable = false;

function dbLog(level: 'info' | 'warn' | 'error', message: string, meta?: object) {
  const ts = new Date().toISOString();
  console.log(JSON.stringify({ timestamp: ts, level, service: 'anchoring-db', message, ...meta }));
}

export function getPool(): Pool {
  if (!pool) {
    const databaseUrl = process.env.DATABASE_URL;
    if (!databaseUrl) {
      dbLog('warn', 'DATABASE_URL not set — running with in-memory storage only');
      throw new Error('DATABASE_URL not configured');
    }
    pool = new Pool({
      connectionString: databaseUrl,
      max: 10,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 5000,
    });

    pool.on('error', (err: Error) => {
      dbLog('error', 'DB pool unexpected error', { error: err.message });
    });
  }
  return pool;
}

export async function query<T extends QueryResultRow = QueryResultRow>(
  text: string,
  params?: unknown[],
): Promise<QueryResult<T>> {
  return getPool().query<T>(text, params);
}

export async function getClient(): Promise<PoolClient> {
  return getPool().connect();
}

export async function transaction<T>(fn: (client: PoolClient) => Promise<T>): Promise<T> {
  const client = await getClient();
  try {
    await client.query('BEGIN');
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

// =============================================================================
// AVAILABILITY PROBE + BACKGROUND RETRY (KS-377)
// =============================================================================
// A failed probe at boot must never latch the service into degraded mode for
// its lifetime: losing the compose/ACA start race against Postgres used to
// leave a healthy-looking service whose writes 202'd but never persisted.
// Every DB-gated code path re-reads isDbAvailable() per call, so flipping the
// flag when a background re-probe succeeds is all recovery takes (schema DDL
// is ensured lazily by callers / owned by the migration path).

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
      dbLog('info', 'Database connection established (recovered after retry)', {
        attempts: retryAttempts,
      });
      retryAttempts = 0;
      retryDelayMs = DB_RETRY_INITIAL_MS;
    } else {
      retryDelayMs = Math.min(retryDelayMs * 2, DB_RETRY_MAX_MS);
      dbLog('warn', 'Database still unavailable — will retry', {
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
    dbLog('warn', 'DATABASE_URL not set — running with in-memory storage only');
    return false;
  }
  const probe = await probeDb();
  if (probe.ok) {
    dbLog('info', 'Database connection established');
  } else {
    dbLog('warn', 'Database unavailable — using in-memory fallback until it comes up, retrying in background (KS-377)', {
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
    dbLog('info', 'Database connection closed');
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
