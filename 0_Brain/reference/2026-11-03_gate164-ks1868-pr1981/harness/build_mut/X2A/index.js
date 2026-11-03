"use strict";
/**
 * =============================================================================
 * SECUURA SECURITY SERVICE
 * =============================================================================
 * Handles:
 * - Audit logging
 * - Security event tracking
 * - Rate limit management
 * - API key validation
 * Port: 4004
 * =============================================================================
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.adminScopeGetQuerySchema = exports.adminScopePutSchema = exports.adminScopeParamsSchema = exports.checkRateLimitSchema = exports.persistableResetAt = exports.usableRateLimitEntry = exports.MAX_RATE_LIMIT_WINDOW_MS = exports.isRepresentableInstant = exports.rowToApiKey = exports.rowToSecurityEvent = exports.parseJsonArray = exports.parseJson = exports.rotateChains = exports.rateLimits = exports.memApiKeys = void 0;
exports.revokePriorConnectorKeys = revokePriorConnectorKeys;
exports.withConnectorChain = withConnectorChain;
exports.saveKeyAndRetirePriors = saveKeyAndRetirePriors;
exports.rowToAuditLog = rowToAuditLog;
exports.loadFromDb = loadFromDb;
// KS-1725: FIRST import, before any module that could parse: installs the zod 3 compatible issue map
// (zod 4 error map; see packages/shared/src/validation/zod3-compat.ts) for this whole process.
require("@secuura/shared/zod3-compat");
const express_1 = __importDefault(require("express"));
const shared_1 = require("@secuura/shared"); // KS-1724: express.json plus the structural caps (array length, node count, depth)
const cors_1 = __importDefault(require("cors"));
const helmet_1 = __importDefault(require("helmet"));
const zod_1 = require("zod");
const crypto_1 = __importDefault(require("crypto"));
const dotenv_1 = __importDefault(require("dotenv"));
const db_1 = require("./db");
const logger_1 = require("./utils/logger");
const requestSchemas_1 = require("./requestSchemas");
const requestRefusal_1 = require("./requestRefusal");
// KS-480 §4 amendment: provisioning mint policy (bootless, unit-tested).
const provisioningPolicy_1 = require("./provisioningPolicy");
const shared_2 = require("@secuura/shared");
const rateLimitBounds_1 = require("./rateLimitBounds");
const rateLimitScope_1 = require("./rateLimitScope");
const keyRevokePolicy_1 = require("./keyRevokePolicy");
const adminScope_1 = require("./adminScope");
// KS-880: the single home of the row mappers and their types (see the ROW CONVERTERS section below).
const converters_1 = require("./converters");
Object.defineProperty(exports, "parseJson", { enumerable: true, get: function () { return converters_1.parseJson; } });
Object.defineProperty(exports, "parseJsonArray", { enumerable: true, get: function () { return converters_1.parseJsonArray; } });
Object.defineProperty(exports, "rowToSecurityEvent", { enumerable: true, get: function () { return converters_1.rowToSecurityEvent; } });
Object.defineProperty(exports, "rowToApiKey", { enumerable: true, get: function () { return converters_1.rowToApiKey; } });
// KS-1725: zod 4 issues rendered in zod 3.25.76's shape for every response (the client contract unchanged).
const zod3_compat_1 = require("@secuura/shared/zod3-compat");
// =============================================================================
// PII FOR audit_logs.details (audit 1.3 phase 5)
// =============================================================================
// audit_logs.details often contains user-supplied input (request bodies,
// query strings, error context). Encrypt the JSONB blob at rest with AAD
// bound to (auditLogId). The column is widened from JSONB to TEXT in the
// startup migration.
function encryptDetails(details, auditId) {
    if (details == null)
        return null;
    const json = JSON.stringify(details);
    if (json === '{}' || json === 'null')
        return null;
    return (0, shared_2.encryptField)(json, `audit_logs.details.${auditId}`);
}
function decryptDetails(stored, auditId) {
    if (stored == null || stored === '')
        return null;
    if (typeof stored === 'string' && /^v\d+:/.test(stored)) {
        try {
            const plain = (0, shared_2.decryptField)(stored, `audit_logs.details.${auditId}`);
            return plain ? JSON.parse(plain) : null;
        }
        catch (err) {
            logger_1.logger.error('[piiCrypto] audit_logs.details decrypt failed', { auditId, error: err?.message });
            return null;
        }
    }
    // Legacy plaintext (still raw JSON or already-parsed object)
    if (typeof stored === 'string') {
        try {
            return JSON.parse(stored);
        }
        catch {
            return null;
        }
    }
    return stored;
}
dotenv_1.default.config();
// Production startup guard — refuse to start with dev defaults in production
(0, shared_2.enforceProductionConfig)('security', {
    requiredEnvVars: ['DATABASE_URL'],
    forbiddenValues: {},
    requireRealProviders: true,
});
const app = (0, express_1.default)();
const PORT = process.env.PORT || 4004;
// =============================================================================
// IN-MEMORY STORAGE (with database persistence fallback)
// =============================================================================
const memAuditLogs = [];
const memSecurityEvents = [];
// KS-577: exported as a test seam; see revokePriorConnectorKeys.
exports.memApiKeys = new Map();
// KS-698: exported as a test seam (see isRepresentableInstant).
exports.rateLimits = new Map(); // Ephemeral - memory only
// =============================================================================
// DATABASE HELPERS
// =============================================================================
/**
 * KS-1570 PR B: the audit_logs INSERT for a SYSTEM-GENERATED audit row (the admin-scope write), run on the
 * caller's own transaction client so a failure rolls the change back.
 *
 * Deliberately NOT dbSaveAuditLog's statement, which is unchanged below, for two measured reasons:
 *   - it names `previous_state` and `new_state`, which no schema source defines (docker/init/01-schema.sql,
 *     migrations/001; only prisma/schema.prisma has them), so on a database built from the repo it always
 *     fails, and dbSaveAuditLog swallows the error (KS-1586);
 *   - it writes ENCRYPTED `details` (a "v1:…" string) into a column that is `jsonb` unless the boot-time
 *     widening to TEXT ran. That widening runs as `secuura_app`, which has no DDL rights by design, so on a
 *     fresh database it fails and the column stays `jsonb` (also KS-1586).
 * This row's details are system-generated ids only (tenant, target user, organisation ids, who granted), no
 * user-supplied input and no personal data, so they are stored as plain JSON. Plain JSON is valid for a
 * `jsonb` and for a widened `text` column alike, and decryptDetails already reads it back.
 */
function systemAuditInsertStatement(a) {
    return {
        text: `INSERT INTO audit_logs (id, tenant_id, user_id, organization_id, action, resource_type, resource_id,
         ip_address, user_agent, details, success, error_message, created_at)
       VALUES ($1,$2::uuid,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)`,
        values: [a.id, a.tenantId, a.userId || null, a.organizationId || null, a.action, a.resourceType,
            a.resourceId || null, a.ipAddress || null, a.userAgent || null, JSON.stringify(a.details ?? {}),
            a.success, a.errorMessage || null, a.createdAt],
    };
}
function rememberAuditLog(a) {
    memAuditLogs.push(a);
    if (memAuditLogs.length > 10000)
        memAuditLogs.splice(0, memAuditLogs.length - 10000);
}
async function dbSaveAuditLog(a) {
    memAuditLogs.push(a);
    if (memAuditLogs.length > 10000)
        memAuditLogs.splice(0, memAuditLogs.length - 10000);
    if (!(0, db_1.isDbAvailable)())
        return;
    try {
        // KS-28: tenant_id is the security boundary (NOT NULL after migration
        // 012). Sourced from the JWT-derived AuditLog.tenantId; the POST
        // handler enforces this so the in-memory cache + DB row both carry it.
        // KS-458: pin the RLS GUC to the row's own tenant — the request ALS may
        // differ (admin acting cross-tenant) or be absent (fire-and-forget after
        // the response), and fail-closed audit_logs would reject a mismatch.
        await (0, shared_2.runWithTenantId)(a.tenantId, () => (0, db_1.query)(`INSERT INTO audit_logs (id, tenant_id, user_id, organization_id, action, resource_type, resource_id,
         ip_address, user_agent, details, previous_state, new_state, success, error_message, created_at)
       VALUES ($1,$2::uuid,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15) ON CONFLICT (id) DO NOTHING`, [a.id, a.tenantId, a.userId || null, a.organizationId || null, a.action, a.resourceType,
            a.resourceId || null, a.ipAddress || null, a.userAgent || null,
            // Audit 1.3 phase 5: encrypt details JSONB at rest. AAD bound to
            // the audit log id so a ciphertext can't be ported between rows.
            encryptDetails(a.details, a.id),
            a.previousState ? JSON.stringify(a.previousState) : null,
            a.newState ? JSON.stringify(a.newState) : null, a.success, a.errorMessage || null, a.createdAt]));
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
        logger_1.logger.error('DB save audit log failed', { error: reason });
    }
}
async function dbSaveSecurityEvent(e) {
    memSecurityEvents.push(e);
    if (!(0, db_1.isDbAvailable)())
        return;
    try {
        await (0, db_1.query)(`INSERT INTO svc_security_events (id, event_type, severity, source, user_id, ip_address,
         details, resolved, resolved_at, resolved_by, created_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11) ON CONFLICT (id) DO NOTHING`, [e.id, e.eventType, e.severity, e.source, e.userId || null, e.ipAddress || null,
            JSON.stringify(e.details || {}), e.resolved, e.resolvedAt || null, e.resolvedBy || null, e.createdAt]);
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
        logger_1.logger.error('DB save event failed', { error: reason });
    }
}
/** KS-577's cutover window, read per call so a deploy can change it without a restart. 0 = retire at once. */
function rotationGraceSeconds() {
    const graceRaw = Number.parseInt(process.env.API_KEY_ROTATION_GRACE_SECONDS ?? '0', 10);
    return Number.isFinite(graceRaw) && graceRaw > 0 ? graceRaw : 0;
}
/** Retire one in-memory key the way the UPDATE below retires its row: at once, or at the end of the window. */
function retireInMemory(k, grace) {
    if (grace === 0) {
        k.isActive = false;
    }
    else {
        const until = new Date(Date.now() + grace * 1000);
        if (!k.expiresAt || k.expiresAt > until)
            k.expiresAt = until;
    }
}
/** The retire statement, shared by revokePriorConnectorKeys and the KS-1549 rotate transaction. RETURNING id
 *  lets the transaction retire exactly those keys in memory. */
function retirePriorStatement(connectorId, tenantId, keepKeyId, grace) {
    return grace === 0
        ? {
            text: `UPDATE svc_api_keys SET is_active = false
             WHERE connector_id = $1 AND tenant_id = $2::uuid AND id <> $3 AND is_active = true
             RETURNING id`,
            values: [connectorId, tenantId, keepKeyId],
        }
        : {
            text: `UPDATE svc_api_keys
             SET expires_at = LEAST(COALESCE(expires_at, 'infinity'::timestamptz), NOW() + ($4 || ' seconds')::interval)
             WHERE connector_id = $1 AND tenant_id = $2::uuid AND id <> $3 AND is_active = true
             RETURNING id`,
            values: [connectorId, tenantId, keepKeyId, String(grace)],
        };
}
/**
 * KS-577. Retire the prior active keys of a connector when a new one is minted
 * with `rotate: true`.
 *
 * Before this, `rotate: true` skipped the gateway early return and went straight
 * to the mint; `dbSaveApiKey` upserts ON CONFLICT (id) and so never touches
 * sibling rows, and validation keys off key_hash -> isActive -> expiresAt. After
 * re-keying a lost credential, the lost credential still worked. Guardrail 1
 * conceded it in a comment ("it invalidates nothing by itself") with nothing
 * acting on it.
 *
 * THE WINDOW IS ONE VALUE, ON PURPOSE. The cutover shape is a contract question
 * for Platform S, not a unilateral K-side call, and KS-577s three options differ
 * only in how long the old key keeps working:
 *   grace = 0  instant revoke. Cleanest containment; S in-flight writes 401
 *              until S picks up the new credential. DEFAULT, because it is what
 *              Kam ruled.
 *   grace > 0  bounded overlap. Softer on S; leaves the credential live for
 *              exactly that window, which is the thing being fixed.
 * The third option (S confirms adoption, then the old key dies) needs an S-side
 * acknowledgement path and a fallback for when it never arrives, so it is NOT
 * implemented here and no default pretends otherwise.
 *
 * Returns how many prior keys were retired, or null if the attempt FAILED. The
 * caller reports that rather than swallowing it: a silent failure here leaves
 * BOTH credentials live, which is exactly the bug.
 */
// Exported as a TEST SEAM together with `memApiKeys` below. The alternative was
// an HTTP-level test, and this service has no supertest dependency — adding one
// to assert a four-line UPDATE is a worse trade than exporting the function that
// performs it. Exporting changes no behaviour: both were already module-level.
async function revokePriorConnectorKeys(connectorId, tenantId, keepKeyId) {
    const grace = rotationGraceSeconds();
    // In-memory first, so a DB-less run still retires the sibling rather than
    // reporting a revoke that did not happen.
    let retired = 0;
    for (const [, k] of exports.memApiKeys) {
        if (k.id === keepKeyId || k.connectorId !== connectorId || k.tenantId !== tenantId)
            continue;
        if (!k.isActive)
            continue;
        retireInMemory(k, grace);
        retired += 1;
    }
    if (!(0, db_1.isDbAvailable)())
        return retired;
    try {
        // KS-458: the GUC names the row's own tenant and svc_api_keys is
        // fail-closed, so a cross-tenant rotate cannot reach another tenant's keys.
        const st = retirePriorStatement(connectorId, tenantId, keepKeyId, grace);
        const r = await (0, shared_2.runWithTenantId)(tenantId, () => (0, db_1.query)(st.text, st.values));
        return r.rowCount ?? retired;
    }
    catch (err) {
        // Loud, never silent. The new key is already minted and returned, so the
        // request cannot be failed without losing it — but the operator is told the
        // old credential is STILL LIVE.
        let reason;
        try {
            reason = String(err);
        }
        catch {
            reason = 'unreadable thrown value';
        }
        log('error', 'KS-577: revoke-on-rotate FAILED — the prior credential is still valid', {
            connectorId, tenantId, keepKeyId, error: reason,
        });
        return null;
    }
}
/**
 * KS-1556. Rotates of ONE connector, in this process, run one at a time. The next caller waits for the
 * previous one to finish COMPLETELY (its transaction AND its in-memory update) before it takes a pooled
 * client, so the waiting costs no connection (KS-757's pool trap) and the in-memory map is updated in
 * the same order the database committed. The wait is bounded: a predecessor that never settles must not
 * hang the connector forever, so after ROTATE_CHAIN_WAIT_MS (read per call; default 10 s) the caller
 * proceeds. The database's advisory lock still serialises it; only the memory ordering is no longer
 * guaranteed, and that is logged. A predecessor that throws releases the chain in its `finally`, so it
 * cannot poison it. An entry is removed when the last waiter finishes, so the map cannot grow without
 * bound. Exported as a test seam, like revokePriorConnectorKeys.
 */
exports.rotateChains = new Map();
function rotateChainWaitMs() {
    const raw = /^\s*\d+\s*$/.test(process.env.ROTATE_CHAIN_WAIT_MS ?? '') ? Number(process.env.ROTATE_CHAIN_WAIT_MS) : Number.NaN;
    return Number.isFinite(raw) && raw > 0 ? raw : 10_000;
}
async function withConnectorChain(key, fn) {
    const predecessor = exports.rotateChains.get(key);
    let release;
    const mine = new Promise((resolve) => { release = resolve; });
    exports.rotateChains.set(key, mine);
    try {
        if (predecessor) {
            const waitMs = rotateChainWaitMs();
            let timer;
            const timedOut = await Promise.race([
                predecessor.then(() => false),
                new Promise((resolve) => { timer = setTimeout(() => resolve(true), waitMs); }),
            ]);
            if (timer)
                clearTimeout(timer);
            if (timedOut)
                log('warn', 'KS-1556: a rotate waited the whole chain timeout for its predecessor and proceeds', { key, waitMs });
        }
        return await fn();
    }
    finally {
        release();
        if (exports.rotateChains.get(key) === mine)
            exports.rotateChains.delete(key);
    }
}
/**
 * KS-1549. A rotate's INSERT and its retire, as ONE transaction on ONE pooled client, serialised per
 * connector. Returns how many prior keys were retired, or null if the retire FAILED (KS-577's contract:
 * the new key still stands and the failure is reported). Throws if the key itself could not be saved,
 * which the caller answers 503/500 with no key (KS-888's contract).
 *
 * Before this, the INSERT and the retire were two autocommit statements, each on its own pooled
 * connection, with an await between them. Two interleaved rotates each retired the OTHER's new key, so
 * the connector was left with ZERO active keys and both callers held dead ones: 0 active in 9 of 10
 * double-submits on real Postgres (the #1521 gate). Ruled (decision D): the last rotate wins, exactly as
 * two sequential rotates behave.
 *
 * Every step here is load-bearing:
 *  - the per-connector in-process chain above, so that this process applies its in-memory changes in
 *    commit order, and waits without holding a pooled client;
 *  - READ COMMITTED, pinned on the transaction itself (KS-1556 m2). Under REPEATABLE READ the snapshot is
 *    taken before the lock is granted, so a rotate that waited cannot see the key the previous one
 *    committed, and its retire fails to serialise: more than one active key. It must be the FIRST
 *    statement: once the transaction has run a query, Postgres refuses to CHANGE the level (setting
 *    the level it already has is a no-op). So a late pin passes silently under a READ COMMITTED
 *    default and fails every rotate under a REPEATABLE READ one;
 *  - the tenant GUC on THIS client: svc_api_keys is FORCE row-level security and fail-closed, so a
 *    transaction without it inserts nothing and retires nothing, silently;
 *  - a TRANSACTION-scoped advisory lock on (tenant, connector): pgbouncer runs pool_mode = transaction,
 *    where a session lock would leak to the next client. It serialises rotates of one connector across
 *    processes;
 *  - the INSERT on the SAME client as the lock. KS-757 measured the trap: an INSERT on a second pooled
 *    connection, made while holding the lock, deadlocks the pool once the waiters fill it;
 *  - the retire under a SAVEPOINT, so a failed retire rolls back alone and the mint stands;
 *  - the in-memory changes ONLY AFTER COMMIT, and never undone (KS-1556). The design this replaces
 *    (#1527) changed memory before COMMIT and undid it on failure. Restoring the captured object let a
 *    concurrent validate leave the prior key refused while the database held it active (m1, the #1527
 *    gate's A8). Restoring by id instead RESURRECTED a revoke whose own save had failed (KS-888 R2),
 *    measured by its author on #1529. After COMMIT there is nothing to undo, and before it, memory and the
 *    database agree. A crash between COMMIT and this update leaves memory stale. Validate re-reads the
 *    stored row for a key in memory, and finds a key that is not in memory by its hash (KS-1370), so it
 *    still answers from the database.
 */
async function saveKeyAndRetirePriors(k, connectorId) {
    if (!(0, db_1.isDbAvailable)()) {
        // In memory nothing awaits between the two steps, so there is no window to close.
        exports.memApiKeys.set(k.id, k);
        return revokePriorConnectorKeys(connectorId, k.tenantId, k.id);
    }
    return withConnectorChain(`${k.tenantId}:${connectorId}`, async () => {
        const grace = rotationGraceSeconds();
        const retiredIds = await (0, shared_2.runWithTenantId)(k.tenantId, () => (0, db_1.transaction)(async (client) => {
            await client.query('SET TRANSACTION ISOLATION LEVEL READ COMMITTED');
            await (0, shared_2.applyTenantGuc)(client);
            await client.query('SELECT pg_advisory_xact_lock(hashtext($1), hashtext($2))', [k.tenantId, connectorId]);
            const ins = apiKeyInsertStatement(k);
            await client.query(ins.text, ins.values);
            const ret = retirePriorStatement(connectorId, k.tenantId, k.id, grace);
            await client.query('SAVEPOINT ks1549_retire');
            try {
                const ids = (await client.query(ret.text, ret.values)).rows.map((row) => row.id);
                await client.query('RELEASE SAVEPOINT ks1549_retire');
                return ids;
            }
            catch (err) {
                await client.query('ROLLBACK TO SAVEPOINT ks1549_retire');
                let reason;
                try {
                    reason = String(err instanceof Error ? err.message : err);
                }
                catch {
                    reason = 'unreadable thrown value';
                }
                log('error', 'KS-577: revoke-on-rotate FAILED — the prior credential is still valid', {
                    connectorId, tenantId: k.tenantId, keepKeyId: k.id, error: reason,
                });
                return null;
            }
        }));
        // COMMITTED. Only now does memory change, so nothing is ever undone, and the new key is in memory
        // before the 201 leaves.
        exports.memApiKeys.set(k.id, k);
        for (const id of retiredIds ?? []) {
            const current = exports.memApiKeys.get(id);
            if (current)
                retireInMemory(current, grace);
        }
        return retiredIds === null ? null : retiredIds.length;
    });
}
/** The INSERT for one key, shared by dbSaveApiKey and the KS-1549 rotate transaction so the two can never drift. */
function apiKeyInsertStatement(k) {
    return {
        text: `INSERT INTO svc_api_keys (id, organization_id, tenant_id, name, key_hash, key_prefix, scopes,
       rate_limit, rate_limit_window, last_used_at, usage_count, is_active, expires_at, created_at,
       connector_id)
     VALUES ($1,$2,$3::uuid,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15)
     ON CONFLICT (id) DO UPDATE SET
       last_used_at = EXCLUDED.last_used_at, usage_count = EXCLUDED.usage_count,
       is_active = EXCLUDED.is_active,
       -- KS-869: COALESCE, not a plain assignment. connector_id is immutable
       -- per key like tenant_id, so a stored value is never overwritten — but
       -- a row written BEFORE this change holds NULL, and a key still live in
       -- memory does know its connectorId, so the next save backfills it for
       -- free. EXCLUDED-first would null a stored value out whenever an
       -- in-memory key lacked one; stored-first would never backfill.
       connector_id = COALESCE(EXCLUDED.connector_id, svc_api_keys.connector_id)`,
        values: [k.id, k.organizationId, k.tenantId, k.name, k.keyHash, k.keyPrefix,
            JSON.stringify(k.scopes || []),
            k.rateLimit, k.rateLimitWindow, k.lastUsedAt || null, k.usageCount, k.isActive,
            k.expiresAt || null, k.createdAt, k.connectorId ?? null],
    };
}
async function dbSaveApiKey(k, opts = {}) {
    exports.memApiKeys.set(k.id, k);
    if (!(0, db_1.isDbAvailable)())
        return;
    try {
        // KS-33: write tenant_id (the load-bearing scoping field) on every
        // INSERT. organization_id is now NULL-able. ON CONFLICT updates
        // the volatile usage fields, but tenant_id is immutable per key —
        // a key minted for tenant A never moves to tenant B.
        // KS-869: connector_id is written too. The column has existed since
        // migration 018 and NOTHING wrote it or read it, so a key's connectorId
        // lived only in memApiKeys and died with the process. That made the
        // KS-843 grace log record `connectorId: null` for every Platform S key
        // after a restart, collapsed every connector's userId to
        // `connector:api-key`, and left revoke-on-rotate (KS-577) with no durable
        // way to find a connector's prior keys.
        // KS-458: pin the RLS GUC to the key's own tenant — callers include the
        // pre-session validate route (no request ALS at all) and admin flows
        // whose request tenant may differ from the key's; fail-closed
        // svc_api_keys requires the GUC to match the row being written.
        const st = apiKeyInsertStatement(k);
        await (0, shared_2.runWithTenantId)(k.tenantId, () => (0, db_1.query)(st.text, st.values));
    }
    catch (err) {
        let reason;
        try {
            reason = err?.message;
        }
        catch {
            reason = 'unreadable thrown value';
        }
        logger_1.logger.error('DB save API key failed', { error: reason });
        // KS-888: re-throws only for a caller that opts in, and each caller that opts in catches it in its own try.
        // Any other caller keeps this log-only swallow: a throw into a handler that takes no next is an unhandled
        // rejection, and that ends the process.
        if (opts.rethrow)
            throw err;
    }
}
// KS-1370 half (i): validate's usage write must NOT carry is_active.
// The shared dbSaveApiKey upsert above sets `is_active = EXCLUDED.is_active`, and it is the ONE
// statement every caller uses — mint, revoke and validate's usage bump. That is what let a stale
// in-memory copy REVIVE a persisted revoke: validate resolved the key from memApiKeys (a boot-time
// snapshot), saw isActive=true there, and its usage write then wrote that true back over the
// revoked row. Measured on real PostgreSQL before this change: usage_count 1 -> 2 and
// is_active false -> TRUE.
//
// Deleting `is_active = EXCLUDED.is_active` from the shared upsert is NOT the fix: the revoke route
// persists its revoke THROUGH that same upsert (`apiKey.isActive = false` then
// `dbSaveApiKey(apiKey, { rethrow: true })`), so removing it would stop a revoke of an existing row
// persisting at all, and the KS 764 call-site guard pins exactly that shape. So the narrow change is
// a usage-only statement for validate's call site, leaving revoke's persistence untouched.
//
// UPDATE, not an upsert: every caller reaches here with a row that already exists — validate either
// hit the boot cache (loaded FROM svc_api_keys) or warmed it from the DB in this same request. A key
// with no row must not be conjured by a usage bump.
//
// KS-458: same tenant GUC pin as dbSaveApiKey. svc_api_keys is fail-closed, and this route is
// pre-session with no request ALS, so the GUC must come from the key's own tenantId.
// KS-888 (card secuura-ks888-validate-usage-write-failure, option a): a failed usage write is
// LOGGED, NEVER REFUSED, and the log line carries no key and no hash. The message is deliberately
// byte-identical to dbSaveApiKey's so #1334's V2 cell keeps pinning one error line for this path.
async function dbRecordApiKeyUsage(k) {
    exports.memApiKeys.set(k.id, k);
    if (!(0, db_1.isDbAvailable)())
        return;
    try {
        await (0, shared_2.runWithTenantId)(k.tenantId, () => (0, db_1.query)(`UPDATE svc_api_keys SET last_used_at = GREATEST(last_used_at, $2), usage_count = usage_count + 1 WHERE id = $1`, [k.id, k.lastUsedAt || null]));
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
        logger_1.logger.error('DB save API key failed', { error: reason });
    }
}
async function dbGetApiKey(id) {
    if ((0, db_1.isDbAvailable)()) {
        try {
            // KS-578: the lookup is platform-scoped (see keyRevokePolicy). Under
            // FORCE RLS a foreign-tenant row read with the caller's tenant GUC
            // returns nothing, so a key written by another service AFTER this one
            // booted 404'd even though it exists. Safe only because the sole caller
            // — the revoke route — puts the result through decideKeyRevoke.
            // Row mapping now uses the canonical rowToApiKey rather than a second
            // inline copy, which also drops a divergence: the inline version passed
            // `scopes` straight through instead of parseJsonArray().
            const row = await (0, keyRevokePolicy_1.lookupKeyForRevoke)(id);
            if (row)
                return (0, converters_1.rowToApiKey)(row);
        }
        catch { /* fall through */ }
    }
    return exports.memApiKeys.get(id);
}
function rowToAuditLog(r) {
    return (0, converters_1.rowToAuditLog)(r, decryptDetails);
}
// =============================================================================
// DATABASE → MEMORY LOADER
// =============================================================================
async function loadFromDb() {
    if (!(0, db_1.isDbAvailable)())
        return;
    // KS-458: boot-time cache warm is deliberately cross-tenant — there is no
    // request context, and the in-memory caches must hold EVERY tenant's rows
    // (the API surface re-filters per caller). Under fail-closed RLS the full
    // scans on audit_logs / svc_api_keys would return zero rows without the
    // platform scope, silently emptying the caches.
    return (0, shared_2.runWithPlatformScope)(async () => {
        try {
            const logsResult = await (0, db_1.query)('SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 10000');
            memAuditLogs.length = 0;
            for (const row of logsResult.rows)
                memAuditLogs.push(rowToAuditLog(row));
            memAuditLogs.reverse();
            const eventsResult = await (0, db_1.query)('SELECT * FROM svc_security_events ORDER BY created_at DESC LIMIT 10000');
            memSecurityEvents.length = 0;
            for (const row of eventsResult.rows)
                memSecurityEvents.push((0, converters_1.rowToSecurityEvent)(row));
            memSecurityEvents.reverse();
            const keysResult = await (0, db_1.query)('SELECT * FROM svc_api_keys');
            exports.memApiKeys.clear();
            for (const row of keysResult.rows) {
                const key = (0, converters_1.rowToApiKey)(row);
                exports.memApiKeys.set(key.id, key);
            }
            logger_1.logger.info('Loaded persisted data from DB', {
                auditLogs: memAuditLogs.length,
                securityEvents: memSecurityEvents.length,
                apiKeys: exports.memApiKeys.size,
            });
        }
        catch (err) {
            logger_1.logger.error('Failed to load persisted data from DB', { error: err?.message });
        }
    });
}
// =============================================================================
// LOGGING
// =============================================================================
function log(level, message, meta) {
    const timestamp = new Date().toISOString();
    console.log(JSON.stringify({ timestamp, level, service: 'security', message, ...meta }));
}
// =============================================================================
// MIDDLEWARE
// =============================================================================
app.use((0, helmet_1.default)());
app.use((0, cors_1.default)({
    origin: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:6100', 'http://localhost:6101'],
    credentials: true,
}));
// KS-1724: was `app.use(express.json());`; the same options, plus the structural caps.
app.use((0, shared_1.boundedJson)({ service: 'security' }));
app.use((0, shared_2.rejectNulBytes)()); // KS-471: no U+0000 may pass the boundary (raw-500 / persist class)
const requestLogger = (req, res, next) => {
    const start = Date.now();
    res.on('finish', () => {
        log('info', 'Request completed', {
            method: req.method,
            path: req.path,
            statusCode: res.statusCode,
            duration: `${Date.now() - start}ms`,
        });
    });
    next();
};
app.use(requestLogger);
// KS-458: seed the request-scoped tenant context (from the gateway-derived
// x-tenant-id header) so the db chokepoint bundles the fail-closed RLS GUC
// into every query's transaction. Mounted before routes/auth so it wraps the
// whole request chain. The pre-session /api/keys/validate path has no tenant
// yet — it uses the SECURITY DEFINER lookup instead (see that route).
app.use((0, shared_2.tenantGucContext)());
// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================
const createAuditLogSchema = zod_1.z.object({
    userId: zod_1.z.string().optional(),
    organizationId: zod_1.z.string().optional(),
    action: zod_1.z.string().trim().min(1),
    resourceType: zod_1.z.string().trim().min(1),
    resourceId: zod_1.z.string().optional(),
    ipAddress: zod_1.z.string().optional(),
    userAgent: zod_1.z.string().optional(),
    details: zod_1.z.record(zod_1.z.string(), zod_1.z.unknown()).default({}),
    previousState: zod_1.z.record(zod_1.z.string(), zod_1.z.unknown()).optional(),
    newState: zod_1.z.record(zod_1.z.string(), zod_1.z.unknown()).optional(),
    success: zod_1.z.boolean().default(true),
    errorMessage: zod_1.z.string().optional(),
});
const createSecurityEventSchema = zod_1.z.object({
    eventType: zod_1.z.string().min(1),
    severity: zod_1.z.enum(['low', 'medium', 'high', 'critical']),
    source: zod_1.z.string().min(1),
    userId: zod_1.z.string().optional(),
    ipAddress: zod_1.z.string().optional(),
    details: zod_1.z.record(zod_1.z.string(), zod_1.z.unknown()).default({}),
});
const createApiKeySchema = zod_1.z.object({
    // KS-33: organizationId is now optional. SYSTEM_ADMIN flows that issue
    // tenant-scoped keys without picking a specific org pass null; the
    // tenant_id-derivation logic below falls through to header / default.
    organizationId: zod_1.z.string().optional(),
    // KS-33: explicit tenantId override. Callers that already know the
    // tenant (e.g. originate's POST /api/admin/api-keys, with X-Tenant-
    // Override resolved by the gateway) can skip the org→tenant lookup.
    tenantId: zod_1.z.string().guid().optional(),
    name: zod_1.z.string().trim().min(1).max(100),
    scopes: zod_1.z.array(zod_1.z.string()).default(['read']),
    rateLimit: zod_1.z.number().int().min(1).max(10000).default(1000),
    rateLimitWindow: zod_1.z.number().int().min(60).max(86400).default(3600),
    expiresAt: shared_2.isoDateTimeSchema.optional(), // KS-427: accept RFC 3339 offsets, normalise to UTC
    connectorId: zod_1.z.string().optional(),
    // KS-577. Kam ruled 2026-08-07 that rotation SHOULD revoke the prior key:
    // shipping the additive version would hand out N new credentials, leave N
    // compromised ones live, and look like recovery. When true and a connectorId
    // is supplied, the prior active keys for that connector are retired — see
    // revokePriorConnectorKeys for the window semantics.
    rotate: zod_1.z.boolean().optional().default(false),
});
// KS-698. The ECMAScript time value range is +/-8.64e15 ms; a Date outside it is
// Invalid and toISOString() THROWS. windowMs had a minimum and no maximum, so a
// single request could compute a resetAt beyond that range.
// KS-698 — extracted to `rateLimitBounds.ts` so the PUBLISHED contract can import
// the same constant the runtime enforces (the #882 gate's F2). Re-exported here
// because callers and tests already import them from this module.
var rateLimitBounds_2 = require("./rateLimitBounds");
Object.defineProperty(exports, "isRepresentableInstant", { enumerable: true, get: function () { return rateLimitBounds_2.isRepresentableInstant; } });
Object.defineProperty(exports, "MAX_RATE_LIMIT_WINDOW_MS", { enumerable: true, get: function () { return rateLimitBounds_2.MAX_RATE_LIMIT_WINDOW_MS; } });
Object.defineProperty(exports, "usableRateLimitEntry", { enumerable: true, get: function () { return rateLimitBounds_2.usableRateLimitEntry; } });
Object.defineProperty(exports, "persistableResetAt", { enumerable: true, get: function () { return rateLimitBounds_2.persistableResetAt; } });
// Exported as a test seam: this service has no supertest dependency, and adding
// one to assert a schema bound is the worse trade. Exporting changes no
// behaviour — the schema was already module-level.
exports.checkRateLimitSchema = zod_1.z.object({
    // KS-952 F10: `min(1)` with no maximum accepted a 100,000-character key and
    // stored it. This bounds one entry; `sweepExpired` bounds the map.
    // KS-974 item 1: the published maxLength 256 counts CODE POINTS; zod .max() counts UTF-16
    // code units, so 256 astral characters were refused on the one route anyone can reach.
    // Same predicate as boundedByCodePoints on /reset (requestSchemas.ts).
    key: zod_1.z.string().min(1).refine((value) => [...value].length <= rateLimitScope_1.RATE_LIMIT_KEY_MAX, {
        message: 'must not exceed ' + rateLimitScope_1.RATE_LIMIT_KEY_MAX + ' characters',
    }),
    limit: zod_1.z.number().int().min(1).default(100),
    // KS-698 fix 1: an UPPER bound. `min` alone let one request poison a key.
    windowMs: zod_1.z.number().int().min(1000).max(rateLimitBounds_1.MAX_RATE_LIMIT_WINDOW_MS).default(60000),
});
// =============================================================================
// ROUTES
// =============================================================================
// Health check
app.get('/health', (_req, res) => {
    res.json({
        status: 'healthy',
        service: 'security',
        version: '0.1.0',
        timestamp: new Date().toISOString(),
        stats: {
            auditLogs: memAuditLogs.length,
            securityEvents: memSecurityEvents.length,
            activeApiKeys: Array.from(exports.memApiKeys.values()).filter(k => k.isActive).length,
        },
    });
});
// API info
app.get('/api', (_req, res) => {
    res.json({
        service: 'Secuura Security Service',
        version: '0.1.0',
        endpoints: {
            audit: {
                'POST /api/audit': 'Create audit log entry',
                'GET /api/audit': 'Query audit logs',
                'GET /api/audit/:id': 'Get audit log by ID',
            },
            events: {
                'POST /api/events': 'Create security event',
                'GET /api/events': 'Query security events',
                'PATCH /api/events/:id/resolve': 'Resolve security event',
            },
            apiKeys: {
                'POST /api/keys': 'Create API key',
                'GET /api/keys': 'List API keys for organization',
                'DELETE /api/keys/:id': 'Revoke API key',
                'POST /api/keys/validate': 'Validate API key',
            },
            rateLimit: {
                'POST /api/rate-limit/check': 'Check rate limit',
                'POST /api/rate-limit/reset': 'Reset rate limit counter',
            },
        },
    });
});
// =============================================================================
// AUDIT LOG ROUTES
// =============================================================================
// Pen-test H2 — every /api/* route below this point JWT-verifies the
// bearer token via @secuura/shared's `authenticate()`. Without this,
// downstream services trusted the gateway-injected x-user-* headers,
// which an attacker reaching a service directly (intra-cluster, leaked
// internal endpoint, etc.) could forge.
//
// KS-39 #5: `/api/keys/validate` is a special case. The gateway calls
// it from `validateApiKey()` to check an inbound `x-api-key` header
// BEFORE there's a user session to authenticate. Forwarding the
// gateway's own bearer token would require a service identity that we
// don't currently mint, and per Pen-test H2 the route is on the
// internal-only Container Apps FQDN so the threat model is "another
// pod inside the env". We skip auth specifically on this path while
// keeping H2 enforcement for every other route.
app.use('/api', (req, res, next) => {
    if (req.path === '/keys/validate' || req.path.startsWith('/keys/validate?')) {
        return next();
    }
    return (0, shared_2.authenticate)()(req, res, next);
});
/**
 * POST /api/audit
 * Create an audit log entry
 */
app.post('/api/audit', async (req, res, next) => {
    try {
        const data = createAuditLogSchema.parse(req.body);
        // KS-28: server-derives tenant_id from the verified JWT, NOT from the
        // request body. Allowing the body to set tenant_id would let any
        // authenticated caller forge audit entries against another tenant.
        // Falls back to the originate default tenant id when no JWT context is
        // present (system-actor calls e.g. cron jobs that authenticate via
        // service tokens with no tenantId claim).
        const jwtTenant = req.user?.tenantId;
        const tenantId = jwtTenant || 'a0000000-0000-4000-8000-000000000001';
        const auditLog = {
            // Pen-test F-09: audit-log IDs MUST be unpredictable. Math.random()
            // is xorshift128+ — an attacker who can race the audit insert can
            // pre-claim an ID and break the evidentiary chain. crypto.randomUUID
            // gives 122-bit entropy from a CSPRNG.
            id: `audit_${require('crypto').randomUUID()}`,
            tenantId,
            ...data,
            createdAt: new Date(),
        };
        await dbSaveAuditLog(auditLog);
        log('info', 'Audit log created', {
            auditId: auditLog.id,
            action: auditLog.action,
            resourceType: auditLog.resourceType
        });
        res.status(201).json({
            success: true,
            data: { id: auditLog.id },
        });
    }
    catch (error) {
        if (error instanceof zod_1.z.ZodError) {
            return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: (0, zod3_compat_1.zod3Issues)(error.issues) } });
        }
        next(error);
    }
});
/**
 * GET /api/audit
 * Query audit logs
 */
app.get('/api/audit', (req, res) => {
    const { userId, organizationId, action, resourceType, from, to, limit = '50', offset = '0' } = req.query;
    // KS-28: scope to the caller's JWT tenant. The in-memory cache is
    // cross-tenant on disk (loaded by loadFromDb at startup) but the API
    // surface must filter so a tenant A admin cannot enumerate tenant B's
    // actions through this endpoint. Cross-tenant audit views for super_admin
    // go through the api-gateway's /admin/audit-logs which already gates on
    // role + applies its own tenant filter (KS-28 partial earlier this
    // session). Security service callers are gateway-internal otherwise.
    // KS-743: a caller with NO tenant claim used to fall through to
    // `[...memAuditLogs]` — every tenant's rows — which is the exact defaulting
    // the KS-28 comment above says this endpoint exists to prevent, and the same
    // fail-open KS-742 refused for `/api/keys`. A missing claim is now a refusal,
    // not a wildcard. Platform roles keep cross-tenant reach explicitly, through
    // the one shared rule in keyRevokePolicy rather than a second copy here.
    const callerTenantId = req.user?.tenantId;
    if (!(0, keyRevokePolicy_1.isPlatformRole)(req.user?.role) && !callerTenantId) {
        return res.status(403).json({
            success: false,
            error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },
        });
    }
    let filtered = callerTenantId
        ? memAuditLogs.filter(l => l.tenantId === callerTenantId)
        : [...memAuditLogs];
    if (userId)
        filtered = filtered.filter(l => l.userId === userId);
    if (organizationId)
        filtered = filtered.filter(l => l.organizationId === organizationId);
    if (action)
        filtered = filtered.filter(l => l.action === action);
    if (resourceType)
        filtered = filtered.filter(l => l.resourceType === resourceType);
    if (from)
        filtered = filtered.filter(l => l.createdAt >= new Date(from));
    if (to)
        filtered = filtered.filter(l => l.createdAt <= new Date(to));
    // Sort by newest first
    filtered.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
    const total = filtered.length;
    const results = filtered.slice(parseInt(offset), parseInt(offset) + parseInt(limit));
    res.json({
        success: true,
        data: {
            logs: results,
            total,
            limit: parseInt(limit),
            offset: parseInt(offset),
        },
    });
});
/**
 * GET /api/audit/:id
 * Get audit log by ID
 */
app.get('/api/audit/:id', (req, res) => {
    // KS-28: same tenant scope as the list endpoint. A foreign-tenant id
    // returns 404 (not 403) so existence isn't leaked.
    //
    // KS-743: that promise was not kept for a caller with NO tenant claim. The
    // guard below reads `callerTenantId && …`, so an absent claim skipped the
    // tenant comparison entirely and ANY audit row was returned by id, from a
    // cache `loadFromDb` warms cross-tenant at boot. Unlike its sibling
    // `GET /api/audit`, this route is NOT shadowed at the edge — the gateway's
    // local alias is exact-path `/api/security/audit` only, so this one is
    // reachable through the public gateway and the fail-open was live.
    // Refusing the tenant-less caller is what makes the comment above true.
    const callerTenantId = req.user?.tenantId;
    if (!(0, keyRevokePolicy_1.isPlatformRole)(req.user?.role) && !callerTenantId) {
        return res.status(403).json({
            success: false,
            error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },
        });
    }
    const auditLog = memAuditLogs.find(l => l.id === req.params.id);
    if (!auditLog || (callerTenantId && auditLog.tenantId !== callerTenantId)) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Audit log not found' } });
    }
    res.json({
        success: true,
        data: auditLog,
    });
});
// =============================================================================
// SECURITY EVENT ROUTES
// =============================================================================
/**
 * POST /api/events
 * Create a security event
 */
app.post('/api/events', requirePlatformOperator, async (req, res, next) => {
    try {
        const data = createSecurityEventSchema.parse(req.body);
        const event = {
            // Pen-test F-09: same evidentiary-integrity rationale as audit IDs.
            id: `event_${require('crypto').randomUUID()}`,
            ...data,
            resolved: false,
            createdAt: new Date(),
        };
        await dbSaveSecurityEvent(event);
        // Log high/critical events
        if (event.severity === 'high' || event.severity === 'critical') {
            log('warn', `Security event: ${event.eventType}`, {
                eventId: event.id,
                severity: event.severity,
                source: event.source,
            });
        }
        res.status(201).json({
            success: true,
            data: event,
        });
    }
    catch (error) {
        if (error instanceof zod_1.z.ZodError) {
            return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: (0, zod3_compat_1.zod3Issues)(error.issues) } });
        }
        next(error);
    }
});
/**
 * KS-743: the security-event surface is PLATFORM-ONLY, and that is a statement
 * about the data model rather than a policy preference.
 *
 * `SecurityEvent` has no tenant field, and neither does `svc_security_events`
 * (migrations/002, and `dbSaveSecurityEvent`'s INSERT names eleven columns,
 * none of them a tenant or an organisation). So there is nothing to scope a
 * tenant-scoped caller TO — `decideTenantAccess` has no `targetTenantId` to be
 * handed here, which is exactly why the read below could return the whole
 * cross-tenant corpus to an ordinary tenant admin (measured: 200, total 651).
 *
 * With no tenant dimension in the data, the only authorisation that is true is
 * "platform operator". Giving events a real tenant column is the larger fix and
 * is not this ticket; until then the honest gate is this one, and it is
 * strictly narrowing — 403 is already a declared response on both operations.
 *
 * `requireKeyAdmin` above is deliberately NOT reused: its role set includes the
 * tenant-scoped ORG_ADMIN / ISSUER_ADMIN / ADMIN, which is the very set that
 * could read every tenant's events.
 */
/**
 * The shared body of the platform-role gates. `subject` only shapes the refusal
 * MESSAGE — the decision is identical.
 *
 * ⚠ These are FUNCTION DECLARATIONS, not `const` arrow bindings, and that is
 * load-bearing: `app.post('/api/events', …)` at :688 mounts its gate ~70 lines
 * ABOVE this point. A `const` is in the temporal dead zone there and the module
 * would throw `ReferenceError: Cannot access 'requirePlatformOperator' before
 * initialization` at import — which the first draft of this change did. Function
 * declarations hoist, so route order and gate order stay independent.
 */
function platformRoleGate(subject, req, res, next) {
    if (!(0, keyRevokePolicy_1.isPlatformRole)(req.user?.role)) {
        res.status(403).json({
            success: false,
            error: { code: 'FORBIDDEN', message: `${subject} require a platform role` },
        });
        return;
    }
    next();
}
/**
 * The events gate. `'Security events require a platform role'` is asserted
 * verbatim by the KS-743 route-contract rows (QA F-8): two gates in this file
 * both answer 403 + FORBIDDEN, so the MESSAGE is the only thing that says which
 * one refused. Changing this string changes what those rows are testing.
 */
function requirePlatformOperator(req, res, next) {
    platformRoleGate('Security events', req, res, next);
}
/**
 * KS-743 QA F-6. `POST /api/rate-limit/reset` is published at
 * `/api/security/rate-limit/reset`, so it is internet-reachable, and it carried
 * NO role gate: any authenticated caller could clear any rate-limit bucket by
 * key — the control standing in front of every brute-force limiter on the
 * platform. Outside the ticket's four routes, inside the "property of the route
 * TABLE" class this file's header defines.
 *
 * Platform-operator rather than a connector scope, on the same measurement as
 * `POST /api/events`: zero callers outside this service's own route table, its
 * OpenAPI module and the published spec, against controls that matched real
 * callers elsewhere (75 `rate-limit` hits in the same corpus).
 */
function requirePlatformOperatorForRateLimit(req, res, next) {
    platformRoleGate('Rate-limit resets', req, res, next);
}
/**
 * GET /api/events
 * Query security events
 */
app.get('/api/events', requirePlatformOperator, (req, res) => {
    const { severity, resolved, from, to, limit = '50', offset = '0' } = req.query;
    let filtered = [...memSecurityEvents];
    if (severity)
        filtered = filtered.filter(e => e.severity === severity);
    if (resolved !== undefined)
        filtered = filtered.filter(e => e.resolved === (resolved === 'true'));
    if (from)
        filtered = filtered.filter(e => e.createdAt >= new Date(from));
    if (to)
        filtered = filtered.filter(e => e.createdAt <= new Date(to));
    filtered.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
    const total = filtered.length;
    const results = filtered.slice(parseInt(offset), parseInt(offset) + parseInt(limit));
    res.json({
        success: true,
        data: { events: results, total, limit: parseInt(limit), offset: parseInt(offset) },
    });
});
/**
 * PATCH /api/events/:id/resolve
 * Resolve a security event
 */
app.patch('/api/events/:id/resolve', requirePlatformOperator, async (req, res) => {
    const event = memSecurityEvents.find(e => e.id === req.params.id);
    if (!event) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Event not found' } });
    }
    event.resolved = true;
    event.resolvedAt = new Date();
    // KS-743: attribution comes from the verified token, not the request body.
    // `resolvedBy = req.body.resolvedBy` let the caller name anyone — on a
    // security-event trail that is the one field whose whole value is that it
    // cannot be chosen by the actor. The body is ignored; a caller that supplies
    // it is not honoured rather than rejected, so this narrows attribution
    // without adding a new failure mode to a route that already resolves.
    event.resolvedBy = String(req.user?.userId || req.user?.sub || 'unknown');
    await dbSaveSecurityEvent(event);
    res.json({
        success: true,
        data: event,
    });
});
// =============================================================================
// API KEY ROUTES
// =============================================================================
// KS-480: key management is an admin surface. Before this gate, ANY
// authenticated JWT — any logged-in user of any role, and (once the KS-480
// connector token exchange landed) any sk_ connector — could mint keys with
// arbitrary scopes or revoke others' keys: a self-service privilege-escalation
// path (mint a wider key than your own grants). Legitimate callers are the
// admin dashboard (platform/org admins) and tenant-provisioning's metering
// mint, which forwards the provisioning admin's own bearer (meteringKey.ts).
// Role strings are uppercased before comparison — JWTs carry both `super_admin`
// (seeded DB casing) and canonical `SYSTEM_ADMIN` shapes (KS-486 precedent).
const KEY_ADMIN_ROLES = new Set(['SYSTEM_ADMIN', 'SUPER_ADMIN', 'ORG_ADMIN', 'ISSUER_ADMIN', 'ADMIN']);
function requireKeyAdmin(req, res, next) {
    // KS-1591: `String(role).toUpperCase()` is not an identity test. U+0131 (dotless i) upper-cases to `I` and U+017F (long s) upper-cases to `S`, so a role spelled with a dotless i read as ISSUER_ADMIN, and a role
    // ARRAY stringifies to its element. Only an ASCII fold is applied (a-z to A-Z, every other character untouched), and a role that is not a string is refused outright.
    const claim = req.user?.role;
    const role = typeof claim === 'string' ? claim.replace(/[a-z]/g, (ch) => ch.toUpperCase()) : '';
    if (!KEY_ADMIN_ROLES.has(role)) {
        res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'API key management requires an admin role' } });
        return;
    }
    next();
}
/**
 * KS-480 §4 amendment (2026-07-30) — mint authorisation for Organisation
 * provisioning. A thin wrapper over the pure policy in ./provisioningPolicy.ts
 * (extracted so it is unit-testable without booting this service): a
 * platform-admin passes as before; a connector carrying the provisioning-only
 * `organizations:register` scope may cause a mint, but never of a wildcard or
 * of the provisioning scope itself, and only into its own tenant. Read/revoke
 * stay admin-only — provisioning is create-only.
 */
/**
 * KS-888's infrastructure/application split, as ONE definition.
 *
 * The SQLSTATE classes 08 (connection), 53 (insufficient resources) and 57 (operator intervention),
 * plus the socket errno set and the pg driver's own connection messages, mean "the database could not
 * be reached", which is retryable: the caller answers 503. Anything else is an application fault and
 * answers 500.
 *
 * Extracted by the pull request 1539 gate's m1 rather than copied a third time. The expression already
 * existed TWICE, byte-identical, at the mint and revoke save sites, and the gate's finding was that the
 * new PUT did not use it — so adding a third inline copy would have fixed the symptom while making the
 * drift worse. Now a change to the classification reaches every caller at once.
 *
 * @param err - the thrown value; a non-Error is handled, since pg can reject with a plain object.
 * @returns true when the failure is infrastructure, so the caller should answer 503.
 */
function isInfrastructureDbError(err) {
    const e = err;
    return /^(08|53|57)|^(ECONNREFUSED|ECONNRESET|ETIMEDOUT|EHOSTUNREACH|ENETUNREACH|EPIPE)$/.test(String(e?.code))
        || /connection terminated|timeout exceeded when trying to connect|connection timeout|pool is draining|client has encountered a connection error/i.test(String(e?.message));
}
function requireKeyAdminOrProvisioner(req, res, next) {
    const decision = (0, provisioningPolicy_1.decideMint)(req.user, (req.body ?? {}));
    if (decision.allow) {
        if (decision.via === 'provisioner') {
            log('info', 'API key mint authorised by a provisioning key', {
                connectorId: req.user?.connectorId,
                tenantId: req.user?.tenantId,
            });
        }
        next();
        return;
    }
    if (decision.offendingScopes) {
        log('warn', 'Provisioning key attempted to mint an escalating scope', {
            offending: decision.offendingScopes,
            connectorId: req.user?.connectorId,
        });
    }
    res.status(decision.status).json({ success: false, error: { code: 'FORBIDDEN', message: decision.message } });
}
app.post('/api/keys', requireKeyAdminOrProvisioner, async (req, res, next) => {
    try {
        const data = createApiKeySchema.parse(req.body);
        // Generate API key
        const keyValue = `sk_${crypto_1.default.randomBytes(32).toString('hex')}`;
        const keyHash = crypto_1.default.createHash('sha256').update(keyValue).digest('hex');
        const keyPrefix = keyValue.substring(0, 12);
        // KS-33: tenant_id resolution. Order:
        //   1. Explicit tenantId in request body (callers that already know).
        //   2. x-tenant-id header (gateway-injected for proxied calls).
        //   3. Look up via organizations.tenant_id (fast path for OAuth-app
        //      flows that pass organizationId).
        //   4. Default-tenant fallback (non-prod / single-tenancy mode).
        const DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';
        let tenantId = data.tenantId ||
            req.headers['x-tenant-id'];
        if (!tenantId && data.organizationId && (0, db_1.isDbAvailable)()) {
            try {
                // KS-458: admin-authorised cross-tenant resolution. The caller may be
                // a platform admin creating a key for an org in ANOTHER tenant, and
                // organizations is fail-closed — the request's own tenant GUC would
                // hide the target org's row. Platform scope covers this single lookup.
                const r = await (0, shared_2.runWithPlatformScope)(() => (0, db_1.query)('SELECT tenant_id::text AS tenant_id FROM organizations WHERE id = $1::uuid LIMIT 1', [data.organizationId]));
                if (r.rows.length > 0 && r.rows[0].tenant_id) {
                    tenantId = r.rows[0].tenant_id;
                }
            }
            catch {
                // organizations table missing or organizationId not a UUID — fall through
            }
        }
        if (!tenantId) {
            // KS-742: a tenant-scoped caller's OWN tenant is the right default here.
            // The platform-wide DEFAULT_TENANT_ID silently placed a tenant-B admin's
            // key in tenant A — the same cross-tenant landing this ticket is about,
            // arrived at by omission rather than by a supplied value.
            tenantId = (!(0, keyRevokePolicy_1.isPlatformRole)(req.user?.role) && req.user?.tenantId)
                ? req.user.tenantId
                : DEFAULT_TENANT_ID;
        }
        // KS-742: resolve first, THEN authorise — the order KS-643 established for
        // revoke. decideMint (requireKeyAdminOrProvisioner) runs before the body is
        // parsed and cannot see which tenant the key will land in; its own tenant
        // limit is on the provisioner branch only, so a KEY_ADMIN_ROLE took its
        // early return and never met a tenancy check. All THREE resolution sources
        // above — body `tenantId`, the `x-tenant-id` header, and the platform-scoped
        // organizations lookup — can name a foreign tenant, and one check placed
        // here after resolution covers all three rather than three checks that must
        // stay in step.
        //
        // KS-1533 arm 1 — the ORGANISATION arm. KS-764 gave revoke an organisation bound and deliberately
        // left the mint on tenant only ("the two existing callers keep exactly today's behaviour"). So an
        // organisation-bounded admin of A could mint a key carrying B's organizationId inside the same
        // tenant, and the KS-695 connector erasure then trusts that row. Passing the scope engages the arm
        // for ORG_ADMIN / ISSUER_ADMIN only: platform roles still bypass by design (KS-577 depends on it).
        // A null target organisation is an unqualified, tenant-level mint and is still allowed, under Kam's
        // 2026-09-03 ruling — so the unqualified mint survives, including for the org-less accounts KS-779
        // recorded as intentionally org-less. Those accounts CAN no longer name an organisation; that is the
        // accepted price, and both open questions (ADMIN's reach, the org-less mint cost) are Kam's cards.
        //
        // KS-1570 (Kam's ruling, shape b): an ADMIN is bounded by its ADMIN ORGANISATION SCOPE, read here per
        // decision and only when it can matter (an ADMIN naming an organisation). A read that fails throws to
        // the catch below and is answered 5xx; it is never an allow. Not passing it would also be refused
        // ("not resolved"): the policy fails closed.
        // KS-1584 HOP 1 (pull request 1535 gate M1). A non-platform caller minting a PROVISIONING-CAPABLE
        // key must NAME an organisation. `decideMint` takes a KEY_ADMIN early return for every admin role
        // whatever the scopes are asked for (provisioningPolicy.ts:97), so an ADMIN could mint an
        // UNQUALIFIED `organizations:register` key — and an unqualified key carries no organisation, so the
        // hop-2 arm below has nothing to bound it to and it would read as platform-minted and unbounded.
        // That is the escape, and the bound cannot close it alone: the refusal has to be here.
        //
        // Default deny, which is stricter than "may mint only unqualified keys": with no organisation there
        // is nothing to bound the key to, so there is no safe unqualified provisioning key for a tenant
        // admin to hold. A platform role still mints the org-less instance key Platform S uses.
        // Wildcards count, through the same shared predicate the gateway's register-connector uses.
        // An ORDINARY unqualified mint is untouched — this reads the REQUESTED scopes, not the mint itself.
        const requestedScopes = Array.isArray(data.scopes) ? data.scopes : [];
        if ((0, shared_2.isProvisioningCapable)(requestedScopes)
            && !(0, keyRevokePolicy_1.isPlatformRole)(req.user?.role)
            && (0, shared_2.normaliseOrgId)(data.organizationId ?? null) === null) {
            log('warn', 'API key mint refused: an unqualified provisioning-capable key has no organisation to bind', {
                callerRole: req.user?.role,
                callerTenantId: req.user?.tenantId,
                requestedScopes,
            });
            return res.status(403).json({
                success: false,
                error: {
                    code: 'FORBIDDEN',
                    message: 'A provisioning-capable key must name an organisation in your scope; only a platform role may mint one without an organisation',
                },
            });
        }
        const mintCaller = req.user;
        const adminOrganisationScope = (0, keyRevokePolicy_1.isScopedAdminRole)(mintCaller?.role) && (0, shared_2.normaliseOrgId)(data.organizationId) !== null
            ? await (0, adminScope_1.getAdminOrganisationScope)(mintCaller?.tenantId, mintCaller?.userId ?? mintCaller?.sub)
            : undefined;
        const mintDecision = (0, keyRevokePolicy_1.decideTenantAccess)(req.user, tenantId, {
            targetOrganizationId: data.organizationId ?? null,
            ...(adminOrganisationScope !== undefined ? { adminOrganisationScope } : {}),
        });
        if (!mintDecision.allow) {
            const reason = mintDecision.reason;
            log('warn', 'API key mint refused', {
                targetTenantId: tenantId,
                targetOrganizationId: data.organizationId ?? null,
                callerTenantId: req.user?.tenantId,
                callerRole: req.user?.role,
                reason,
            });
            // The message names the boundary that actually refused. A same-tenant organisation refusal that
            // said "your own tenant" would send the reader to the wrong fix — the tenants match.
            // KS-1584: the provisioning reason needs its own line for the reason this chain already gives:
            // the tenants MATCH on a provisioning-organisation refusal, so the default tenant message would
            // send the reader to the wrong fix. Caught by reading the gate cell's ledger, which recorded a
            // correct 403 carrying "may only be minted in your own tenant".
            const message = reason === 'cross-organisation'
                ? 'API keys may only be minted for your own organisation'
                : reason === 'caller has no organisation'
                    ? 'Your token carries no organisation, so it cannot mint a key that names one; omit organizationId to mint a tenant-level key'
                    : reason === 'outside admin organisation scope' || reason === 'admin organisation scope not resolved'
                        ? 'API keys may only be minted for an organisation in your admin organisation scope; omit organizationId to mint a tenant-level key'
                        : reason === 'outside provisioning key organisation'
                            ? 'A provisioning key may only mint for its own organisation; omit organizationId to mint a tenant-level key'
                            : 'API keys may only be minted in your own tenant';
            return res.status(mintDecision.status ?? 403).json({ success: false, error: { code: 'FORBIDDEN', message } });
        }
        // KS-1533 arm 1, second half — a caller-chosen connectorId. Only a platform role or a PROVISIONER
        // (role `connector` carrying organizations:register) may name one: those are exactly the two caller
        // kinds register-connector's requireOrgProvisioner admits, so Platform S registration is untouched.
        // Anyone else naming a connector id could bind a key to another organisation's connector, and with
        // `rotate: true` retire that organisation's live keys: revokePriorConnectorKeys is scoped by
        // connector id and TENANT only (Path 3 — an availability harm that needs no erasure and is
        // reachable on any build with KS-577's revoke-on-rotate). Refused here, BEFORE the key is built,
        // saved or rotated, so a refusal writes nothing and retires nothing.
        if (data.connectorId !== undefined) {
            const caller = req.user;
            const isProvisioner = caller?.role === 'connector' && (caller?.scopes ?? []).includes(provisioningPolicy_1.PROVISIONING_SCOPE);
            if (!(0, keyRevokePolicy_1.isPlatformRole)(caller?.role) && !isProvisioner) {
                log('warn', 'API key mint refused: a non-provisioner named a connectorId', {
                    callerRole: caller?.role,
                    connectorId: data.connectorId,
                    rotate: data.rotate === true,
                });
                return res.status(403).json({
                    success: false,
                    error: { code: 'FORBIDDEN', message: 'Only a platform role or a provisioning connector may set connectorId' },
                });
            }
            // #1521 gate M1. A provisioner may NAME a connectorId (register-connector's path), but nothing binds
            // that id to its own connector or organisation, so with `rotate: true` it could retire ANOTHER
            // organisation's live keys and take a fresh key on that connector: Path 3, left open for exactly this
            // caller class. Rotation is platform-only, as the gateway already says ("GUARDRAIL 1" in
            // api-gateway routes/platform.ts, register-connector); this service enforces it too, because a key
            // can reach it directly.
            // KS-1584 (pull request 1535 gate M1), the second half of the hop-2 hazard. A provisioner may name
            // a connectorId — register-connector's own path needs it — but a BOUNDED one may not. Binding an
            // A1-bounded key to A2's connector id is the erasure shape this ticket exists to remove: the KS-695
            // connector erasure trusts the row's connector and organisation, and the erasure is irreversible.
            // Only a platform role and an UNBOUNDED (platform-minted, org-less) provisioner keep the capability,
            // which is exactly the Platform S registration path. Refused BEFORE the key is built or saved.
            const boundedProvisioner = caller?.role === 'connector'
                && (0, shared_2.isProvisioningCapable)(caller?.scopes)
                && (0, shared_2.normaliseOrgId)(caller?.organizationId ?? null) !== null;
            if (boundedProvisioner) {
                log('warn', 'API key mint refused: a bounded provisioning connector named a connectorId', {
                    callerRole: caller?.role,
                    connectorId: data.connectorId,
                });
                return res.status(403).json({
                    success: false,
                    error: {
                        code: 'FORBIDDEN',
                        message: 'A provisioning key bound to an organisation may not set connectorId; that is reserved for a platform role or the platform-minted instance key',
                    },
                });
            }
            if (isProvisioner && data.rotate === true) {
                log('warn', 'API key mint refused: a provisioning connector asked to rotate', {
                    callerRole: caller?.role,
                    connectorId: data.connectorId,
                });
                return res.status(403).json({
                    success: false,
                    error: { code: 'FORBIDDEN', message: 'Key rotation requires a platform role; a provisioning connector may not rotate' },
                });
            }
        }
        const apiKey = {
            // Internal record ID — not a secret, but using crypto.randomUUID keeps
            // us consistent with the no-Math.random rule across the codebase.
            id: `key_${crypto_1.default.randomUUID()}`,
            // #1521 gate m1: stored in the SAME form the organisation arm compares (normaliseOrgId: trimmed,
            // lower-case, blank = absent). A raw write let a padded or upper-case own id pass the arm and then
            // vanish from its own organisation's listing, and stored a blank id as '' instead of absent.
            organizationId: (0, shared_2.normaliseOrgId)(data.organizationId),
            tenantId,
            name: data.name,
            keyHash,
            keyPrefix,
            scopes: data.scopes,
            rateLimit: data.rateLimit,
            rateLimitWindow: data.rateLimitWindow,
            usageCount: 0,
            isActive: true,
            expiresAt: data.expiresAt ? new Date(data.expiresAt) : undefined,
            createdAt: new Date(),
            connectorId: data.connectorId,
        };
        // KS-888 (Kam ruled 2026-09-28, the KS-1194 contract): a mint whose save did not persist is never
        // acknowledged, and no key material leaves the service. The in-memory copy is dropped so the
        // unsaved key is neither listed nor valid. An infrastructure fault (the auth dbErrors classes:
        // SQLSTATE 08, 53, 57, a lost socket, a pool timeout) answers a retryable 503; anything else 500.
        //
        // KS-577 + KS-1549. A rotate saves the key and retires the connector's prior keys in ONE transaction,
        // serialised per connector (saveKeyAndRetirePriors), so concurrent rotates leave exactly one active
        // key. The mint still stands if only the retire fails: priorKeysRevoked is then null and reported.
        let priorKeysRevoked = null;
        try {
            if (data.rotate && data.connectorId) {
                priorKeysRevoked = await saveKeyAndRetirePriors(apiKey, data.connectorId);
            }
            else {
                await dbSaveApiKey(apiKey, { rethrow: true });
            }
        }
        catch (saveErr) {
            exports.memApiKeys.delete(apiKey.id);
            let infra = false;
            let code;
            try {
                infra = isInfrastructureDbError(saveErr);
                code = saveErr?.code;
            }
            catch {
                // A thrown value that cannot be read cannot be classified: no code, not infrastructure (500), as for any non-infrastructure error.
            }
            log('error', 'KS-888: API key mint refused, the key could not be saved', { keyId: apiKey.id, code, infra });
            return res.status(infra ? 503 : 500).json({
                success: false,
                error: { code: infra ? 'SERVICE_UNAVAILABLE' : 'INTERNAL_ERROR', message: 'The API key could not be saved, so no key was issued' },
            });
        }
        // KS-577's order still holds inside that transaction: MINT FIRST, THEN REVOKE. A failed revoke leaves
        // the old key live, the status quo being fixed; a failed mint after a revoke would leave the connector
        // with NO working credential. The worse failure is the outage, so the retire goes second, under a
        // savepoint, and reports itself.
        log('info', 'API key created', { keyId: apiKey.id, organizationId: apiKey.organizationId });
        res.status(201).json({
            success: true,
            data: {
                id: apiKey.id,
                key: keyValue, // Only returned once at creation
                prefix: keyPrefix,
                name: apiKey.name,
                scopes: apiKey.scopes,
                rateLimit: apiKey.rateLimit,
                createdAt: apiKey.createdAt,
                connectorId: apiKey.connectorId || null,
                // KS-577: reported, not assumed. `null` means the revoke was attempted
                // and FAILED, so the prior credential is still valid — a caller that
                // ignores this is back to the bug.
                ...(data.rotate && data.connectorId ? { priorKeysRevoked } : {}),
            },
        });
    }
    catch (error) {
        if (error instanceof zod_1.z.ZodError) {
            return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: (0, zod3_compat_1.zod3Issues)(error.issues) } });
        }
        next(error);
    }
});
/**
 * GET /api/keys
 * List API keys for organization
 */
app.get('/api/keys', requireKeyAdmin, (req, res) => {
    const { organizationId } = req.query;
    if (!organizationId) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'organizationId required' } });
    }
    // KS-742: requireKeyAdmin checks the ROLE only, and KEY_ADMIN_ROLES includes
    // the tenant-scoped ORG_ADMIN / ISSUER_ADMIN / ADMIN — the same gap KS-643
    // closed on revoke. `organizationId` arrives straight from the query string
    // and memApiKeys is warmed CROSS-TENANT by loadFromDb at boot, so without
    // this a tenant-A admin naming tenant-B's organisation was handed that
    // customer's key ids, names, prefixes and full scope lists. Measured live
    // before this fix: 200 + one foreign key, against a 401 no-token control and
    // a SUPER_ADMIN control returning the identical payload.
    //
    // Filtering (rather than 403) is deliberate and follows GET /api/audit two
    // hundred lines up, which solved this exact problem under KS-28: a list
    // scoped to nothing the caller may see leaks no existence. The tenant-less
    // non-platform caller is refused outright, for the reason decideTenantAccess
    // gives — defaulting would hand them the default tenant's keys.
    const caller = req.user;
    const callerIsPlatform = (0, keyRevokePolicy_1.isPlatformRole)(caller?.role);
    if (!callerIsPlatform && !caller?.tenantId) {
        log('warn', 'API key list refused: caller has no tenant', { callerRole: caller?.role });
        return res.status(403).json({
            success: false,
            error: { code: 'FORBIDDEN', message: 'API key management requires a tenant context' },
        });
    }
    // KS-1553 (a): compare in the form the mint STORES. Since #1521 the mint stores normaliseOrgId(id)
    // (trimmed, lower-cased, blank = absent), so a raw compare missed an organisation listing its own keys
    // with its id in upper case. The SAME function, from @secuura/shared, on BOTH sides: a key stored before
    // #1521 in upper-case or padded form (KS-1565) must stay listable too. A query that normalises to null
    // (whitespace-only, or a repeated parameter, which Express parses as an array) matches nothing: null
    // must not equal the stored null of every org-less, tenant-level key.
    // KS-1577 (ruled: accept as is): a key whose STORED organisation id is blank (whitespace-only, which
    // only a pre-#1521 mint or a direct write can produce) normalises to null too, so NO query lists it.
    // Before KS-1553 (a) it was listed by the exact blank query. It is still revocable by id.
    // The list still has NO organisation arm for ORG_ADMIN / ISSUER_ADMIN (KS-1574), nor for a scoped ADMIN
    // (KS-1570 bounds the mint and the revoke): a scoped ADMIN can still list other organisations' keys.
    const wantedOrg = (0, shared_2.normaliseOrgId)(typeof organizationId === 'string' ? organizationId : null);
    const keys = Array.from(exports.memApiKeys.values())
        .filter(k => wantedOrg !== null && (0, shared_2.normaliseOrgId)(k.organizationId) === wantedOrg)
        .filter(k => callerIsPlatform || k.tenantId === caller.tenantId)
        .map(k => ({
        id: k.id,
        name: k.name,
        prefix: k.keyPrefix,
        scopes: k.scopes,
        lastUsedAt: k.lastUsedAt,
        usageCount: k.usageCount,
        isActive: k.isActive,
        createdAt: k.createdAt,
        connectorId: k.connectorId || null,
    }));
    res.json({
        success: true,
        data: keys,
    });
});
/**
 * DELETE /api/keys/:id
 * Revoke an API key
 */
app.delete('/api/keys/:id', requireKeyAdmin, async (req, res, next) => {
    const apiKey = await dbGetApiKey(req.params.id);
    if (!apiKey) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'API key not found' } });
    }
    // KS-643: requireKeyAdmin checks the ROLE only, and KEY_ADMIN_ROLES includes
    // the tenant-scoped ORG_ADMIN / ISSUER_ADMIN / ADMIN — so without this a
    // tenant-scoped admin could revoke another customer's key. Resolve first,
    // then authorise: the comparison needs the key's own tenant.
    // KS-764: the key's ORGANISATION goes in too. Tenant alone let an org-bounded
    // admin in organisation A revoke organisation B's key inside the same tenant.
    // KS-1570 (Kam's ruling, shape b): an ADMIN revokes only keys of organisations in its ADMIN
    // ORGANISATION SCOPE. Read only when it can matter (an ADMIN, a key that names an organisation). A read
    // that fails is answered 5xx and revokes nothing; it is never an allow.
    const revokeCaller = req.user;
    let adminOrganisationScope;
    if ((0, keyRevokePolicy_1.isScopedAdminRole)(revokeCaller?.role) && (0, shared_2.normaliseOrgId)(apiKey.organizationId) !== null) {
        try {
            adminOrganisationScope = await (0, adminScope_1.getAdminOrganisationScope)(revokeCaller?.tenantId, revokeCaller?.userId ?? revokeCaller?.sub);
        }
        catch (err) {
            return next(err);
        }
    }
    const decision = (0, keyRevokePolicy_1.decideKeyRevoke)(req.user, {
        id: apiKey.id,
        tenantId: apiKey.tenantId,
        organizationId: apiKey.organizationId,
    }, adminOrganisationScope !== undefined ? { adminOrganisationScope } : undefined);
    if (!decision.allow) {
        log('warn', 'Cross-tenant API key revoke refused', {
            keyId: apiKey.id,
            keyTenantId: apiKey.tenantId,
            keyOrganizationId: apiKey.organizationId,
            callerTenantId: req.user?.tenantId,
            callerOrganizationId: req.user?.organizationId,
            callerRole: req.user?.role,
            reason: decision.reason,
        });
        // KS-764: the message no longer asserts "another tenant" — the refusal now
        // has four causes and three of them are not that. Saying the wrong one to a
        // caller debugging a 403 costs them the time the message was meant to save.
        return res.status(decision.status ?? 403).json({
            success: false,
            error: { code: 'FORBIDDEN', message: 'Not authorised to revoke this API key' },
        });
    }
    apiKey.isActive = false;
    // KS-888 (card secuura-ks888-revoke-validate-on-failed-save, option a, the default from 2026-09-28 18:00):
    // a revoke whose save did not persist is not acknowledged. The in-memory revoke above is KEPT, so the key
    // stops working in this process, and the caller is told the revoke was not stored: 503 for an infrastructure
    // fault (the mint classifier: SQLSTATE 08, 53, 57, a lost socket, a pool timeout), 500 for anything else.
    // The try is required: this handler takes no next, so an uncaught throw would end the process (KS-888 r2).
    try {
        await dbSaveApiKey(apiKey, { rethrow: true });
    }
    catch (saveErr) {
        let infra = false;
        let code;
        try {
            infra = isInfrastructureDbError(saveErr);
            code = saveErr?.code;
        }
        catch {
            // A thrown value that cannot be read cannot be classified: no code, not infrastructure (500), as for any non-infrastructure error.
        }
        log('error', 'KS-888: API key revoke not stored, the key is revoked in this process only', { keyId: apiKey.id, code, infra });
        return res.status(infra ? 503 : 500).json({
            success: false,
            error: { code: infra ? 'SERVICE_UNAVAILABLE' : 'INTERNAL_ERROR', message: 'The API key revoke could not be saved, so it may not survive a restart' },
        });
    }
    log('info', 'API key revoked', { keyId: apiKey.id });
    res.json({
        success: true,
        message: 'API key revoked',
    });
});
/**
 * KS-1570 PR B: an ADMIN's ORGANISATION SCOPE, written and read by a PLATFORM role only.
 *
 * PR A made the mint and the revoke read `admin_organisation_scopes`; this is the only way to write it.
 * Wednesday's rulings, each enforced here:
 *   - platform roles only (platformRoleGate): an ADMIN can never widen its own scope;
 *   - validated at WRITE time, because the table has no foreign keys (the pull request 1535 gate's m3):
 *     the target is an ADMIN of that tenant, and every organisation belongs to that tenant;
 *   - PUT REPLACES the set (an empty list clears it); duplicates and case variants collapse;
 *   - the audit row is written on the SAME transaction as the change, so a failed audit insert rolls the
 *     scope change back (dbSaveAuditLog would swallow the error; see systemAuditInsertStatement);
 *   - a pure scope write: removing an organisation revokes no key (that is an ops step).
 */
function requireAdminScopeWriter(req, res, next) {
    platformRoleGate('Admin organisation scopes', req, res, next);
}
const UUID_TEXT = zod_1.z.string().guid().transform((v) => v.toLowerCase());
exports.adminScopeParamsSchema = zod_1.z.object({ userId: UUID_TEXT });
exports.adminScopePutSchema = zod_1.z.object({
    tenantId: UUID_TEXT,
    organizationIds: zod_1.z.array(UUID_TEXT).max(1000),
});
exports.adminScopeGetQuerySchema = zod_1.z.object({ tenantId: UUID_TEXT });
function badRequestFromZod(res, error) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: (0, zod3_compat_1.zod3Issues)(error.issues) } });
}
app.put('/api/keys/admin-scopes/:userId', requireAdminScopeWriter, async (req, res, next) => {
    try {
        const { userId } = exports.adminScopeParamsSchema.parse(req.params);
        const body = exports.adminScopePutSchema.parse(req.body);
        const tenantId = body.tenantId;
        const wanted = [...new Set(body.organizationIds)].sort();
        if (!(0, db_1.isDbAvailable)()) {
            return res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Admin organisation scopes need the database' } });
        }
        // The pull request 1539 gate's m2: the target must also be LIVE. A user with role ADMIN and
        // status 'deleted' could be granted a scope (200, row written) — harmless while the account cannot
        // log in, but the grant revives silently if it is reactivated or re-promoted. `users.status` is
        // NOT NULL DEFAULT 'active' (checked against the schema, so this adds no NULL hole).
        //
        // KS-1598 (the pull request 1539 gate's m1): the status comparison FOLDS CASE, as the role one
        // already did with upper(role). This column is stored in either case on purpose —
        // migrations/046_users_status_vocabulary.sql bounds it with `CHECK (lower(status) IN (...))` at
        // :60, under the constraint name `users_status_vocabulary`, and says at :47 "Case is folded
        // rather than forbidden: mapDbStatus already accepts either case". (:34 and :41 are the
        // NORMALISING UPDATE's `NOT IN`, not the constraint — the pull request 1548 gate's i1 corrected
        // that citation.) With a raw `status = 'active'` a live ADMIN whose row held 'ACTIVE' satisfied
        // the CHECK and failed this guard, so a platform operator got 404 for a user plainly present.
        //
        // The fold is `COLLATE "C"`, not the database's default, and that is the pull request 1548 gate's
        // m1. libc collations fold U+0130 (LATIN CAPITAL LETTER I WITH DOT ABOVE) to `i`, so a stored
        // 'ACTİVE' satisfied the CHECK *and* satisfied a default-collation `lower(status) = 'active'`,
        // while auth's `mapDbStatus` folds the same bytes with JS `toLowerCase()` and gets `acti` +
        // U+0307 + `ve`, which is outside the vocabulary — so auth read that same user as DEACTIVATED.
        // One spelling was therefore granted a scope its owner could never use. Measured on PostgreSQL
        // 15.14 under en_AU.UTF-8, and by the gate under en_US.UTF-8: `lower('ACTİVE') = 'active'` is
        // true by default and FALSE under both `COLLATE "C"` and ICU `und-x-icu`, while every ASCII
        // spelling stays true under all three. So `COLLATE "C"` is neutral for the fold this guard was
        // added for, and closed for the Unicode one.
        //
        // `upper(role) = $3` beside it carries the SAME libc-fold class — U+0131 (dotless i) upper-cases
        // to `I`, so `upper('admın') = 'ADMIN'` is true. That is PRE-EXISTING, it is not touched here,
        // and it is on its own ticket: the pull request 1548 gate's i6.
        //
        // Folding does NOT widen liveness: 'DELETED' still does not match, and neither does any other
        // status in the vocabulary in any of three spellings — the KS-1598 spectrum cells pin all 18, and
        // they read the vocabulary off the live CHECK rather than carrying a typed copy of it.
        // Purging existing rows on demotion or deletion is NOT in this change — it is on its own ticket.
        const target = await (0, shared_2.runWithTenantId)(tenantId, () => (0, db_1.query)("SELECT 1 FROM users WHERE id = $1::uuid AND tenant_id = $2::uuid AND upper(role) = $3 AND lower(status COLLATE \"C\") = 'active' LIMIT 1", [userId, tenantId, 'ADMIN']));
        if (target.rows.length === 0) {
            return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'No ADMIN with that id in that tenant' } });
        }
        if (wanted.length > 0) {
            const found = await (0, shared_2.runWithTenantId)(tenantId, () => (0, db_1.query)('SELECT id::text AS id FROM organizations WHERE tenant_id = $1::uuid AND id = ANY($2::uuid[])', [tenantId, wanted]));
            const known = new Set(found.rows.map((r) => r.id));
            const unknown = wanted.filter((o) => !known.has(o));
            if (unknown.length > 0) {
                return res.status(400).json({
                    success: false,
                    error: {
                        code: 'BAD_REQUEST',
                        message: `Not organisations of tenant ${tenantId}: ${unknown.join(', ')}`,
                        details: { unknownOrganizationIds: unknown },
                    },
                });
            }
        }
        const caller = req.user;
        const callerId = String(caller?.userId ?? caller?.sub ?? '');
        const callerUuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(callerId) ? callerId : undefined;
        const grantedBy = callerId || String(caller?.role ?? 'platform');
        const audit = {
            id: crypto_1.default.randomUUID(),
            tenantId,
            userId: callerUuid,
            action: 'admin_scope.set',
            resourceType: 'admin_organisation_scope',
            resourceId: userId,
            ipAddress: req.ip,
            userAgent: req.headers['user-agent'],
            details: {},
            success: true,
            createdAt: new Date(),
        };
        const before = await (0, shared_2.runWithTenantId)(tenantId, () => (0, db_1.transaction)(async (client) => {
            await (0, shared_2.applyTenantGuc)(client);
            // KS-1570 PR B, the pull request 1539 gate's M1 (Major). Without this line two overlapping PUTs
            // for the same ADMIN leave the UNION of their sets, not the last write: Y's DELETE waits on X's
            // row lock, then under READ COMMITTED re-reads, finds the old row gone and CANNOT see X's
            // newly inserted row, so it inserts its own beside it. The gate measured {A2, A3} stored 3 runs
            // of 3, with the last audit row reporting before [A1] → after [A3] — a grant WIDER than any
            // request asked for, described by an audit row that misstates it. On a route whose whole purpose
            // is an exact, audited authorisation grant, that is the defect, not an edge case.
            //
            // Serialised per (tenant, user) INSIDE the transaction, so the lock is released at COMMIT or
            // ROLLBACK and cannot outlive the request. `pg_advisory_xact_lock` and not `SELECT … FOR UPDATE`
            // for two reasons: it is the variant the gate actually measured green, and FOR UPDATE needs a
            // row to lock — on a FIRST grant there is none, which is exactly when two concurrent writers
            // are most likely. KS-1549 serialises concurrent rotates per connector the same way.
            // KS-1598, carried from bd11c34e as DEFENCE IN DEPTH and NOT as a fix. Stated carefully,
            // because the commit it came from claimed the opposite and was wrong:
            //   `hashtext()` IS case-sensitive while `uuid` comparison is not, so an un-lowered key pair
            //   WOULD fail to serialise two callers who spelled the same ids in different hex case.
            //   On this route that cannot happen today: `UUID_TEXT` (see adminScopeParamsSchema /
            //   adminScopePutSchema) is `z.string().uuid().transform(toLowerCase)`, so both `tenantId` and
            //   `userId` arrive ALREADY lower-cased and the lock folds case end to end without this.
            //   The pull request 1539 r2 gate measured that end to end (its F1, one waiter seen, exact
            //   audit chain) and its mutant R4 — the lock keyed on raw ids — was killed by F1.
            // So this adds no behaviour today. It is here so the key stays case-insensitive if a future
            // caller path ever reaches this lock without passing through UUID_TEXT.
            // CONSEQUENCE worth knowing: with lower() inside the key, mutant R4 becomes EQUIVALENT BY
            // CONSTRUCTION rather than killable — SQL re-normalises the raw ids, so R4 and the original
            // compute the same key. A surviving R4 after this change is not a coverage hole.
            await client.query('SELECT pg_advisory_xact_lock(hashtext(lower($1)), hashtext(lower($2)))', [tenantId, userId]);
            const prev = await client.query('SELECT organization_id::text AS o FROM admin_organisation_scopes WHERE tenant_id = $1::uuid AND user_id = $2::uuid ORDER BY 1', [tenantId, userId]);
            await client.query('DELETE FROM admin_organisation_scopes WHERE tenant_id = $1::uuid AND user_id = $2::uuid', [tenantId, userId]);
            if (wanted.length > 0) {
                await client.query(`INSERT INTO admin_organisation_scopes (tenant_id, user_id, organization_id, granted_by)
           SELECT $1::uuid, $2::uuid, o, $3 FROM unnest($4::uuid[]) AS o`, [tenantId, userId, grantedBy, wanted]);
            }
            const b = prev.rows.map((r) => r.o);
            audit.details = { tenantId, targetUserId: userId, before: b, after: wanted, grantedBy };
            const st = systemAuditInsertStatement(audit);
            await client.query(st.text, st.values);
            return b;
        }));
        rememberAuditLog(audit);
        log('info', 'Admin organisation scope set', { tenantId, targetUserId: userId, before, after: wanted });
        return res.json({ success: true, data: { userId, tenantId, before, organizationIds: wanted } });
    }
    catch (error) {
        let isZod = false;
        let infra = false;
        try {
            isZod = error instanceof zod_1.z.ZodError;
            infra = isInfrastructureDbError(error);
        }
        catch {
            // A thrown value that cannot be read cannot be classified: hand the error handler an ordinary Error, as for any non-infrastructure error.
            return next(new Error('unreadable thrown value'));
        }
        if (isZod)
            return badRequestFromZod(res, error);
        // The pull request 1539 gate's m1. An infrastructure fault reached errorHandler and answered a
        // generic 500 INTERNAL_ERROR, while develop's mint path answers 503 for the same killed backend.
        // Fail-closed held either way — the transaction rolls back and nothing is written — but a 500 tells
        // a caller the request was wrong when the honest answer is "retry".
        if (infra) {
            // Read off the request, not the parsed locals: those are declared inside the try and are not in
            // scope here, which tsc caught.
            log('error', 'Admin organisation scope write failed on infrastructure, nothing written', {
                tenantId: req.body?.tenantId,
                targetUserId: req.params?.userId,
                code: error?.code,
            });
            return res.status(503).json({
                success: false,
                error: { code: 'SERVICE_UNAVAILABLE', message: 'The admin organisation scope could not be written, so nothing changed' },
            });
        }
        return next(error);
    }
});
app.get('/api/keys/admin-scopes/:userId', requireAdminScopeWriter, async (req, res, next) => {
    try {
        const { userId } = exports.adminScopeParamsSchema.parse(req.params);
        const { tenantId } = exports.adminScopeGetQuerySchema.parse(req.query);
        if (!(0, db_1.isDbAvailable)()) {
            return res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Admin organisation scopes need the database' } });
        }
        const r = await (0, shared_2.runWithTenantId)(tenantId, () => (0, db_1.query)('SELECT organization_id::text AS o FROM admin_organisation_scopes WHERE tenant_id = $1::uuid AND user_id = $2::uuid ORDER BY 1', [tenantId, userId]));
        return res.json({ success: true, data: { userId, tenantId, organizationIds: r.rows.map((x) => x.o) } });
    }
    catch (error) {
        let isZod;
        try {
            isZod = error instanceof zod_1.z.ZodError;
        }
        catch {
            return next(new Error('unreadable thrown value'));
        }
        if (isZod)
            return badRequestFromZod(res, error);
        return next(error);
    }
});
/**
 * POST /api/keys/validate
 * Validate an API key
 */
app.post('/api/keys/validate', async (req, res) => {
    // KS-444: schema-validate instead of truthy-check — a wrong-typed `key`
    // (object/number) previously reached crypto.createHash().update() and threw.
    const parsedBody = requestSchemas_1.validateKeySchema.safeParse(req.body);
    if (!parsedBody.success) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'API key required', details: (0, zod3_compat_1.zod3Issues)(parsedBody.error.issues) } });
    }
    const { key } = parsedBody.data;
    const keyHash = crypto_1.default.createHash('sha256').update(key).digest('hex');
    let apiKey = Array.from(exports.memApiKeys.values()).find(k => k.keyHash === keyHash);
    // KS-39 #5: in-memory map is populated only at boot from svc_api_keys.
    // Keys minted by originate AFTER security started are invisible until
    // the next restart, so any test or runtime caller minting a key + using
    // it within the same uptime window saw "invalid api key" even though
    // the row was correctly in svc_api_keys. Fall through to a fresh DB
    // lookup on cache-miss before we declare the key invalid, and warm the
    // memory cache for next time.
    // KS-1370 half (ii): a cache HIT is a boot-time snapshot, so it cannot be trusted for the one
    // question this route exists to answer. A revoke performed in ANOTHER process is invisible here,
    // and answering `valid: true` from that snapshot is how a revoked credential kept working.
    // So on a cache hit, re-read the STORED state through the same reviewed carve-out the cache-miss
    // branch uses, and decide on the stored row rather than on memory.
    //
    // Kam's ruling, card `secuura-ks1370-validate-when-the-revoke-check-cannot-read`, option (a):
    // "Split: refuse on a failed read, memory-only mode answers from memory. A failed stored read with
    // a database configured returns 503 'Unable to verify key'. ... A revoked key is never honoured.
    // Memory-only deployments behave as today. The usage write stays log-only, as you ruled."
    // Hence the isDbAvailable() guard: with NO database configured there is no stored state to be
    // blind to — memory IS the store of record in that mode, and the revoke route writes isActive
    // false into it — so refusing there would break every memory-only deployment and #1334's control
    // C4 for no security gain. That is a deployment with no store, not an unverifiable read.
    //
    // The stale copy is REFRESHED, not merely consulted, so the cache stops lying for later requests
    // in this process. A row that has VANISHED is treated as not found and evicted: a deleted key is a
    // stronger revocation than is_active=false, and a stale copy must not honour it either.
    //
    // This handler takes NO `next` (see ks888-failed-mint-save-issues-no-key.test.ts:5-7), so a throw
    // here would be an unhandled rejection that can end the process. The read therefore has its own
    // try and every exit from it is a response, never a throw.
    if (apiKey && (0, db_1.isDbAvailable)()) {
        try {
            const storedResult = await (0, db_1.query)('SELECT * FROM security_find_api_key_by_hash($1)', [keyHash]);
            if (storedResult.rows.length === 0) {
                exports.memApiKeys.delete(apiKey.id);
                return res.json({ success: true, data: { valid: false, reason: 'Key not found' } });
            }
            // A REVOKE IS STICKY IN BOTH DIRECTIONS, and this line is the one that keeps KS-888 intact.
            // KS-888 (card secuura-ks888-revoke-validate-on-failed-save, option a) says a revoke whose
            // SAVE failed keeps its in-memory revoke, so the key stops working in this process even though
            // the row still reads active. Refreshing blindly from the stored row would UNDO exactly that
            // and re-honour a key an operator has revoked — measured: #1334's cell R2 fails without this.
            // So the two sources are combined in the safe direction: revoked if EITHER says revoked.
            // Stored-revoked beats cached-active (that is KS-1370), and cached-revoked beats
            // stored-active (that is KS-888 R2). Neither source can revive a revocation the other holds.
            const revokedInMemory = apiKey.isActive === false;
            apiKey = (0, converters_1.rowToApiKey)(storedResult.rows[0]);
            if (revokedInMemory)
                apiKey.isActive = false;
            exports.memApiKeys.set(apiKey.id, apiKey);
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
            logger_1.logger.error('KS-1370: stored API key state could not be read', { error: reason });
            return res.status(503).json({
                success: false,
                error: { code: 'SERVICE_UNAVAILABLE', message: 'Unable to verify key' },
            });
        }
    }
    if (!apiKey) {
        try {
            // KS-458: this route is deliberately unauthenticated (the gateway calls
            // it BEFORE any session exists — see the KS-39 #5 auth carve-out above),
            // so there is no tenant context to set the RLS GUC from. Under the
            // fail-closed tenant_isolation policy a direct SELECT on svc_api_keys
            // would return zero rows and break every sk_* API-key auth. The
            // migration-039 SECURITY DEFINER function is the reviewed pre-session
            // carve-out: same row shape (SETOF svc_api_keys), lookup by hash only.
            const dbResult = await (0, db_1.query)('SELECT * FROM security_find_api_key_by_hash($1)', [keyHash]);
            if (dbResult.rows.length > 0) {
                apiKey = (0, converters_1.rowToApiKey)(dbResult.rows[0]);
                exports.memApiKeys.set(apiKey.id, apiKey);
            }
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
            logger_1.logger.warn('DB fallback for api-key validation failed', { error: reason });
        }
    }
    if (!apiKey) {
        return res.json({ success: true, data: { valid: false, reason: 'Key not found' } });
    }
    if (!apiKey.isActive) {
        return res.json({ success: true, data: { valid: false, reason: 'Key revoked' } });
    }
    if (apiKey.expiresAt && apiKey.expiresAt < new Date()) {
        return res.json({ success: true, data: { valid: false, reason: 'Key expired' } });
    }
    // Update usage
    apiKey.lastUsedAt = new Date();
    apiKey.usageCount++;
    // KS-1370 half (i): usage-only. dbSaveApiKey would carry is_active and revive a revoke.
    await dbRecordApiKeyUsage(apiKey);
    res.json({
        success: true,
        data: {
            valid: true,
            organizationId: apiKey.organizationId,
            // KS-33: return tenantId so the gateway's auth middleware can set
            // req.tenantId from sk_* requests without an extra DB roundtrip.
            // Pre-KS-33 this field was missing from the response and the
            // gateway fell back to '' (empty), which broke every downstream
            // tenant-scoped query for sk_*-authenticated requests.
            tenantId: apiKey.tenantId,
            scopes: apiKey.scopes,
            rateLimit: apiKey.rateLimit,
            rateLimitWindow: apiKey.rateLimitWindow,
            connectorId: apiKey.connectorId || null,
        },
    });
});
// =============================================================================
// RATE LIMIT ROUTES
// =============================================================================
/**
 * POST /api/rate-limit/check
 * Check and increment rate limit
 */
app.post('/api/rate-limit/check', (req, res, next) => {
    try {
        const data = exports.checkRateLimitSchema.parse(req.body);
        // KS-952 F3/F4: the bucket is DERIVED from the verified principal; the body
        // can no longer choose it. `data.key` is now a label WITHIN the caller's own
        // namespace, so naming another tenant's key selects a bucket of the caller's
        // own rather than the owner's. That closes both directions of one lever: the
        // 1s window that turned an owner's 100/minute into 100/second (60x), and the
        // 24h window that turned an intended 60s lockout into 1440x.
        //
        // No platform exception, deliberately. Cross-tenant reach is a capability on
        // /reset; on a *check* naming someone else's bucket IS the attack, so there
        // is nobody this route should let do it.
        const scope = (0, rateLimitScope_1.principalScope)(req.user);
        if (scope === null) {
            // KS-743's rule applied here: a missing claim is a refusal, not a wildcard.
            // Defaulting to a shared namespace would put unrelated callers in one
            // bucket, which is the same fail-open this change exists to remove.
            return res.status(403).json({
                success: false,
                // KS-976 item 2: scope is null for three reasons - say whether a claim was present but unusable, or absent.
                error: { code: 'FORBIDDEN', message: [req.user?.tenantId, req.user?.userId, req.user?.sub].some((v) => v !== undefined && v !== null) ? 'Caller scope claims are present but unusable (tenant, user or sub)' : 'Caller has no tenant' },
            });
        }
        const bucketKey = (0, rateLimitScope_1.scopedRateLimitKey)(scope, data.key);
        const now = Date.now();
        const stored = exports.rateLimits.get(bucketKey);
        // KS-698 fix 3: SELF-HEAL. A key poisoned before this fix holds a resetAt
        // outside the time-value range, so `now > entry.resetAt` is false and every
        // later request reached `new Date(entry.resetAt).toISOString()` and threw —
        // 500 forever for that key, however valid the new request was. Because the
        // limiter fails OPEN on error (KS-616) that key was effectively unlimited: a
        // CORRECTED by the #882 tier-1 gate: this said "a rate-limit BYPASS", and that is
        // WRONG on two counts, both measured. KS-616 is a DIFFERENT limiter that never
        // calls this endpoint, and its fail-open was already remediated at this SHA. The
        // impact is AVAILABILITY — a caller-named key permanently answering 500.
        // treated as expired, so poisoned keys recover on their next request rather
        // than needing a flush.
        const entry = (0, rateLimitBounds_1.usableRateLimitEntry)(stored);
        if (!entry || now > entry.resetAt) {
            // KS-698 fix 2: compute BEFORE the write and refuse to persist a value we
            // cannot render. The original order wrote the entry and THEN threw while
            // formatting the response, so the bad state outlived the failed request.
            // Unreachable from this route now that the schema bounds windowMs — kept
            // because it guards the WRITE rather than the INPUT, and those can drift.
            const resetAt = (0, rateLimitBounds_1.persistableResetAt)(now, data.windowMs);
            if (resetAt === null) {
                return res.status(400).json({
                    success: false,
                    error: {
                        code: 'BAD_REQUEST',
                        message: 'windowMs produces a reset time outside the representable range',
                    },
                });
            }
            // KS-952 F10: sweep expired entries before growing the map. Only expired
            // ones go — dropping a live bucket would itself be a bypass.
            (0, rateLimitScope_1.sweepExpired)(exports.rateLimits, now);
            exports.rateLimits.set(bucketKey, { count: 1, resetAt });
            return res.json({
                success: true,
                data: {
                    allowed: true,
                    remaining: data.limit - 1,
                    resetAt: new Date(now + data.windowMs).toISOString(),
                },
            });
        }
        if (entry.count >= data.limit) {
            return res.json({
                success: true,
                data: {
                    allowed: false,
                    remaining: 0,
                    resetAt: new Date(entry.resetAt).toISOString(),
                    retryAfter: Math.ceil((entry.resetAt - now) / 1000),
                },
            });
        }
        entry.count++;
        res.json({
            success: true,
            data: {
                allowed: true,
                remaining: data.limit - entry.count,
                resetAt: new Date(entry.resetAt).toISOString(),
            },
        });
    }
    catch (error) {
        if (error instanceof zod_1.z.ZodError) {
            return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: (0, zod3_compat_1.zod3Issues)(error.issues) } });
        }
        next(error);
    }
});
/**
 * POST /api/rate-limit/reset
 * Reset rate limit for a key
 */
app.post('/api/rate-limit/reset', requirePlatformOperatorForRateLimit, (req, res) => {
    // KS-444: schema-validate instead of truthy-check — a wrong-typed `key`
    // (object/number) was previously accepted and answered 200 "Rate limit reset".
    const parsedBody = requestSchemas_1.resetRateLimitSchema.safeParse(req.body);
    if (!parsedBody.success) {
        // KS-976 item 1: the message names the field that actually failed. It was the
        // constant 'Key required', which was wrong for every refusal that was not about
        // the key - and `tenantId`/`userId` refusals are exactly what KS-970 item 6
        // published. `details` is unchanged and remains the authoritative, parseable half.
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: (0, requestRefusal_1.bodyRefusalMessage)(parsedBody.error), details: (0, zod3_compat_1.zod3Issues)(parsedBody.error.issues) } });
    }
    // KS-952 (the folded-in KS-645 half): /check now stores under a
    // principal-derived namespace, so a raw key would no longer match anything and
    // this route would silently become a no-op. The platform operator therefore
    // names the SCOPE explicitly — which is also the capability the strict rule on
    // /check must NOT be copied onto: clearing another tenant's bucket is
    // plausibly what a platform-operator reset is FOR.
    //
    // Only a platform role reaches this line (requirePlatformOperatorForRateLimit
    // above), so there is deliberately NO "a tenant role may name only its own"
    // arm — no tenant role can reach the route, and code that cannot be exercised
    // is a check that cannot fail wearing a feature's clothes. If the gate is ever
    // relaxed, `explicitScope` is the one place that rule goes.
    const scope = (0, rateLimitScope_1.explicitScope)(parsedBody.data, req.user);
    if (scope === null) {
        return res.status(403).json({
            success: false,
            error: { code: 'FORBIDDEN', message: [req.user?.tenantId, req.user?.userId, req.user?.sub].some((v) => v !== undefined && v !== null) ? 'Caller scope claims are present but unusable (tenant, user or sub)' : 'Caller has no tenant' },
        });
    }
    exports.rateLimits.delete((0, rateLimitScope_1.scopedRateLimitKey)(scope, parsedBody.data.key));
    res.json({
        success: true,
        message: 'Rate limit reset',
    });
});
// =============================================================================
// ERROR HANDLING
// =============================================================================
app.use((_req, res) => {
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Not Found' } });
});
// KS-111: route errors through the shared AppError-aware handler (maps
// AppError.statusCode + Zod -> 4xx; emits the canonical {success,error} shape).
app.use(shared_2.errorHandler);
// =============================================================================
// START SERVER
// =============================================================================
// Audit 1.3 phase 5: PII keyring for audit_logs.details encryption.
if (process.env.PII_ENCRYPTION_KEY) {
    try {
        (0, shared_2.initFromEnv)();
        log('info', 'PII encryption keyring initialised');
    }
    catch (err) {
        log('warn', 'PII encryption init failed (audit_logs.details will store plaintext)', { error: err?.message });
    }
}
else if (process.env.NODE_ENV === 'production') {
    log('error', 'FATAL: PII_ENCRYPTION_KEY missing in production — refusing to start');
    process.exit(1);
}
else {
    log('warn', 'PII_ENCRYPTION_KEY not set — audit_logs.details will store plaintext');
}
/**
 * One-shot DB boot work: warm the in-memory caches (audit logs, security
 * events, API keys) and apply the idempotent audit_logs.details widening.
 * Passed to initDb as its onReady hook so it runs on the boot success path
 * AND again when the DB only comes up after a lost start race (KS-377
 * background retry) — recovery re-runs it instead of silently skipping it
 * (KS-382).
 */
async function runDbBootTasks() {
    await loadFromDb();
    // Audit 1.3 phase 5: widen audit_logs.details from JSONB to TEXT so
    // AES-GCM ciphertext fits. Idempotent — only runs if currently jsonb.
    try {
        await (0, db_1.query)(`
      DO $$ BEGIN
        IF EXISTS (
          SELECT 1 FROM information_schema.columns
          WHERE table_name='audit_logs' AND column_name='details' AND data_type='jsonb'
        ) THEN
          ALTER TABLE audit_logs ALTER COLUMN details TYPE TEXT USING details::text;
        END IF;
      END $$
    `);
        log('info', 'audit_logs.details migration applied (or already TEXT)');
    }
    catch (err) {
        log('warn', 'audit_logs.details migration failed (non-fatal)', { error: err?.message });
    }
}
// KS-742: the /api/keys routes had no wire test because importing this module
// starts a listener and a DB connect, so a test could only call the pure policy
// functions — which is exactly how a route can keep a defect while its policy
// unit tests stay green. One documented guard makes the app importable. It is
// opt-IN: unset (every deployment) means boot, so production behaviour is
// byte-identical.
if (process.env.SECURITY_DISABLE_BOOT !== '1') {
    (0, db_1.initDb)(runDbBootTasks).then((connected) => {
        console.log('[Security] DB init:', connected);
    });
    const server = app.listen(PORT, () => {
        log('info', 'Security Service started', { port: PORT });
        console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                SECUURA SECURITY SERVICE                       ║
╠═══════════════════════════════════════════════════════════════╣
║  Port:      ${PORT}                                              ║
║  API Info:  http://localhost:${PORT}/api                          ║
║  Health:    http://localhost:${PORT}/health                       ║
╠═══════════════════════════════════════════════════════════════╣
║  Features:                                                    ║
║    • Audit Logging                                           ║
║    • Security Event Tracking                                 ║
║    • API Key Management                                      ║
║    • Rate Limiting                                           ║
╚═══════════════════════════════════════════════════════════════╝
`);
    });
    // KS-252: hold keep-alive sockets longer than any upstream proxy's idle
    // window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
    // sockets; Node's 5 s default close races their reuse -> ECONNRESET and
    // 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
    server.keepAliveTimeout = 65_000;
    server.headersTimeout = 66_000;
}
exports.default = app;
