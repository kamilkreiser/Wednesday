/**
 * =============================================================================
 * KS-597 option B — the caller-organisation read, in a REAL database, as the
 * role originate really runs as, under the request's tenant context
 * =============================================================================
 * The route's option-B arm accepts a claim equal to the caller Organisation's
 * own `externalRef`, read by `getOrganizationExternalRef(callerOrgId, tenantId, db)`.
 * The mocked route suite (`ks597-b-caller-scoped-externalref.test.ts`) cannot see
 * whether that read works in the database the product meets, and there are two
 * ways it could come back BLIND while every superuser test stays green:
 *
 *   1. `organizations` carries FORCE RLS with the fail-closed policy of
 *      migration 039. Originate connects as `secuura_app` (NOSUPERUSER,
 *      NOBYPASSRLS), so a read with no tenant scope returns zero rows.
 *   2. The explicit `tenant_id` predicate could hide the caller's own row if the
 *      request tenant and the organisation's tenant were ever confused.
 *
 * So every cell here runs the product's own statement as `secuura_app`, inside
 * one transaction carrying `app.current_tenant_id` — the same shape db.ts's
 * KS-458 proxy gives a tenant-scoped request — and reads the result, not the SQL.
 *
 * DB-gated, and never silently skipped: without a database `beforeAll` throws,
 * and without the `secuura_app` role every cell throws at SET ROLE. Point it at
 * a disposable Postgres built from `docker/init` + `scripts/run-migrations.sh`
 * via TEST_DATABASE_URL, whose role must be able to SET ROLE secuura_app.
 * =============================================================================
 */

import { Client } from 'pg';

const TEST_DB = process.env.TEST_DATABASE_URL || process.env.DATABASE_URL;
if (TEST_DB) {
  process.env.DATABASE_URL = TEST_DB;
}
process.env.JWT_SECRET = process.env.JWT_SECRET || 'ks597b-integration-secret';

import { getOrganizationExternalRef } from '../repositories/documentRepo';

const TENANT_A = '55555555-5555-4555-8555-555555555555';
const TENANT_B = '66666666-6666-4666-8666-666666666666';
// Two Organisations in DIFFERENT tenants sharing ONE externalRef — the schema has
// no unique index on it, which the seed itself proves by succeeding.
const ORG_A = '77777777-7777-4777-8777-777777777777';
const ORG_B = '88888888-8888-4888-8888-888888888888';
// An Organisation in tenant A with no externalRef at all.
const ORG_A_NO_REF = '99999999-aaaa-4aaa-8aaa-999999999999';
// Stored upper-case, as a .NET caller could register it; the route normalises.
const SHARED_REF = 'C0FFEE00-7777-4777-8777-00000000A7B8';

type Scope = { tenant: string | null; platformBypass?: boolean };

let admin: Client;
let conn: Client;

/**
 * A `$queryRaw` client for one request shape: `SET LOCAL ROLE secuura_app`, then
 * the scope GUCs db.ts would set, then the product's own statement with its
 * interpolations bound positionally (the shape Prisma emits). Rolled back, so a
 * cell can never leave state behind for the next one.
 */
function asAppRole(scope: Scope) {
  return {
    $queryRaw: async (strings: TemplateStringsArray, ...values: unknown[]) => {
      let text = '';
      strings.forEach((s, i) => {
        text += s;
        if (i < values.length) text += `$${i + 1}`;
      });
      await conn.query('BEGIN');
      try {
        await conn.query('SET LOCAL ROLE secuura_app');
        if (scope.tenant !== null) {
          await conn.query("SELECT set_config('app.current_tenant_id', $1, true)", [scope.tenant]);
        }
        if (scope.platformBypass) {
          await conn.query("SELECT set_config('app.tenant_scope_bypass', 'platform_admin', true)");
        }
        return (await conn.query(text, values as unknown[])).rows;
      } finally {
        await conn.query('ROLLBACK');
      }
    },
  } as never;
}

beforeAll(async () => {
  if (!TEST_DB) {
    throw new Error(
      'KS-597 option-B integration suite needs a database. Set TEST_DATABASE_URL to a Postgres built from ' +
        'docker/init + scripts/run-migrations.sh. It is DB-gated, never skipped.',
    );
  }
  admin = new Client({ connectionString: TEST_DB });
  await admin.connect();
  conn = new Client({ connectionString: TEST_DB });
  await conn.connect();

  for (const tid of [TENANT_A, TENANT_B]) {
    await admin.query(
      `INSERT INTO tenants (id, name, slug, status, created_at, updated_at)
       VALUES ($1, $2, $3, 'active', NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
      [tid, `Tenant ${tid.slice(0, 4)}`, `t-${tid.slice(0, 8)}`],
    ).catch(() => undefined); // tenants may live in the platform DB; org rows are what matter
  }
  const seed: Array<[string, string, string, string | null]> = [
    [ORG_A, TENANT_A, 'KS-597 B org A', SHARED_REF],
    [ORG_B, TENANT_B, 'KS-597 B org B', SHARED_REF],
    [ORG_A_NO_REF, TENANT_A, 'KS-597 B org A (no ref)', null],
  ];
  for (const [oid, tid, name, ref] of seed) {
    await admin.query(
      `INSERT INTO organizations (id, tenant_id, name, slug, type, metadata, created_at, updated_at)
       VALUES ($1, $2, $3, $4, 'issuer', $5::jsonb, NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
      [oid, tid, name, `ks597b-${oid.slice(0, 8)}`, JSON.stringify(ref ? { externalRef: ref } : {})],
    );
  }
});

afterAll(async () => {
  if (admin) {
    await admin.query('DELETE FROM organizations WHERE id = ANY($1::uuid[])', [[ORG_A, ORG_B, ORG_A_NO_REF]]);
    await admin.end();
  }
  if (conn) await conn.end();
});

describe('KS-597 option B — the caller-organisation read as secuura_app, under the request tenant', () => {
  // Everything below is only evidence if RLS actually binds. A superuser or a
  // BYPASSRLS role would see every row and pass every cell for the wrong reason.
  it('ROLE CHECK: the cells act as secuura_app — not superuser, not BYPASSRLS', async () => {
    const [row] = (await (asAppRole({ tenant: TENANT_A }) as any).$queryRaw`
      SELECT current_user AS who, rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user
    `) as Array<{ who: string; rolsuper: boolean; rolbypassrls: boolean }>;
    expect(row).toEqual({ who: 'secuura_app', rolsuper: false, rolbypassrls: false });
  });

  it("row 3: under the request's tenant, the caller Organisation's own externalRef is read", async () => {
    expect(await getOrganizationExternalRef(ORG_A, TENANT_A, asAppRole({ tenant: TENANT_A }))).toBe(SHARED_REF);
  });

  it("row 4: another tenant's Organisation reads as nothing from this tenant — and IS readable in its own", async () => {
    expect(await getOrganizationExternalRef(ORG_B, TENANT_A, asAppRole({ tenant: TENANT_A }))).toBeNull();
    // Control: the row exists and this role can read it in the right tenant, so
    // the null above is a refusal and not an absent row.
    expect(await getOrganizationExternalRef(ORG_B, TENANT_B, asAppRole({ tenant: TENANT_B }))).toBe(SHARED_REF);
  });

  it('row 4, predicate not only RLS: on the platform-bypass path the tenant predicate still hides another tenant', async () => {
    const bypassA = asAppRole({ tenant: TENANT_A, platformBypass: true });
    // RLS is NOT excluding ORG_B on this path — proved here, so the null below
    // cannot be credited to the policy.
    const visible = (await (bypassA as any).$queryRaw`SELECT id FROM organizations WHERE id = ${ORG_B}::uuid`) as unknown[];
    expect(visible).toHaveLength(1);
    expect(await getOrganizationExternalRef(ORG_B, TENANT_A, bypassA)).toBeNull();
  });

  it('row 5: an Organisation with no externalRef reads as null — while its row is visible', async () => {
    const scopeA = asAppRole({ tenant: TENANT_A });
    const visible = (await (scopeA as any).$queryRaw`SELECT id FROM organizations WHERE id = ${ORG_A_NO_REF}::uuid`) as unknown[];
    expect(visible).toHaveLength(1);
    expect(await getOrganizationExternalRef(ORG_A_NO_REF, TENANT_A, scopeA)).toBeNull();
  });

  it('row 6: the schema accepted two Organisations with one externalRef, and each caller reads only its own row', async () => {
    const { rows } = await admin.query(
      `SELECT count(*)::int AS n FROM organizations WHERE metadata->>'externalRef' = $1`,
      [SHARED_REF],
    );
    expect(rows[0].n).toBe(2);
    expect(await getOrganizationExternalRef(ORG_A, TENANT_A, asAppRole({ tenant: TENANT_A }))).toBe(SHARED_REF);
    expect(await getOrganizationExternalRef(ORG_B, TENANT_B, asAppRole({ tenant: TENANT_B }))).toBe(SHARED_REF);
  });

  // The trap Wednesday named (a): this is what the read looks like WITHOUT the
  // request's tenant scope — blind. Paired with row 3's non-null on the same
  // row, it shows the result is decided by the scope, which is why the route
  // must read through `req.db` (the tenant-GUC client) and nothing else.
  it('TRAP: with NO tenant scope the same read is blind under fail-closed RLS', async () => {
    expect(await getOrganizationExternalRef(ORG_A, TENANT_A, asAppRole({ tenant: null }))).toBeNull();
  });

  it('a malformed organisation or tenant id reads as null without reaching the database', async () => {
    const neverCalled = { $queryRaw: jest.fn() } as never;
    expect(await getOrganizationExternalRef('not-a-uuid', TENANT_A, neverCalled)).toBeNull();
    expect(await getOrganizationExternalRef(ORG_A, 'not-a-uuid', neverCalled)).toBeNull();
    expect((neverCalled as any).$queryRaw).not.toHaveBeenCalled();
  });
});
