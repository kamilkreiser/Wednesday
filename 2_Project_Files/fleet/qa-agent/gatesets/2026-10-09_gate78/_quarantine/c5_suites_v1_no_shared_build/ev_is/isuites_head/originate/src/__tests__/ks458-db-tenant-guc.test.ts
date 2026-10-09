/**
 * KS-458 — fail-closed RLS tenant-GUC plumbing in src/db.ts (no DB needed).
 *
 * Verifies, against a fake PrismaClient / pg pool:
 *  - the module `prisma` proxy passes raw calls straight through with no
 *    scope, and wraps them in ONE $transaction with the matching set_config
 *    (app.current_tenant_id / app.tenant_scope_bypass) when a tenant or
 *    platform scope is active;
 *  - createPoolProxy bundles BEGIN → set_config → query → COMMIT for a Pool,
 *    but queries directly when handed withTenant()'s open transaction client;
 *  - withTenant (single-tenant Prisma branch) sets BOTH app.tenant_id
 *    (rights_holders policy, KS-108) and app.current_tenant_id (KS-458)
 *    inside the same transaction.
 */

process.env.DATABASE_URL = 'postgresql://user:pass@localhost:5432/db';
delete process.env.MULTI_TENANCY_ENABLED;

const prismaCalls: any[] = [];

class FakeTx {
  async $executeRaw(strings: TemplateStringsArray, ...values: any[]) {
    prismaCalls.push(['tx.$executeRaw', strings.join('?'), values]);
    return 1;
  }
  async $queryRaw(strings: TemplateStringsArray, ...values: any[]) {
    prismaCalls.push(['tx.$queryRaw', strings.join('?'), values]);
    return [{ ok: 1 }];
  }
  async $queryRawUnsafe(text: string, ...params: any[]) {
    prismaCalls.push(['tx.$queryRawUnsafe', text, params]);
    return [{ ok: 1 }];
  }
  async $executeRawUnsafe(text: string, ...params: any[]) {
    prismaCalls.push(['tx.$executeRawUnsafe', text, params]);
    return 1;
  }
}

jest.mock('@prisma/client', () => ({
  PrismaClient: class {
    async $queryRaw(strings: TemplateStringsArray, ...values: any[]) {
      prismaCalls.push(['root.$queryRaw', strings.join('?'), values]);
      return [{ ok: 1 }];
    }
    async $queryRawUnsafe(text: string, ...params: any[]) {
      prismaCalls.push(['root.$queryRawUnsafe', text, params]);
      return [{ ok: 1 }];
    }
    async $transaction(fn: (tx: any) => Promise<any>) {
      prismaCalls.push(['$transaction']);
      return fn(new FakeTx());
    }
    async $disconnect() {}
  },
}), { virtual: false });

import { runWithTenantId, runWithPlatformScope } from '@secuura/shared';
import { prisma, createPoolProxy, withTenant } from '../db';

describe('KS-458 db.ts smoke', () => {
  beforeEach(() => { prismaCalls.length = 0; });

  it('no scope → raw call passes straight through (no transaction)', async () => {
    await prisma.$queryRaw`SELECT 1`;
    expect(prismaCalls).toEqual([['root.$queryRaw', 'SELECT 1', []]]);
  });

  it('tenant scope → wraps in $transaction and sets app.current_tenant_id', async () => {
    await runWithTenantId('t-111', () => prisma.$queryRaw`SELECT 2`);
    expect(prismaCalls[0]).toEqual(['$transaction']);
    expect(prismaCalls[1][0]).toBe('tx.$executeRaw');
    expect(prismaCalls[1][1]).toContain("set_config('app.current_tenant_id'");
    expect(prismaCalls[1][2]).toEqual(['t-111']);
    expect(prismaCalls[2]).toEqual(['tx.$queryRaw', 'SELECT 2', []]);
  });

  it('platform scope → wraps in $transaction and sets app.tenant_scope_bypass', async () => {
    await runWithPlatformScope(() => prisma.$queryRawUnsafe('SELECT 3'));
    expect(prismaCalls[0]).toEqual(['$transaction']);
    expect(prismaCalls[1][1]).toContain("set_config('app.tenant_scope_bypass', 'platform_admin', true)");
    expect(prismaCalls[2]).toEqual(['tx.$queryRawUnsafe', 'SELECT 3', []]);
  });

  it('createPoolProxy(Pool) bundles the GUC in one BEGIN/COMMIT transaction', async () => {
    const calls: any[] = [];
    const client = {
      query: async (text: string, params?: any[]) => { calls.push([text, params]); return { rows: [{ ok: 1 }], rowCount: 1 }; },
      release: () => calls.push(['release']),
    };
    const pool = {
      connect: async () => client,
      query: async (text: string, params?: any[]) => { calls.push(['pool.direct', text, params]); return { rows: [], rowCount: 0 }; },
    };
    const proxy = createPoolProxy(pool);

    // no scope → plain pool.query
    await proxy.$queryRaw`SELECT 4`;
    expect(calls).toEqual([['pool.direct', 'SELECT 4', []]]);

    calls.length = 0;
    await runWithTenantId('t-222', () => proxy.$queryRaw`SELECT ${5}`);
    expect(calls[0][0]).toBe('BEGIN');
    expect(calls[1][0]).toContain("set_config('app.current_tenant_id', $1, true)");
    expect(calls[1][1]).toEqual(['t-222']);
    expect(calls[2]).toEqual(['SELECT $1', [5]]);
    expect(calls[3][0]).toBe('COMMIT');
    expect(calls[4]).toEqual(['release']);
  });

  it('createPoolProxy(PoolClient) queries directly on the open transaction', async () => {
    const calls: any[] = [];
    const txClient = {
      query: async (text: string, params?: any[]) => { calls.push([text, params]); return { rows: [], rowCount: 2 }; },
      release: () => calls.push(['release']),
    };
    const proxy = createPoolProxy(txClient);
    await runWithTenantId('t-333', () => proxy.$executeRaw`UPDATE t SET x = ${1}`);
    // No BEGIN/set_config — withTenant applied them right after its own BEGIN.
    expect(calls).toEqual([['UPDATE t SET x = $1', [1]]]);
  });

  it('withTenant (single-tenant Prisma branch) sets BOTH app.tenant_id and app.current_tenant_id', async () => {
    await withTenant('t-444', async (tx) => tx.$queryRawUnsafe('SELECT 6'));
    expect(prismaCalls[0]).toEqual(['$transaction']);
    expect(prismaCalls[1][1]).toContain("set_config('app.tenant_id', $1, true)");
    expect(prismaCalls[1][2]).toEqual(['t-444']);
    expect(prismaCalls[2][1]).toContain("set_config('app.current_tenant_id', $1, true)");
    expect(prismaCalls[2][2]).toEqual(['t-444']);
    expect(prismaCalls[3]).toEqual(['tx.$queryRawUnsafe', 'SELECT 6', []]);
  });
});
