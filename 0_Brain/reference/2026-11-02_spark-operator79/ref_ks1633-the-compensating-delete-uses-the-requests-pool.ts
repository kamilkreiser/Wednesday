/**
 * KS-1633, gate AI1 note N4 — the compensating delete must run in the pool the REQUEST wrote to.
 *
 * `withTenant`'s multi-tenancy branch checks out of `tenantManager.getDefaultPool()` (`db.ts`). Under
 * multi-tenancy with a separate database per tenant that is a DIFFERENT database from the one the request's
 * write went to, so a compensating delete issued there would look for the row in the wrong place, remove
 * nothing, and raise nothing — the same silent-no-op shape the RLS GUC produces.
 *
 * WHAT THIS CELL DOES NOT DO, stated because it matters: it does not stand up a second tenant database. There is
 * no Docker on the machine this was written on and the scratch Postgres is a single instance, so the end-to-end
 * cross-database case is NOT covered by any cell. This pins the one thing that can be pinned without it — that
 * the request's pool is the pool handed to `withTenant` — and the PR body says the rest is unmeasured.
 */
const withTenantCalls: unknown[][] = [];
jest.mock('../db', () => ({
  prisma: { $executeRaw: jest.fn(async () => 1), $queryRaw: jest.fn(async () => []) },
  withTenant: (...a: unknown[]) => {
    withTenantCalls.push(a);
    const fn = a[1] as (tx: unknown) => Promise<unknown>;
    return fn({ $executeRaw: async () => 1 });
  },
}));
jest.mock('../utils/logger', () => ({ logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() } }));

import { deleteCertification } from '../repositories/certificationRepo';

const TENANT = 'a0000000-0000-4000-8000-0000000000aa';
const ID = 'b0000000-0000-4000-8000-0000000000bb';

describe('KS-1633 N4: the compensating delete runs in the request\'s pool', () => {
  beforeEach(() => { withTenantCalls.length = 0; });

  it('the pool it is GIVEN is the pool handed to withTenant', async () => {
    const requestPool = { connect: async () => ({}) };
    await deleteCertification(ID, TENANT, requestPool as any);
    expect(withTenantCalls).toHaveLength(1);
    expect(withTenantCalls[0][0]).toBe(TENANT);
    expect(withTenantCalls[0][2]).toEqual({ pool: requestPool });
    // the identity matters, not just the shape: a copy would be a different pool
    expect((withTenantCalls[0][2] as { pool: unknown }).pool).toBe(requestPool);
  });

  it('CONTROL - with NO pool it passes none, so single-tenant behaviour is exactly as before', async () => {
    await deleteCertification(ID, TENANT);
    expect(withTenantCalls).toHaveLength(1);
    expect(withTenantCalls[0][2]).toBeUndefined();
  });

  it('CONTROL - a DIFFERENT pool is not silently replaced by the default (the two calls carry different pools)', async () => {
    const a = { connect: async () => ({}) };
    const b = { connect: async () => ({}) };
    await deleteCertification(ID, TENANT, a as any);
    await deleteCertification(ID, TENANT, b as any);
    expect((withTenantCalls[0][2] as { pool: unknown }).pool).toBe(a);
    expect((withTenantCalls[1][2] as { pool: unknown }).pool).toBe(b);
    expect((withTenantCalls[0][2] as { pool: unknown }).pool).not.toBe((withTenantCalls[1][2] as { pool: unknown }).pool);
  });

  it('it returns the row count the transaction reports, so a no-op is distinguishable from a removal', async () => {
    expect(await deleteCertification(ID, TENANT)).toBe(1);
  });
});
