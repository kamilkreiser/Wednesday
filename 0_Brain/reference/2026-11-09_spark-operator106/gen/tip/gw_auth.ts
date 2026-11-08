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
import { isPlatformRole, isSessionActive, runWithTenantId } from '@secuura/shared';
import { verifyJwtRs256 } from '@secuura/shared/crypto/jwks';
import { getRedisClient } from '../services/redis';
import { enforceClientRateLimit, recordApiKeyBucket } from './rateLimitEnforce';
import { logger } from '../utils/logger';

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
  // KS-1198: set only on the connector JWTs the auth service mints from a validated API key
  // (`type: 'connector'`). The gateway forwards one upstream; it never accepts one as a Bearer credential.
  type?: string;
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

// KS-1240: both front-door calls (key validation at security, the connector exchange at auth) sit on the path of every
// request that presents an `sk_` key, and neither carried a timeout: an upstream that never answered, or answered the
// headers and stalled the body, held the request open with no bound. 5 s each, the bound the gateway's own health probes
// already give the same internal services (services/health.ts, routes/system-status.ts, routes/health-dashboard.ts). A
// signal on the fetch also bounds the body read that follows it (measured on Node 26.8.1: a stall mid-body rejects
// `json()` with the same TimeoutError as a hang before the headers).
const KEY_VALIDATE_TIMEOUT_MS = 5_000;
const CONNECTOR_EXCHANGE_TIMEOUT_MS = 5_000;

/** True for the rejection our own timeout signal produces (`TimeoutError`; `AbortError` from a plain abort). Never throws. */
function isTimeout(err: unknown): boolean {
  try {
    const name = (err as { name?: unknown } | null)?.name;
    return name === 'TimeoutError' || name === 'AbortError';
  } catch {
    return false;
  }
}

/**
 * KS-1240: what a key check found. `rejected` is the security service saying the key is not valid; `unavailable` is
 * the check not completing (no answer in time, a stalled or unparseable body, a 5xx, 408 or 429). Only `valid` and
 * `rejected` are cached; the front door answers `unavailable` with 503, never with 401.
 */
export type ApiKeyCheck =
  | { outcome: 'valid'; meta: ConnectorMeta }
  | { outcome: 'rejected' }
  | { outcome: 'unavailable'; reason: string };

/** A status that says the security service could not answer the question, as opposed to answering "not valid". */
function couldNotAnswer(status: number): boolean {
  return status >= 500 || status === 408 || status === 429;
}

function unavailable(reason: string): ApiKeyCheck {
  // The key is never logged; the reason names only what failed.
  logger.warn('[gateway-auth] API key validation could not complete; the request is answered 503, and nothing is cached', {
    type: 'security',
    event: 'API_KEY_VALIDATION_UNAVAILABLE',
    reason,
  });
  return { outcome: 'unavailable', reason };
}

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
      signal: AbortSignal.timeout(CONNECTOR_EXCHANGE_TIMEOUT_MS),
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
    // KS-1240: still fail closed (no Bearer, so a Bearer-only upstream refuses the request), but say which failure it was.
    if (isTimeout(err)) {
      console.error(`[gateway] connector-token exchange timed out after ${CONNECTOR_EXCHANGE_TIMEOUT_MS} ms — downstream Bearer-only services will 401 this connector request`);
    } else {
      console.error(`[gateway] connector-token exchange unreachable: ${(err as Error).message}`);
    }
    return null;
  }
}

/**
 * Validate an API key by calling the Security Service.
 * Returns the key's metadata, or null when the key is not valid OR could not be checked. Kept for its callers;
 * `authenticateToken` uses `checkApiKey`, which tells those two apart (KS-1240).
 */
export async function validateApiKey(key: string): Promise<ConnectorMeta | null> {
  const check = await checkApiKey(key);
  return check.outcome === 'valid' ? check.meta : null;
}

/**
 * Check an API key at the Security Service. Results are cached for 60 s (valid) / 30 s (rejected) to reduce latency;
 * a check that could not complete is never cached (KS-1240), so the key is asked about again on the next request.
 */
export async function checkApiKey(key: string): Promise<ApiKeyCheck> {
  const cached = apiKeyCache.get(key);
  if (cached && cached.expiresAt > Date.now()) return cached.result ? { outcome: 'valid', meta: cached.result } : { outcome: 'rejected' };

  let body: any;
  try {
    const resp = await fetch(`${SECURITY_SERVICE_URL}/api/keys/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key }),
      signal: AbortSignal.timeout(KEY_VALIDATE_TIMEOUT_MS),
    });
    if (!resp.ok) {
      // KS-1240: the security service answers 503 'Unable to verify key' when it cannot read the key's stored state
      // (security/src/index.ts, Kam's ruling on card secuura-ks1370-validate-when-the-revoke-check-cannot-read (a)).
      // That is not a rejection, so it is neither cached nor answered as one.
      if (couldNotAnswer(resp.status)) return unavailable(`security service answered ${resp.status}`);
      apiKeyCache.set(key, { result: null, expiresAt: Date.now() + 30_000 });
      return { outcome: 'rejected' };
    }
    body = await resp.json();
  } catch (err) {
    return unavailable(isTimeout(err) ? `no complete answer within ${KEY_VALIDATE_TIMEOUT_MS} ms` : 'security service unreachable or its answer unreadable');
  }
  const data = body?.data ?? body;
  if (!data?.valid) {
    apiKeyCache.set(key, { result: null, expiresAt: Date.now() + 30_000 });
    return { outcome: 'rejected' };
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
  return { outcome: 'valid', meta };
}

// ---------------------------------------------------------------------------
// KS-1198 / KS-1470: a connector JWT is never a client credential
// ---------------------------------------------------------------------------

/**
 * The one refusal for a verified connector JWT presented as a Bearer. It is shared by `authenticateToken`
 * (KS-1198) and the front-door `rejectConnectorBearer` (KS-1470), so the two cannot drift: one structured
 * warning that names `x-api-key`, never the token, and one 401 body.
 */
function refuseConnectorBearer(req: Request, res: Response, decoded: Pick<UserPayload, 'userId' | 'tenantId'>): void {
  logger.warn('[gateway-auth] refused a connector JWT presented as a Bearer credential; the caller should present its API key in the x-api-key header', {
    type: 'security',
    event: 'CONNECTOR_JWT_AS_BEARER_REFUSED',
    expectedHeader: 'x-api-key',
    connector: decoded.userId,
    tenantId: decoded.tenantId,
    method: req.method,
    path: req.baseUrl + req.path,
    requestId: req.requestId,
  });
  res.status(401).json({
    success: false,
    error: { code: 'UNAUTHORIZED', message: 'A connector token is not accepted as a Bearer credential. Present your API key in the x-api-key header.' },
  });
}

/** True when it answered: the request carries a Bearer whose signature verifies and whose signed `type` is `connector`. */
async function refusesConnectorBearer(req: Request, res: Response): Promise<boolean> {
  const authHeader = req.headers.authorization;
  // The same parse `authenticateToken` and the upstreams' shared `authenticate()` use: the literal `Bearer ` scheme and
  // the second space-separated word. A header either of them would not read as a Bearer is nothing they would accept.
  if (!authHeader || !authHeader.startsWith('Bearer ')) return false;
  let decoded: UserPayload;
  try {
    decoded = await verifyRs256(authHeader.split(' ')[1]);
  } catch {
    // Not a verifiable token (bad signature, expired, malformed, no key): not a connector credential, so it goes on exactly
    // as it did before this check existed. `authenticateToken` answers its own 401; a mount without it forwards the header
    // and the upstream's signature check refuses it. Only a token whose signature verified is acted on.
    return false;
  }
  if (decoded.type !== 'connector') return false;
  refuseConnectorBearer(req, res, decoded);
  return true;
}

/**
 * KS-1470: refuse a connector JWT presented as a Bearer at the FRONT DOOR, before any mount.
 *
 * KS-1198 refuses it inside `authenticateToken` only. A mount that does not use it (`/api/verification`,
 * `/api/v2/verification`, `/api/presentations/verify`, `/api/documents/:id/sig-json`, `/api/auth/*`, `/api/oauth/*`,
 * `/api/sessions`, the gateway-internal `/originate/`, ...) forwarded the header to the upstream verbatim, where the
 * shared `authenticate()` checks the signature only and takes the connector JWT for an ordinary principal.
 * Nothing client-side holds a connector JWT: the gateway mints one from a validated `x-api-key` and attaches it itself.
 *
 * This sees only what the CALLER sent. The `x-api-key` branch of `authenticateToken` sets its own
 * `Authorization: Bearer <connector JWT>` later, on a route that this middleware has already let through, so the
 * gateway's own flow is untouched. Same trigger as KS-1198 (the SIGNED `type` claim, after the signature verifies),
 * same 401, same warning. A valid `x-api-key` beside a connector Bearer is refused too: a mount that never validates
 * the key forwards the Bearer regardless, so the key cannot be what makes it safe.
 *
 * Mounted once, in `index.ts`, after the audit middleware and before the first route.
 */
export function rejectConnectorBearer(): RequestHandler {
  return async (req: Request, res: Response, next: NextFunction) => {
    let answered: boolean;
    try {
      answered = await refusesConnectorBearer(req, res);
    } catch (err) {
      next(err);
      return;
    }
    if (!answered) next();
  };
}

// ---------------------------------------------------------------------------
// KS-1244: a repeated x-api-key is refused, never validated
// ---------------------------------------------------------------------------

const API_KEY_HEADER = 'x-api-key';

/** KS-1244: how many header lines named x-api-key (any case) the request arrived with, and whether any value carried a comma. */
function apiKeyLineShape(req: Request): { lines: number; commaInLine: boolean } {
  let lines = 0;
  let commaInLine = false;
  // `rawHeaders` is Node's per-line record, [name, value, name, value, ...] in arrival order and spelling. A hand-built
  // request (a unit test) has none, and then only `req.headers` below speaks.
  const raw: unknown = (req as { rawHeaders?: unknown }).rawHeaders;
  if (Array.isArray(raw)) {
    for (let i = 0; i + 1 < raw.length; i += 2) {
      if (String(raw[i]).toLowerCase() !== API_KEY_HEADER) continue;
      lines += 1;
      if (String(raw[i + 1]).includes(',')) commaInLine = true;
    }
  }
  return { lines, commaInLine };
}

/**
 * KS-1244: true when the request carries x-api-key more than once. Before this, `authenticateToken` read
 * `req.headers['x-api-key']`, where Node has already JOINED repeated lines into one string ("sk_a, sk_b"); that string
 * failed validation, so a required mount answered 401 "Invalid API key" and an OPTIONAL mount fell through to the Bearer
 * path (KS-1207) and served the request anonymously, or as the Bearer's user. A joined value whose first segment was
 * empty or not `sk_` (", sk_b", "junk, sk_b") was not read as a key at all.
 *
 * Three clauses, each measured to matter on its own (Seat E 34th, Node 26.8.1, raw socket bytes; the image's Node 24 is
 * not measured, which is why the clauses do not lean on each other):
 *  1. more than one raw header line named x-api-key, in any case: what an HTTP client that sends an array (node:http)
 *     puts on the wire, read without trusting how the runtime joins it;
 *  2. a comma in any raw line: `fetch` sends a duplicate as ONE comma-joined line, and RFC 9110 section 5.3 lets any
 *     intermediary fold two lines the same way;
 *  3. a comma in, or a non-string, `req.headers` value: what Node shows for both shapes, and the only thing a hand-built
 *     request carries.
 * A minted key is `sk_` plus 64 hex characters (security, originate adminConfig), so no valid key contains a comma.
 * Kam's ruling: card secuura-ks1244-repeated-api-key-1104 = a; the comma and the empty segment count (Wednesday,
 * 2026-11-04 04:36:56Z). Never throws on a request Node built; reads no value beyond the comma test.
 */
export function carriesRepeatedApiKey(req: Request): boolean {
  const { lines, commaInLine } = apiKeyLineShape(req);
  if (lines > 1 || commaInLine) return true;
  const value: unknown = req.headers[API_KEY_HEADER];
  if (value === undefined) return false;
  return typeof value !== 'string' || value.includes(',');
}

/**
 * KS-1244: the one refusal for a repeated x-api-key, shared by the front door and `authenticateToken` so the two cannot
 * drift. 400, not 401 (Wednesday's ruling 2026-11-04 04:36:56Z): it is a malformed request, refused before either value
 * is read, on every route including the public ones, and the body is constant whatever the values are, so it tells a
 * caller nothing about any key. One structured warning carries the line count and the path; neither value is ever logged.
 */
function refuseRepeatedApiKey(req: Request, res: Response): void {
  const { lines, commaInLine } = apiKeyLineShape(req);
  logger.warn('[gateway-auth] refused a request that carries the x-api-key header more than once; no key was checked', {
    type: 'security',
    event: 'REPEATED_API_KEY_REFUSED',
    headerLines: lines,
    commaInValue: commaInLine,
    method: req.method,
    path: req.baseUrl + req.path,
    requestId: req.requestId,
  });
  res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'The x-api-key header must be sent once' } });
}

/**
 * KS-1244: refuse a repeated x-api-key at the FRONT DOOR, before any route, any key check and the spec auth gate.
 * Mounted once, in `index.ts`, immediately before `rejectConnectorBearer` (KS-1470's spot): after csrf (whose header-
 * credential skip grants a refused request nothing: it sets no principal), after the production 307 (so an unversioned
 * request still redirects, KS-1234) and after the audit middleware; before the spec gate, which counts any `sk_` string
 * as a credential, and before every route and proxy. A mount that never runs `authenticateToken` forwarded the joined
 * header upstream verbatim; this is what covers it.
 */
export function rejectRepeatedApiKey(): RequestHandler {
  return (req: Request, res: Response, next: NextFunction) => {
    let repeated: boolean;
    try {
      repeated = carriesRepeatedApiKey(req);
    } catch (err) {
      // Fail closed: a request this cannot read goes to the error handler, never on to a route.
      next(err);
      return;
    }
    if (!repeated) {
      next();
      return;
    }
    refuseRepeatedApiKey(req, res);
  };
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

// KS-1205 F-4: the limiter runs as a floating promise (the continuation of each
// branch). If the continuation throws, that promise rejects; with nothing attached
// it is an unhandled rejection, which in production's default exit mode shuts the
// process down, and on the JWT branch it must not be turned into a 401 either.
// Hand the rejection to Express instead.
const continueThroughLimiter = (req: Request, res: Response, next: NextFunction): Promise<void> =>
  clientRateLimit(req, res, next).catch(next);

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
    // KS-1244: a repeated x-api-key is refused here too, before either value is read, so a router mounted ahead of the
    // front door (`rejectRepeatedApiKey` in index.ts) cannot reach the KS-1207 fall-through with one. Before, the joined
    // value was validated below as one key: 401 on a required mount, anonymous (or the Bearer's user) on an optional one.
    // In the assembled app the front door answers first, so this does not log a second warning.
    if (carriesRepeatedApiKey(req)) {
      refuseRepeatedApiKey(req, res);
      return;
    }
    // --- API key path ---
    const apiKey = req.headers['x-api-key'] as string | undefined;
    const presentedKey = Boolean(apiKey && apiKey.startsWith('sk_'));
    const check = apiKey && presentedKey ? await checkApiKey(apiKey) : null;
    // KS-1240: a presented key whose check could not complete is answered 503 on required AND optional mounts. It is
    // not "Invalid API key" (Kam's rulings on cards secuura-ks888-revoke-validate-on-failed-save (a) and
    // secuura-ks1370-validate-when-the-revoke-check-cannot-read (a): an unverifiable key is refused with 503), and an
    // optional mount does not serve the caller as anonymous instead: the caller asked to be the key's principal. It is
    // a refusal, never a pass, so the KS-1207 guarantee below holds. A REJECTED key keeps every answer it had.
    if (check?.outcome === 'unavailable') {
      res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Unable to verify API key, please retry' } });
      return;
    }
    const meta = check?.outcome === 'valid' ? check.meta : null;
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
      // KS-1215 (Wednesday's ruling O3): this branch never carries the caller's
      // Bearer. The principal here is the connector, so any Authorization the
      // caller sent is dropped first, before any await. A successful exchange
      // below sets the connector JWT; a failed one forwards no Bearer at all.
      // Before, a failed exchange left the caller's header in place: a REVOKED
      // session's JWT beside a valid key reached the upstreams past the
      // revocation check, and a live user's JWT travelled under the connector
      // principal. A valid key alone still grants the connector, by design.
      delete req.headers.authorization;
      // KS-1205 N-2: the bucket is recorded against the request below; the limiter reads
      // that record, not this field, so a JWT claim of the same name cannot reach it.
      const rateLimitBucket = `api_key:${createHash('sha256').update('secuura-rate-limit-bucket\0').update(apiKey).digest('hex')}`;
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
        rateLimitBucket,
        // KS-480: the key's scopes must live on the principal — requireScope
        // reads user.scopes, and without this every scope-gated mount 403'd
        // sk_ callers with `granted: []` regardless of the key's actual grants.
        scopes: meta.scopes,
        tenantId: meta.tenantId || undefined,
        tenantSlug: meta.tenantSlug || undefined,
      };
      req.user = connectorUser;
      recordApiKeyBucket(req, rateLimitBucket);
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
      runWithTenantId(meta.tenantId, () => continueThroughLimiter(req, res, next));
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
      runWithTenantId(testPayload.tenantId, () => continueThroughLimiter(req, res, next));
      return;
    }

    // Verify JWT
    try {
      // KS-184/347: RS256-only verification; key resolved by kid via JWKS with a
      // static-key fallback (see verifyRs256). Async for the JWKS fetch.
      const decoded = await verifyRs256(token);

      // KS-1198: a connector JWT is the gateway's own transport to the upstream services. It is minted from a
      // validated `x-api-key` at auth's internal endpoint and forwarded; nothing on the client side holds one, and
      // the mint is not routed through the edge. Presented directly as a Bearer it would be an ordinary principal
      // here and skip the gates only the API-key branch sets up (connectorMeta: the scope check and the
      // allowedDocumentTypes allow-list). So it is refused: hard, on required AND optional mounts (a pass-through
      // would forward the verified Bearer upstream), and only after the signature verified (an unverifiable token
      // keeps taking the invalid-token path below). One structured warning per refusal; the token is never logged.
      if (decoded.type === 'connector') {
        refuseConnectorBearer(req, res, decoded);
        return;
      }

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
      // KS-1536 (Kam, card secuura-ks-1536-platform-admin-role-one-list-1106, option a, "One shared list without platform_admin, after a check"): was a local list that also named platform_admin.
      const tenantOverride = req.headers['x-tenant-override'] as string | undefined;
      if (tenantOverride && isPlatformRole(decoded.role)) {
        req.headers['x-tenant-id'] = tenantOverride;
        // Clear slug — service will resolve from config
        req.headers['x-tenant-slug'] = '';
      } else {
        if (decoded.tenantId) req.headers['x-tenant-id'] = decoded.tenantId;
        if (decoded.tenantSlug) req.headers['x-tenant-slug'] = decoded.tenantSlug;
      }
      // KS-458: seed the RLS tenant context from the verified JWT (or the
      // super-admin override that was just written to x-tenant-id).
      runWithTenantId((req.headers['x-tenant-id'] as string | undefined) || decoded.tenantId, () => continueThroughLimiter(req, res, next));
    } catch (error) {
      if (required) {
        res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid or expired token' } });
        return;
      }
      next();
    }
  };
}
