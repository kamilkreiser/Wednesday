/**
 * =============================================================================
 * AUDIT-LOG MIDDLEWARE — captures business events with actor identity
 * =============================================================================
 *
 * BACKLOG H1 (was F-ADM-03 critical): the platform_audit_log table contained
 * only `tenant_created` (×19) + `migration_default_tenant` (×1) entries, every
 * row with `actor_id:null, ip_address:null`. Zero login / doc / anchor / verify
 * / revoke events. That's a compliance failure — an audit log isn't an audit
 * log if it doesn't record business events with actor identity.
 *
 * What this middleware captures:
 *   - method, path, status, duration
 *   - actor (req.user.userId if available, or extracted from /api/auth/login
 *     response body for the login-success case where req.user isn't set yet)
 *   - organizationId / tenantId from req.user
 *   - ipAddress from X-Forwarded-For (first hop) or req.socket.remoteAddress
 *   - userAgent from request headers
 *   - resourceType + resourceId derived from the route (POST /api/documents
 *     → resource_type:'document'; PATCH /api/users/me → resource_id is the
 *     calling user)
 *   - success boolean from response status
 *
 * Scope:
 *   - state-changing methods only (POST/PUT/PATCH/DELETE) on /api/* paths
 *   - excludes a small allow-list of noisy / system endpoints (health, csrf,
 *     metrics) and the audit endpoints themselves (avoids recursion / noise)
 *   - reads (GET) are NOT logged — this is to keep volume manageable; if
 *     specific high-sensitivity reads need auditing later, route them through
 *     a dedicated audit hook
 *
 * Reliability:
 *   - fire-and-forget DB write inside res.on('finish'); a failure NEVER blocks
 *     or affects the response (only logs a warning)
 *   - if isDbAvailable() is false (no DATABASE_URL), the entry is dropped —
 *     a future enhancement could buffer to Redis or stdout
 *
 * Encryption:
 *   - audit_logs.details is widened to TEXT and the security service can
 *     decrypt v<N>:iv:tag:ciphertext payloads. Today we write plaintext
 *     JSON; the security-service reader already handles plaintext as a
 *     legacy fallback so reads still work. Encrypting from gateway too is a
 *     potential follow-up (would need initFromEnv() at gateway startup).
 * =============================================================================
 */

import { Request, Response, NextFunction, RequestHandler } from 'express';
import { runWithTenantId } from '@secuura/shared';

export interface AuditMiddlewareDeps {
  /** Database query function. Best-effort — write failures don't propagate. */
  query: (sql: string, params: unknown[]) => Promise<{ rows: any[] }>;
  isDbAvailable: () => boolean;
  /** Logger compatible with the existing api-gateway `log()` signature. */
  log: (level: 'info' | 'warn' | 'error', msg: string, ctx?: object) => void;
}

const AUDITED_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

// audit_logs.resource_id is a UUID column. Non-UUID values from the route
// (e.g. 'me' on PATCH /api/users/me, or 'verify' on POST /api/verification/verify)
// must NULL out instead of being inserted — otherwise Postgres throws
// "invalid input syntax for type uuid" and the audit row is dropped.
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
function asUuidOrNull(v: string | null): string | null {
  return v && UUID_RE.test(v) ? v : null;
}

// Exact paths that should never produce an audit entry.
const EXCLUDED_PATHS = new Set<string>([
  '/api/health',
  '/api/csrf',
  '/api/csrf-token',
]);

// Path prefixes that should never produce an audit entry. Audit endpoints
// themselves are excluded so the act of querying audit doesn't generate
// new audit rows.
const EXCLUDED_PREFIXES = [
  '/health',
  '/system/',
  '/api/system/health',
  '/api/audit',           // security service POST/GET/etc.
  '/api/security/audit',  // gateway's audit-export router
  '/api/admin/audit',     // gateway's audit-export router
];

/**
 * Build a `{action, resourceType, resourceId}` triple from the request route.
 * The mapping is intentionally permissive — anything we haven't explicitly
 * mapped falls back to `${section}.${verb}` based on the path's first
 * segments + the HTTP method. That gives a sensible default for the long
 * tail without needing to enumerate every route.
 */
function deriveAction(req: Request, path: string): {
  action: string;
  resourceType: string;
  resourceId: string | null;
} {
  const method = req.method.toUpperCase();
  const verb = method === 'POST' ? 'create'
    : method === 'PUT' ? 'replace'
    : method === 'PATCH' ? 'update'
    : method === 'DELETE' ? 'delete'
    : method.toLowerCase();

  // Trim trailing slashes and pull the first 3-4 segments after /api.
  // KS-871: derive from `path`, the canonical path captured when the middleware ran
  // (see createAuditMiddleware), not from req.path at call time (the prior read).
  // This runs inside 'finish', where a responding router.use gate has left req.path
  // mount-relative, so a refused POST /api/gdpr/erasures derived 'unknown.create'.
  const segments = path.replace(/\/+$/, '').split('/').filter(Boolean);
  // segments[0] === 'api' for everything we audit
  const section = segments[1] || 'unknown';
  const subResource = segments[2];
  const subAction = segments[3];

  // Special-case routes where the conventional verb-from-method mapping is
  // wrong (e.g. POST /api/documents/:id/verify is a 'verify', not a 'create').
  // Auth routes also don't fit the CRUD shape.
  if (section === 'auth') {
    if (subResource === 'login') return { action: 'auth.login', resourceType: 'session', resourceId: null };
    if (subResource === 'logout') return { action: 'auth.logout', resourceType: 'session', resourceId: null };
    if (subResource === 'refresh') return { action: 'auth.refresh', resourceType: 'session', resourceId: null };
    if (subResource === 'register') return { action: 'auth.register', resourceType: 'user', resourceId: null };
    return { action: `auth.${subResource || verb}`, resourceType: 'session', resourceId: null };
  }

  // Two URL shapes that don't fit CRUD-from-method need verb detection:
  //   /api/<noun>/<verb>           — POST /api/verification/verify
  //   /api/<noun>/:id/<verb>       — POST /api/documents/:id/revoke
  // A small whitelist disambiguates "verb" from "resource designator" — we
  // can't just assume "subResource not UUID == verb" because /api/users/me
  // legitimately uses 'me' as a self-designator and should still be
  // 'users.update', not 'users.me'.
  const VERB_WORDS = new Set([
    'verify', 'revoke', 'sign', 'mint', 'anchor', 'certify', 'recertify',
    'approve', 'reject', 'initiate', 'archive', 'share', 'unshare',
    'transfer', 'delegate', 'export', 'import', 'enable', 'disable',
    'rotate', 'regenerate', 'resend', 'cancel', 'lock', 'unlock',
    'reset', 'change-password',
  ]);

  // Shape: /api/<noun>/:id/<verb>
  if (subAction && VERB_WORDS.has(subAction)) {
    return {
      action: `${section}.${subAction}`,
      resourceType: section.replace(/s$/, ''),
      resourceId: typeof req.params?.id === 'string' ? req.params.id : (subResource || null),
    };
  }

  // Shape: /api/<noun>/<verb>
  if (subResource && !subAction && VERB_WORDS.has(subResource)) {
    return {
      action: `${section}.${subResource}`,
      resourceType: section.replace(/s$/, ''),
      resourceId: null,
    };
  }

  // H27 (2026-04-28): when subAction is a UUID, it's the resource ID,
  // NOT a verb. Previous code would emit action=`platform.<uuid>` for
  // DELETE /api/platform/tenants/<uuid>, polluting the action namespace
  // with one entry per deleted tenant. SIEM / dashboards group by
  // `action`, so this needs to be a stable verb. Pattern:
  //   /api/<section>/<subResource>/<uuid>     → action=<section>.<subResource(singular)>.<verb>
  //   /api/<section>/<subResource>            → action=<section>.<subResource>.<verb>
  if (subAction && UUID_RE.test(subAction)) {
    const noun = (subResource || '').replace(/s$/, '') || 'resource';
    return {
      action: `${section}.${noun}.${verb}`,
      resourceType: noun,
      resourceId: subAction,
    };
  }

  // Generic CRUD shape: POST /api/foo → foo.create, PATCH /api/foo/:id → foo.update
  const action = subAction
    ? `${section}.${subAction}`
    : `${section}.${verb}`;
  const resourceType = section.replace(/s$/, '') || 'unknown';
  const resourceId = typeof req.params?.id === 'string'
    ? req.params.id
    : (subResource && !subAction ? subResource : null);

  return { action, resourceType, resourceId };
}

function getClientIp(req: Request): string | null {
  const xff = req.headers['x-forwarded-for'];
  if (typeof xff === 'string' && xff.length > 0) {
    return xff.split(',')[0].trim();
  }
  if (Array.isArray(xff) && xff.length > 0) {
    return xff[0];
  }
  return req.socket?.remoteAddress || null;
}

/**
 * Returns an Express middleware that records an audit entry for every
 * mutation on /api/*. Wire it into the gateway after auth-related middleware
 * but before route handlers, so req.user (when set by route-level
 * authenticate()) is visible and the response body can still be intercepted.
 */
export function createAuditMiddleware(deps: AuditMiddlewareDeps): RequestHandler {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!AUDITED_METHODS.has(req.method.toUpperCase())) return next();
    if (!req.path.startsWith('/api/')) return next();
    if (EXCLUDED_PATHS.has(req.path)) return next();
    if (EXCLUDED_PREFIXES.some((p) => req.path.startsWith(p))) return next();

    const start = Date.now();

    // KS-871: capture the path once, at entry. A responding router.use gate (the
    // KS-843 erasure door) leaves req.path mount-relative, and 'finish' fires before
    // anything restores it, so a refused POST /api/gdpr/erasures was audited as '/'.
    // The source is req.path HERE, where this middleware is mounted at the app root
    // after index.ts's /api/v1 strip: the canonical path the entry gates above read.
    // Round 1 read req.originalUrl, which express never rewrites, so it kept the
    // /api/v1 spelling (every production write after the 307), an absolute-form host,
    // a #fragment and repeated slashes (QA gate on #1011, F-1011-1..3).
    const auditPath = req.path;

    // Wrap res.json so the login-success path can extract the userId from the
    // response body. Without this, /api/auth/login audit entries have a null
    // actor — defeating the whole point of the audit log for the most
    // important event. The wrapper is non-invasive: it captures the body
    // synchronously then defers to the original res.json().
    const origJson = res.json.bind(res);
    let capturedBody: unknown = null;
    res.json = function patched(body: unknown) {
      capturedBody = body;
      return origJson(body);
    };

    res.on('finish', () => {
      // Fire-and-forget. If anything goes wrong, log a warning and move on —
      // a failed audit write must never affect the actual response.
      void (async () => {
        try {
          if (!deps.isDbAvailable()) return;
          const { action, resourceType, resourceId: routeResourceId } = deriveAction(req, auditPath);

          const u = (req as Request & { user?: { userId?: string; organizationId?: string; tenantId?: string } }).user;
          let userId: string | null = u?.userId || null;
          let resourceId: string | null = routeResourceId;

          // Login special case — req.user isn't set on incoming /login (the
          // user is being authenticated AS PART OF this request). Try the
          // response body. NOTE: /api/auth/login is proxied to the auth
          // service via http-proxy-middleware which streams the upstream
          // body straight to the client without ever calling res.json(), so
          // capturedBody will be null on success — the entry will record IP
          // + success but not user_id. The next authed request WILL carry
          // req.user, so the chain is still traceable. Follow-up: have the
          // auth-service POST /api/audit on login success directly, where
          // it knows the user_id with certainty.
          if (
            req.path === '/api/auth/login' &&
            res.statusCode === 200 &&
            capturedBody &&
            typeof capturedBody === 'object'
          ) {
            const body = capturedBody as {
              data?: { user?: { id?: string } };
              user?: { id?: string };
            };
            const loginUserId = body?.data?.user?.id || body?.user?.id || null;
            if (loginUserId) {
              userId = loginUserId;
              resourceId = loginUserId;
            }
          }

          const success = res.statusCode >= 200 && res.statusCode < 400;
          const ip = getClientIp(req);
          const userAgent = (req.headers['user-agent'] as string) || null;
          // H29 (2026-04-28): capture the attempted login email so the UI
          // can show "who tried to log in" even when the proxy stream meant
          // we couldn't resolve the user_id from the response. Email comes
          // from the request body — we already have it in this request
          // cycle; safe to include in details. (Failed-login enumeration
          // risk is bounded — the audit log is only readable by super-
          // admins, who can already enumerate users via /api/admin/users.)
          let attemptedEmail: string | undefined;
          if (req.path === '/api/auth/login' && req.body && typeof req.body === 'object') {
            const e = (req.body as { email?: unknown }).email;
            if (typeof e === 'string') attemptedEmail = e.toLowerCase();
          }
          const details = JSON.stringify({
            method: req.method,
            path: auditPath, // KS-871: was req.path, the trimmed remainder for a refused request
            status: res.statusCode,
            durationMs: Date.now() - start,
            tenantId: u?.tenantId || null,
            ...(attemptedEmail ? { attemptedEmail } : {}),
          });

          // KS-28: every audit row carries the writing tenant. Falls back to
          // the default tenant id (same as extractTenantContext's non-prod
          // fallback) when the request has no tenant context (e.g. an
          // unauthenticated request to a public endpoint, or a service-to-
          // service call before auth middleware has resolved the JWT).
          const auditTenantId = u?.tenantId || 'a0000000-0000-4000-8000-000000000001';
          // KS-458: the res 'finish' callback keeps the ALS context from
          // registration time (pre-auth), so pin the GUC to the row's tenant
          // explicitly — fail-closed WITH CHECK rejects a mismatched write.
          await runWithTenantId(auditTenantId, () => deps.query(
            `INSERT INTO audit_logs (
               id, tenant_id, user_id, organization_id, action, resource_type,
               resource_id, ip_address, user_agent, details, success, created_at
             ) VALUES (
               gen_random_uuid(), $1::uuid, $2, $3, $4, $5, $6, $7, $8, $9, $10, NOW()
             )`,
            [
              auditTenantId,
              asUuidOrNull(userId),
              asUuidOrNull(u?.organizationId || null),
              action,
              resourceType,
              asUuidOrNull(resourceId),
              ip,
              userAgent,
              details,
              success,
            ],
          ));
        } catch (err) {
          deps.log('warn', 'audit middleware: write failed', {
            error: err instanceof Error ? err.message : String(err),
            path: req.path,
          });
        }
      })();
    });

    next();
  };
}
