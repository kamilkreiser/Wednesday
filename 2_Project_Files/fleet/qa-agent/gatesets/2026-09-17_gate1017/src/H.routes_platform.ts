/**
 * Platform / multi-tenancy route handlers — extracted from the API gateway monolith.
 *
 * Usage in index.ts:
 *   import { createPlatformRoutes } from './routes/platform';
 *   app.use(createPlatformRoutes({
 *     authenticateToken,
 *     tenantProvisioningUrl: TENANT_PROVISIONING_URL,
 *     setTenantKey,
 *     getTenantKey,
 *     removeTenantKey,
 *   }));
 */

import { Router, Request, Response, NextFunction, RequestHandler } from 'express';
import { runWithPlatformScope } from '@secuura/shared';
// KS-480 §4 amendment: provisioning may be authorised by a scoped connector key.
import { hasScope } from '@secuura/shared/security/scopes';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface UserPayload {
  userId: string;
  email: string;
  role: string;
  organizationId?: string;
  verificationLevel: string;
  authMethod?: string;
  mfaEnabled?: boolean;
  tenantId?: string;
  tenantSlug?: string;
}

declare module 'express-serve-static-core' {
  interface Request {
    user?: UserPayload;
    requestId?: string;
  }
}

export interface PlatformRouteDeps {
  /** Middleware factory that validates JWT tokens */
  authenticateToken: (required?: boolean) => RequestHandler;
  /** Base URL for the tenant-provisioning micro-service */
  tenantProvisioningUrl: string;
  /** Base URL for the security micro-service (KS-480 register-connector key mint) */
  securityServiceUrl?: string;
  /** Store an encryption key for a tenant in the current session */
  setTenantKey: (tenantId: string, key: string) => void;
  /** Retrieve a previously stored tenant key */
  getTenantKey: (tenantId: string) => string | undefined;
  /** Remove a tenant key from the session store */
  removeTenantKey: (tenantId: string) => void;
  /** Database query function (BACKLOG H1: needed to merge audit_logs into the platform audit view) */
  query: (sql: string, params?: unknown[]) => Promise<{ rows: any[] }>;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN'];

function requireSuperAdmin(req: Request, res: Response, next: NextFunction): void {
  const user = req.user;
  if (!user || !SUPER_ROLES.includes(user.role)) {
    res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Super-admin access required' } });
    return;
  }
  next();
}

/**
 * KS-480 §4 amendment (2026-07-30) — authorise Organisation provisioning by
 * EITHER a platform-admin bearer OR a connector key carrying the
 * provisioning-only `organizations:register` scope.
 *
 * Why: the original §4 required a platform-admin bearer, which cannot scale to
 * S-side signup (a human in the loop per Organisation). A provisioning-scoped
 * key lets S self-serve org onboarding without holding a credential whose blast
 * radius is the whole tenant — `organizations:register` grants provisioning and
 * nothing else (no document/certification/anchor access).
 *
 * Records which kind of principal authorised the call on `req.provisionerKind`
 * so the handler can apply the connector-only guardrails (own-tenant pinning,
 * no scope widening, no rotation). Admin callers keep the pre-amendment
 * behaviour unchanged.
 */
export function requireOrgProvisioner(req: Request, res: Response, next: NextFunction): void {
  const user = req.user;
  if (!user) {
    res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    return;
  }
  if (SUPER_ROLES.includes(user.role)) {
    (req as { provisionerKind?: string }).provisionerKind = 'admin';
    next();
    return;
  }
  if (user.role === 'connector' && hasScope((user as { scopes?: string[] }).scopes ?? [], 'organizations:register')) {
    (req as { provisionerKind?: string }).provisionerKind = 'connector';
    next();
    return;
  }
  res.status(403).json({
    success: false,
    error: {
      code: 'FORBIDDEN',
      message: 'Organisation provisioning requires a platform-admin role or the organizations:register scope',
    },
  });
}

// ---------------------------------------------------------------------------
// Upstream fetch with a hard deadline
// ---------------------------------------------------------------------------
//
// KS-5 (F-PLATFORM-01): every call from here to the tenant-provisioning
// service used a bare `fetch` with no AbortController. When that service was
// slow or its container was mid-restart, the gateway worker hung on the OS
// TCP timeout (75–300s on Linux containers) before the surrounding
// `try/catch` ever ran — that's the "/api/platform/tenants and
// /api/platform/audit-log hang 20+s" symptom. Wrapping upstream calls in a
// deadline turns that into a fast 504, and frees the worker.
const UPSTREAM_TIMEOUT_MS = parseInt(process.env.PLATFORM_UPSTREAM_TIMEOUT_MS || '8000', 10);

class UpstreamTimeoutError extends Error {
  constructor(url: string, ms: number) {
    super(`Upstream timed out after ${ms}ms: ${url}`);
    this.name = 'UpstreamTimeoutError';
  }
}

// NB: return type is intentionally inferred (the global Fetch `Response`).
// Annotating it as `Response` would resolve to express's `Response` — that
// name is imported into this module — so we let TS infer from `fetch`.
async function fetchWithTimeout(
  url: string,
  init?: RequestInit,
  timeoutMs: number = UPSTREAM_TIMEOUT_MS,
) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...init, signal: controller.signal });
  } catch (err) {
    if (err instanceof Error && err.name === 'AbortError') {
      throw new UpstreamTimeoutError(url, timeoutMs);
    }
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

/** Map an upstream failure to 504 (timeout) vs 502 (refused / DNS / other). */
function sendUpstreamError(res: Response, err: unknown): void {
  if (err instanceof UpstreamTimeoutError) {
    res.status(504).json({
      success: false,
      error: { code: 'GATEWAY_TIMEOUT', message: 'Tenant provisioning service did not respond in time' },
    });
    return;
  }
  res.status(502).json({
    success: false,
    error: { code: 'BAD_GATEWAY', message: 'Tenant provisioning service unavailable' },
  });
}

// ---------------------------------------------------------------------------
// Router factory
// ---------------------------------------------------------------------------

export function createPlatformRoutes(deps: PlatformRouteDeps): Router {
  const {
    authenticateToken,
    tenantProvisioningUrl,
    securityServiceUrl = 'http://security:4008',
    setTenantKey,
    getTenantKey,
    removeTenantKey,
    query,
  } = deps;

  const router = Router();

  // -----------------------------------------------------------------------
  // Tenant CRUD
  // -----------------------------------------------------------------------

  // BACKLOG H13: tenant-provisioning's routes require a Bearer token.
  // Earlier proxies skipped forwarding Authorization, so DELETE / PATCH /
  // GET-by-id calls all failed at the upstream auth check with
  // "No token provided". The gateway then surfaced a misleading
  // "service unavailable" instead of the actual 401, which is why the
  // test agent saw "DELETE doesn't actually delete" — the request
  // never reached the DELETE handler. Forward Authorization on every
  // proxy call to tenant-provisioning.
  //
  // BUG-PLATFORM-AUTH-001 fix (2026-05-01): prefer the rawAuthorization
  // captured at request entry (see api-gateway/src/index.ts early-capture
  // middleware) over `req.headers.authorization`, which may be cleared
  // by intermediate middleware before this handler runs. Falls back to
  // the live header for routes registered before the capture middleware.
  function authHeaders(req: Request, contentType?: string): Record<string, string> {
    const h: Record<string, string> = {};
    if (contentType) h['Content-Type'] = contentType;
    const auth = (req as any).rawAuthorization || req.headers.authorization;
    if (auth) h['Authorization'] = auth;
    return h;
  }

  router.get(
    '/api/platform/tenants',
    authenticateToken(),
    requireSuperAdmin,
    async (req: Request, res: Response) => {
      try {
        const r = await fetchWithTimeout(`${tenantProvisioningUrl}/api/tenants`, {
          headers: authHeaders(req),
        });
        const data = await r.json();
        res.json(data);
      } catch (err: unknown) {
        sendUpstreamError(res, err);
      }
    },
  );

  router.post(
    '/api/platform/tenants',
    authenticateToken(),
    requireSuperAdmin,
    async (req: Request, res: Response) => {
      try {
        const r = await fetchWithTimeout(`${tenantProvisioningUrl}/api/tenants`, {
          method: 'POST',
          headers: authHeaders(req, 'application/json'),
          body: JSON.stringify(req.body),
        });
        const upstream = await r.json() as Record<string, unknown>;

        // Notify originate to refresh tenant configs so the new tenant is immediately available
        if (r.ok) {
          const originateUrl = process.env.ORIGINATE_SERVICE_URL || 'http://originate:4000';
          fetchWithTimeout(`${originateUrl}/api/admin/refresh-tenants`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': req.headers.authorization || '' },
          }).catch(() => { /* best-effort refresh */ });
        }

        // KS-39 #6: tenant-provisioning returns `{success, tenant: {...}, keyFile}`
        // — every other write endpoint on the platform uses the
        // `{success, data: {...}}` envelope. Add `data` alongside `tenant`
        // (keep `tenant` for backward compatibility with any caller already
        // reading that shape) so callers using either convention work.
        const tenantObj = upstream && typeof upstream === 'object' && 'tenant' in upstream
          ? (upstream as { tenant?: Record<string, unknown> }).tenant
          : undefined;
        const responseBody = tenantObj
          ? { ...upstream, data: tenantObj }
          : upstream;

        res.status(r.status).json(responseBody);
      } catch (err: unknown) {
        sendUpstreamError(res, err);
      }
    },
  );

  // KS-515/KS-497 follow-up: re-encode the decoded :id when building the
  // upstream URL — Express hands over the DECODED segment, so a literal
  // '#' ('%23' on the wire) became a fragment in fetch(), truncating the
  // path to the LIST route and skipping the upstream UUID guard entirely.
  router.get(
    '/api/platform/tenants/:id',
    authenticateToken(),
    requireSuperAdmin,
    async (req: Request, res: Response) => {
      try {
        const r = await fetchWithTimeout(`${tenantProvisioningUrl}/api/tenants/${encodeURIComponent(req.params.id)}`, {
          headers: authHeaders(req),
        });
        const data = await r.json();
        res.status(r.status).json(data);
      } catch (err: unknown) {
        sendUpstreamError(res, err);
      }
    },
  );

  router.patch(
    '/api/platform/tenants/:id',
    authenticateToken(),
    requireSuperAdmin,
    async (req: Request, res: Response) => {
      try {
        const r = await fetchWithTimeout(`${tenantProvisioningUrl}/api/tenants/${encodeURIComponent(req.params.id)}`, {
          method: 'PATCH',
          headers: authHeaders(req, 'application/json'),
          body: JSON.stringify(req.body),
        });
        const data = await r.json();
        res.status(r.status).json(data);
      } catch (err: unknown) {
        sendUpstreamError(res, err);
      }
    },
  );

  router.patch(
    '/api/platform/tenants/:id/status',
    authenticateToken(),
    requireSuperAdmin,
    async (req: Request, res: Response) => {
      try {
        const r = await fetchWithTimeout(`${tenantProvisioningUrl}/api/tenants/${encodeURIComponent(req.params.id)}/status`, {
          method: 'PATCH',
          headers: authHeaders(req, 'application/json'),
          body: JSON.stringify(req.body),
        });
        const data = await r.json();
        res.status(r.status).json(data);
      } catch (err: unknown) {
        sendUpstreamError(res, err);
      }
    },
  );

  router.delete(
    '/api/platform/tenants/:id',
    authenticateToken(),
    requireSuperAdmin,
    async (req: Request, res: Response) => {
      try {
        const r = await fetchWithTimeout(`${tenantProvisioningUrl}/api/tenants/${encodeURIComponent(req.params.id)}`, {
          method: 'DELETE',
          headers: authHeaders(req, 'application/json'),
          body: JSON.stringify(req.body),
        });
        const data = await r.json();
        res.status(r.status).json(data);
      } catch (err: unknown) {
        sendUpstreamError(res, err);
      }
    },
  );

  // -----------------------------------------------------------------------
  // Audit log
  // -----------------------------------------------------------------------

  router.get(
    '/api/platform/audit-log',
    authenticateToken(),
    requireSuperAdmin,
    async (req: Request, res: Response) => {
      // BACKLOG H1: the platform audit page used to read only from
      // tenant-provisioning's `platform_audit_log` table — which contained
      // only tenant_created entries with null actor_id. Business events
      // (login / docs / verify / revoke) are recorded in the `audit_logs`
      // table by the gateway audit middleware. Merge both sources so the
      // existing UI sees every event without needing dual-writes.
      const limit = Math.min(parseInt(req.query.limit as string) || 50, 500);
      // KS-5: the merge below overfetches `limit + offset` rows from BOTH
      // sources so it can paginate after sorting. Unbounded `offset` made
      // that overfetch (and the in-memory sort + per-row JSON.parse) the
      // latency floor on a growing audit_logs table. Clamp it — deep audit
      // paging past this point clamps rather than crawling.
      const MAX_AUDIT_OFFSET = parseInt(process.env.PLATFORM_AUDIT_MAX_OFFSET || '5000', 10);
      const offset = Math.min(parseInt(req.query.offset as string) || 0, MAX_AUDIT_OFFSET);
      const overfetch = limit + offset;
      let platformEntries: any[] = [];
      let platformTotal = 0;
      try {
        const qs = new URLSearchParams({
          limit: String(overfetch),  // overfetch so the merge can paginate cleanly
          offset: '0',
        }).toString();
        const r = await fetchWithTimeout(`${tenantProvisioningUrl}/api/audit-log?${qs}`, {
          headers: authHeaders(req),
        });
        const data = await r.json() as { entries?: any[]; total?: number };
        platformEntries = Array.isArray(data?.entries) ? data.entries : [];
        platformTotal = typeof data?.total === 'number' ? data.total : platformEntries.length;
      } catch {
        // Tenant-provisioning down or slow — degrade gracefully and serve only audit_logs.
      }

      // Pull from audit_logs and reshape into the platform_audit_log envelope
      // the UI already understands. We can't surface actor_email cheaply
      // without a JOIN to users; leave it undefined for now.
      let appEntries: any[] = [];
      let appTotal = 0;
      try {
        // KS-458: super-admin platform audit view — deliberate cross-tenant scope.
        const totalResult = await runWithPlatformScope(() => query('SELECT COUNT(*)::int AS total FROM audit_logs', []));
        appTotal = Number(totalResult?.rows?.[0]?.total) || 0;
        const result = await runWithPlatformScope(() => query(
          `SELECT id, user_id, action, resource_type, resource_id,
                  details, ip_address, success, created_at
           FROM audit_logs
           ORDER BY created_at DESC
           LIMIT $1`,
          [overfetch],
        ));
        const rows = result.rows;
        appEntries = rows.map((r) => {
          // details is TEXT in audit_logs (encrypted-able). The middleware
          // writes plaintext JSON; if it's encrypted we'd need the security
          // service to decrypt — out of scope here. Try-parse and fall back
          // to a shallow object so the UI gets something useful.
          let detailsObj: Record<string, unknown> = {};
          if (typeof r.details === 'string' && r.details.length > 0) {
            try { detailsObj = JSON.parse(r.details); } catch { detailsObj = { raw: '<encrypted or unparseable>' }; }
          } else if (r.details && typeof r.details === 'object') {
            detailsObj = r.details;
          }
          if (typeof r.success === 'boolean') {
            detailsObj.success = r.success;
          }
          // H29: surface the attemptedEmail captured by the audit
          // middleware as actor_email for entries where user_id is null
          // (login events don't have a user_id at the time the row is
          // written — see middleware comments).
          const attemptedEmail =
            typeof (detailsObj as Record<string, unknown>).attemptedEmail === 'string'
              ? ((detailsObj as Record<string, unknown>).attemptedEmail as string)
              : undefined;
          return {
            id: String(r.id),
            actor_id: r.user_id || undefined,
            actor_email: r.user_id ? undefined : attemptedEmail,
            action: r.action,
            target_type: r.resource_type || undefined,
            target_id: r.resource_id || undefined,
            details: detailsObj,
            ip_address: r.ip_address || undefined,
            created_at: r.created_at instanceof Date ? r.created_at.toISOString() : String(r.created_at),
          };
        });
      } catch {
        // audit_logs query failed — degrade gracefully and serve only platform.
      }

      const merged = [...platformEntries, ...appEntries].sort((a, b) =>
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
      );
      const paginated = merged.slice(offset, offset + limit);
      res.json({ entries: paginated, total: platformTotal + appTotal });
    },
  );

  // -----------------------------------------------------------------------
  // KS-480 §4 — Organisation registration + connector-key provisioning.
  // One platform-admin-authorised handshake per SSD Organisation: upserts the
  // organizations row (idempotent on S's OrganisationGuid, stored in
  // metadata.externalRef — no new columns), binds it to a tenant, and mints
  // the per-org sk_ connector key via the security service (folding in the
  // unminted KS-320 S partner key). The plaintext key is returned exactly
  // once; re-registration returns the existing org and NO key (rotation is
  // the explicit `rotate: true` flag, §5).
  // -----------------------------------------------------------------------

  // §8 scope set as signed off 2026-07-29: +certifications:write (Stuart ①),
  // −users:read (Stuart ③ — on-behalf-of resolution is K-side, §6).
  // KS-843 (2026-09-06): +subjects:erase. Kam ruled 2026-09-03 that the GDPR
  // erasure route gets its own scope, minted for S's key at registration.
  // Adding it here is ADDITIVE and non-breaking — a key minted or rotated from
  // now on carries it; keys issued before this change are untouched and keep
  // working, because no route requires the scope yet. Enforcement is a
  // separate, sequenced cutover (KS-843 second half).
  const S_CONNECTOR_SCOPES = [
    'documents:write', 'documents:read', 'documents:share', 'documents:revoke',
    'documents:transfer-custody', 'certifications:write', 'anchors:read', 'anchors:write',
    'subjects:erase',
  ];
  const DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';

  router.post(
    '/api/platform/organizations/register-connector',
    authenticateToken(),
    requireOrgProvisioner,
    async (req: Request, res: Response) => {
      const body = (req.body || {}) as Record<string, unknown>;
      // KS-480 §4 amendment: a connector-authorised registration is provisioning
      // ONLY — the three guardrails below keep a leaked provisioning key from
      // becoming a tenant-wide or credential-replacement capability.
      const byConnector = (req as { provisionerKind?: string }).provisionerKind === 'connector';
      const callerTenantId = (req.user as { tenantId?: string } | undefined)?.tenantId;
      const organizationName = typeof body.organizationName === 'string' ? body.organizationName.trim() : '';
      const externalRef = typeof body.externalRef === 'string' ? body.externalRef.trim() : '';
      // KS-480 sweep follow-up: an EMPTY tenantSlug is a caller error (the
      // spec says min 1), not "use the default" — silently defaulting hid a
      // mis-mapped field. Absent/undefined still means the default tenant.
      if (body.tenantSlug !== undefined && (typeof body.tenantSlug !== 'string' || body.tenantSlug.trim() === '')) {
        res.status(400).json({ success: false, error: { code: 'VALIDATION_ERROR', message: 'tenantSlug, when provided, must be a non-empty string' } });
        return;
      }
      const tenantSlug = typeof body.tenantSlug === 'string' ? body.tenantSlug.trim() : '';
      const rotate = body.rotate === true;

      // GUARDRAIL 1 — rotation stays platform-admin-only (§5). Re-minting an
      // existing org's key is credential REPLACEMENT, not provisioning: it
      // invalidates nothing by itself but hands out a fresh live credential for
      // an org that already has one, so it must not be self-service.
      if (byConnector && rotate) {
        res.status(403).json({
          success: false,
          error: { code: 'FORBIDDEN', message: 'Key rotation requires a platform-admin role (organizations:register provisions new Organisations only)' },
        });
        return;
      }
      // GUARDRAIL 2 — a provisioning key may not widen the minted scope set.
      // Refused explicitly rather than silently ignored: quietly dropping a
      // security-relevant field hides a caller (or attacker) error.
      if (byConnector && body.scopes !== undefined) {
        res.status(403).json({
          success: false,
          error: { code: 'FORBIDDEN', message: 'A provisioning key may not override the minted scope set; omit `scopes` to receive the agreed contract set' },
        });
        return;
      }
      const scopes = Array.isArray(body.scopes) && body.scopes.every(s => typeof s === 'string') && body.scopes.length > 0
        ? (body.scopes as string[])
        : S_CONNECTOR_SCOPES;
      // KS-480 §4 (Stuart, 2026-07-30): `externalRef` (S's Org GUID) is the
      // immutable, REQUIRED identity; `organizationName` is a mutable display
      // label, so nothing structural may depend on it. It is therefore OPTIONAL
      // — S has real Organisations with a null name that could not register at
      // all while it was required. An absent name yields a deterministic,
      // obviously-derived placeholder (below) that a later registration
      // REPLACES, so no fabricated name is ever permanent.
      if (organizationName.length > 255 || !externalRef || externalRef.length > 128) {
        res.status(400).json({ success: false, error: { code: 'VALIDATION_ERROR', message: 'externalRef (≤128) is required; organizationName, when supplied, must be ≤255 chars' } });
        return;
      }
      const hasName = organizationName.length > 0;
      // Placeholder is visibly derived from the GUID — never an invented
      // human-looking name (Stuart: "an honestly-empty name is better than a
      // permanent fabrication"). `organizations.name` is NOT NULL, so a value
      // is required; `metadata.nameProvided` records whether it is real.
      const effectiveName = hasName ? organizationName : `Organisation ${externalRef}`;

      try {
        // Tenant binding: explicit slug → resolve via tenant-provisioning
        // (the platform DB owns tenants); absent → the canonical default
        // tenant, per §4, until real multi-tenant onboarding exists.
        let tenantId = DEFAULT_TENANT_ID;
        let resolvedSlug = 'default';
        if (tenantSlug) {
          const tRes = await fetchWithTimeout(`${tenantProvisioningUrl}/api/tenants`, { headers: authHeaders(req) });
          if (!tRes.ok) {
            res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Tenant lookup unavailable' } });
            return;
          }
          const tBody = await tRes.json() as { tenants?: Array<{ id: string; slug: string }>; data?: Array<{ id: string; slug: string }> };
          const tenants = tBody.tenants || tBody.data || [];
          const match = tenants.find(t => t.slug === tenantSlug);
          if (!match) {
            res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: `Tenant slug "${tenantSlug}" not found` } });
            return;
          }
          tenantId = match.id;
          resolvedSlug = tenantSlug;
        }

        // GUARDRAIL 3 — a provisioning key is pinned to its OWN tenant. An
        // admin may provision into any tenant (platform scope); a connector may
        // not, so a resolved slug that isn't the caller key's tenant is refused
        // rather than honoured. Absent slug for a connector = its own tenant,
        // not the platform default.
        if (byConnector) {
          if (!callerTenantId) {
            res.status(403).json({
              success: false,
              error: { code: 'FORBIDDEN', message: 'Provisioning key carries no tenant binding' },
            });
            return;
          }
          if (tenantSlug && tenantId !== callerTenantId) {
            res.status(403).json({
              success: false,
              error: { code: 'FORBIDDEN', message: 'A provisioning key may only register Organisations in its own tenant' },
            });
            return;
          }
          tenantId = callerTenantId;
        }

        // Idempotency: the org row is keyed on S's OrganisationGuid.
        // Cross-tenant read — the registering admin is platform-scoped and
        // the target org may sit in any tenant (KS-458 fail-closed RLS).
        const existing = await runWithPlatformScope(() => query(
          `SELECT id, tenant_id::text AS tenant_id, slug, name FROM organizations WHERE metadata->>'externalRef' = $1 LIMIT 1`,
          [externalRef],
        ));

        let organizationId: string;
        let orgSlug: string;
        if (existing.rows.length > 0) {
          // GUARDRAIL 4 — the idempotency lookup runs under PLATFORM scope, so
          // it can see an org in ANY tenant. Without this check a provisioning
          // key could name another tenant's externalRef and read back that
          // org's ids (and, with rotate, obtain a live credential for it). A
          // cross-tenant hit is reported as NOT_FOUND, not FORBIDDEN, so the
          // response cannot be used to probe which externalRefs exist elsewhere.
          const existingTenant = existing.rows[0].tenant_id as string | null;
          if (byConnector && existingTenant && existingTenant !== callerTenantId) {
            res.status(404).json({
              success: false,
              error: { code: 'NOT_FOUND', message: 'No Organisation with that externalRef in this tenant' },
            });
            return;
          }
          organizationId = existing.rows[0].id as string;
          orgSlug = existing.rows[0].slug as string;
          tenantId = (existing.rows[0].tenant_id as string) || tenantId;

          // KS-480 §4 (Stuart ask 2, 2026-07-30): refresh the display NAME when
          // the caller supplies one that differs. Org names are mutable in S,
          // so K's captured copy went stale the moment anyone renamed —
          // permanently and silently, for every org. S's registration sweep runs
          // periodically, so renames now propagate on the next pass.
          //
          // The SLUG is deliberately NOT refreshed: it is an identifier that may
          // already be referenced elsewhere, and rotating it on a rename would
          // break those references. Display name mutable, identifier frozen.
          let nameRefreshed = false;
          if (hasName && organizationName !== (existing.rows[0].name as string | null)) {
            await runWithPlatformScope(() => query(
              `UPDATE organizations
                  SET name = $1,
                      metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object('nameProvided', true),
                      updated_at = NOW()
                WHERE id = $2::uuid`,
              [organizationName, organizationId],
            ));
            nameRefreshed = true;
          }

          if (!rotate) {
            // §4: re-registration returns the existing org and NO key.
            res.json({
              success: true,
              data: { organizationId, tenantId, tenantSlug: resolvedSlug, alreadyRegistered: true, nameRefreshed },
            });
            return;
          }
        } else {
          // Slug source: the name when there is one, else the externalRef —
          // which is unique by construction, so the fallback is deterministic
          // and collision-free (the retry below stays as a cheap safety net,
          // since externalRef is only contractually a GUID).
          const slugSource = hasName ? organizationName : `org-${externalRef}`;
          const slugBase = slugSource.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80) || 'org';
          const crypto = require('crypto') as typeof import('crypto');
          const insert = async (slug: string) => runWithPlatformScope(() => query(
            `INSERT INTO organizations (name, slug, type, status, verified, tenant_id, metadata)
             VALUES ($1, $2, 'business', 'active', false, $3::uuid, $4::jsonb)
             RETURNING id, slug`,
            [effectiveName, slug, tenantId, JSON.stringify({ externalRef, connectorSource: 'platform-s', nameProvided: hasName })],
          ));
          let inserted;
          try {
            inserted = await insert(slugBase);
          } catch (e: unknown) {
            // Slug collision → one deterministic retry with an entropy suffix.
            if ((e as { code?: string }).code !== '23505') throw e;
            inserted = await insert(`${slugBase}-${crypto.randomBytes(2).toString('hex')}`);
          }
          organizationId = inserted.rows[0].id as string;
          orgSlug = inserted.rows[0].slug as string;
        }

        // Mint the per-org sk_ key (security service; the admin's own bearer
        // authorises + audits the mint — same pattern as KS-336 metering keys).
        const mintRes = await fetchWithTimeout(`${securityServiceUrl}/api/keys`, {
          method: 'POST',
          headers: authHeaders(req, 'application/json'),
          body: JSON.stringify({
            // KS-480 §4: label falls back to the GUID so a nameless org's key
            // never renders as a dangling `Platform S connector — `.
            name: `Platform S connector — ${hasName ? organizationName : externalRef}`,
            organizationId,
            tenantId,
            scopes,
            connectorId: `platform-s:${externalRef}`,
            // KS-577: on a rotate, the security service retires this
            // connector's PRIOR active keys. Without this flag the mint is
            // purely additive — the re-keyed credential is issued and the lost
            // one keeps working, which is the defect this closes. The flag
            // travels WITH the mint so one call decides both halves; a second
            // round trip could fail and leave both credentials live.
            rotate,
          }),
        });
        if (!mintRes.ok) {
          res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: `Key mint failed (security service ${mintRes.status})` } });
          return;
        }
        const mintBody = await mintRes.json() as {
          data?: { id: string; key: string; prefix: string; priorKeysRevoked?: number | null };
        };
        // KS-577: `null` means the revoke was ATTEMPTED AND FAILED, so the prior
        // credential is still valid. Surfaced rather than swallowed — an
        // operator re-keying a lost credential needs to know the lost one still
        // works. `console.error` matches this file's existing idiom (:899).
        if (rotate && mintBody?.data?.priorKeysRevoked === null) {
          console.error(
            '[KS-577] rotate minted a new key but the prior-key revoke FAILED — prior credential STILL VALID',
            { externalRef, organizationId },
          );
        }
        if (!mintBody?.data?.key) {
          res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Key mint returned no key material' } });
          return;
        }

        // Best-effort audit trail on the security service's audit log.
        fetchWithTimeout(`${securityServiceUrl}/api/audit`, {
          method: 'POST',
          headers: authHeaders(req, 'application/json'),
          body: JSON.stringify({
            userId: req.user?.userId,
            organizationId,
            action: rotate ? 'connector.key-rotate' : 'connector.register',
            resourceType: 'organization',
            resourceId: organizationId,
            details: { externalRef, keyId: mintBody.data.id, keyPrefix: mintBody.data.prefix, tenantId },
          }),
        }).catch(() => { /* audit is best-effort — the mint itself is logged by security */ });

        res.status(existing.rows.length > 0 ? 200 : 201).json({
          success: true,
          data: {
            organizationId,
            tenantId,
            tenantSlug: resolvedSlug,
            organizationSlug: orgSlug,
            keyId: mintBody.data.id,
            // Plaintext — returned exactly once; the server stores a hash.
            key: mintBody.data.key,
            scopes,
            rotated: rotate && existing.rows.length > 0,
          },
        });
      } catch (err: unknown) {
        sendUpstreamError(res, err);
      }
    },
  );

  // -----------------------------------------------------------------------
  // Tenant key management (session-scoped)
  // -----------------------------------------------------------------------

  router.post(
    '/api/platform/tenant-key',
    authenticateToken(),
    requireSuperAdmin,
    (req: Request, res: Response) => {
      const { tenantId, key } = req.body;
      if (!tenantId || !key) {
        res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'tenantId and key are required' } });
        return;
      }
      setTenantKey(tenantId, key);
      res.json({ success: true, message: 'Tenant key loaded for this session' });
    },
  );

  router.delete(
    '/api/platform/tenant-key/:tenantId',
    authenticateToken(),
    requireSuperAdmin,
    (req: Request, res: Response) => {
      removeTenantKey(req.params.tenantId);
      res.json({ success: true, message: 'Tenant key removed from session' });
    },
  );

  router.get(
    '/api/platform/tenant-key/:tenantId/status',
    authenticateToken(),
    requireSuperAdmin,
    (req: Request, res: Response) => {
      const loaded = !!getTenantKey(req.params.tenantId);
      res.json({ tenantId: req.params.tenantId, keyLoaded: loaded });
    },
  );

  // -----------------------------------------------------------------------
  // Platform Templates (document types + workflows)
  // -----------------------------------------------------------------------

  router.get(
    '/api/platform/templates/document-types',
    authenticateToken(),
    requireSuperAdmin,
    async (_req: Request, res: Response) => {
      try {
        const pg = require('pg');
        const pool = new pg.Pool({ connectionString: process.env.PLATFORM_DATABASE_URL, max: 2 });
        try {
          const result = await pool.query('SELECT * FROM platform_document_type_templates WHERE is_active = true ORDER BY name');
          res.json({
            success: true,
            templates: result.rows.map((r: any) => ({
              id: r.id, name: r.name, code: r.code, description: r.description,
              category: r.category, creatorVerificationLevel: r.creator_verification_level,
              verifierVerificationLevel: r.verifier_verification_level,
              requireMFA: r.require_mfa, requireWalletSignature: r.require_wallet_signature,
              autoAnchor: r.auto_anchor, metadataSchema: r.metadata_schema,
              createdAt: r.created_at, updatedAt: r.updated_at,
            })),
          });
        } finally { await pool.end(); }
      } catch (err: any) { res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch templates', details: { detail: err?.message } } }); }
    },
  );

  router.get(
    '/api/platform/templates/workflows',
    authenticateToken(),
    requireSuperAdmin,
    async (_req: Request, res: Response) => {
      try {
        const pg = require('pg');
        const pool = new pg.Pool({ connectionString: process.env.PLATFORM_DATABASE_URL, max: 2 });
        try {
          const result = await pool.query('SELECT * FROM platform_workflow_templates WHERE is_active = true ORDER BY name');
          res.json({
            success: true,
            templates: result.rows.map((r: any) => ({
              id: r.id, name: r.name, description: r.description,
              type: r.type, steps: r.steps, slaHours: r.sla_hours,
              createdAt: r.created_at, updatedAt: r.updated_at,
            })),
          });
        } finally { await pool.end(); }
      } catch { res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch templates' } }); }
    },
  );

  /**
   * POST /api/platform/templates/clone-to-tenant
   * Clone platform templates to a specific tenant's database
   */
  router.post(
    '/api/platform/templates/clone-to-tenant',
    authenticateToken(),
    requireSuperAdmin,
    async (req: Request, res: Response) => {
      try {
        const { tenantId, templateType } = req.body;
        if (!tenantId || !templateType) {
          return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'tenantId and templateType are required' } });
        }

        const r = await fetchWithTimeout(`${tenantProvisioningUrl}/api/tenants/${tenantId}`);
        if (!r.ok) return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Tenant not found' } });
        const tenantResp = await r.json() as any;
        const tenant = tenantResp.tenant || tenantResp;
        const dbName = tenant.config?.db_name || `secuura_tenant_${tenant.slug}`;

        const pg = require('pg');
        const platformPool = new pg.Pool({ connectionString: process.env.PLATFORM_DATABASE_URL, max: 2 });

        // Build tenant DB connection from PLATFORM_DATABASE_URL (points to real PG, not PgBouncer)
        const platformUrl = new URL(process.env.PLATFORM_DATABASE_URL || '');
        const tenantDbUrl = `postgresql://${platformUrl.username}:${platformUrl.password}@${platformUrl.hostname}:${platformUrl.port || 5432}/${dbName}`;
        const tenantPool = new pg.Pool({ connectionString: tenantDbUrl, max: 2 });

        try {
          let cloned = 0;
          if (templateType === 'document-types' || templateType === 'all') {
            const templates = await platformPool.query('SELECT * FROM platform_document_type_templates WHERE is_active = true');
            for (const t of templates.rows) {
              await tenantPool.query(
                `INSERT INTO document_type_configs (id, name, code, description, category, is_active,
                  creator_verification_level, owner_verification_level, viewer_verification_level, verifier_verification_level,
                  require_mfa, require_wallet_signature, require_kyc, auto_anchor, anchor_network, metadata_schema)
                 VALUES ($1,$2,$3,$4,$5,true,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15)
                 ON CONFLICT DO NOTHING`,
                [t.code, t.name, t.code, t.description, t.category,
                 t.creator_verification_level, t.owner_verification_level || 'basic',
                 t.viewer_verification_level || 'none', t.verifier_verification_level,
                 t.require_mfa, t.require_wallet_signature, t.require_kyc || false,
                 t.auto_anchor, t.anchor_network || 'preprod', JSON.stringify(t.metadata_schema || [])],
              );
              cloned++;
            }
          }
          if (templateType === 'workflows' || templateType === 'all') {
            const templates = await platformPool.query('SELECT * FROM platform_workflow_templates WHERE is_active = true');
            for (const t of templates.rows) {
              const wfId = t.name.toLowerCase().replace(/[^a-z0-9]+/g, '_');
              await tenantPool.query(
                `INSERT INTO workflow_configs (id, name, description, trigger_type, is_active, steps, sla_hours)
                 VALUES ($1,$2,$3,$4,true,$5,$6)
                 ON CONFLICT DO NOTHING`,
                [wfId, t.name, t.description, t.type || 'manual', JSON.stringify(t.steps), t.sla_hours],
              );
              cloned++;
            }
          }
          res.json({ success: true, cloned });
        } finally {
          await platformPool.end();
          await tenantPool.end();
        }
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : String(err);
        console.error('[Clone] Failed:', msg);
        res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Clone failed', details: { detail: msg } } });
      }
    },
  );

  // -----------------------------------------------------------------------
  // Cross-tenant document registry (public — for verifier portal)
  // -----------------------------------------------------------------------

  /**
   * GET /api/platform/document-lookup
   * Look up which tenant owns a document by hash or document ID.
   * Public endpoint — used by the verifier portal to resolve tenant context.
   */
  router.get(
    '/api/platform/document-lookup',
    async (req: Request, res: Response) => {
      try {
        const { hash, documentId } = req.query;
        if (!hash && !documentId) {
          return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'hash or documentId query parameter is required' } });
        }

        const platformDbUrl = process.env.PLATFORM_DATABASE_URL;
        if (!platformDbUrl) {
          return res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Platform database not configured' } });
        }

        // Dynamic import to avoid pg dependency at module level
        const pg = require('pg');
        const pool = new pg.Pool({ connectionString: platformDbUrl, max: 2 });

        try {
          let result;
          if (hash) {
            result = await pool.query(
              'SELECT document_id, tenant_id, tenant_slug, document_type, title, status, certified_at FROM platform_document_registry WHERE content_hash = $1 LIMIT 5',
              [hash],
            );
          } else {
            result = await pool.query(
              'SELECT document_id, tenant_id, tenant_slug, document_type, title, status, certified_at FROM platform_document_registry WHERE document_id = $1 LIMIT 5',
              [documentId],
            );
          }

          res.json({
            success: true,
            results: result.rows.map((r: any) => ({
              documentId: r.document_id,
              tenantId: r.tenant_id,
              tenantSlug: r.tenant_slug,
              documentType: r.document_type,
              title: r.title,
              status: r.status,
              certifiedAt: r.certified_at,
            })),
          });
        } finally {
          await pool.end();
        }
      } catch (err: unknown) {
        res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Document lookup failed' } });
      }
    },
  );

  return router;
}
