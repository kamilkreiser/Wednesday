// Gate 175 recorder for PR 1991: the three security stores, their in-file callers, and cacheMiddleware, driven as the
// REAL module over a stand-in redis client whose chosen operations reject with the cell's value. Real winston logger.
import { describe, it, vi } from 'vitest';
import fs from 'node:fs';
import { VALUES, capture, kind, hits } from './values';

const OUT = process.env.GATE175_OUT as string;
const TAG = process.env.GATE175_TAG as string;
const rec = (o: Record<string, unknown>) => fs.appendFileSync(OUT, JSON.stringify({ tag: TAG, ...o }) + '\n');

const h = vi.hoisted(() => ({ v: undefined as unknown, failOps: new Set<string>(), record: null as unknown }));
vi.mock('../cache/redis-client', () => {
  const op = (name: string, ok: () => unknown) => (..._a: unknown[]) => (h.failOps.has(name) ? Promise.reject(h.v) : Promise.resolve(ok()));
  return {
    CACHE_TTL: { SESSION: 300, SHORT: 60, MEDIUM: 300, LONG: 3600 },
    CACHE_PREFIX: {},
    redisClient: {
      get: op('get', () => (h.record ? JSON.parse(JSON.stringify(h.record)) : h.record)),
      set: op('set', () => undefined),
      delete: op('delete', () => true),
      incrWithExpiry: op('incrWithExpiry', () => 999),
      ttl: op('ttl', () => 10),
      exists: op('exists', () => true),
      isReady: () => true,
      connect: op('connect', () => undefined),
      ping: op('ping', () => true),
    },
  };
});

import { RedisRateLimitStore, RedisBruteForceStore, RedisCSRFStore } from '../security/redis-security-store';
import { cacheMiddleware } from '../cache/cache-middleware';

type Call = { site: string; fail: string[]; record?: unknown; run: () => Promise<unknown> };

const blocked = { attempts: 99, lastAttempt: Date.now(), blockedUntil: Date.now() + 3600_000 };
const CALLS: Call[] = [
  { site: 'RateLimit.get', fail: ['get'], run: () => new RedisRateLimitStore().get('k') },
  { site: 'RateLimit.increment', fail: ['incrWithExpiry'], run: () => new RedisRateLimitStore().increment('k', 60000) },
  { site: 'BruteForce.get', fail: ['get'], run: () => new RedisBruteForceStore().get('k') },
  { site: 'BruteForce.set', fail: ['set'], run: () => new RedisBruteForceStore().set('k', blocked) },
  { site: 'CSRF.generate', fail: ['set'], run: () => new RedisCSRFStore().generate('s') },
  { site: 'CSRF.validate', fail: ['get'], run: () => new RedisCSRFStore().validate('s', 'a'.repeat(64)) },
  // in-file callers (no caller of these stores exists elsewhere in the repo at head; see verdict)
  { site: 'caller BruteForce.isBlocked (get fails; stored record says BLOCKED)', fail: ['get'], record: blocked, run: () => new RedisBruteForceStore().isBlocked('k') },
  { site: 'caller BruteForce.getAttempts (get fails)', fail: ['get'], record: blocked, run: () => new RedisBruteForceStore().getAttempts('k') },
  { site: 'caller BruteForce.recordFailure (get fails)', fail: ['get'], record: blocked, run: () => new RedisBruteForceStore().recordFailure('k', { freeRetries: 3, minWait: 1000, maxWait: 60000, lifetime: 300000 }) },
  { site: 'caller BruteForce.recordFailure (set fails)', fail: ['set'], record: blocked, run: () => new RedisBruteForceStore().recordFailure('k', { freeRetries: 3, minWait: 1000, maxWait: 60000, lifetime: 300000 }) },
  { site: 'caller CSRF.refresh (set fails)', fail: ['set'], run: () => new RedisCSRFStore().refresh('s') },
];

const summarise = (x: unknown): string => {
  if (x === null || x === undefined) return String(x);
  if (typeof x === 'string') return x.length === 64 ? '<64-hex token>' : x;
  try {
    const o = JSON.parse(JSON.stringify(x));
    if (o && typeof o === 'object') {
      if ('resetAt' in o) o.resetAt = '<t>';
      if ('lastAttempt' in o) o.lastAttempt = '<t>';
      if ('blockedUntil' in o) o.blockedUntil = '<t>';
      if ('retryAfter' in o) o.retryAfter = '<n>';
    }
    return JSON.stringify(o);
  } catch {
    return '<unserialisable>';
  }
};

describe('gate175 PR1991 stores recorder', () => {
  it('Q4 stores and in-file callers', async () => {
    for (const c of CALLS) {
      for (const [name, make] of VALUES) {
        const v = make();
        h.v = v;
        h.failOps = new Set(c.fail);
        h.record = c.record ?? null;
        const { result, lines } = await capture(async () => {
          try {
            return 'returned ' + summarise(await c.run());
          } catch (e) {
            return 'threw ' + kind(e, v);
          }
        });
        rec({ q: 'Q4', site: c.site, value: name, out: result, sentinelLines: hits(lines) });
      }
    }
  });

  it('Q5a cacheMiddleware lookup fails, and downstream next throws', async () => {
    for (const trig of ['redis.get fails', 'downstream next() throws']) {
      for (const [name, make] of VALUES) {
        const v = make();
        h.v = v;
        h.failOps = new Set(trig === 'redis.get fails' ? ['get'] : []);
        h.record = null;
        const mw = cacheMiddleware({ ttl: 60 } as never);
        let nextCalls = 0;
        const res: any = { statusCode: 200, setHeader() {}, getHeader() {}, status() { return res; }, json() { return res; } };
        const { result, lines } = await capture(async () => {
          try {
            await mw({ method: 'GET', originalUrl: '/x', url: '/x', path: '/x', query: {}, headers: {} } as never, res, () => {
              nextCalls += 1;
              if (trig.startsWith('downstream') && nextCalls === 1) throw v;
            });
            return 'resolved';
          } catch (e) {
            return 'rejected ' + kind(e, v);
          }
        });
        rec({ q: 'Q5a', site: `cacheMiddleware via ${trig}`, value: name, out: result, nextCalls, sentinelLines: hits(lines) });
      }
    }
  });
});
