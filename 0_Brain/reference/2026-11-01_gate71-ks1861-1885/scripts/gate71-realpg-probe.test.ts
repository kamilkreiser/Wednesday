/**
 * QA GATE 71 probe (KS-1861 #1885). The tenant-provisioning entry module is imported for real with the REAL `pg`
 * driver against the throwaway container gate71-pg (platform schema from docker/init-platform, plus the gate-only
 * fault triggers in scripts/pg_faults.sql). Only the JWT middleware is replaced by a pass-through.
 *
 * Cells:
 *  M-*   status route, all 16 (from, to) pairs over {provisioning, active, suspended, archived}
 *  D-*   Delete from each of the 4 statuses, with PROVISION_PER_TENANT_DB / MULTI_TENANCY_ENABLED in 3x3 combinations
 *  E-*   Delete error paths: no confirm, unknown id, malformed id, update fails, audit fails, both audits fail
 *  V-*   reversal: Delete -> archived -> suspended -> active, then the tenant is archivable again
 *  C-*   concurrency on real row locks: two Deletes; Delete vs status change; Delete vs reactivation
 *  S-*   status route's own audit atomicity (unchanged code, measured because it now carries the reversal)
 * Every Delete cell asserts: every row in every public table is kept (row counts and the tenant's own rows), the
 * per-tenant database secuura_tenant_<slug> still exists, and the exact audit rows written.
 * usage: GATE71_PG_URL=postgres://... vitest run src/__tests__/gate71-realpg-probe.test.ts
 */
import { describe, it, expect, beforeAll, afterAll, beforeEach, afterEach, vi } from 'vitest';
import net from 'node:net';
import type { AddressInfo } from 'node:net';
import pg from 'pg';


vi.mock('@secuura/shared', async (importOriginal) => {
  const real = (await importOriginal()) as Record<string, unknown>;
  return { ...real, authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next() };
});

const URL_ = process.env.GATE71_PG_URL as string;
const ADMIN_URL = URL_.replace(/\/secuura_platform$/, '/postgres');
const ID = 'a7100000-0000-4000-8000-000000000071';
const UNKNOWN = 'a7100000-0000-4000-8000-0000000000ff';
const SLUG = 'gate71-acme';
const TENANT_DB = 'secuura_tenant_gate71_acme';
const STATUSES = ['provisioning', 'active', 'suspended', 'archived'] as const;
// The rulings: KS-1860 order + KS-1861 (b) archived -> suspended. Delete: provisioning/active/suspended -> archived.
const RULED_STATUS_MOVES = new Set(['provisioning>active', 'active>suspended', 'suspended>active', 'suspended>archived', 'archived>suspended']);
const RULED_ARCHIVABLE = new Set(['provisioning', 'active', 'suspended']);
const CONSTANT_500 = { success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } };
const ARCHIVED_ANSWER = {
  success: true, deleted: false, archived: true, status: 'archived',
  message: 'Tenant archived. No data was removed: every row is kept and no database is dropped.',
};

let c: pg.Client;
let admin: pg.Client;
let base = '';
const saved = { p: process.env.PROVISION_PER_TENANT_DB, m: process.env.MULTI_TENANCY_ENABLED };

async function freePort(): Promise<number> {
  const s = net.createServer();
  await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
  const port = (s.address() as AddressInfo).port;
  await new Promise<void>((r) => s.close(() => r()));
  return port;
}

beforeAll(async () => {
  c = new pg.Client({ connectionString: URL_ }); await c.connect();
  admin = new pg.Client({ connectionString: ADMIN_URL }); await admin.connect();
  const exists = await admin.query('SELECT 1 FROM pg_database WHERE datname = $1', [TENANT_DB]);
  if (!exists.rowCount) await admin.query(`CREATE DATABASE "${TENANT_DB}"`);
  const port = await freePort();
  process.env.PORT = String(port);
  process.env.PLATFORM_DATABASE_URL = URL_;
  process.env.DATABASE_URL = URL_;
  await import('../index.js');
  base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i += 1) {
    try { await fetch(base + '/health'); break; } catch { await new Promise((r) => setTimeout(r, 30)); }
  }
}, 60_000);

afterAll(async () => { await c.end(); await admin.end(); });

async function seed(status: string): Promise<void> {
  await c.query('DELETE FROM gate_fault');
  await c.query('DELETE FROM platform_audit_log WHERE target_id = $1', [ID]);
  await c.query('DELETE FROM platform_document_registry WHERE tenant_id = $1', [ID]);
  await c.query('DELETE FROM tenants WHERE id = $1', [ID]); // cascades contacts, config, vault_entries (gate DB only)
  await c.query(`INSERT INTO tenants (id, name, slug, status) VALUES ($1, 'Gate71 Acme', $2, $3)`, [ID, SLUG, status]);
  await c.query(`INSERT INTO tenant_contacts (tenant_id, name, email) VALUES ($1, 'A', 'a@example.test')`, [ID]);
  await c.query(`INSERT INTO tenant_config (tenant_id, db_name) VALUES ($1, $2)`, [ID, TENANT_DB]);
  await c.query(`INSERT INTO vault_entries (tenant_id, token, encrypted_value, iv, auth_tag) VALUES ($1, 'tok71', '\\x00', 'aa', '\\x00')`, [ID]);
  await c.query(`INSERT INTO platform_document_registry (content_hash, document_id, tenant_id, tenant_slug) VALUES ('h71', 'd71', $1, $2)`, [ID, SLUG]);
  const exists = await admin.query('SELECT 1 FROM pg_database WHERE datname = $1', [TENANT_DB]);
  if (!exists.rowCount) await admin.query(`CREATE DATABASE "${TENANT_DB}"`);
}

async function snapshot(): Promise<Record<string, number>> {
  const t = await c.query(`SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename NOT IN ('platform_audit_log', 'gate_fault') ORDER BY 1`);
  const out: Record<string, number> = {};
  for (const r of t.rows) out[r.tablename] = Number((await c.query(`SELECT count(*) AS n FROM "${r.tablename}"`)).rows[0].n);
  for (const tbl of ['tenant_contacts', 'tenant_config', 'vault_entries', 'platform_document_registry']) {
    out[`own:${tbl}`] = Number((await c.query(`SELECT count(*) AS n FROM ${tbl} WHERE tenant_id = $1`, [ID])).rows[0].n);
  }
  out['own:tenants'] = Number((await c.query('SELECT count(*) AS n FROM tenants WHERE id = $1', [ID])).rows[0].n);
  out['db:' + TENANT_DB] = (await admin.query('SELECT 1 FROM pg_database WHERE datname = $1', [TENANT_DB])).rowCount ?? 0;
  out['dbs'] = Number((await admin.query('SELECT count(*) AS n FROM pg_database')).rows[0].n);
  return out;
}
const status = async () => (await c.query('SELECT status FROM tenants WHERE id = $1', [ID])).rows[0]?.status;
const audit = async () => (await c.query(`SELECT action, details FROM platform_audit_log WHERE target_id = $1 ORDER BY created_at, id`, [ID])).rows
  .map((r) => ({ action: r.action, details: r.details }));

async function call(method: string, path: string, body?: unknown): Promise<{ code: number; body: any }> {
  const r = await fetch(base + path, { method, headers: { 'content-type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
  return { code: r.status, body: await r.json().catch(() => ({})) };
}
const del = (id = ID, body: unknown = { confirm: true }) => call('DELETE', `/api/tenants/${id}`, body);
const patch = (to: string, id = ID) => call('PATCH', `/api/tenants/${id}/status`, { status: to });

afterEach(() => {
  if (saved.p === undefined) delete process.env.PROVISION_PER_TENANT_DB; else process.env.PROVISION_PER_TENANT_DB = saved.p;
  if (saved.m === undefined) delete process.env.MULTI_TENANCY_ENABLED; else process.env.MULTI_TENANCY_ENABLED = saved.m;
});

describe('gate71 Q1 status route, 16 pairs (real PG)', () => {
  for (const from of STATUSES) for (const to of STATUSES) {
    it(`gate71 M ${from}>${to}`, async () => {
      await seed(from);
      const before = await snapshot();
      const r = await patch(to);
      if (to === 'provisioning') {
        expect(r.code).toBe(400);
        expect(r.body).toEqual({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid status' } });
        expect(await status()).toBe(from);
        expect(await audit()).toEqual([]);
      } else if (RULED_STATUS_MOVES.has(`${from}>${to}`)) {
        expect(r.code).toBe(200);
        expect(r.body).toEqual({ success: true, status: to });
        expect(await status()).toBe(to);
        expect(await audit()).toEqual([{ action: 'tenant_status_changed', details: { status: to } }]);
      } else {
        expect(r.code).toBe(409);
        expect(r.body).toEqual({ success: false, error: { code: 'CONFLICT', message: `Cannot change tenant status from ${from} to ${to}` } });
        expect(await status()).toBe(from);
        expect(await audit()).toEqual([]);
      }
      expect(await snapshot()).toEqual(before);
    });
  }
});

describe('gate71 Q1/Q2 Delete from each status x flags (real PG)', () => {
  const FLAGS: Array<string | undefined> = ['true', 'false', undefined];
  for (const from of STATUSES) for (const p of FLAGS) for (const m of FLAGS) {
    it(`gate71 D ${from} PROVISION_PER_TENANT_DB=${p} MULTI_TENANCY_ENABLED=${m}`, async () => {
      if (p === undefined) delete process.env.PROVISION_PER_TENANT_DB; else process.env.PROVISION_PER_TENANT_DB = p;
      if (m === undefined) delete process.env.MULTI_TENANCY_ENABLED; else process.env.MULTI_TENANCY_ENABLED = m;
      await seed(from);
      const before = await snapshot();
      const r = await del();
      if (RULED_ARCHIVABLE.has(from)) {
        expect(r.code).toBe(200);
        expect(r.body).toEqual(ARCHIVED_ANSWER);
        expect(await status()).toBe('archived');
        expect(await audit()).toEqual([{ action: 'tenant_archived', details: { slug: SLUG, previousStatus: from, erased: false } }]);
      } else {
        expect(r.code).toBe(409);
        expect(r.body).toEqual({ success: false, error: { code: 'CONFLICT', message: 'Tenant is already archived' } });
        expect(await status()).toBe('archived');
        expect(await audit()).toEqual([]);
      }
      expect(await snapshot()).toEqual(before); // every row kept, the tenant DB still exists, no DB dropped
    });
  }
});

describe('gate71 Q2/Q4 Delete error paths (real PG)', () => {
  it('gate71 E1 no confirm -> 400, nothing written', async () => {
    await seed('active'); const before = await snapshot();
    const r = await del(ID, {});
    expect(r.code).toBe(400);
    expect(await status()).toBe('active'); expect(await audit()).toEqual([]); expect(await snapshot()).toEqual(before);
  });
  it('gate71 E2 unknown id -> 404, nothing written', async () => {
    await seed('active'); const before = await snapshot();
    const r = await del(UNKNOWN);
    expect(r.code).toBe(404);
    expect(await audit()).toEqual([]); expect(await snapshot()).toEqual(before);
    expect((await c.query('SELECT count(*) AS n FROM platform_audit_log WHERE target_id = $1', [UNKNOWN])).rows[0].n).toBe('0');
  });
  it('gate71 E3 malformed id -> 400 at the param guard, nothing written', async () => {
    await seed('active'); const before = await snapshot();
    const r = await del('not-a-uuid');
    expect(r.code).toBe(400);
    expect(await snapshot()).toEqual(before);
  });
  it('gate71 E4 the UPDATE fails (trigger) -> constant 500, status unchanged, tenant_archive_failed written', async () => {
    await seed('active'); await c.query(`INSERT INTO gate_fault VALUES ('update_tenants')`); const before = await snapshot();
    const r = await del();
    expect(r.code).toBe(500); expect(r.body).toEqual(CONSTANT_500);
    expect(await status()).toBe('active');
    expect(await audit()).toEqual([{ action: 'tenant_archive_failed', details: { erased: false } }]);
    expect(await snapshot()).toEqual(before);
  });
  it('gate71 E5 the tenant_archived INSERT fails (trigger) -> rolled back on real PG, constant 500, failure audited', async () => {
    await seed('suspended'); await c.query(`INSERT INTO gate_fault VALUES ('audit:tenant_archived')`); const before = await snapshot();
    const r = await del();
    expect(r.code).toBe(500); expect(r.body).toEqual(CONSTANT_500);
    expect(await status()).toBe('suspended');
    expect(await audit()).toEqual([{ action: 'tenant_archive_failed', details: { erased: false } }]);
    expect(await snapshot()).toEqual(before);
  });
  it('gate71 E6 both audit INSERTs fail -> constant 500, status unchanged, no audit row, nothing else written', async () => {
    await seed('active');
    await c.query(`INSERT INTO gate_fault VALUES ('audit:tenant_archived'), ('audit:tenant_archive_failed')`); const before = await snapshot();
    const r = await del();
    expect(r.code).toBe(500); expect(r.body).toEqual(CONSTANT_500);
    expect(await status()).toBe('active'); expect(await audit()).toEqual([]); expect(await snapshot()).toEqual(before);
  });
  it('gate71 E8 COMMIT itself fails (deferred trigger): status unchanged, NO tenant_archived row survives, failure audited', async () => {
    await seed('active'); await c.query(`INSERT INTO gate_fault VALUES ('commit_tenants')`); const before = await snapshot();
    const r = await del();
    expect(r.code).toBe(500); expect(r.body).toEqual(CONSTANT_500);
    expect(await status()).toBe('active');
    expect(await audit()).toEqual([{ action: 'tenant_archive_failed', details: { erased: false } }]);
    expect(await snapshot()).toEqual(before);
  });
  it('gate71 E7 the platform pool is not leaked: 12 failing Deletes in a row (pool max 5), then a good one still answers', async () => {
    await seed('active'); await c.query(`INSERT INTO gate_fault VALUES ('audit:tenant_archived')`);
    for (let i = 0; i < 12; i += 1) expect((await del()).code).toBe(500);
    await c.query('DELETE FROM gate_fault');
    const r = await del();
    expect(r.code).toBe(200);
    expect(await status()).toBe('archived');
  }, 30_000);
});

describe('gate71 Q3 reversal through the API (real PG)', () => {
  it('gate71 V1 active -Delete-> archived -> suspended -> active; every row kept; tenant archivable again', async () => {
    await seed('active'); const before = await snapshot();
    expect((await del()).code).toBe(200);
    expect((await patch('active')).code).toBe(409); // archived -> active stays refused (KS-1860)
    expect((await patch('suspended')).code).toBe(200);
    expect((await patch('active')).code).toBe(200);
    expect(await status()).toBe('active');
    expect(await snapshot()).toEqual(before);
    expect((await call('GET', `/api/tenants/${ID}`)).code).toBe(200);
    expect(await audit()).toEqual([
      { action: 'tenant_archived', details: { slug: SLUG, previousStatus: 'active', erased: false } },
      { action: 'tenant_status_changed', details: { status: 'suspended' } },
      { action: 'tenant_status_changed', details: { status: 'active' } },
    ]);
    expect((await del()).code).toBe(200); // the cycle can repeat
    expect(await status()).toBe('archived');
  });
});

async function lockWaiters(): Promise<number> {
  const r = await c.query(`SELECT count(*) AS n FROM pg_stat_activity WHERE datname = current_database() AND wait_event_type = 'Lock'`);
  return Number(r.rows[0].n);
}
async function untilWaiters(n: number): Promise<void> {
  for (let i = 0; i < 300; i += 1) { if ((await lockWaiters()) >= n) return; await new Promise((r) => setTimeout(r, 20)); }
  throw new Error(`never saw ${n} lock waiters`);
}

describe('gate71 Q4 concurrency on real row locks', () => {
  it('gate71 C1 two Deletes at once: exactly one 200, one 409, one tenant_archived row', async () => {
    await seed('active');
    const holder = new pg.Client({ connectionString: URL_ }); await holder.connect();
    await holder.query('BEGIN'); await holder.query('SELECT 1 FROM tenants WHERE id = $1 FOR UPDATE', [ID]);
    const p = Promise.all([del(), del()]);
    await untilWaiters(2);
    await holder.query('COMMIT'); await holder.end();
    const codes = (await p).map((x) => x.code).sort();
    expect(codes).toEqual([200, 409]);
    expect(await status()).toBe('archived');
    expect((await audit()).map((a) => a.action)).toEqual(['tenant_archived']);
  });
  it('gate71 C2 Delete reads active, a concurrent suspend commits first: Delete 409, final suspended, no tenant_archived', async () => {
    await seed('active');
    const holder = new pg.Client({ connectionString: URL_ }); await holder.connect();
    await holder.query('BEGIN'); await holder.query(`UPDATE tenants SET status = 'suspended' WHERE id = $1`, [ID]);
    const p = del();
    await untilWaiters(1);
    await holder.query('COMMIT'); await holder.end();
    const r = await p;
    expect(r.code).toBe(409);
    expect(r.body.error.message).toBe('Tenant status changed while archiving; nothing was changed');
    expect(await status()).toBe('suspended');
    expect(await audit()).toEqual([]);
  });
  it('gate71 C3 Delete vs status route reactivation from suspended, both blocked then released: one wins, state consistent', async () => {
    await seed('suspended');
    const holder = new pg.Client({ connectionString: URL_ }); await holder.connect();
    await holder.query('BEGIN'); await holder.query('SELECT 1 FROM tenants WHERE id = $1 FOR UPDATE', [ID]);
    const p = Promise.all([del(), patch('active')]);
    await untilWaiters(2);
    await holder.query('ROLLBACK'); await holder.end();
    const [d, s] = await p;
    const final = await status();
    const actions = (await audit()).map((a) => a.action);
    expect([d.code, s.code].sort()).toEqual([200, 409]);
    if (d.code === 200) { expect(final).toBe('archived'); expect(actions).toEqual(['tenant_archived']); }
    else { expect(final).toBe('active'); expect(actions).toEqual(['tenant_status_changed']); }
  });
});

describe('gate71 S status route audit atomicity (unchanged code; measured)', () => {
  it('gate71 S1 archived -> suspended with the tenant_status_changed INSERT failing: answer vs committed state', async () => {
    await seed('archived'); await c.query(`INSERT INTO gate_fault VALUES ('audit:tenant_status_changed')`);
    const r = await patch('suspended');
    // Recorded, not asserted as a ruling: what the client is told and what the database holds afterwards.
    const fs = await import('node:fs');
    fs.writeFileSync(process.env.GATE71_S1_OUT || '/dev/null', JSON.stringify({ code: r.code, body: r.body, status: await status(), audit: await audit() }) + '\n');
    expect(r.code).toBe(500);
  });
});
