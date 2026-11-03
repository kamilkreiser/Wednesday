/**
 * =============================================================================
 * REFRESH-TOKEN DENYLIST — audit A-05
 * =============================================================================
 * When a refresh token is rotated (or its session revoked at logout), the
 * old token's jti goes here so it can't be replayed for the rest of its
 * natural lifetime. Stored in the same Redis instance as sessions; the key
 * carries its own TTL so cleanup is automatic.
 *
 * Threat model: an attacker who steals a refresh token (XSS, malware,
 * shoulder-surf, hostile router) can otherwise keep using it for up to
 * 7 days even after the legitimate user rotates — because the rotation
 * path here only updates a hex string in the session record that nothing
 * compares against.
 * =============================================================================
 */

import { getRedisClient } from './session';
import { logger } from '../utils/logger';

const denylistKey = (jti: string) => `refresh_denylist:${jti}`;

/**
 * Add a refresh-token jti to the denylist. ttlSeconds should be the refresh
 * token's remaining lifetime — past that, even an "allowed" reuse would fail
 * JWT verification, so there's no value in keeping the entry around longer.
 */
export async function denylistRefreshJti(jti: string, ttlSeconds: number): Promise<void> {
  const redis = getRedisClient();
  if (!redis) {
    // Fail loud — without Redis the denylist isn't enforceable, and silent
    // skip would mean A-05 silently regresses.
    logger.error('[RefreshDenylist] Redis unavailable — cannot denylist refresh jti', { jti });
    throw new Error('Refresh denylist requires Redis');
  }
  if (ttlSeconds <= 0) return; // Already expired naturally — nothing to do.
  await redis.setex(denylistKey(jti), ttlSeconds, '1');
}

/**
 * Returns true if this jti has been denylisted (rotated, revoked, or logged out).
 * Callers MUST treat a true result as token-reuse and respond by killing the
 * entire session, not just rejecting this single request — that's the
 * "compromise detection" pattern from RFC 6819 §5.2.2.3.
 */
export async function isRefreshJtiDenylisted(jti: string): Promise<boolean> {
  const redis = getRedisClient();
  if (!redis) {
    // Fail closed: if we can't check, refuse the refresh. Redis outages are
    // recoverable; letting through a possibly-replayed token is not.
    logger.error('[RefreshDenylist] Redis unavailable — refusing refresh');
    return true;
  }
  const exists = await redis.exists(denylistKey(jti));
  return exists === 1;
}
