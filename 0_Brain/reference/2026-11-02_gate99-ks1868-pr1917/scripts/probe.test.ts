// QA GATE 99 probe (not part of the PR). Copied into the gate clone's src/__tests__ for the run only, then moved out.
// Imports the REAL tenant-provisioning entry module: real Express 4 (real listener on loopback), real @secuura/shared
// authenticate() verifying a real RS256 token, real zod. ONLY `pg` is replaced, by a recording in-memory platform DB
// (tenants, tenant_contacts, tenant_config, platform_audit_log) with snapshot BEGIN/COMMIT/ROLLBACK on pooled clients.
// One statement (matched by regex) rejects with the scenario's value. The key-service and security fetches go to a closed
// loopback port (ECONNREFUSED), the path an unreachable key service already takes.
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'node:crypto';
import net from 'node:net';
import type { AddressInfo } from 'node:net';
import { appendFileSync } from 'node:fs';
import { z } from 'zod';

const OUT = process.env.PROBE_OUT as string;
const ID = 'e9900000-0000-4000-8000-000000000099';

type St = { tenants: Map<string, { slug: string; status: string }>; contacts: Set<string>; config: Set<string>; audit: string[] };
const h = vi.hoisted(() => ({
  st: null as unknown as St,
  sql: [] as string[],
  fail: [] as Array<{ re: RegExp; make: () => unknown }>,
}));

vi.mock('pg', () => {
  const clone = (s: St): St => ({ tenants: new Map([...s.tenants].map(([k, v]) => [k, { ...v }])), contacts: new Set(s.contacts), config: new Set(s.config), audit: [...s.audit] });
  async function run(text: string, p: unknown[] = [], tx: { snap: St | null }) {
    const sql = String(text).replace(/\s+/g, ' ').trim();
    h.sql.push(sql.length > 90 ? sql.slice(0, 90) + '...' : sql);
    for (const f of h.fail) if (f.re.test(sql)) throw f.make();
    if (sql === 'SELECT 1') return { rows: [], rowCount: 0 };
    if (sql === 'BEGIN') { tx.snap = clone(h.st); return { rows: [], rowCount: 0 }; }
    if (sql === 'COMMIT') { tx.snap = null; return { rows: [], rowCount: 0 }; }
    if (sql === 'ROLLBACK') { if (tx.snap) h.st = tx.snap; tx.snap = null; return { rows: [], rowCount: 0 }; }
    if (/^SELECT id FROM tenants WHERE slug/.test(sql)) {
      const hit = [...h.st.tenants].filter(([, t]) => t.slug === p[0]);
      return { rows: hit.map(([id]) => ({ id })), rowCount: hit.length };
    }
    if (/^INSERT INTO tenants /.test(sql)) { h.st.tenants.set(ID, { slug: String(p[1]), status: 'provisioning' }); return { rows: [{ id: ID }], rowCount: 1 }; }
    if (/^INSERT INTO tenant_contacts/.test(sql)) { h.st.contacts.add(String(p[0])); return { rows: [], rowCount: 1 }; }
    if (/^INSERT INTO tenant_config/.test(sql)) { h.st.config.add(String(p[0])); return { rows: [], rowCount: 1 }; }
    if (/^UPDATE tenants SET status = 'active' WHERE id = \$1$/.test(sql)) { const t = h.st.tenants.get(String(p[0])); if (t) t.status = 'active'; return { rows: [], rowCount: t ? 1 : 0 }; }
    let m = /^INSERT INTO platform_audit_log \(action, target_type, target_id, details\) VALUES \('(\w+)'/.exec(sql);
    if (m) { h.st.audit.push(m[1]); return { rows: [], rowCount: 1 }; }
    if (sql === 'DELETE FROM tenant_config WHERE tenant_id = $1') { const had = h.st.config.delete(String(p[0])); return { rows: [], rowCount: had ? 1 : 0 }; }
    if (sql === 'DELETE FROM tenant_contacts WHERE tenant_id = $1') { const had = h.st.contacts.delete(String(p[0])); return { rows: [], rowCount: had ? 1 : 0 }; }
    if (sql === 'DELETE FROM tenants WHERE id = $1') { const had = h.st.tenants.delete(String(p[0])); return { rows: [], rowCount: had ? 1 : 0 }; }
    if (/^SELECT slug, status FROM tenants WHERE id = \$1$/.test(sql)) { const t = h.st.tenants.get(String(p[0])); return t ? { rows: [{ ...t }], rowCount: 1 } : { rows: [], rowCount: 0 }; }
    m = /^UPDATE tenants SET status = 'archived', updated_at = now\(\) WHERE id = \$1 AND status = \$2$/.exec(sql);
    if (m) { const t = h.st.tenants.get(String(p[0])); if (!t || t.status !== p[1]) return { rows: [], rowCount: 0 }; t.status = 'archived'; return { rows: [], rowCount: 1 }; }
    if (/^UPDATE tenants SET status = \$1, updated_at = now\(\) WHERE id = \$2 AND status = ANY/.test(sql)) {
      const t = h.st.tenants.get(String(p[1])); if (!t || !(p[2] as string[]).includes(t.status)) return { rows: [], rowCount: 0 }; t.status = String(p[0]); return { rows: [], rowCount: 1 };
    }
    if (/^SELECT status FROM tenants WHERE id/.test(sql)) { const t = h.st.tenants.get(String(p[0])); return t ? { rows: [{ status: t.status }], rowCount: 1 } : { rows: [], rowCount: 0 }; }
    if (/^UPDATE tenants SET /.test(sql)) return { rows: [], rowCount: 1 };
    if (/^SELECT t\.\*/.test(sql)) { const rows = [...h.st.tenants].map(([id, t]) => ({ id, ...t })); return { rows, rowCount: rows.length }; }
    if (/^SELECT \* FROM tenant_contacts/.test(sql)) return { rows: [], rowCount: 0 };
    if (/^SELECT \* FROM platform_audit_log/.test(sql)) return { rows: h.st.audit.map((a) => ({ action: a })), rowCount: h.st.audit.length };
    if (/^SELECT COUNT\(\*\) as total FROM platform_audit_log/.test(sql)) return { rows: [{ total: String(h.st.audit.length) }], rowCount: 1 };
    throw new Error('gate99 fake pg: unmodelled statement: ' + sql);
  }
  class Pool {
    constructor(_o?: unknown) {}
    query(text: string, params?: unknown[]) { return run(text, params, { snap: null }); }
    async connect() { const tx = { snap: null as St | null }; return { query: (t: string, p?: unknown[]) => run(t, p, tx), release: () => undefined }; }
    on() { return this; }
    async end() { return undefined; }
  }
  return { default: { Pool }, Pool };
});

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64url = (b: Buffer) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function token(): string {
  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const payload = b64url(Buffer.from(JSON.stringify({ sub: 'gate99', role: 'super_admin', iat: now, exp: now + 600 })));
  const sig = b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM));
  return `${header}.${payload}.${sig}`;
}

const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('db down'),
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  throwingGetter: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  zod: () => new z.ZodError([{ code: 'custom', path: ['injected'], message: 'injected zod issue' }]),
  plainString: () => 'plain string thrown',
  throwingToString: () => ({ toString() { throw new Error('toString boom'); } }),
  stackGetterThrows: () => { const e = new Error('stack boom'); Object.defineProperty(e, 'stack', { get() { throw new Error('stack getter boom'); } }); return e; },
};

let base = '';
const SAVED = process.listeners('unhandledRejection');
let unhandled = 0; const onUnhandled = () => { unhandled += 1; };
const errLines: string[] = [];

async function freePort(): Promise<number> {
  const s = net.createServer(); await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
  const port = (s.address() as AddressInfo).port; await new Promise<void>((r) => s.close(() => r())); return port;
}

beforeAll(async () => {
  h.st = { tenants: new Map(), contacts: new Set(), config: new Set(), audit: [] };
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;
  const port = await freePort();
  process.env.PORT = String(port);
  process.env.PLATFORM_DATABASE_URL = 'postgres://platform:pw@127.0.0.1:5432/platform';
  process.env.DATABASE_URL = 'postgres://app:pw@127.0.0.1:5432/app';
  process.env.TOKENISATION_URL = 'http://127.0.0.1:1';
  process.env.SECURITY_SERVICE_URL = 'http://127.0.0.1:1';
  delete process.env.PROVISION_PER_TENANT_DB;
  appendFileSync(OUT, '{"dbg":"before import"}\n');
  await import('../index.js');
  appendFileSync(OUT, '{"dbg":"after import"}\n');
  base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i += 1) { try { await fetch(base + '/health'); break; } catch { await new Promise((r) => setTimeout(r, 30)); } }
  appendFileSync(OUT, '{"dbg":"after health"}\n');
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
  // positive control: the token is accepted by the real authenticate()
  const r = await fetch(base + '/api/audit-log', { signal: AbortSignal.timeout(5000), headers: { Authorization: `Bearer ${token()}` } });
  appendFileSync(OUT, JSON.stringify({ positive_control_auth: r.status, without_token: (await fetch(base + '/api/audit-log', { signal: AbortSignal.timeout(5000) })).status }) + '\n');
}, 60_000);
afterAll(() => { process.removeListener('unhandledRejection', onUnhandled); for (const l of SAVED) process.on('unhandledRejection', l as any); });

function seed(status: string | null) {
  h.st = { tenants: new Map(), contacts: new Set(), config: new Set(), audit: [] };
  if (status) { h.st.tenants.set(ID, { slug: 'gate-co', status }); h.st.contacts.add(ID); h.st.config.add(ID); }
  h.sql.length = 0; h.fail = [];
}

async function cell(route: string, scenario: string, method: string, path: string, body: unknown, seedStatus: string | null, fails: Array<[RegExp, string]>) {
  seed(seedStatus);
  h.fail = fails.map(([re, k]) => ({ re, make: KINDS[k] }));
  unhandled = 0; errLines.length = 0;
  const spyE = vi.spyOn(console, 'error').mockImplementation((...a: unknown[]) => { errLines.push(a.map((x) => typeof x === 'string' ? x.split('\n')[0] : `<${typeof x}>`).join(' | ')); });
  const spyW = vi.spyOn(console, 'warn').mockImplementation(() => undefined);
  let status: number | string = 'none'; let text = '';
  try {
    const res = await fetch(base + path, { method, signal: AbortSignal.timeout(2500),
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token()}` }, body: body === undefined ? undefined : JSON.stringify(body) });
    status = res.status; text = await res.text();
  } catch (e) { status = 'UNANSWERED(' + (e as Error).name + ')'; }
  await new Promise((r) => setTimeout(r, 60));
  spyE.mockRestore(); spyW.mockRestore();
  const erasing = h.sql.filter((s) => /^(DELETE|DROP|TRUNCATE)\b/i.test(s));
  const t = h.st.tenants.get(ID);
  appendFileSync(OUT, JSON.stringify({
    route, scenario, status, body: text, bodySha: crypto.createHash('sha256').update(text).digest('hex').slice(0, 16),
    sql: [...h.sql], erasing: erasing.length, erasingStmts: erasing,
    after: { tenant: t ? t.status : 'ABSENT', contacts: h.st.contacts.has(ID), config: h.st.config.has(ID), audit: [...h.st.audit] },
    errLines: [...errLines], unhandled,
  }) + '\n');
}

const K3 = ['ordinary', 'revokedProxy', 'throwingGetter'];
const KALL = Object.keys(KINDS);
const GOOD = { name: 'Gate Co', slug: 'gate-co' };

describe('gate 99 probe', () => {
  it('POST control ok', async () => { await cell('POST', 'control', 'POST', '/api/tenants', GOOD, null, []); });
  it('POST bad body (ZodError from parse)', async () => { await cell('POST', 'badBody', 'POST', '/api/tenants', { name: '', slug: 'X' }, null, []); });
  for (const k of KALL) it(`POST config INSERT rejects ${k}`, async () => { await cell('POST', `afterInsert:configInsert/${k}`, 'POST', '/api/tenants', GOOD, null, [[/^INSERT INTO tenant_config/, k]]); });
  for (const k of K3) it(`POST status UPDATE rejects ${k}`, async () => { await cell('POST', `afterInsert:activeUpdate/${k}`, 'POST', '/api/tenants', GOOD, null, [[/^UPDATE tenants SET status = 'active'/, k]]); });
  for (const k of [...K3, 'zod']) it(`POST slug SELECT rejects ${k}`, async () => { await cell('POST', `beforeInsert:slugSelect/${k}`, 'POST', '/api/tenants', GOOD, null, [[/^SELECT id FROM tenants WHERE slug/, k]]); });

  it('DELETE control', async () => { await cell('DELETE', 'control', 'DELETE', `/api/tenants/${ID}`, { confirm: true }, 'active', []); });
  it('DELETE no confirm', async () => { await cell('DELETE', 'noConfirm', 'DELETE', `/api/tenants/${ID}`, {}, 'active', []); });
  it('DELETE already archived', async () => { await cell('DELETE', 'alreadyArchived', 'DELETE', `/api/tenants/${ID}`, { confirm: true }, 'archived', []); });
  it('DELETE not found', async () => { await cell('DELETE', 'notFound', 'DELETE', `/api/tenants/${ID}`, { confirm: true }, null, []); });
  for (const k of K3) {
    it(`DELETE SELECT rejects ${k}`, async () => { await cell('DELETE', `select/${k}`, 'DELETE', `/api/tenants/${ID}`, { confirm: true }, 'active', [[/^SELECT slug, status FROM tenants/, k]]); });
    it(`DELETE archive UPDATE rejects ${k}`, async () => { await cell('DELETE', `archiveUpdate/${k}`, 'DELETE', `/api/tenants/${ID}`, { confirm: true }, 'active', [[/^UPDATE tenants SET status = 'archived'/, k]]); });
    it(`DELETE archived-audit INSERT rejects ${k}`, async () => { await cell('DELETE', `archivedAudit/${k}`, 'DELETE', `/api/tenants/${ID}`, { confirm: true }, 'active', [[/'tenant_archived'/, k]]); });
    it(`DELETE COMMIT rejects ${k}`, async () => { await cell('DELETE', `commit/${k}`, 'DELETE', `/api/tenants/${ID}`, { confirm: true }, 'active', [[/^COMMIT$/, k]]); });
    it(`DELETE UPDATE ordinary + ROLLBACK rejects ${k}`, async () => { await cell('DELETE', `rollbackFails/${k}`, 'DELETE', `/api/tenants/${ID}`, { confirm: true }, 'active', [[/^UPDATE tenants SET status = 'archived'/, 'ordinary'], [/^ROLLBACK$/, k]]); });
    it(`DELETE UPDATE ordinary + failed-audit INSERT rejects ${k}`, async () => { await cell('DELETE', `failedAudit/${k}`, 'DELETE', `/api/tenants/${ID}`, { confirm: true }, 'active', [[/^UPDATE tenants SET status = 'archived'/, 'ordinary'], [/'tenant_archive_failed'/, k]]); });
  }

  for (const k of [...K3, 'zod']) {
    it(`GET list rejects ${k}`, async () => { await cell('GET list', k, 'GET', '/api/tenants', undefined, 'active', [[/^SELECT t\.\*/, k]]); });
    it(`PATCH :id UPDATE rejects ${k}`, async () => { await cell('PATCH :id', k, 'PATCH', `/api/tenants/${ID}`, { name: 'New' }, 'active', [[/^UPDATE tenants SET name/, k]]); });
  }
  it('PATCH :id bad body (ZodError from parse)', async () => { await cell('PATCH :id', 'badBody', 'PATCH', `/api/tenants/${ID}`, { name: '' }, 'active', []); });
  for (const k of K3) {
    it(`GET :id rejects ${k}`, async () => { await cell('GET :id', k, 'GET', `/api/tenants/${ID}`, undefined, 'active', [[/^SELECT t\.\*/, k]]); });
    it(`PATCH status rejects ${k}`, async () => { await cell('PATCH status', k, 'PATCH', `/api/tenants/${ID}/status`, { status: 'suspended' }, 'active', [[/^UPDATE tenants SET status = \$1/, k]]); });
    it(`GET audit-log rejects ${k}`, async () => { await cell('GET audit-log', k, 'GET', '/api/audit-log', undefined, 'active', [[/^SELECT \* FROM platform_audit_log/, k]]); });
  }
});
