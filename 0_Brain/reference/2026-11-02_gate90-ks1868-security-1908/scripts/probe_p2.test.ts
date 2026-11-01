// QA GATE 90 probe P2 (not part of the PR). Copied into the gate clone's src/__tests__ for the run only, then moved out.
// Drives the REAL route POST /api/keys {rotate:true, connectorId} through the REAL db.ts (transaction(), query(),
// initDb()) and the real @secuura/shared queryWithTenantGuc; only the `pg` driver is replaced by a recording Pool whose
// client models BEGIN / SAVEPOINT / ROLLBACK TO SAVEPOINT / RELEASE / COMMIT / ROLLBACK over a one-table store
// (svc_api_keys). The retire UPDATE (or the INSERT) rejects with an ordinary Error or an unreadable value.
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import { appendFileSync } from 'fs';

process.env.SECURITY_DISABLE_BOOT = '1';
process.env.DATABASE_URL = 'postgres://gate90:stub@127.0.0.1:1/gate90';
delete process.env.API_KEY_ROTATION_GRACE_SECONDS;

const OUT = process.env.PROBE_OUT as string;
const TENANT = 'c0000000-0000-4000-8000-000000009090';
const ORG = '90909090-9090-4090-8090-909090909090';
const CONNECTOR = 'gate90-connector';
const PRIOR = 'key_gate90_prior';

const h = vi.hoisted(() => ({
  mode: 'none' as string,             // none | retireFails | insertFails
  toThrow: undefined as unknown,
  table: new Map<string, { active: boolean; connector: string | null }>(),
  sql: [] as string[],
}));

vi.mock('pg', () => {
  type W = { kind: 'insert' | 'retire' | 'mark'; id?: string; connector?: string | null };
  const norm = (s: string) => String(s).replace(/\s+/g, ' ').trim();
  const label = (s: string) => {
    const n = norm(s);
    if (/^INSERT INTO svc_api_keys/i.test(n)) return 'INSERT svc_api_keys';
    if (/^UPDATE svc_api_keys/i.test(n)) return 'UPDATE svc_api_keys (retire)';
    if (/set_config/i.test(n)) return 'set_config(tenant GUC)';
    if (/pg_advisory_xact_lock/i.test(n)) return 'advisory_xact_lock';
    return n.slice(0, 60);
  };
  function exec(s: string, values: unknown[] | undefined, pending: W[] | null): Promise<any> {
    const n = norm(s);
    h.sql.push(label(s));
    const apply = (w: W) => {
      if (w.kind === 'insert') h.table.set(w.id!, { active: true, connector: w.connector ?? null });
      if (w.kind === 'retire') { const r = h.table.get(w.id!); if (r) r.active = false; }
    };
    if (/^SELECT 1 AS ok/i.test(n)) return Promise.resolve({ rows: [{ ok: 1 }], rowCount: 1 });
    if (/^INSERT INTO svc_api_keys/i.test(n)) {
      if (h.mode === 'insertFails') return Promise.reject(h.toThrow);
      const w: W = { kind: 'insert', id: String(values?.[0]), connector: (values?.[14] as string) ?? null };
      if (pending) pending.push(w); else apply(w);
      return Promise.resolve({ rows: [], rowCount: 1 });
    }
    if (/^UPDATE svc_api_keys/i.test(n) && /connector_id = \$1/.test(n)) {
      if (h.mode === 'retireFails') return Promise.reject(h.toThrow);
      const [conn, , keep] = values as string[];
      const ids = [...h.table.entries()].filter(([id, r]) => r.active && r.connector === conn && id !== keep).map(([id]) => id);
      for (const id of ids) { const w: W = { kind: 'retire', id }; if (pending) pending.push(w); else apply(w); }
      return Promise.resolve({ rows: ids.map((id) => ({ id })), rowCount: ids.length });
    }
    return Promise.resolve({ rows: [], rowCount: 0 });
  }
  class Client {
    pending: W[] | null = null;
    query(text: string, values?: unknown[]) {
      const n = norm(text);
      if (n === 'BEGIN') { h.sql.push('BEGIN'); this.pending = []; return Promise.resolve({ rows: [] }); }
      if (n === 'COMMIT') {
        h.sql.push('COMMIT');
        for (const w of this.pending ?? []) {
          if (w.kind === 'insert') h.table.set(w.id!, { active: true, connector: w.connector ?? null });
          if (w.kind === 'retire') { const r = h.table.get(w.id!); if (r) r.active = false; }
        }
        this.pending = null; return Promise.resolve({ rows: [] });
      }
      if (n === 'ROLLBACK') { h.sql.push('ROLLBACK'); this.pending = null; return Promise.resolve({ rows: [] }); }
      if (/^SAVEPOINT /i.test(n)) { h.sql.push(n); this.pending?.push({ kind: 'mark' }); return Promise.resolve({ rows: [] }); }
      if (/^ROLLBACK TO SAVEPOINT /i.test(n)) {
        h.sql.push(n);
        if (this.pending) { const i = this.pending.map((w) => w.kind).lastIndexOf('mark'); this.pending.splice(i + 1); }
        return Promise.resolve({ rows: [] });
      }
      if (/^RELEASE SAVEPOINT /i.test(n)) { h.sql.push(n); return Promise.resolve({ rows: [] }); }
      return exec(text, values, this.pending);
    }
    release() { h.sql.push('release'); }
  }
  class Pool {
    constructor(_o?: unknown) {}
    on() { return this; }
    connect() { return Promise.resolve(new Client()); }
    query(text: string, values?: unknown[]) { return exec(text, values, null); }
    end() { return Promise.resolve(); }
  }
  return { Pool, default: { Pool } };
});

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64url = (b: Buffer) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function token(claims: Record<string, unknown>): string {
  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const payload = b64url(Buffer.from(JSON.stringify({ sub: 'gate90', iat: now, exp: now + 300, ...claims })));
  const sig = b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM));
  return `${header}.${payload}.${sig}`;
}

const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('db down'),
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  throwingGetter: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
};

let server: Server; let base: string; let memApiKeys: Map<string, any>; let dbAvail: () => boolean;
const SAVED = process.listeners('unhandledRejection');
let unhandled = 0; const onUnhandled = () => { unhandled += 1; };
const consoleLines: string[] = [];

beforeAll(async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;
  const db = await import('../db');
  const ok = await db.initDb();
  dbAvail = db.isDbAvailable;
  const mod: any = await import('../index');
  memApiKeys = mod.memApiKeys;
  await new Promise<void>((r) => { server = mod.default.listen(0, '127.0.0.1', r); });
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
  appendFileSync(OUT, JSON.stringify({ positive_control: { initDb: ok, isDbAvailable: dbAvail() } }) + '\n');
});
afterAll(async () => {
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED) process.on('unhandledRejection', l as any);
  await new Promise<void>((r) => server.close(() => r()));
});

async function cell(name: string, mode: string, kind: string | null) {
  // seed: one prior ACTIVE key on the connector, committed and in memory
  h.table.clear(); h.sql.length = 0; memApiKeys.clear();
  h.table.set(PRIOR, { active: true, connector: CONNECTOR });
  memApiKeys.set(PRIOR, { id: PRIOR, organizationId: ORG, tenantId: TENANT, name: 'prior', keyHash: 'h-prior', keyPrefix: 'sk_prior',
    scopes: ['documents:read'], rateLimit: 100, rateLimitWindow: 60, usageCount: 0, isActive: true, createdAt: new Date(), connectorId: CONNECTOR });
  h.mode = mode; h.toThrow = kind ? KINDS[kind]() : undefined;
  unhandled = 0; consoleLines.length = 0;
  const spy = vi.spyOn(console, 'log').mockImplementation((...a: unknown[]) => { consoleLines.push(String(a[0])); });
  let status: number | string = 'none'; let body: any = null;
  try {
    const res = await fetch(`${base}/api/keys`, {
      method: 'POST', signal: AbortSignal.timeout(3000),
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token({ role: 'super_admin' })}` },
      body: JSON.stringify({ name: 'gate90', scopes: ['documents:read'], tenantId: TENANT, organizationId: ORG, connectorId: CONNECTOR, rotate: true }),
    });
    status = res.status; const t = await res.text(); try { body = JSON.parse(t); } catch { body = t.slice(0, 200); }
  } catch (e) { status = 'UNANSWERED(' + (e as Error).name + ')'; }
  await new Promise((r) => setTimeout(r, 50));
  spy.mockRestore();
  const rows = Object.fromEntries([...h.table.entries()].map(([id, r]) => [id === PRIOR ? 'prior' : id, r.active ? 'active' : 'retired']));
  const mem = Object.fromEntries([...memApiKeys.entries()].map(([id, k]) => [id === PRIOR ? 'prior' : id, k.isActive ? 'active' : 'inactive']));
  const pick = (re: RegExp) => consoleLines.filter((s) => re.test(s)).map((s) => { try { const j = JSON.parse(s); return { message: j.message, error: j.error, code: j.code, infra: j.infra }; } catch { return s.slice(0, 120); } });
  const rec = {
    cell: name, mode, kind, status,
    priorKeysRevoked: body?.data && 'priorKeysRevoked' in body.data ? body.data.priorKeysRevoked : '(absent)',
    keyIssued: typeof body?.data?.key === 'string' && body.data.key.length > 0,
    errorMessage: body?.error?.message ?? null,
    sql: h.sql.filter((s) => s !== 'release'),
    committedRows: rows, memApiKeys: mem,
    log_ks577: pick(/KS-577: revoke-on-rotate FAILED/), log_ks888: pick(/KS-888/), log_created: pick(/"API key created"/).length,
    unhandled,
  };
  appendFileSync(OUT, JSON.stringify(rec) + '\n');
}

describe('gate 90 probe P2: rotate route through the real transaction()', () => {
  it('control: retire succeeds', async () => { await cell('control', 'none', null); });
  for (const k of Object.keys(KINDS)) it(`retire UPDATE rejects: ${k}`, async () => { await cell(`retire/${k}`, 'retireFails', k); });
  for (const k of Object.keys(KINDS)) it(`INSERT rejects: ${k}`, async () => { await cell(`insert/${k}`, 'insertFails', k); });
});
