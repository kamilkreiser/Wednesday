// Gate 175 recorder for PR 1990. Drives the REAL modules (key-vault, jwt.ts from services/auth, tenant-rate-limiter,
// tenant-pool-manager, tenant-context, auto-migrate) with every value class, and writes one JSON line per cell to
// $GATE175_OUT. Stand-ins: the Azure vault client (instance field), pg (vi.mock), ioredis (Module._load hook), req/res.
import { describe, it, vi, expect } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import Module from 'node:module';
import { VALUES, capture, kind, hits } from './values';

const OUT = process.env.GATE175_OUT as string;
const TAG = process.env.GATE175_TAG as string;
const rec = (o: Record<string, unknown>) => fs.appendFileSync(OUT, JSON.stringify({ tag: TAG, ...o }) + '\n');

const h = vi.hoisted(() => ({ pgMode: 'ok' as string, toThrow: undefined as unknown, rows: [] as unknown[] }));
vi.mock('pg', () => {
  class Pool {
    async query(text: string) {
      if (h.pgMode === 'platform-fail') return Promise.reject(h.toThrow);
      return { rows: h.rows, rowCount: h.rows.length };
    }
    on() {
      return this;
    }
    async connect() {
      return {
        query: (text: string) => (text === 'SELECT 175;' ? Promise.reject(h.toThrow) : Promise.resolve({ rows: [] })),
        release: () => undefined,
      };
    }
    async end() {}
  }
  return { default: { Pool }, Pool };
});

// Two RSA keys generated in memory only: A = the environment's, B = the vault's. Never written anywhere.
const mk = () => {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
  return {
    b64: Buffer.from(privateKey.export({ type: 'pkcs8', format: 'pem' }).toString()).toString('base64'),
    pub: publicKey.export({ type: 'spki', format: 'pem' }).toString(),
  };
};
const KA = mk();
const KB = mk();
const which = (pub: string) => (pub === KA.pub ? 'ENV key A' : pub === KB.pub ? 'VAULT key B' : 'unknown');

describe('gate175 PR1990 recorder', () => {
  it('Q1a getSecret direct, fallbackToEnv true and false', async () => {
    const { SecretsManager } = await import('../vault/key-vault');
    for (const [name, make] of VALUES) {
      for (const fb of [true, false]) {
        process.env.GATE175_SECRET = 'env-value';
        const v = make();
        const mgr = new SecretsManager({ vaultUrl: 'https://gate175.vault.invalid', fallbackToEnv: fb, cacheTimeMs: 300000 });
        const inner = mgr as any;
        inner.vaultInitAttempted = true;
        inner.vaultClient = { getSecret: () => Promise.reject(v) };
        const { result, lines } = await capture(async () => {
          try {
            return { out: 'returned ' + (await mgr.getSecret('gate175-secret')) };
          } catch (e) {
            return { out: 'threw ' + kind(e, v) };
          }
        });
        const cached = inner.cache.get('gate175-secret');
        rec({ q: 'Q1a', site: `getSecret fallbackToEnv=${fb}`, value: name, out: result.out, cached: cached ? cached.value : null, sentinelLines: hits(lines) });
      }
    }
    delete process.env.GATE175_SECRET;
  });

  it('Q1b jwt.ts initJwtKeys through the real getSecret, then vault recovers', async () => {
    const exitSpy = vi.spyOn(process, 'exit').mockImplementation(((c: number) => {
      throw new Error(`process.exit(${c})`);
    }) as never);
    for (const [name, make] of VALUES) {
      vi.resetModules();
      process.env.AZURE_KEY_VAULT_URL = 'https://gate175.vault.invalid';
      process.env.JWT_PRIVATE_KEY = KA.b64;
      process.env.JWT_KEY_ID = 'kid-env';
      const kv = await import('@secuura/shared/vault/key-vault');
      const jwt = await import('../../../../services/auth/src/services/jwt');
      const sm = kv.getSecretsManager({ fallbackToEnv: true }) as any;
      let phase = 'fail';
      const v = make();
      sm.vaultInitAttempted = true;
      sm.vaultClient = {
        getSecret: (n: string) =>
          phase === 'fail' ? Promise.reject(v) : Promise.resolve({ value: n === 'jwt-private-key' ? KB.b64 : 'kid-vault' }),
      };
      const run1 = await capture(async () => {
        try {
          await jwt.initJwtKeys();
          const j = jwt.getActiveJwk();
          return `key=${which(j.publicKeyPem)} kid=${j.kid}`;
        } catch (e) {
          return 'threw ' + kind(e, v);
        }
      });
      const cacheAfter1 = [...sm.cache.keys()].sort().join(',');
      phase = 'ok';
      const run2 = await capture(async () => {
        try {
          await jwt.initJwtKeys();
          const j = jwt.getActiveJwk();
          return `key=${which(j.publicKeyPem)} kid=${j.kid}`;
        } catch (e) {
          return 'threw ' + kind(e, v);
        }
      });
      rec({ q: 'Q1b', site: 'jwt.initJwtKeys', value: name, failingVault: run1.result, cacheAfterFailing: cacheAfter1, recoveredVaultSameProcessWithin5min: run2.result, sentinelLines: hits(run1.lines) + hits(run2.lines) });
    }
    exitSpy.mockRestore();
    delete process.env.AZURE_KEY_VAULT_URL;
  });

  it('Q2 tenant rate limiter: redis path, res.setHeader path, downstream next path', async () => {
    const M = Module as any;
    const origLoad = M._load;
    let incrValue: unknown;
    class FakeRedis {
      constructor() {}
      connect() {
        return Promise.resolve();
      }
      incr() {
        return Promise.reject(incrValue);
      }
      pexpire() {
        return Promise.resolve();
      }
      pttl() {
        return Promise.resolve(1000);
      }
    }
    M._load = function (req: string, ...rest: unknown[]) {
      if (req === 'ioredis') return FakeRedis;
      return origLoad.call(this, req, ...rest);
    };
    const { createTenantRateLimiter } = await import('../middleware/tenant-rate-limiter');
    for (const [name, make] of VALUES) {
      for (const trig of ['redis.incr', 'res.setHeader', 'downstream next() throws']) {
        const v = make();
        incrValue = v;
        const limiter = createTenantRateLimiter({
          defaultLimits: { windowMs: 60000, maxRequests: 5 },
          ...(trig === 'redis.incr' ? { redisUrl: 'redis://gate175.invalid:6379' } : {}),
        });
        await new Promise((r) => setTimeout(r, 5));
        let status: number | undefined;
        const res: any = {
          setHeader() {
            if (trig === 'res.setHeader') throw v;
          },
          status(s: number) {
            status = s;
            return res;
          },
          json() {
            return res;
          },
        };
        let nextCalls = 0;
        const { result, lines } = await capture(async () => {
          try {
            await limiter({ headers: { 'x-tenant-id': 't175' } } as any, res, () => {
              nextCalls += 1;
              if (trig === 'downstream next() throws' && nextCalls === 1) throw v;
            });
            return 'resolved';
          } catch (e) {
            return 'rejected ' + kind(e, v);
          }
        });
        rec({ q: 'Q2', site: `rateLimiter via ${trig}`, value: name, out: result, nextCalls, status: status ?? null, sentinelLines: hits(lines) });
      }
    }
    M._load = origLoad;
  });

  it('Q3a refreshConfigs (direct and via init) with a prior good load', async () => {
    const { TenantPoolManager } = await import('../db/tenant-pool-manager');
    for (const [name, make] of VALUES) {
      for (const via of ['refreshConfigs after a good load', 'init (first load)']) {
        h.pgMode = 'ok';
        h.rows = [{ tenant_id: 't-susp', slug: 's', status: 'suspended', db_name: null, db_host: null, db_port: null }];
        const mgr = new TenantPoolManager({
          platformDatabaseUrl: 'postgres://p:pw@127.0.0.1:5432/secuura_platform',
          defaultDatabaseUrl: 'postgres://a:pw@127.0.0.1:5432/secuura',
          enabled: true,
          perTenantDbEnabled: false,
        });
        if (via.startsWith('refresh')) await capture(() => mgr.refreshConfigs());
        const v = make();
        h.toThrow = v;
        h.pgMode = 'platform-fail';
        const { result, lines } = await capture(async () => {
          try {
            if (via.startsWith('refresh')) await mgr.refreshConfigs();
            else await mgr.init();
            return 'resolved';
          } catch (e) {
            return 'rejected ' + kind(e, v);
          }
        });
        const st = mgr.getTenantStatus('t-susp') ?? 'undefined';
        (mgr as any).refreshTimer && clearInterval((mgr as any).refreshTimer);
        rec({ q: 'Q3a', site: via, value: name, out: result, suspendedTenantStatusAfter: st, sentinelLines: hits(lines) });
      }
    }
    h.pgMode = 'ok';
  });

  it('Q3b extractTenantContext: getPool throws, and downstream next throws', async () => {
    const { TenantPoolManager } = await import('../db/tenant-pool-manager');
    const { extractTenantContext } = await import('../db/tenant-context');
    for (const [name, make] of VALUES) {
      for (const trig of ['getPool throws', 'downstream next() throws']) {
        h.pgMode = 'ok';
        h.rows = [];
        const mgr = new TenantPoolManager({
          platformDatabaseUrl: 'postgres://p:pw@127.0.0.1:5432/secuura_platform',
          defaultDatabaseUrl: 'postgres://a:pw@127.0.0.1:5432/secuura',
          enabled: true,
          perTenantDbEnabled: false,
        });
        const v = make();
        if (trig === 'getPool throws')
          (mgr as any).getPool = () => {
            throw v;
          };
        let status: number | undefined;
        let body: unknown;
        const res: any = {
          status(s: number) {
            status = s;
            return res;
          },
          json(b: unknown) {
            body = b;
            return res;
          },
        };
        let nextCalls = 0;
        const { result, lines } = await capture(async () => {
          try {
            extractTenantContext(mgr)({ headers: { 'x-tenant-id': 't175' } } as any, res, () => {
              nextCalls += 1;
              if (trig.startsWith('downstream')) throw v;
            });
            return 'returned';
          } catch (e) {
            return 'threw ' + kind(e, v);
          }
        });
        let bodyStr = '';
        try {
          bodyStr = JSON.stringify(body) ?? '';
        } catch {
          bodyStr = '<unserialisable body: res.json would throw in express>';
        }
        rec({ q: 'Q3b', site: `extractTenantContext via ${trig}`, value: name, out: result, status: status ?? null, body: bodyStr.replace(/SNTL175/g, 'SNTL'), bodyHasSentinel: bodyStr.includes('SNTL175'), nextCalls, sentinelLines: hits(lines) });
      }
    }
  });

  it('Q3c runMigrations', async () => {
    const { runMigrations } = await import('../db/auto-migrate');
    const dir = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'g175m-'));
    fs.writeFileSync(path.join(dir, '001_g175.sql'), 'SELECT 175;');
    fs.writeFileSync(path.join(dir, '002_g175.sql'), 'SELECT 2;');
    for (const [name, make] of VALUES) {
      const v = make();
      h.toThrow = v;
      h.pgMode = 'ok';
      h.rows = [];
      const { result, lines } = await capture(async () => {
        try {
          const r = await runMigrations({ migrationsDir: dir, databaseUrl: 'postgres://a:pw@127.0.0.1:5432/secuura' });
          return `returned applied=${r.applied.length} errors=${r.errors.length} err0=${(r.errors[0] || '').replace(/SNTL175/g, 'SNTL')}`;
        } catch (e) {
          return 'rejected ' + kind(e, v);
        }
      });
      rec({ q: 'Q3c', site: 'runMigrations', value: name, out: result, sentinelLines: hits(lines) });
    }
    expect(true).toBe(true);
  });
});
