/**
 * KS-164 — API-key (machine) callers must be governed by the per-client
 * rate limiter.
 *
 * Regression: the API-key auth path built `req.user` without copying the
 * connector's `rateLimit`, so `enforceClientRateLimit` saw no limit and let
 * API-key traffic bypass the per-key ceiling. These tests lock:
 *   - a machine caller with a configured rateLimit IS enforced (429 over limit)
 *   - interactive/human auth methods are NOT enforced here (global limiter)
 *   - a machine caller WITHOUT a rateLimit is NOT silently bypassed (default)
 */

import { describe, it, expect, vi } from 'vitest';
import { enforceClientRateLimit } from '../middleware/rateLimitEnforce';

type MockRes = {
  setHeader: ReturnType<typeof vi.fn>;
  status: ReturnType<typeof vi.fn>;
  json: ReturnType<typeof vi.fn>;
  statusCode?: number;
};

function makeRes(): MockRes {
  const res: MockRes = {
    setHeader: vi.fn(),
    status: vi.fn(),
    json: vi.fn(),
  };
  res.status.mockImplementation((code: number) => {
    res.statusCode = code;
    return res;
  });
  return res;
}

// In-memory limiter (no redis client) — each test uses a unique connectorId so
// the module-level counter map doesn't leak between tests.
const mw = enforceClientRateLimit();

async function run(user: Record<string, unknown> | undefined) {
  const req = { user } as any;
  const res = makeRes();
  const next = vi.fn();
  await mw(req, res, next);
  return { res, next };
}

describe('enforceClientRateLimit (KS-164)', () => {
  it('enforces the per-key ceiling for an api_key caller (429 over limit)', async () => {
    const user = { authMethod: 'api_key', connectorId: 'ks164-enforced', rateLimit: 2, rateLimitWindow: 60 };

    const first = await run(user);
    expect(first.next).toHaveBeenCalledOnce();
    expect(first.res.statusCode).toBeUndefined();

    const second = await run(user);
    expect(second.next).toHaveBeenCalledOnce();
    expect(second.res.statusCode).toBeUndefined();

    const third = await run(user);
    expect(third.next).not.toHaveBeenCalled();
    expect(third.res.statusCode).toBe(429);
    expect(third.res.json).toHaveBeenCalledWith(
      expect.objectContaining({ error: expect.objectContaining({ code: 'RATE_LIMIT_EXCEEDED' }) }),
    );
  });

  it.each(['email', 'wallet', 'federated', 'social', 'jwt'])(
    'does NOT enforce the per-client limiter on interactive method "%s"',
    async (authMethod) => {
      const { res, next } = await run({ authMethod, userId: `human-${authMethod}`, rateLimit: 1 });
      expect(next).toHaveBeenCalledOnce();
      expect(res.statusCode).toBeUndefined();
      expect(res.setHeader).not.toHaveBeenCalled();
    },
  );

  it('passes through when there is no authenticated user', async () => {
    const { res, next } = await run(undefined);
    expect(next).toHaveBeenCalledOnce();
    expect(res.setHeader).not.toHaveBeenCalled();
  });

  it('does NOT silently bypass a machine caller missing rateLimit (applies default)', async () => {
    const { res, next } = await run({ authMethod: 'api_key', connectorId: 'ks164-no-limit' });
    // Entered enforcement (headers set) rather than bypassing.
    expect(res.setHeader).toHaveBeenCalledWith('X-RateLimit-Limit', '100');
    expect(next).toHaveBeenCalledOnce();
  });
});

describe('enforceClientRateLimit — shared Redis counter (KS-170)', () => {
  it('uses the ioredis distributed counter (incr/pexpire/pttl) and 429s over the limit', async () => {
    let n = 0;
    const redis = {
      status: 'ready',
      incr: vi.fn(async () => ++n),
      pexpire: vi.fn(async () => 1),
      pttl: vi.fn(async () => 60_000),
    };
    // Inject the mock client (production resolves it lazily via getRedisClient).
    const redisMw = enforceClientRateLimit(redis);
    const user = { authMethod: 'api_key', connectorId: 'ks170-redis', rateLimit: 1, rateLimitWindow: 60 };
    const hit = async () => {
      const req = { user } as any;
      const res = makeRes();
      const next = vi.fn();
      await redisMw(req, res, next);
      return { res, next };
    };

    // 1st request: counted in Redis, window set once, allowed.
    const first = await hit();
    expect(redis.incr).toHaveBeenCalledWith('ratelimit:ks170-redis');
    expect(redis.pexpire).toHaveBeenCalledOnce();
    expect(first.next).toHaveBeenCalledOnce();
    expect(first.res.statusCode).toBeUndefined();

    // 2nd request exceeds the limit of 1 → 429, and the window is NOT re-set.
    const second = await hit();
    expect(second.next).not.toHaveBeenCalled();
    expect(second.res.statusCode).toBe(429);
    expect(redis.pexpire).toHaveBeenCalledOnce();
  });

  it('falls back to the in-memory counter when Redis is not ready', async () => {
    const redis = {
      status: 'connecting',
      incr: vi.fn(),
      pexpire: vi.fn(),
      pttl: vi.fn(),
    };
    const redisMw = enforceClientRateLimit(redis);
    const user = { authMethod: 'api_key', connectorId: 'ks170-fallback', rateLimit: 5, rateLimitWindow: 60 };
    const req = { user } as any;
    const res = makeRes();
    const next = vi.fn();
    await redisMw(req, res, next);

    // Redis not ready → in-memory path; no Redis commands issued.
    expect(redis.incr).not.toHaveBeenCalled();
    expect(next).toHaveBeenCalledOnce();
    expect(res.setHeader).toHaveBeenCalledWith('X-RateLimit-Limit', '5');
  });
});

/**
 * KS-616 — a Redis command that THROWS must not remove the ceiling.
 *
 * This is the surviving half of Review F's F-6. The other half (per-replica
 * counters) closed with KS-170, so the finding read as resolved while
 * `catch (err) { next(); }` still allowed every request through with no limit
 * applied at all — and did it silently, at exactly the moment load makes Redis
 * wobble.
 *
 * Note this is NOT the "Redis is down" path: that is handled by the readiness
 * branch above and is covered by the KS-170 test. This is Redis reporting
 * `status: 'ready'` and then failing mid-command.
 *
 * RED-PROOF: against the previous implementation the first test below fails on
 * its 3rd request — old code called next() so statusCode was undefined where
 * 429 is expected — and the second fails because no headers were ever set.
 */
describe('enforceClientRateLimit — degraded ceiling on Redis error (KS-616)', () => {
  function throwingRedis() {
    return {
      status: 'ready',
      incr: vi.fn().mockRejectedValue(new Error('READONLY You cannot write against a read only replica')),
      pexpire: vi.fn(),
      pttl: vi.fn(),
    };
  }

  it('still enforces the limit when the Redis counter throws (degrades, does not disable)', async () => {
    const redis = throwingRedis();
    const mwErr = enforceClientRateLimit(redis);
    const user = { authMethod: 'api_key', connectorId: 'ks616-degrade', rateLimit: 2, rateLimitWindow: 60 };
    const hit = async () => {
      const req = { user } as any;
      const res = makeRes();
      const next = vi.fn();
      await mwErr(req, res, next);
      return { res, next };
    };

    // Limit is 2: the first two are allowed, the third must be refused.
    const first = await hit();
    expect(first.next).toHaveBeenCalledOnce();
    expect(first.res.statusCode).toBeUndefined();

    const second = await hit();
    expect(second.next).toHaveBeenCalledOnce();
    expect(second.res.statusCode).toBeUndefined();

    const third = await hit();
    expect(third.next).not.toHaveBeenCalled();
    expect(third.res.statusCode).toBe(429);

    // The Redis path was genuinely attempted and genuinely failed each time —
    // otherwise this would be testing the readiness branch by accident.
    expect(redis.incr).toHaveBeenCalledTimes(3);
  });

  it('still reports rate-limit headers while degraded', async () => {
    const redis = throwingRedis();
    const mwErr = enforceClientRateLimit(redis);
    const user = { authMethod: 'api_key', connectorId: 'ks616-headers', rateLimit: 9, rateLimitWindow: 60 };
    const req = { user } as any;
    const res = makeRes();
    const next = vi.fn();
    await mwErr(req, res, next);

    expect(next).toHaveBeenCalledOnce();
    expect(res.setHeader).toHaveBeenCalledWith('X-RateLimit-Limit', '9');
    expect(res.setHeader).toHaveBeenCalledWith('X-RateLimit-Remaining', '8');
  });

  it('returns a 429 body a caller can act on, not a bare status', async () => {
    const redis = throwingRedis();
    const mwErr = enforceClientRateLimit(redis);
    const user = { authMethod: 'api_key', connectorId: 'ks616-body', rateLimit: 1, rateLimitWindow: 60 };
    const hit = async () => {
      const req = { user } as any;
      const res = makeRes();
      const next = vi.fn();
      await mwErr(req, res, next);
      return { res, next };
    };

    await hit();
    const blocked = await hit();
    expect(blocked.res.statusCode).toBe(429);
    const payload = blocked.res.json.mock.calls[0][0];
    expect(payload.success).toBe(false);
    expect(payload.error.code).toBe('RATE_LIMIT_EXCEEDED');
    expect(payload.error.details.limit).toBe(1);
    expect(payload.error.details.retryAfter).toBeGreaterThan(0);
  });
});
