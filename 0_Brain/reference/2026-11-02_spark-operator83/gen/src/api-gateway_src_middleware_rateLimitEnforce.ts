/**
 * =============================================================================
 * PER-CLIENT RATE LIMIT ENFORCEMENT
 * =============================================================================
 * Enforces rate limits defined in API key / OAuth app metadata.
 * Uses the shared Redis counter for a correct distributed ceiling across
 * replicas; falls back to in-memory only when Redis is genuinely unavailable.
 * Adds standard rate limit headers to all responses.
 * =============================================================================
 */

import { Request, Response, NextFunction } from 'express';
import { getRedisClient } from '../services/redis';
import { logger } from '../utils/logger';

// In-memory fallback counter (used when Redis is unavailable)
const memoryCounters = new Map<string, { count: number; resetAt: number }>();

/**
 * Count this request against the per-replica in-memory window.
 *
 * KS-616: extracted so the error path can reach the SAME degraded ceiling the
 * "Redis not ready" path already uses. That fallback existed three lines above
 * the fail-open `catch` the whole time — the error path simply never used it.
 */
function countInMemory(clientId: string, windowMs: number): { count: number; resetAt: number } {
  const now = Date.now();
  let entry = memoryCounters.get(clientId);
  if (!entry || now > entry.resetAt) {
    entry = { count: 0, resetAt: now + windowMs };
    memoryCounters.set(clientId, entry);
  }
  entry.count++;
  return { count: entry.count, resetAt: entry.resetAt };
}

// KS-616: a sustained Redis outage would otherwise emit one log line per
// request. Throttle to first-occurrence-then-periodic so the signal stays
// visible without drowning the log (an unreadable log is another way for a
// degradation to be invisible).
const DEGRADE_LOG_INTERVAL_MS = 30_000;
let lastDegradeLogAt = 0;
function logDegraded(reason: string, clientId: string, err?: unknown): void {
  const now = Date.now();
  if (now - lastDegradeLogAt < DEGRADE_LOG_INTERVAL_MS) return;
  lastDegradeLogAt = now;
  logger.warn('[rateLimit] DEGRADED — per-client ceiling is no longer distributed', {
    reason,
    clientId,
    effect: 'counting per-replica in memory; the effective ceiling inflates to limit × replicas',
    error: err instanceof Error ? err.message : err ? String(err) : undefined,
    throttledFor: `${DEGRADE_LOG_INTERVAL_MS / 1000}s`,
  });
}

// KS-164: machine auth methods that MUST be governed by the per-client limiter.
// Interactive/human methods (email, wallet, federated, social, jwt) are NOT
// listed — they're handled by the global limiter. A new machine auth method
// must be added here AND must populate req.user.rateLimit (see auth.ts), or it
// would silently bypass the per-key ceiling.
const MACHINE_AUTH_METHODS = new Set(['api_key', 'oauth_app']);

// Conservative fallback applied only when a machine caller reaches the limiter
// without a configured rateLimit (misconfiguration / future path) — a machine
// caller is never allowed through unlimited.
const DEFAULT_MACHINE_RATE_LIMIT = 100;
const DEFAULT_MACHINE_RATE_WINDOW = 60; // seconds

// KS-1195: the limiter runs as the continuation of authenticateToken (auth.ts),
// and one request's chain can pass authenticateToken more than once (a router-level
// mount plus a route-level one). Count each request once, or a key allowed N per
// window would be refused after N/2 requests.
const countedRequests = new WeakSet<object>();

// KS-1205 N-2: the per-key bucket is minted ONLY by the API-key branch of
// authenticateToken, which records it here against the request. The limiter used
// to read `req.user.rateLimitBucket`, but the JWT branch copies the decoded
// payload into req.user, so a signed `rateLimitBucket` claim (or an
// `api_key:`-prefixed `connectorId` claim, through the fallback below) named
// another key's bucket and drew that key's allowance down. A WeakMap keyed by the
// request cannot be written by anything in a token.
const apiKeyBuckets = new WeakMap<object, string>();
export function recordApiKeyBucket(req: object, bucket: string): void {
  apiKeyBuckets.set(req, bucket);
}

// KS-1205 FALLBACK: every other machine principal (a machine JWT, a test token)
// is counted under `jwt:<tenant>:<connectorId || userId>`. The `jwt:` namespace
// can never equal an `api_key:` bucket, and the tenant keeps two tenants that
// happen to share a connectorId or userId from sharing one allowance.
//
// KS-1464: each claim is escaped before it is joined ('%' first, then ':'), so a claim containing ':' cannot make two
// different (tenant, id) pairs produce one key (tenant `a:b` + id `x` and tenant `a` + id `b:x` were both `jwt:a:b:x`).
// The escape is injective over JS strings (not on the Redis wire: ioredis sends UTF-8, so claims that differ only by a lone
// surrogate still land on one key, which needs a signing-authority claim), leaves every ordinary tenant and id byte for byte as
// before (so they cost no rollout), and,
// unlike encodeURIComponent, cannot throw on a lone surrogate: this runs outside the limiter's try.
const escapePart = (v: unknown): string => String(v).replace(/%/g, '%25').replace(/:/g, '%3A');
function jwtBucket(user: { tenantId?: string; connectorId?: string; userId?: string }): string {
  return `jwt:${escapePart(user.tenantId || 'no-tenant')}:${escapePart(user.connectorId || user.userId || 'unknown')}`;
}

// KS-1205 R-2: the "no rateLimit" warning used to fire on every request of such a
// principal (197 lines in the gate's probe). Once per principal per interval.
// KS-1464: "principal" is the bucket the limiter counts under (it carries the tenant), not the connector id alone, so
// two tenants' principals that share a connectorId no longer share one warning slot, and the line names the tenant.
// KS-1480: the principal and the tenant in the warning below come from signed claims or key-validation values, so each is
// escaped before it reaches the log line: JSON string escaping (backslash, quote, control characters and lone surrogates),
// then NEL, DEL and the other C1 controls and the Unicode line and paragraph separators, which JSON leaves raw. A claim cannot
// forge or split a line, ordinary ids are written byte for byte as before, and typing an escape cannot forge a real break
// (the backslash is escaped too).
const logField = (v: unknown): string =>
  JSON.stringify(String(v)).slice(1, -1).replace(/[\u007f-\u009f\u2028\u2029]/g, (c) => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'));

const NO_ALLOWANCE_WARN_INTERVAL_MS = 30_000;
const noAllowanceWarnedAt = new Map<string, number>();
function warnNoAllowance(throttleKey: string, principal: string, tenant: string, authMethod: string): void {
  const now = Date.now();
  const last = noAllowanceWarnedAt.get(throttleKey);
  if (last !== undefined && now - last < NO_ALLOWANCE_WARN_INTERVAL_MS) return;
  noAllowanceWarnedAt.set(throttleKey, now);
  console.warn(
    `[rateLimit] machine caller ${logField(principal)} (${authMethod}, tenant ${logField(tenant)}) has no rateLimit — applying default ${DEFAULT_MACHINE_RATE_LIMIT}/${DEFAULT_MACHINE_RATE_WINDOW}s (warned once per ${NO_ALLOWANCE_WARN_INTERVAL_MS / 1000}s)`,
  );
}

function sendRateLimited(res: Response, limit: number, windowMs: number, resetAt: number): void {
  const retryAfter = Math.max(1, Math.ceil((resetAt - Date.now()) / 1000));
  res.setHeader('Retry-After', retryAfter.toString());
  res.status(429).json({
    success: false,
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Rate limit exceeded',
      details: {
        limit,
        remaining: 0,
        retryAfter,
        hint: `Your app is limited to ${limit} requests per ${Math.round(windowMs / 1000)}s. Try again in ${retryAfter}s.`,
      },
    },
  });
}

/**
 * Enforce per-client rate limits.
 * Reads rateLimit and rateLimitWindow from req.user (set by auth middleware).
 * Regular JWT users are NOT rate-limited by this middleware (handled by global limiter).
 *
 * @param injectedClient Optional Redis client override (tests). In production the
 *   client is resolved lazily per request via getRedisClient() — see KS-170.
 */
export function enforceClientRateLimit(injectedClient?: any) {
  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const user = (req as any).user;

    // Only enforce on machine callers (API key / OAuth app). No user, or any
    // interactive/human auth method, is governed by the global limiter instead.
    if (!user || !MACHINE_AUTH_METHODS.has(user.authMethod)) {
      next();
      return;
    }

    if (countedRequests.has(req)) {
      next();
      return;
    }
    countedRequests.add(req);

    // KS-1195 (A5): bucket by the caller's own identity. The API-key path records a
    // per-key bucket against the request (auth.ts, recordApiKeyBucket). KS-1205 N-2:
    // that record is the ONLY source of an `api_key:` bucket; a machine principal
    // that did not come through that path (a machine JWT, a test token) is counted
    // under its own tenant-scoped `jwt:` namespace and can never name a key's bucket.
    const clientId = apiKeyBuckets.get(req) ?? jwtBucket(user);

    if (!user.rateLimit) {
      // Defensive (KS-164): a machine caller with no configured allowance must
      // not slip through unlimited — apply a conservative default and warn.
      // KS-1464: throttled on the bucket (clientId), decided above, which carries the tenant.
      warnNoAllowance(clientId, String(user.connectorId || user.userId), String(user.tenantId || 'none'), logField(user.authMethod));
    }
    const limit = user.rateLimit || DEFAULT_MACHINE_RATE_LIMIT;
    const windowMs = (user.rateLimitWindow || DEFAULT_MACHINE_RATE_WINDOW) * 1000;

    // KS-170: resolve the Redis client PER REQUEST. The factory runs at module
    // load (api-gateway index.ts:494), before initRedis() connects — capturing
    // the client there pins null, so the limiter silently counts in-memory.
    // In-memory counting is per-replica, and the api-gateway scales 1->3
    // replicas, so under load the effective ceiling inflates to limit ×
    // replicas — exactly when the limit matters. Resolving lazily uses the
    // shared distributed counter once Redis is up, and survives reconnects.
    // An injected client (tests) takes precedence.
    const redisClient = injectedClient ?? getRedisClient();

    // KS-1205 F-4: decide inside the try, act after it. `next()` used to sit inside
    // it, so a continuation that threw was caught by this very catch, counted a
    // second time, and dispatched again (measured: three dispatches for one throw).
    // `outcome` is null only when the limiter itself is broken.
    let outcome: { count: number; resetAt: number } | null;
    try {
      // `count` is the number of requests seen in this window INCLUDING the
      // current one. We allow exactly `limit` requests, blocking the
      // (limit+1)th — so a key configured at N/min lets N through and 429s the
      // (N+1)th (KS-164 acceptance).
      let count: number;
      let resetAt: number;

      // ioredis API (the gateway client is ioredis, NOT node-redis): readiness
      // is `.status === 'ready'`, and the millisecond commands are lowercase
      // `pexpire`/`pttl`. The previous node-redis names (isReady/pExpire/pTTL)
      // silently no-op'd on ioredis — the other half of why this never used
      // Redis even once a client was wired in (KS-170).
      if (redisClient && redisClient.status === 'ready') {
        // Redis-based distributed counting
        const key = `ratelimit:${clientId}`;
        count = await redisClient.incr(key);
        if (count === 1) {
          await redisClient.pexpire(key, windowMs);
        }
        const ttl = await redisClient.pttl(key);
        resetAt = Date.now() + (ttl > 0 ? ttl : windowMs);
      } else {
        // In-memory fallback (Redis genuinely down). KS-616: this was silent —
        // the ceiling quietly stopped being distributed with nothing to notice
        // it by. Now it says so.
        logDegraded('redis-not-ready', clientId);
        ({ count, resetAt } = countInMemory(clientId, windowMs));
      }

      outcome = { count, resetAt };
    } catch (err) {
      // =====================================================================
      // KS-616 — was: `next()`, i.e. allow with NO limit applied at all
      // =====================================================================
      // Review F, F-6. The old behaviour triggered precisely when the platform
      // was under the load that makes Redis wobble — the moment the limiter
      // matters most — and did so silently and unmetered.
      //
      // Recorded so the next reviewer does not have to re-derive it, per the
      // ticket. Three options were on the table:
      //
      //   1. Hard fail-closed (429 on error). REJECTED. Unlike tenant
      //      isolation — where KS-458 deliberately chose fail-closed because
      //      leaking another tenant's data is unrecoverable — rate limiting
      //      has a real availability tradeoff: a Redis blip would become a
      //      total outage for every machine caller. KS-617 is an open ticket
      //      about exactly that failure shape, so adding another instance of
      //      it would be perverse.
      //   2. Fail open, unlimited (the old behaviour). REJECTED. It removes
      //      the control entirely at the worst moment, and leaves no trace.
      //   3. Degrade to the per-replica in-memory ceiling. CHOSEN.
      //
      // Option 3 costs nothing to implement because that fallback already
      // existed for the "Redis not ready" branch — the error path simply
      // never reached it. It is weaker than the distributed counter (the
      // effective ceiling inflates to limit × replicas, the KS-170 problem),
      // but "weaker ceiling" is a different class of thing from "no ceiling",
      // and it fails toward availability rather than toward an open door.
      //
      // The catch is also narrower than it looks: Redis being DOWN is already
      // handled by the readiness branch above. This path is Redis reporting
      // ready and then throwing mid-command — a timeout, a reset connection,
      // an OOM reply — which is transient by nature and exactly what a local
      // ceiling covers well.
      try {
        logDegraded('redis-command-failed', clientId, err);
        outcome = countInMemory(clientId, windowMs);
      } catch (fallbackErr) {
        // The degraded path is pure in-process arithmetic, so reaching here
        // means something outside the limiter is broken. Allow the request
        // rather than 500 the caller on a rate-limit bookkeeping failure — but
        // say so at error level, since unlike the degradation above this is not
        // an expected state.
        logger.error('[rateLimit] in-memory fallback ALSO failed — request allowed unlimited', {
          clientId,
          error: fallbackErr instanceof Error ? fallbackErr.message : String(fallbackErr),
        });
        outcome = null;
      }
    }

    let refused = false;
    if (outcome) {
      try {
        const remaining = Math.max(0, limit - outcome.count);

        // Set rate limit headers on ALL responses
        res.setHeader('X-RateLimit-Limit', limit.toString());
        res.setHeader('X-RateLimit-Remaining', remaining.toString());
        res.setHeader('X-RateLimit-Reset', Math.ceil(outcome.resetAt / 1000).toString());

        if (outcome.count > limit) {
          sendRateLimited(res, limit, windowMs, outcome.resetAt);
          refused = true;
        }
      } catch (writeErr) {
        // e.g. the response is already committed. Same rule as above: a bookkeeping
        // failure does not 500 the caller, and it is not silent.
        logger.error('[rateLimit] could not write the rate-limit headers or the 429 — request allowed unlimited', {
          clientId,
          error: writeErr instanceof Error ? writeErr.message : String(writeErr),
        });
        refused = false;
      }
    }

    // The continuation runs OUTSIDE every try above. A throw from it propagates out of
    // this async function (authenticateToken hands the rejection to next(err)).
    if (!refused) next();
  };
}

// Cleanup stale memory counters every 5 minutes
setInterval(() => {
  const now = Date.now();
  for (const [key, entry] of memoryCounters.entries()) {
    if (now > entry.resetAt) {
      memoryCounters.delete(key);
    }
  }
  for (const [principal, at] of noAllowanceWarnedAt.entries()) {
    if (now - at >= NO_ALLOWANCE_WARN_INTERVAL_MS) noAllowanceWarnedAt.delete(principal);
  }
}, 5 * 60 * 1000);
