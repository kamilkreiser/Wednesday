/**
 * =============================================================================
 * Authentication Middleware
 * =============================================================================
 * Extracted from the API gateway monolith. Handles:
 * - JWT token verification
 * - Test token parsing (development/test only)
 * - API key validation via the Security Service
 * =============================================================================
 */

import { createHash } from 'crypto';
import { Request, Response, NextFunction, RequestHandler } from 'express';
import { isSessionActive, runWithTenantId } from '@secuura/shared';
import { verifyJwtRs256 } from '@secuura/shared/crypto/jwks';
import { getRedisClient } from '../services/redis';
import { enforceClientRateLimit } from './rateLimitEnforce';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface UserPayload {
  userId: string;
  email: string;
  role: string;
  organizationId?: string;
  verificationLevel: string;
  authMethod?: string;
  mfaEnabled?: boolean;
  // KS-257: session identifier minted by auth at login; present on interactive
  // JWTs (absent for API-key/connector + test tokens). Used to enforce session
  // revocation here, not just at the auth service.
  sessionId?: string;
  tenantId?: string;
  tenantSlug?: string;
  // KS-151: role-derived scopes carried on the JWT. Used downstream by
  // `isAllowedByRoleOrScope` so the gateway pass-through and the
  // downstream services see the same scope set.
  scopes?: string[];
  // KS-164: per-client rate-limit allowance, populated for machine callers
  // (API key / OAuth app) from the connector record so `enforceClientRateLimit`
  // can apply the per-key ceiling. Absent for interactive (human) users, who
  // are governed by the global limiter instead.
  connectorId?: string;
  rateLimit?: number;
  rateLimitWindow?: number;
  // KS-1195 (A5): the caller's OWN rate-limit bucket. An API key's validate
  // response carries no key id, and connectorId is null for admin-minted keys, so
  // `connectorId || userId` gave every such key the one userId
  // `connector:api-key`: one bucket across all tenants. The key itself is the
  // only per-key identity the gateway holds, so the bucket is a domain-separated
  // SHA-256 of it (never the raw key, and never equal to the stored key_hash).
  rateLimitBucket?: string;
}

export interface ConnectorMeta {
  connectorId: string;
  scopes: string[];
  organizationId: string;
  tenantId?: string;
  tenantSlug?: string;
  rateLimit: number;
  rateLimitWindow: number;
}

// ---------------------------------------------------------------------------
// Module-level configuration – call `configureAuth()` once at startup
// ---------------------------------------------------------------------------

let ENABLE_TEST_TOKENS = false;
let DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';
let SECURITY_SERVICE_URL = 'http://localhost:6008';
let AUTH_SERVICE_URL = 'http://localhost:6003';

export interface AuthConfig {
  enableTestTokens?: boolean;
  defaultTenantId?: string;
  securityServiceUrl?: string;
  authServiceUrl?: string;
}

/**
 * Initialise auth module configuration.
 * Must be called before any middleware runs.
 */
export function configureAuth(cfg: AuthConfig): void {
  if (cfg.enableTestTokens !== undefined) ENABLE_TEST_TOKENS = cfg.enableTestTokens;
  if (cfg.defaultTenantId !== undefined) DEFAULT_TENANT_ID = cfg.defaultTenantId;
  if (cfg.securityServiceUrl !== undefined) SECURITY_SERVICE_URL = cfg.securityServiceUrl;
  if (cfg.authServiceUrl !== undefined) AUTH_SERVICE_URL = cfg.authServiceUrl;
}

// KS-347: verify RS256 tokens with a public key resolved by the token's `kid`
// from auth's JWKS endpoint, falling back to the static JWT_PUBLIC_KEY. This
// lets an auth signing-key rotation (KS-326/346) be picked up WITHOUT redeploying
// the gateway, while remaining a strict superset of the previous static-key
// behaviour (JWKS unconfigured/unreachable → static key, exactly as before). The
// accepted algorithm set stays registry-pinned inside the shared verifier
// (no RS256->HS256 confusion / alg:none, KS-179/326); the gateway still holds
// only PUBLIC key material, never a signing secret. Async because the JWKS fetch
// is async — the only caller is the async authenticateToken middleware below.
export async function verifyRs256(token: string): Promise<UserPayload> {
  return (await verifyJwtRs256(token)) as unknown as UserPayload;
}

// ---------------------------------------------------------------------------
// Test token support (development / test environments only)
// ---------------------------------------------------------------------------

const TEST_TOKEN_PREFIX = 'test_token_';

/**
 * Parse a test token for E2E testing (development/test only).
 * Returns null when the token is not a valid test token or when test tokens
 * are disabled.
 */
export function parseTestToken(token: string): UserPayload | null {
  const env = process.env.NODE_ENV || '';
  if (!['development', 'test'].includes(env)) {
    return null;
  }
  // Require explicit opt-in for test tokens (security hardening)
  if (!ENABLE_TEST_TOKENS) {
    return null;
  }

  if (!token.startsWith(TEST_TOKEN_PREFIX)) {
    return null;
  }

  try {
    const base64Payload = token.slice(TEST_TOKEN_PREFIX.length);
    const payloadJson = Buffer.from(base64Payload, 'base64').toString('utf-8');
    const payload = JSON.parse(payloadJson);

    // Support both 'sub' and 'userId' fields for test tokens
    const userId = payload.sub || payload.userId;

    // Validate required fields
    if (!userId || !payload.role) {
      return null;
    }

    // Check expiration
    if (payload.exp && payload.exp < Date.now()) {
      return null;
    }

    return {
      userId,
      role: payload.role,
      email: payload.email || `test-${userId}@secuura.test`,
      organizationId: payload.organizationId || 'test-org',
      verificationLevel: payload.verificationLevel || 'BASIC',
      authMethod: payload.authMethod || payload.auth_method || 'email',
      mfaEnabled: payload.mfaEnabled || payload.mfa_enabled || false,
    };
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// API key validation (via Security Service)
// ---------------------------------------------------------------------------

export const apiKeyCache = new Map<string, { result: ConnectorMeta | null; expiresAt: number }>();

// ---------------------------------------------------------------------------
// KS-480: connector bearer exchange. Downstream services enforce Bearer-only
// authentication on /api/* (pen-test H2 — they deliberately do NOT trust
// gateway-forwarded x-user-* headers), so an sk_-authenticated request needs a
// real RS256 JWT to cross the second hop. The gateway exchanges the validated
// key for a short-lived connector JWT minted by auth and attaches it as the
// Authorization header. Cached per key well inside the token TTL; revocation
// therefore propagates within cache TTL + validate cache (≈ same order as the
// existing 60-s validate cache).
// ---------------------------------------------------------------------------
const CONNECTOR_BEARER_CACHE_MS = 8 * 60_000; // token TTL is 10 min at auth
export const connectorBearerCache = new Map<string, { token: string; expiresAt: number }>();

/**
 * Exchange a validated sk_ key for a short-lived connector JWT via auth.
 * Returns null (and logs) on failure — downstream Bearer-only services will
 * then 401 the request, which fails closed rather than open.
 */
export async function getConnectorBearer(key: string): Promise<string | null> {
  const cached = connectorBearerCache.get(key);
  if (cached && cached.expiresAt > Date.now()) return cached.token;

  try {
    const resp = await fetch(`${AUTH_SERVICE_URL}/internal/connector-token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ apiKey: key }),
    });
    if (!resp.ok) {
      console.error(`[gateway] connector-token exchange failed (${resp.status}) — downstream Bearer-only services will 401 this connector request`);
      return null;
    }
    const body = (await resp.json()) as { data?: { token?: string; expiresIn?: number } };
    const token = body?.data?.token;
    if (!token) return null;
    const ttlMs = Math.min(CONNECTOR_BEARER_CACHE_MS, ((body.data?.expiresIn ?? 600) - 120) * 1000);
    connectorBearerCache.set(key, { token, expiresAt: Date.now() + Math.max(ttlMs, 30_000) });
    return token;
  } catch (err) {
    console.error(`[gateway] connector-token exchange unreachable: ${(err as Error).message}`);
    return null;
  }
}

/**
 * Validate an API key by calling the Security Service.
 * Results are cached for 60 s (valid) / 30 s (invalid) to reduce latency.
 */
export async function validateApiKey(key: string): Promise<ConnectorMeta | null> {
  const cached = apiKeyCache.get(key);
  if (cached && cached.expiresAt > Date.now()) return cached.result;

  try {
    const resp = await fetch(`${SECURITY_SERVICE_URL}/api/keys/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key }),
    });
    if (!resp.ok) {
      apiKeyCache.set(key, { result: null, expiresAt: Date.now() + 30_000 });
      return null;
    }
    const body = (await resp.json()) as any;
    const data = body?.data ?? body;
    if (!data?.valid) {
      apiKeyCache.set(key, { result: null, expiresAt: Date.now() + 30_000 });
      return null;
    }
    const meta: ConnectorMeta = {
      connectorId: data.connectorId || '',
      scopes: data.scopes || [],
      organizationId: data.organizationId || '',
      tenantId: data.tenantId || '',
      tenantSlug: data.tenantSlug || '',
      rateLimit: data.rateLimit || 100,
      rateLimitWindow: data.rateLimitWindow || 60,
    };
    apiKeyCache.set(key, { result: meta, expiresAt: Date.now() + 60_000 });
    return meta;
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Express middleware factory
// ---------------------------------------------------------------------------

// KS-1195: the per-key limiter (KS-164/170/616) reads req.user, which only this
// middleware sets. It used to be app.use()d in index.ts ahead of every
// authenticateToken, so it never saw a user and never fired. It now runs as the
// continuation of each branch below that sets req.user, inside that branch's
// tenant context; it passes non-machine callers straight through.
const clientRateLimit = enforceClientRateLimit();

/**
 * Returns Express middleware that authenticates incoming requests via:
 * 1. `x-api-key` header (API key / connector authentication)
 * 2. `Authorization: Bearer <token>` header (JWT or test token)
 *
 * When `required` is true (default) unauthenticated requests receive 401.
 * When false the request proceeds without a user context.
 */
export function authenticateToken(required: boolean = true): RequestHandler {
  return async (req: Request, res: Response, next: NextFunction) => {
    // --- API key path ---
    const apiKey = req.headers['x-api-key'] as string | undefined;
    const presentedKey = Boolean(apiKey && apiKey.startsWith('sk_'));
    const meta = apiKey && presentedKey ? await validateApiKey(apiKey) : null;
    if (presentedKey && !meta && required) {
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } });
      return;
    }
    // KS-1207: a key that fails validation on an OPTIONAL mount falls through to
    // the Bearer path below instead of calling next(). It used to call next()
    // straight away, so any junk `sk_` header switched off the Bearer check and
    // with it the session-revocation check: a revoked session's JWT plus
    // `x-api-key: sk_x` was forwarded, and the upstreams (shared authenticate(),
    // signature only) accepted it. With no Bearer the request is still anonymous,
    // exactly as before.
    if (apiKey && meta) {
      const connectorUser: UserPayload = {
        userId: `connector:${meta.connectorId || 'api-key'}`,
        email: 'connector@secuura.io',
        role: 'connector',
        organizationId: meta.organizationId,
        verificationLevel: 'api_key',
        authMethod: 'api_key',
        // KS-164: carry the connector's per-key allowance onto req.user so
        // enforceClientRateLimit applies it. Without this the limiter saw no
        // rateLimit and API-key traffic bypassed the per-key ceiling entirely.
        connectorId: meta.connectorId,
        rateLimit: meta.rateLimit,
        rateLimitWindow: meta.rateLimitWindow,
        rateLimitBucket: `api_key:${createHash('sha256').update('secuura-rate-limit-bucket\0').update(apiKey).digest('hex')}`,
        // KS-480: the key's scopes must live on the principal — requireScope
        // reads user.scopes, and without this every scope-gated mount 403'd
        // sk_ callers with `granted: []` regardless of the key's actual grants.
        scopes: meta.scopes,
        tenantId: meta.tenantId || undefined,
        tenantSlug: meta.tenantSlug || undefined,
      };
      req.user = connectorUser;
      (req as any).connectorMeta = meta;
      // KS-480: exchange the key for a short-lived connector JWT so downstream
      // Bearer-only services (originate documents, anchoring — pen-test H2)
      // accept the proxied request. On exchange failure the header is left
      // unset and Bearer-only upstreams 401 (fail closed, loudly logged above).
      const connectorBearer = await getConnectorBearer(apiKey);
      if (connectorBearer) {
        req.headers.authorization = `Bearer ${connectorBearer}`;
      }
      req.headers['x-user-id'] = connectorUser.userId;
      req.headers['x-user-email'] = connectorUser.email;
      req.headers['x-user-role'] = 'connector';
      if (meta.organizationId) req.headers['x-organization-id'] = meta.organizationId;
      if (meta.tenantId) req.headers['x-tenant-id'] = meta.tenantId;
      if (meta.tenantSlug) req.headers['x-tenant-slug'] = meta.tenantSlug;
      req.headers['x-verification-level'] = 'api_key';
      // KS-458: the gateway is the trust boundary — seed the RLS tenant
      // context from the VERIFIED credential (never the inbound header) so
      // the gateway's own DB reads/writes satisfy fail-closed RLS.
      runWithTenantId(meta.tenantId, () => clientRateLimit(req, res, next));
      return;
    }

    // --- Bearer token path ---
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      if (required) {
        res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
        return;
      }
      next();
      return;
    }

    const token = authHeader.split(' ')[1];

    // Try test token first (no-ops outside dev/test)
    const testPayload = parseTestToken(token);
    if (testPayload) {
      req.user = testPayload;
      req.headers['x-user-id'] = testPayload.userId;
      req.headers['x-user-email'] = testPayload.email;
      req.headers['x-user-role'] = testPayload.role;
      if (testPayload.organizationId) {
        req.headers['x-organization-id'] = testPayload.organizationId;
      }
      req.headers['x-verification-level'] = testPayload.verificationLevel;
      // KS-458: seed the RLS tenant context from the verified test payload.
      runWithTenantId(testPayload.tenantId, () => clientRateLimit(req, res, next));
      return;
    }

    // Verify JWT
    try {
      // KS-184/347: RS256-only verification; key resolved by kid via JWKS with a
      // static-key fallback (see verifyRs256). Async for the JWKS fetch.
      const decoded = await verifyRs256(token);

      // KS-257: enforce session revocation for interactive JWT sessions. The
      // stateless verify above doesn't see logout / the KS-43 session cap /
      // breach revocation, so a revoked-session token kept passing here — and at
      // every header-trusting downstream service — until it expired (~1h). The
      // API-key/connector and test-token paths return earlier and carry no
      // sessionId, so this only gates interactive sessions. Fail OPEN if the
      // session store is unreachable so a Redis blip can't 401 all traffic.
      if (decoded.sessionId) {
        const active = await isSessionActive(decoded.sessionId, getRedisClient() ?? undefined);
        if (active === false) {
          res.status(401).json({ success: false, error: { code: 'SESSION_INVALIDATED', message: 'Session has been invalidated' } });
          return;
        }
        if (active === null) {
          console.warn('[gateway-auth] session-revocation check skipped — session store unreachable', { sessionId: decoded.sessionId });
        }
      }

      if (!decoded.tenantId) decoded.tenantId = DEFAULT_TENANT_ID;
      req.user = decoded;
      req.headers['x-user-id'] = decoded.userId;
      if (decoded.email) req.headers['x-user-email'] = decoded.email;
      req.headers['x-user-role'] = decoded.role;
      if (decoded.organizationId) {
        req.headers['x-organization-id'] = decoded.organizationId;
      }
      if (decoded.verificationLevel) req.headers['x-verification-level'] = decoded.verificationLevel;
      else delete req.headers['x-verification-level'];

      // Tenant context: super_admin can override via X-Tenant-Id header (admin portal tenant selector)
      const SUPER_ADMIN_ROLES = ['super_admin', 'SUPER_ADMIN', 'SYSTEM_ADMIN', 'platform_admin'];
      const tenantOverride = req.headers['x-tenant-override'] as string | undefined;
      if (tenantOverride && SUPER_ADMIN_ROLES.includes(decoded.role)) {
        req.headers['x-tenant-id'] = tenantOverride;
        // Clear slug — service will resolve from config
        req.headers['x-tenant-slug'] = '';
      } else {
        if (decoded.tenantId) req.headers['x-tenant-id'] = decoded.tenantId;
        if (decoded.tenantSlug) req.headers['x-tenant-slug'] = decoded.tenantSlug;
      }
      // KS-458: seed the RLS tenant context from the verified JWT (or the
      // super-admin override that was just written to x-tenant-id).
      runWithTenantId((req.headers['x-tenant-id'] as string | undefined) || decoded.tenantId, () => clientRateLimit(req, res, next));
    } catch (error) {
      if (required) {
        res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid or expired token' } });
        return;
      }
      next();
    }
  };
}

// qa1034 control: a develop auth.ts nobody pinned
