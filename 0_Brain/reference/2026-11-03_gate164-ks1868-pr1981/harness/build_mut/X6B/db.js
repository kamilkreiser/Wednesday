"use strict";
/**
 * =============================================================================
 * DATABASE CLIENT — security Service
 * =============================================================================
 * Lightweight PostgreSQL connection using the `pg` library.
 * Falls back gracefully if the database is unavailable, allowing the service
 * to function in degraded mode with in-memory storage.
 * =============================================================================
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.getPool = getPool;
exports.query = query;
exports.getClient = getClient;
exports.transaction = transaction;
exports.initDb = initDb;
exports.isDbAvailable = isDbAvailable;
exports.closeDb = closeDb;
exports.getTenantManager = getTenantManager;
exports.initTenantManager = initTenantManager;
exports.getTenantPool = getTenantPool;
const pg_1 = require("pg");
const shared_1 = require("@secuura/shared");
let pool = null;
let dbAvailable = false;
function dbLog(level, message, meta) {
    const ts = new Date().toISOString();
    console.log(JSON.stringify({ timestamp: ts, level, service: 'security-db', message, ...meta }));
}
function getPool() {
    if (!pool) {
        const databaseUrl = process.env.DATABASE_URL;
        if (!databaseUrl) {
            dbLog('warn', 'DATABASE_URL not set — running with in-memory storage only');
            throw new Error('DATABASE_URL not configured');
        }
        pool = new pg_1.Pool({
            connectionString: databaseUrl,
            max: 10,
            idleTimeoutMillis: 30000,
            connectionTimeoutMillis: 5000,
        });
        pool.on('error', (err) => {
            let reason;
            try {
                const m = err?.message;
                reason = m === undefined || m === null ? m : String(m);
            }
            catch {
                reason = 'unreadable thrown value';
            }
            dbLog('error', 'DB pool unexpected error', { error: reason });
        });
    }
    return pool;
}
async function query(text, params) {
    // KS-458: fail-closed RLS — bundle the request's tenant GUC (seeded by
    // tenantGucContext() in index.ts, or an explicit runWithTenantId/
    // runWithPlatformScope wrapper) into the same transaction as the statement.
    // Without a scope this degrades to a plain pool.query, which under
    // fail-closed policies returns zero tenant-scoped rows — the fail-safe.
    return (0, shared_1.queryWithTenantGuc)(getPool(), text, params);
}
async function getClient() {
    return getPool().connect();
}
async function transaction(fn) {
    const client = await getClient();
    try {
        await client.query('BEGIN');
        const result = await fn(client);
        await client.query('COMMIT');
        return result;
    }
    catch (err) {
        await client.query('ROLLBACK');
        throw err;
    }
    finally {
        client.release();
    }
}
// =============================================================================
// AVAILABILITY PROBE + BACKGROUND RETRY (KS-377)
// =============================================================================
// A failed probe at boot must never latch the service into degraded mode for
// its lifetime: losing the compose/ACA start race against Postgres used to
// leave a healthy-looking service serving its in-memory fallback until a
// manual restart. Every DB-gated code path re-reads isDbAvailable() per call,
// so flipping the flag when a background re-probe succeeds restores steady
// state — and the one-shot boot work registered via initDb's onReady hook
// (cache warm / idempotent migration) is re-run too, so recovery is complete
// rather than just the flag flip (KS-382).
const DB_RETRY_INITIAL_MS = 1_000;
const DB_RETRY_MAX_MS = 30_000;
let retryDelayMs = DB_RETRY_INITIAL_MS;
let retryAttempts = 0;
let retryTimer = null;
let onDbReady = null;
async function runDbReadyHook() {
    if (!onDbReady)
        return;
    try {
        await onDbReady();
    }
    catch (err) {
        let reason;
        try {
            const m = err?.message;
            reason = m === undefined || m === null ? m : String(m);
        }
        catch {
            reason = 'unreadable thrown value';
        }
        // Boot work failing must not un-flag an otherwise reachable DB.
        dbLog('error', 'DB ready boot work failed', { error: reason });
    }
}
async function probeDb() {
    try {
        const result = await query('SELECT 1 AS ok');
        dbAvailable = result.rows[0]?.ok === 1;
        return { ok: dbAvailable };
    }
    catch (err) {
        dbAvailable = false;
        let reason;
        try {
            const m = err?.message;
            reason = m === undefined || m === null ? m : String(m);
        }
        catch {
            reason = 'unreadable thrown value';
        }
        return { ok: false, error: reason };
    }
}
function scheduleRetry() {
    if (retryTimer || dbAvailable)
        return;
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
            // Recovery is more than the flag flip: run the boot work that was
            // skipped while the DB was down (cache warm / migration) (KS-382).
            await runDbReadyHook();
        }
        else {
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
 * instead of latching degraded mode until a manual restart. Optional onReady
 * boot work runs on the success path — at boot or on later recovery (KS-382).
 */
async function initDb(onReady) {
    if (onReady)
        onDbReady = onReady;
    if (!process.env.DATABASE_URL) {
        // Missing config, not a boot race — retrying can never succeed.
        dbLog('warn', 'DATABASE_URL not set — running with in-memory storage only');
        return false;
    }
    const probe = await probeDb();
    if (probe.ok) {
        dbLog('info', 'Database connection established');
        await runDbReadyHook();
    }
    else {
        dbLog('warn', 'Database unavailable — using in-memory fallback until it comes up, retrying in background (KS-377)', {
            error: probe.error,
            nextRetryMs: retryDelayMs,
        });
        scheduleRetry();
    }
    return dbAvailable;
}
function isDbAvailable() {
    return dbAvailable;
}
async function closeDb() {
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
let TenantPoolManager;
try {
    TenantPoolManager = require('@secuura/shared').TenantPoolManager;
}
catch { /* shared package not available */ }
let tenantManager = null;
function getTenantManager() {
    return tenantManager;
}
async function initTenantManager() {
    if (process.env.MULTI_TENANCY_ENABLED !== 'true')
        return;
    const platformUrl = process.env.PLATFORM_DATABASE_URL;
    if (!platformUrl)
        return;
    const dbUrl = process.env.DATABASE_URL || '';
    if (!TenantPoolManager)
        return;
    tenantManager = new TenantPoolManager({
        platformDatabaseUrl: platformUrl,
        defaultDatabaseUrl: dbUrl,
    });
    await tenantManager.init();
}
function getTenantPool(tenantId) {
    if (!tenantManager || !tenantId)
        return null;
    return tenantManager.getPool(tenantId);
}
