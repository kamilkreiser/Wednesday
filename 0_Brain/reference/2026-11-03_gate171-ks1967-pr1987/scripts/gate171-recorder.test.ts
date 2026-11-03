/**
 * Gate 171 recorder (QA, not product). Drives the REAL accountLockout + passwordLoginGate + routers
 * (auth, oauth, wallet) over HTTP against seven session-store states and records every observable
 * per cell to the JSON file named by G171_OUT. No assertions about the fix: the comparator decides.
 * Written by gate 171; independent of the builder's ks1967 test (own store doubles, own doors).
 */
import { it, beforeAll, afterAll, vi } from 'vitest';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import express from 'express';
import fs from 'fs';

const LOCK_SENT = 'G171LOCKSENTINEL';
const SESS_SENT = 'G171SESSSENTINEL';
const RIGHT = 'g171-Right-pw!';
const WRONG = 'g171-Wrong-pw!';
const WALLET = 'addr_test1qrjjw7rrks796exampleaddress0000000000000000000000';
const CHALLENGE_ID = '11111111-2222-4333-8444-555555555555';

type Mode = 'connected' | 'slow' | 'null' | 'throwAll' | 'maxRetries' | 'readsThrow' | 'writesThrow';

const S = vi.hoisted(() => ({
  store: null as unknown,
  mode: 'connected' as string,
  admin: false,
  mfa: false,
  wallet: false,
  variant: '' as string,
  verifyCalls: 0,
  totpCalls: 0,
  cip8Calls: 0,
  createSessionCalls: 0,
  sessionsMinted: 0,
  codesMinted: 0,
  tokenPairs: 0,
  challengeDeletes: 0,
  logs: [] as string[],
  sessErr: null as null | (() => Error),
}));

vi.mock('../utils/logger', () => {
  const cap = (l: string) => vi.fn((...a: unknown[]) => { let s: string; try { s = JSON.stringify(a); } catch { s = String(a); } S.logs.push(`${l} ${s}`); });
  const logger = { warn: cap('warn'), error: cap('error'), info: cap('info'), debug: cap('debug'), log: cap('log') };
  return { logger, createLogger: () => logger, validateEnv: () => undefined };
});
vi.mock('@secuura/shared/utils/logger', () => {
  const cap = (l: string) => vi.fn((...a: unknown[]) => { let s: string; try { s = JSON.stringify(a); } catch { s = String(a); } S.logs.push(`${l} ${s}`); });
  const logger = { warn: cap('warn'), error: cap('error'), info: cap('info'), debug: cap('debug'), log: cap('log') };
  return { logger, createLogger: () => logger };
});

// session.ts stand-in: getRedisClient mirrors `redisAvailable ? redis : null`; createSession mirrors the
// real function's dependence on the same store (it throws "Redis is not available" with no client, and
// its first command is a read then writes, so any store fault rejects it).
vi.mock('../services/session', () => ({
  getRedisClient: vi.fn(() => S.store),
  isRedisAvailable: vi.fn(() => S.store !== null),
  createSession: vi.fn(async () => {
    S.createSessionCalls++;
    if (S.sessErr) throw S.sessErr();
    S.sessionsMinted++;
    return { id: 'sess-g171' };
  }),
  revokeSession: vi.fn(async () => undefined),
  getSession: vi.fn(async () => null),
  rotateSessionRefreshToken: vi.fn(async () => undefined),
}));

vi.mock('../services/password', () => ({
  verifyPassword: vi.fn(async (pw: string) => { S.verifyCalls++; return pw === RIGHT; }),
  hashPassword: vi.fn(async () => '$argon2id$stub'),
  checkPasswordStrength: vi.fn(() => ({ isStrong: true, score: 4, feedback: [] })),
  generateResetToken: vi.fn(() => 'tok'),
  shouldRehashAfterVerify: vi.fn(() => false),
}));
vi.mock('../services/totp', () => ({
  verifyTotpCode: vi.fn((_s: string, c: string) => { S.totpCalls++; return c === '123456'; }),
  verifyBackupCode: vi.fn(async (c: string) => (S.variant === 'race' && c === 'ABCD1234' ? { valid: true, index: 0 } : { valid: false, index: -1 })),
}));
vi.mock('../services/jwt', () => ({
  generateTokenPair: vi.fn(() => { S.tokenPairs++; return { accessToken: 'A', refreshToken: 'R', expiresIn: 900 }; }),
  verifyRefreshToken: vi.fn(() => ({})),
  decodeToken: vi.fn(() => ({})),
}));
vi.mock('../utils/cip8', () => ({
  verifyCIP8Signature: vi.fn(async (_a: string, _c: string, sig: string) => { S.cip8Calls++; return sig === RIGHT ? { valid: true } : { valid: false, error: 'Invalid signature' }; }),
  isValidCardanoAddress: vi.fn(() => true),
}));
vi.mock('../services/oauth', () => ({
  createAuthorizationCode: vi.fn(async () => { S.codesMinted++; return 'MINTEDCODE'; }),
  createApp: vi.fn(), getAppById: vi.fn(), listApps: vi.fn(), updateApp: vi.fn(), rotateSecret: vi.fn(), exchangeCode: vi.fn(),
  getAppByClientId: vi.fn(async () => ({ id: 'app-1', name: 'App', clientId: 'client-1', appType: 'confidential', redirectUris: ['https://app.example.com/cb'], allowedScopes: ['openid'] })),
  validateScopes: vi.fn((r: string[]) => r ?? []),
  parseScopeString: vi.fn(() => []),
  AVAILABLE_SCOPES: {},
}));
const WALLET_EMAIL = `${WALLET.slice(0, 8)}...@wallet.local`;
vi.mock('../repositories/userRepo', () => {
  const user = () => ({
    id: S.wallet ? 'wallet-user-1' : 'user-1', email: S.wallet ? WALLET_EMAIL : 'victim@example.com', walletAddress: S.wallet ? WALLET : undefined,
    passwordHash: '$argon2id$stub', role: 'ISSUER', status: 'ACTIVE', verificationLevel: 'BASIC', tenantId: 't-1',
    mfaEnabled: S.mfa, mfaSecret: S.mfa ? 'JBSWY3DPEHPK3PXP' : undefined, mfaBackupCodes: S.variant === 'race' ? ['stored-hash-1'] : null,
    ...(S.variant === 'suspended' ? { status: 'SUSPENDED' } : {}), ...(S.variant === 'sso' ? { passwordHash: undefined } : {}),
  });
  return {
    getPlatformAdmin: vi.fn(async () => (S.admin ? { id: 'admin-1', email: 'victim@example.com', passwordHash: '$argon2id$stub', name: 'Admin', mfaEnabled: S.mfa, mfaSecret: S.mfa ? 'JBSWY3DPEHPK3PXP' : null, role: 'SYSTEM_ADMIN' } : null)),
    getUserByEmail: vi.fn(async () => (S.variant === 'unknown' ? null : user())),
    getUserByIdPreAuth: vi.fn(async () => user()),
    createUser: vi.fn(async (u: unknown) => u),
    updateUser: vi.fn(async () => null),
    updateUserOrThrow: vi.fn(async () => ({ id: 'user-1' })),
    consumeBackupCode: vi.fn(async () => ({ consumed: S.variant !== 'race' })),
    reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
    reencryptPlatformAdminMfaSecretIfLegacy: vi.fn(async () => undefined),
    updatePlatformAdminPassword: vi.fn(async () => undefined),
    seedDemoUsers: vi.fn(async () => undefined),
  };
});
vi.mock('../db', () => ({
  query: vi.fn(async (text: string) => {
    if (text.includes('auth_find_user_by_wallet')) return { rows: [{ id: 'wallet-user-1' }] };
    if (text.includes('wallet_auth_challenges') && text.trim().toUpperCase().startsWith('SELECT')) {
      return { rows: [{ id: CHALLENGE_ID, wallet_address: WALLET, challenge: 'sign-this', nonce: CHALLENGE_ID, created_at: new Date(), expires_at: new Date(Date.now() + 600000), used: false }] };
    }
    if (text.includes('wallet_auth_challenges') && /^\s*(DELETE|UPDATE)/i.test(text) && !text.includes('expires_at <')) S.challengeDeletes++;
    return { rows: [] };
  }),
}));
vi.mock('../services/refreshDenylist', () => ({ isRefreshJtiDenylisted: vi.fn(async () => false) }));
vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
vi.mock('../services/email', () => ({ sendVerificationEmail: vi.fn(async () => undefined), sendPasswordResetEmail: vi.fn(async () => undefined) }));
vi.mock('../middleware/authenticate', () => {
  const p = () => (_r: unknown, _s: unknown, n: () => void) => n();
  return { authenticate: p, authenticateAccessOrConnector: p, requireRole: p, requireVerificationLevel: p, requireOwnership: p, requireSameOrganization: p };
});

/** One store double for every state. Counts ATTEMPTS per op, whatever the outcome. */
class Store {
  ops: Record<string, number> = { get: 0, set: 0, incr: 0, expire: 0, del: 0 };
  constructor(private mode: Mode, private locked: boolean, private mk: () => Error) {}
  private async step(op: string, isWrite: boolean) {
    this.ops[op]++;
    if (this.mode === 'slow') await new Promise((r) => setTimeout(r, 40));
    if (this.mode === 'throwAll' || this.mode === 'maxRetries') throw this.mk();
    if (this.mode === 'readsThrow' && !isWrite) throw this.mk();
    if (this.mode === 'writesThrow' && isWrite) throw this.mk();
  }
  async get(k: string) { await this.step('get', false); return k.startsWith('lockout:locked:') && this.locked ? '1' : null; }
  async set() { await this.step('set', true); return 'OK'; }
  async incr() { await this.step('incr', true); return 1; }
  async expire() { await this.step('expire', true); return 1; }
  async del(...k: string[]) { await this.step('del', true); return k.length; }
}

let MaxRetries: new (n: number) => Error;
function storeError(mode: Mode, sentinel: string): () => Error {
  if (mode === 'maxRetries') return () => { const e = new MaxRetries(3); e.message = `${e.message} ${sentinel}`; return e; };
  if (mode === 'writesThrow') return () => { const e = new Error(`OOM command not allowed when used memory > 'maxmemory'. ${sentinel}`); e.name = 'ReplyError'; return e; };
  return () => new Error(`${sentinel} store fault`);
}

function arrange(mode: Mode, locked: boolean): Store | null {
  S.mode = mode;
  if (mode === 'null') { S.store = null; S.sessErr = () => new Error('Redis is not available — cannot create session'); return null; }
  const st = new Store(mode, locked, storeError(mode, LOCK_SENT));
  S.store = st;
  S.sessErr = mode === 'connected' || mode === 'slow' ? null : storeError(mode, SESS_SENT);
  return st;
}

let authBase = '', oauthBase = '', walletBase = '';
const servers: Server[] = [];
let gate: (u: never, i: never) => Promise<unknown>;

beforeAll(async () => {
  ({ MaxRetriesPerRequestError: MaxRetries } = (await import('ioredis/built/errors/index.js')) as never);
  const { authRoutes } = await import('../routes/auth');
  const { oauthRouter } = await import('../routes/oauth');
  const { walletRoutes } = await import('../routes/wallet');
  const { errorHandler } = await import('../middleware/errorHandler');
  ({ assertAccountMayReceiveCredential: gate } = (await import('../services/passwordLoginGate')) as never);
  const mk = async (mount: string, r: express.Router) => {
    const a = express(); a.use(express.json()); a.use(mount, r); a.use(errorHandler);
    const s = await new Promise<Server>((res) => { const x = a.listen(0, '127.0.0.1', () => res(x)); });
    servers.push(s);
    return `http://127.0.0.1:${(s.address() as AddressInfo).port}`;
  };
  authBase = await mk('/api/auth', authRoutes);
  oauthBase = await mk('/api/oauth', oauthRouter);
  walletBase = await mk('/api/auth/wallet', walletRoutes);
}, 120000);

afterAll(async () => { for (const s of servers) await new Promise<void>((r) => s.close(() => r())); });

type Door = 'login-unknown' | 'login-suspended' | 'login-sso' | 'login-backup-race' | 'login-user' | 'login-user-mfa' | 'login-admin' | 'login-admin-mfa' | 'authorize' | 'authorize-mfa' | 'wallet-verify' | 'wallet-authenticate' | 'wallet-mfa' | 'credential-gate' | 'credential-gate-mfa';
const DOORS: Door[] = ['login-unknown', 'login-suspended', 'login-sso', 'login-backup-race', 'login-user', 'login-user-mfa', 'login-admin', 'login-admin-mfa', 'authorize', 'authorize-mfa', 'wallet-verify', 'wallet-authenticate', 'wallet-mfa', 'credential-gate', 'credential-gate-mfa'];
const MODES: Mode[] = ['connected', 'slow', 'null', 'throwAll', 'maxRetries', 'readsThrow', 'writesThrow'];

async function drive(door: Door, cred: string) {
  S.admin = door.startsWith('login-admin');
  S.variant = ({ 'login-unknown': 'unknown', 'login-suspended': 'suspended', 'login-sso': 'sso', 'login-backup-race': 'race' } as Record<string, string>)[door] ?? '';
  S.mfa = door.endsWith('-mfa') || S.variant === 'race';
  S.wallet = door.startsWith('wallet') ;
  // For an -mfa door the PASSWORD (or signature) is right and the second factor is what is right or wrong.
  const first = S.mfa ? RIGHT : cred;
  const mfaCode = S.variant === 'race' ? (cred === RIGHT ? 'ABCD1234' : 'ZZZZ9999') : S.mfa ? (cred === RIGHT ? '123456' : '654321') : undefined;
  const t0 = performance.now();
  let status = 0, body = '', headers: Record<string, string | null> = {}, thrownStatus: unknown = null, result: unknown = null;
  if (door.startsWith('credential-gate')) {
    try { result = await gate({ id: 'user-1', email: 'victim@example.com', status: 'ACTIVE', mfaEnabled: S.mfa, mfaSecret: S.mfa ? 'JBSWY3DPEHPK3PXP' : undefined, mfaBackupCodes: null } as never, { mfaCode, sourceIp: '127.0.0.1', route: 'g171' } as never); }
    catch (e) { thrownStatus = (e as { statusCode?: unknown })?.statusCode ?? 'non-AppError'; body = String((e as Error)?.message); }
  } else {
    let url: string; let payload: Record<string, unknown>;
    if (door.startsWith('authorize')) { url = `${oauthBase}/api/oauth/authorize`; payload = { email: 'victim@example.com', password: first, client_id: 'client-1', redirect_uri: 'https://app.example.com/cb', ...(mfaCode ? { mfaCode } : {}) }; }
    else if (door.startsWith('wallet')) { url = `${walletBase}/api/auth/wallet/${door === 'wallet-authenticate' ? 'authenticate' : 'verify'}`; payload = { challengeId: CHALLENGE_ID, walletAddress: WALLET, signature: first, key: 'k', ...(mfaCode ? { mfaCode } : {}) }; }
    else { url = `${authBase}/api/auth/login`; payload = { email: 'victim@example.com', password: first, ...(mfaCode ? { mfaCode } : {}) }; }
    const res = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json' }, redirect: 'manual', body: JSON.stringify(payload) });
    status = res.status; body = await res.text();
    for (const h of ['content-type', 'location', 'retry-after', 'cache-control']) headers[h] = res.headers.get(h);
    headers['set-cookie'] = res.headers.get('set-cookie') ? 'present' : null;
  }
  const ms = performance.now() - t0;
  return { status, body, headers, thrownStatus, result, ms };
}

const OUT: Record<string, unknown> = {};

it('records every cell', async () => {
  for (const door of DOORS) for (const mode of MODES) for (const locked of [true, false]) for (const cred of [RIGHT, WRONG]) {
    const st = arrange(mode, locked);
    S.verifyCalls = 0; S.totpCalls = 0; S.cip8Calls = 0; S.createSessionCalls = 0; S.sessionsMinted = 0; S.codesMinted = 0; S.tokenPairs = 0; S.challengeDeletes = 0; S.logs = [];
    const r = await drive(door, cred);
    const logs = S.logs.join('\n');
    OUT[`${door}|${mode}|${locked ? 'locked' : 'unlocked'}|${cred === RIGHT ? 'right' : 'wrong'}`] = {
      ...r,
      verifyCalls: S.verifyCalls, totpCalls: S.totpCalls, cip8Calls: S.cip8Calls,
      createSessionCalls: S.createSessionCalls, sessionsMinted: S.sessionsMinted, codesMinted: S.codesMinted, tokenPairs: S.tokenPairs, challengeDeletes: S.challengeDeletes,
      storeOps: st ? { ...st.ops } : null,
      lockSentInLogs: logs.split(LOCK_SENT).length - 1,
      sessSentInLogs: logs.split(SESS_SENT).length - 1,
      lockSentInBody: (r.body.split(LOCK_SENT).length - 1) + JSON.stringify(r.headers).split(LOCK_SENT).length - 1,
      sessSentInBody: (r.body.split(SESS_SENT).length - 1) + JSON.stringify(r.headers).split(SESS_SENT).length - 1,
      lockoutLogLines: S.logs.filter((l) => l.includes('lockout:')).map((l) => l.replace(/"ip":"[^"]*"/, '')),
    };
  }
  fs.writeFileSync(process.env.G171_OUT as string, JSON.stringify(OUT, null, 1));
}, 600000);
