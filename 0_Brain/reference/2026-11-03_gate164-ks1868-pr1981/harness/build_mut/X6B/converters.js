"use strict";
/**
 * =============================================================================
 * SECURITY SERVICE — row → domain converters (the ONE home)
 * =============================================================================
 * Pure functions that map a DB row to the service's domain types, kept in their
 * own import-light module so they can be unit-tested without importing the
 * express app or its side-effect dependencies (shared keyring init, env
 * validation, DB connection). T2-D.
 *
 * KS-880: index.ts used to carry a second copy of every function here, and this
 * file's copy had drifted from the live one (its rowToApiKey mapped neither
 * tenantId, the RLS-enforced tenancy field, nor connectorId - KS-869). It was
 * imported by nothing in production yet carried a passing test, so a refactor
 * onto "the canonical converters module" would have reintroduced both. These are
 * now the only definitions: index.ts imports and re-exports them, and
 * __tests__/ks880-one-mapper-home.test.ts pins that they are the same objects.
 * Keep this file free of value imports.
 * =============================================================================
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseJson = parseJson;
exports.parseJsonArray = parseJsonArray;
exports.rowToAuditLog = rowToAuditLog;
exports.rowToSecurityEvent = rowToSecurityEvent;
exports.rowToApiKey = rowToApiKey;
function parseJson(val) {
    if (!val)
        return {};
    if (typeof val === 'string') {
        try {
            return JSON.parse(val);
        }
        catch {
            return {};
        }
    }
    return val;
}
function parseJsonArray(val) {
    if (!val)
        return [];
    if (Array.isArray(val))
        return val;
    if (typeof val === 'string') {
        try {
            return JSON.parse(val);
        }
        catch {
            return [];
        }
    }
    return [];
}
/**
 * Map a DB row to an AuditLog domain object.
 * `decryptDetails` is injected: the production one needs the shared keyring (index.ts binds it), and this
 * module must stay loadable without it - env validation, a DB and a booted server are exactly what it exists
 * to be tested without.
 */
function rowToAuditLog(r, decryptDetails) {
    const id = r.id;
    return {
        id,
        // KS-28: row.tenant_id is NOT NULL on rows written post-migration 012.
        // Older rows backfilled to default tenant by the migration, so this
        // is always present. Cast to string; the default-tenant fallback here
        // is a belt-and-braces guard against a hand-edited row that somehow
        // lost the column.
        tenantId: r.tenant_id || 'a0000000-0000-4000-8000-000000000001',
        userId: r.user_id || undefined,
        organizationId: r.organization_id || undefined,
        action: r.action,
        resourceType: r.resource_type,
        resourceId: r.resource_id || undefined,
        ipAddress: r.ip_address || undefined,
        userAgent: r.user_agent || undefined,
        // Audit 1.3 phase 5: details is encrypted at rest. Plaintext-tail
        // handling for the migration window.
        details: decryptDetails(r.details, id) || {},
        previousState: r.previous_state ? parseJson(r.previous_state) : undefined,
        newState: r.new_state ? parseJson(r.new_state) : undefined,
        success: Boolean(r.success),
        errorMessage: r.error_message || undefined,
        createdAt: new Date(r.created_at),
    };
}
function rowToSecurityEvent(r) {
    return {
        id: r.id,
        eventType: r.event_type,
        severity: r.severity,
        source: r.source,
        userId: r.user_id || undefined,
        ipAddress: r.ip_address || undefined,
        details: parseJson(r.details),
        resolved: Boolean(r.resolved),
        resolvedAt: r.resolved_at ? new Date(r.resolved_at) : undefined,
        resolvedBy: r.resolved_by || undefined,
        createdAt: new Date(r.created_at),
    };
}
function rowToApiKey(r) {
    return {
        id: r.id,
        organizationId: r.organization_id ?? null,
        // KS-33: tenant_id NOT NULL post-018; default-tenant fallback is a
        // belt-and-braces guard for a hand-edited row that somehow lost it.
        tenantId: r.tenant_id || 'a0000000-0000-4000-8000-000000000001',
        name: r.name,
        keyHash: r.key_hash,
        keyPrefix: r.key_prefix,
        scopes: parseJsonArray(r.scopes),
        rateLimit: Number(r.rate_limit),
        rateLimitWindow: Number(r.rate_limit_window),
        lastUsedAt: r.last_used_at ? new Date(r.last_used_at) : undefined,
        usageCount: Number(r.usage_count),
        // KS-1639: a text value is active only when it is a text form of true; 'f' / 'false' (and anything unrecognised) read inactive.
        isActive: typeof r.is_active === 'string'
            ? /^(t|true)$/i.test(r.is_active.trim())
            : Boolean(r.is_active),
        expiresAt: r.expires_at ? new Date(r.expires_at) : undefined,
        createdAt: new Date(r.created_at),
        // KS-869: without this the loader reads every row back with no
        // connectorId, so persisting the column would change nothing observable —
        // the write and the read have to land together.
        connectorId: r.connector_id ?? undefined,
    };
}
