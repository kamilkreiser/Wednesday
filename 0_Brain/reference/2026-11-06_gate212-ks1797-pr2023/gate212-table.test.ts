// Gate 212 harness: the real POST /authorize route over real HTTP; only storage and collaborators doubled (the seat's seam).
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import type { Server } from 'node:http';
import { appendFileSync } from 'node:fs';
import express from 'express';

const h = vi.hoisted(() => ({ strict: false, userMfa: false, CONF: { id: 'a1', name: 'Conf', clientId: 'client-conf', appType: 'confidential', redirectUris: ['https://app.example.com/cb'], allowedScopes: ['openid', 'profile'] }, PUB: { id: 'a2', name: 'Pub', clientId: 'client-pub', appType: 'public', redirectUris: ['https://app.example.com/cb'], allowedScopes: ['openid', 'profile'] } }));

const silent = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: silent, createLogger: () => silent }));
vi.mock('../services/oauth', async (importOriginal) => {
  const real = await importOriginal<Record<string, unknown>>();
  return {
    ...real,
    createAuthorizationCode: vi.fn(async () => 'MINTED'),
    createApp: vi.fn(),
    // strict=false: permissive (String(id)), an upper bound. strict=true: a non-string id is not a row (what a text column compare would do; READ, not measured against pg).
    getAppByClientId: vi.fn(async (id: unknown) => {
      if (h.strict && typeof id !== 'string') return null;
      const s = String(id);
      return s === 'client-conf' ? h.CONF : s === 'client-pub' ? h.PUB : null;
    }),
    getAppById: vi.fn(),
  };
});
vi.mock('../services/accountLockout', () => ({
  isLockedOut: vi.fn(async () => false), recordFailure: vi.fn(async () => undefined),
  recordSuccess: vi.fn(async () => undefined), clearFailures: vi.fn(async () => undefined),
}));
vi.mock('../services/session', () => ({
  createSession: vi.fn(async () => ({ id: 's' })), getRedisClient: vi.fn(() => null),
  validateSession: vi.fn(async () => true), updateSessionActivity: vi.fn(async () => undefined),
}));
vi.mock('../services/password', () => ({ verifyPassword: vi.fn(async (p: unknown) => p === 'correct-horse'), hashPassword: vi.fn(async () => 'h') }));
vi.mock('../repositories/userRepo', () => ({
  getUserByEmail: vi.fn(async () => ({ id: 'user-1', email: 'u@secuura.local', status: 'ACTIVE', mfaEnabled: h.userMfa, passwordHash: 'h', role: 'OWNER', verificationLevel: 'BASIC' })),
  getUserById: vi.fn(async () => null), updateUser: vi.fn(async () => undefined),
  getPlatformAdmin: vi.fn(async () => null), reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
}));
vi.mock('../services/jwt', () => ({ generateTokenPair: vi.fn(() => ({ accessToken: 'a', refreshToken: 'r', expiresIn: 900 })) }));
vi.mock('../services/refreshDenylist', () => ({ isRefreshJtiDenylisted: vi.fn(async () => false) }));
vi.mock('../middleware/authenticate', () => ({ authenticate: () => (_r: unknown, _s: unknown, n: () => void) => n() }));
vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [] })) }));
vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));

let server: Server; let base: string;
let M: Record<string, ReturnType<typeof vi.fn>>;
beforeAll(async () => {
  const { oauthRouter } = await import('../routes/oauth');
  const o = (await import('../services/oauth')) as never as Record<string, ReturnType<typeof vi.fn>>;
  const p = (await import('../services/password')) as never as Record<string, ReturnType<typeof vi.fn>>;
  const u = (await import('../repositories/userRepo')) as never as Record<string, ReturnType<typeof vi.fn>>;
  const l = (await import('../services/accountLockout')) as never as Record<string, ReturnType<typeof vi.fn>>;
  M = { getApp: o.getAppByClientId, mint: o.createAuthorizationCode, verifyPw: p.verifyPassword, getUser: u.getUserByEmail, locked: l.isLockedOut, recFail: l.recordFailure };
  const app = express();
  app.use(express.json());
  app.use(express.urlencoded({ extended: true })); // index.ts
  app.use('/api/oauth', oauthRouter);
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', r); });
  const a = server.address();
  base = `http://127.0.0.1:${typeof a === 'object' && a ? a.port : 0}`;
});
afterAll(async () => { await new Promise<void>((r) => server.close(() => r())); });

const CB = 'https://app.example.com/cb';
const OUT = process.env.GATE_OUT as string;
const ABS = Symbol('absent');
const JSHAPES: [string, unknown][] = [['absent', ABS], ['xyz', 'xyz'], ['empty', ''], ['arr_ab', ['a', 'b']], ['arr_a', ['a']], ['arr_empty', []], ['obj_empty', {}], ['obj_ab', { a: 'b' }], ['null', null], ['0', 0], ['123', 123], ['true', true], ['false', false]];
const FSHAPES: [string, string | null][] = [['absent', null], ['xyz', 'F=xyz'], ['empty', 'F='], ['rep_ab', 'F=a&F=b'], ['br_a', 'F[]=a'], ['obj_ab', 'F[a]=b']];
const ACTIONS: (string | null)[] = ['deny', 'approve', null];
const CLIENTS = ['client-pub', 'client-conf', 'client-unreg'];
const CREDS = ['valid', 'wrong', 'missing'];
const MFAS: [string, boolean, string | null][] = [['u0_nocode', false, null], ['u0_code', false, '123456'], ['u1_nocode', true, null], ['u1_code', true, '123456']];

function credsBody(c: string): Record<string, string> {
  if (c === 'valid') return { email: 'u@secuura.local', password: 'correct-horse' };
  if (c === 'wrong') return { email: 'u@secuura.local', password: 'wrong' };
  return {};
}
const buf: string[] = [];
function flush() { if (buf.length) { appendFileSync(OUT, buf.join('')); buf.length = 0; } }

async function fire(key: Record<string, unknown>, init: RequestInit) {
  vi.clearAllMocks();
  const res = await fetch(`${base}/api/oauth/authorize`, { method: 'POST', redirect: 'manual', ...init });
  const text = await res.text();
  const mintArg = M.mint.mock.calls[0]?.[0];
  buf.push(JSON.stringify({ key, status: res.status, text, location: res.headers.get('location'), setCookie: res.headers.get('set-cookie'), ctype: res.headers.get('content-type'),
    calls: { getApp: M.getApp.mock.calls.length, getUser: M.getUser.mock.calls.length, verifyPw: M.verifyPw.mock.calls.length, locked: M.locked.mock.calls.length, recFail: M.recFail.mock.calls.length, mint: M.mint.mock.calls.length }, mintArg: mintArg ?? null, getAppArg: M.getApp.mock.calls[0]?.[0] ?? null }) + '\n');
  if (buf.length > 500) flush();
}

function sendJson(key: Record<string, unknown>, body: Record<string, unknown>, xhr = false) {
  return fire(key, { headers: { 'content-type': 'application/json', ...(xhr ? { 'x-requested-with': 'XMLHttpRequest' } : {}) }, body: JSON.stringify(body) });
}
function sendForm(key: Record<string, unknown>, parts: string[]) {
  return fire(key, { headers: { 'content-type': 'application/x-www-form-urlencoded' }, body: parts.filter(Boolean).join('&') });
}
function fbody(b: Record<string, string>) { return Object.entries(b).map(([k, v]) => `${k}=${encodeURIComponent(v)}`); }

describe('gate212', () => {
  it('Q3 table', async () => {
    for (const action of ACTIONS) for (const client of CLIENTS) for (const creds of CREDS) for (const [mfaName, userMfa, code] of MFAS) {
      h.userMfa = userMfa; h.strict = false;
      const common: Record<string, string> = { client_id: client, redirect_uri: CB, ...credsBody(creds) };
      if (action) common.action = action;
      if (code) common.mfaCode = code;
      const ctx = { action: action ?? 'absent', client, creds, mfa: mfaName };
      // state rows, with companion challenge absent / valid
      for (const comp of ['nochal', 'chal']) {
        const c2: Record<string, string> = comp === 'chal' ? { code_challenge: 'challenge-string', code_challenge_method: 'S256' } : {};
        for (const [n, v] of JSHAPES) { const b: Record<string, unknown> = { ...common, ...c2 }; if (v !== ABS) b.state = v; await sendJson({ q: 'state', enc: 'json', shape: n, comp, ...ctx }, b); }
        for (const [n, f] of FSHAPES) await sendForm({ q: 'state', enc: 'form', shape: n, comp, ...ctx }, [...fbody({ ...common, ...c2 }), f ? f.replaceAll('F', 'state') : '']);
      }
      // code_challenge rows, method S256 / absent, state string
      for (const m of ['S256', 'nomethod']) {
        const c2: Record<string, string> = { state: 'xyz', ...(m === 'S256' ? { code_challenge_method: 'S256' } : {}) };
        for (const [n, v] of JSHAPES) { const b: Record<string, unknown> = { ...common, ...c2 }; if (v !== ABS) b.code_challenge = v; await sendJson({ q: 'cc', enc: 'json', shape: n, comp: m, ...ctx }, b); }
        for (const [n, f] of FSHAPES) await sendForm({ q: 'cc', enc: 'form', shape: n, comp: m, ...ctx }, [...fbody({ ...common, ...c2 }), f ? f.replaceAll('F', 'code_challenge') : '']);
      }
      // both bad at once
      await sendJson({ q: 'both', enc: 'json', shape: 'arr+arr', comp: '-', ...ctx }, { ...common, state: ['a', 'b'], code_challenge: ['x', 'y'] });
      await sendJson({ q: 'both', enc: 'json', shape: 'null+str', comp: '-', ...ctx }, { ...common, state: null, code_challenge: 'c' });
    }
    // XHR (the consent page's own delivery), compact
    h.userMfa = false;
    for (const action of ACTIONS) for (const client of CLIENTS) {
      const common: Record<string, string> = { client_id: client, redirect_uri: CB, ...credsBody('valid') };
      if (action) common.action = action;
      for (const [n, v] of JSHAPES) {
        const b: Record<string, unknown> = { ...common, code_challenge: 'challenge-string' }; if (v !== ABS) b.state = v;
        await sendJson({ q: 'state_xhr', enc: 'json', shape: n, comp: 'chal', action: action ?? 'absent', client, creds: 'valid', mfa: 'u0_nocode' }, b, true);
      }
    }
    flush();
    expect(true).toBe(true);
  }, 900000);

  it('Q4 other params', async () => {
    h.userMfa = false;
    const SHAPES: [string, (s: string) => unknown][] = [['arr1', (s) => [s]], ['arr2', (s) => [s, s]], ['obj', (s) => ({ a: s })]];
    const baseVals: Record<string, string> = { client_id: 'client-conf', redirect_uri: CB, response_type: 'code', scope: 'openid', code_challenge_method: 'S256', email: 'u@secuura.local', password: 'correct-horse', mfaCode: '123456' };
    for (const strict of [false, true]) { h.strict = strict;
      for (const action of ['deny', 'approve', null] as (string | null)[]) for (const client of ['client-conf', 'client-pub']) {
        for (const param of ['client_id', 'redirect_uri', 'response_type', 'scope', 'code_challenge_method', 'email', 'password', 'mfaCode', 'action']) for (const [sn, f] of SHAPES) {
          const b: Record<string, unknown> = { client_id: client, redirect_uri: CB, email: baseVals.email, password: baseVals.password, state: 'xyz', code_challenge: 'challenge-string' };
          if (action) b.action = action;
          const val = param === 'action' ? (action ?? 'deny') : param === 'client_id' ? client : baseVals[param];
          b[param] = f(val);
          await sendJson({ q: 'q4', param, shape: sn, action: action ?? 'absent', client, strict }, b);
        }
        // scalars for controls
        await sendJson({ q: 'q4', param: 'control', shape: 'scalar', action: action ?? 'absent', client, strict }, { client_id: client, redirect_uri: CB, email: baseVals.email, password: baseVals.password, state: 'xyz', code_challenge: 'challenge-string', ...(action ? { action } : {}) });
      }
    }
    h.strict = false;
    flush();
    expect(true).toBe(true);
  }, 300000);
});
