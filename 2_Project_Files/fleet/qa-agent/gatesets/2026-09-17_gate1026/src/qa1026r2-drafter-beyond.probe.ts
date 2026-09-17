// QA #1026 ROUND 2 (KS-839) DRAFTER PROBE v3 BEYOND-THE-8 CARRIERS (JS \s members the splitter DOES split, non-separators it does not, NFKC star look-alikes) + registration schema — not product code; placed at services/auth/src/qa_probe/ in the drafter clone only, run with its own
// vitest config (include src/qa_probe/**/*.probe.ts), so the whole-suite denominator never sees it. Harness shape = ks804-authorize-get-post-agree-per-rule
// (REAL routes/oauth.ts resolver + REAL validateScopes/parseScopeString; createAuthorizationCode mocked to capture the minted scope string).
// Stage 2: the REAL generateAccessToken mints from the captured grant; the REAL api-gateway requireScope and the REAL shared hasScope judge it.
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import type { Server } from 'node:http';
import { writeFileSync } from 'node:fs';
import express from 'express';

const state = vi.hoisted(() => ({ app: null as any, minted: [] as string[] }));
const silent = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: silent, createLogger: () => silent }));
vi.mock('../../../api-gateway/src/utils/logger', () => ({ logger: silent, default: silent }));
vi.mock('../services/oauth', async (importOriginal) => {
  const real = await importOriginal<Record<string, unknown>>();
  return {
    ...real,
    createAuthorizationCode: vi.fn(async (p: { scope: string }) => { state.minted.push(p.scope); return 'MINTED_AUTHORIZATION_CODE'; }),
    createApp: vi.fn(), getAppByClientId: vi.fn(async () => state.app), getAppById: vi.fn(),
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
vi.mock('../services/password', () => ({ verifyPassword: vi.fn(async () => true), hashPassword: vi.fn(async () => 'h') }));
vi.mock('../repositories/userRepo', () => ({
  getUserByEmail: vi.fn(async () => ({ id: 'user-1', email: 'u@secuura.local', status: 'ACTIVE', mfaEnabled: false, passwordHash: 'h', role: 'OWNER', verificationLevel: 'BASIC' })),
  getUserById: vi.fn(async () => null), updateUser: vi.fn(async () => undefined),
  getPlatformAdmin: vi.fn(async () => null), reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
}));
vi.mock('../services/refreshDenylist', () => ({ isRefreshJtiDenylisted: vi.fn(async () => false) }));
vi.mock('../middleware/authenticate', () => ({ authenticate: () => (_r: unknown, _s: unknown, n: () => void) => n() }));
vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [] })) }));
vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));

let server: Server; let base = '';
const rows: any[] = [];
const APPS: Record<string, string[]> = {
  NBSP_STAR: ['\u00a0*'], STAR_IDEOSP: ['*\u3000'], BOM_STAR: ['\ufeff*'], LSEP_STAR: ['\u2028*'], VT_STAR: ['\v*'], FF_STAR: ['\f*'], CR_STAR: ['\r*'],
  OGHAM_STAR: ['\u1680*'], NNBSP_STAR: ['\u202f*'], MVS_STAR: ['\u180e*'], SEMI_STAR: [';*'], PIPE_STAR: ['|*'], STAR_SEMI: ['*;'], PCT20_STAR: ['%20*'], PLUS_STAR: ['+*'],
  STAR_STAR_SPACED: ['* *'], EMPTY_THEN_STAR_NBSP: ['', '\u00a0*'], OPENID_NBSP_STAR: ['openid\u00a0*'], ASTERISK_OP: ['\u2217'], SMALL_ASTERISK: ['\ufe61'], FULLWIDTH_STAR: ['\uff0a'], ZWSP_STAR: ['*\u200b'],
  SPACE_STAR: [' *'], OPENID_THEN_SPACE_STAR: ['openid', ' *'], EXPLICIT: ['openid', 'profile'], EMPTY: [], RES: ['documents:*'],
};
const SCOPES: Array<string | undefined> = [undefined, '', 'openid', '*', 'admin:everything'];
beforeAll(async () => {
  const { oauthRouter } = await import('../routes/oauth');
  const app = express(); app.use(express.json()); app.use('/api/oauth', oauthRouter);
  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', resolve); });
  const a = server.address(); base = 'http://127.0.0.1:' + (typeof a === 'object' && a ? a.port : 0);
  rows.push({ kind: 'listener', address: a, pid: process.pid });
});
afterAll(async () => {
  await new Promise<void>((resolve) => server.close(() => resolve()));
  writeFileSync(process.env.QA_OUT as string, JSON.stringify(rows, null, 1));
});
describe('qa1026 drafter probe', () => {
  it('authorize GET + POST per app x scope, then mint + gateway judgement', async () => {
    const { generateAccessToken, initJwtKeys } = await import('../services/jwt');
    await initJwtKeys(); // QA1026-MARKER init
    const { validateScopes, parseScopeString } = await import('../services/oauth');
    const { requireScope } = await import('../../../api-gateway/src/middleware/scopes');
    const { hasScope } = await import('@secuura/shared/security/scopes');
    const jwt = (await import('jsonwebtoken')).default;
    const routes: any = await import('../routes/oauth');
    for (const [name, allowed] of Object.entries(APPS)) {
      const c = routes.CreateOAuthAppSchema.safeParse({ name: 'n', redirectUris: ['https://app.example.com/cb'], scopes: allowed });
      const u = routes.UpdateOAuthAppSchema.safeParse({ scopes: allowed });
      rows.push({ kind: 'schema', app: name, allowed, create: c.success, createStored: c.success ? c.data.scopes : null, update: u.success, updateStored: u.success ? u.data.scopes : null });
    }
    for (const [name, allowed] of Object.entries(APPS)) {
      for (const scope of SCOPES) {
        state.app = { id: 'app-1', name: 'QA', clientId: 'client-1', appType: 'confidential', redirectUris: ['https://app.example.com/cb'], allowedScopes: allowed };
        const params: Record<string, string> = { client_id: 'client-1', redirect_uri: 'https://app.example.com/cb', response_type: 'code', state: 'xyz' };
        if (scope !== undefined) params.scope = scope;
        const g = await fetch(base + '/api/oauth/authorize?' + new URLSearchParams(params), { redirect: 'manual' });
        const gb = await g.text(); let gm: string | undefined; try { gm = JSON.parse(gb)?.error?.message; } catch { gm = undefined; }
        const hidden = /name="scope" value="([^"]*)"/.exec(gb);
        state.minted = [];
        const p = await fetch(base + '/api/oauth/authorize', { method: 'POST', headers: { 'content-type': 'application/json' }, redirect: 'manual', body: JSON.stringify({ email: 'u@secuura.local', password: 'correct-horse', action: 'approve', ...params }) });
        const pb = await p.text(); let pm: string | undefined; try { pm = JSON.parse(pb)?.error?.message; } catch { pm = undefined; }
        const row: any = { app: name, allowed, scope: scope === undefined ? '<omitted>' : scope, get: g.status, getMsg: gm ?? null, consentScope: hidden ? hidden[1] : null, post: p.status, postMsg: pm ?? null, minted: state.minted.length, mintedScope: state.minted.length ? state.minted[0] : null, direct: validateScopes(scope ? parseScopeString(scope) : allowed, allowed) };
        if (state.minted.length) {
          const tok = generateAccessToken({ id: 'user-1', email: 'u@secuura.local', role: 'OWNER', organizationId: 'org-1', verificationLevel: 'BASIC', tenantId: 't', tenantSlug: 't' } as any, 'sid', { clientId: 'client-1', scopes: parseScopeString(state.minted[0]) });
          const claims: any = jwt.decode(tok);
          row.tokenScopes = claims.scopes; row.tokenAuthMethod = claims.authMethod;
          for (const need of ['documents:read', 'admin:everything']) {
            let status = 0; let nexted = false;
            const res: any = { status: (s: number) => { status = s; return res; }, json: () => res };
            requireScope(need)({ user: { authMethod: claims.authMethod, scopes: claims.scopes } } as any, res, () => { nexted = true; });
            row['gateway_' + need] = nexted ? 'next' : status;
            row['hasScope_' + need] = hasScope(claims.scopes, need);
          }
        }
        rows.push(row);
      }
    }
  }, 120000);
});
