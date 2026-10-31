/**
 * Gate 64 probe (KS-1860 #1876). Runs on BASE product code and on HEAD.
 *  G*  getPool snapshot: every tenant status x PROVISION_PER_TENANT_DB off/on x fresh/cached, classified as
 *      default | own:<db> | throw:<msg>. Written to $GATE64_SNAPSHOT so base and head can be diffed byte-for-byte.
 *  F*  failure / staleness of the status map (HEAD behaviour asserted; at base these document base behaviour).
 * The pg fake applies the refresh query's own WHERE (if any) to an in-memory table, like the PR's harness, and counts
 * platform queries. Tenant pools are fake Pools carrying their constructor options.
 */
import { describe, it, expect, afterEach, vi } from 'vitest';
import { readFileSync, writeFileSync } from 'node:fs';
import type { NextFunction, Request, Response } from 'express';

const fake = vi.hoisted(() => ({
  tenants: [] as Array<{ id: string; slug: string; status: string; db_name: string | null; db_host: string | null; db_port: number | null }>,
  fail: 'none' as 'none' | 'next' | 'always',
  platformQueries: 0,
}));

vi.mock('pg', () => {
  const PLATFORM_URL = 'postgres://platform:pw@127.0.0.1:5432/secuura_platform';
  function platformRows(text: string): Array<Record<string, unknown>> {
    const sql = text.replace(/\s+/g, ' ').trim();
    const head = 'SELECT t.id AS tenant_id, t.slug, t.status, tc.db_name, tc.db_host, tc.db_port FROM tenants t LEFT JOIN tenant_config tc ON tc.tenant_id = t.id';
    if (!sql.startsWith(head)) throw new Error('fake pg: unmodelled platform query: ' + sql);
    const rest = sql.slice(head.length).trim();
    let keep: (s: string) => boolean = () => true;
    if (rest !== '') {
      const m = /^WHERE t\.status IN \(((?:'[a-z_]+'(?:, )?)+)\)$/.exec(rest);
      if (!m) throw new Error('fake pg: unmodelled WHERE: ' + rest);
      const allowed = m[1].split(', ').map((s) => s.slice(1, -1));
      keep = (s) => allowed.includes(s);
    }
    return fake.tenants.filter((t) => keep(t.status)).map((t) => ({ tenant_id: t.id, slug: t.slug, status: t.status, db_name: t.db_name, db_host: t.db_host, db_port: t.db_port }));
  }
  class Pool {
    readonly opts: Record<string, unknown>;
    constructor(opts: Record<string, unknown>) { this.opts = opts ?? {}; }
    async query(text: string) {
      if (this.opts.connectionString !== PLATFORM_URL) throw new Error('fake pg: only the platform pool is queried here');
      fake.platformQueries += 1;
      if (fake.fail === 'always') throw new Error('platform database unavailable');
      if (fake.fail === 'next') { fake.fail = 'none'; throw new Error('platform database unavailable'); }
      const rows = platformRows(text);
      return { rows, rowCount: rows.length };
    }
    on() { return this; }
    async end() { return undefined; }
    async connect() { throw new Error('fake pg: connect is not modelled'); }
  }
  return { default: { Pool }, Pool };
});

import { TenantPoolManager } from '../db/tenant-pool-manager';
import { extractTenantContext } from '../db/tenant-context';

const PLATFORM_URL = 'postgres://platform:pw@127.0.0.1:5432/secuura_platform';
const DEFAULT_URL = 'postgres://app:pw@127.0.0.1:5432/secuura';
const DEFAULT_TENANT = 'a0000000-0000-4000-8000-000000000001';
const T = {
  ACTIVE_OWN: 'b6400000-0000-4000-8000-00000000000a',
  ACTIVE_SHARED: 'b6400000-0000-4000-8000-00000000000b',
  SUSPENDED: 'b6400000-0000-4000-8000-00000000000c',
  ARCHIVED: 'b6400000-0000-4000-8000-00000000000d',
  PROVISIONING: 'b6400000-0000-4000-8000-00000000000e',
  UNKNOWN: 'b6400000-0000-4000-8000-00000000000f',
  DEFAULT: DEFAULT_TENANT,
};
function seed(): void {
  fake.fail = 'none';
  fake.platformQueries = 0;
  fake.tenants = [
    { id: T.ACTIVE_OWN, slug: 'own', status: 'active', db_name: 'secuura_tenant_own', db_host: 'db2', db_port: 5432 },
    { id: T.ACTIVE_SHARED, slug: 'shared', status: 'active', db_name: null, db_host: null, db_port: null },
    { id: T.SUSPENDED, slug: 'shut', status: 'suspended', db_name: 'secuura_tenant_shut', db_host: 'db2', db_port: 5432 },
    { id: T.ARCHIVED, slug: 'gone', status: 'archived', db_name: 'secuura_tenant_gone', db_host: 'db2', db_port: 5432 },
    { id: T.PROVISIONING, slug: 'newco', status: 'provisioning', db_name: 'secuura_tenant_newco', db_host: 'db2', db_port: 5432 },
  ];
}
const managers: TenantPoolManager[] = [];
async function manager(enabled: boolean, perTenantDbEnabled: boolean): Promise<TenantPoolManager> {
  const m = new TenantPoolManager({ platformDatabaseUrl: PLATFORM_URL, defaultDatabaseUrl: DEFAULT_URL, enabled, perTenantDbEnabled });
  managers.push(m);
  await m.init();
  return m;
}
afterEach(async () => {
  vi.useRealTimers();
  while (managers.length) await managers.pop()!.shutdown();
});
function classify(m: TenantPoolManager, id: string): string {
  try {
    const p = m.getPool(id) as unknown as { opts: Record<string, unknown> };
    if ((p as unknown) === m.getDefaultPool()) return 'default';
    return `own:${String(p.opts.database)}@${String(p.opts.host)}`;
  } catch (e) {
    return `throw:${(e as Error).message}`;
  }
}
function run(m: TenantPoolManager, tenantId: string) {
  let statusCode: number | undefined;
  let body: unknown;
  const res = { status(c: number) { statusCode = c; return this; }, json(b: unknown) { body = b; return this; } } as unknown as Response;
  const req = { headers: { 'x-tenant-id': tenantId } } as unknown as Request;
  const next = vi.fn() as unknown as NextFunction;
  extractTenantContext(m)(req, res, next);
  return { status: statusCode, body, served: (next as unknown as { mock: { calls: unknown[] } }).mock.calls.length === 1 };
}

describe('gate64 G: getPool snapshot (diffed base vs head)', () => {
  it('G1: snapshot of getPool for every status x perTenantDb x fresh/cached, and multi-tenancy off', async () => {
    const snap: Record<string, string> = {};
    for (const per of [false, true]) {
      seed();
      const m = await manager(true, per);
      for (const [k, id] of Object.entries(T)) snap[`enabled|per=${per}|fresh|${k}`] = classify(m, id);
      // cached: the tenant was active and got a pool, then flips to suspended / archived, then a refresh runs
      for (const to of ['suspended', 'archived']) {
        seed();
        const m2 = await manager(true, per);
        const before = classify(m2, T.ACTIVE_OWN);
        fake.tenants.find((t) => t.id === T.ACTIVE_OWN)!.status = to;
        await m2.refreshConfigs();
        snap[`enabled|per=${per}|cached-then-${to}|ACTIVE_OWN`] = `${before} -> ${classify(m2, T.ACTIVE_OWN)}`;
      }
      // a refresh that fails keeps the pool map (base and head)
      seed();
      const m3 = await manager(true, per);
      fake.fail = 'always';
      await m3.refreshConfigs();
      for (const [k, id] of Object.entries(T)) snap[`enabled|per=${per}|after-failed-refresh|${k}`] = classify(m3, id);
      // first refresh fails at init
      seed();
      fake.fail = 'always';
      const m4 = await manager(true, per);
      for (const [k, id] of Object.entries(T)) snap[`enabled|per=${per}|init-failed|${k}`] = classify(m4, id);
    }
    seed();
    const off = await manager(false, true);
    await off.refreshConfigs();
    for (const [k, id] of Object.entries(T)) snap[`disabled|per=true|${k}`] = classify(off, id);
    const out = process.env.GATE64_SNAPSHOT;
    if (out) writeFileSync(out, JSON.stringify(snap, null, 1) + '\n');
    expect(Object.keys(snap).length).toBe(2 * (7 + 2 + 7 + 7) + 7);
    const expectFile = process.env.GATE64_EXPECT;
    if (expectFile) expect(snap).toEqual(JSON.parse(readFileSync(expectFile, 'utf8')));
  });
});

describe('gate64 F: status-map failure and staleness (HEAD behaviour)', () => {
  it('F1 FAIL-OPEN AT BOOT: the first refresh fails, a suspended and an archived tenant are served', async () => {
    seed();
    fake.fail = 'always';
    const m = await manager(true, false);
    expect(m.getTenantStatus(T.SUSPENDED)).toBeUndefined();
    expect(run(m, T.SUSPENDED).served).toBe(true);
    expect(run(m, T.ARCHIVED).served).toBe(true);
  });

  it('F2 STALE: suspended after the last refresh, the tenant is still served until the next one', async () => {
    seed();
    const m = await manager(true, false);
    fake.tenants.find((t) => t.id === T.ACTIVE_SHARED)!.status = 'suspended';
    expect(run(m, T.ACTIVE_SHARED).served).toBe(true);
    await m.refreshConfigs();
    const r = run(m, T.ACTIVE_SHARED);
    expect(r.served).toBe(false);
    expect(r.status).toBe(403);
  });

  it('F3 STALE INDEFINITELY: suspended after the last refresh, and every later refresh fails -> served on every request', async () => {
    seed();
    const m = await manager(true, false);
    fake.tenants.find((t) => t.id === T.ACTIVE_SHARED)!.status = 'suspended';
    fake.fail = 'always';
    for (let i = 0; i < 5; i += 1) await m.refreshConfigs();
    expect(run(m, T.ACTIVE_SHARED).served).toBe(true);
  });

  it('F4 LAST-KNOWN: reactivated after the last refresh, refreshes failing -> still refused', async () => {
    seed();
    const m = await manager(true, false);
    expect(run(m, T.SUSPENDED).status).toBe(403);
    fake.tenants.find((t) => t.id === T.SUSPENDED)!.status = 'active';
    fake.fail = 'always';
    await m.refreshConfigs();
    expect(run(m, T.SUSPENDED).status).toBe(403);
    // and every other tenant is unaffected by the failure (not fail-closed for everyone)
    expect(run(m, T.ACTIVE_SHARED).served).toBe(true);
  });

  it('F5 BOOT RECOVERY: after a failed boot refresh, the next successful refresh starts refusing', async () => {
    seed();
    fake.fail = 'next';
    const m = await manager(true, false);
    expect(run(m, T.SUSPENDED).served).toBe(true);
    await m.refreshConfigs();
    expect(run(m, T.SUSPENDED).status).toBe(403);
  });

  it('F6 INTERVAL: the timer refreshes every 60 000 ms, and not before', async () => {
    vi.useFakeTimers();
    seed();
    const m = await manager(true, false);
    expect(fake.platformQueries).toBe(1);
    await vi.advanceTimersByTimeAsync(59_999);
    expect(fake.platformQueries).toBe(1);
    await vi.advanceTimersByTimeAsync(1);
    expect(fake.platformQueries).toBe(2);
    fake.tenants.find((t) => t.id === T.ACTIVE_SHARED)!.status = 'suspended';
    await vi.advanceTimersByTimeAsync(60_000);
    expect(fake.platformQueries).toBe(3);
    expect(m.getTenantStatus(T.ACTIVE_SHARED)).toBe('suspended');
  });

  it('F7 OFF: multi-tenancy off -> init never queries, nothing is refused', async () => {
    seed();
    const m = await manager(false, false);
    expect(fake.platformQueries).toBe(0);
    expect(m.getTenantStatus(T.SUSPENDED)).toBeUndefined();
    expect(run(m, T.SUSPENDED).served).toBe(true);
    expect(run(m, T.ARCHIVED).served).toBe(true);
  });

  it('F8 ARCHIVED == SUSPENDED: same status code, same error, same body shape; per-tenant DB on too', async () => {
    for (const per of [false, true]) {
      seed();
      const m = await manager(true, per);
      const s = run(m, T.SUSPENDED);
      const a = run(m, T.ARCHIVED);
      expect([s.status, s.served, a.status, a.served]).toEqual([403, false, 403, false]);
      expect(s.body).toEqual({ error: 'Tenant access denied', message: 'Tenant is suspended' });
      expect(a.body).toEqual({ error: 'Tenant access denied', message: 'Tenant is archived' });
    }
  });

  it('F9 status values outside the schema (e.g. upper case) are not refused (the check is an exact match)', async () => {
    seed();
    fake.tenants.push({ id: T.UNKNOWN, slug: 'odd', status: 'SUSPENDED', db_name: null, db_host: null, db_port: null });
    const m = await manager(true, false);
    expect(run(m, T.UNKNOWN).served).toBe(true);
  });
});
