// =============================================================================
// SECUURA MIDDLEWARE
// =============================================================================
// Shared Express middleware for all services
// =============================================================================

import express from 'express';
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { verifyJwtRs256 } from '../crypto/jwks';
import { isPlatformRole } from '../security/keyRevokePolicy';
import { getRateLimitConfig } from '../config';
import { UnauthorizedError, ForbiddenError, RateLimitError, ValidationError } from '../errors';
import { logger, logRequest } from '../logger';
// KS-1724: the JSON body parser with structural caps (array length, node count, depth).
import { boundedJson } from './request-limits';
import { ZodSchema } from 'zod';
import Redis from 'ioredis';
// KS-1725: zod 4 issues rendered in zod 3.25.76's shape for every response (the client contract unchanged).
import { zod3Issues } from '../validation/zod3-compat';

// =============================================================================
// TYPE DEFINITIONS
// =============================================================================

export interface JwtPayload {
  userId: string;
  email: string;
  role: string;
  organizationId?: string;
  /**
   * KS-764 (Peter's #799 review, finding 3): DECLARED because a policy reads it.
   *
   * `decideTenantAccess` — which `decideKeyRevoke` delegates to — compares
   * `user.tenantId` against the target and returns `403 caller has no tenant`
   * when it is absent (`keyRevokePolicy.ts:175`). Until this line, no payload
   * type declared the field: the revoke routes worked only because the auth
   * service HAPPENS to sign it in, and `services/auth/src/services/jwt.ts:263`
   * signs it CONDITIONALLY — `...(meta.tenantId ? { tenantId } : {})` — so a
   * tenant-less user genuinely receives a token without the claim.
   *
   * The dependency was real, load-bearing and invisible to the compiler, which
   * is what made it undeclared rather than merely optional. Declaring it does
   * not change behaviour; it makes the contract checkable, so a future token
   * minter can see what the authorisation path requires.
   */
  tenantId?: string;
  verificationLevel: string;
  iat?: number;
  exp?: number;
}

export interface AuthenticatedRequest extends Request {
  user?: JwtPayload;
  requestId?: string;
}

// =============================================================================
// AUTHENTICATION MIDDLEWARE
// =============================================================================

// KS-347: verifier services that inherit this shared middleware verify RS256
// tokens with a public key resolved by the token's `kid` from auth's JWKS
// endpoint, falling back to the static JWT_PUBLIC_KEY. An auth signing-key
// rotation (KS-326/346) is therefore picked up WITHOUT redeploying the verifier,
// while remaining a strict superset of the previous static-key path (JWKS
// unconfigured/unreachable → static key, exactly as before). Verifiers still hold
// ONLY PUBLIC key material — never a signing secret — and the accepted algorithm
// set stays registry-pinned (no RS256->HS256 confusion / alg:none, KS-179/326)
// inside the shared verifier. Async because the JWKS fetch is async; the only
// caller is the async authenticate() middleware below.
async function verifyRs256(token: string): Promise<JwtPayload> {
  return (await verifyJwtRs256(token)) as unknown as JwtPayload;
}

/**
 * Verify JWT token and attach user to request.
 *
 * `publicOps` (KS-442) exempts exact operations from a blanket
 * `app.use('/api', authenticate())` mount without moving their handlers:
 * entries are `"METHOD /path"` strings matched against the request path
 * RELATIVE to the mount point (Express strips the mount prefix from
 * `req.path` inside a mounted middleware). The published OpenAPI spec marks
 * the same operations `security: []` — spec and runtime stay in lockstep.
 * A valid bearer token on an exempt op is still verified and attached
 * (callers may personalise), but an absent/invalid one no longer 401s.
 */
export function authenticate(
  options: { required?: boolean; publicOps?: readonly string[] } = {},
) {
  // Normalise once at mount time, not per request. `required` defaults to
  // true whenever omitted (an absent key must never silently disable auth).
  const required = options.required ?? true;
  const publicOps = new Set((options.publicOps ?? []).map(op => op.replace(/\/+$/, '')));
  return async (req: AuthenticatedRequest, _res: Response, next: NextFunction) => {
    try {
      const authHeader = req.headers.authorization;
      // Exempt op (trailing slashes ignored): fall through to the handler.
      // Guard req.path — non-Express callers (tests, bare handlers) may omit it.
      const isPublicOp =
        publicOps.size > 0 &&
        typeof req.path === 'string' &&
        publicOps.has(`${req.method} ${req.path.replace(/\/+$/, '')}`);

      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        if (required && !isPublicOp) {
          throw new UnauthorizedError('No token provided');
        }
        return next();
      }
      // A malformed/expired token on a public op must not block verification:
      // verify best-effort and continue anonymous on failure.
      if (isPublicOp) {
        try {
          req.user = await verifyRs256(authHeader.split(' ')[1]);
        } catch {
          // Anonymous access is the contract for public ops.
        }
        return next();
      }
      
      const token = authHeader.split(' ')[1];
      // KS-184/347: RS256-only verification; key resolved by kid via JWKS with a
      // static-key fallback (see verifyRs256). Async for the JWKS fetch.
      const decoded = await verifyRs256(token);
      req.user = decoded;
      
      next();
    } catch (error) {
      if (error instanceof jwt.JsonWebTokenError) {
        return next(new UnauthorizedError('Invalid token'));
      }
      if (error instanceof jwt.TokenExpiredError) {
        return next(new UnauthorizedError('Token expired'));
      }
      next(error);
    }
  };
}

/**
 * Check if user has required role
 */
export function requireRole(...allowedRoles: string[]) {
  return (req: AuthenticatedRequest, _res: Response, next: NextFunction) => {
    if (!req.user) {
      return next(new UnauthorizedError('Authentication required'));
    }
    
    if (!allowedRoles.includes(req.user.role)) {
      return next(new ForbiddenError(`Role ${req.user.role} is not authorized for this action`));
    }
    
    next();
  };
}

/**
 * KS-1536 (Kam, card secuura-ks-1536-platform-admin-role-one-list-1106, option a, "One shared list without platform_admin, after a check"): requireRole with the one platform list, so a service
 * needing this gate does not re-declare it. Same errors as requireRole. Added for tokenisation's two key routes.
 */
export function requirePlatformRole() {
  return (req: AuthenticatedRequest, _res: Response, next: NextFunction) => {
    if (!req.user) {
      return next(new UnauthorizedError('Authentication required'));
    }

    if (!isPlatformRole(req.user.role)) {
      return next(new ForbiddenError(`Role ${req.user.role} is not authorized for this action`));
    }

    next();
  };
}

/**
 * Check if user has required verification level (static check).
 * For policy-engine-aware enforcement, use requirePolicy() instead.
 */
const verificationLevels = ['NONE', 'BASIC', 'SOCIAL', 'STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT'];

export function requireVerificationLevel(minLevel: string) {
  return (req: AuthenticatedRequest, _res: Response, next: NextFunction) => {
    if (!req.user) {
      return next(new UnauthorizedError('Authentication required'));
    }
    
    const userLevelIndex = verificationLevels.indexOf(req.user.verificationLevel);
    const requiredLevelIndex = verificationLevels.indexOf(minLevel);
    
    if (userLevelIndex < requiredLevelIndex) {
      return next(new ForbiddenError(
        `Verification level ${minLevel} required, current level is ${req.user.verificationLevel}`
      ));
    }
    
    next();
  };
}

/**
 * Policy-engine-aware enforcement middleware.
 * Evaluates the user (and optional org) against all active policies
 * for the given scope(s), then blocks, warns, or allows accordingly.
 */
export interface PolicyEngineDeps {
  evaluatePolicies: (
    user: { userId: string; verificationLevel: string; mfaEnabled: boolean; walletConnected: boolean; authProviders: string[]; region?: string },
    org: { orgId: string; trustLevel: string; verificationMode?: string; domain?: string; domainVerified: boolean } | null,
    policies: unknown[],
  ) => { status: string; policyId: string; policyName: string; violations: { field: string; required: string; actual: string; message: string }[]; upgradePath?: string[] };
  getEffectivePolicies: (scopes: { scope: string; scopeId: string }[]) => Promise<unknown[]>;
  logEnforcement: (entry: Record<string, unknown>) => Promise<void>;
}

export function requirePolicy(
  engine: PolicyEngineDeps,
  scopes: { scope: string; scopeId: string }[],
) {
  return async (req: AuthenticatedRequest, _res: Response, next: NextFunction) => {
    if (!req.user) {
      return next(new UnauthorizedError('Authentication required'));
    }

    try {
      const policies = await engine.getEffectivePolicies(scopes);
      if (!policies || policies.length === 0) {
        return next();
      }

      const userIdentity = {
        userId: req.user.userId,
        verificationLevel: req.user.verificationLevel || 'NONE',
        mfaEnabled: false,
        walletConnected: false,
        authProviders: [] as string[],
        region: (req.headers['x-user-region'] as string) || undefined,
      };

      const orgIdentity = req.user.organizationId
        ? {
            orgId: req.user.organizationId,
            trustLevel: (req.headers['x-org-trust-level'] as string) || 'UNVERIFIED',
            domainVerified: false,
          }
        : null;

      const result = engine.evaluatePolicies(userIdentity, orgIdentity, policies);

      req.headers['x-policy-result'] = result.status;
      req.headers['x-policy-id'] = result.policyId;

      engine.logEnforcement({
        policyId: result.policyId,
        userId: req.user.userId,
        orgId: req.user.organizationId || null,
        action: `${req.method} ${req.path}`,
        result: result.status,
        userLevel: req.user.verificationLevel,
        requiredLevel: result.violations[0]?.required || req.user.verificationLevel,
        ipAddress: req.ip,
        userAgent: req.get('user-agent'),
      }).catch(() => {});

      if (result.status === 'blocked') {
        return next(new ForbiddenError(
          JSON.stringify({
            message: 'Verification requirements not met',
            policy: result.policyName,
            violations: result.violations,
            upgradePath: result.upgradePath,
          }),
        ));
      }

      next();
    } catch (error) {
      logger.warn('Policy evaluation failed, allowing request', { error });
      next();
    }
  };
}

// =============================================================================
// RATE LIMITING MIDDLEWARE
// =============================================================================

let redisClient: Redis | null = null;

export function setRedisClient(client: Redis) {
  redisClient = client;
}

/**
 * Rate limit requests per user/IP
 */
export function rateLimit(options: {
  windowMs?: number;
  maxRequests?: number;
  keyPrefix?: string;
} = {}) {
  const config = getRateLimitConfig();
  const windowMs = options.windowMs || config.windowMs;
  const maxRequests = options.maxRequests || config.maxRequests;
  const keyPrefix = options.keyPrefix || 'ratelimit';
  
  // In-memory fallback
  const memoryStore = new Map<string, { count: number; resetAt: number }>();
  
  return async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    const key = req.user?.userId || req.ip || 'anonymous';
    const fullKey = `${keyPrefix}:${key}`;
    
    try {
      if (redisClient) {
        // Redis-based rate limiting
        const current = await redisClient.incr(fullKey);
        
        if (current === 1) {
          await redisClient.pexpire(fullKey, windowMs);
        }
        
        const ttl = await redisClient.pttl(fullKey);
        
        res.setHeader('X-RateLimit-Limit', maxRequests);
        res.setHeader('X-RateLimit-Remaining', Math.max(0, maxRequests - current));
        res.setHeader('X-RateLimit-Reset', Math.ceil(Date.now() / 1000) + Math.ceil(ttl / 1000));
        
        if (current > maxRequests) {
          return next(new RateLimitError(Math.ceil(ttl / 1000)));
        }
      } else {
        // In-memory fallback
        const now = Date.now();
        const record = memoryStore.get(fullKey);
        
        if (!record || now > record.resetAt) {
          memoryStore.set(fullKey, { count: 1, resetAt: now + windowMs });
        } else {
          record.count++;
          if (record.count > maxRequests) {
            return next(new RateLimitError(Math.ceil((record.resetAt - now) / 1000)));
          }
        }
      }
      
      next();
    } catch (error) {
      logger.warn('Rate limit check failed, allowing request', { error });
      next();
    }
  };
}

// =============================================================================
// VALIDATION MIDDLEWARE
// =============================================================================

/**
 * Validate request body against Zod schema
 */
export function validateBody<T>(schema: ZodSchema<T>) {
  return (req: Request, _res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);

    if (!result.success) {
      return next(new ValidationError('Invalid request body', zod3Issues(result.error.issues)));
    }

    req.body = result.data;
    next();
  };
}

/**
 * Validate request query parameters
 */
export function validateQuery<T>(schema: ZodSchema<T>) {
  return (req: Request, _res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.query);

    if (!result.success) {
      return next(new ValidationError('Invalid query parameters', zod3Issues(result.error.issues)));
    }

    (req as unknown as Record<string, unknown>).validatedQuery = result.data;
    next();
  };
}

/**
 * Validate request params
 */
export function validateParams<T>(schema: ZodSchema<T>) {
  return (req: Request, _res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.params);

    if (!result.success) {
      return next(new ValidationError('Invalid URL parameters', zod3Issues(result.error.issues)));
    }

    (req as unknown as Record<string, unknown>).validatedParams = result.data;
    next();
  };
}

// =============================================================================
// REQUEST LOGGING MIDDLEWARE
// =============================================================================

/**
 * Log all incoming requests
 */
export function requestLogger() {
  return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    const start = Date.now();
    
    // Generate request ID
    req.requestId = `req_${require('crypto').randomUUID()}`;
    res.setHeader('X-Request-ID', req.requestId);
    
    res.on('finish', () => {
      const duration = Date.now() - start;
      logRequest({
        method: req.method,
        path: req.path,
        statusCode: res.statusCode,
        duration,
        userId: req.user?.userId,
        ipAddress: req.ip,
      });
    });
    
    next();
  };
}

// =============================================================================
// CORS MIDDLEWARE
// =============================================================================

/**
 * Custom CORS middleware
 */
export function cors(allowedOrigins: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    const origin = req.headers.origin;
    
    if (origin && allowedOrigins.includes(origin)) {
      res.setHeader('Access-Control-Allow-Origin', origin);
    }
    
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Request-ID');
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    res.setHeader('Access-Control-Max-Age', '86400');
    
    if (req.method === 'OPTIONS') {
      res.status(204).end();
      return;
    }
    
    next();
  };
}

// =============================================================================
// HEALTH CHECK MIDDLEWARE
// =============================================================================

export interface HealthCheckDependency {
  name: string;
  check: () => Promise<boolean>;
}

/**
 * Create health check endpoint handler
 */
export function healthCheck(dependencies: HealthCheckDependency[] = []) {
  return async (_req: Request, res: Response) => {
    const checks: Record<string, { status: string; latency?: number }> = {};
    let healthy = true;
    
    for (const dep of dependencies) {
      const start = Date.now();
      try {
        const ok = await dep.check();
        checks[dep.name] = {
          status: ok ? 'healthy' : 'unhealthy',
          latency: Date.now() - start,
        };
        if (!ok) healthy = false;
      } catch (error) {
        checks[dep.name] = {
          status: 'unhealthy',
          latency: Date.now() - start,
        };
        healthy = false;
      }
    }
    
    res.status(healthy ? 200 : 503).json({
      status: healthy ? 'healthy' : 'unhealthy',
      timestamp: new Date().toISOString(),
      checks,
    });
  };
}

// =============================================================================
// NUL-BYTE BODY GUARD (KS-471)
// =============================================================================

// The NUL character, built programmatically so no raw control byte or fragile
// escape literal lives in this source file.
const NUL_CHAR = String.fromCharCode(0);

/**
 * KS-471: walk a parsed JSON body and return the path of the first string
 * (value or object key) carrying a U+0000 NUL byte, or null when clean.
 *
 * Postgres text/varchar/jsonb cannot store U+0000 — the driver throws
 * `invalid byte sequence for encoding "UTF8"` and the write path surfaces a
 * raw 500. The per-field noNulBytes/pgSafeStringSchema primitives (KS-451)
 * only protect fields someone remembered to wire; this walker underpins the
 * request-level guard so EVERY field is covered.
 */
export function findNulBytePath(value: unknown, path = ''): string | null {
  if (typeof value === 'string') {
    return value.includes(NUL_CHAR) ? path || '(root)' : null;
  }
  if (Array.isArray(value)) {
    for (let i = 0; i < value.length; i++) {
      const hit = findNulBytePath(value[i], `${path}[${i}]`);
      if (hit) return hit;
    }
    return null;
  }
  if (value && typeof value === 'object') {
    for (const [k, v] of Object.entries(value)) {
      const keyPath = path ? `${path}.${k}` : k;
      if (k.includes(NUL_CHAR)) return `${keyPath} (key)`;
      const hit = findNulBytePath(v, keyPath);
      if (hit) return hit;
    }
    return null;
  }
  return null;
}

// =============================================================================
// CONTROL-BYTE BODY GUARD (KS-472, generalising the KS-471 NUL guard)
// =============================================================================

// Disallowed control bytes: the C0 range U+0000–U+001F EXCEPT the
// structurally-legal whitespace \t (U+0009), \n (U+000A), \r (U+000D) —
// legitimate in multi-line free text — plus DEL (U+007F). Matches the
// systemTest `control_byte_acceptance_guard` definition exactly
// (systemTest/schemathesis/config/checks.py `_is_control_char`), so the
// platform rejects precisely what the sweep probes for. Built without raw
// control bytes in source.
const CONTROL_BYTE_RE = new RegExp('[\\u0000-\\u0008\\u000B\\u000C\\u000E-\\u001F\\u007F]');

/** Human-readable name for a disallowed control byte (message building). */
function describeControlByte(ch: string): string {
  const cp = ch.charCodeAt(0);
  const hex = cp.toString(16).toUpperCase().padStart(4, '0');
  return cp === 0 ? `a NUL (U+0000) byte` : `control byte U+${hex}`;
}

/**
 * KS-472: walk a parsed JSON body and return the path + offending character
 * of the first string (value or object key) carrying a disallowed control
 * byte, or null when clean. The broader sibling of {@link findNulBytePath}
 * (kept for API compatibility) — NUL crashes the Postgres driver (KS-471),
 * while the other C0 bytes were silently accepted AND persisted, round-
 * tripping back out of the API (the KS-472 finding: invisible to every
 * sweep check until the control_byte_acceptance_guard hard gate).
 */
export function findControlBytePath(value: unknown, path = ''): { path: string; char: string } | null {
  if (typeof value === 'string') {
    const m = CONTROL_BYTE_RE.exec(value);
    return m ? { path: path || '(root)', char: m[0] } : null;
  }
  if (Array.isArray(value)) {
    for (let i = 0; i < value.length; i++) {
      const hit = findControlBytePath(value[i], `${path}[${i}]`);
      if (hit) return hit;
    }
    return null;
  }
  if (value && typeof value === 'object') {
    for (const [k, v] of Object.entries(value)) {
      const keyPath = path ? `${path}.${k}` : k;
      const keyHit = CONTROL_BYTE_RE.exec(k);
      if (keyHit) return { path: `${keyPath} (key)`, char: keyHit[0] };
      const hit = findControlBytePath(v, keyPath);
      if (hit) return hit;
    }
    return null;
  }
  return null;
}

/**
 * KS-471 + KS-472: request-level control-byte guard — mount AFTER EVERY body
 * parser, not after `express.json()` alone.
 *
 * ⚠ KS-781 P3-3. This comment used to read "mount immediately after
 * `express.json()`", and five services followed it literally, landing the guard
 * BETWEEN `express.json()` and `express.urlencoded()`. It inspects `req.body`;
 * on a form-encoded request `express.json()` leaves `req.body` as `{}` and
 * skips parsing, so the guard walked an empty object and the form body was
 * parsed after it. Measured: the same NUL was a 400 as JSON and a 200 as a
 * form. Mounting after every parser is a no-op when `req.body` is unset, so
 * "last" is always safe and "immediately after json" is not.
 * Enforced by `__tests__/ks781-p3-3-body-parser-order.test.ts`.
 *
 * Rejects any request whose parsed body contains a disallowed control byte
 * (C0 minus \t \n \r, plus DEL) in any string value or object key with an
 * honest `400 VALIDATION_ERROR` naming the path, instead of either 500ing at
 * the Postgres driver (the NUL case, KS-431 -> KS-438 -> KS-451 -> KS-471)
 * or silently accepting AND persisting the byte (the KS-472 case — verified
 * round-tripping back out of the API on 30 write ops). Base64/hex payloads
 * cannot contain these bytes by charset, so no legitimate field class is
 * affected; \t and \n survive for multi-line text.
 *
 * Responds directly (no reliance on a downstream error handler) with the
 * platform's standard error envelope. Skips non-JSON/empty bodies.
 */
export function rejectControlBytes() {
  return (req: Request, res: Response, next: NextFunction) => {
    if (req.body !== undefined && req.body !== null) {
      const hit = findControlBytePath(req.body);
      if (hit) {
        const message = `Must not contain ${describeControlByte(hit.char)}`;
        res.status(400).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message,
            details: [{ path: hit.path, message }],
          },
        });
        return;
      }
    }
    next();
  };
}

/**
 * KS-800: mount the body parsers AND the control-byte guard in the one order
 * that works, so no service has to remember it.
 *
 * The order is load-bearing and the failure is silent. `rejectControlBytes()`
 * inspects `req.body`; mounted between `express.json()` and
 * `express.urlencoded()` it walks `{}` on every form request and passes
 * everything. Five services shipped exactly that, and the same NUL byte was
 * 400 as JSON and 200 as a form — on `/api/oauth/authorize` it reached the
 * authorization-code minter (KS-781 P3-3).
 *
 * The doc comment on the guard used to say "mount immediately after
 * `express.json()`", which TOLD people to get it wrong. A per-service
 * convention is the class of guard that eventually fails; this is the fix that
 * removes the convention.
 *
 * @param app - the express application
 * @param opts.limit - body size limit passed to both parsers (default '1mb')
 * @param opts.urlencoded - mount `express.urlencoded` too (default true)
 * @param opts.service - KS-1724: the service name on the structural cap's refusal log line (default 'secuura')
 *
 * @example
 * const app = express();
 * mountBodyParsers(app);   // json + urlencoded + guard, correctly ordered
 */
export function mountBodyParsers(
  app: { use: (...handlers: unknown[]) => unknown },
  opts: { limit?: string; urlencoded?: boolean; service?: string } = {},
): void {
  const limit = opts.limit ?? '1mb';
  // KS-1724: was `express.json({ limit })`; now the same parser with the structural caps (boundedJson, request-limits.ts).
  app.use(boundedJson({ service: opts.service ?? 'secuura', limit }));
  if (opts.urlencoded !== false) {
    app.use(express.urlencoded({ extended: true, limit }));
  }
  // LAST, and this line is the whole point of the helper.
  app.use(rejectControlBytes());
}

/**
 * KS-471 compatibility export — the guard every service already mounts.
 * Since KS-472 it rejects the full disallowed control-byte class (not just
 * NUL), so all 20 shared-consuming services pick the wider guard up on
 * rebuild with zero call-site changes. Prefer {@link rejectControlBytes} in
 * new code.
 */
export function rejectNulBytes() {
  return rejectControlBytes();
}

// KS-1724: the JSON body parser with structural caps, re-exported so services reach it
// through the package root (src/index.ts) exactly as they reach mountBodyParsers.
export {
  boundedJson,
  findStructuralBreach,
  STRUCTURAL_JSON_DEFAULTS,
  STRUCTURAL_JSON_ENV,
  type BoundedJsonOptions,
  type StructuralJsonCaps,
  type StructuralBreach,
} from './request-limits';
