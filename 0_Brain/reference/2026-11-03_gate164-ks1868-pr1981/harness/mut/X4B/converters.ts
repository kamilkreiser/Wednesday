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

export interface AuditLog {
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

export interface SecurityEvent {
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

export interface ApiKey {
  id: string;
  // KS-33: organization_id is now NULL-able on the API-key row. Originate's
  // admin endpoint can issue tenant-scoped keys without an explicit org
  // (e.g. SYSTEM_ADMIN flows). Code paths that filter by org just won't
  // match null-org keys.
  // The table is deliberately not named here. This file also reads is_active
  // (below), and the KS-764 drift sweep in packages/shared reports any file
  // holding BOTH that column and the table name unless it is a listed revoke
  // call site. This mapper neither decides nor writes, so it belongs in
  // neither of that guard's lists, and naming the table would re-break it for
  // no added information. The guard stays live for this file: add a real query
  // against the table here and it fires again.
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

/**
 * Map a DB row to an AuditLog domain object.
 * `decryptDetails` is injected: the production one needs the shared keyring (index.ts binds it), and this
 * module must stay loadable without it - env validation, a DB and a booted server are exactly what it exists
 * to be tested without.
 */
export function rowToAuditLog(
  r: Record<string, unknown>,
  decryptDetails: (stored: unknown, auditId: string) => Record<string, unknown> | null,
): AuditLog {
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
    // KS-1639: a text value is active only when it is a text form of true; 'f' / 'false' (and anything unrecognised) read inactive.
    isActive: typeof r.is_active === 'string'
      ? /^(t|true)$/i.test(r.is_active.trim())
      : Boolean(r.is_active),
    expiresAt: r.expires_at ? new Date(r.expires_at as string) : undefined,
    createdAt: new Date(r.created_at as string),
    // KS-869: without this the loader reads every row back with no
    // connectorId, so persisting the column would change nothing observable —
    // the write and the read have to land together.
    connectorId: (r.connector_id as string | null) ?? undefined,
  };
}
