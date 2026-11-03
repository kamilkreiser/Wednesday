"use strict";
/**
 * =============================================================================
 * SESSION SERVICE — Redis-backed
 * =============================================================================
 * Sessions are stored in Redis for persistence across container restarts.
 * =============================================================================
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.__setRedisForTesting = __setRedisForTesting;
exports.initRedisSession = initRedisSession;
exports.getRedisClient = getRedisClient;
exports.isRedisAvailable = isRedisAvailable;
exports.createSession = createSession;
exports.getSession = getSession;
exports.updateSessionActivity = updateSessionActivity;
exports.rotateSessionRefreshToken = rotateSessionRefreshToken;
exports.revokeSession = revokeSession;
exports.revokeAllUserSessions = revokeAllUserSessions;
exports.getUserSessions = getUserSessions;
exports.validateSession = validateSession;
exports.extendSession = extendSession;
exports.cleanupExpiredSessions = cleanupExpiredSessions;
const crypto_1 = __importDefault(require("crypto"));
const logger_1 = require("../utils/logger");
// =============================================================================
// REDIS CLIENT
// =============================================================================
let redis = null;
let redisAvailable = false;
/** Test-only: inject a mock Redis client */
function __setRedisForTesting(mockRedis) {
    redis = mockRedis;
    redisAvailable = true;
}
async function initRedisSession() {
    const redisUrl = process.env.REDIS_URL;
    if (!redisUrl) {
        logger_1.logger.warn('REDIS_URL not set — session operations will fail until Redis is available');
        return;
    }
    try {
        const Redis = (await Promise.resolve().then(() => __importStar(require('ioredis')))).default;
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
            retryStrategy(times) {
                return Math.min(times * 200, 5000);
            },
            lazyConnect: true,
        });
        await redis.connect();
        await redis.ping();
        redisAvailable = true;
        logger_1.logger.info('Redis connection established for sessions');
        redis.on('error', (err) => {
            let reason;
            try {
                const m = err?.message;
                reason = m === undefined || m === null ? m : String(m);
            }
            catch {
                reason = 'unreadable thrown value';
            }
            logger_1.logger.error('Redis error', { error: reason });
            redisAvailable = false;
        });
        redis.on('reconnecting', () => {
            logger_1.logger.info('Redis reconnecting...');
        });
        redis.on('ready', () => {
            redisAvailable = true;
            logger_1.logger.info('Redis ready');
        });
    }
    catch (err) {
        let reason;
        try {
            const m = err?.message;
            reason = m === undefined || m === null ? m : `${m}`;
        }
        catch {
            reason = 'unreadable thrown value';
        }
        logger_1.logger.warn('Redis unavailable — using in-memory session fallback', { error: reason });
        redisAvailable = false;
    }
}
/** Returns the underlying Redis client (or null if not connected) */
function getRedisClient() {
    return redisAvailable ? redis : null;
}
/** Whether the Redis session store is currently reachable */
function isRedisAvailable() {
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
const MAX_SESSIONS_BROWSER = parseInt(process.env.MAX_SESSIONS_PER_USER_BROWSER || `${MAX_SESSIONS_PER_USER_LEGACY ?? 10}`, 10);
const MAX_SESSIONS_NATIVE = parseInt(process.env.MAX_SESSIONS_PER_USER_NATIVE || `${MAX_SESSIONS_PER_USER_LEGACY ?? 10}`, 10);
const SESSION_TTL_SECONDS = SESSION_EXPIRY_HOURS * 3600;
function capForClientType(clientType) {
    if (clientType === 'api')
        return 1;
    if (clientType === 'native')
        return MAX_SESSIONS_NATIVE;
    return MAX_SESSIONS_BROWSER;
}
// Redis key helpers
const sessionKey = (id) => `sess:${id}`;
const userSessionsKey = (userId) => `user_sessions:${userId}`;
function generateSessionId() {
    return `sess_${crypto_1.default.randomBytes(32).toString('hex')}`;
}
// =============================================================================
// SESSION CRUD
// =============================================================================
/** Create a new session */
async function createSession(user, ipAddress, userAgent, deviceId, clientType = 'browser', mintedBy) {
    const sessionId = generateSessionId();
    const now = new Date();
    const expiresAt = new Date(now.getTime() + SESSION_EXPIRY_HOURS * 3600000);
    const session = {
        id: sessionId,
        userId: user.id,
        token: crypto_1.default.randomBytes(32).toString('hex'),
        refreshToken: crypto_1.default.randomBytes(32).toString('hex'),
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
    const existingIds = await redis.smembers(userSessionsKey(user.id));
    const records = [];
    for (const sid of existingIds) {
        try {
            const raw = await redis.get(sessionKey(sid));
            if (raw) {
                const parsed = JSON.parse(raw);
                records.push({
                    id: sid,
                    createdAt: new Date(parsed.createdAt ?? 0).getTime(),
                    // Legacy records pre-KS-43 have no clientType; treat as 'browser'
                    // since that was the only multi-session path before this fix.
                    clientType: parsed.clientType ?? 'browser',
                    deviceId: parsed.deviceId,
                });
            }
            else {
                // Dangling set member with no backing record — evict on sight.
                records.push({ id: sid, createdAt: 0, clientType: 'browser' });
            }
        }
        catch {
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
        for (const r of records.filter((rec) => rec.clientType === clientType && rec.deviceId === deviceId)) {
            await revokeSession(r.id);
        }
    }
    // (3) Per-cohort LRU eviction. Re-read the set (steps 1-2 may have just
    // shrunk it) and only count records of the same clientType.
    const refreshedIds = await redis.smembers(userSessionsKey(user.id));
    const sameCohort = records.filter((r) => r.clientType === clientType && refreshedIds.includes(r.id));
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
    logger_1.logger.info('Session created', { sessionId, userId: user.id, clientType });
    return session;
}
/** Get session by ID */
async function getSession(sessionId) {
    if (!redisAvailable)
        return null;
    const data = await redis.get(sessionKey(sessionId));
    if (!data)
        return null;
    const session = JSON.parse(data);
    // Rehydrate dates
    session.expiresAt = new Date(session.expiresAt);
    session.lastActivityAt = new Date(session.lastActivityAt);
    session.createdAt = new Date(session.createdAt);
    if (session.revokedAt)
        session.revokedAt = new Date(session.revokedAt);
    if (new Date() > session.expiresAt || !session.isActive)
        return null;
    return session;
}
/** Update session activity */
async function updateSessionActivity(sessionId) {
    if (!redisAvailable)
        return;
    const data = await redis.get(sessionKey(sessionId));
    if (data) {
        const session = JSON.parse(data);
        session.lastActivityAt = new Date();
        await redis.setex(sessionKey(sessionId), SESSION_TTL_SECONDS, JSON.stringify(session));
    }
}
/** Rotate refresh token — invalidates the old one by updating the session in Redis */
async function rotateSessionRefreshToken(sessionId, newRefreshToken) {
    if (!redisAvailable)
        return;
    const data = await redis.get(sessionKey(sessionId));
    if (!data)
        return;
    const session = JSON.parse(data);
    session.refreshToken = newRefreshToken;
    session.lastActivityAt = new Date();
    await redis.setex(sessionKey(sessionId), SESSION_TTL_SECONDS, JSON.stringify(session));
    logger_1.logger.debug('Session refresh token rotated', { sessionId });
}
/** Revoke session */
async function revokeSession(sessionId) {
    if (!redisAvailable)
        return false;
    const data = await redis.get(sessionKey(sessionId));
    if (!data)
        return false;
    const session = JSON.parse(data);
    session.isActive = false;
    session.revokedAt = new Date();
    // Keep for audit but with short TTL
    await redis.setex(sessionKey(sessionId), 3600, JSON.stringify(session));
    await redis.srem(userSessionsKey(session.userId), sessionId);
    logger_1.logger.info('Session revoked', { sessionId, userId: session.userId });
    return true;
}
/** Revoke all sessions for a user */
async function revokeAllUserSessions(userId) {
    if (!redisAvailable)
        return 0;
    let count = 0;
    const sessionIds = await redis.smembers(userSessionsKey(userId));
    for (const sid of sessionIds) {
        if (await revokeSession(sid))
            count++;
    }
    await redis.del(userSessionsKey(userId));
    logger_1.logger.info('All sessions revoked', { userId, count });
    return count;
}
/** Get all active sessions for a user */
async function getUserSessions(userId) {
    if (!redisAvailable)
        return [];
    const sessionIds = await redis.smembers(userSessionsKey(userId));
    if (sessionIds.length === 0)
        return [];
    const keys = sessionIds.map((sid) => sessionKey(sid));
    const results = await redis.mget(...keys);
    const sessions = [];
    const now = new Date();
    for (const data of results) {
        if (data) {
            const session = JSON.parse(data);
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
async function validateSession(sessionId) {
    const session = await getSession(sessionId);
    return session !== null && session.isActive;
}
/** Extend session expiry */
async function extendSession(sessionId) {
    const session = await getSession(sessionId);
    if (!session || !session.isActive)
        return null;
    session.expiresAt = new Date(Date.now() + SESSION_EXPIRY_HOURS * 3600000);
    session.lastActivityAt = new Date();
    if (!redisAvailable)
        return null;
    await redis.setex(sessionKey(sessionId), SESSION_TTL_SECONDS, JSON.stringify(session));
    return session;
}
/** Clean up expired sessions */
async function cleanupExpiredSessions() {
    // Redis handles TTL-based expiry automatically — nothing to clean up.
    return 0;
}
