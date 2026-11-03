/**
 * =============================================================================
 * SESSION SERVICE — Redis-backed
 * =============================================================================
 * Sessions are stored in Redis for persistence across container restarts.
 * =============================================================================
 */

import crypto from 'crypto';
import { Session, User } from '../types';
import { logger } from '../utils/logger';

// =============================================================================
// REDIS CLIENT
// =============================================================================
let redis: any = null;
let redisAvailable = false;

/** Test-only: inject a mock Redis client */
export function __setRedisForTesting(mockRedis: any): void {
  redis = mockRedis;
  redisAvailable = true;
}

export async function initRedisSession(): Promise<void> {
  const redisUrl = process.env.REDIS_URL;
  if (!redisUrl) {
    logger.warn('REDIS_URL not set — session operations will fail until Redis is available');
    return;
  }

  try {
    const Redis = (await import('ioredis')).default;
    redis = new Redis(redisUrl, {
      maxRetriesPerRequest: 3,
      // KS-617: NEVER return null from retryStrategy. ioredis treats null as
      // "stop reconnecting, permanently" — it is not a back-off signal. The
      // previous `if (times > 3) return null` meant any Redis blip lasting
      // more than a few hundred milliseconds killed this client for the life
      // of the process: no further reconnect attempts, so the 'ready'/'connect'
      // event never fired again and the availability flag stayed false until a
      // human restarted the container — while the container kept reporting
      // healthy. Reconnect forever with capped exponential backoff instead.
      // Per-command latency is bounded separately by maxRetriesPerRequest, so
      // this does not make callers hang while Redis is down: individual
      // commands still fail fast and the connection heals itself.
      retryStrategy(times: number) {
        return Math.min(times * 200, 5000);
      },
      lazyConnect: true,
    });

    await redis.connect();
    await redis.ping();
    redisAvailable = true;
    logger.info('Redis connection established for sessions');

    redis.on('error', (err: Error) => {
      logger.error('Redis error', { error: err.message });
      redisAvailable = false;
    });

    redis.on('reconnecting', () => {
      logger.info('Redis reconnecting...');
    });

    redis.on('ready', () => {
      redisAvailable = true;
      logger.info('Redis ready');
    });
  } catch (err: any) {
    logger.warn('Redis unavailable — using in-memory session fallback', { error: err?.message });
    redisAvailable = false;
  }
}

/** Returns the underlying Redis client (or null if not connected) */
export function getRedisClient(): any {
  return redisAvailable ? redis : null;
}

/** Whether the Redis session store is currently reachable */
export function isRedisAvailable(): boolean {
  return redisAvailable;
}

// Configuration
const SESSION_EXPIRY_HOURS = parseInt(process.env.SESSION_EXPIRY_HOURS || '24', 10);
// KS-43: per-cohort caps. Browser + native cohorts share the multi-session
// pool (default 10 each — large enough that 4 parallel Playwright workers
// across 5 personas don't churn). 'api' is always single-session (cap 1).
// `MAX_SESSIONS_PER_USER` is the legacy env var; if set, it overrides the
// browser+native default so existing deployments keep working.
const MAX_SESSIONS_PER_USER_LEGACY = process.env.MAX_SESSIONS_PER_USER
  ? parseInt(process.env.MAX_SESSIONS_PER_USER, 10)
  : undefined;
const MAX_SESSIONS_BROWSER = parseInt(
  process.env.MAX_SESSIONS_PER_USER_BROWSER || `${MAX_SESSIONS_PER_USER_LEGACY ?? 10}`,
  10,
);
const MAX_SESSIONS_NATIVE = parseInt(
  process.env.MAX_SESSIONS_PER_USER_NATIVE || `${MAX_SESSIONS_PER_USER_LEGACY ?? 10}`,
  10,
);
const SESSION_TTL_SECONDS = SESSION_EXPIRY_HOURS * 3600;

type ClientType = 'browser' | 'native' | 'api';

function capForClientType(clientType: ClientType): number {
  if (clientType === 'api') return 1;
  if (clientType === 'native') return MAX_SESSIONS_NATIVE;
  return MAX_SESSIONS_BROWSER;
}

// Redis key helpers
const sessionKey = (id: string) => `sess:${id}`;
const userSessionsKey = (userId: string) => `user_sessions:${userId}`;

function generateSessionId(): string {
  return `sess_${crypto.randomBytes(32).toString('hex')}`;
}

// =============================================================================
// SESSION CRUD
// =============================================================================

/** Create a new session */
export async function createSession(
  user: User,
  ipAddress?: string,
  userAgent?: string,
  deviceId?: string,
  clientType: ClientType = 'browser',
  mintedBy?: 'oauth',
): Promise<Session> {
  const sessionId = generateSessionId();
  const now = new Date();
  const expiresAt = new Date(now.getTime() + SESSION_EXPIRY_HOURS * 3600000);

  const session: Session = {
    id: sessionId,
    userId: user.id,
    token: crypto.randomBytes(32).toString('hex'),
    refreshToken: crypto.randomBytes(32).toString('hex'),
    ipAddress,
    userAgent,
    deviceId,
    clientType,
    ...(mintedBy ? { mintedBy } : {}),
    expiresAt,
    lastActivityAt: now,
    isActive: true,
    createdAt: now,
  };

  if (!redisAvailable) {
    throw new Error('Redis is not available — cannot create session');
  }

  // KS-43: cohort-aware eviction. Hydrate every existing session for this
  // user, then bucket by clientType. Three policies:
  //
  //  1. 'api' is single-session — any prior 'api' session is revoked
  //     unconditionally. Browser/native sessions are untouched (an admin
  //     can have a browser dashboard open AND an API token at the same
  //     time without one nuking the other).
  //  2. Same-device replacement — if the new login carries a deviceId and
  //     there is already a session for (userId, deviceId, clientType),
  //     revoke that one first. Stops a 4-worker test harness with stable
  //     deviceIds from accreting sessions across runs.
  //  3. Per-cohort LRU — count remaining sessions of the same clientType;
  //     if at or over the cap, evict the genuinely oldest by createdAt
  //     (KS-14: Redis SMEMBERS order is arbitrary, so sort don't slice).
  //
  // Old comment retained for context: the pre-KS-43 blanket policy capped
  // sessions across all clientTypes in a single pool, which caused tier-1
  // through tier-3 e2e flakes whenever 4 parallel workers x 5 personas
  // pushed the active set over the (then-5) cap and the LRU evicted a
  // session a worker was mid-request with.
  const existingIds: string[] = await redis.smembers(userSessionsKey(user.id));
  const records: Array<{
    id: string;
    createdAt: number;
    clientType: ClientType;
    deviceId?: string;
  }> = [];
  for (const sid of existingIds) {
    try {
      const raw = await redis.get(sessionKey(sid));
      if (raw) {
        const parsed = JSON.parse(raw) as {
          createdAt?: string | number;
          clientType?: ClientType;
          deviceId?: string;
        };
        records.push({
          id: sid,
          createdAt: new Date(parsed.createdAt ?? 0).getTime(),
          // Legacy records pre-KS-43 have no clientType; treat as 'browser'
          // since that was the only multi-session path before this fix.
          clientType: parsed.clientType ?? 'browser',
          deviceId: parsed.deviceId,
        });
      } else {
        // Dangling set member with no backing record — evict on sight.
        records.push({ id: sid, createdAt: 0, clientType: 'browser' });
      }
    } catch {
      records.push({ id: sid, createdAt: 0, clientType: 'browser' });
    }
  }

  // (1) 'api' single-session
  if (clientType === 'api') {
    for (const r of records.filter((rec) => rec.clientType === 'api')) {
      await revokeSession(r.id);
    }
  }

  // (2) same-device replacement (browser/native only; 'api' has no stable
  //     device concept and step 1 already cleared its prior sessions)
  if (clientType !== 'api' && deviceId) {
    for (const r of records.filter(
      (rec) => rec.clientType === clientType && rec.deviceId === deviceId,
    )) {
      await revokeSession(r.id);
    }
  }

  // (3) Per-cohort LRU eviction. Re-read the set (steps 1-2 may have just
  // shrunk it) and only count records of the same clientType.
  const refreshedIds: string[] = await redis.smembers(userSessionsKey(user.id));
  const sameCohort = records.filter(
    (r) => r.clientType === clientType && refreshedIds.includes(r.id),
  );
  const cap = capForClientType(clientType);
  if (sameCohort.length >= cap) {
    sameCohort.sort((a, b) => a.createdAt - b.createdAt);
    const evictCount = sameCohort.length - cap + 1;
    for (let i = 0; i < evictCount && i < sameCohort.length; i++) {
      await revokeSession(sameCohort[i].id);
    }
  }

  // Store session as JSON with TTL
  await redis.setex(sessionKey(sessionId), SESSION_TTL_SECONDS, JSON.stringify(session));
  await redis.sadd(userSessionsKey(user.id), sessionId);
  await redis.expire(userSessionsKey(user.id), SESSION_TTL_SECONDS);

  logger.info('Session created', { sessionId, userId: user.id, clientType });
  return session;
}

/** Get session by ID */
export async function getSession(sessionId: string): Promise<Session | null> {
  if (!redisAvailable) return null;

  const data = await redis.get(sessionKey(sessionId));
  if (!data) return null;
  const session: Session = JSON.parse(data);
  // Rehydrate dates
  session.expiresAt = new Date(session.expiresAt);
  session.lastActivityAt = new Date(session.lastActivityAt);
  session.createdAt = new Date(session.createdAt);
  if (session.revokedAt) session.revokedAt = new Date(session.revokedAt);

  if (new Date() > session.expiresAt || !session.isActive) return null;
  return session;
}

/** Update session activity */
export async function updateSessionActivity(sessionId: string): Promise<void> {
  if (!redisAvailable) return;

  const data = await redis.get(sessionKey(sessionId));
  if (data) {
    const session = JSON.parse(data);
    session.lastActivityAt = new Date();
    await redis.setex(sessionKey(sessionId), SESSION_TTL_SECONDS, JSON.stringify(session));
  }
}

/** Rotate refresh token — invalidates the old one by updating the session in Redis */
export async function rotateSessionRefreshToken(sessionId: string, newRefreshToken: string): Promise<void> {
  if (!redisAvailable) return;

  const data = await redis.get(sessionKey(sessionId));
  if (!data) return;
  const session: Session = JSON.parse(data);

  session.refreshToken = newRefreshToken;
  session.lastActivityAt = new Date();

  await redis.setex(sessionKey(sessionId), SESSION_TTL_SECONDS, JSON.stringify(session));
  logger.debug('Session refresh token rotated', { sessionId });
}

/** Revoke session */
export async function revokeSession(sessionId: string): Promise<boolean> {
  if (!redisAvailable) return false;

  const data = await redis.get(sessionKey(sessionId));
  if (!data) return false;
  const session: Session = JSON.parse(data);

  session.isActive = false;
  session.revokedAt = new Date();
  // Keep for audit but with short TTL
  await redis.setex(sessionKey(sessionId), 3600, JSON.stringify(session));
  await redis.srem(userSessionsKey(session.userId), sessionId);

  logger.info('Session revoked', { sessionId, userId: session.userId });
  return true;
}

/** Revoke all sessions for a user */
export async function revokeAllUserSessions(userId: string): Promise<number> {
  if (!redisAvailable) return 0;

  let count = 0;
  const sessionIds = await redis.smembers(userSessionsKey(userId));
  for (const sid of sessionIds) {
    if (await revokeSession(sid)) count++;
  }
  await redis.del(userSessionsKey(userId));
  logger.info('All sessions revoked', { userId, count });
  return count;
}

/** Get all active sessions for a user */
export async function getUserSessions(userId: string): Promise<Session[]> {
  if (!redisAvailable) return [];

  const sessionIds = await redis.smembers(userSessionsKey(userId));
  if (sessionIds.length === 0) return [];

  const keys = sessionIds.map((sid: string) => sessionKey(sid));
  const results = await redis.mget(...keys);
  const sessions: Session[] = [];
  const now = new Date();

  for (const data of results) {
    if (data) {
      const session: Session = JSON.parse(data);
      session.expiresAt = new Date(session.expiresAt);
      session.lastActivityAt = new Date(session.lastActivityAt);
      session.createdAt = new Date(session.createdAt);
      if (session.isActive && now < session.expiresAt) {
        sessions.push(session);
      }
    }
  }
  return sessions;
}

/** Validate session exists and is active */
export async function validateSession(sessionId: string): Promise<boolean> {
  const session = await getSession(sessionId);
  return session !== null && session.isActive;
}

/** Extend session expiry */
export async function extendSession(sessionId: string): Promise<Session | null> {
  const session = await getSession(sessionId);
  if (!session || !session.isActive) return null;

  session.expiresAt = new Date(Date.now() + SESSION_EXPIRY_HOURS * 3600000);
  session.lastActivityAt = new Date();

  if (!redisAvailable) return null;

  await redis.setex(sessionKey(sessionId), SESSION_TTL_SECONDS, JSON.stringify(session));
  return session;
}

/** Clean up expired sessions */
export async function cleanupExpiredSessions(): Promise<number> {
  // Redis handles TTL-based expiry automatically — nothing to clean up.
  return 0;
}
