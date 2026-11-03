// Gate 175 recorder for PR 1991: the REAL redis-client connect (ioredis replaced by vi.mock) and the REAL ConnectionPool
// (createConnection via acquire/initialize/performMaintenance, removeConnection via maintenance). Real winston logger.
import { describe, it, vi } from 'vitest';
import fs from 'node:fs';
import { VALUES, capture, kind, hits } from './values';

const OUT = process.env.GATE175_OUT as string;
const TAG = process.env.GATE175_TAG as string;
const rec = (o: Record<string, unknown>) => fs.appendFileSync(OUT, JSON.stringify({ tag: TAG, ...o }) + '\n');

const h = vi.hoisted(() => ({ v: undefined as unknown }));
vi.mock('ioredis', () => {
  class Redis {
    on() {
      return this;
    }
    connect() {
      return Promise.reject(h.v);
    }
    disconnect() {}
    quit() {
      return Promise.resolve();
    }
  }
  return { default: Redis, Redis };
});

import { redisClient } from '../cache/redis-client';
import { getSecurityStores } from '../security/redis-security-store';
import { ConnectionPool } from '../cache/connection-pool';

const unhandled: unknown[] = [];
process.on('unhandledRejection', (r) => {
  unhandled.push(r);
});

describe('gate175 PR1991 client + pool recorder', () => {
  it('Q5b redisClient.connect and its in-file caller getSecurityStores', async () => {
    for (const [name, make] of VALUES) {
      const v = make();
      h.v = v;
      (redisClient as any).client = null;
      (redisClient as any).isConnected = false;
      const a = await capture(async () => {
        try {
          await redisClient.connect();
          return 'resolved';
        } catch (e) {
          return 'rejected ' + kind(e, v);
        }
      });
      rec({ q: 'Q5b', site: 'redisClient.connect', value: name, out: a.result, sentinelLines: hits(a.lines) });
      (redisClient as any).client = null;
      (redisClient as any).isConnected = false;
      const b = await capture(async () => {
        try {
          const s = await getSecurityStores();
          return 'resolved isRedis=' + s.isRedis;
        } catch (e) {
          return 'rejected ' + kind(e, v);
        }
      });
      rec({ q: 'Q5b', site: 'caller getSecurityStores', value: name, out: b.result, sentinelLines: hits(b.lines) });
    }
  });

  it('Q5d ConnectionPool maintenance on its REAL setInterval (startMaintenance), factory failing', async () => {
    for (const [name, make] of VALUES) {
      const v = make();
      let factoryCalls = 0;
      const pool: any = new ConnectionPool(
        async () => {
          factoryCalls += 1;
          throw v;
        },
        undefined,
        { min: 1, max: 2, maxRetries: 3, createRetryMs: 0, acquireTimeoutMs: 30, idleTimeoutMs: 40 },
      );
      const before = unhandled.length;
      const r = await capture(async () => {
        pool.startMaintenance();
        await new Promise((res) => setTimeout(res, 70));
        clearInterval(pool.maintenanceInterval);
        await new Promise((res) => setTimeout(res, 10));
        return 'ran';
      });
      const got = unhandled.slice(before);
      rec({ q: 'Q5d', site: 'pool maintenance interval', value: name, out: r.result, ticksWithFactoryCalls: factoryCalls > 0, unhandledRejections: got.length, sentinelLines: hits(r.lines) });
    }
  });

  it('Q5c ConnectionPool create paths and removeConnection', async () => {
    const mkConn = (closeThrows?: unknown) => ({
      id: 'c',
      createdAt: new Date(),
      lastUsedAt: new Date(0),
      isValid: async () => true,
      close: async () => {
        if (closeThrows !== undefined) throw closeThrows;
      },
    });
    for (const [name, make] of VALUES) {
      for (const path of ['createConnection direct', 'caller acquire', 'caller initialize', 'caller performMaintenance (create)', 'removeConnection via maintenance (close throws)']) {
        const v = make();
        let factoryCalls = 0;
        const factory = async () => {
          factoryCalls += 1;
          if (path.startsWith('removeConnection')) return mkConn(v) as any;
          throw v;
        };
        const pool: any = new ConnectionPool(factory, undefined, { min: 1, max: 2, maxRetries: 3, createRetryMs: 0, acquireTimeoutMs: 30, idleTimeoutMs: 1 });
        let removed = 0;
        pool.on('connectionRemoved', () => (removed += 1));
        const before = unhandled.length;
        const r = await capture(async () => {
          try {
            if (path === 'createConnection direct') await pool.createConnection();
            else if (path === 'caller acquire') await pool.acquire();
            else if (path === 'caller initialize') {
              await pool.initialize();
              if (pool.maintenanceInterval) clearInterval(pool.maintenanceInterval);
            } else if (path === 'caller performMaintenance (create)') await pool.performMaintenance();
            else {
              await pool.createConnection();
              await pool.createConnection();
              pool.connections.forEach((c: any) => (c.lastUsedAt = new Date(0)));
              await new Promise((res) => setTimeout(res, 5));
              await pool.performMaintenance();
            }
            return 'resolved';
          } catch (e) {
            return 'rejected ' + kind(e, v);
          }
        });
        if (pool.maintenanceInterval) clearInterval(pool.maintenanceInterval);
        await new Promise((res) => setTimeout(res, 5));
        rec({ q: 'Q5c', site: `pool ${path}`, value: name, out: r.result, factoryCalls, removedEvents: removed, unhandledRejections: unhandled.length - before, sentinelLines: hits(r.lines) });
      }
    }
  });
});
