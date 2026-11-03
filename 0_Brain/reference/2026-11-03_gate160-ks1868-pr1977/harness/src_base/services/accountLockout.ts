/**
 * =============================================================================
 * ACCOUNT LOCKOUT (pen-test F-06)
 * =============================================================================
 * Defence-in-depth on top of the per-IP login rate limit. The rate limiter
 * stops a single IP hammering the endpoint; this service stops a single
 * email being targeted across IPs (credential stuffing distributed).
 *
 * Behaviour:
 *   - 5 failed attempts within 15 minutes → 15 minute lockout.
 *   - Counter is keyed by (email_lowercased, source_ip_/24) so an
 *     attacker rotating IPs in a single /24 cannot trivially bypass it,
 *     while legitimate users on the same office NAT aren't all locked
 *     out by one user's typos.
 *   - Lockout returns InvalidCredentialsError to the caller — same shape
 *     as a wrong password (pen-test F-11 — no user enumeration).
 *
 * Storage: Redis (uses the existing session.ts client). If Redis is down,
 * lockout fails OPEN — i.e. requests proceed. This is the conservative
 * choice for availability; the per-IP rate limiter is still the load-
 * bearing first line of defence.
 *
 * Test surface: every public function takes the redis client + clock as
 * arguments so tests don't need a real Redis or `Date.now()` mock.
 * =============================================================================
 */

import { logger } from '../utils/logger';

const LOCKOUT_THRESHOLD = parseInt(process.env.LOGIN_LOCKOUT_THRESHOLD || '5', 10);
const COUNTER_WINDOW_MS = parseInt(process.env.LOGIN_LOCKOUT_WINDOW_MS || `${15 * 60 * 1000}`, 10);
const LOCKOUT_DURATION_MS = parseInt(process.env.LOGIN_LOCKOUT_DURATION_MS || `${15 * 60 * 1000}`, 10);

/** Reduce an IPv4 to its /24 prefix string for keying. IPv6 keys on the address. */
export function ipPrefix(ip: string): string {
  if (!ip) return 'unknown';
  // Strip IPv6-in-v4 prefix
  const stripped = ip.replace(/^::ffff:/, '');
  if (stripped.includes('.')) {
    const parts = stripped.split('.');
    if (parts.length === 4) return `${parts[0]}.${parts[1]}.${parts[2]}.0/24`;
  }
  return stripped;
}

/**
 * KS-781 N-6 — NORMALISE HERE, IN THE PRIMITIVE, NOT IN EACH CALLER.
 *
 * These keys lowercased but did not trim, while `userRepo.getUserByEmail`
 * lowercases AND trims. The two consumers of one address therefore disagreed:
 * `" victim@example.com"` resolved the victim's row while producing a lockout
 * key nothing had ever incremented. That was KS-781 F-1 — a lockout defeated by
 * one space, measured at 30 of 30 attempts across six whitespace variants.
 *
 * F-1 was closed by normalising in the two callers. That is a convention, and a
 * convention holds only while every future caller remembers it — doors 2 and 3
 * (KS-795 / KS-796) add callers. Trimming in the derivation makes it structural.
 * Idempotent for both current callers, which already pass a trimmed address:
 * `routes/auth.ts:310` (via `loginSchema`'s `z.string().trim()`) and
 * `services/passwordLoginGate.ts:119` (via the gate's own normalisation).
 */
function normaliseEmailForKey(email: string): string {
  return String(email).toLowerCase().trim();
}

function counterKey(email: string, ip: string): string {
  return `lockout:counter:${normaliseEmailForKey(email)}:${ipPrefix(ip)}`;
}
function lockoutKey(email: string, ip: string): string {
  return `lockout:locked:${normaliseEmailForKey(email)}:${ipPrefix(ip)}`;
}

export interface LockoutClient {
  get(key: string): Promise<string | null>;
  set(key: string, value: string, mode?: string, ttl?: number): Promise<unknown>;
  incr(key: string): Promise<number>;
  expire(key: string, seconds: number): Promise<unknown>;
  del(...keys: string[]): Promise<unknown>;
}

/**
 * True iff the (email, ip) is currently locked out. Caller should treat
 * lockout the same as a wrong-password attempt: throw
 * InvalidCredentialsError, do not differentiate.
 */
export async function isLockedOut(redis: LockoutClient | null, email: string, ip: string): Promise<boolean> {
  if (!redis) return false;
  try {
    const v = await redis.get(lockoutKey(email, ip));
    return v !== null;
  } catch (err: any) {
    logger.warn('lockout: redis error on isLockedOut — failing open', { error: err?.message });
    return false;
  }
}

/**
 * Record a failed login attempt. If the counter crosses the threshold,
 * set the lockout flag with TTL. Returns the new failure count so the
 * caller can log it (do NOT surface to the client — that's enumeration).
 */
export async function recordFailure(redis: LockoutClient | null, email: string, ip: string): Promise<number> {
  if (!redis) return 0;
  try {
    const ck = counterKey(email, ip);
    const count = await redis.incr(ck);
    if (count === 1) {
      // First failure — start the rolling window.
      await redis.expire(ck, Math.ceil(COUNTER_WINDOW_MS / 1000));
    }
    if (count >= LOCKOUT_THRESHOLD) {
      await redis.set(lockoutKey(email, ip), '1', 'EX', Math.ceil(LOCKOUT_DURATION_MS / 1000));
      logger.warn('lockout: threshold reached — account locked', {
        emailHash: hashEmail(email),
        ipPrefix: ipPrefix(ip),
        count,
        durationMs: LOCKOUT_DURATION_MS,
      });
    }
    return count;
  } catch (err: any) {
    logger.warn('lockout: redis error on recordFailure — continuing', { error: err?.message });
    return 0;
  }
}

/** Clear counter + lockout on successful authentication. */
export async function recordSuccess(redis: LockoutClient | null, email: string, ip: string): Promise<void> {
  if (!redis) return;
  try {
    await redis.del(counterKey(email, ip), lockoutKey(email, ip));
  } catch (err: any) {
    logger.warn('lockout: redis error on recordSuccess — non-fatal', { error: err?.message });
  }
}

function hashEmail(email: string): string {
  // Truncated SHA-256 for log correlation without storing the email itself
  const crypto = require('crypto') as typeof import('crypto');
  // Same normalisation as the keys: a padded address must not produce a second
  // identifier in the logs for the same account.
  return crypto.createHash('sha256').update(normaliseEmailForKey(email)).digest('hex').slice(0, 12);
}
