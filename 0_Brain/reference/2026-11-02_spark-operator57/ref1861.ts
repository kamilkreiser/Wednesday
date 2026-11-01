/**
 * KS-1861 — DELETE /api/tenants/:id deleted the tenant's registry rows from the platform database (each delete in an
 * empty catch), ran DROP DATABASE on a per-tenant database name whatever PROVISION_PER_TENANT_DB said, and answered
 * { success: true, deleted: true } while the tenant's data stayed in the application database. Kam's ruling
 * (2026-10-31 11:33:19 AEDT, card secuura-ks1861-what-tenant-delete-means-1031, a: "Archive, not erase") makes DELETE
 * set the status to archived and keep every row. No database is dropped under any flag value (Wednesday, 12:47:44Z), the
 * answer says what happened, and the audit row records the outcome. The status change and its audit row commit together.
 *
 * The service entry module is imported for real, with `pg` replaced by a fake platform database and the JWT middleware by
 * a pass-through (as in the KS 1544 file). The fake models develop's statements (the four registry deletes, the tenant
 * delete, DROP DATABASE on an admin pool) as well as the archive transaction, so develop's behaviour is measured rather
 * than assumed. BEGIN, COMMIT and ROLLBACK work on a snapshot. Any other statement that names the tenants table throws.
 */
import { describe, it, expect, beforeAll, beforeEach, afterEach, vi } from 'vitest';
import net from 'node:net';
import type { AddressInfo } from 'node:net';

type State = {
  tenants: Map<string, { slug: string; status: string }>;
  related: Map<string, Set<string>>; // table -> tenant ids that still have rows there
  audit: Array<{ action: string; targetId: unknown; details: unknown }>;
};

const db = vi.hoisted(() => ({
  state: null as unknown as State,
  statements: [] as string[],
  adminPools: 0,
  dropped: [] as string[],
  failAudit: '' as string,
  failUpdate: false,
  raceTo: '' as string,
}));

vi.mock('pg', () => {
  const RELATED = ['vault_entries', 'tenant_contacts', 'tenant_config', 'platform_document_registry'];
  const clone = (s: State): State => ({
    tenants: new Map([...s.tenants].map(([k, v]) => [k, { ...v }])),
    related: new Map([...s.related].map(([k, v]) => [k, new Set(v)])),
    audit: s.audit.map((a) => ({ ...a })),
  });
  function run(text: string, params: unknown[] | undefined, tx: { snap: State | null }) {
    const sql = text.replace(/\s+/g, ' ').trim();
    db.statements.push(sql);
    const p = (params ?? []) as unknown[];
    if (sql === 'SELECT 1') return { rows: [], rowCount: 0 };
    if (sql === 'BEGIN') { tx.snap = clone(db.state); return { rows: [], rowCount: 0 }; }
    if (sql === 'COMMIT') { tx.snap = null; return { rows: [], rowCount: 0 }; }
    if (sql === 'ROLLBACK') { if (tx.snap) db.state = tx.snap; tx.snap = null; return { rows: [], rowCount: 0 }; }
    let m = /^SELECT slug(, status)? FROM tenants WHERE id = \$1$/.exec(sql);
    if (m) {
      const t = db.state.tenants.get(p[0] as string);
      const out = t ? { rows: [m[1] ? { slug: t.slug, status: t.status } : { slug: t.slug }], rowCount: 1 } : { rows: [], rowCount: 0 };
      if (t && db.raceTo) { t.status = db.raceTo; db.raceTo = ''; }
      return out;
    }
    m = /^DELETE FROM (\w+) WHERE tenant_id = \$1$/.exec(sql);
    if (m && RELATED.includes(m[1])) {
      const set = db.state.related.get(m[1])!;
      const had = set.delete(p[0] as string);
      return { rows: [], rowCount: had ? 1 : 0 };
    }
    if (sql === 'DELETE FROM tenants WHERE id = $1') {
      const had = db.state.tenants.delete(p[0] as string);
      return { rows: [], rowCount: had ? 1 : 0 };
    }
    m = /^DROP DATABASE IF EXISTS "([a-z0-9_]+)"$/.exec(sql);
    if (m) { db.dropped.push(m[1]); return { rows: [], rowCount: 0 }; }
    // The conditional update, and the unconditional shape too, so a dropped condition is measured, not thrown on.
    m = /^UPDATE tenants SET status = 'archived', updated_at = now\(\) WHERE id = \$1( AND status = \$2)?$/.exec(sql);
    if (m) {
      if (db.failUpdate) throw new Error('connect ECONNREFUSED 10.0.0.5:5432');
      const t = db.state.tenants.get(p[0] as string);
      if (!t || (m[1] && t.status !== p[1])) return { rows: [], rowCount: 0 };
      t.status = 'archived';
      return { rows: [], rowCount: 1 };
    }
    m = /^INSERT INTO platform_audit_log \(action, target_type, target_id, details\) VALUES \('(\w+)', 'tenant', \$1, \$2\)$/.exec(sql);
    if (m) {
      if (db.failAudit === m[1]) throw new Error('audit insert failed: disk full on 10.0.0.5');
      db.state.audit.push({ action: m[1], targetId: p[0], details: JSON.parse(String(p[1])) });
      return { rows: [], rowCount: 1 };
    }
    if (/\btenants\b|platform_audit_log|DROP/.test(sql)) throw new Error('fake pg: unmodelled statement: ' + sql);
    return { rows: [], rowCount: 0 };
  }
  class Pool {
    constructor(opts: { database?: string } = {}) { if (opts.database === 'postgres') db.adminPools += 1; }
    async query(text: string, params?: unknown[]) { return run(text, params, { snap: null }); }
    async connect() {
      const tx = { snap: null as State | null };
      return { query: async (text: string, params?: unknown[]) => run(text, params, tx), release: () => undefined };
    }
    on() { return this; }
    async end() { return undefined; }
  }
  return { default: { Pool }, Pool };
});
vi.mock('@secuura/shared', async (importOriginal) => {
  const real = (await importOriginal()) as Record<string, unknown>;
  return { ...real, authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next() };
});

const ID = 'd1861000-0000-4000-8000-000000000001';
const UNKNOWN = 'd1861000-0000-4000-8000-0000000000ff';
const RELATED = ['vault_entries', 'tenant_contacts', 'tenant_config', 'platform_document_registry'];
const ARCHIVED_ANSWER = {
  success: true,
  deleted: false,
  archived: true,
  status: 'archived',
  message: 'Tenant archived. No data was removed: every row is kept and no database is dropped.',
};
const CONSTANT_500 = { success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } };
let base = '';
const savedFlag = process.env.PROVISION_PER_TENANT_DB;

async function freePort(): Promise<number> {
  const s = net.createServer();
  await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
  const port = (s.address() as AddressInfo).port;
  await new Promise<void>((r) => s.close(() => r()));
  return port;
}

// The first import of the entry module transpiles it cold; on a loaded host that has run past vitest's 10 s hook
// default and skipped every cell (measured on the KS-1860 file: load1 8.8). The import is the hook's only slow part.
beforeAll(async () => {
  db.state = { tenants: new Map(), related: new Map(), audit: [] };
  const port = await freePort();
  process.env.PORT = String(port);
  process.env.PLATFORM_DATABASE_URL = 'postgres://platform:pw@127.0.0.1:5432/platform';
  process.env.DATABASE_URL = 'postgres://app:pw@127.0.0.1:5432/app';
  await import('../index.js');
  base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i += 1) {
    try { await fetch(base + '/health'); break; } catch { await new Promise((r) => setTimeout(r, 30)); }
  }
}, 30_000);

/** One tenant with rows in every related table, and clean counters. */
function seed(status: string): void {
  db.state = {
    tenants: new Map([[ID, { slug: 'acme-co', status }]]),
    related: new Map(RELATED.map((t) => [t, new Set([ID])])),
    audit: [],
  };
  db.statements.length = 0;
  db.adminPools = 0;
  db.dropped.length = 0;
  db.failAudit = '';
  db.failUpdate = false;
  db.raceTo = '';
}

beforeEach(() => seed('active'));
afterEach(() => {
  if (savedFlag === undefined) delete process.env.PROVISION_PER_TENANT_DB;
  else process.env.PROVISION_PER_TENANT_DB = savedFlag;
});

async function del(id: string, body: unknown = { confirm: true }): Promise<{ code: number; body: any }> {
  const r = await fetch(`${base}/api/tenants/${id}`, {
    method: 'DELETE',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  return { code: r.status, body: await r.json().catch(() => ({})) };
}

/** Every related row and the tenant row are still there, and no DELETE statement ran. */
function everyRowKept(): void {
  expect(db.state.tenants.has(ID)).toBe(true);
  for (const t of RELATED) expect(db.state.related.get(t)!.has(ID)).toBe(true);
  expect(db.statements.filter((s) => s.startsWith('DELETE'))).toEqual([]);
}

describe('KS-1861 DELETE /api/tenants/:id archives the tenant and keeps every row', () => {
  it.each([
    ['A1', 'active'],
    ['A2', 'suspended'],
    ['A3', 'provisioning'],
  ])('RED KS-1861 %s: a %s tenant is archived, every row is kept and the answer says so', async (_id, from) => {
    seed(from);
    const r = await del(ID);
    expect(r.code).toBe(200);
    expect(r.body).toEqual(ARCHIVED_ANSWER);
    expect(db.state.tenants.get(ID)!.status).toBe('archived');
    everyRowKept();
    expect(db.state.audit).toEqual([{ action: 'tenant_archived', targetId: ID, details: { slug: 'acme-co', previousStatus: from, erased: false } }]);
  });

  it('RED KS-1861 X1: an already-archived tenant answers 409, with no change and no audit row', async () => {
    seed('archived');
    const r = await del(ID);
    expect(r.code).toBe(409);
    expect(r.body).toEqual({ success: false, error: { code: 'CONFLICT', message: 'Tenant is already archived' } });
    everyRowKept();
    expect(db.state.audit).toEqual([]);
  });

  it.each([
    ['F1', 'true'],
    ['F2', undefined],
  ])('RED KS-1861 %s: with PROVISION_PER_TENANT_DB=%s no admin pool is opened and no DROP DATABASE runs', async (_id, flag) => {
    if (flag === undefined) delete process.env.PROVISION_PER_TENANT_DB;
    else process.env.PROVISION_PER_TENANT_DB = flag;
    const r = await del(ID);
    expect(r.code).toBe(200);
    expect(db.adminPools).toBe(0);
    expect(db.dropped).toEqual([]);
    expect(db.statements.filter((s) => /DROP/i.test(s))).toEqual([]);
  });

  it('RED KS-1861 T1: when the audit row cannot be written, the archive is rolled back and the answer is the constant 500', async () => {
    db.failAudit = 'tenant_archived';
    const r = await del(ID);
    expect(r.code).toBe(500);
    expect(r.body).toEqual(CONSTANT_500);
    expect(db.state.tenants.get(ID)!.status).toBe('active');
    everyRowKept();
    expect(db.state.audit).toEqual([{ action: 'tenant_archive_failed', targetId: ID, details: { erased: false } }]);
  });

  it('RED KS-1861 T2: when the status update fails, the answer is the constant 500 and the failure is audited', async () => {
    db.failUpdate = true;
    const r = await del(ID);
    expect(r.code).toBe(500);
    expect(r.body).toEqual(CONSTANT_500);
    expect(db.state.tenants.get(ID)!.status).toBe('active');
    everyRowKept();
    expect(db.state.audit).toEqual([{ action: 'tenant_archive_failed', targetId: ID, details: { erased: false } }]);
  });

  it('RED KS-1861 T3: a status that changes between the read and the update answers 409 and changes nothing', async () => {
    db.raceTo = 'suspended';
    const r = await del(ID);
    expect(r.code).toBe(409);
    expect(r.body).toEqual({ success: false, error: { code: 'CONFLICT', message: 'Tenant status changed while archiving; nothing was changed' } });
    expect(db.state.tenants.get(ID)!.status).toBe('suspended');
    everyRowKept();
    expect(db.state.audit).toEqual([]);
  });

  it('CONTROL KS-1861 N1: a well-formed id with no tenant still answers 404 and touches nothing', async () => {
    const r = await del(UNKNOWN);
    expect(r.code).toBe(404);
    expect(r.body).toEqual({ success: false, error: { code: 'NOT_FOUND', message: 'Tenant not found' } });
    everyRowKept();
    expect(db.state.audit).toEqual([]);
  });

  it('CONTROL KS-1861 K1: without "confirm": true the answer is still 400 and nothing is touched', async () => {
    const r = await del(ID, {});
    expect(r.code).toBe(400);
    expect(r.body).toEqual({ success: false, error: { code: 'BAD_REQUEST', message: 'Set "confirm": true in the request body to delete' } });
    expect(db.state.tenants.get(ID)!.status).toBe('active');
    everyRowKept();
    expect(db.state.audit).toEqual([]);
  });

  it('CONTROL KS-1861 K2: a malformed id still answers 400 at the KS 497 param guard', async () => {
    const r = await del('not-a-uuid');
    expect(r.code).toBe(400);
    expect(r.body.error.code).toBe('VALIDATION_ERROR');
  });
});
