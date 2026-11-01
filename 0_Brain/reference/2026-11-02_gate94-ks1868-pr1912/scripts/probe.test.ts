// QA GATE 94 probe (NOT part of PR 1912). Copied into the gate clone's src/__tests__ for the run only, then moved out.
// Drives the REAL routes DELETE /api/keys/:id, POST /api/keys (plain and rotate) and PUT /api/keys/admin-scopes/:userId,
// plus POST /api/keys/validate afterwards, through the REAL db.ts (query(), transaction(), initDb()) and the real shared
// queryWithTenantGuc. Only the `pg` driver is replaced: a recording Pool whose clients stage writes and apply them
// only on COMMIT (ROLLBACK drops them). One statement class is made to reject with the cell's value.
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import { appendFileSync } from 'fs';
import { z } from 'zod';

process.env.SECURITY_DISABLE_BOOT = '1';
process.env.DATABASE_URL = 'postgres://gate94:stub@127.0.0.1:1/gate94';

const OUT = process.env.PROBE_OUT as string;
const TENANT = 'c0000000-0000-4000-8000-000000009494';
const ORG = '94949494-9494-4094-8094-949494949494';
const ORG_A = '94000000-0000-4000-8000-00000000000a';
const ORG_B = '94000000-0000-4000-8000-00000000000b';
const ADMIN_USER = '94000000-0000-4000-8000-0000000000ad';
const KEY_ID = 'key_gate94_target';
const KEY_VALUE = 'sk_gate94_' + 'a'.repeat(40);
const KEY_HASH = crypto.createHash('sha256').update(KEY_VALUE).digest('hex');

const h = vi.hoisted(() => ({
  failRe: null as RegExp | null,
  failValue: undefined as unknown,
  keys: new Map<string, Record<string, unknown>>(),
  scopes: new Set<string>(),
  sql: [] as string[],
}));

vi.mock('pg', () => {
  type W = () => void;
  const norm = (s: string) => String(s).replace(/\s+/g, ' ').trim();
  const label = (n: string) => n.slice(0, 48);
  function exec(text: string, values: any[] | undefined, pending: W[] | null): Promise<any> {
    const n = norm(text);
    h.sql.push(label(n));
    if (h.failRe && h.failRe.test(n)) return Promise.reject(h.failValue);
    const stage = (w: W) => { if (pending) pending.push(w); else w(); };
    if (/^SELECT 1 AS ok/i.test(n) || /^SELECT 1$/i.test(n)) return Promise.resolve({ rows: [{ ok: 1 }], rowCount: 1 });
    if (/^INSERT INTO svc_api_keys/i.test(n)) {
      const v = values as any[];
      const row = { id: v[0], organization_id: v[1], tenant_id: v[2], name: v[3], key_hash: v[4], key_prefix: v[5], scopes: v[6],
        rate_limit: v[7], rate_limit_window: v[8], last_used_at: v[9], usage_count: v[10], is_active: v[11], expires_at: v[12],
        created_at: v[13], connector_id: v[14] };
      stage(() => { const prev = h.keys.get(String(v[0])); h.keys.set(String(v[0]), prev ? { ...prev, is_active: v[11], usage_count: v[10], last_used_at: v[9] } : row); });
      return Promise.resolve({ rows: [], rowCount: 1 });
    }
    if (/^SELECT \* FROM svc_api_keys WHERE id = \$1/i.test(n)) {
      const r = h.keys.get(String(values?.[0])); return Promise.resolve({ rows: r ? [{ ...r }] : [], rowCount: r ? 1 : 0 });
    }
    if (/security_find_api_key_by_hash/i.test(n)) {
      const r = [...h.keys.values()].find((x) => x.key_hash === values?.[0]); return Promise.resolve({ rows: r ? [{ ...r }] : [], rowCount: r ? 1 : 0 });
    }
    if (/^UPDATE svc_api_keys SET last_used_at/i.test(n)) return Promise.resolve({ rows: [], rowCount: 1 });
    if (/^SELECT 1 FROM users/i.test(n)) return Promise.resolve({ rows: [{ '?column?': 1 }], rowCount: 1 });
    if (/^SELECT id::text AS id FROM organizations/i.test(n)) return Promise.resolve({ rows: (values?.[1] as string[]).map((id) => ({ id })), rowCount: 1 });
    if (/^SELECT organization_id::text AS o FROM admin_organisation_scopes/i.test(n)) return Promise.resolve({ rows: [...h.scopes].sort().map((o) => ({ o })), rowCount: h.scopes.size });
    if (/^DELETE FROM admin_organisation_scopes/i.test(n)) { stage(() => h.scopes.clear()); return Promise.resolve({ rows: [], rowCount: 1 }); }
    if (/^INSERT INTO admin_organisation_scopes/i.test(n)) { const ids = values?.[3] as string[]; stage(() => ids.forEach((o) => h.scopes.add(o))); return Promise.resolve({ rows: [], rowCount: ids.length }); }
    return Promise.resolve({ rows: [], rowCount: 0 });
  }
  class Client {
    pending: W[] | null = null;
    query(text: string, values?: any[]) {
      const n = norm(text);
      if (n === 'BEGIN') { h.sql.push('BEGIN'); this.pending = []; return Promise.resolve({ rows: [] }); }
      if (n === 'COMMIT') { h.sql.push('COMMIT'); for (const w of this.pending ?? []) w(); this.pending = null; return Promise.resolve({ rows: [] }); }
      if (n === 'ROLLBACK') { h.sql.push('ROLLBACK'); this.pending = null; return Promise.resolve({ rows: [] }); }
      if (/^(SAVEPOINT|ROLLBACK TO SAVEPOINT|RELEASE SAVEPOINT) /i.test(n)) { h.sql.push(n); return Promise.resolve({ rows: [] }); }
      return exec(text, values, this.pending);
    }
    release() {}
  }
  class Pool {
    constructor(_o?: unknown) {}
    on() { return this; }
    connect() { return Promise.resolve(new Client()); }
    query(text: string, values?: any[]) { return exec(text, values, null); }
    end() { return Promise.resolve(); }
  }
  return { Pool, default: { Pool } };
});

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64url = (b: Buffer) => b.toString('base64url');
function token(): string {
  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const payload = b64url(Buffer.from(JSON.stringify({ sub: 'gate94', iat: now, exp: now + 300, role: 'super_admin' })));
  return `${header}.${payload}.${b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM))}`;
}

const throwingCode = () => { throw new Error('getter boom'); };
const KINDS: Record<string, () => unknown> = {
  infraError: () => Object.assign(new Error('connect ECONNREFUSED 127.0.0.1:5432'), { code: 'ECONNREFUSED' }),
  ordinaryError: () => new Error('db down'),
  zodError: () => new z.ZodError([{ code: 'custom', message: 'gate94', path: ['x'] } as any]),
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  messageGetterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  codeGetterThrows: () => Object.defineProperty(new Error('db down'), 'code', { get: throwingCode }),
  codeGetterThrowsInfraMsg: () => Object.defineProperty(new Error('Connection terminated unexpectedly'), 'code', { get: throwingCode }),
  plainObjCodeGetter: () => ({ message: 'db down', get code(): string { return throwingCode(); } }),
};

let server: Server; let base: string; let memApiKeys: Map<string, any>;
const SAVED = process.listeners('unhandledRejection');
let unhandled = 0; const onUnhandled = () => { unhandled += 1; };
const lines: string[] = [];

beforeAll(async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;
  const db = await import('../db');
  const ok = await db.initDb();
  const mod: any = await import('../index');
  memApiKeys = mod.memApiKeys;
  await new Promise<void>((r) => { server = mod.default.listen(0, '127.0.0.1', r); });
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
  appendFileSync(OUT, JSON.stringify({ positive_control: { initDb: ok, isDbAvailable: db.isDbAvailable() } }) + '\n');
});
afterAll(async () => {
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED) process.on('unhandledRejection', l as any);
  await new Promise<void>((r) => server.close(() => r()));
});

async function call(method: string, path: string, payload?: unknown, auth = true) {
  try {
    const res = await fetch(base + path, {
      method, signal: AbortSignal.timeout(2500),
      headers: { 'Content-Type': 'application/json', ...(auth ? { Authorization: `Bearer ${token()}` } : {}) },
      body: payload === undefined ? undefined : JSON.stringify(payload),
    });
    const text = await res.text(); let body: any; try { body = JSON.parse(text); } catch { body = text.slice(0, 200); }
    return { status: res.status as number | string, text, body };
  } catch (e) { return { status: 'UNANSWERED(' + (e as Error).name + ')', text: '', body: null }; }
}

function begin(failRe: RegExp | null, kind: string | null) {
  h.sql.length = 0; unhandled = 0; lines.length = 0;
  h.failRe = kind ? failRe : null; h.failValue = kind ? KINDS[kind]() : undefined;
  const push = (...a: unknown[]) => { lines.push(a.map(String).join(' ')); };
  const pushChunk = (chunk: unknown) => { String(chunk).split('\n').filter(Boolean).forEach((l) => lines.push(l)); return true; };
  return [vi.spyOn(console, 'log').mockImplementation(push), vi.spyOn(console, 'error').mockImplementation(push), vi.spyOn(console, 'warn').mockImplementation(push),
    vi.spyOn(process.stdout, 'write').mockImplementation(pushChunk as any), vi.spyOn(process.stderr, 'write').mockImplementation(pushChunk as any)];
}
const end = async (spies: any[]) => { await new Promise((r) => setTimeout(r, 60)); h.failRe = null; spies.forEach((s) => s.mockRestore()); };
const logs = (re: RegExp) => lines.filter((s) => re.test(s)).map((s) => { try { const j = JSON.parse(s); return { message: j.message, fields: Object.keys(j).filter((k) => !['timestamp', 'level', 'service', 'message'].includes(k)), values: j }; } catch { return { raw: s.slice(0, 200) }; } });

function seedKey() {
  memApiKeys.clear(); h.keys.clear();
  const row = { id: KEY_ID, organization_id: ORG, tenant_id: TENANT, name: 'gate94', key_hash: KEY_HASH, key_prefix: 'sk_gate94', scopes: '["documents:read"]',
    rate_limit: 100, rate_limit_window: 60, last_used_at: null, usage_count: 0, is_active: true, expires_at: null, created_at: new Date().toISOString(), connector_id: null };
  h.keys.set(KEY_ID, row);
  memApiKeys.set(KEY_ID, { id: KEY_ID, organizationId: ORG, tenantId: TENANT, name: 'gate94', keyHash: KEY_HASH, keyPrefix: 'sk_gate94', scopes: ['documents:read'],
    rateLimit: 100, rateLimitWindow: 60, usageCount: 0, isActive: true, createdAt: new Date() });
}
async function validate() { const r = await call('POST', '/api/keys/validate', { key: KEY_VALUE }, false); return { status: r.status, valid: r.body?.data?.valid, reason: r.body?.data?.reason ?? null }; }

async function revokeCell(kind: string | null) {
  seedKey();
  const spies = begin(/^INSERT INTO svc_api_keys/i, kind);
  const r = await call('DELETE', '/api/keys/' + KEY_ID);
  await end(spies);
  const rec: any = {
    route: 'DELETE /api/keys/:id', kind: kind ?? 'control(save lands)', status: r.status, code: r.body?.error?.code ?? null, message: r.body?.error?.message ?? r.body?.message ?? null,
    memIsActive: memApiKeys.get(KEY_ID)?.isActive, persistedIsActive: h.keys.get(KEY_ID)?.is_active,
    sql: [...h.sql], ks888: logs(/KS-888/), errorHandlerLines: logs(/Error occurred/), dbSaveLines: logs(/DB save API key failed/), unhandledAtRevoke: unhandled,
  };
  rec.validateSameProcess = await validate();
  // A restart: memory is rebuilt from the store only (boot warms memApiKeys from svc_api_keys). Simulated by clearing memory.
  memApiKeys.clear();
  rec.validateAfterRestart = await validate();
  appendFileSync(OUT, JSON.stringify(rec) + '\n');
}

async function registerCell(rotate: boolean, kind: string | null) {
  memApiKeys.clear(); h.keys.clear();
  const spies = begin(/^INSERT INTO svc_api_keys/i, kind);
  const r = await call('POST', '/api/keys', { name: 'gate94', scopes: ['documents:read'], tenantId: TENANT, organizationId: ORG, ...(rotate ? { connectorId: 'gate94-conn', rotate: true } : {}) });
  await end(spies);
  appendFileSync(OUT, JSON.stringify({
    route: rotate ? 'POST /api/keys rotate' : 'POST /api/keys plain', kind: kind ?? 'control(save lands)', status: r.status, code: r.body?.error?.code ?? null, message: r.body?.error?.message ?? null,
    keyIssued: typeof r.body?.data?.key === 'string', skInText: r.text.includes('sk_'), memKeys: memApiKeys.size, committedKeys: h.keys.size,
    sql: [...h.sql], ks888: logs(/KS-888/), errorHandlerLines: logs(/Error occurred/), unhandled,
  }) + '\n');
}

async function scopesCell(kind: string | null, badBody = false) {
  h.scopes.clear(); h.scopes.add(ORG_A);
  const spies = begin(badBody ? null : /^DELETE FROM admin_organisation_scopes/i, kind);
  const r = await call('PUT', '/api/keys/admin-scopes/' + ADMIN_USER, badBody ? { tenantId: 'not-a-uuid', organizationIds: [ORG_B] } : { tenantId: TENANT, organizationIds: [ORG_B] });
  await end(spies);
  appendFileSync(OUT, JSON.stringify({
    route: 'PUT /api/keys/admin-scopes/:userId', kind: badBody ? 'zod(bad body)' : (kind ?? 'control(write lands)'), status: r.status, code: r.body?.error?.code ?? null, message: r.body?.error?.message ?? null,
    committedScopes: [...h.scopes].map((o) => (o === ORG_A ? 'A' : o === ORG_B ? 'B' : o)), sql: [...h.sql],
    infraLines: logs(/scope write failed on infrastructure/), errorHandlerLines: logs(/Error occurred/), unhandled,
  }) + '\n');
}

const FAIL_KINDS = ['infraError', 'ordinaryError', 'revokedProxy', 'messageGetterThrows', 'codeGetterThrows', 'codeGetterThrowsInfraMsg', 'plainObjCodeGetter'];
describe('gate 94 probe', () => {
  it('revoke control', async () => { await revokeCell(null); });
  for (const k of FAIL_KINDS) it(`revoke ${k}`, async () => { await revokeCell(k); });
  for (const rot of [false, true]) {
    it(`register ${rot} control`, async () => { await registerCell(rot, null); });
    for (const k of FAIL_KINDS) it(`register ${rot} ${k}`, async () => { await registerCell(rot, k); });
  }
  it('scopes control', async () => { await scopesCell(null); });
  it('scopes zod bad body', async () => { await scopesCell(null, true); });
  for (const k of [...FAIL_KINDS, 'zodError']) it(`scopes ${k}`, async () => { await scopesCell(k); });
});
