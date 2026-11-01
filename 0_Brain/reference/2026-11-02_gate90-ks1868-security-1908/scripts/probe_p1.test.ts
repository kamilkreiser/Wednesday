// QA GATE 90 probe P1 (not part of the PR). Copied into the gate clone's src/__tests__ for the run only, then moved out.
// The :293 catch (revokePriorConnectorKeys) through the REAL route. That catch is reachable from the route only when
// isDbAvailable() reads false in saveKeyAndRetirePriors and true a moment later inside revokePriorConnectorKeys (the
// availability flag flipping between two reads, e.g. the KS-377 background re-probe succeeding). The stand-in db module
// models exactly that window: isDbAvailable() answers true only when called from revokePriorConnectorKeys (stack check,
// recorded as a positive control), and query() rejects the retire UPDATE.
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import { appendFileSync } from 'fs';

process.env.SECURITY_DISABLE_BOOT = '1';
delete process.env.API_KEY_ROTATION_GRACE_SECONDS;

const OUT = process.env.PROBE_OUT as string;
const TENANT = 'c0000000-0000-4000-8000-000000009091';
const ORG = '91919191-9191-4191-8191-919191919191';
const CONNECTOR = 'gate90-connector-p1';
const PRIOR = 'key_gate90_prior_p1';

const h = vi.hoisted(() => ({
  mode: 'none' as string,
  toThrow: undefined as unknown,
  sql: [] as string[],
  availCalls: [] as string[],
  dbPriorActive: true,
}));

vi.mock('../db', () => ({
  initDb: async () => true,
  isDbAvailable: () => {
    const st = String(new Error().stack);
    const fromRevoke = /revokePriorConnectorKeys/.test(st);
    h.availCalls.push(fromRevoke ? 'revokePriorConnectorKeys:true' : 'other:false');
    return fromRevoke;
  },
  query: (sql: string) => {
    const n = String(sql).replace(/\s+/g, ' ').trim();
    if (/^UPDATE svc_api_keys/i.test(n) && /connector_id = \$1/.test(n)) {
      h.sql.push('UPDATE svc_api_keys (retire, autocommit)');
      if (h.mode === 'retireFails') return Promise.reject(h.toThrow);
      h.dbPriorActive = false;
      return Promise.resolve({ rows: [{ id: 'x' }], rowCount: 1 });
    }
    h.sql.push(n.slice(0, 50));
    return Promise.resolve({ rows: [], rowCount: 0 });
  },
  transaction: async () => { h.sql.push('transaction() CALLED (unexpected)'); throw new Error('transaction not expected on this path'); },
  getPool: () => { throw new Error('no pool'); },
  getClient: async () => { throw new Error('no client'); },
  closeDb: async () => undefined,
}));

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

let server: Server; let base: string; let memApiKeys: Map<string, any>;
const SAVED = process.listeners('unhandledRejection');
let unhandled = 0; const onUnhandled = () => { unhandled += 1; };
const consoleLines: string[] = [];

beforeAll(async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;
  const mod: any = await import('../index');
  memApiKeys = mod.memApiKeys;
  await new Promise<void>((r) => { server = mod.default.listen(0, '127.0.0.1', r); });
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
});
afterAll(async () => {
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED) process.on('unhandledRejection', l as any);
  await new Promise<void>((r) => server.close(() => r()));
});

async function cell(name: string, mode: string, kind: string | null) {
  h.sql.length = 0; h.availCalls.length = 0; h.dbPriorActive = true; memApiKeys.clear();
  memApiKeys.set(PRIOR, { id: PRIOR, organizationId: ORG, tenantId: TENANT, name: 'prior', keyHash: 'h-prior-p1', keyPrefix: 'sk_prior',
    scopes: ['documents:read'], rateLimit: 100, rateLimitWindow: 60, usageCount: 0, isActive: true, createdAt: new Date(), connectorId: CONNECTOR });
  h.mode = mode; h.toThrow = kind ? KINDS[kind]() : undefined;
  unhandled = 0; consoleLines.length = 0;
  const spy = vi.spyOn(console, 'log').mockImplementation((...a: unknown[]) => { consoleLines.push(String(a[0])); });
  let status: number | string = 'none'; let body: any = null;
  try {
    const res = await fetch(`${base}/api/keys`, {
      method: 'POST', signal: AbortSignal.timeout(3000),
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token({ role: 'super_admin' })}` },
      body: JSON.stringify({ name: 'gate90p1', scopes: ['documents:read'], tenantId: TENANT, organizationId: ORG, connectorId: CONNECTOR, rotate: true }),
    });
    status = res.status; const t = await res.text(); try { body = JSON.parse(t); } catch { body = t.slice(0, 200); }
  } catch (e) { status = 'UNANSWERED(' + (e as Error).name + ')'; }
  await new Promise((r) => setTimeout(r, 50));
  spy.mockRestore();
  const mem = Object.fromEntries([...memApiKeys.entries()].map(([id, k]) => [id === PRIOR ? 'prior' : 'new', k.isActive ? 'active' : 'inactive']));
  const pick = (re: RegExp) => consoleLines.filter((s) => re.test(s)).map((s) => { try { const j = JSON.parse(s); return { message: j.message, error: j.error, code: j.code, infra: j.infra }; } catch { return s.slice(0, 120); } });
  const rec = {
    cell: name, mode, kind, status,
    priorKeysRevoked: body?.data && 'priorKeysRevoked' in body.data ? body.data.priorKeysRevoked : '(absent)',
    keyIssued: typeof body?.data?.key === 'string' && body.data.key.length > 0,
    errorMessage: body?.error?.message ?? null,
    availCalls: [...h.availCalls], sql: [...h.sql],
    dbPriorRow: h.dbPriorActive ? 'active' : 'retired', memApiKeys: mem,
    log_ks577: pick(/KS-577: revoke-on-rotate FAILED/), log_ks888: pick(/KS-888/), log_created: pick(/"API key created"/).length,
    unhandled,
  };
  appendFileSync(OUT, JSON.stringify(rec) + '\n');
}

describe('gate 90 probe P1: :293 through the route in the availability-flip window', () => {
  it('control: retire succeeds', async () => { await cell('p1/control', 'none', null); });
  for (const k of Object.keys(KINDS)) it(`retire rejects: ${k}`, async () => { await cell(`p1/retire/${k}`, 'retireFails', k); });
});
