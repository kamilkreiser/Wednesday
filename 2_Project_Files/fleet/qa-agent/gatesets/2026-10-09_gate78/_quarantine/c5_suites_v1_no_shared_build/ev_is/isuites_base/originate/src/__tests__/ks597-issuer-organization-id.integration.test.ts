/**
 * =============================================================================
 * KS-597 — CROSS-TENANT ORG ATTRIBUTION, PROVED IN A REAL DATABASE
 * =============================================================================
 * QA Finding 2 (round-1 gate on #889): the mocked suite is blind to the tenancy
 * predicate — the one property it was written to protect. Deleting
 * `AND tenant_id = ${tenantId}::uuid` from BOTH `organizations` subqueries left
 * all 8 mocked cells green while the tree attributed documents across tenants.
 * The sibling file's cell 2 is now pinned as one unit and by binding position
 * and DOES red under that tamper — but a SQL-text assertion still only proves
 * what we sent, never what the database did with it.
 *
 * This file proves the behaviour. It drives the REAL `saveDocument` against a
 * real Postgres and reads every value back out of the row on a SEPARATE
 * connection, never from the binding.
 *
 * WHY THE OBVIOUS TEST CANNOT FAIL, and what this does instead
 * -----------------------------------------------------------
 * `organizations` has forced RLS, and the request pool sets
 * `app.current_tenant_id`. So on the ORDINARY `secuura_app` path the policy
 * already hides tenant B's organisation and the explicit predicate is
 * REDUNDANT: tamper it and the result is still NULL. That is a passing cell
 * over a removed guard — it produced the gate's own false null.
 *
 * So both cells here isolate the two paths where RLS does NOT exclude the row,
 * which is exactly where the predicate is the only thing left:
 *   P1  `app.tenant_scope_bypass = 'platform_admin'`  (the documented admin path)
 *   P2  a BYPASSRLS role                              (the documented rollback connection)
 *
 * KS-980: P1 and P2 are only two paths if they connect as two ROLES. Until this
 * change both opened TEST_DATABASE_URL, whose role is the BYPASSRLS one - so the
 * P1 cell set a GUC on a connection RLS never constrained, the GUC was INERT, and
 * the documented admin path was never exercised. P1 now connects as the ordinary
 * application role (TEST_APP_DATABASE_URL, or APP_DB_USER/APP_DB_PASSWORD against
 * the same server), which RLS does constrain, so its GUC is load-bearing. The
 * D1/D2 cells at the end of this file exist to keep that true: both go red if P1
 * is ever pointed back at a BYPASSRLS connection.
 *
 * DB-gated, and never silently skipped: without a database `beforeAll` throws.
 * Point it at one with TEST_DATABASE_URL. A disposable instance built from the
 * repo's own provisioning path (`docker/init` + `scripts/run-migrations.sh`) is
 * the intended target — NOT the shared dev stack, whose schema drifts.
 * =============================================================================
 */

import { Client } from 'pg';
import { randomUUID } from 'crypto';

const TEST_DB = process.env.TEST_DATABASE_URL || process.env.DATABASE_URL;
if (TEST_DB) {
  process.env.DATABASE_URL = TEST_DB;
}

/**
 * KS-980: the connection for P1 - a role RLS actually constrains.
 *
 * Either given outright as TEST_APP_DATABASE_URL, or composed from APP_DB_USER /
 * APP_DB_PASSWORD against the same server as TEST_DB (which is how docker-compose
 * threads them into the postgres container, so a disposable instance built the
 * documented way already has the role). The compose default password is NEVER
 * written here: a literal in the tree would be a credential in the tree, and it
 * would also silently stop matching any instance provisioned with its own value.
 */
function appDatabaseUrl(): string | null {
  const explicit = process.env.TEST_APP_DATABASE_URL;
  if (explicit) return explicit;
  const user = process.env.APP_DB_USER;
  const password = process.env.APP_DB_PASSWORD;
  if (!TEST_DB || !user || !password) return null;
  const url = new URL(TEST_DB);
  url.username = encodeURIComponent(user);
  url.password = encodeURIComponent(password);
  return url.toString();
}

const TEST_APP_DB = appDatabaseUrl();

/**
 * KS-1306: the host ports a SHARED Postgres is reachable on, so this suite can refuse them.
 * `5432` is Postgres's own default. The repo's stack port is read from docker-compose.yml rather
 * than pasted, because a literal here would silently stop matching the stack it is meant to refuse.
 * If the file cannot be read (a packaged checkout), the default is still refused - failing closed.
 */
const SHARED_STACK_PORTS: string[] = (() => {
  const ports = new Set(['5432']);
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const fs = require('fs') as typeof import('fs');
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const path = require('path') as typeof import('path');
    const compose = fs.readFileSync(path.resolve(__dirname, '../../../../docker-compose.yml'), 'utf8');
    const m = compose.match(/POSTGRES_EXTERNAL_PORT:-(\d+)\}:5432/);
    if (m) ports.add(m[1]);
    else ports.add('6432');
  } catch {
    ports.add('6432');
  }
  return [...ports];
})();
process.env.JWT_SECRET = process.env.JWT_SECRET || 'ks597-integration-secret';

// eslint-disable-next-line @typescript-eslint/no-var-requires
import { saveDocument, DocumentRecord } from '../repositories/documentRepo';

const TENANT_A = '11111111-1111-4111-8111-111111111111';
const TENANT_B = '22222222-2222-4222-8222-222222222222';
const ORG_IN_A = '33333333-3333-4333-8333-333333333333';
const ORG_IN_B = '44444444-4444-4444-8444-444444444444';

/**
 * The product calls `client.$executeRaw` as a Prisma tagged template. There is
 * no generated Prisma client in this tree, so the statement is executed through
 * a `pg` pool proxy that binds the interpolations positionally — the same shape
 * Prisma emits. The SQL is the product's own, verbatim; only the driver differs,
 * and that equivalence is READ from the call shape rather than executed.
 */
function poolProxy(client: Client) {
  return {
    $executeRaw: async (strings: TemplateStringsArray, ...values: unknown[]) => {
      let text = '';
      strings.forEach((s, i) => {
        text += s;
        if (i < values.length) text += `$${i + 1}`;
      });
      const res = await client.query(text, values as unknown[]);
      return res.rowCount ?? 0;
    },
  } as never;
}

function makeDoc(externalId: string): DocumentRecord {
  return {
    id: externalId,
    type: 'degree',
    status: 'draft',
    owner: { id: 'issuer-1', walletAddress: 'addr_test1qexample' },
    data: { title: 'KS-597 integration' },
    contentHash: 'a'.repeat(64),
    signatures: [],
    createdAt: new Date('2026-01-01T00:00:00.000Z'),
    updatedAt: new Date('2026-01-01T00:00:00.000Z'),
  } as unknown as DocumentRecord;
}

let admin: Client;

/** Reads the row back on the ADMIN connection — never from the write binding. */
async function readIssuerOrg(externalId: string): Promise<string | null> {
  const { rows } = await admin.query(
    'SELECT issuer_organization_id FROM documents WHERE external_id = $1',
    [externalId],
  );
  if (rows.length !== 1) throw new Error(`expected 1 row for ${externalId}, got ${rows.length}`);
  return rows[0].issuer_organization_id;
}

beforeAll(async () => {
  if (!TEST_DB) {
    throw new Error(
      'KS-597 integration suite needs a database. Set TEST_DATABASE_URL to a Postgres built from ' +
        'docker/init + scripts/run-migrations.sh. It is DB-gated, never skipped.',
    );
  }
  if (!TEST_APP_DB) {
    throw new Error(
      'KS-980: the platform_bypass cell needs a role that does NOT carry BYPASSRLS, or it sets a GUC ' +
        'on a connection RLS never constrained and proves nothing. Set TEST_APP_DATABASE_URL, or set ' +
        'APP_DB_USER and APP_DB_PASSWORD alongside TEST_DATABASE_URL. Never hardcode the compose ' +
        'default password. DB-gated, never skipped.',
    );
  }
  // KS-1306, a WIDENING of this ticket's scope and recorded as one. Before this, the suite checked
  // only that both DSNs were SET. It performed no host, port or disposability check at all, so it
  // would connect to a shared or a remote Postgres without complaint - and it INSERTs rows. The
  // #1262 precedent is that a test which writes to a database must be unable to reach a shared one.
  //
  // WHY NOT A SEAT'S PORT RANGE, which is how #1262 states the same rule: #1262's cell installs a
  // trigger, so its range is part of a DDL containment argument. This suite writes only INSERTs, and
  // a hardcoded range would refuse every runner outside it - a later formal test pass, a gate on
  // another seat's ports. The two properties that actually protect the row writes are asserted
  // instead: the host must be LOOPBACK (which refuses every remote database outright), and the port
  // must not be a SHARED-STACK port. The shared port is READ from docker-compose.yml's own default
  // rather than pasted here, so this guard cannot drift away from the stack it is protecting.
  for (const [label, dsn] of [['TEST_DATABASE_URL', TEST_DB], ['TEST_APP_DATABASE_URL', TEST_APP_DB]] as const) {
    const u = new URL(dsn as string);
    if (!['127.0.0.1', 'localhost', '::1', '[::1]'].includes(u.hostname)) {
      throw new Error(
        `KS-1306: ${label} points at host "${u.hostname}", which is not loopback. This suite INSERTs ` +
          'rows; it refuses any database it could share with something else. Point it at a disposable ' +
          'Postgres on 127.0.0.1 built from docker/init + scripts/run-migrations.sh.',
      );
    }
    if (SHARED_STACK_PORTS.includes(u.port)) {
      throw new Error(
        `KS-1306: ${label} points at port ${u.port}, which is a shared-stack port ` +
          `(${SHARED_STACK_PORTS.join(', ')} - read from docker-compose.yml). This suite INSERTs rows ` +
          'and refuses the shared dev stack, whose schema drifts. Use a disposable instance on its own port.',
      );
    }
  }
  admin = new Client({ connectionString: TEST_DB });
  await admin.connect();

  // Two tenants, and an organisation in each. Seeded on the admin connection so
  // the seeding itself is not what the cells are measuring.
  for (const [tid, oid, name] of [
    [TENANT_A, ORG_IN_A, 'Org in tenant A'],
    [TENANT_B, ORG_IN_B, 'Org in tenant B'],
  ] as const) {
    await admin.query(
      `INSERT INTO tenants (id, name, slug, status, created_at, updated_at)
       VALUES ($1, $2, $3, 'active', NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
      [tid, `Tenant ${tid.slice(0, 4)}`, `t-${tid.slice(0, 8)}`],
    ).catch(() => undefined); // tenants may live in the platform DB; org rows are what matter
    await admin.query(
      `INSERT INTO organizations (id, tenant_id, name, slug, type, created_at, updated_at)
       VALUES ($1, $2, $3, $4, 'issuer', NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
      [oid, tid, name, `ks597-${oid.slice(0, 8)}`],
    );
  }
});

afterAll(async () => {
  if (admin) {
    await admin.query('DELETE FROM documents WHERE external_id LIKE $1', ['ks597-int-%']);
    await admin.query('DELETE FROM organizations WHERE id = ANY($1::uuid[])', [[ORG_IN_A, ORG_IN_B]]);
    await admin.end();
  }
});

/** A writer connection on one of the two RLS-permissive paths. */
async function writerOn(path: 'platform_bypass' | 'bypassrls'): Promise<Client> {
  // KS-980: the ROLE is what makes these two different mechanisms. 'platform_bypass'
  // takes the ordinary application role, which RLS constrains, so the GUC below is
  // what admits the row. 'bypassrls' keeps TEST_DATABASE_URL, whose role bypasses
  // RLS outright and therefore needs no GUC.
  const c = new Client({
    connectionString: path === 'platform_bypass' ? (TEST_APP_DB as string) : TEST_DB,
  });
  await c.connect();
  await c.query(`SELECT set_config('app.current_tenant_id', $1, false)`, [TENANT_A]);
  if (path === 'platform_bypass') {
    await c.query(`SELECT set_config('app.tenant_scope_bypass', 'platform_admin', false)`);
  }
  return c;
}

describe('KS-597 in a real database — the tenancy predicate is the only thing stopping cross-tenant attribution', () => {
  it.each(['platform_bypass', 'bypassrls'] as const)(
    'on the %s path, another tenant organisation folds to NULL rather than being attributed',
    async (path) => {
      const writer = await writerOn(path);
      try {
        // A document in tenant A, naming tenant B's organisation.
        const extId = `ks597-int-cross-${path}-${randomUUID().slice(0, 8)}`;
        await saveDocument(makeDoc(extId), TENANT_A, poolProxy(writer), {
            // KS-597 bind (Kam, 2026-09-07): the COLUMN is fed by the route-bound
            // `issuerOrganizationId`, not by the raw `sIdentity` claim. Passing the
            // claim alone made all three NULL cells in this file VACUOUS -- they
            // passed because nothing was ever written, which is exactly what the
            // positive control below was put here to catch, and did.
            issuerOrganizationId: ORG_IN_B,
            sIdentity: { organizationUuid: ORG_IN_B },
        });

        // RLS is NOT excluding ORG_IN_B on this path — proved right here, so the
        // NULL below cannot be credited to the policy.
        const { rows } = await writer.query(
          'SELECT id FROM organizations WHERE id = $1',
          [ORG_IN_B],
        );
        expect(rows).toHaveLength(1);

        expect(await readIssuerOrg(extId)).toBeNull();
      } finally {
        await writer.end();
      }
    },
  );

  it('POSITIVE CONTROL: an organisation in the SAME tenant IS attributed, so NULL is a refusal and not an inert column', async () => {
    // Without this, every cell above would pass on a build where
    // issuer_organization_id is never written at all.
    const writer = await writerOn('platform_bypass');
    try {
      const extId = `ks597-int-same-${randomUUID().slice(0, 8)}`;
      await saveDocument(makeDoc(extId), TENANT_A, poolProxy(writer), {
        issuerOrganizationId: ORG_IN_A,
        sIdentity: { organizationUuid: ORG_IN_A },
      });
      expect(await readIssuerOrg(extId)).toBe(ORG_IN_A);
    } finally {
      await writer.end();
    }
  });

  it('CONTROL: an organisation id that exists in NO tenant also folds to NULL', async () => {
    const writer = await writerOn('platform_bypass');
    try {
      const extId = `ks597-int-unknown-${randomUUID().slice(0, 8)}`;
      const unknownOrg = randomUUID();
      await saveDocument(makeDoc(extId), TENANT_A, poolProxy(writer), {
        issuerOrganizationId: unknownOrg,
        sIdentity: { organizationUuid: unknownOrg },
      });
      expect(await readIssuerOrg(extId)).toBeNull();
    } finally {
      await writer.end();
    }
  });
});


describe('KS-980 - the two RLS-permissive paths are two MECHANISMS, not one connection opened twice', () => {
  it('KS-980 D1 - platform_bypass connects as a role RLS constrains; bypassrls connects as one it does not', async () => {
    const p1 = await writerOn('platform_bypass');
    const p2 = await writerOn('bypassrls');
    try {
      // KS-1306: `rolsuper` is asserted ALONGSIDE `rolbypassrls`, because rolbypassrls alone does
      // not decide whether RLS constrains a role. A Postgres SUPERUSER bypasses RLS regardless of
      // rolbypassrls, so a role with `rolsuper = true, rolbypassrls = false` satisfied the previous
      // form of this cell while being exactly the thing the cell reads as "constrained by RLS".
      // MEASURED on a disposable instance built the documented way: the admin role provisioned by
      // `docker/init` is `rolbypassrls = true, rolsuper = true`, and a role can be created with
      // SUPERUSER NOBYPASSRLS, which is the blind spot in a form this suite could actually meet.
      // The GUC cell (KS-980 D2, below) covers the consequence; this cell now covers the premise.
      const sql = 'SELECT rolbypassrls, rolsuper FROM pg_roles WHERE rolname = current_user';
      const onP1 = await p1.query(sql);
      const onP2 = await p2.query(sql);
      // A BYPASSRLS role on P1 makes its GUC inert and leaves P1 untested - the defect this
      // ticket is about. jest's expect() takes one argument, so the label rides inside the
      // asserted object and a failure names the path rather than printing a bare false.
      expect({ path: 'platform_bypass', rolbypassrls: onP1.rows[0].rolbypassrls, rolsuper: onP1.rows[0].rolsuper })
        .toEqual({ path: 'platform_bypass', rolbypassrls: false, rolsuper: false });
      // P2 is the role that is MEANT to bypass. rolbypassrls is the property under test; rolsuper is
      // asserted as a boolean rather than a value, because either setting is a legitimate way to
      // provision an admin role and pinning one would refuse a valid instance. Asserting its TYPE
      // still fails if the column stops being read, which is the failure mode that matters here.
      expect({ path: 'bypassrls', rolbypassrls: onP2.rows[0].rolbypassrls, superIsBoolean: typeof onP2.rows[0].rolsuper === 'boolean' })
        .toEqual({ path: 'bypassrls', rolbypassrls: true, superIsBoolean: true });
    } finally {
      await p1.end();
      await p2.end();
    }
  });

  it('KS-980 D2 - the admin GUC is load-bearing on the platform_bypass connection: strip it and the other tenant organisation disappears', async () => {
    // Deliberately taken from writerOn(), not from a client built here: this cell has to fail
    // if P1 is ever pointed back at a BYPASSRLS connection, and a locally built client would
    // keep passing while the suite under test regressed.
    const p1 = await writerOn('platform_bypass');
    try {
      // Predicate-free - the shape the ticket's own tamper produces. On a BYPASSRLS connection
      // it returns the row whatever the GUC says, which is exactly why the cell above it could
      // not tell the two paths apart.
      const sql = 'SELECT id FROM organizations WHERE id = $1';
      const withGuc = await p1.query(sql, [ORG_IN_B]);
      expect({ guc: 'platform_admin', rows: withGuc.rowCount })
        .toEqual({ guc: 'platform_admin', rows: 1 });
      await p1.query(`SELECT set_config('app.tenant_scope_bypass', '', false)`);
      const withoutGuc = await p1.query(sql, [ORG_IN_B]);
      expect({ guc: 'stripped', rows: withoutGuc.rowCount })
        .toEqual({ guc: 'stripped', rows: 0 });
    } finally {
      await p1.end();
    }
  });
});
