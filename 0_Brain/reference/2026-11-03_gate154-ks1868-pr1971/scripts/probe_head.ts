/**
 * KS-1677 — the Microsoft 365 sign-in callback no longer trusts whoever completes it.
 *
 * On develop the OAuth `state` was the connection's own id, looked up alone by an unauthenticated route, so any
 * holder of a connection id could finish its sign-in with a code from their own Microsoft account, pending OR
 * already connected; a garbage code flipped it to `error`; and the redirect told a known id from an unknown one.
 * Gate AS1 measured that on #1633 (KS-1677 comment 7fad8f7e).
 *
 * Every cell below sends the SAME requests to develop and to the fix. The state a cell uses is the one the
 * authorization URL carries, and the cookie is whatever init set; on develop that is the connection id and no
 * cookie at all. That is what makes a RED cell red on develop and green with the fix.
 *   RED     fails on develop, passes with the fix.
 *   CONTROL passes on both: the legitimate flow keeps working.
 *   GUARD   passes on both, and exists to kill one mutant that no RED cell can reach. A constructed state record
 *           (organisation mismatch; connection no longer pending) cannot be produced by any request on develop.
 * Every label was MEASURED on both sides, not assigned by intent: a first draft labelled R15 a control and asserted
 * the refusal's wording in G1/G2, and the develop run showed both were wrong.
 *
 * Harness: the production path. `../db` is up (`isDbAvailable: () => true`), `svc_m365_connections` is served
 * from seeded rows through the real loadFromDb, and `svc_m365_oauth_states` is a fake table that honours the
 * statements' PARAMETERS (the SQL text itself runs on a real engine in
 * ks1677-oauth-state-statements-on-a-real-engine.test.ts). The PII keyring is real, so the verifier is really
 * encrypted at rest and really decrypted at the callback.
 * Mocked: `exchangeAuthCode` (records the code and the verifier it was given; 'garbage' throws, like Microsoft
 * refusing a code), `authenticate` from `@secuura/shared` (a cell picks its caller), Graph's /organization via a
 * `fetch` spy, and express's `listen`. The routes are real, driven over 127.0.0.1.
 */
import { describe, it, expect, vi, beforeAll, beforeEach, afterAll } from 'vitest';
import http from 'http';
import crypto from 'crypto';

const seen = vi.hoisted(() => {
  process.env.NODE_ENV = 'test';
  process.env.FRONTEND_URL = 'http://frontend.test';
  process.env.ENTRA_CLIENT_ID = 'test-client-id';
  process.env.ENTRA_CLIENT_SECRET = 'test-client-secret';
  process.env.ENTRA_TENANT_ID = 'test-entra-tenant';
  // a real keyring, so the verifier is encrypted at rest (index.ts initialises it at load when the key is set)
  process.env.PII_ENCRYPTION_KEY = '00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff';
  process.env.PII_ENCRYPTION_KEY_VERSION = '1';
  return {
    warmed: false,
    exchanged: [] as Array<{ code: string; verifier: string | undefined }>,
    states: new Map<string, Record<string, unknown>>(),
    graphCalls: 0,
    /** R17: make the next state INSERT fail, as a DB blip would; the store logs it and keeps the record in memory only. */
    failNextInsert: false,
    insertThrow: { on: false, value: undefined as unknown },
    consumeThrow: { on: false, value: undefined as unknown },
  };
});

const ORG_A = 'org-ks1677-a';
const ORG_B = 'org-ks1677-b';
const now = new Date().toISOString();
const row = (id: string, organizationId: string, status: 'pending' | 'connected') => ({
  id, organization_id: organizationId, tenant_id: 'entra-tenant', tenant_name: null, status,
  access_token: status === 'connected' ? 'owner-access-token' : null,
  refresh_token: status === 'connected' ? 'owner-refresh-token' : null,
  token_expires_at: null, scopes: ['User.Read'], connected_at: status === 'connected' ? now : null,
  last_sync_at: null, error_message: null, created_at: now, updated_at: now,
});
// one seeded row per cell that touches one, so no cell can change another's row
const SEEDED = {
  r1Pending: 'conn_r1_pending_a', r2Connected: 'conn_r2_connected_a', r3Connected: 'conn_r3_connected_a',
  g1PendingB: 'conn_g1_pending_b', g2Connected: 'conn_g2_connected_a',
};

vi.mock('../db', () => ({
  initDb: async (onReady?: () => Promise<void>) => { await onReady?.(); },
  isDbAvailable: () => true,
  query: async (sql: string, params: unknown[] = []) => {
    if (/SELECT \* FROM svc_m365_connections\s*$/.test(sql)) {
      seen.warmed = true;
      return { rows: [
        row(SEEDED.r1Pending, ORG_A, 'pending'), row(SEEDED.r2Connected, ORG_A, 'connected'),
        row(SEEDED.r3Connected, ORG_A, 'connected'), row(SEEDED.g1PendingB, ORG_B, 'pending'),
        row(SEEDED.g2Connected, ORG_A, 'connected'),
      ] };
    }
    if (/^INSERT INTO svc_m365_oauth_states/.test(sql.trim())) {
      if (seen.insertThrow.on) throw seen.insertThrow.value;
      if (seen.failNextInsert) { seen.failNextInsert = false; throw new Error('stub: the database dropped this insert'); }
      const [state_hash, binding_hash, connection_id, organization_id, initiated_by, code_verifier, expires_at] = params as any[];
      seen.states.set(String(state_hash), { state_hash, binding_hash, connection_id, organization_id, initiated_by, code_verifier, expires_at });
      return { rows: [] };
    }
    if (/^DELETE FROM svc_m365_oauth_states\s+WHERE state_hash = \$1 AND binding_hash = \$2/.test(sql.trim())) {
      if (seen.consumeThrow.on) throw seen.consumeThrow.value;
      const r = seen.states.get(String(params[0]));
      if (!r || r.binding_hash !== params[1]) return { rows: [] };
      seen.states.delete(String(params[0]));
      return { rows: [r] };
    }
    return { rows: [] };
  },
}));

vi.mock('../auth/token-manager', async (importOriginal) => {
  const actual = await importOriginal<Record<string, unknown>>();
  return {
    ...actual,
    exchangeAuthCode: async (code: string, _redirectUri: string, _scopes: string[], codeVerifier?: string) => {
      seen.exchanged.push({ code, verifier: codeVerifier });
      if (code === 'garbage') throw new Error('stub: Microsoft refused this code');
      return { accessToken: `access-of-${code}`, refreshToken: `refresh-of-${code}`, expiresAt: new Date(Date.now() + 3600_000), tenantName: `tenant-of-${code}` };
    },
  };
});

const caller: { user: unknown } = { user: undefined };
const as = (organizationId: string, userId = `user-in-${organizationId}`) => { caller.user = { userId, role: 'ISSUER_ADMIN', organizationId }; };

vi.mock('@secuura/shared', async (importOriginal) => {
  const actual = await importOriginal<Record<string, unknown>>();
  return { ...actual, authenticate: () => (req: any, _res: any, next: any) => { req.user = caller.user; next(); } };
});

vi.mock('express', async (importOriginal) => {
  const actual: any = (await importOriginal<any>()).default ?? (await importOriginal<any>());
  const factory: any = (...args: any[]) => {
    const app = actual(...args);
    app.listen = (_p: any, cb?: () => void) => { setTimeout(() => cb?.(), 0); return { close: (c?: () => void) => c?.(), address: () => ({ port: 0 }), on() { return this; } }; };
    return app;
  };
  Object.assign(factory, actual);
  return { ...actual, default: factory };
});

const realFetch = globalThis.fetch;
vi.spyOn(globalThis, 'fetch').mockImplementation(((url: any, init?: any) => {
  if (String(url).startsWith('https://graph.microsoft.com/')) {
    seen.graphCalls += 1;
    return Promise.resolve(new Response(JSON.stringify({ value: [{ displayName: 'Graph Org' }] }), { status: 200, headers: { 'content-type': 'application/json' } }));
  }
  return realFetch(url, init);
}) as typeof fetch);

let server: http.Server;
let base = '';

beforeAll(async () => {
  const app = (await import('../index')).default as any;
  for (let i = 0; i < 200 && !seen.warmed; i++) await new Promise((r) => setTimeout(r, 20));
  await new Promise((r) => setTimeout(r, 50));
  server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
  base = `http://127.0.0.1:${(server.address() as any).port}`;
}, 30_000);

afterAll(async () => { if (server) await new Promise<void>((r) => server.close(() => r())); });

beforeEach(() => { seen.exchanged.length = 0; caller.user = undefined; });

const sha256Hex = (v: string) => crypto.createHash('sha256').update(v, 'utf8').digest('hex');
const s256 = (v: string) => crypto.createHash('sha256').update(v, 'ascii').digest('base64url');

/** POST init as the current caller; returns what a browser would hold afterwards. */
async function init() {
  const res = await realFetch(`${base}/api/connections/init`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' });
  const body: any = await res.json();
  const authUrl = new URL(body?.data?.authorizationUrl ?? 'http://none.invalid/');
  const setCookie = res.headers.get('set-cookie') ?? '';
  const pair = setCookie.split(';')[0] ?? '';
  return { status: res.status, connId: String(body?.data?.connectionId), authUrl, state: authUrl.searchParams.get('state') ?? '', cookie: pair.includes('=') ? pair : '', setCookie };
}

/** The browser's arrival back from Microsoft. */
async function cb(state: string, code: string, cookie = '') {
  const res = await realFetch(`${base}/api/callback?code=${encodeURIComponent(code)}&state=${encodeURIComponent(state)}`, { redirect: 'manual', headers: cookie ? { cookie } : {} });
  const location = res.headers.get('location') || 'http://none.invalid/';
  const u = new URL(location);
  return { status: res.status, location, m365: u.searchParams.get('m365'), message: u.searchParams.get('message') };
}

/** The connection as its own organisation reads it. */
async function statusOf(id: string, org: string) {
  as(org);
  const res = await realFetch(`${base}/api/connections/${encodeURIComponent(id)}`);
  const body: any = await res.json().catch(() => ({}));
  return body?.data?.status ?? `http-${res.status}`;
}

const refused = (r: { status: number; m365: string | null; message: string | null }) => [r.status, r.m365, r.message];
const REFUSED = [302, 'error', 'invalid_state'];