/**
 * =============================================================================
 * PROXY ROUTE DEFINITIONS
 * =============================================================================
 * Extracted from the API gateway monolith. Contains:
 * - createServiceProxy helper (http-proxy-middleware config factory)
 * - Blocked-extension / MIME-type file-upload inspection middleware
 * - All service proxy route definitions
 * - MCP server proxy endpoint
 * =============================================================================
 */

import express, { Router, Request, Response, NextFunction, RequestHandler } from 'express';
import * as http from 'http';
import { createProxyMiddleware, Options } from 'http-proxy-middleware';
import { requireScope, attachScopes, requireScopeOrRole } from '../middleware/scopes';
import * as redisService from '../services/redis';
import { CircuitBreaker } from '@secuura/shared';
import { collapseRepeatedSlashes } from '../middleware/normalisePath';

// KS-1041 Step 2 — the shared secret that proves a request came through this
// gateway. Read once at module load; see onProxyReq below for what it does and
// who receives it, and utils/trustHeaders.ts's TRUST_HEADER_PATTERN (applied by
// index.ts at the edge) for why a client can never supply it.
//
// Deliberately NOT placed in @secuura/shared alongside the other cross-service
// constants: that package is linked into all 31 service images, so touching it
// invalidates every one of them. Keeping the constant local to the two services
// that need it holds the rebuild to those two. The cost is that the header name
// is written twice — gateway and originate — so both sides carry a comment
// naming the other.
const GATEWAY_VOUCH_SECRET = process.env.GATEWAY_VOUCH_SECRET || '';

// KS-1041 Step 2 — the ONLY upstream service keys the vouch is sent to. A
// service that receives the vouch holds a credential that impersonates this
// gateway to originate, so a key belongs here only if that service VERIFIES the
// vouch — never because it reads trust headers. A per-request HMAC over method,
// path and timestamp, verified by originate, would make a captured value
// unreplayable; that is the considered follow-up, not part of this change.
// Until then, reach is the defence.
const VOUCH_RECIPIENTS: ReadonlySet<string> = new Set(['originate']);

// Pen-test M3 fix: per-service circuit breaker registry. http-proxy-middleware
// streams; we can't easily wrap it in CircuitBreaker.execute, so instead we:
//   1. Track failures from `onError`.
//   2. Pre-check the breaker state in a gate middleware. If OPEN, return 503
//      immediately without ever touching the downstream service.
// Conservative thresholds: 5 failures in 30s window → open for 60s.
/**
 * KS-453: decide whether a proxied request must have its parsed body
 * re-serialised and written to the upstream, and what to write.
 *
 * The api-gateway's `express.json()` runs before the proxy on any non-`proxyPaths`
 * route and consumes the request stream, leaving the body only on `req.body`.
 * http-proxy-middleware then has nothing to pipe, so a body-bearing method must
 * have its parsed body re-written explicitly — INCLUDING an empty object `{}`.
 * The prior guard skipped empty objects, so `PATCH /api/did/0` with `{}` set a
 * Content-Length header but wrote no body and the upstream hung to a 60 s
 * timeout → a misleading 502.
 *
 * @param method - the request's HTTP method (any case)
 * @param parsedBody - `req.body` after express.json (undefined on unparsed/proxyPaths routes)
 * @returns the JSON string to write to the upstream, or `null` when nothing
 *          should be re-streamed (unparsed body, non-object, or a bodyless method)
 */
export function proxyBodyToWrite(method: string, parsedBody: unknown): string | null {
  const m = (method || '').toUpperCase();
  if (m !== 'POST' && m !== 'PUT' && m !== 'PATCH') return null;
  if (!parsedBody || typeof parsedBody !== 'object' || Buffer.isBuffer(parsedBody)) return null;
  return JSON.stringify(parsedBody);
}

const breakerRegistry = new Map<string, CircuitBreaker>();
function getBreaker(serviceKey: string): CircuitBreaker {
  let b = breakerRegistry.get(serviceKey);
  if (!b) {
    b = new CircuitBreaker({
      name: serviceKey,
      failureThreshold: 5,
      resetTimeoutMs: 60_000,
      requestTimeoutMs: 60_000,
      halfOpenMaxAttempts: 2,
    });
    breakerRegistry.set(serviceKey, b);
  }
  return b;
}

export function circuitBreakerGate(serviceKey: string): RequestHandler {
  return (_req: Request, res: Response, next: NextFunction) => {
    const b = getBreaker(serviceKey);
    if (b.getState() === 'open') {
      res.status(503).json({
        success: false,
        error: {
          code: 'SERVICE_UNAVAILABLE',
          message: 'Service temporarily unavailable',
          details: {
            service: serviceKey,
            retryAfterMs: 60_000,
          },
        },
      });
      return;
    }
    next();
  };
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface ServiceConfig {
  name: string;
  url: string;
  healthPath: string;
  requiresAuth: boolean;
}

export interface ProxyRouteDeps {
  /** Map of service key -> service config (url, name, etc.) */
  services: Record<string, ServiceConfig>;
  /** Auth middleware factory – call with `true` (required) or `false` (optional) */
  authenticateToken: (required?: boolean) => RequestHandler;
  /** Structured logger matching the gateway's `log()` signature */
  log: (level: 'info' | 'warn' | 'error', message: string, meta?: object) => void;
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const BLOCKED_EXTENSIONS = [
  '.exe', '.bat', '.cmd', '.com', '.msi', '.scr',
  '.pif', '.vbs', '.js', '.ws', '.ps1', '.sh',
];

// KS-529: shared keep-alive agent for the upstream (gateway→service) hop.
// Without an explicit agent, http-proxy-middleware falls back to Node's global
// agent (keepAlive:false), which opens a fresh TCP socket per proxied request.
// Under a concurrent Schemathesis sweep that socket churn exhausts ephemeral
// ports / overruns each upstream's listen backlog → ECONNRESET/ECONNREFUSED →
// the onError 502 on requests that should have been a deterministic 401/400.
// A pooled keep-alive agent reuses connections and bounds per-upstream
// concurrency, collapsing the transient-502 class. All upstreams are plain
// http on the internal Docker network. maxSockets is per-host, so each service
// gets its own pool.
const proxyAgent = new http.Agent({
  keepAlive: true,
  keepAliveMsecs: 30_000,
  maxSockets: 128,
  maxFreeSockets: 32,
  timeout: 60_000,
  scheduling: 'lifo',
});

// ---------------------------------------------------------------------------
// Helper: build http-proxy-middleware Options for a service
// ---------------------------------------------------------------------------

function createServiceProxy(
  services: Record<string, ServiceConfig>,
  log: ProxyRouteDeps['log'],
  serviceKey: string,
  pathRewrite?: Record<string, string>,
): Options {
  const service = services[serviceKey];
  if (!service) {
    log('warn', `Service '${serviceKey}' not configured — proxy will use fallback URL`);
    return {
      target: `http://${serviceKey}:4000`,
      changeOrigin: true,
      agent: proxyAgent,
      pathRewrite: pathRewrite || { [`^/api/${serviceKey}`]: '' },
    };
  }
  return {
    target: service.url,
    changeOrigin: true,
    agent: proxyAgent,
    pathRewrite: pathRewrite || { [`^/api/${serviceKey}`]: '' },
    proxyTimeout: 60000,
    timeout: 60000,
    onError: (err, _req, res) => {
      // Pen-test M3: record failure with the per-service breaker. After
      // failureThreshold consecutive failures, the next request is
      // short-circuited by circuitBreakerGate above (returns 503 without
      // touching the downstream service).
      try {
        const breaker = getBreaker(serviceKey);
        // Drive the state machine via execute() against a rejecting
        // promise — the breaker counts the failure and may open.
        breaker.execute(async () => { throw err; }).catch(() => {});
      } catch (_e) { /* breaker accounting must never throw */ }
      log('error', 'Proxy error', { service: serviceKey, error: err.message });
      (res as Response).status(502).json({
        success: false,
        error: {
          code: 'BAD_GATEWAY',
          message: `Upstream service "${service.name}" is unreachable or returned an error.`,
        },
      });
    },
    onProxyRes: (proxyRes, req) => {
      // Pen-test M3: a 5xx from downstream counts as a failure for breaker.
      const code = proxyRes.statusCode || 0;
      if (code >= 500 && code < 600) {
        try {
          const breaker = getBreaker(serviceKey);
          breaker.execute(async () => { throw new Error(`upstream ${code}`); }).catch(() => {});
        } catch (_e) { /* breaker accounting must never throw */ }
      }
      // Rewrite Location headers ONLY when a downstream service leaked its own
      // internal address — e.g. a relative res.redirect() that Express resolved
      // against the internal upstream Host (m365-integration:4013). A redirect
      // the service deliberately pointed at a public URL (the admin SPA via
      // FRONTEND_URL, the verifier, etc.) must be left untouched. The previous
      // unconditional rewrite replaced the host with req.headers.host, which
      // (a) strips the gateway port locally — nginx forwards `Host $host` with
      // no port, so a correct `:6882` became `:80` (dead) — and (b) would send
      // the client to the wrong origin on the cross-origin demo, where the admin
      // SPA and the api are different hosts. Scoping the rewrite to the upstream
      // target host fixes both without disturbing the genuine internal-leak case
      // (where the leaked host equals the proxy target). (KS-241)
      if (proxyRes.headers.location) {
        try {
          const loc = new URL(proxyRes.headers.location);
          const targetHost = new URL(service.url).host;
          if (loc.host === targetHost) {
            const gatewayHost = req.headers.host || 'localhost:6882';
            const protocol = req.headers['x-forwarded-proto'] || 'https';
            proxyRes.headers.location = `${protocol}://${gatewayHost}${loc.pathname}${loc.search}${loc.hash}`;
          }
        } catch {
          // Relative or unparseable Location → leave as-is. A relative Location
          // is resolved by the browser against the gateway origin, which is the
          // correct public origin, so no rewrite is needed.
        }
      }
    },
    onProxyReq: (proxyReq, req) => {
      // Forward request ID
      const requestId = (req as Request).requestId;
      if (requestId) {
        proxyReq.setHeader('X-Request-ID', requestId);
      }

      // KS-1041 Step 2 — vouch that this request came through the edge, and
      // vouch ONLY to the service that checks it.
      //
      // originate honours identity/tenant/role headers that this gateway sets
      // from a verified JWT. Those headers are only trustworthy if the request
      // actually came through here: a peer container on the flat compose
      // network can address originate:4000 directly and send them itself. This
      // header is what lets originate tell the two apart.
      //
      // The vouch is a bearer credential, so WHO RECEIVES IT is the control:
      // any service it reaches can replay it straight to originate:4000 and
      // have forged trust headers honoured. Minted here for every upstream, as
      // it first was, it reached every other service (measured at analytics
      // and auth by the #951 gate, round 1, F1), which moved the KS-1041
      // forgery one hop instead of closing it. So it goes only to the keys in
      // VOUCH_RECIPIENTS — read that constant before adding one. Both halves
      // (originate receives it; analytics and auth do not) are pinned in
      // __tests__/ks1041-vouch-mint-scope.test.ts.
      //
      // Set on the OUTGOING request, after the edge strip in index.ts has
      // already removed any client-supplied `x-gateway-vouch` from the
      // inbound one — so this value is always gateway-minted.
      //
      // Unset secret => header not sent => originate treats the call as
      // unvouched and drops the trust headers. That is the fail-closed
      // direction: an unconfigured gateway loses privilege, never gains it.
      if (GATEWAY_VOUCH_SECRET && VOUCH_RECIPIENTS.has(serviceKey)) {
        proxyReq.setHeader('x-gateway-vouch', GATEWAY_VOUCH_SECRET);
      }

      // Forward policy evaluation headers to downstream services
      const policyResult = req.headers['x-policy-result'];
      if (policyResult) {
        proxyReq.setHeader('X-Policy-Result', policyResult as string);
      }
      const policyId = req.headers['x-policy-id'];
      if (policyId) {
        proxyReq.setHeader('X-Policy-ID', policyId as string);
      }

      // Explicitly forward Authorization. http-proxy-middleware passes
      // headers by default, but the body-restream block below can race
      // with header serialisation on POST/PUT/PATCH and drop it. Setting
      // it explicitly here is a no-op when it's already present and a
      // fix when it isn't — addresses BACKLOG #2 (anchoring "No token
      // provided" 500 → nginx 502 chain).
      if (req.headers.authorization) {
        proxyReq.setHeader('Authorization', req.headers.authorization);
      }

      // Re-stream the parsed body. The api-gateway's express.json() body
      // parser runs before this proxy and consumes the request stream,
      // leaving the body only on req.body. http-proxy-middleware then has
      // nothing to pipe to proxyReq and the upstream connection is closed
      // mid-headers (ECONNRESET → 502). Re-serialising the body and
      // writing it explicitly fixes this for any POST/PUT/PATCH that has
      // a JSON body. (BACKLOG #2 — gateway proxy strips Authorization.)
      // KS-453: re-stream the parsed body (empty `{}` included — see
      // proxyBodyToWrite). A proxyPaths route is never parsed here, so req.body
      // is undefined and the raw stream pipes natively; only parsed-body routes
      // reach the write branch.
      const bodyData = proxyBodyToWrite(req.method || '', (req as any).body);
      if (bodyData !== null) {
        proxyReq.setHeader('Content-Type', 'application/json');
        proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
        proxyReq.write(bodyData);
      } else if (req.headers['content-length']) {
        proxyReq.setHeader('Content-Length', req.headers['content-length']);
      }
    },
  };
}

/**
 * KS-1187: which gdpr sub-path the erasure door must judge, decided on the
 * CANONICAL path rather than the raw spelling. `subUrl` is `req.url` inside the
 * `/api/gdpr` mount, where express keeps an absolute-form target's
 * `scheme://authority` in front of the path. Canonical means: the path express
 * routes on (no query, fragment or authority), each segment's `;params`
 * dropped, percent-decoded, `.`/`..` resolved and empty segments removed. The
 * first segment is compared the way the door's router compares (case-folded
 * unless it is case sensitive).
 *
 * - `door`: the canonical path is `/erasures` or below it. The door judges it.
 * - `not-door`: the canonical path plainly is not the door. Forwarded as before,
 *   even when a later segment is malformed.
 * - `undetermined`: the first segment cannot be decoded, or `..` climbs out of the
 *   mount, so nothing can say whether it names the door. Refused fail-closed.
 *
 * The door and its tests both use this function; there is no second copy.
 */
export function erasureDoorVerdict(
  subUrl: string,
  caseSensitive: boolean,
): { verdict: 'door' | 'not-door' | 'undetermined'; canonicalPath: string | null } {
  let path = subUrl;
  const tailStart = path.search(/[?#]/);
  if (tailStart !== -1) path = path.slice(0, tailStart);
  const scheme = /^[A-Za-z][A-Za-z0-9+\-.]*:\/\//.exec(path);
  if (scheme) {
    const pathStart = path.indexOf('/', scheme[0].length);
    path = pathStart === -1 ? '/' : path.slice(pathStart);
  }
  const segments: Array<string | null> = [];
  for (const raw of path.split('/')) {
    let decoded: string | null;
    try {
      decoded = decodeURIComponent(raw.split(';')[0]);
    } catch {
      decoded = null;
    }
    for (const segment of decoded === null ? [null] : decoded.split('/')) {
      if (segment === '' || segment === '.') continue;
      if (segment === '..') {
        if (segments.length === 0) return { verdict: 'undetermined', canonicalPath: null };
        segments.pop();
        continue;
      }
      segments.push(segment);
    }
  }
  const first = segments[0];
  if (first === undefined) return { verdict: 'not-door', canonicalPath: '/' };
  if (first === null) return { verdict: 'undetermined', canonicalPath: null };
  if ((caseSensitive ? first : first.toLowerCase()) !== 'erasures') {
    return { verdict: 'not-door', canonicalPath: null };
  }
  return { verdict: 'door', canonicalPath: '/' + segments.map((x) => x ?? '').join('/') };
}

// ---------------------------------------------------------------------------
// Factory
// ---------------------------------------------------------------------------

export function createProxyRoutes(deps: ProxyRouteDeps): Router {
  const { services, authenticateToken, log } = deps;
  const router = Router();

  /** Shorthand so route definitions stay concise */
  const proxy = (key: string, rewrite?: Record<string, string>) => {
    const inner = createProxyMiddleware(createServiceProxy(services, log, key, rewrite));
    // KS-41: wrap the proxy so synchronous throws (e.g. "body already
    // consumed by express.json before proxy could re-stream it" — happens
    // when a route mount is missing from proxyPaths in index.ts) get logged
    // with the service key + path instead of falling through to Express's
    // default error handler as a bare `{"error":"Internal Server Error"}`.
    const wrapped: RequestHandler = (req, res, next) => {
      try {
        return (inner as unknown as RequestHandler)(req, res, next);
      } catch (err) {
        log('error', 'Proxy chain threw synchronously', {
          service: key,
          path: req.path,
          method: req.method,
          error: (err as Error).message,
        });
        if (res.headersSent) return;
        res.status(502).json({
          success: false,
          error: {
            code: 'BAD_GATEWAY',
            message: `Upstream "${key}" proxy chain failed before forwarding`,
            details: { reason: (err as Error).message },
          },
        });
        return;
      }
    };
    return wrapped;
  };

  // =========================================================================
  // AUTH / USER / SESSION (no gateway auth — handled by auth service)
  // =========================================================================

  router.use('/api/auth', proxy('auth', { '^/api/auth': '/api/auth' }));

  // OAuth 2.0 routes — proxy to auth service
  router.use('/api/oauth', proxy('auth', { '^/api/oauth': '/api/oauth' }));

  // Webhooks — proxy to originate (requires webhooks:manage scope)
  router.use('/api/webhooks',
    authenticateToken(true),
    attachScopes,
    requireScope('webhooks:manage'),
    proxy('originate', { '^/api/webhooks': '/api/webhooks' }),
  );

  // User routes — proxy to auth service (includes /api/users/me)
  router.use('/api/users/me',
    authenticateToken(true),
    proxy('auth', { '^/api/users': '/api/users' }),
  );

  // KS-69: GET /api/users/lookup?email=… — tenant-scoped email → userId.
  // Explicit handler ahead of the catch-all so the `users:read` scope gate
  // fires for OAuth / sk_* callers. JWT humans satisfy `requireScope`
  // automatically (the middleware short-circuits authMethod='jwt'/'email');
  // the downstream auth-service handler then enforces the role allow-list
  // and tenant filter for them — see services/auth/src/routes/users.ts.
  router.use('/api/users/lookup',
    authenticateToken(true),
    attachScopes,
    requireScope('users:read'),
    proxy('auth', { '^/api/users': '/api/users' }),
  );

  // POST /api/users/admin/create — explicit handler to avoid proxy body issues.
  // KS-689: authenticateToken(true) was missing here while the identically-written
  // PATCH neighbour below carried it. Not a live bypass — this handler forwards the
  // bearer to services/auth, which owns the session table and re-checks — but the
  // gateway's own session-revocation check lives inside this middleware, so without
  // it the route was protected only by which service happens to sit behind it.
  router.post('/api/users/admin/create', authenticateToken(true), async (req: any, res: any) => {
    try {
      const authUrl = services.auth?.url || 'http://auth:4003';
      const token = req.headers.authorization;
      // Read body from raw request if not parsed
      let body = '';
      if (req.body && Object.keys(req.body).length > 0) {
        body = JSON.stringify(req.body);
      } else {
        body = await new Promise<string>((resolve) => {
          let data = '';
          req.on('data', (chunk: any) => { data += chunk; });
          req.on('end', () => resolve(data));
        });
      }
      const upstream = await fetch(`${authUrl}/api/users/admin/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: token } : {}),
        },
        body,
      });
      const data = await upstream.json().catch(() => ({}));
      res.status(upstream.status).json(data);
    } catch (err: any) {
      console.error('User create proxy failed:', err?.message);
      res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Auth service unavailable' } });
    }
  });

  // PATCH /api/users/admin/:id — explicit handler to avoid proxy body-stream hang
  router.patch('/api/users/admin/:id', authenticateToken(true), async (req: any, res: any) => {
    try {
      const authUrl = services.auth?.url || 'http://auth:4003';
      const token = req.headers.authorization;
      let body = '';
      if (req.body && Object.keys(req.body).length > 0) {
        body = JSON.stringify(req.body);
      } else {
        body = await new Promise<string>((resolve) => {
          let data = '';
          req.on('data', (chunk: any) => { data += chunk; });
          req.on('end', () => resolve(data));
        });
      }
      const upstream = await fetch(`${authUrl}/api/users/admin/${req.params.id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: token } : {}),
        },
        body,
      });
      const data = await upstream.json().catch(() => ({}));
      res.status(upstream.status).json(data);
    } catch (err: any) {
      console.error('User admin PATCH proxy failed:', err?.message);
      res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Auth service unavailable' } });
    }
  });

  router.use('/api/users',
    authenticateToken(true),
    proxy('auth', { '^/api/users': '/api/users' }),
  );
  router.use('/api/sessions', proxy('auth', { '^/api/sessions': '/api/sessions' }));

  // KS-83: per-org X.509 cert lifecycle. Auth-required at gateway; the
  // service enforces ORG_ADMIN+ role OR `issuer-certs:*` scope.
  router.use('/api/issuer-certs',
    authenticateToken(true),
    proxy('auth', { '^/api/issuer-certs': '/api/issuer-certs' }),
  );

  // =========================================================================
  // FILE UPLOAD SECURITY
  // =========================================================================

  router.post('/api/documents/upload', authenticateToken(true), (req: Request, res: Response, next: NextFunction) => {
    const contentType = req.headers['content-type'] || '';
    if (contentType.includes('multipart/form-data')) {
      const chunks: Buffer[] = [];
      req.on('data', (chunk: Buffer) => { chunks.push(chunk); });
      req.on('end', () => {
        const rawBody = Buffer.concat(chunks);
        const bodyStr = rawBody.toString('utf8', 0, Math.min(rawBody.length, 8192));

        // Check filename in Content-Disposition
        const filenameMatch = bodyStr.match(/filename="([^"]+)"/i) || bodyStr.match(/filename=([^\r\n;]+)/i);
        if (filenameMatch) {
          const filename = filenameMatch[1].trim().toLowerCase();
          const hasBlockedExt = BLOCKED_EXTENSIONS.some(ext => filename.endsWith(ext));
          if (hasBlockedExt) {
            log('warn', 'Blocked dangerous file upload', { filename });
            res.status(400).json({ success: false, error: { code: 'BLOCKED_FILE_TYPE', message: 'File type not allowed' } });
            return;
          }
        }

        // Check MIME type for executable types
        const mimeType = bodyStr.match(/Content-Type:\s*([^\r\n]+)/gi);
        if (mimeType) {
          const blockedMimes = [
            'application/x-msdownload', 'application/x-msdos-program',
            'application/x-executable', 'application/x-dosexec',
          ];
          for (const mt of mimeType) {
            const mimeValue = mt.replace(/Content-Type:\s*/i, '').trim().toLowerCase();
            if (blockedMimes.includes(mimeValue)) {
              log('warn', 'Blocked dangerous MIME type upload', { mimeType: mimeValue });
              res.status(400).json({ success: false, error: { code: 'BLOCKED_MIME_TYPE', message: 'File type not allowed' } });
              return;
            }
          }
        }

        // Forward the request to originate service
        const originateUrl = services.originate?.url || 'http://localhost:6000';
        const http = originateUrl.startsWith('https') ? require('https') : require('http');
        const url = new URL(`${originateUrl}/api/documents/upload`);
        const forwardHeaders: Record<string, string> = {};
        for (const [key, value] of Object.entries(req.headers)) {
          if (value && typeof value === 'string') forwardHeaders[key] = value;
        }
        forwardHeaders['content-length'] = String(rawBody.length);

        const proxyReq = http.request(
          { hostname: url.hostname, port: url.port, path: url.pathname, method: 'POST', headers: forwardHeaders },
          (proxyRes: any) => {
            res.status(proxyRes.statusCode || 500);
            Object.entries(proxyRes.headers).forEach(([k, v]) => { if (v) res.setHeader(k, v as string); });
            proxyRes.pipe(res);
          },
        );
        proxyReq.on('error', (err: Error) => {
          log('error', 'Failed to forward upload to originate', { error: err.message });
          res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Upload service unavailable' } });
        });
        proxyReq.write(rawBody);
        proxyReq.end();
      });
    } else {
      next();
    }
  });

  // =========================================================================
  // DOCUMENT / ORIGINATE SERVICE ROUTES
  // =========================================================================

  // KS-87: GET /api/documents/:id/sig-json is the public out-of-band signature
  // envelope used by offline verifiers — it must skip auth + scope checks. Must
  // be registered BEFORE the auth-gated `router.use('/api/documents', ...)`
  // below so Express resolves this specific path first; any other path falls
  // through to the auth-required catch-all. (Originate mirrors this with
  // publicDocumentsRouter mounted before documentsRouter.)
  router.get('/api/documents/:id/sig-json',
    proxy('originate', { '^/api/documents': '/api/documents' }),
  );

  router.use('/api/documents',
    authenticateToken(true),
    attachScopes,
    requireScope('documents:read', 'documents:write'),
    proxy('originate', { '^/api/documents': '/api/documents' }),
  );

  router.use('/api/certifications',
    authenticateToken(false),
    attachScopes,
    requireScope('certifications:read', 'certifications:write'),
    proxy('originate', { '^/api/certifications': '/api/certifications' }),
  );

  // Metering / usage — partner-facing, tenant-scoped read API over charge_events
  // (KS-320, Option 2). JWT-required (mirrors the billing customer endpoints'
  // auth); the tenant is enforced server-side in originate, so a partner caller
  // (Platform-S) only ever sees its own tenant's usage.
  router.use('/api/metering',
    authenticateToken(true),
    proxy('originate', { '^/api/metering': '/api/metering' }),
  );

  // Verification — proxy to originate (no auth required for public verification)
  router.use('/api/verification',
    proxy('originate', { '^/api/verification': '/api/verification' }),
  );
  // KS-584 P3: v2 verify-list contract — same public posture as v1 above.
  // ABSENT bearer → anonymous 200; PRESENT-but-invalid → originate 401s.
  router.use('/api/v2/verification',
    proxy('originate', { '^/api/v2/verification': '/api/v2/verification' }),
  );

  // Signatories — proxy to originate, relaying status verbatim. Audit A-09:
  // the previous shim swallowed ANY non-OK upstream (including 401/403/500)
  // and returned a fake success with an empty list — masking auth failures
  // and other real errors.
  router.get('/api/signatories',
    authenticateToken(true),
    (async (req: Request, res: Response) => {
      try {
        const originateUrl = services.originate?.url || 'http://originate:4000';
        const qs = req.url.includes('?') ? req.url.slice(req.url.indexOf('?')) : '';
        const upstream = await fetch(`${originateUrl}/api/signatories${qs}`, {
          headers: { 'Authorization': req.headers.authorization || '' },
        });
        const body = await upstream.json().catch(() => ({}));
        return res.status(upstream.status).json(body);
      } catch (err) {
        // Originate genuinely unreachable.
        return res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Originate service unreachable' } });
      }
    }) as RequestHandler,
  );

  // Third-party verifiers — require auth at the gateway. Audit A-09 fix at
  // originate (commit a88c9394b) returns 401 when the route is unauthenticated;
  // the previous shim here swallowed that 401 and returned a fake-success
  // empty list, masking the auth requirement. Now: gateway enforces auth
  // first, and any non-OK upstream response is relayed verbatim instead of
  // hidden behind a fake success.
  router.get('/api/third-party-verifiers',
    authenticateToken(true),
    (async (_req: Request, res: Response) => {
      try {
        const originateUrl = services.originate?.url || 'http://originate:4000';
        const upstream = await fetch(`${originateUrl}/api/third-party-verifiers`, {
          headers: { 'Authorization': _req.headers.authorization || '' },
        });
        const body = await upstream.json().catch(() => ({}));
        return res.status(upstream.status).json(body);
      } catch (err) {
        // Originate genuinely unreachable (network error, not an HTTP status).
        return res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Originate service unreachable' } });
      }
    }) as RequestHandler,
  );

  // =========================================================================
  // GDPR ERASURE — KS-843 (Kam's ruling, 2026-09-03)
  // =========================================================================
  // Both erasure routes — the write and the status read — are scope-gated on
  // `subjects:erase`. The gate is registered BEFORE the catch-all
  // `router.use('/api/gdpr', …)` below, because a gate mounted after it is
  // unreachable while looking exactly like a gate.
  //
  // It is an express Router mounted at `/erasures`, fed the
  // SEPARATOR-COLLAPSED sub-path — see `erasureDoor` below for why an exact
  // route and then a hand-rolled matcher were each walked around.
  //
  // BOTH routes, not just the write. The GET discloses whether an erasure
  // exists for a given external reference and what state it is in — that is
  // information about a named person's erasure request, and the same caller
  // class uses both. Gating only the write would leave any connector key able
  // to enumerate erasure status by external reference.
  //
  // Gated with `requireScopeOrRole`, not `requireScope`: every connector key
  // issued before the scope existed lacks it, and K cannot add a scope to an
  // existing key (create / list / revoke / validate only — no PATCH). With
  // `SUBJECTS_ERASE_SCOPE_ENFORCED` unset (the default) a role-only caller is
  // still admitted and logged, so this ships without breaking Platform S; the
  // flag is flipped once the log shows S on a rotated key.
  const ERASURE_GRACE_ROLES = ['connector'] as const;
  const ERASURE_SCOPE = 'subjects:erase';
  const ERASURE_ENFORCE_FLAG = 'SUBJECTS_ERASE_SCOPE_ENFORCED';

  /**
   * The erasure door.
   *
   * KS-843 F-7 — the FIRST hole. The original gate was two exact routes,
   * `router.post('/api/gdpr/erasures')` and
   * `router.get('/api/gdpr/erasures/:externalRef')`, sitting above the
   * catch-all mount below. `POST /api/gdpr//erasures` matched NEITHER, fell
   * through to the catch-all, and reached the real upstream handler with no
   * gate and no log — a 200 for a principal that got 403 on the same route
   * spelled with one slash. Measured, six shapes, driven against a real
   * express router:
   *
   *   spelling                    prefix mount   collapsed handoff
   *   /api/gdpr/erasures          HIT            HIT
   *   /api/gdpr//erasures         MISS           HIT
   *   /api/gdpr///erasures        MISS           HIT
   *   /api/gdpr/erasures/abc      HIT            HIT
   *   /api/gdpr//erasures/abc     MISS           HIT
   *   /api/gdpr/erasures//abc     HIT            HIT
   *
   * — so mounting on the `/api/gdpr/erasures` PREFIX alone, the obvious fix,
   * closes only three of the six.
   *
   * KS-843 F-9 — the SECOND hole, which the fix for the first one created.
   * Round 2 closed those six with a hand-rolled matcher tested against the
   * collapsed sub-path. That matcher was case-SENSITIVE, while both express
   * routers in the request path match case-INSENSITIVELY (neither this service
   * nor originate sets `case sensitive routing`). So `ERASURES`, `Erasures`,
   * `Erasures/`, `//ERASURES`, `/API/GDPR/ERASURES` and `GET …/ERASURES/abc`
   * walked around the door and ran originate's erasure handler in ENFORCING
   * mode for a principal with neither the scope nor an accepted role — five of
   * which the PARENT commit had refused. Two matchers inside one request path,
   * two answers, one upstream.
   *
   * So the door does not do its own matching any more. `erasureDoor` is an
   * express Router mounted at `/erasures`, and express decides — which means
   * case, trailing slash and the mount's own separator handling are whatever
   * express does everywhere else in this file, and cannot drift from it again.
   * The one normalisation express will NOT do is collapsing repeated
   * separators, so the sub-path is collapsed before it is handed on; that, and
   * only that, is what closes the six shapes in the table above.
   *
   * `req.url` is restored before the request continues. A gateway that
   * silently forwards a normalised copy of what it was sent hides what it
   * forwarded, and the grace log — which records `req.originalUrl` — would
   * then disagree with the upstream about what the caller actually typed.
   *
   * DELIBERATELY NOT gateway-wide path normalisation. That would close the
   * whole class — `POST /api/anchors//batch` walks around `anchors:write` the
   * same way — but it changes the routing of every endpoint at once. The class
   * has its own ticket (KS-858); this change is scoped to the door the ticket
   * is about. The class-forward lesson recorded there: a fix that
   * re-implements path matching inherits every normalisation express already
   * does — case, trailing slash, and the mount's own separator handling.
   */
  const erasureDoor = Router();
  erasureDoor.use(
    '/erasures',
    authenticateToken(true),
    attachScopes,
    requireScopeOrRole(ERASURE_SCOPE, ERASURE_GRACE_ROLES, ERASURE_ENFORCE_FLAG),
  );

  // KS-1187: the door used to collapse `//` across the WHOLE req.url, so an
  // absolute-form target (`http://h/erasures` inside this mount) became
  // `http:/h/erasures`, the `/erasures` mount never matched, and the catch-all
  // below forwarded it. The path is now judged canonically (erasureDoorVerdict)
  // with the same case rule as the door's router. The door is handed the
  // canonical path, and anything that cannot be canonicalised is refused.
  const erasureDoorCaseSensitive = Boolean((erasureDoor as unknown as { caseSensitive?: boolean }).caseSensitive);
  router.use('/api/gdpr', (req: Request, res: Response, next: NextFunction) => {
    const original = req.url;
    const { verdict, canonicalPath } = erasureDoorVerdict(collapseRepeatedSlashes(original), erasureDoorCaseSensitive);
    if (verdict === 'not-door') {
      next();
      return;
    }
    if (verdict === 'undetermined') {
      res.status(400).json({
        success: false,
        error: { code: 'NON_CANONICAL_PATH', message: 'The request path cannot be canonicalised' },
      });
      return;
    }
    req.url = canonicalPath as string;
    erasureDoor(req, res, (err?: unknown) => {
      req.url = original;
      next(err as Error | undefined);
    });
  });

  router.use('/api/gdpr',
    authenticateToken(true),
    proxy('originate', { '^/api/gdpr': '/api/gdpr' }),
  );

  // =========================================================================
  // ANCHORING
  // =========================================================================

  // KS-480: the flat anchor + batch writes are scope-gated `anchors:write`
  // for machine callers (sk_ keys / OAuth apps) — resolving the S↔K contract's
  // open question on which scope gates S's fallback anchor path. Human JWT
  // callers are unaffected (requireScope short-circuits authMethod jwt/email).
  // Registered before the catch-all mount so Express matches the POSTs here.
  router.post('/api/anchors',
    authenticateToken(true),
    attachScopes,
    requireScope('anchors:write'),
    proxy('anchoring', { '^/api/anchors': '/api/anchors' }),
  );
  router.post('/api/anchors/batch',
    authenticateToken(true),
    attachScopes,
    requireScope('anchors:write'),
    proxy('anchoring', { '^/api/anchors': '/api/anchors' }),
  );

  router.use('/api/anchors',
    authenticateToken(true),
    proxy('anchoring', { '^/api/anchors': '/api/anchors' }),
  );

  router.use('/api/anchoring',
    authenticateToken(true),
    proxy('anchoring', { '^/api/anchoring': '/api/anchoring' }),
  );

  // =========================================================================
  // WALLET
  // =========================================================================

  router.use('/api/wallets',
    authenticateToken(true),
    proxy('wallet', { '^/api/wallets': '/api/wallets' }),
  );

  // KS-10: removed the dead `/api/wallet` (singular) mount. The
  // wallet-connector only ever served `/api/wallets/*`; the singular
  // prefix forwarded 1:1 and always 404'd at the connector. It was never
  // in the OpenAPI spec and nothing real calls it — clients use
  // `/api/wallets/*`. (An alias mount was tried but http-proxy-middleware's
  // pathRewrite runs on the post-router-mount-stripped path, so
  // `^/api/wallet → /api/wallets` never matched. Not worth the complexity
  // for a non-endpoint.)

  // =========================================================================
  // DID / PRISM
  // =========================================================================

  router.use('/api/did',
    authenticateToken(true),
    proxy('prism', { '^/api/did': '/api/did' }),
  );

  // =========================================================================
  // TIMESTAMPING
  // =========================================================================

  router.use('/api/timestamps',
    authenticateToken(true),
    proxy('timestamping', { '^/api/timestamps': '/api/timestamps' }),
  );

  // =========================================================================
  // M365
  // =========================================================================

  // M365 callback must bypass auth (Microsoft redirects here after OAuth consent)
  router.use('/api/m365/callback',
    proxy('m365', { '^/api/m365': '/api' }),
  );

  // KS-442: outlook/verify-hash is public by contract (spec `security: []`) —
  // the Outlook add-in verifies a document hash without a platform account.
  // Mounted before the authed /api/m365 block; POST only (same shape as the
  // callback bypass above). The m365 service applies the matching exemption.
  router.post('/api/m365/outlook/verify-hash',
    proxy('m365', { '^/api/m365': '/api' }),
  );

  router.use('/api/m365',
    authenticateToken(true),
    proxy('m365', { '^/api/m365': '/api' }),
  );

  // OneDrive routes — same m365 service
  router.use('/api/onedrive',
    authenticateToken(true),
    proxy('m365', { '^/api/onedrive': '/api/onedrive' }),
  );

  // Teams routes — same m365 service
  router.use('/api/teams',
    authenticateToken(true),
    proxy('m365', { '^/api/teams': '/api/teams' }),
  );

  // =========================================================================
  // VERIFIABLE CREDENTIALS
  // =========================================================================

  router.use('/api/credentials',
    authenticateToken(false),
    proxy('vcIssuer', { '^/api/credentials': '/api/credentials' }),
  );

  // KS-570: this mount carried NO auth middleware, so the gateway's
  // session-revocation check (middleware/auth.ts) never ran for it. vc-issuer
  // then falls back on @secuura/shared's authenticate(), which verifies the
  // RS256 signature and nothing else — so an anonymous caller got 401 (the
  // route LOOKED protected) while a revoked or suspended user's still-valid
  // token got 200 on credential-revocation writes. `true` (not `false`)
  // because the mount already 401s anonymous callers today, so it was never
  // intentionally public — proved by probe before the change.
  router.use('/api/status',
    authenticateToken(true),
    proxy('vcIssuer', { '^/api/status': '/api/status' }),
  );

  // KS-442: presentations/verify is public by contract (spec `security: []`) —
  // tokenless verification is the verifier story. Mounted before the authed
  // /api/presentations block; POST only. vc-issuer applies the matching
  // exemption (credentials/verify needs no gateway change: /api/credentials
  // is already authenticateToken(false), its 401 came from the service).
  router.post('/api/presentations/verify',
    proxy('vcIssuer', { '^/api/presentations': '/api/presentations' }),
  );

  router.use('/api/presentations',
    authenticateToken(true),
    proxy('vcIssuer', { '^/api/presentations': '/api/presentations' }),
  );

  // KS-476 (Kam, 2026-07-17): identity-credentials was spec'd + mounted in
  // vc-issuer (index.ts /api/identity-credentials) but the gateway never
  // proxied the prefix — both ops 404'd forever. Types is public by contract
  // (spec `security: []`), mounted before the authed block; the service does
  // NOT enforce auth on /issue, so the gateway gate here is the enforcement.
  router.get('/api/identity-credentials/types',
    proxy('vcIssuer', { '^/api/identity-credentials': '/api/identity-credentials' }),
  );

  router.use('/api/identity-credentials',
    authenticateToken(true),
    proxy('vcIssuer', { '^/api/identity-credentials': '/api/identity-credentials' }),
  );

  // =========================================================================
  // STAKING
  // =========================================================================
  //
  // The staking service mounts its routers at /api/stake, /api/rewards, and
  // /api/tiers (NOT /api/staking). The previous gateway proxy at /api/staking
  // → /api/staking pointed at a path the service never serves, causing every
  // staking call through the gateway to 404.
  //
  // /api/rewards is intentionally NOT routed here — that path is proxied to
  // the referral service below (referral's reward + leaderboard surface).
  // Staking's /api/rewards routes are gateway-shadowed by design. Direct hits
  // on the staking service port still work.
  //
  // /api/staking/* (legacy gateway path) is also kept as a thin shim that
  // strips the prefix → /api/stake/*, so old clients keep working during
  // the cutover.

  router.use('/api/stake',
    authenticateToken(true),
    proxy('staking', { '^/api/stake': '/api/stake' }),
  );

  router.use('/api/tiers',
    authenticateToken(true),
    proxy('staking', { '^/api/tiers': '/api/tiers' }),
  );

  router.use('/api/staking',
    authenticateToken(true),
    proxy('staking', { '^/api/staking': '/api/stake' }),
  );

  // =========================================================================
  // REFERRAL / MILESTONES / REWARDS / LEADERBOARD
  // =========================================================================

  router.use('/api/referrals',
    authenticateToken(false),
    proxy('referral', { '^/api/referrals': '/api/referrals' }),
  );

  router.use('/api/milestones',
    authenticateToken(true),
    proxy('referral', { '^/api/milestones': '/api/milestones' }),
  );

  router.use('/api/rewards',
    authenticateToken(true),
    proxy('referral', { '^/api/rewards': '/api/rewards' }),
  );

  // KS-570: same defect as /api/status above — no auth middleware, so a
  // revoked session read the whole /api/leaderboard subtree. `router.use`
  // covers the subtree, so every path under it inherited the gap, not just
  // the endpoints that happened to be listed on the ticket.
  router.use('/api/leaderboard',
    authenticateToken(true),
    proxy('referral', { '^/api/leaderboard': '/api/leaderboard' }),
  );

  // =========================================================================
  // TRANSFER / DELEGATION / WORKFLOW
  // =========================================================================

  router.use('/api/transfers',
    authenticateToken(true),
    proxy('transfer', { '^/api/transfers': '/api/transfers' }),
  );

  router.use('/api/delegations',
    authenticateToken(true),
    proxy('transfer', { '^/api/delegations': '/api/delegations' }),
  );

  // Workflow CRUD — handled directly (transfer service not deployed on Azure)
  const workflowAdminCheck = (req: Request, res: Response, next: NextFunction) => {
    const user = (req as any).user;
    const allowed = ['SYSTEM_ADMIN', 'system_admin', 'super_admin', 'SUPER_ADMIN', 'platform_admin', 'ORG_ADMIN', 'ISSUER_ADMIN', 'issuer_admin'];
    if (!user || !allowed.includes(user.role)) { res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin access required' } }); return; }
    next();
  };

  router.get('/api/workflows', authenticateToken(true), workflowAdminCheck, async (_req: Request, res: Response) => {
    const workflows = await redisService.getAllWorkflows();
    res.json({ success: true, data: { workflows } });
  });

  router.post('/api/workflows', authenticateToken(true), workflowAdminCheck, express.json(), async (req: Request, res: Response) => {
    const { name, description, type, steps } = req.body || {};
    if (!name) { res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Workflow name is required' } }); return; }
    const id = `wf-${Date.now()}`;
    const workflow = {
      id, name, description, type: type || 'approval',
      steps: (steps || []).map((s: any, i: number) => ({ ...s, id: `step-${Date.now()}-${i}`, order: i + 1 })),
      status: 'active', createdBy: (req as any).user?.userId,
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
    };
    await redisService.setWorkflow(id, workflow);
    res.status(201).json({ success: true, data: workflow });
  });

  router.get('/api/workflows/:id', authenticateToken(true), workflowAdminCheck, async (req: Request, res: Response) => {
    const wf = await redisService.getWorkflow(req.params.id);
    if (!wf) { res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Workflow not found' } }); return; }
    res.json({ success: true, data: wf });
  });

  router.delete('/api/workflows/:id', authenticateToken(true), workflowAdminCheck, async (req: Request, res: Response) => {
    await redisService.deleteWorkflow(req.params.id);
    res.json({ success: true, deleted: true });
  });

  // =========================================================================
  // KYC
  // =========================================================================

  router.use('/api/kyc',
    authenticateToken(true),
    proxy('kyc', { '^/api/kyc': '/api/kyc' }),
  );

  // =========================================================================
  // DAO GOVERNANCE
  // =========================================================================

  router.use('/api/governance',
    authenticateToken(false),
    proxy('governance', { '^/api/governance': '/api/governance' }),
  );

  // =========================================================================
  // NFT CERTIFICATES
  // =========================================================================

  // KS-39 #2: the NFT service is not deployed on dev (no `secuura-dev-nft`
  // container app) so any proxy attempt 502s after the connection refused.
  // Test-side expectation is "responds or 404" — i.e. anything < 500. Guard
  // the route so when `NFT_SERVICE_URL` is unset (default localhost in a
  // non-local env), we 404 early with a clear "not deployed in this env"
  // body rather than letting the proxy bubble a 502. Once an `nft`
  // container app is added to Bicep + `NFT_SERVICE_URL` is set, the guard
  // becomes a no-op and the real proxy takes over.
  router.use('/api/nft',
    authenticateToken(false),
    (req: Request, res: Response, next: NextFunction) => {
      const nftUrl = services.nft?.url || '';
      const looksLikeDefault = /^http:\/\/localhost(:\d+)?$/i.test(nftUrl) || /^http:\/\/nft:\d+$/i.test(nftUrl);
      // Only short-circuit when the env didn't explicitly set NFT_SERVICE_URL
      // (i.e. we're still on the localhost fallback) AND we're not on a
      // localhost host (where the dev container compose actually runs nft
      // locally).
      const isLocalhostCaller = req.hostname === 'localhost' || req.hostname.endsWith('.local');
      if (looksLikeDefault && !isLocalhostCaller) {
        res.status(404).json({
          success: false,
          error: {
            code: 'NOT_DEPLOYED',
            message: 'NFT certificate service is not deployed in this environment.',
            details: { service: 'nft' },
          },
        });
        return;
      }
      next();
    },
    proxy('nft', { '^/api/nft': '/api/nft' }),
  );

  // =========================================================================
  // SECURITY / ANALYTICS / DASHBOARD
  // =========================================================================

  router.use('/api/security',
    authenticateToken(true),
    proxy('security', { '^/api/security': '/api' }),
  );

  router.use('/api/analytics',
    authenticateToken(true),
    proxy('analytics', { '^/api/analytics': '/api/analytics' }),
  );

  router.use('/api/dashboard',
    authenticateToken(true),
    proxy('dashboard', { '^/api/dashboard': '/api/dashboard' }),
  );

  // =========================================================================
  // BILLING
  // =========================================================================

  router.use('/api/billing',
    authenticateToken(false),
    proxy('billing', { '^/api': '' }),
  );

  // Billing webhooks (no auth — Stripe signed, needs raw body)
  router.use('/webhooks/stripe',
    proxy('billing', { '^/webhooks': '/webhooks' }),
  );

  // =========================================================================
  // ORIGINATE SERVICE PROXY (admin pages, system-errors, GDPR)
  // =========================================================================

  router.use('/originate/',
    proxy('originate', { '^/originate': '' }),
  );

  // Admin API routes — enforce admin role
  const PROXY_ADMIN_ROLES = ['SYSTEM_ADMIN', 'system_admin', 'super_admin', 'SUPER_ADMIN', 'platform_admin', 'ORG_ADMIN'];
  const enforceAdminProxy: RequestHandler = (req, res, next) => {
    const user = req.user;
    if (!user || !PROXY_ADMIN_ROLES.includes(user.role)) {
      res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin access required' } });
      return;
    }
    next();
  };

  router.use('/api/admin/',
    authenticateToken(true),
    enforceAdminProxy,
    proxy('originate', { '^/api/admin': '/api/admin' }),
  );

  router.use('/api/system-errors',
    authenticateToken(true),
    proxy('originate', { '^/api/system-errors': '/api/system-errors' }),
  );

  // KS-11: /api/gdpr was registered twice — the live route is the earlier
  // mount (~line 477). This second copy was dead (Express keeps the first
  // matching `router.use`). Removed.

  // =========================================================================
  // ANALYTICS SERVICE PROXY (legacy /analytics/ path)
  // =========================================================================

  router.use('/analytics/',
    proxy('analytics', { '^/analytics': '' }),
  );

  // =========================================================================
  // MCP SERVER PROXY (package generation — admin only)
  // =========================================================================

  const MCP_SERVER_URL = process.env.MCP_SERVER_URL || 'http://mcp-server:4023';

  router.post('/api/mcp/generate-package',
    authenticateToken(),
    async (req: Request, res: Response) => {
      try {
        const r = await fetch(`${MCP_SERVER_URL}/generate-package`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(req.body),
        });
        if (!r.ok) {
          const err = await r.json().catch(() => ({ error: 'Package generation failed' }));
          res.status(r.status).json(err);
          return;
        }
        res.setHeader('Content-Type', 'application/zip');
        const disposition = r.headers.get('Content-Disposition');
        if (disposition) res.setHeader('Content-Disposition', disposition);
        const arrayBuf = await r.arrayBuffer();
        res.send(Buffer.from(arrayBuf));
      } catch {
        res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'MCP server unreachable' } });
      }
    },
  );

  return router;
}
