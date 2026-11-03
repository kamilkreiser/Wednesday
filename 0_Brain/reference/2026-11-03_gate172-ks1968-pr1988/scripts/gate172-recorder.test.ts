/**
 * QA Gate 172 recorder (written by the gate; independent of the builder's ks1968 file). Copied into the clone's
 * src/__tests__ for a run and removed after. Drives the REAL routes/auth.ts register and reset-password handlers and the
 * REAL services/password.ts isPasswordBreached over HTTP on 127.0.0.1, with a STATEFUL in-memory user/token store.
 *
 * NO REAL BREACH SERVICE: globalThis.fetch is a forwarder. 127.0.0.1 goes to the fetch captured at load (the gate guard's),
 * the breach host goes to the stub below, anything else is recorded and refused. The process also runs under the gate's
 * outbound guard (NODE_OPTIONS --import), which blocks and counts that host at fetch, dns, net and tls.
 *
 * Every cell writes one JSON line to process.env.GATE_REC (observations, never a password).
 */
import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import { createHash } from 'crypto';
import { appendFileSync } from 'fs';
import express from 'express';

const MSG = 'This password has appeared in a data breach, choose another';
const SENT = 'G172SENTINELq9z';
const BREACHED = 'Gate172!Breached#Pass-77';
const CLEAN = 'Gate172!Clean#Unlisted-88';
const UNI = 'Gäte172!Brëached#Ünï-99';

const s = vi.hoisted(() => ({
  mode: 'normal' as string,
  calls: [] as Array<{ url: string; method: unknown; headers: Record<string, string>; body: unknown; hasSignal: boolean }>,
  foreign: [] as string[],
  logs: [] as string[],
  users: new Map<string, any>(),
  tokens: new Map<string, { userId: string; expiresAt: Date }>(),
  writes: [] as string[],
  hashCalls: 0,
  breachedSet: new Set<string>(),
  timeoutMs: -1,
  redisUp: true,
}));

vi.mock('../utils/logger', () => {
  const cap = (lv: string) => (...a: unknown[]) => { let t: string; try { t = JSON.stringify(a); } catch { t = String(a); } s.logs.push(`${lv} ${t}`); };
  const logger = { warn: cap('warn'), error: cap('error'), info: cap('info'), debug: cap('debug'), log: cap('log') };
  return { logger, createLogger: () => logger, validateEnv: () => undefined };
});
vi.mock('@secuura/shared/utils/logger', () => {
  const cap = (lv: string) => (...a: unknown[]) => { let t: string; try { t = JSON.stringify(a); } catch { t = String(a); } s.logs.push(`shared-${lv} ${t}`); };
  const logger = { warn: cap('warn'), error: cap('error'), info: cap('info'), debug: cap('debug'), log: cap('log') };
  return { logger, createLogger: () => logger };
});
vi.mock('../repositories/userRepo', () => {
  const byEmail = (e: string) => [...s.users.values()].find((u) => u.email === e.toLowerCase()) ?? null;
  const repo = {
    getUserByEmail: async (e: string) => byEmail(e),
    createUser: async (u: any) => { s.writes.push('createUser'); const ex = byEmail(u.email); s.users.set(ex ? ex.id : u.id, { ...(ex ?? {}), ...u, status: ex ? ex.status : u.status }); return u; },
    updateUserOrThrow: async (id: string, patch: any) => { s.writes.push('updateUserOrThrow'); const u = s.users.get(id); if (!u) throw new Error('no user'); s.users.set(id, { ...u, ...patch }); return s.users.get(id); },
    updateUser: async (id: string, patch: any) => { s.writes.push('updateUser'); const u = s.users.get(id); if (u) s.users.set(id, { ...u, ...patch }); return u ?? null; },
    storeEmailToken: async () => { s.writes.push('storeEmailToken'); },
    getResetToken: async (h: string) => s.tokens.get(h) ?? null,
    consumeResetToken: async (h: string) => { s.writes.push('consumeResetToken'); s.tokens.delete(h); },
    getUserByIdPreAuth: async (id: string) => s.users.get(id) ?? null,
    seedDemoUsers: async () => undefined,
  };
  return { default: repo, __esModule: true, ...repo };
});
vi.mock('../services/password', async (orig) => {
  const real = await orig<Record<string, unknown>>();
  return { ...real, hashPassword: async (pw: string) => { s.hashCalls += 1; return 'gatehash:' + createHash('sha256').update(pw).digest('hex').slice(0, 8); } };
});
vi.mock('../services/jwt', async (orig) => ({ ...(await orig<Record<string, unknown>>()), generateTokenPair: () => ({ accessToken: 'a', refreshToken: 'r', expiresIn: 900 }) }));
vi.mock('../services/session', () => ({
  createSession: async () => { s.writes.push('createSession'); return { id: 'sess-172' }; },
  revokeAllUserSessions: async () => { s.writes.push('revokeAllUserSessions'); return 0; },
  isRedisAvailable: () => s.redisUp,
  revokeSession: async () => undefined, getSession: async () => null, rotateSessionRefreshToken: async () => null,
}));
vi.mock('../services/email', () => ({ sendVerificationEmail: async () => { s.writes.push('sendVerificationEmail'); return true; }, sendPasswordResetEmail: async () => true }));
vi.mock('../events', () => ({ publishEvent: async () => { s.writes.push('publishEvent'); }, EventTypes: { USER_REGISTERED: 'user.registered' } }));
vi.mock('../db', () => ({ isDbAvailable: () => false, query: async () => ({ rows: [], rowCount: 0 }) }));

import { authRoutes } from '../routes/auth';
import { errorHandler } from '../middleware/errorHandler';
import * as password from '../services/password';

const sha1 = (x: string) => createHash('sha1').update(x).digest('hex').toUpperCase();
const sha256 = (x: string) => createHash('sha256').update(x).digest('hex');
const loadFetch = globalThis.fetch;
const savedEnv = process.env.HIBP_ENABLED;
let server: Server; let base = '';
const REC = process.env.GATE_REC;
const rec = (o: Record<string, unknown>) => { if (REC) appendFileSync(REC, JSON.stringify(o) + '\n'); };

class SentinelNamedError extends Error {}
Object.defineProperty(SentinelNamedError, 'name', { value: 'Err' + SENT });

function stub(url: string, init: any): Promise<Response> | Response {
  const m = s.mode;
  if (m === 'throw') throw new Error('boom ' + SENT, { cause: new Error('cause ' + SENT) });
  if (m === 'throwPlain') throw ('plain ' + SENT);
  if (m === 'throwNamed') throw new SentinelNamedError('named ' + SENT);
  if (m === 'reject') return Promise.reject(Object.assign(new TypeError('fetch failed ' + SENT), { code: SENT }));
  if (m.startsWith('status')) return new Response('down ' + SENT, { status: Number(m.slice(6)) });
  if (m === 'timeout') {
    const t0 = Date.now();
    return new Promise((_, rej) => {
      const sig: AbortSignal | undefined = init?.signal;
      if (!sig) return; // never settles: would hang the cell, which then fails on the vitest timeout
      sig.addEventListener('abort', () => { s.timeoutMs = Date.now() - t0; rej(sig.reason); });
    });
  }
  if (m === 'bodyThrows') return { ok: true, status: 200, text: async () => { throw new Error('body ' + SENT); } } as unknown as Response;
  const prefix = url.slice(url.lastIndexOf('/') + 1);
  const lines = ['00000000000000000000000000000000000:0'];
  for (const pw of s.breachedSet) { const h = sha1(pw); if (h.slice(0, 5) === prefix) lines.push(`${h.slice(5)}:42`); }
  return new Response(lines.join('\r\n'), { status: 200 });
}

beforeAll(async () => {
  globalThis.fetch = (async (input: any, init?: any) => {
    const url = typeof input === 'string' ? input : input?.url ?? String(input);
    const u = new URL(url);
    if (u.hostname === 'api.pwnedpasswords.com') {
      const hd: Record<string, string> = {};
      new Headers(init?.headers ?? {}).forEach((v, k) => { hd[k] = v; });
      s.calls.push({ url, method: init?.method, headers: hd, body: init?.body, hasSignal: !!init?.signal });
      return stub(url, init);
    }
    if (u.hostname === '127.0.0.1') return loadFetch(input, init);
    s.foreign.push(u.hostname); throw new Error('gate172: unexpected host');
  }) as typeof fetch;
  const app = express(); app.use(express.json()); app.use('/api/auth', authRoutes); app.use(errorHandler);
  server = app.listen(0, '127.0.0.1'); await new Promise<void>((r) => server.once('listening', () => r()));
  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(async () => {
  globalThis.fetch = loadFetch;
  if (savedEnv === undefined) delete process.env.HIBP_ENABLED; else process.env.HIBP_ENABLED = savedEnv;
  await new Promise<void>((r) => server.close(() => r()));
});
beforeEach(() => {
  s.mode = 'normal'; s.calls = []; s.foreign = []; s.logs = []; s.users.clear(); s.tokens.clear(); s.writes = []; s.hashCalls = 0;
  s.breachedSet = new Set([BREACHED, UNI]); s.timeoutMs = -1; s.redisUp = true;
  delete process.env.HIBP_ENABLED;
});

async function post(path: string, body: unknown) {
  const r = await loadFetch(base + '/api/auth' + path, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) });
  const text = await r.text(); let json: any = {}; try { json = JSON.parse(text); } catch { /* */ }
  return { status: r.status, text, json };
}
const USER = { id: 'u-172', email: 'g172@example.test', status: 'ACTIVE', role: 'OWNER', passwordHash: 'old-hash' };
function seedReset(tok = 'tok-172', ms = 3_600_000) { s.users.set(USER.id, { ...USER }); s.tokens.set(sha256(tok), { userId: USER.id, expiresAt: new Date(Date.now() + ms) }); return tok; }
const reg = (pw: string, email = 'new172@example.test') => post('/register', { email, password: pw, name: 'Ann Lee' });
const reset = (pw: string, token = 'tok-172') => post('/reset-password', { token, password: pw });
type Route = 'register' | 'reset';
async function drive(route: Route, pw: string) { if (route === 'reset') { seedReset(); return reset(pw); } return reg(pw); }
const snap = (cell: string, route: string, r: { status: number; text: string; json: any }, extra: Record<string, unknown> = {}) => {
  const o = { cell, route, status: r.status, code: r.json?.error?.code, message: r.json?.error?.message, details: r.json?.error?.details, lookups: s.calls.length, hashCalls: s.hashCalls, writes: [...s.writes], foreign: s.foreign.length, ...extra };
  rec(o); return o;
};
const ROUTES: Route[] = ['register', 'reset'];
const OK: Record<Route, number> = { register: 201, reset: 200 };

describe('G172 Q1 refusal and acceptance', () => {
  it.each(ROUTES)('Q1 %s: breached refused 422 with ONLY Kam\'s sentence, nothing hashed or written', async (route) => {
    const r = await drive(route, BREACHED);
    const o = snap('Q1-breached', route, r, { body: r.text });
    expect(o.status).toBe(422);
    expect(r.json.success).toBe(false);
    expect(o.code).toBe('VALIDATION_ERROR');
    expect(o.message).toBe(MSG);
    expect(o.details).toEqual([{ code: 'custom', path: ['password'], message: MSG }]);
    expect(Object.keys(r.json.error).sort()).toEqual(['code', 'details', 'message']);
    expect(r.text).not.toContain(BREACHED);
    expect(o.hashCalls).toBe(0);
    expect(o.writes).toEqual([]);
    expect(o.lookups).toBe(1);
  });
  it.each(ROUTES)('Q1 %s: a breached UNICODE password is refused too (UTF-8 SHA-1)', async (route) => {
    const r = await drive(route, UNI);
    snap('Q1-unicode', route, r);
    expect(r.status).toBe(422);
    expect(r.json.error?.message).toBe(MSG);
  });
  it.each(ROUTES)('Q1 %s: a clean password is accepted after exactly one lookup', async (route) => {
    const r = await drive(route, CLEAN);
    const o = snap('Q1-clean', route, r);
    expect(o.status).toBe(OK[route]);
    expect(o.lookups).toBe(1);
    expect(o.hashCalls).toBe(1);
  });
  it('Q1 register: the 422 bytes are identical across register and reset', async () => {
    const a = await drive('register', BREACHED); s.users.clear(); s.calls = [];
    const b = await drive('reset', BREACHED);
    rec({ cell: 'Q1-bytes', register: a.text, reset: b.text, same: a.text === b.text });
    expect(a.text).toBe(b.text);
  });
});

describe('G172 Q2 k-anonymity', () => {
  for (const route of ROUTES) for (const [label, pw] of [['breached', BREACHED], ['clean', CLEAN], ['unicode', UNI]] as const) {
    it(`Q2 ${route} ${label}: only /range/ + 5 hex leaves; no password, full hash or suffix in URL, headers or body`, async () => {
      await drive(route, pw);
      expect(s.calls).toHaveLength(1);
      const c = s.calls[0]; const u = new URL(c.url); const full = sha1(pw);
      const sent = c.url + '\n' + JSON.stringify(c.headers) + '\n' + JSON.stringify(c.body ?? null) + '\n' + String(c.method ?? '');
      const leaks = [pw, full, full.slice(5), full.toLowerCase(), full.slice(5).toLowerCase(), full.slice(0, 6), encodeURIComponent(pw)].filter((l) => sent.includes(l)).length;
      rec({ cell: 'Q2', route, label, host: u.hostname, protocol: u.protocol, pathShape: u.pathname.replace(/[0-9A-F]/g, 'H'), search: u.search, method: c.method ?? null, body: c.body ?? null, headerNames: Object.keys(c.headers), hasSignal: c.hasSignal, leaks });
      expect(u.protocol).toBe('https:');
      expect(u.hostname).toBe('api.pwnedpasswords.com');
      expect(u.pathname).toMatch(/^\/range\/[0-9A-F]{5}$/);
      expect(u.pathname).toBe('/range/' + full.slice(0, 5));
      expect(u.search).toBe('');
      expect(c.body ?? null).toBeNull();
      expect(leaks).toBe(0);
    });
  }
});

describe('G172 Q3 outage allows, switch', () => {
  const OUT = ['throw', 'throwPlain', 'reject', 'status404', 'status429', 'status500', 'status503', 'bodyThrows'];
  for (const route of ROUTES) for (const m of OUT) {
    it(`Q3 ${route} ${m}: a breached password is ALLOWED`, async () => {
      s.mode = m;
      const r = await drive(route, BREACHED);
      const o = snap('Q3-outage', route, r, { mode: m });
      expect(o.status).toBe(OK[route]);
      expect(o.lookups).toBe(1);
    });
  }
  for (const route of ROUTES) it(`Q3 ${route} timeout: the 2 s abort fires and the password is ALLOWED`, async () => {
    s.mode = 'timeout';
    const t0 = Date.now();
    const r = await drive(route, BREACHED);
    const o = snap('Q3-timeout', route, r, { abortAfterMs: s.timeoutMs, wallMs: Date.now() - t0 });
    expect(o.status).toBe(OK[route]);
    expect(s.timeoutMs).toBeGreaterThanOrEqual(1900);
    expect(s.timeoutMs).toBeLessThan(3000);
  }, 10_000);
  for (const route of ROUTES) for (const v of ['false', 'FALSE', '0', '', 'true', 'off']) {
    it(`Q3 ${route} HIBP_ENABLED=${JSON.stringify(v)}: lookup only unless exactly 'false'`, async () => {
      process.env.HIBP_ENABLED = v;
      const r = await drive(route, BREACHED);
      const o = snap('Q3-switch', route, r, { value: v });
      if (v === 'false') { expect(o.lookups).toBe(0); expect(o.status).toBe(OK[route]); }
      else { expect(o.lookups).toBe(1); expect(o.status).toBe(422); }
    });
  }
  const SETUP = '../../vitest.setup';
  it('Q3 setup: unset becomes "false"', async () => {
    delete process.env.HIBP_ENABLED; vi.resetModules(); await import(/* @vite-ignore */ SETUP);
    rec({ cell: 'Q3-setup', given: 'unset', after: process.env.HIBP_ENABLED ?? null });
    expect(process.env.HIBP_ENABLED).toBe('false');
  });
  for (const v of ['true', '', 'FALSE']) it(`Q3 setup: explicit ${JSON.stringify(v)} is left alone`, async () => {
    process.env.HIBP_ENABLED = v; vi.resetModules(); await import(/* @vite-ignore */ SETUP);
    rec({ cell: 'Q3-setup', given: v, after: process.env.HIBP_ENABLED ?? null });
    expect(process.env.HIBP_ENABLED).toBe(v);
  });
});

describe('G172 Q4 reset ordering and the store after', () => {
  it('Q4 invalid token: 404 and no lookup', async () => {
    s.users.set(USER.id, { ...USER });
    const r = await reset(BREACHED, 'no-such-token'); const o = snap('Q4-invalid', 'reset', r);
    expect(o.status).toBe(404); expect(o.lookups).toBe(0); expect(o.hashCalls).toBe(0);
  });
  it('Q4 expired token: 400 and no lookup', async () => {
    seedReset('tok-172', -1000);
    const r = await reset(BREACHED); const o = snap('Q4-expired', 'reset', r);
    expect(o.status).toBe(400); expect(o.lookups).toBe(0);
  });
  it('Q4 token for a missing user: 404 and no lookup', async () => {
    s.tokens.set(sha256('tok-172'), { userId: 'gone', expiresAt: new Date(Date.now() + 60_000) });
    const r = await reset(BREACHED); const o = snap('Q4-nouser', 'reset', r);
    expect(o.status).toBe(404); expect(o.lookups).toBe(0);
  });
  it('Q4 refused reset: token UNCONSUMED, hash unchanged, nothing written; the same token then works for a clean password', async () => {
    const tok = seedReset();
    const r1 = await reset(BREACHED);
    const after1 = { tokenPresent: s.tokens.has(sha256(tok)), hash: s.users.get(USER.id).passwordHash, writes: [...s.writes], hashCalls: s.hashCalls };
    s.calls = [];
    const r2 = await reset(CLEAN);
    const after2 = { tokenPresent: s.tokens.has(sha256(tok)), hashChanged: s.users.get(USER.id).passwordHash !== 'old-hash' };
    rec({ cell: 'Q4-store', s1: r1.status, after1, s2: r2.status, after2 });
    expect(r1.status).toBe(422);
    expect(after1).toEqual({ tokenPresent: true, hash: 'old-hash', writes: [], hashCalls: 0 });
    expect(r2.status).toBe(200);
    expect(after2).toEqual({ tokenPresent: false, hashChanged: true });
  });
  it('Q4 breached with the session store down: 422 (breach first), token unconsumed', async () => {
    const tok = seedReset(); s.redisUp = false;
    const r = await reset(BREACHED); const o = snap('Q4-redisdown', 'reset', r, { tokenPresent: s.tokens.has(sha256(tok)) });
    expect(o.status).toBe(422); expect(s.tokens.has(sha256(tok))).toBe(true);
  });
});

describe('G172 Q5 register ordering', () => {
  it.each(ROUTES)('Q5 %s: weak (but schema-valid) password: the strength 422 and no lookup', async (route) => {
    const r = await drive(route, 'weakpass'); const o = snap('Q5-weak', route, r);
    expect(o.status).toBe(422); expect(o.message).toBe('Password is too weak'); expect(o.lookups).toBe(0);
  });
  it.each(ROUTES)('Q5 %s: schema-invalid (7 chars): refused and no lookup', async (route) => {
    const r = await drive(route, 'Ab1!xyz'); const o = snap('Q5-schema', route, r);
    expect(o.status).toBeGreaterThanOrEqual(400); expect(o.lookups).toBe(0);
  });
  it('Q5 register: an ACTIVE email: 409 and no lookup', async () => {
    s.users.set('x', { id: 'x', email: 'new172@example.test', status: 'ACTIVE' });
    const r = await reg(BREACHED); const o = snap('Q5-conflict', 'register', r);
    expect(o.status).toBe(409); expect(o.lookups).toBe(0);
  });
  it('Q5 register: a client role field: 422 role message and no lookup', async () => {
    const r = await post('/register', { email: 'new172@example.test', password: BREACHED, role: 'SYSTEM_ADMIN' }); const o = snap('Q5-role', 'register', r);
    expect(o.status).toBe(422); expect(o.lookups).toBe(0);
  });
  it('Q5 register: claiming an INVITED stub with a breached password: 422 and the stub unchanged', async () => {
    s.users.set('stub', { id: 'stub', email: 'new172@example.test', status: 'INVITED', passwordHash: null });
    const r = await reg(BREACHED); const o = snap('Q5-stub', 'register', r, { stub: s.users.get('stub') });
    expect(o.status).toBe(422); expect(s.users.get('stub')).toEqual({ id: 'stub', email: 'new172@example.test', status: 'INVITED', passwordHash: null }); expect(o.writes).toEqual([]);
  });
});

describe('G172 Q6 logging', () => {
  for (const route of ROUTES) for (const m of ['throw', 'throwPlain', 'reject', 'status503', 'bodyThrows']) {
    it(`Q6 ${route} ${m}: the sentinel reaches no log line and no body`, async () => {
      s.mode = m;
      const spies = (['log', 'warn', 'error', 'info', 'debug'] as const).map((k) => vi.spyOn(console, k));
      const r = await drive(route, BREACHED);
      const consoleText = JSON.stringify(spies.map((sp) => sp.mock.calls)); spies.forEach((sp) => sp.mockRestore());
      const hibp = s.logs.filter((l) => l.includes('HIBP'));
      rec({ cell: 'Q6', route, mode: m, status: r.status, hibpLines: hibp, sentinelInLogs: s.logs.join('\n').includes(SENT), sentinelInConsole: consoleText.includes(SENT), sentinelInBody: r.text.includes(SENT) });
      expect(s.logs.join('\n')).not.toContain(SENT);
      expect(consoleText).not.toContain(SENT);
      expect(r.text).not.toContain(SENT);
      expect(hibp).toHaveLength(1);
    });
  }
  it('Q6 INFO: a thrown value whose CLASS NAME carries the sentinel (logged type = constructor name, by design)', async () => {
    s.mode = 'throwNamed';
    expect(await password.isPasswordBreached(BREACHED)).toBe(false);
    rec({ cell: 'Q6-named', line: s.logs.filter((l) => l.includes('HIBP')), sentinelInLogs: s.logs.join('\n').includes(SENT) });
  });
});
