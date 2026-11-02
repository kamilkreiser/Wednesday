// QA GATE 112 probe (not part of the PR). Copied into the gate clone's src/__tests__ for the run only, then moved out.
// REAL app (index.ts routes, auth middleware, shared errorHandler), REAL db.ts (query/transaction/initDb) and the REAL
// shared queryWithTenantGuc, REAL winston logger (utils/logger, format chosen by LOGFMT). Only `pg` is replaced by a
// recording Pool: writes are staged per transaction and applied on COMMIT, dropped on ROLLBACK. Failures are injected
// per statement class with one thrown value kind. Every cell records the HTTP answer, the persisted store, the
// in-memory cache, usage-write attempts, captured log output, unhandled rejections and uncaught exceptions.
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import net from 'net';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import { appendFileSync } from 'fs';

process.env.SECURITY_DISABLE_BOOT = '1';
process.env.DATABASE_URL = 'postgres://gate112:stub@127.0.0.1:1/gate112';
delete process.env.API_KEY_ROTATION_GRACE_SECONDS;
delete process.env.LOG_LEVEL;

const OUT = process.env.PROBE_OUT as string;
const TENANT = 'c0000000-0000-4000-8000-000000001120';
const ORG = '11201120-1120-4112-8112-112011201120';
const USER = 'd0000000-0000-4000-8000-000000001120';

// ---- outbound network witness (installed before anything connects) ----
const connects: string[] = [];
const origConnect = net.Socket.prototype.connect;
(net.Socket.prototype as any).connect = function (...a: any[]) {
  const o = a[0];
  const tgt = typeof o === 'object' && o !== null ? (o.path ? 'unix:' + o.path : `${o.host ?? 'localhost'}:${o.port}`) : `${a[1] ?? 'localhost'}:${o}`;
  connects.push(tgt);
  return (origConnect as any).apply(this, a);
};

const h = vi.hoisted(() => ({
  fail: null as null | string,  // insertKey | findByHash | usage | audit | event | scopes | lookupById
  toThrow: undefined as unknown,
  keys: new Map<string, Record<string, unknown>>(),
  audit: new Set<string>(),
  events: new Map<string, boolean>(),
  usageAttempts: 0,
  committedWrites: [] as string[],
}));

vi.mock('pg', () => {
  type W = () => void;
  const norm = (s: string) => String(s).replace(/\s+/g, ' ').trim();
  function cls(n: string): string {
    if (/^INSERT INTO svc_api_keys/i.test(n)) return 'insertKey';
    if (/security_find_api_key_by_hash/i.test(n)) return 'findByHash';
    if (/^UPDATE svc_api_keys SET last_used_at/i.test(n)) return 'usage';
    if (/^INSERT INTO audit_logs/i.test(n)) return 'audit';
    if (/^INSERT INTO svc_security_events/i.test(n)) return 'event';
    if (/admin_organisation_scopes/i.test(n)) return 'scopes';
    if (/^SELECT \* FROM svc_api_keys WHERE id/i.test(n)) return 'lookupById';
    if (/^SELECT 1 AS ok/i.test(n)) return 'select1';
    return 'other';
  }
  function exec(s: string, values: unknown[] | undefined, pending: W[] | null): Promise<any> {
    const n = norm(s); const c = cls(n);
    if (c === 'usage') h.usageAttempts += 1;
    if (h.fail === c) return Promise.reject(h.toThrow);
    const stage = (label: string, w: W) => { const ww = () => { w(); h.committedWrites.push(label); }; if (pending) pending.push(ww); else ww(); };
    const v = values ?? [];
    switch (c) {
      case 'select1': return Promise.resolve({ rows: [{ ok: 1 }], rowCount: 1 });
      case 'insertKey': {
        const row: Record<string, unknown> = { id: v[0], organization_id: v[1], tenant_id: v[2], name: v[3], key_hash: v[4], key_prefix: v[5],
          scopes: v[6], rate_limit: v[7], rate_limit_window: v[8], last_used_at: v[9], usage_count: v[10], is_active: v[11], expires_at: v[12],
          created_at: v[13], connector_id: v[14] };
        stage('upsert ' + String(v[0]).slice(0, 8) + ' active=' + v[11], () => {
          const prev = h.keys.get(String(v[0]));
          h.keys.set(String(v[0]), prev ? { ...prev, last_used_at: row.last_used_at, usage_count: row.usage_count, is_active: row.is_active } : row);
        });
        return Promise.resolve({ rows: [], rowCount: 1 });
      }
      case 'findByHash': {
        const r = [...h.keys.values()].filter((k) => k.key_hash === v[0]);
        return Promise.resolve({ rows: r.map((x) => ({ ...x })), rowCount: r.length });
      }
      case 'lookupById': {
        const r = h.keys.get(String(v[0]));
        return Promise.resolve({ rows: r ? [{ ...r }] : [], rowCount: r ? 1 : 0 });
      }
      case 'usage': {
        stage('usage', () => { const r = h.keys.get(String(v[0])); if (r) r.usage_count = Number(r.usage_count) + 1; });
        return Promise.resolve({ rows: [], rowCount: 1 });
      }
      case 'audit': stage('audit', () => h.audit.add(String(v[0]))); return Promise.resolve({ rows: [], rowCount: 1 });
      case 'event': stage('event', () => h.events.set(String(v[0]), Boolean(v[7]))); return Promise.resolve({ rows: [], rowCount: 1 });
      case 'scopes': return Promise.resolve({ rows: [{ o: ORG_ }], rowCount: 1 });
      default: return Promise.resolve({ rows: [], rowCount: 0 });
    }
  }
  const ORG_ = '11201120-1120-4112-8112-112011201120';
  class Client {
    pending: W[] | null = null;
    query(text: string, values?: unknown[]) {
      const n = norm(text);
      if (n === 'BEGIN') { this.pending = []; return Promise.resolve({ rows: [] }); }
      if (n === 'COMMIT') { for (const w of this.pending ?? []) w(); this.pending = null; return Promise.resolve({ rows: [] }); }
      if (n === 'ROLLBACK') { this.pending = null; return Promise.resolve({ rows: [] }); }
      return exec(text, values, this.pending);
    }
    release() {}
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
  const payload = b64url(Buffer.from(JSON.stringify({ sub: USER, userId: USER, iat: now, exp: now + 600, ...claims })));
  const sig = b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM));
  return `${header}.${payload}.${sig}`;
}

const SECRET = 'G112-SECRET-IN-MESSAGE';
function withMsg(get: () => unknown, code?: string) {
  const e = Object.create(Error.prototype, { message: { get, configurable: true } });
  if (code) e.code = code;
  return e;
}
const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('db down ' + SECRET),
  ordinary08006: () => Object.assign(new Error('db down ' + SECRET), { code: '08006' }),
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  getterThrows: () => withMsg(() => { throw new Error('getter boom ' + SECRET); }),
  getterThrows08006: () => withMsg(() => { throw new Error('getter boom ' + SECRET); }, '08006'),
  nullProto: () => Object.create(null),
  plainString: () => 'db down ' + SECRET,
  msgSymbol: () => withMsg(() => Symbol(SECRET)),
  msgRevokedProxy: () => withMsg(() => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }),
  msgBigInt: () => withMsg(() => 1868n),
  msgToStringThrows: () => withMsg(() => ({ toString() { throw new Error('toString boom'); }, secret: SECRET })),
};

let server: Server; let base: string; let mod: any;
const SAVED_UR = process.listeners('unhandledRejection'); const SAVED_UE = process.listeners('uncaughtException');
let unhandled = 0; let uncaught = 0;
const onUR = () => { unhandled += 1; }; const onUE = () => { uncaught += 1; };
const captured: string[] = [];
let rawKey = ''; let keyHash = '';

beforeAll(async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;
  // logger format: create the REAL logger under the requested NODE_ENV, then restore NODE_ENV before the app loads
  const prevEnv = process.env.NODE_ENV;
  process.env.NODE_ENV = process.env.LOGFMT === 'production' ? 'production' : 'test';
  const lg: any = await import('../utils/logger');
  process.env.NODE_ENV = prevEnv;
  for (const t of lg.logger.transports) {
    const orig = t.log.bind(t);
    t.log = (info: any, cb: any) => { captured.push('W ' + String(info[Symbol.for('message')])); return orig(info, cb); };
  }
  const db = await import('../db');
  const ok = await db.initDb();
  mod = await import('../index');
  await new Promise<void>((r) => { server = mod.default.listen(0, '127.0.0.1', r); });
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  process.removeAllListeners('unhandledRejection'); process.on('unhandledRejection', onUR);
  process.removeAllListeners('uncaughtException'); process.on('uncaughtException', onUE);
  appendFileSync(OUT, JSON.stringify({ positive_control: { initDb: ok, isDbAvailable: db.isDbAvailable(), logfmt: process.env.LOGFMT, transports: lg.logger.transports.length } }) + '\n');
});
afterAll(async () => {
  process.removeListener('unhandledRejection', onUR); process.removeListener('uncaughtException', onUE);
  for (const l of SAVED_UR) process.on('unhandledRejection', l as any);
  for (const l of SAVED_UE) process.on('uncaughtException', l as any);
  await new Promise<void>((r) => server.close(() => r()));
  const outbound = connects.filter((c) => !/^(127\.0\.0\.1|localhost|::1|unix:)/.test(c));
  appendFileSync(OUT, JSON.stringify({ network: { connects, outbound } }) + '\n');
});

const ADMIN = () => token({ role: 'super_admin', tenantId: TENANT });
async function call(method: string, path: string, body?: unknown, auth = true) {
  let status: number | string = 'none'; let json: any = null;
  try {
    const res = await fetch(base + path, { method, signal: AbortSignal.timeout(2500),
      headers: { 'Content-Type': 'application/json', ...(auth ? { Authorization: `Bearer ${ADMIN()}` } : {}) },
      body: body === undefined ? undefined : JSON.stringify(body) });
    status = res.status; const t = await res.text(); try { json = JSON.parse(t); } catch { json = t.slice(0, 160); }
  } catch (e) { status = 'UNANSWERED(' + (e as Error).name + ')'; }
  return { status, json };
}
function snapshot() {
  return {
    keys: Object.fromEntries([...h.keys.values()].map((r) => [String(r.id).slice(0, 12), { active: r.is_active, usage: r.usage_count }])),
    audit: h.audit.size, events: Object.fromEntries([...h.events.entries()].map(([k, v]) => [k.slice(0, 12), v])),
    mem: Object.fromEntries([...mod.memApiKeys.values()].map((k: any) => [String(k.id).slice(0, 12), k.isActive])),
  };
}
function reset() { h.fail = null; h.toThrow = undefined; h.keys.clear(); h.audit.clear(); h.events.clear(); h.usageAttempts = 0; h.committedWrites.length = 0; mod.memApiKeys.clear(); }

let cap: string[] = [];
function startCap() {
  cap = []; captured.length = 0; unhandled = 0; uncaught = 0;
  const push = (...a: unknown[]) => { try { cap.push('C ' + a.map(String).join(' ')); } catch { cap.push('C <unprintable>'); } };
  return [vi.spyOn(console, 'log').mockImplementation(push), vi.spyOn(console, 'warn').mockImplementation(push), vi.spyOn(console, 'error').mockImplementation(push)];
}
async function stopCap(spies: any[]) { await new Promise((r) => setTimeout(r, 60)); for (const s of spies) s.mockRestore(); return [...captured, ...cap]; }

async function mintControl(): Promise<string> {
  const r = await call('POST', '/api/keys', { name: 'g112', scopes: ['documents:read'], tenantId: TENANT, organizationId: ORG });
  rawKey = r.json?.data?.key ?? ''; keyHash = crypto.createHash('sha256').update(rawKey).digest('hex');
  return r.json?.data?.id ?? '';
}

function rec(cell: string, kind: string | null, r: any, lines: string[], extra: Record<string, unknown> = {}) {
  const valueLeak = lines.filter((l) => l.includes(SECRET)).length;
  const keyLeak = rawKey ? lines.filter((l) => l.includes(rawKey) || l.includes(keyHash)).length : 0;
  const rel = lines.filter((l) => /save|unreadable|KS-1370|DB fallback|KS-888|Error occurred|boot work|Database/i.test(l)).map((l) => l.replace(/\u001b\[[0-9;]*m/g, '').slice(0, 220));
  appendFileSync(OUT, JSON.stringify({ cell, kind, status: r.status, body: r.json && typeof r.json === 'object' ? { success: r.json.success, code: r.json.error?.code, message: r.json.error?.message, data: r.json.data ? Object.keys(r.json.data).sort() : undefined, valid: r.json.data?.valid, reason: r.json.data?.reason, keyIssued: typeof r.json.data?.key === 'string' } : r.json,
    store: snapshot(), usageAttempts: h.usageAttempts, committedWrites: [...h.committedWrites], unhandled, uncaught, valueLeak, keyLeak, unreadableConst: lines.some((l) => l.includes('unreadable thrown value')), logs: rel, ...extra }) + '\n');
}

const K = Object.keys(KINDS);
describe('gate 112 probe', () => {
  it('control: mint, validate, revoke, audit, event, scopes all succeed', async () => {
    reset(); const s = startCap();
    const id = await mintControl();
    const v = await call('POST', '/api/keys/validate', { key: rawKey }, false);
    const a = await call('POST', '/api/audit', { action: 'g112', resourceType: 'gate' });
    const e = await call('POST', '/api/events', { eventType: 'g112', severity: 'low', source: 'gate' });
    const sc = await call('GET', `/api/keys/admin-scopes/${USER}?tenantId=${TENANT}`);
    const d = await call('DELETE', `/api/keys/${id}`);
    const v2 = await call('POST', '/api/keys/validate', { key: rawKey }, false);
    const lines = await stopCap(s);
    rec('control', null, v, lines, { mint: !!rawKey, validate: v.json?.data?.valid, audit: a.status, event: e.status, scopes: sc.status, revoke: d.status, afterRevoke: v2.json?.data });
  });
  for (const k of K) {
    it(`mint: INSERT rejects ${k}`, async () => {
      reset(); rawKey = ''; const s = startCap(); h.fail = 'insertKey'; h.toThrow = KINDS[k]();
      const r = await call('POST', '/api/keys', { name: 'g112', scopes: ['documents:read'], tenantId: TENANT, organizationId: ORG });
      rec('mint', k, r, await stopCap(s));
    });
    it(`revoke: save rejects ${k}`, async () => {
      reset(); const id = await mintControl(); const s = startCap(); h.fail = 'insertKey'; h.toThrow = KINDS[k]();
      const r = await call('DELETE', `/api/keys/${id}`);
      h.fail = null; const after = await call('POST', '/api/keys/validate', { key: rawKey }, false);
      rec('revoke', k, r, await stopCap(s), { validateAfter: after.json?.data ?? after.status });
    });
    it(`validate cached: stored read rejects ${k}`, async () => {
      reset(); await mintControl(); const s = startCap(); h.fail = 'findByHash'; h.toThrow = KINDS[k]();
      rec('validate-stored', k, await call('POST', '/api/keys/validate', { key: rawKey }, false), await stopCap(s));
    });
    it(`validate cached REVOKED in memory: stored read rejects ${k}`, async () => {
      reset(); await mintControl(); for (const x of mod.memApiKeys.values()) x.isActive = false;
      const s = startCap(); h.fail = 'findByHash'; h.toThrow = KINDS[k]();
      rec('validate-stored-memrevoked', k, await call('POST', '/api/keys/validate', { key: rawKey }, false), await stopCap(s));
    });
    it(`validate miss: lookup rejects ${k}`, async () => {
      reset(); await mintControl(); mod.memApiKeys.clear(); const s = startCap(); h.fail = 'findByHash'; h.toThrow = KINDS[k]();
      rec('validate-lookup', k, await call('POST', '/api/keys/validate', { key: rawKey }, false), await stopCap(s));
    });
    it(`validate active: usage write rejects ${k}`, async () => {
      reset(); await mintControl(); const s = startCap(); h.fail = 'usage'; h.toThrow = KINDS[k]();
      rec('validate-usage', k, await call('POST', '/api/keys/validate', { key: rawKey }, false), await stopCap(s));
    });
    it(`validate stored-REVOKED: usage write would reject ${k}`, async () => {
      reset(); await mintControl(); for (const r of h.keys.values()) r.is_active = false;
      const s = startCap(); h.fail = 'usage'; h.toThrow = KINDS[k]();
      rec('validate-storedrevoked', k, await call('POST', '/api/keys/validate', { key: rawKey }, false), await stopCap(s));
    });
    it(`audit: INSERT rejects ${k}`, async () => {
      reset(); const s = startCap(); h.fail = 'audit'; h.toThrow = KINDS[k]();
      rec('audit', k, await call('POST', '/api/audit', { action: 'g112', resourceType: 'gate' }), await stopCap(s), { memAudit: mod.memAuditLogs?.length });
    });
    it(`event: INSERT rejects ${k}`, async () => {
      reset(); const s = startCap(); h.fail = 'event'; h.toThrow = KINDS[k]();
      rec('event', k, await call('POST', '/api/events', { eventType: 'g112', severity: 'low', source: 'gate' }), await stopCap(s));
    });
    it(`resolve: event save rejects ${k}`, async () => {
      reset(); const e = await call('POST', '/api/events', { eventType: 'g112', severity: 'low', source: 'gate' });
      const s = startCap(); h.fail = 'event'; h.toThrow = KINDS[k]();
      rec('resolve', k, await call('PATCH', `/api/events/${e.json?.data?.id}/resolve`, {}), await stopCap(s));
    });
    it(`admin-scopes GET: read rejects ${k}`, async () => {
      reset(); const s = startCap(); h.fail = 'scopes'; h.toThrow = KINDS[k]();
      rec('scopes', k, await call('GET', `/api/keys/admin-scopes/${USER}?tenantId=${TENANT}`), await stopCap(s));
    });
  }
});
