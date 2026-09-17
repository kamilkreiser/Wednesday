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

import express, { Request, Response, NextFunction, RequestHandler } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { z } from 'zod';
import crypto from 'crypto';
import dotenv from 'dotenv';
import { initDb, query, isDbAvailable } from './db';
import { logger } from './utils/logger';
import { validateKeySchema, resetRateLimitSchema } from './requestSchemas';
// KS-480 §4 amendment: provisioning mint policy (bootless, unit-tested).
import { decideMint, type MintRequest } from './provisioningPolicy';
import { encryptField, decryptField, initFromEnv as initPiiCrypto, authenticate as jwtAuthenticate, enforceProductionConfig, errorHandler, isoDateTimeSchema, tenantGucContext, runWithTenantId, runWithPlatformScope, rejectNulBytes } from '@secuura/shared';
import {
  MAX_RATE_LIMIT_WINDOW_MS,
  usableRateLimitEntry,
  persistableResetAt,
} from './rateLimitBounds';
import {
  RATE_LIMIT_KEY_MAX,
  principalScope,
  explicitScope,
  scopedRateLimitKey,
  sweepExpired,
} from './rateLimitScope';
import { decideKeyRevoke, decideTenantAccess, isPlatformRole, lookupKeyForRevoke } from './keyRevokePolicy';

// =============================================================================
// PII FOR audit_logs.details (audit 1.3 phase 5)
// =============================================================================
// audit_logs.details often contains user-supplied input (request bodies,
// query strings, error context). Encrypt the JSONB blob at rest with AAD
// bound to (auditLogId). The column is widened from JSONB to TEXT in the
// startup migration.

function encryptDetails(details: unknown, auditId: string): string | null {
  if (details == null) return null;
  const json = JSON.stringify(details);
  if (json === '{}' || json === 'null') return null;
  return encryptField(json, `audit_logs.details.${auditId}`);
}

function decryptDetails(stored: any, auditId: string): Record<string, unknown> | null {
  if (stored == null || stored === '') return null;
  if (typeof stored === 'string' && /^v\d+:/.test(stored)) {
    try {
      const plain = decryptField(stored, `audit_logs.details.${auditId}`);
      return plain ? JSON.parse(plain) : null;
    } catch (err: any) {
      logger.error('[piiCrypto] audit_logs.details decrypt failed', { auditId, error: err?.message });
      return null;
    }
  }
  // Legacy plaintext (still raw JSON or already-parsed object)
  if (typeof stored === 'string') {
    try { return JSON.parse(stored); } catch { return null; }
  }
  return stored as Record<string, unknown>;
}

dotenv.config();

// Production startup guard — refuse to start with dev defaults in production
enforceProductionConfig('security', {
  requiredEnvVars: ['DATABASE_URL'],
  forbiddenValues: {},
  requireRealProviders: true,
});

const app = express();
const PORT = process.env.PORT || 4004;

// =============================================================================
// TYPE DEFINITIONS
// =============================================================================

interface AuditLog {
  id: string;
  tenantId: string;             // KS-28: required after migration 012's NOT NULL
  userId?: string;
  organizationId?: string;
  action: string;
  resourceType: string;
  resourceId?: string;
  ipAddress?: string;
  userAgent?: string;
  details: Record<string, unknown>;
  previousState?: Record<string, unknown>;
  newState?: Record<string, unknown>;
  success: boolean;
  errorMessage?: string;
  createdAt: Date;
}

interface SecurityEvent {
  id: string;
  eventType: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  source: string;
  userId?: string;
  ipAddress?: string;
  details: Record<string, unknown>;
  resolved: boolean;
  resolvedAt?: Date;
  resolvedBy?: string;
  createdAt: Date;
}

interface ApiKey {
  id: string;
  // KS-33: organization_id is now NULL-able in svc_api_keys. Originate's
  // admin endpoint can issue tenant-scoped keys without an explicit org
  // (e.g. SYSTEM_ADMIN flows). Code paths that filter by org just won't
  // match null-org keys.
  organizationId: string | null;
  // KS-33: tenant_id is the load-bearing tenancy field. NOT NULL + RLS
  // enforced at the DB layer post-migration 018. Validate response
  // returns this so the gateway can set req.tenantId from sk_* requests
  // without hitting the DB again.
  tenantId: string;
  name: string;
  keyHash: string;
  keyPrefix: string;
  scopes: string[];
  rateLimit: number;
  rateLimitWindow: number;
  lastUsedAt?: Date;
  usageCount: number;
  isActive: boolean;
  expiresAt?: Date;
  createdAt: Date;
  connectorId?: string;
}

interface RateLimitEntry {
  count: number;
  resetAt: number;
}

// =============================================================================
// IN-MEMORY STORAGE (with database persistence fallback)
// =============================================================================

const memAuditLogs: AuditLog[] = [];
const memSecurityEvents: SecurityEvent[] = [];
// KS-577: exported as a test seam; see revokePriorConnectorKeys.
export const memApiKeys = new Map<string, ApiKey>();
// KS-698: exported as a test seam (see isRepresentableInstant).
export const rateLimits = new Map<string, RateLimitEntry>(); // Ephemeral - memory only

// =============================================================================
// DATABASE HELPERS
// =============================================================================

async function dbSaveAuditLog(a: AuditLog): Promise<void> {
  memAuditLogs.push(a);
  if (memAuditLogs.length > 10000) memAuditLogs.splice(0, memAuditLogs.length - 10000);
  if (!isDbAvailable()) return;
  try {
    // KS-28: tenant_id is the security boundary (NOT NULL after migration
    // 012). Sourced from the JWT-derived AuditLog.tenantId; the POST
    // handler enforces this so the in-memory cache + DB row both carry it.
    // KS-458: pin the RLS GUC to the row's own tenant — the request ALS may
    // differ (admin acting cross-tenant) or be absent (fire-and-forget after
    // the response), and fail-closed audit_logs would reject a mismatch.
    await runWithTenantId(a.tenantId, () => query(
      `INSERT INTO audit_logs (id, tenant_id, user_id, organization_id, action, resource_type, resource_id,
         ip_address, user_agent, details, previous_state, new_state, success, error_message, created_at)
       VALUES ($1,$2::uuid,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15) ON CONFLICT (id) DO NOTHING`,
      [a.id, a.tenantId, a.userId || null, a.organizationId || null, a.action, a.resourceType,
       a.resourceId || null, a.ipAddress || null, a.userAgent || null,
       // Audit 1.3 phase 5: encrypt details JSONB at rest. AAD bound to
       // the audit log id so a ciphertext can't be ported between rows.
       encryptDetails(a.details, a.id),
       a.previousState ? JSON.stringify(a.previousState) : null,
       a.newState ? JSON.stringify(a.newState) : null, a.success, a.errorMessage || null, a.createdAt]
    ));
  } catch (err: any) {
    logger.error('DB save audit log failed', { error: err?.message });
  }
}

async function dbSaveSecurityEvent(e: SecurityEvent): Promise<void> {
  memSecurityEvents.push(e);
  if (!isDbAvailable()) return;
  try {
    await query(
      `INSERT INTO svc_security_events (id, event_type, severity, source, user_id, ip_address,
         details, resolved, resolved_at, resolved_by, created_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11) ON CONFLICT (id) DO NOTHING`,
      [e.id, e.eventType, e.severity, e.source, e.userId || null, e.ipAddress || null,
       JSON.stringify(e.details || {}), e.resolved, e.resolvedAt || null, e.resolvedBy || null, e.createdAt]
    );
  } catch (err: any) {
    logger.error('DB save event failed', { error: err?.message });
  }
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
export async function revokePriorConnectorKeys(
  connectorId: string,
  tenantId: string,
  keepKeyId: string,
): Promise<number | null> {
  const graceRaw = Number.parseInt(process.env.API_KEY_ROTATION_GRACE_SECONDS ?? '0', 10);
  const grace = Number.isFinite(graceRaw) && graceRaw > 0 ? graceRaw : 0;

  // In-memory first, so a DB-less run still retires the sibling rather than
  // reporting a revoke that did not happen.
  let retired = 0;
  for (const [, k] of memApiKeys) {
    if (k.id === keepKeyId || k.connectorId !== connectorId || k.tenantId !== tenantId) continue;
    if (!k.isActive) continue;
    if (grace === 0) {
      k.isActive = false;
    } else {
      const until = new Date(Date.now() + grace * 1000);
      if (!k.expiresAt || k.expiresAt > until) k.expiresAt = until;
    }
    retired += 1;
  }

  if (!isDbAvailable()) return retired;

  try {
    // KS-458: the GUC names the row's own tenant and svc_api_keys is
    // fail-closed, so a cross-tenant rotate cannot reach another tenant's keys.
    const r = await runWithTenantId(tenantId, () => query(
      grace === 0
        ? `UPDATE svc_api_keys SET is_active = false
             WHERE connector_id = $1 AND tenant_id = $2::uuid AND id <> $3 AND is_active = true`
        : `UPDATE svc_api_keys
             SET expires_at = LEAST(COALESCE(expires_at, 'infinity'::timestamptz), NOW() + ($4 || ' seconds')::interval)
             WHERE connector_id = $1 AND tenant_id = $2::uuid AND id <> $3 AND is_active = true`,
      grace === 0 ? [connectorId, tenantId, keepKeyId] : [connectorId, tenantId, keepKeyId, String(grace)],
    ));
    return r.rowCount ?? retired;
  } catch (err) {
    // Loud, never silent. The new key is already minted and returned, so the
    // request cannot be failed without losing it — but the operator is told the
    // old credential is STILL LIVE.
    log('error', 'KS-577: revoke-on-rotate FAILED — the prior credential is still valid', {
      connectorId, tenantId, keepKeyId, error: err instanceof Error ? err.message : String(err),
    });
    return null;
  }
}

async function dbSaveApiKey(k: ApiKey): Promise<void> {
  memApiKeys.set(k.id, k);
  if (!isDbAvailable()) return;
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
    await runWithTenantId(k.tenantId, () => query(
      `INSERT INTO svc_api_keys (id, organization_id, tenant_id, name, key_hash, key_prefix, scopes,
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
      [k.id, k.organizationId, k.tenantId, k.name, k.keyHash, k.keyPrefix,
       JSON.stringify(k.scopes || []),
       k.rateLimit, k.rateLimitWindow, k.lastUsedAt || null, k.usageCount, k.isActive,
       k.expiresAt || null, k.createdAt, k.connectorId ?? null]
    ));
  } catch (err: any) {
    logger.error('DB save API key failed', { error: err?.message });
  }
}

async function dbGetApiKey(id: string): Promise<ApiKey | undefined> {
  if (isDbAvailable()) {
    try {
      // KS-578: the lookup is platform-scoped (see keyRevokePolicy). Under
      // FORCE RLS a foreign-tenant row read with the caller's tenant GUC
      // returns nothing, so a key written by another service AFTER this one
      // booted 404'd even though it exists. Safe only because the sole caller
      // — the revoke route — puts the result through decideKeyRevoke.
      // Row mapping now uses the canonical rowToApiKey rather than a second
      // inline copy, which also drops a divergence: the inline version passed
      // `scopes` straight through instead of parseJsonArray().
      const row = await lookupKeyForRevoke(id);
      if (row) return rowToApiKey(row);
    } catch { /* fall through */ }
  }
  return memApiKeys.get(id);
}

// =============================================================================
// ROW CONVERTERS — map DB rows to in-memory types
// =============================================================================

export function parseJson(val: unknown): Record<string, unknown> {
  if (!val) return {};
  if (typeof val === 'string') {
    try { return JSON.parse(val); } catch { return {}; }
  }
  return val as Record<string, unknown>;
}

export function parseJsonArray(val: unknown): string[] {
  if (!val) return [];
  if (Array.isArray(val)) return val;
  if (typeof val === 'string') {
    try { return JSON.parse(val); } catch { return []; }
  }
  return [];
}

export function rowToAuditLog(r: Record<string, unknown>): AuditLog {
  const id = r.id as string;
  return {
    id,
    // KS-28: row.tenant_id is NOT NULL on rows written post-migration 012.
    // Older rows backfilled to default tenant by the migration, so this
    // is always present. Cast to string; the default-tenant fallback here
    // is a belt-and-braces guard against a hand-edited row that somehow
    // lost the column.
    tenantId: (r.tenant_id as string) || 'a0000000-0000-4000-8000-000000000001',
    userId: (r.user_id as string) || undefined,
    organizationId: (r.organization_id as string) || undefined,
    action: r.action as string,
    resourceType: r.resource_type as string,
    resourceId: (r.resource_id as string) || undefined,
    ipAddress: (r.ip_address as string) || undefined,
    userAgent: (r.user_agent as string) || undefined,
    // Audit 1.3 phase 5: details is encrypted at rest. Plaintext-tail
    // handling for the migration window.
    details: decryptDetails(r.details, id) || {},
    previousState: r.previous_state ? parseJson(r.previous_state) : undefined,
    newState: r.new_state ? parseJson(r.new_state) : undefined,
    success: Boolean(r.success),
    errorMessage: (r.error_message as string) || undefined,
    createdAt: new Date(r.created_at as string),
  };
}

export function rowToSecurityEvent(r: Record<string, unknown>): SecurityEvent {
  return {
    id: r.id as string,
    eventType: r.event_type as string,
    severity: r.severity as SecurityEvent['severity'],
    source: r.source as string,
    userId: (r.user_id as string) || undefined,
    ipAddress: (r.ip_address as string) || undefined,
    details: parseJson(r.details),
    resolved: Boolean(r.resolved),
    resolvedAt: r.resolved_at ? new Date(r.resolved_at as string) : undefined,
    resolvedBy: (r.resolved_by as string) || undefined,
    createdAt: new Date(r.created_at as string),
  };
}

export function rowToApiKey(r: Record<string, unknown>): ApiKey {
  return {
    id: r.id as string,
    organizationId: (r.organization_id as string | null) ?? null,
    // KS-33: tenant_id NOT NULL post-018; default-tenant fallback is a
    // belt-and-braces guard for a hand-edited row that somehow lost it.
    tenantId: (r.tenant_id as string) || 'a0000000-0000-4000-8000-000000000001',
    name: r.name as string,
    keyHash: r.key_hash as string,
    keyPrefix: r.key_prefix as string,
    scopes: parseJsonArray(r.scopes),
    rateLimit: Number(r.rate_limit),
    rateLimitWindow: Number(r.rate_limit_window),
    lastUsedAt: r.last_used_at ? new Date(r.last_used_at as string) : undefined,
    usageCount: Number(r.usage_count),
    isActive: Boolean(r.is_active),
    expiresAt: r.expires_at ? new Date(r.expires_at as string) : undefined,
    createdAt: new Date(r.created_at as string),
    // KS-869: without this the loader reads every row back with no
    // connectorId, so persisting the column would change nothing observable —
    // the write and the read have to land together.
    connectorId: (r.connector_id as string | null) ?? undefined,
  };
}

// =============================================================================
// DATABASE → MEMORY LOADER
// =============================================================================

export async function loadFromDb(): Promise<void> {
  if (!isDbAvailable()) return;
  // KS-458: boot-time cache warm is deliberately cross-tenant — there is no
  // request context, and the in-memory caches must hold EVERY tenant's rows
  // (the API surface re-filters per caller). Under fail-closed RLS the full
  // scans on audit_logs / svc_api_keys would return zero rows without the
  // platform scope, silently emptying the caches.
  return runWithPlatformScope(async () => {
    try {
      const logsResult = await query(
        'SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 10000'
      );
      memAuditLogs.length = 0;
      for (const row of logsResult.rows) memAuditLogs.push(rowToAuditLog(row));
      memAuditLogs.reverse();

      const eventsResult = await query(
        'SELECT * FROM svc_security_events ORDER BY created_at DESC LIMIT 10000'
      );
      memSecurityEvents.length = 0;
      for (const row of eventsResult.rows) memSecurityEvents.push(rowToSecurityEvent(row));
      memSecurityEvents.reverse();

      const keysResult = await query('SELECT * FROM svc_api_keys');
      memApiKeys.clear();
      for (const row of keysResult.rows) {
        const key = rowToApiKey(row);
        memApiKeys.set(key.id, key);
      }

      logger.info('Loaded persisted data from DB', {
        auditLogs: memAuditLogs.length,
        securityEvents: memSecurityEvents.length,
        apiKeys: memApiKeys.size,
      });
    } catch (err: any) {
      logger.error('Failed to load persisted data from DB', { error: err?.message });
    }
  });
}

// =============================================================================
// LOGGING
// =============================================================================

function log(level: 'info' | 'warn' | 'error', message: string, meta?: object) {
  const timestamp = new Date().toISOString();
  console.log(JSON.stringify({ timestamp, level, service: 'security', message, ...meta }));
}

// =============================================================================
// MIDDLEWARE
// =============================================================================

app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:6100', 'http://localhost:6101'],
  credentials: true,
}));
app.use(express.json());
app.use(rejectNulBytes()); // KS-471: no U+0000 may pass the boundary (raw-500 / persist class)

const requestLogger: RequestHandler = (req, res, next) => {
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
app.use(tenantGucContext());

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

const createAuditLogSchema = z.object({
  userId: z.string().optional(),
  organizationId: z.string().optional(),
  action: z.string().trim().min(1),
  resourceType: z.string().trim().min(1),
  resourceId: z.string().optional(),
  ipAddress: z.string().optional(),
  userAgent: z.string().optional(),
  details: z.record(z.unknown()).default({}),
  previousState: z.record(z.unknown()).optional(),
  newState: z.record(z.unknown()).optional(),
  success: z.boolean().default(true),
  errorMessage: z.string().optional(),
});

const createSecurityEventSchema = z.object({
  eventType: z.string().min(1),
  severity: z.enum(['low', 'medium', 'high', 'critical']),
  source: z.string().min(1),
  userId: z.string().optional(),
  ipAddress: z.string().optional(),
  details: z.record(z.unknown()).default({}),
});

const createApiKeySchema = z.object({
  // KS-33: organizationId is now optional. SYSTEM_ADMIN flows that issue
  // tenant-scoped keys without picking a specific org pass null; the
  // tenant_id-derivation logic below falls through to header / default.
  organizationId: z.string().optional(),
  // KS-33: explicit tenantId override. Callers that already know the
  // tenant (e.g. originate's POST /api/admin/api-keys, with X-Tenant-
  // Override resolved by the gateway) can skip the org→tenant lookup.
  tenantId: z.string().uuid().optional(),
  name: z.string().trim().min(1).max(100),
  scopes: z.array(z.string()).default(['read']),
  rateLimit: z.number().int().min(1).max(10000).default(1000),
  rateLimitWindow: z.number().int().min(60).max(86400).default(3600),
  expiresAt: isoDateTimeSchema.optional(), // KS-427: accept RFC 3339 offsets, normalise to UTC
  connectorId: z.string().optional(),
  // KS-577. Kam ruled 2026-08-07 that rotation SHOULD revoke the prior key:
  // shipping the additive version would hand out N new credentials, leave N
  // compromised ones live, and look like recovery. When true and a connectorId
  // is supplied, the prior active keys for that connector are retired — see
  // revokePriorConnectorKeys for the window semantics.
  rotate: z.boolean().optional().default(false),
});

// KS-698. The ECMAScript time value range is +/-8.64e15 ms; a Date outside it is
// Invalid and toISOString() THROWS. windowMs had a minimum and no maximum, so a
// single request could compute a resetAt beyond that range.
// KS-698 — extracted to `rateLimitBounds.ts` so the PUBLISHED contract can import
// the same constant the runtime enforces (the #882 gate's F2). Re-exported here
// because callers and tests already import them from this module.
export {
  isRepresentableInstant,
  MAX_RATE_LIMIT_WINDOW_MS,
  usableRateLimitEntry,
  persistableResetAt,
} from './rateLimitBounds';

// Exported as a test seam: this service has no supertest dependency, and adding
// one to assert a schema bound is the worse trade. Exporting changes no
// behaviour — the schema was already module-level.
export const checkRateLimitSchema = z.object({
  // KS-952 F10: `min(1)` with no maximum accepted a 100,000-character key and
  // stored it. This bounds one entry; `sweepExpired` bounds the map.
  key: z.string().min(1).max(RATE_LIMIT_KEY_MAX),
  limit: z.number().int().min(1).default(100),
  // KS-698 fix 1: an UPPER bound. `min` alone let one request poison a key.
  windowMs: z.number().int().min(1000).max(MAX_RATE_LIMIT_WINDOW_MS).default(60000),
});

// =============================================================================
// ROUTES
// =============================================================================

// Health check
app.get('/health', (_req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    service: 'security',
    version: '0.1.0',
    timestamp: new Date().toISOString(),
    stats: {
      auditLogs: memAuditLogs.length,
      securityEvents: memSecurityEvents.length,
      activeApiKeys: Array.from(memApiKeys.values()).filter(k => k.isActive).length,
    },
  });
});

// API info
app.get('/api', (_req: Request, res: Response) => {
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
app.use('/api', (req: Request, res: Response, next: NextFunction) => {
  if (req.path === '/keys/validate' || req.path.startsWith('/keys/validate?')) {
    return next();
  }
  return jwtAuthenticate()(req, res, next);
});

/**
 * POST /api/audit
 * Create an audit log entry
 */
app.post('/api/audit', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = createAuditLogSchema.parse(req.body);

    // KS-28: server-derives tenant_id from the verified JWT, NOT from the
    // request body. Allowing the body to set tenant_id would let any
    // authenticated caller forge audit entries against another tenant.
    // Falls back to the originate default tenant id when no JWT context is
    // present (system-actor calls e.g. cron jobs that authenticate via
    // service tokens with no tenantId claim).
    const jwtTenant = (req as any).user?.tenantId as string | undefined;
    const tenantId = jwtTenant || 'a0000000-0000-4000-8000-000000000001';

    const auditLog: AuditLog = {
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
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
    }
    next(error);
  }
});

/**
 * GET /api/audit
 * Query audit logs
 */
app.get('/api/audit', (req: Request, res: Response) => {
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
  const callerTenantId = (req as any).user?.tenantId as string | undefined;
  if (!isPlatformRole((req as any).user?.role) && !callerTenantId) {
    return res.status(403).json({
      success: false,
      error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },
    });
  }
  let filtered = callerTenantId
    ? memAuditLogs.filter(l => l.tenantId === callerTenantId)
    : [...memAuditLogs];

  if (userId) filtered = filtered.filter(l => l.userId === userId);
  if (organizationId) filtered = filtered.filter(l => l.organizationId === organizationId);
  if (action) filtered = filtered.filter(l => l.action === action);
  if (resourceType) filtered = filtered.filter(l => l.resourceType === resourceType);
  if (from) filtered = filtered.filter(l => l.createdAt >= new Date(from as string));
  if (to) filtered = filtered.filter(l => l.createdAt <= new Date(to as string));
  
  // Sort by newest first
  filtered.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
  
  const total = filtered.length;
  const results = filtered.slice(parseInt(offset as string), parseInt(offset as string) + parseInt(limit as string));
  
  res.json({
    success: true,
    data: {
      logs: results,
      total,
      limit: parseInt(limit as string),
      offset: parseInt(offset as string),
    },
  });
});

/**
 * GET /api/audit/:id
 * Get audit log by ID
 */
app.get('/api/audit/:id', (req: Request, res: Response) => {
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
  const callerTenantId = (req as any).user?.tenantId as string | undefined;
  if (!isPlatformRole((req as any).user?.role) && !callerTenantId) {
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
app.post('/api/events', requirePlatformOperator, async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = createSecurityEventSchema.parse(req.body);
    
    const event: SecurityEvent = {
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
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
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
function platformRoleGate(subject: string, req: Request, res: Response, next: NextFunction): void {
  if (!isPlatformRole((req as any).user?.role)) {
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
function requirePlatformOperator(req: Request, res: Response, next: NextFunction): void {
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
function requirePlatformOperatorForRateLimit(req: Request, res: Response, next: NextFunction): void {
  platformRoleGate('Rate-limit resets', req, res, next);
}

/**
 * GET /api/events
 * Query security events
 */
app.get('/api/events', requirePlatformOperator, (req: Request, res: Response) => {
  const { severity, resolved, from, to, limit = '50', offset = '0' } = req.query;
  
  let filtered = [...memSecurityEvents];
  
  if (severity) filtered = filtered.filter(e => e.severity === severity);
  if (resolved !== undefined) filtered = filtered.filter(e => e.resolved === (resolved === 'true'));
  if (from) filtered = filtered.filter(e => e.createdAt >= new Date(from as string));
  if (to) filtered = filtered.filter(e => e.createdAt <= new Date(to as string));
  
  filtered.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
  
  const total = filtered.length;
  const results = filtered.slice(parseInt(offset as string), parseInt(offset as string) + parseInt(limit as string));
  
  res.json({
    success: true,
    data: { events: results, total, limit: parseInt(limit as string), offset: parseInt(offset as string) },
  });
});

/**
 * PATCH /api/events/:id/resolve
 * Resolve a security event
 */
app.patch('/api/events/:id/resolve', requirePlatformOperator, async (req: Request, res: Response) => {
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
  event.resolvedBy = String((req as any).user?.userId || (req as any).user?.sub || 'unknown');

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
function requireKeyAdmin(req: Request, res: Response, next: NextFunction): void {
  const role = String((req as any).user?.role || '').toUpperCase();
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
function requireKeyAdminOrProvisioner(req: Request, res: Response, next: NextFunction): void {
  const decision = decideMint((req as any).user, (req.body ?? {}) as MintRequest);
  if (decision.allow) {
    if (decision.via === 'provisioner') {
      log('info', 'API key mint authorised by a provisioning key', {
        connectorId: (req as any).user?.connectorId,
        tenantId: (req as any).user?.tenantId,
      });
    }
    next();
    return;
  }
  if (decision.offendingScopes) {
    log('warn', 'Provisioning key attempted to mint an escalating scope', {
      offending: decision.offendingScopes,
      connectorId: (req as any).user?.connectorId,
    });
  }
  res.status(decision.status).json({ success: false, error: { code: 'FORBIDDEN', message: decision.message } });
}

app.post('/api/keys', requireKeyAdminOrProvisioner, async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = createApiKeySchema.parse(req.body);

    // Generate API key
    const keyValue = `sk_${crypto.randomBytes(32).toString('hex')}`;
    const keyHash = crypto.createHash('sha256').update(keyValue).digest('hex');
    const keyPrefix = keyValue.substring(0, 12);

    // KS-33: tenant_id resolution. Order:
    //   1. Explicit tenantId in request body (callers that already know).
    //   2. x-tenant-id header (gateway-injected for proxied calls).
    //   3. Look up via organizations.tenant_id (fast path for OAuth-app
    //      flows that pass organizationId).
    //   4. Default-tenant fallback (non-prod / single-tenancy mode).
    const DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';
    let tenantId =
      ((data as any).tenantId as string | undefined) ||
      (req.headers['x-tenant-id'] as string | undefined);

    if (!tenantId && data.organizationId && isDbAvailable()) {
      try {
        // KS-458: admin-authorised cross-tenant resolution. The caller may be
        // a platform admin creating a key for an org in ANOTHER tenant, and
        // organizations is fail-closed — the request's own tenant GUC would
        // hide the target org's row. Platform scope covers this single lookup.
        const r = await runWithPlatformScope(() => query(
          'SELECT tenant_id::text AS tenant_id FROM organizations WHERE id = $1::uuid LIMIT 1',
          [data.organizationId],
        ));
        if (r.rows.length > 0 && r.rows[0].tenant_id) {
          tenantId = r.rows[0].tenant_id as string;
        }
      } catch {
        // organizations table missing or organizationId not a UUID — fall through
      }
    }
    if (!tenantId) {
      // KS-742: a tenant-scoped caller's OWN tenant is the right default here.
      // The platform-wide DEFAULT_TENANT_ID silently placed a tenant-B admin's
      // key in tenant A — the same cross-tenant landing this ticket is about,
      // arrived at by omission rather than by a supplied value.
      tenantId = (!isPlatformRole((req as any).user?.role) && (req as any).user?.tenantId)
        ? ((req as any).user.tenantId as string)
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
    const mintDecision = decideTenantAccess((req as any).user, tenantId);
    if (!mintDecision.allow) {
      log('warn', 'Cross-tenant API key mint refused', {
        targetTenantId: tenantId,
        callerTenantId: (req as any).user?.tenantId,
        callerRole: (req as any).user?.role,
        reason: mintDecision.reason,
      });
      return res.status(mintDecision.status ?? 403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'API keys may only be minted in your own tenant' },
      });
    }

    const apiKey: ApiKey = {
      // Internal record ID — not a secret, but using crypto.randomUUID keeps
      // us consistent with the no-Math.random rule across the codebase.
      id: `key_${crypto.randomUUID()}`,
      organizationId: data.organizationId ?? null,
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

    await dbSaveApiKey(apiKey);

    // KS-577. MINT FIRST, THEN REVOKE — deliberately this order. A failed
    // revoke leaves the old key live, which is the status quo being fixed; a
    // failed mint AFTER a revoke would leave the connector with NO working
    // credential. The worse failure is the outage, so the irreversible step
    // goes second and reports itself.
    let priorKeysRevoked: number | null = null;
    if (data.rotate && data.connectorId) {
      priorKeysRevoked = await revokePriorConnectorKeys(data.connectorId, tenantId, apiKey.id);
    }
    
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
        // KS-577: reported, not assumed. `null` means the revoke was attempted
        // and FAILED, so the prior credential is still valid — a caller that
        // ignores this is back to the bug.
        ...(data.rotate && data.connectorId ? { priorKeysRevoked } : {}),
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
    }
    next(error);
  }
});

/**
 * GET /api/keys
 * List API keys for organization
 */
app.get('/api/keys', requireKeyAdmin, (req: Request, res: Response) => {
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
  const caller = (req as any).user as { role?: string; tenantId?: string } | undefined;
  const callerIsPlatform = isPlatformRole(caller?.role);
  if (!callerIsPlatform && !caller?.tenantId) {
    log('warn', 'API key list refused: caller has no tenant', { callerRole: caller?.role });
    return res.status(403).json({
      success: false,
      error: { code: 'FORBIDDEN', message: 'API key management requires a tenant context' },
    });
  }

  const keys = Array.from(memApiKeys.values())
    .filter(k => k.organizationId === organizationId)
    .filter(k => callerIsPlatform || k.tenantId === caller!.tenantId)
    .map(k => ({
      id: k.id,
      name: k.name,
      prefix: k.keyPrefix,
      scopes: k.scopes,
      lastUsedAt: k.lastUsedAt,
      usageCount: k.usageCount,
      isActive: k.isActive,
      createdAt: k.createdAt,
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
app.delete('/api/keys/:id', requireKeyAdmin, async (req: Request, res: Response) => {
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
  const decision = decideKeyRevoke((req as any).user, {
    id: apiKey.id,
    tenantId: apiKey.tenantId,
    organizationId: apiKey.organizationId,
  });
  if (!decision.allow) {
    log('warn', 'Cross-tenant API key revoke refused', {
      keyId: apiKey.id,
      keyTenantId: apiKey.tenantId,
      keyOrganizationId: apiKey.organizationId,
      callerTenantId: (req as any).user?.tenantId,
      callerOrganizationId: (req as any).user?.organizationId,
      callerRole: (req as any).user?.role,
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
  await dbSaveApiKey(apiKey);
  
  log('info', 'API key revoked', { keyId: apiKey.id });
  
  res.json({
    success: true,
    message: 'API key revoked',
  });
});

/**
 * POST /api/keys/validate
 * Validate an API key
 */
app.post('/api/keys/validate', async (req: Request, res: Response) => {
  // KS-444: schema-validate instead of truthy-check — a wrong-typed `key`
  // (object/number) previously reached crypto.createHash().update() and threw.
  const parsedBody = validateKeySchema.safeParse(req.body);
  if (!parsedBody.success) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'API key required', details: parsedBody.error.errors } });
  }
  const { key } = parsedBody.data;

  const keyHash = crypto.createHash('sha256').update(key).digest('hex');

  let apiKey = Array.from(memApiKeys.values()).find(k => k.keyHash === keyHash);

  // KS-39 #5: in-memory map is populated only at boot from svc_api_keys.
  // Keys minted by originate AFTER security started are invisible until
  // the next restart, so any test or runtime caller minting a key + using
  // it within the same uptime window saw "invalid api key" even though
  // the row was correctly in svc_api_keys. Fall through to a fresh DB
  // lookup on cache-miss before we declare the key invalid, and warm the
  // memory cache for next time.
  if (!apiKey) {
    try {
      // KS-458: this route is deliberately unauthenticated (the gateway calls
      // it BEFORE any session exists — see the KS-39 #5 auth carve-out above),
      // so there is no tenant context to set the RLS GUC from. Under the
      // fail-closed tenant_isolation policy a direct SELECT on svc_api_keys
      // would return zero rows and break every sk_* API-key auth. The
      // migration-039 SECURITY DEFINER function is the reviewed pre-session
      // carve-out: same row shape (SETOF svc_api_keys), lookup by hash only.
      const dbResult = await query('SELECT * FROM security_find_api_key_by_hash($1)', [keyHash]);
      if (dbResult.rows.length > 0) {
        apiKey = rowToApiKey(dbResult.rows[0]);
        memApiKeys.set(apiKey.id, apiKey);
      }
    } catch (err: any) {
      logger.warn('DB fallback for api-key validation failed', { error: err?.message });
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
  await dbSaveApiKey(apiKey);
  
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
app.post('/api/rate-limit/check', (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = checkRateLimitSchema.parse(req.body);

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
    const scope = principalScope((req as any).user);
    if (scope === null) {
      // KS-743's rule applied here: a missing claim is a refusal, not a wildcard.
      // Defaulting to a shared namespace would put unrelated callers in one
      // bucket, which is the same fail-open this change exists to remove.
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },
      });
    }
    const bucketKey = scopedRateLimitKey(scope, data.key);

    const now = Date.now();
    const stored = rateLimits.get(bucketKey);

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
    const entry = usableRateLimitEntry(stored);
    
    if (!entry || now > entry.resetAt) {
      // KS-698 fix 2: compute BEFORE the write and refuse to persist a value we
      // cannot render. The original order wrote the entry and THEN threw while
      // formatting the response, so the bad state outlived the failed request.
      // Unreachable from this route now that the schema bounds windowMs — kept
      // because it guards the WRITE rather than the INPUT, and those can drift.
      const resetAt = persistableResetAt(now, data.windowMs);
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
      sweepExpired(rateLimits, now);
      rateLimits.set(bucketKey, { count: 1, resetAt });
      
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
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
    }
    next(error);
  }
});

/**
 * POST /api/rate-limit/reset
 * Reset rate limit for a key
 */
app.post('/api/rate-limit/reset', requirePlatformOperatorForRateLimit, (req: Request, res: Response) => {
  // KS-444: schema-validate instead of truthy-check — a wrong-typed `key`
  // (object/number) was previously accepted and answered 200 "Rate limit reset".
  const parsedBody = resetRateLimitSchema.safeParse(req.body);
  if (!parsedBody.success) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Key required', details: parsedBody.error.errors } });
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
  const scope = explicitScope(parsedBody.data, (req as any).user);
  if (scope === null) {
    return res.status(403).json({
      success: false,
      error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },
    });
  }
  rateLimits.delete(scopedRateLimitKey(scope, parsedBody.data.key));
  
  res.json({
    success: true,
    message: 'Rate limit reset',
  });
});

// =============================================================================
// ERROR HANDLING
// =============================================================================

app.use((_req: Request, res: Response) => {
  res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Not Found' } });
});

// KS-111: route errors through the shared AppError-aware handler (maps
// AppError.statusCode + Zod -> 4xx; emits the canonical {success,error} shape).
app.use(errorHandler);

// =============================================================================
// START SERVER
// =============================================================================

// Audit 1.3 phase 5: PII keyring for audit_logs.details encryption.
if (process.env.PII_ENCRYPTION_KEY) {
  try {
    initPiiCrypto();
    log('info', 'PII encryption keyring initialised');
  } catch (err: any) {
    log('warn', 'PII encryption init failed (audit_logs.details will store plaintext)', { error: err?.message });
  }
} else if (process.env.NODE_ENV === 'production') {
  log('error', 'FATAL: PII_ENCRYPTION_KEY missing in production — refusing to start');
  process.exit(1);
} else {
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
async function runDbBootTasks(): Promise<void> {
  await loadFromDb();
  // Audit 1.3 phase 5: widen audit_logs.details from JSONB to TEXT so
  // AES-GCM ciphertext fits. Idempotent — only runs if currently jsonb.
  try {
    await query(`
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
  } catch (err: any) {
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
  initDb(runDbBootTasks).then((connected) => {
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

export default app;
