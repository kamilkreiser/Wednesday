/**
 * Gate 64 tenant-provisioning probe (KS-1860 #1876): statement-level evidence the PR file does not assert.
 * Same harness shape as the PR file (real entry module, pg fake, pass-through authenticate) but the fake LOGS every
 * statement, so each cell can assert exactly which statements ran: on a refusal one guarded UPDATE + one SELECT and no
 * INSERT; on an allowed move one guarded UPDATE + one INSERT and no SELECT.
 */
import { describe, it, expect, beforeAll, beforeEach, vi } from 'vitest';
import net from 'node:net';
import type { AddressInfo } from 'node:net';

const db = vi.hoisted(() => ({
  tenants: new Map<string, string>(),
  log: [] as Array<{ sql: string; params: unknown[] | undefined }>,
}));

vi.mock('pg', () => {
  const PLAIN = 'UPDATE tenants SET status = $1, updated_at = now() WHERE id = $2';
  const GUARDED = 'UPDATE tenants SET status = $1, updated_at = now() WHERE id = $2 AND status = ANY($3::text[])';
  const READ = 'SELECT status FROM tenants WHERE id = $1';
  class Pool {
    async query(text: string, params?: unknown[]) {
      const sql = text.replace(/\s+/g, ' ').trim();
      if (/tenants|platform_audit_log/.test(sql)) db.log.push({ sql, params });
      if (sql === PLAIN || sql === GUARDED) {
        const [status, id, from] = params as [string, string, string[] | undefined];
        const cur = db.tenants.get(id);
        const ok = sql === PLAIN || (Array.isArray(from) && cur !== undefined && from.includes(cur));
        if (cur === undefined || !ok) return { rows: [], rowCount: 0 };
        db.tenants.set(id, status);
        return { rows: [], rowCount: 1 };
      }
      if (sql === READ) {
        const cur = db.tenants.get((params as [string])[0]);
        return cur === undefined ? { rows: [], rowCount: 0 } : { rows: [{ status: cur }], rowCount: 1 };
      }
      if (/INSERT INTO platform_audit_log/.test(sql)) return { rows: [], rowCount: 1 };
      if (/\btenants\b/.test(sql)) throw new Error('fake pg: unmodelled tenants statement: ' + sql);
      return { rows: [], rowCount: 0 };
    }
    async connect() { return { query: async () => ({ rows: [] }), release: () => undefined }; }
    on() { return this; }
    async end() { return undefined; }
  }
  return { default: { Pool }, Pool };
});
vi.mock('@secuura/shared', async (importOriginal) => {
  const real = (await importOriginal()) as Record<string, unknown>;
  return { ...real, authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next() };
});

const ID = 'c6400000-0000-4000-8000-000000000001';
const UNKNOWN = 'c6400000-0000-4000-8000-0000000000ff';
let base = '';
async function freePort(): Promise<number> {
  const s = net.createServer();
  await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
  const port = (s.address() as AddressInfo).port;
  await new Promise<void>((r) => s.close(() => r()));
  return port;
}
beforeAll(async () => {
  const port = await freePort();
  process.env.PORT = String(port);
  process.env.PLATFORM_DATABASE_URL = 'postgres://platform:pw@127.0.0.1:5432/platform';
  process.env.DATABASE_URL = 'postgres://app:pw@127.0.0.1:5432/app';
  await import('../index.js');
  base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i += 1) {
    try { await fetch(base + '/health'); break; } catch { await new Promise((r) => setTimeout(r, 30)); }
  }
}, 60_000);
beforeEach(() => { db.tenants.clear(); db.log.length = 0; });
async function patch(id: string, status: unknown) {
  const r = await fetch(`${base}/api/tenants/${id}/status`, { method: 'PATCH', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ status }) });
  return { code: r.status, body: await r.json().catch(() => ({})) };
}
const kinds = () => db.log.map((l) => (l.sql.startsWith('UPDATE') ? (l.sql.includes('ANY($3') ? 'UPDATE_GUARDED' : 'UPDATE_PLAIN') : l.sql.startsWith('SELECT') ? 'SELECT' : l.sql.startsWith('INSERT') ? 'INSERT' : 'OTHER'));

const STATUSES = ['provisioning', 'active', 'suspended', 'archived'];
const TARGETS = ['active', 'suspended', 'archived'];
const ALLOWED = new Set(['provisioning>active', 'active>suspended', 'suspended>active', 'suspended>archived']);

describe('gate64 TP: the full 4x3 matrix with statement-level assertions', () => {
  const cells = STATUSES.flatMap((f) => TARGETS.map((t) => [f, t] as const));
  it.each(cells)('TP %s -> %s', async (from, to) => {
    db.tenants.set(ID, from);
    const r = await patch(ID, to);
    if (ALLOWED.has(`${from}>${to}`)) {
      expect(r.code).toBe(200);
      expect(kinds()).toEqual(['UPDATE_GUARDED', 'INSERT']);
      expect(db.tenants.get(ID)).toBe(to);
    } else {
      expect(r.code).toBe(409);
      expect(r.body).toEqual({ success: false, error: { code: 'CONFLICT', message: `Cannot change tenant status from ${from} to ${to}` } });
      expect(kinds()).toEqual(['UPDATE_GUARDED', 'SELECT']);
      expect(db.tenants.get(ID)).toBe(from);
    }
    // the guarded UPDATE carried exactly the from-list for this target
    const from3 = db.log[0].params![2];
    expect(from3).toEqual({ active: ['provisioning', 'suspended'], suspended: ['active'], archived: ['suspended'] }[to]);
  });

  it('TP-U unknown id: 404, one guarded UPDATE + one SELECT, no INSERT', async () => {
    const r = await patch(UNKNOWN, 'suspended');
    expect(r.code).toBe(404);
    expect(kinds()).toEqual(['UPDATE_GUARDED', 'SELECT']);
  });

  it.each([['provisioning'], [['active']], [null], [''], ['Active'], ['__proto__'], ['constructor']])(
    'TP-V target %j answers 400 and runs no statement', async (to) => {
      db.tenants.set(ID, 'active');
      const r = await patch(ID, to);
      expect(r.code).toBe(400);
      expect(db.log).toHaveLength(0);
    });

  it('TP-C concurrent: active -> suspended and active -> archived fired together; archived is never reached from active', async () => {
    db.tenants.set(ID, 'active');
    const [a, b] = await Promise.all([patch(ID, 'suspended'), patch(ID, 'archived')]);
    expect(a.code).toBe(200);
    // either order is legal: archived first -> 409 (from active); suspended first -> archived is then allowed (200)
    expect([200, 409]).toContain(b.code);
    if (b.code === 200) expect(db.tenants.get(ID)).toBe('archived'); else expect(db.tenants.get(ID)).toBe('suspended');
  });
});
