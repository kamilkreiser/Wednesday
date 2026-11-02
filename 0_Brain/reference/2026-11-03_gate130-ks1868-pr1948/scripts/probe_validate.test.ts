// QA GATE 130 probe (NOT part of PR 1948). Copied into the gate clone's src/__tests__ for the run only, then moved out.
// Drives the REAL POST /api/keys/validate route (and POST /api/audit, /api/events) with the REAL winston logger
// (src/utils/logger.ts, not mocked). Only '../db' is replaced (as the PR's own cells do). Each cell imports a FRESH copy of
// the app and logger (vi.resetModules), so a winston stream broken by one cell cannot leak into the next; a canary line is
// logged through the same logger after every cell to detect a logger that has stopped writing.
// PROBE_FMT=production -> the logger is built with NODE_ENV=production (json() format); otherwise NODE_ENV=test (dev printf).
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import { appendFileSync } from 'fs';

process.env.SECURITY_DISABLE_BOOT = '1';
const OUT = process.env.PROBE_OUT as string;
const FMT = process.env.PROBE_FMT === 'production' ? 'production' : 'test';

const h = vi.hoisted(() => ({
  storedBoom: undefined as unknown, lookupBoom: undefined as unknown, usageBoom: undefined as unknown,
  auditBoom: undefined as unknown,
  row: undefined as Record<string, unknown> | undefined,
  sql: [] as string[],
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  initDb: async () => true,
  query: async (statement: string) => {
    const s = String(statement).replace(/\s+/g, ' ').trim();
    h.sql.push(s.slice(0, 48));
    if (/security_find_api_key_by_hash/i.test(s)) {
      if (h.storedBoom !== undefined) return Promise.reject(h.storedBoom);
      if (h.lookupBoom !== undefined) return Promise.reject(h.lookupBoom);
      return { rows: h.row ? [h.row] : [], rowCount: h.row ? 1 : 0 };
    }
    if (/^UPDATE svc_api_keys SET last_used_at/i.test(s) && h.usageBoom !== undefined) return Promise.reject(h.usageBoom);
    if (/^INSERT INTO (audit_logs|svc_security_events)/i.test(s) && h.auditBoom !== undefined) return Promise.reject(h.auditBoom);
    return { rows: [], rowCount: 0 };
  },
  transaction: async (run: (client: unknown) => Promise<unknown>) => run({ query: (t: string) => { h.sql.push(String(t).replace(/\s+/g, ' ').trim().slice(0, 48)); return Promise.resolve({ rows: [], rowCount: 0 }); } }),
}));

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const SIGNING_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const VERIFY_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const ORG_ID = '13013013-0130-4130-8130-130130130130';
const TENANT_ID = 'c0000000-0000-4000-8000-000000000130';
function token(): string {
  const now = Math.floor(Date.now() / 1000);
  const hd = Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })).toString('base64url');
  const cl = Buffer.from(JSON.stringify({ sub: 'gate130', iat: now, exp: now + 300, role: 'super_admin' })).toString('base64url');
  return hd + '.' + cl + '.' + crypto.sign('RSA-SHA256', Buffer.from(hd + '.' + cl), SIGNING_PEM).toString('base64url');
}

const withMessage = (value: () => unknown): unknown =>
  Object.create(Error.prototype, { message: { get() { return value(); } } });
const revoked = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('db down'),
  msgRevokedProxy: () => withMessage(revoked),
  msgToStringThrows: () => withMessage(() => ({ toString: () => { throw new Error('toString boom'); } })),
  msgNullProto: () => withMessage(() => Object.create(null)),
  msgSymbol: () => withMessage(() => Symbol('g130')),
  msgBigInt: () => withMessage(() => BigInt(130)),
  msgCyclic: () => withMessage(() => { const o: any = { a: 1 }; o.self = o; return o; }),
  msgThrowingField: () => withMessage(() => Object.defineProperty({}, 'f', { enumerable: true, get() { throw new Error('field boom'); } })),
  msgToJSONThrows: () => withMessage(() => ({ toJSON() { throw new Error('toJSON boom'); } })),
  wholeRevokedProxy: () => revoked(),
  plainString: () => 'plain string down',
};

let caught: string[] = []; let unhandled = 0; let uncaught = 0;
const onUnh = (r: unknown) => { unhandled += 1; let d = 'unreadable'; try { d = r instanceof Error ? r.constructor.name + ': ' + r.message : typeof r; } catch { /* */ } caught.push('unhandledRejection ' + d); };
const onUnc = (e: unknown) => { uncaught += 1; let d = 'unreadable'; try { d = e instanceof Error ? e.constructor.name + ': ' + e.message : typeof e; } catch { /* */ } caught.push('uncaughtException ' + d); };
const SAVED_R = process.listeners('unhandledRejection'); const SAVED_E = process.listeners('uncaughtException');
const lines: string[] = [];
beforeAll(() => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(VERIFY_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;
  process.removeAllListeners('unhandledRejection'); process.on('unhandledRejection', onUnh);
  process.removeAllListeners('uncaughtException'); process.on('uncaughtException', onUnc);
  const grab = (...a: unknown[]) => { lines.push(a.map((x) => { try { return String(x); } catch { return '?'; } }).join(' ')); return true; };
  const out = (console as any)._stdout; const err = (console as any)._stderr;
  if (out) vi.spyOn(out, 'write').mockImplementation(grab as any);
  if (err) vi.spyOn(err, 'write').mockImplementation(grab as any);
  vi.spyOn(console, 'log').mockImplementation(grab as any);
  vi.spyOn(console, 'error').mockImplementation(grab as any);
  vi.spyOn(console, 'warn').mockImplementation(grab as any);
  vi.spyOn(process.stdout, 'write').mockImplementation(grab as any);
});
afterAll(() => {
  process.removeListener('unhandledRejection', onUnh); for (const l of SAVED_R) process.on('unhandledRejection', l as any);
  process.removeListener('uncaughtException', onUnc); for (const l of SAVED_E) process.on('uncaughtException', l as any);
  vi.restoreAllMocks();
});

async function call(root: string, method: string, path: string, payload: unknown, auth: boolean) {
  try {
    const res = await fetch(root + path, { method, headers: { 'Content-Type': 'application/json', ...(auth ? { Authorization: 'Bearer ' + token() } : {}) },
      body: JSON.stringify(payload), signal: AbortSignal.timeout(2500) });
    const text = await res.text();
    const hdr = [...res.headers.keys()].filter((k) => !['date', 'etag', 'content-length', 'keep-alive', 'connection'].includes(k)).sort().join(',');
    return { status: res.status, text, hdr };
  } catch (e: any) { return { status: 0, text: 'NO RESPONSE (' + (e?.name ?? '?') + ')', hdr: '' }; }
}

async function cell(site: string, state: string, kind: string | null) {
  vi.resetModules();
  const prev = process.env.NODE_ENV; process.env.NODE_ENV = FMT;
  const { logger } = await import('../utils/logger');   // the logger reads NODE_ENV once, here (utils/logger.ts:11)
  process.env.NODE_ENV = prev;                          // index's enforceProductionConfig must not see production
  const mod: any = await import('../index');            // same module registry: index gets the logger built above
  const server: Server = await new Promise((r) => { const s = mod.default.listen(0, '127.0.0.1', () => r(s)); });
  const root = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
  h.storedBoom = h.lookupBoom = h.usageBoom = h.auditBoom = undefined; h.row = undefined; h.sql.length = 0;
  unhandled = 0; uncaught = 0; caught = [];
  let r: { status: number; text: string; hdr: string }; let keyMem: any = null;
  if (site === 'audit' || site === 'event') {
    h.auditBoom = kind ? KINDS[kind]() : undefined;
    lines.length = 0;
    r = site === 'audit'
      ? await call(root, 'POST', '/api/audit', { action: 'gate130', resourceType: 'probe', success: true }, true)
      : await call(root, 'POST', '/api/events', { eventType: 'gate130', severity: 'low', source: 'probe' }, true);
  } else {
    let key = 'sk_gate130_never_minted_' + crypto.randomUUID();
    if (state !== 'unknown') {
      const m = await call(root, 'POST', '/api/keys', { name: 'g130', organizationId: ORG_ID, tenantId: TENANT_ID, scopes: ['documents:read'] }, true);
      const d = JSON.parse(m.text).data; key = String(d.key);
      h.row = { id: d.id, organization_id: ORG_ID, tenant_id: TENANT_ID, name: 'g130', key_hash: crypto.createHash('sha256').update(key).digest('hex'),
        key_prefix: d.prefix, scopes: '["documents:read"]', rate_limit: 1000, rate_limit_window: 3600, usage_count: 0,
        is_active: state !== 'revoked', expires_at: state === 'expired' ? new Date(Date.now() - 60_000).toISOString() : null, created_at: new Date().toISOString() };
      if (site === 'lookup') mod.memApiKeys.delete(d.id);     // force the cache-miss branch
    }
    const v = kind ? KINDS[kind]() : undefined;
    if (site === 'stored') h.storedBoom = v; if (site === 'lookup') h.lookupBoom = v; if (site === 'usage') h.usageBoom = v;
    h.sql.length = 0; lines.length = 0;
    r = await call(root, 'POST', '/api/keys/validate', { key }, false);
    const k = [...mod.memApiKeys.values()].find((x: any) => x.keyHash === crypto.createHash('sha256').update(key).digest('hex'));
    keyMem = k ? { isActive: k.isActive, usageCount: k.usageCount } : null;
  }
  await new Promise((res) => setTimeout(res, 150));
  const before = lines.length;
  try { logger.info('gate130-canary'); } catch (e: any) { caught.push('canary threw ' + (e?.constructor?.name ?? '?')); }
  await new Promise((res) => setTimeout(res, 50));
  const canary = lines.slice(before).some((l) => l.includes('gate130-canary'));
  const logged = lines.filter((l) => /KS-1370: stored|DB fallback for api-key|DB save API key failed|DB save audit log failed|DB save event failed/.test(l))
    .map((l) => l.replace(/\u001b\[[0-9;]*m/g, '').replace(/^\S+ \S+ /, '').trim().slice(0, 200));
  let body: any = null; try { body = JSON.parse(r.text); } catch { body = r.text.slice(0, 80); }
  const rec = { fmt: FMT, site, state, kind: kind ?? 'none', status: r.status,
    answer: body?.data ? { valid: body.data.valid, reason: body.data.reason } : body?.error ?? (body?.success !== undefined ? { success: body.success } : body),
    bodyKeys: body && typeof body === 'object' ? Object.keys(body.data ?? body.error ?? {}).sort().join(',') : '', hdr: r.hdr, bodyLen: r.text.length,
    usageWrites: h.sql.filter((s) => /^UPDATE svc_api_keys SET last_used_at/i.test(s)).length,
    auditEventWrites: h.sql.filter((s) => /^INSERT INTO (audit_logs|svc_security_events)/i.test(s)).length,
    keyMem, logged, canary, unhandled, uncaught, caught };
  appendFileSync(OUT, JSON.stringify(rec) + '\n');
  await new Promise<void>((res) => server.close(() => res()));
}

const ALL = Object.keys(KINDS);
describe('gate130 probe', () => {
  for (const st of ['active', 'revoked', 'expired']) {
    it(`stored ${st} none`, async () => { await cell('stored', st, null); });
    for (const k of ALL) it(`stored ${st} ${k}`, async () => { await cell('stored', st, k); });
    for (const k of ALL) it(`usage ${st} ${k}`, async () => { await cell('usage', st, k); });
  }
  for (const st of ['unknown', 'active', 'revoked', 'expired']) {
    it(`lookup ${st} none`, async () => { await cell('lookup', st, null); });
    for (const k of ALL) it(`lookup ${st} ${k}`, async () => { await cell('lookup', st, k); });
  }
  for (const site of ['audit', 'event']) {
    it(`${site} none`, async () => { await cell(site, '-', null); });
    for (const k of ALL) it(`${site} ${k}`, async () => { await cell(site, '-', k); });
  }
});
