/**
 * =============================================================================
 * KS-1263 — a partly-completed /share or /transfer-custody must leave NOTHING
 * =============================================================================
 * The BEHAVIOURAL half of KS-1263, and the half that cannot be proved in the
 * unit suite: `services/originate/src/__tests__/ks1228-…` mocks `../db`, and a
 * mock cannot ROLL BACK. Its KS-1263 cells prove the STRUCTURE instead (one
 * `withTenant()` per request, both writes on the client it hands out). This
 * suite proves the consequence against a real Postgres.
 *
 * What it pins, from the ticket's D-table:
 *   D1/D2 — /share refuses at recipient k > 1  → ZERO share rows, not k-1.
 *   C7    — /transfer-custody's owner flip throws after the custody INSERT
 *           → ZERO custody_events rows.
 * Before KS-1263 each left the earlier rows behind with no action_provenance
 * row (develop carried one; after KS-1228 it does not).
 *
 * RUNS TWICE where the stack allows it — the two branches of `withTenant()`
 * are different code paths and only one of them is the one production scales to:
 *   - MULTI_TENANCY_ENABLED=false → the Prisma interactive-transaction branch
 *     (db.ts:329-335);
 *   - MULTI_TENANCY_ENABLED=true  → the TenantPoolManager pg-pool branch
 *     (db.ts:306-325), which is what deployment/azure/services.bicep:798 sets.
 * MT_MODES below selects which; the gate runs it once per mode.
 *
 * DB-gated and never silently skipped: without a database `beforeAll` throws a
 * setup error naming what to set. Point it at a Postgres via TEST_DATABASE_URL
 * (falls back to the service's DATABASE_URL).
 *
 * KS-1311 — THE FAULTS HERE ARE TEST VEHICLES, NOT PRODUCT CONCERNS. Read that
 * before treating any of them as a finding:
 *   - The NUL byte (`\u0000`) in a recipient email makes Postgres raise 22021
 *     ("unsupported Unicode escape sequence") at the SECOND write. It is chosen
 *     because it fails DB-SIDE and LATE — after the first row is already in the
 *     transaction — which is the only way to tell a ROLLBACK from a no-op. No
 *     caller sends it and nothing in the product accepts it; it is not a
 *     validation gap and it is not the defect under test.
 *   - Likewise any trigger a cell creates: a fault the cell installs and drops
 *     is a vehicle for reaching the rollback path, never a claim about schema.
 * The DEFECT under test is the transaction boundary. The vehicle is only how the
 * boundary is made observable.
 * =============================================================================
 */

import { randomUUID } from 'crypto';
import { Client } from 'pg';

const DEFAULT_DB = process.env.TEST_DATABASE_URL || process.env.DATABASE_URL;
const MT = process.env.MULTI_TENANCY_ENABLED === 'true';

// KS-1263 round 2 (PLATFORM-URL-TRAP): the platform URL was never mapped, so a run with
// MULTI_TENANCY_ENABLED=true and no PLATFORM_DATABASE_URL made initDb() warn and fall back to
// single-tenant - and the describe title still said "=true". That is a MODE-F run wearing MODE T's
// name. Map it here, and assert the manager exists below, so the label cannot lie.
const PLATFORM_DB = process.env.TEST_PLATFORM_DATABASE_URL || process.env.PLATFORM_DATABASE_URL;
if (PLATFORM_DB) {
  process.env.PLATFORM_DATABASE_URL = PLATFORM_DB;
}

if (DEFAULT_DB) {
  process.env.DATABASE_URL = DEFAULT_DB;
}
process.env.JWT_SECRET = process.env.JWT_SECRET || 'ks1263-integration-secret';
if (process.env.NODE_ENV === 'production' || !process.env.NODE_ENV) {
  process.env.NODE_ENV = 'test';
}

const RUN = randomUUID().slice(0, 8);

// =============================================================================================
// KS-1263 round 2 — the ROUTE-LEVEL cell's seam.
// =============================================================================================
// The three cells below call `withTenant` DIRECTLY, and withTenant already rolled back BEFORE
// this ticket. So they are green on BOTH sides of the change and pin the route's rollback NOT AT
// ALL — the gate's NOT-PINNED ROUTE-ROLLBACK. This block mounts the REAL `documentsRouter` so a
// request travels the route's own code.
//
// The mock set is ks739-transfer-custody-lookup-4xx-mapping.test.ts's, MINUS two:
// `../db` and `../repositories/shareRepo` are REAL here. Mock either and nothing reaches Postgres,
// and a cell that never reaches Postgres cannot tell a rollback from a no-op.
process.env.SIMULATE_ANCHORING = 'true';
// KS-1293: 127.0.0.1:**2**, not :1. Port 1 is on the Fetch spec's bad-port list, so undici refuses
// the request BEFORE opening a socket — the "closed port" this file relies on never actually happens,
// and the error carries no `cause.code`. Measured on node 24: `:2` gives cause.code ECONNREFUSED (a
// socket was attempted and refused); `:1` gives cause.code undefined. That is the erosion KS-1293's
// second acceptance criterion names, and this file was the live instance of it.
process.env.ANCHORING_SERVICE_URL = process.env.ANCHORING_SERVICE_URL || 'http://127.0.0.1:2';

const ROUTE_TENANT = randomUUID();
const ROUTE_DOC_UUID = randomUUID();
const ROUTE_DOC_EXT = `doc-route-${RUN}`;

jest.mock('../repositories/documentRepo', () => ({
  getDocument: jest.fn(async () => ({
    id: ROUTE_DOC_EXT, tenantId: ROUTE_TENANT, title: 'KS-1263 route cell',
    documentType: 'degree', contentHash: 'a'.repeat(64), status: 'draft',
  })),
  listDocuments: jest.fn(), saveDocument: jest.fn(), updateDocument: jest.fn(async () => undefined),
  getSigningRequest: jest.fn(), saveSigningRequest: jest.fn(), deleteSigningRequest: jest.fn(),
  generateContentHash: jest.fn(() => 'a'.repeat(64)), seedDemoDocuments: jest.fn(async () => undefined),
  assertNoCycle: jest.fn(async () => undefined),
}));
jest.mock('../repositories/lifecycleEventRepo', () => ({
  createLifecycleEvent: jest.fn(), setLifecycleEventAnchor: jest.fn(), listLifecycleEvents: jest.fn(),
}));
jest.mock('../events', () => ({
  publishEvent: jest.fn(async () => undefined),
  EventTypes: { DOCUMENT_CREATED: 'document.created', DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred', DOCUMENT_VERSIONED: 'document.versioned', CERTIFICATION_ISSUED: 'certification.issued' },
}));
jest.mock('../services/threadTokenClient', () => ({ mintAndRegisterThreadToken: jest.fn(async () => ({})) }));
jest.mock('../routes/verification', () => ({ registerInPlatformRegistry: jest.fn(async () => undefined) }));
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee', role: 'SYSTEM_ADMIN', tenantId: ROUTE_TENANT };
    next();
  },
}));
jest.mock('../middleware/rbac', () => ({ isAllowedByRoleOrScope: () => true }));
jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

describe(`KS-1263 — the multi-write rolls back (MULTI_TENANCY_ENABLED=${MT})`, () => {
  let sql: Client;
  let withTenant: <T>(tenantId: string, fn: (tx: any) => Promise<T>) => Promise<T>;
  let disconnectDb: () => Promise<void>;
  const tenantId = randomUUID();
  // A REAL document row. shares.target_id and custody_events.document_id are both uuid NOT NULL,
  // and the latter REFERENCES documents(id) - so both writes need this to exist.
  const documentId = randomUUID();

  beforeAll(async () => {
    if (!DEFAULT_DB) {
      throw new Error(
        'KS-1263 integration suite requires a database. Set TEST_DATABASE_URL, ' +
          'or run with the service DATABASE_URL exported. It is never skipped: ' +
          'the rollback it proves is the whole point of the ticket.',
      );
    }
    // Required AFTER the env above - db.ts reads it at import time.
    let db;
    try {
      db = require('../db');
    } catch (err) {
      throw new Error(`KS-1263: could not load ../db - ${(err as Error).message}`);
    }
    withTenant = db.withTenant;
    disconnectDb = db.disconnectDb;
    await db.initDb();
    if (typeof withTenant !== 'function') {
      throw new Error('withTenant is not exported from ../db — the transaction path is missing.');
    }
    sql = new Client({ connectionString: DEFAULT_DB });
    await sql.connect();

    // KS-1263 round 2 (PLATFORM-URL-TRAP): prove the branch this run CLAIMS to be on. With MT set
    // and no platform URL, initDb() falls back to single-tenant and getTenantManager() stays null -
    // the run would then be MODE F under a MODE T title. Fail by name instead.
    if (MT) {
      const manager = typeof db.getTenantManager === 'function' ? db.getTenantManager() : null;
      if (manager === null || manager === undefined) {
        throw new Error(
          'MULTI_TENANCY_ENABLED=true but getTenantManager() is null - initDb() fell back to ' +
            'single-tenant mode. Set TEST_PLATFORM_DATABASE_URL (or PLATFORM_DATABASE_URL) to a ' +
            'real platform database. Refusing to run: this would be a MODE F run labelled MODE T.',
        );
      }
    }

    // Seed a REAL tenant and a REAL document. Round 1's cells wrote a text literal into
    // shares.target_id (uuid NOT NULL) and NULL into custody_events.document_id (uuid NOT NULL
    // REFERENCES documents(id)), so every cell died in the INSERT and none of them ever reached the
    // rollback they exist to prove. These rows are what make the writes legal.
    await sql.query(
      `INSERT INTO tenants (id, name, slug, status, created_at, updated_at)
       VALUES ($1, $2, $3, 'active', NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
      [tenantId, `ks1263-${RUN}`, `ks1263-${RUN}`],
    ).catch(() => undefined);
    await sql.query(
      `INSERT INTO documents (id, tenant_id, title, document_type, content_hash, status, created_at, updated_at)
       VALUES ($1, $2, $3, 'degree', $4, 'draft', NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
      [documentId, tenantId, `KS-1263 ${RUN}`, 'a'.repeat(64)],
    );
    const seeded = await sql.query('SELECT 1 FROM documents WHERE id = $1', [documentId]);
    if (seeded.rowCount !== 1) {
      throw new Error(`KS-1263: the seeded document ${documentId} is not readable - the cells below would be vacuous.`);
    }

    // KS-1311: the MODE T guard above proves a MANAGER OBJECT EXISTS. It does not prove the tenant
    // CONFIGS LOADED, and a manager with an empty config map routes every checkout to the default
    // pool - which is MODE T's object wearing MODE F's behaviour, the same class as the
    // PLATFORM-URL-TRAP one level down. `tenantConfigs` is private, but `getTenantStatus()` reads it,
    // so it is an observable proxy: after a refresh, a seeded ACTIVE tenant must be visible through
    // it. The tenant is only seeded above, which is why this sits here and not with the guard.
    if (MT) {
      const manager = db.getTenantManager();
      if (typeof manager?.refreshConfigs === 'function') await manager.refreshConfigs();
      const status = typeof manager?.getTenantStatus === 'function' ? manager.getTenantStatus(tenantId) : undefined;
      if (status === undefined) {
        throw new Error(
          `KS-1311: MULTI_TENANCY_ENABLED=true and a manager exists, but after refreshConfigs() the ` +
            `seeded tenant ${tenantId} is invisible to getTenantStatus() - the tenant configs did not ` +
            `load from the platform database. Every checkout would fall to the default pool, so this ` +
            `run would exercise MODE F behaviour under a MODE T title. Refusing to run.`,
        );
      }
    }
  });

  afterAll(async () => {
    if (sql) {
      await sql.query('DELETE FROM shares WHERE tenant_id = $1', [tenantId]).catch(() => undefined);
      await sql.query('DELETE FROM custody_events WHERE tenant_id = $1', [tenantId]).catch(() => undefined);
      await sql.query('DELETE FROM documents WHERE id = $1', [documentId]).catch(() => undefined);
      await sql.query('DELETE FROM tenants WHERE id = $1', [tenantId]).catch(() => undefined);
      await sql.end().catch(() => undefined);
    }
    if (disconnectDb) await disconnectDb().catch(() => undefined);
  });

  const countShares = async (): Promise<number> => {
    const r = await sql.query('SELECT COUNT(*)::int AS n FROM shares WHERE tenant_id = $1', [tenantId]);
    return r.rows[0].n;
  };
  const countCustody = async (): Promise<number> => {
    const r = await sql.query('SELECT COUNT(*)::int AS n FROM custody_events WHERE tenant_id = $1', [tenantId]);
    return r.rows[0].n;
  };

  it('CONTROL — a withTenant callback that completes COMMITS its writes', async () => {
    const before = await countShares();
    await withTenant(tenantId, async (tx) => {
      await tx.$executeRaw`
        INSERT INTO shares (id, tenant_id, target_type, target_id, recipient_email, share_type, status, created_at, updated_at)
        VALUES (${randomUUID()}::uuid, ${tenantId}::uuid, 'document', ${documentId}::uuid, ${'ctl-' + RUN + '@example.test'}, 'view', 'active', NOW(), NOW())
      `;
    });
    expect(await countShares()).toBe(before + 1);
  });

  it('🔴 D1/D2 — a throw after the FIRST of two share rows leaves ZERO, not one', async () => {
    const before = await countShares();
    await expect(
      withTenant(tenantId, async (tx) => {
        await tx.$executeRaw`
          INSERT INTO shares (id, tenant_id, target_type, target_id, recipient_email, share_type, status, created_at, updated_at)
          VALUES (${randomUUID()}::uuid, ${tenantId}::uuid, 'document', ${documentId}::uuid, ${'d1-' + RUN + '@example.test'}, 'view', 'active', NOW(), NOW())
        `;
        // recipient 2 refuses, exactly as SHARE_TARGET_NOT_FOUND does in the route
        throw Object.assign(new Error('recipient 2 refused'), { code: 'SHARE_TARGET_NOT_FOUND' });
      }),
    ).rejects.toMatchObject({ code: 'SHARE_TARGET_NOT_FOUND' });
    // The whole point: recipient 1's row is GONE, not orphaned.
    expect(await countShares()).toBe(before);
  });

  it('🔴 C7 — a throw after the custody INSERT leaves ZERO custody_events rows', async () => {
    const before = await countCustody();
    await expect(
      withTenant(tenantId, async (tx) => {
        await tx.$executeRaw`
          INSERT INTO custody_events (id, tenant_id, document_id, to_holder_id, transferred_by_id, effective_at, created_at)
          VALUES (${randomUUID()}::uuid, ${tenantId}::uuid, ${documentId}::uuid, ${randomUUID()}::uuid, ${randomUUID()}::uuid, NOW(), NOW())
        `;
        // the owner flip throws
        throw new Error('owner flip failed');
      }),
    ).rejects.toThrow('owner flip failed');
    expect(await countCustody()).toBe(before);
  });
});


// =================================================================================================
// KS-1263 round 2 — THE ROUTE-LEVEL CELL. RED AT BASE, GREEN AT HEAD.
// =================================================================================================
// What the three cells above cannot do. They call `withTenant` directly, and withTenant rolled back
// at BASE too, so they are green on both sides. This one sends a REQUEST through the real
// `/api/documents/:id/share`, over the real `../db` and the real `createShare`, and asks the only
// question that separates the two trees:
//
//     recipient 2's email carries U+0000 -> Postgres 22021 at k = 2.
//     BASE  leaves 1 share row (recipient 1 committed on its own statement).
//     HEAD  leaves 0 (one transaction, rolled back).
//
// A red at BASE must name WHY: "1 row where 0 expected". A connection or auth error is a LOUD
// failure, never a red — the cell would otherwise pass for the wrong reason on a broken database.
describe('KS-1263 ROUTE-LEVEL — /share rolls back the whole multi-write (MULTI_TENANCY_ENABLED=' + String(MT) + ')', () => {
  let sql2: Client;
  let server: any;
  let baseUrl = '';
  let disconnect2: () => Promise<void>;

  const NUL_EMAIL = 'r2-' + RUN + '\u0000@example.test';

  beforeAll(async () => {
    if (!DEFAULT_DB) {
      throw new Error('KS-1263 route cell requires a database. Set TEST_DATABASE_URL. It is never skipped.');
    }
    const db = require('../db');
    await db.initDb();
    disconnect2 = db.disconnectDb;
    if (MT) {
      const manager = typeof db.getTenantManager === 'function' ? db.getTenantManager() : null;
      if (manager === null || manager === undefined) {
        throw new Error(
          'MULTI_TENANCY_ENABLED=true but getTenantManager() is null — this would be a MODE F run ' +
            'labelled MODE T. Set TEST_PLATFORM_DATABASE_URL. Refusing to run.',
        );
      }
    }

    // ---------------------------------------------------------------------------------------
    // THE SEAM PROBE — why it exists, measured.
    // ---------------------------------------------------------------------------------------
    // In MODE F this suite's client is Prisma, and a fresh worktree has no generated Prisma client
    // (KS-1305). `createShare` then throws a MODULE error for recipient 1 as well, so the route
    // writes NOTHING — and `ROUTE-ROLLBACK`'s "0 share rows" assertion PASSES for the exact wrong
    // reason: 0 because nothing ran, not 0 because the transaction rolled back. Measured on
    // 2026-09-25: MODE F reported `4 failed, 1 passed`, and the ONE green was ROUTE-ROLLBACK.
    // A vacuous green is worse than a red, so the mode is proved REACHABLE here and the whole
    // describe fails by name when it is not. Never let this cell report a pass it did not earn.
    try {
      await db.prisma.$queryRaw`SELECT 1`;
    } catch (err) {
      throw new Error(
        'KS-1263 route cell: the ROUTE\'s own db client cannot reach Postgres — ' +
          `${(err as Error).message}. Refusing to run: every cell below would report 0 share rows ` +
          'because nothing was written, which is indistinguishable from a successful rollback. ' +
          'In MODE F this is the missing generated Prisma client (residual, ticket KS-1305).',
      );
    }

    sql2 = new Client({ connectionString: DEFAULT_DB });
    await sql2.connect();
    // A REAL tenant and a REAL document. createShare resolves shares.target_id through
    // `SELECT id FROM documents WHERE external_id = $targetId AND tenant_id = $tenantId`, so the
    // EXTERNAL id is what the route is called with and what must exist. Without it the first INSERT
    // writes NULL into a NOT NULL column and dies at k = 1 — the cell would be vacuous on both sides.
    await sql2.query(
      `INSERT INTO tenants (id, name, slug, status, created_at, updated_at)
       VALUES ($1, $2, $3, 'active', NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
      [ROUTE_TENANT, `ks1263-route-${RUN}`, `ks1263-route-${RUN}`],
    ).catch(() => undefined);
    await sql2.query(
      `INSERT INTO documents (id, tenant_id, external_id, title, document_type, content_hash, status, created_at, updated_at)
       VALUES ($1, $2, $3, $4, 'degree', $5, 'draft', NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
      [ROUTE_DOC_UUID, ROUTE_TENANT, ROUTE_DOC_EXT, `KS-1263 route ${RUN}`, 'a'.repeat(64)],
    );
    const seeded = await sql2.query(
      'SELECT 1 FROM documents WHERE external_id = $1 AND tenant_id = $2',
      [ROUTE_DOC_EXT, ROUTE_TENANT],
    );
    if (seeded.rowCount !== 1) {
      throw new Error(
        `KS-1263 route cell: the seeded document ${ROUTE_DOC_EXT} is not resolvable by external_id — ` +
          'createShare would write NULL into shares.target_id and the cell would be vacuous.',
      );
    }

    const express = require('express');
    const { documentsRouter } = require('../routes/documents');
    const app = express();
    app.use((req: any, _res: unknown, next: () => void) => {
      req.user = { userId: 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee', role: 'SYSTEM_ADMIN', tenantId: ROUTE_TENANT };
      req.tenantId = ROUTE_TENANT;
      // What index.ts:225 hands a request. At BASE the loop writes through THIS client; at head the
      // route ignores it and uses withTenant(). Setting it explicitly keeps BASE faithful rather
      // than resting on createShare's `(db || prisma)` fallback.
      req.db = db.getRequestPrisma(req);
      next();
    });
    app.use('/api/documents', express.json(), documentsRouter);
    await new Promise<void>((resolve) => {
      server = app.listen(0, '127.0.0.1', () => resolve());
    });
    baseUrl = `http://127.0.0.1:${server.address().port}`;
  });

  afterAll(async () => {
    if (server) await new Promise<void>((resolve) => server.close(() => resolve()));
    if (sql2) {
      await sql2.query('DELETE FROM shares WHERE tenant_id = $1', [ROUTE_TENANT]).catch(() => undefined);
      await sql2.query('DELETE FROM documents WHERE id = $1', [ROUTE_DOC_UUID]).catch(() => undefined);
      await sql2.query('DELETE FROM tenants WHERE id = $1', [ROUTE_TENANT]).catch(() => undefined);
      await sql2.end().catch(() => undefined);
    }
    if (disconnect2) await disconnect2().catch(() => undefined);
  });

  const countRouteShares = async (): Promise<number> => {
    const r = await sql2.query('SELECT COUNT(*)::int AS n FROM shares WHERE tenant_id = $1', [ROUTE_TENANT]);
    return r.rows[0].n;
  };

  it('CONTROL — two clean recipients through the ROUTE both land (the seam reaches Postgres)', async () => {
    const before = await countRouteShares();
    const res = await fetch(`${baseUrl}/api/documents/${ROUTE_DOC_EXT}/share`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ recipients: [{ email: `ok1-${RUN}@example.test` }, { email: `ok2-${RUN}@example.test` }] }),
    });
    // Without this control a route that refused everything would make the cell below green for
    // exactly the wrong reason: 0 rows because nothing was ever written.
    expect(res.status).toBeLessThan(400);
    expect(await countRouteShares()).toBe(before + 2);
    await sql2.query('DELETE FROM shares WHERE tenant_id = $1', [ROUTE_TENANT]);
  });

  it('🔴 ROUTE-ROLLBACK — a 22021 at recipient 2 leaves ZERO share rows, not one', async () => {
    const before = await countRouteShares();
    expect(before).toBe(0);
    const res = await fetch(`${baseUrl}/api/documents/${ROUTE_DOC_EXT}/share`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ recipients: [{ email: `r1-${RUN}@example.test` }, { email: NUL_EMAIL }] }),
    });
    // The request MUST have failed, and not at validation: a 400 would mean recipient 1 was never
    // written and 0 rows proves nothing.
    expect(res.status).toBeGreaterThanOrEqual(500);
    const after = await countRouteShares();
    expect(after).toBe(0);
  });
});

// =============================================================================================
// KS-1310 — /transfer-custody's ROUTE-LEVEL rollback
// =============================================================================================
// C7 above already proves the custody rollback INSIDE a withTenant callback: it throws in the
// callback, which is a JS-side fault the route itself would never produce. What was unpinned is the
// ROUTE path — the real documentsRouter over the real db, where the fault has to come from the
// DATABASE because there is no seam to throw from.
//
// WHY THE FAULT IS A TRIGGER, and why the NUL byte is NOT reused here (Wednesday's ruling (a),
// 2026-09-25): /transfer-custody writes twice inside one transaction — INSERT custody_events, then
// the owner flip on documents. To prove a ROLLBACK the fault must hit the FLIP, so the INSERT has
// already succeeded and must be undone. A NUL byte in `reason` is consumed by the INSERT, so the
// insert dies, nothing is ever written, and "0 custody rows" is true for the WRONG REASON — it
// proves insert-failure, not rollback. That is a vacuous cell wearing the right assertion. A
// BEFORE UPDATE trigger scoped to this one document fires on the flip and not the insert.
// The trigger is a TEST VEHICLE, exactly as the NUL byte is — see the header.
const FLIP_TAG = `ks1310_flipfault_${RUN.replace(/-/g, '')}`;
const FLIP_MSG = `KS1310 FLIP FAULT ${RUN}`;
const CUSTODY_TENANT = randomUUID();
const CUSTODY_DOC_UUID = randomUUID();
const CUSTODY_DOC_EXT = `doc-custody-${RUN}`;
const ORIGINAL_OWNER = randomUUID();
const NEW_HOLDER = randomUUID();
const ACTOR = randomUUID();

describe('KS-1310 ROUTE-LEVEL — a failed owner flip leaves ZERO custody rows and an UNFLIPPED owner (MULTI_TENANCY_ENABLED=' + String(MT) + ')', () => {
  let sql3: Client;
  let server3: any;
  let base3 = '';
  let disconnect3: () => Promise<void>;
  let mockedLogger: { error: jest.Mock; info: jest.Mock; warn: jest.Mock; debug: jest.Mock };

  const countCustody = async (): Promise<number> => {
    const r = await sql3.query('SELECT COUNT(*)::int AS n FROM custody_events WHERE tenant_id = $1', [CUSTODY_TENANT]);
    return r.rows[0].n;
  };
  const ownerOf = async (): Promise<string | null> => {
    const r = await sql3.query('SELECT owner_user_id FROM documents WHERE id = $1', [CUSTODY_DOC_UUID]);
    return r.rows[0]?.owner_user_id ?? null;
  };
  const triggerRows = async (): Promise<number> => {
    const r = await sql3.query(
      `SELECT (SELECT COUNT(*) FROM pg_trigger WHERE tgname = $1)
            + (SELECT COUNT(*) FROM pg_proc WHERE proname = $1) AS n`,
      [FLIP_TAG],
    );
    return Number(r.rows[0].n);
  };
  const installFlipFault = async (): Promise<void> => {
    await sql3.query(
      `CREATE OR REPLACE FUNCTION ${FLIP_TAG}() RETURNS trigger AS $fn$
       BEGIN RAISE EXCEPTION '${FLIP_MSG}' USING ERRCODE = 'P0001'; END;
       $fn$ LANGUAGE plpgsql`,
    );
    await sql3.query(
      `CREATE TRIGGER ${FLIP_TAG} BEFORE UPDATE ON documents
       FOR EACH ROW WHEN (OLD.id = '${CUSTODY_DOC_UUID}'::uuid) EXECUTE FUNCTION ${FLIP_TAG}()`,
    );
  };
  const dropFlipFault = async (): Promise<void> => {
    await sql3.query(`DROP TRIGGER IF EXISTS ${FLIP_TAG} ON documents`).catch(() => undefined);
    await sql3.query(`DROP FUNCTION IF EXISTS ${FLIP_TAG}()`).catch(() => undefined);
  };
  const transfer = (body: Record<string, unknown>) =>
    fetch(`${base3}/api/documents/${CUSTODY_DOC_EXT}/transfer-custody`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body),
    });

  beforeAll(async () => {
    if (!DEFAULT_DB) throw new Error('KS-1310 needs a database. Set TEST_DATABASE_URL.');

    // CONDITION 4 — DISPOSABLE DATABASE ONLY. This describe creates a TRIGGER, which is schema DDL.
    // A cell that writes DDL must be UNABLE to reach a shared or real database, so this is a
    // refusal and not a warning: loopback host, and a port inside this seat's own allocated range.
    const dsn = new URL(DEFAULT_DB);
    const port = Number(dsn.port);
    if (!['127.0.0.1', 'localhost'].includes(dsn.hostname) || !(port >= 55410 && port <= 55419)) {
      throw new Error(
        `KS-1310 installs a trigger (schema DDL) and therefore refuses any database that is not this ` +
          `seat's disposable one. Got host=${dsn.hostname} port=${dsn.port || '(none)'}; required ` +
          `host 127.0.0.1/localhost and port 55410-55419. Refusing to run rather than write DDL ` +
          `somewhere shared.`,
      );
    }

    const db = require('../db');
    await db.initDb();
    disconnect3 = db.disconnectDb;
    mockedLogger = require('../utils/logger').logger;

    // `../repositories/documentRepo` is MOCKED for this whole file (:93), and its canned document
    // belongs to the /share describe and carries NO `owner` — so `doc.owner.id` in the handler threw
    // before the transaction was ever reached, and the request 500'd for a reason that had nothing to
    // do with the rollback. The CONTROL cell is what caught that: without it the red cell's "0 custody
    // rows" would have been green for exactly the wrong reason.
    // The WRITES are unaffected by this mock and stay real: the custody INSERT resolves document_id
    // with a subquery against Postgres, and the owner flip is `tx.$executeRaw UPDATE documents` — both
    // inside withTenant, which is why a DB-side trigger can fault the flip at all.
    // Scoped by external id so the sibling /share describe keeps the canned document it expects,
    // whatever order the describes run in.
    const repoMock = require('../repositories/documentRepo');
    const cannedForShare = {
      id: ROUTE_DOC_EXT, tenantId: ROUTE_TENANT, title: 'KS-1263 route cell',
      documentType: 'degree', contentHash: 'a'.repeat(64), status: 'draft',
    };
    repoMock.getDocument.mockImplementation(async (extId: string) =>
      extId === CUSTODY_DOC_EXT
        ? {
            id: CUSTODY_DOC_EXT, tenantId: CUSTODY_TENANT, title: `KS-1310 ${RUN}`,
            documentType: 'degree', contentHash: 'c'.repeat(64), status: 'draft',
            owner: { id: ORIGINAL_OWNER },
          }
        : cannedForShare,
    );

    // The same seam probe the /share route describe carries: in MODE F a missing generated Prisma
    // client makes the route write NOTHING, and "0 custody rows" would then pass for the wrong
    // reason (residual, ticket KS-1305).
    try {
      await db.prisma.$queryRaw`SELECT 1`;
    } catch (err) {
      throw new Error(
        `KS-1310: the ROUTE's own db client cannot reach Postgres — ${(err as Error).message}. ` +
          'Refusing to run: every cell below would report 0 custody rows because nothing was written, ' +
          'which is indistinguishable from a successful rollback.',
      );
    }

    sql3 = new Client({ connectionString: DEFAULT_DB });
    await sql3.connect();
    await sql3.query(
      `INSERT INTO tenants (id, name, slug, status, created_at, updated_at)
       VALUES ($1, $2, $3, 'active', NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
      [CUSTODY_TENANT, `ks1310-${RUN}`, `ks1310-${RUN}`],
    ).catch(() => undefined);
    // The holder must EXIST: since KS-697 the id path 404s an unknown holder before the transaction,
    // so without this row the cell would measure that 404 and never reach the rollback path at all.
    for (const [id, email] of [[ORIGINAL_OWNER, `owner-${RUN}@example.test`], [NEW_HOLDER, `holder-${RUN}@example.test`], [ACTOR, `actor-${RUN}@example.test`]] as const) {
      await sql3.query(
        `INSERT INTO users (id, tenant_id, email, created_at, updated_at)
         VALUES ($1, $2, $3, NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
        [id, CUSTODY_TENANT, email],
      ).catch(() => undefined);
    }
    await sql3.query(
      `INSERT INTO documents (id, tenant_id, external_id, title, document_type, content_hash, status, owner_user_id, created_at, updated_at)
       VALUES ($1, $2, $3, $4, 'degree', $5, 'draft', $6, NOW(), NOW()) ON CONFLICT (id) DO NOTHING`,
      [CUSTODY_DOC_UUID, CUSTODY_TENANT, CUSTODY_DOC_EXT, `KS-1310 ${RUN}`, 'c'.repeat(64), ORIGINAL_OWNER],
    );
    const seeded = await sql3.query('SELECT owner_user_id FROM documents WHERE external_id = $1 AND tenant_id = $2', [CUSTODY_DOC_EXT, CUSTODY_TENANT]);
    if (seeded.rowCount !== 1 || seeded.rows[0].owner_user_id !== ORIGINAL_OWNER) {
      throw new Error(
        `KS-1310: the seeded document is not resolvable by external_id with owner ${ORIGINAL_OWNER} — ` +
          'the "unflipped owner" assertion would have nothing to compare against.',
      );
    }

    const express = require('express');
    const { documentsRouter } = require('../routes/documents');
    const app = express();
    app.use((req: any, _res: unknown, next: () => void) => {
      req.user = { userId: ACTOR, role: 'SYSTEM_ADMIN', tenantId: CUSTODY_TENANT };
      req.tenantId = CUSTODY_TENANT;
      req.db = db.getRequestPrisma(req);
      next();
    });
    app.use('/api/documents', express.json(), documentsRouter);
    await new Promise<void>((resolve) => {
      server3 = app.listen(0, '127.0.0.1', () => resolve());
    });
    base3 = `http://127.0.0.1:${server3.address().port}`;
  });

  afterAll(async () => {
    // CONDITION 2 — ALWAYS DROPPED, including on failure. A leftover trigger on `documents` would
    // poison every later cell on this database, so the drop is unconditional here rather than at the
    // end of the red cell.
    try {
      if (sql3) await dropFlipFault();
    } finally {
      if (sql3) {
        await sql3.query('DELETE FROM custody_events WHERE tenant_id = $1', [CUSTODY_TENANT]).catch(() => undefined);
        await sql3.query('DELETE FROM documents WHERE id = $1', [CUSTODY_DOC_UUID]).catch(() => undefined);
        await sql3.query('DELETE FROM users WHERE tenant_id = $1', [CUSTODY_TENANT]).catch(() => undefined);
        await sql3.query('DELETE FROM tenants WHERE id = $1', [CUSTODY_TENANT]).catch(() => undefined);
        await sql3.end().catch(() => undefined);
      }
      if (disconnect3) await disconnect3().catch(() => undefined);
      if (server3) await new Promise<void>((resolve) => server3.close(() => resolve()));
    }
  });

  it('CONTROL — a clean transfer writes ONE custody row and DOES flip the owner (the seam reaches Postgres)', async () => {
    // Without this, a route that refused everything would make the red cell green for exactly the
    // wrong reason: 0 rows because nothing was ever written.
    expect(await countCustody()).toBe(0);
    const res = await transfer({ newHolderId: NEW_HOLDER, reason: `control ${RUN}` });
    expect(res.status).toBe(201);
    expect(await countCustody()).toBe(1);
    expect(await ownerOf()).toBe(NEW_HOLDER);
    // put the document back so the red cell starts from the same state this one did
    await sql3.query('DELETE FROM custody_events WHERE tenant_id = $1', [CUSTODY_TENANT]);
    await sql3.query('UPDATE documents SET owner_user_id = $1 WHERE id = $2', [ORIGINAL_OWNER, CUSTODY_DOC_UUID]);
    expect(await ownerOf()).toBe(ORIGINAL_OWNER);
  });

  it('🔴 ROUTE-CUSTODY-ROLLBACK — a DB-side fault on the owner flip leaves ZERO custody rows and the owner UNFLIPPED', async () => {
    expect(await countCustody()).toBe(0);
    expect(await ownerOf()).toBe(ORIGINAL_OWNER);
    expect(await triggerRows()).toBe(0);

    await installFlipFault();
    try {
      // CONDITION 5 — the vehicle is PRESENT while the cell runs, measured rather than assumed.
      expect(await triggerRows()).toBe(2); // the trigger and its function

      mockedLogger.error.mockClear();
      const res = await transfer({ newHolderId: NEW_HOLDER, reason: `flip fault ${RUN}` });

      // A 400 or 404 would mean the request never reached the transaction, and 0 rows would prove
      // nothing. It must fail at the WRITE.
      expect(res.status).toBeGreaterThanOrEqual(500);

      // CONDITION 3 — the fault the route received is THE TRIGGER'S, not a connection error and not
      // a refusal. The HTTP body is deliberately generic ('Failed to transfer custody'), so the
      // assertion is made on what the route actually saw and logged.
      const logged = mockedLogger.error.mock.calls.map((c) => JSON.stringify(c)).join(' | ');
      expect(logged).toContain(FLIP_MSG);

      // The rollback itself: the INSERT had already run inside the transaction, and neither write survives.
      expect(await countCustody()).toBe(0);
      expect(await ownerOf()).toBe(ORIGINAL_OWNER);
    } finally {
      await dropFlipFault();
    }

    // CONDITION 2 — proven gone from the catalogue, not merely dropped.
    expect(await triggerRows()).toBe(0);
  });
});

