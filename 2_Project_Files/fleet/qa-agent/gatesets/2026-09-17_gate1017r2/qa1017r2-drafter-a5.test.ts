/**
 * qa1017r2-drafter-a5.test.ts — Wednesday's #1017 ROUND 2 (KS-1195, A5 bucket identity) gate DRAFTER probe. Copied into a drafter clone's api-gateway
 * src/__tests__, run SOLO, quarantined by rename. Rows -> process.env.QA_OUT (JSON). PREDICTIONS ONLY: the gate re-measures every row.
 *
 * On the REAL index.ts app (every upstream one loopback recording stub):
 *   ident   — N keys (no connectorId x tenants, one shared connectorId, admin-mint-shaped 1000/3600, own connectorId), ONE GET /api/anchors each, then
 *             a second pass; for every key: raw key R, security's stored form S = sha256(R) hex (security/src/index.ts :1284), the round-2 form
 *             D = sha256('secuura-rate-limit-bucket\0' + R) hex. Corpora: (1) logger error/warn/info/http/verbose/debug/silly/log + console
 *             log/info/warn/error/debug lines, (2) fake-Redis command keys (QA_FAKE_REDIS=1 only), (3) upstream requests' headers + bodies EXCLUDING
 *             /api/keys/validate and /internal/connector-token (which carry R by design: counted separately as the in-design channel), (4) client
 *             responses' headers + bodies. Search R, S, D (and S/D without hex case change) in each corpus.
 *             POSITIVE CONTROLS on the SAME search: planted R of key #0 into a logger.warn line, planted S of key #1 as a fake-Redis key (or, in-memory,
 *             a console.warn line), planted R of key #2 as an x-qa-plant header on a proxied request — each must be found exactly once, nothing else.
 *   variants— the same key with trailing / leading whitespace in the header (Node strips OWS) and a second key differing only in case: same bucket?
 *   claim   — a JWT (RS256, authMethod api_key) and a test token carrying a `rateLimitBucket` claim naming a victim key's bucket: does it count
 *             against the victim? (READ: no signer emits the claim — the gate re-reads.)
 *   fallback— machine principals NOT from x-api-key: JWT api_key x {no connectorId, distinct userIds} / {same connectorId, distinct userIds, two tenants}
 *             / {userId `connector:api-key`, no connectorId, two tenants}.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import crypto from 'crypto';
import jwt from 'jsonwebtoken';
import fs from 'fs';
import type { AddressInfo } from 'net';

const OUT = process.env.QA_OUT || '';
const PRIV = process.env.__TEST_JWT_PRIVATE_PEM || '';
const FAKE = process.env.QA_FAKE_REDIS === '1';

const fakeRedis = { calls: 0, keys: [] as string[], store: new Map<string, { n: number; exp: number }>(), status: 'ready' as string,
  async incr(k: string) { this.calls++; this.keys.push(k); await new Promise((r) => setTimeout(r, 1)); const e = this.store.get(k); const now = Date.now();
    if (!e || (e.exp && now > e.exp)) { this.store.set(k, { n: 1, exp: 0 }); return 1; } e.n++; return e.n; },
  async pexpire(k: string, ms: number) { this.calls++; this.keys.push(k); const e = this.store.get(k); if (e) e.exp = Date.now() + ms; return 1; },
  async pttl(k: string) { this.calls++; this.keys.push(k); const e = this.store.get(k); return e && e.exp ? e.exp - Date.now() : -1; } };
(globalThis as any).__qaFakeRedis = fakeRedis;
vi.mock('../services/redis', async (importOriginal) => {
  const m: any = await importOriginal();
  if (process.env.QA_FAKE_REDIS !== '1') return m;
  return { ...m, getRedisClient: () => (globalThis as any).__qaFakeRedis };
});

type Rec = { method: string; url: string; headers: http.IncomingHttpHeaders; body: string };
const seen: Rec[] = [];
const logged: string[] = [];
const responses: string[] = [];
const KEYS = new Map<string, Record<string, unknown>>();
const sha = (s: string) => crypto.createHash('sha256').update(s).digest('hex');
const dom = (s: string) => crypto.createHash('sha256').update('secuura-rate-limit-bucket\0').update(s).digest('hex');

function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
}
type Res = { status: number; limit: string | null; remaining: string | null; raw: string };
function send(base: string, method: string, p: string, headers: Record<string, string>): Promise<Res> {
  return new Promise((resolve) => {
    const u = new URL(base);
    const req = http.request({ hostname: u.hostname, port: u.port, path: p, method, headers, agent: false }, (res) => {
      const c: Buffer[] = []; res.on('data', (d) => c.push(d));
      res.on('end', () => {
        const raw = JSON.stringify(res.headers) + '\n' + Buffer.concat(c).toString();
        responses.push(raw);
        resolve({ status: res.statusCode || 0, limit: (res.headers['x-ratelimit-limit'] as string) ?? null, remaining: (res.headers['x-ratelimit-remaining'] as string) ?? null, raw });
      });
    });
    req.setTimeout(3000, () => { req.destroy(); resolve({ status: -1, limit: null, remaining: null, raw: '' }); });
    req.on('error', (e) => resolve({ status: -2, limit: null, remaining: String((e as Error).message).slice(0, 80), raw: '' }));
    req.end();
  });
}
async function listen(s: http.Server): Promise<string> {
  await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
  return `http://127.0.0.1:${(s.address() as AddressInfo).port}`;
}
async function close(s?: http.Server): Promise<void> {
  if (!s) return;
  (s as any).closeAllConnections?.();
  await new Promise<void>((r) => s.close(() => r()));
}
const sign = (claims: Record<string, unknown>) => jwt.sign({ email: 'qa1017r2@example.test', role: 'connector', verificationLevel: 'api_key', ...claims }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
const testToken = (p: Record<string, unknown>) => 'test_token_' + Buffer.from(JSON.stringify(p)).toString('base64');

let stub: http.Server; let stubUrl = '';
let gw: http.Server; let gwUrl = '';
const rows: Record<string, any> = { meta: {}, ident: {}, variants: [], claim: [], fallback: [] };
let logger: any;

beforeAll(async () => {
  expect(PRIV.length).toBeGreaterThan(100);
  stub = http.createServer(async (req, res) => {
    const body = await readBody(req);
    seen.push({ method: req.method || '', url: req.url || '', headers: { ...req.headers }, body });
    const j = (s: number, o: unknown) => { res.writeHead(s, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); };
    if (req.url === '/api/keys/validate') {
      const m = KEYS.get(JSON.parse(body || '{}').key);
      return j(200, m ? { success: true, data: { valid: true, ...m } } : { success: true, data: { valid: false } });
    }
    if (req.url === '/internal/connector-token') {
      const m = KEYS.get(JSON.parse(body || '{}').apiKey);
      if (!m) return j(401, { success: false });
      const token = jwt.sign({ userId: `connector:${String(m.connectorId || 'api-key')}`, email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', tenantId: m.tenantId, scopes: m.scopes }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
      return j(200, { success: true, data: { token, expiresIn: 600 } });
    }
    if (req.url === '/.well-known/jwks.json') return j(404, {});
    return j(200, { success: true, data: [] });
  });
  stubUrl = await listen(stub);
  vi.resetModules();
  vi.stubEnv('NODE_ENV', 'test');
  vi.stubEnv('ENABLE_TEST_TOKENS', 'true');
  vi.stubEnv('UNHANDLED_REJECTION_MODE', 'survive');
  vi.stubEnv('RATE_LIMIT_MAX_REQUESTS', '1000000');
  vi.stubEnv('VERIFICATION_RATE_LIMIT_MAX', '1000000');
  for (const n of ['ORIGINATE', 'WALLET', 'AUTH', 'SECURITY', 'ANCHORING', 'TIMESTAMPING', 'PRISM', 'VC_ISSUER', 'STAKING', 'REFERRAL', 'TRANSFER', 'KYC', 'GOVERNANCE', 'NFT', 'BILLING', 'ANALYTICS', 'NOTIFICATION']) vi.stubEnv(`${n}_SERVICE_URL`, stubUrl);
  vi.stubEnv('TENANT_PROVISIONING_URL', stubUrl); vi.stubEnv('TOKENISATION_URL', stubUrl); vi.stubEnv('MCP_SERVER_URL', stubUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  delete process.env.JWT_JWKS_URL;
  const app = (await import('../index')).default;
  logger = (await import('../utils/logger')).logger;
  for (const level of ['error', 'warn', 'info', 'http', 'verbose', 'debug', 'silly', 'log'] as const) {
    if (typeof logger[level] === 'function') vi.spyOn(logger, level).mockImplementation(((...a: unknown[]) => { logged.push(`[logger.${level}] ` + a.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))).join(' ')); return logger; }) as any);
  }
  for (const level of ['log', 'info', 'warn', 'error', 'debug'] as const) {
    vi.spyOn(console, level).mockImplementation((...a: unknown[]) => { logged.push(`[console.${level}] ` + a.map((x) => (typeof x === 'string' ? x : (() => { try { return JSON.stringify(x); } catch { return String(x); } })())).join(' ')); });
  }
  gw = http.createServer(app as http.RequestListener);
  gwUrl = await listen(gw);
  rows.meta = { fakeRedis: FAKE, at: new Date().toISOString() };
}, 60000);

afterAll(async () => {
  rows.meta.loggedLines = logged.length; rows.meta.fakeRedisCalls = fakeRedis.calls;
  if (OUT) fs.writeFileSync(OUT, JSON.stringify(rows, null, 1));
  await close(gw); await close(stub);
  vi.restoreAllMocks(); vi.unstubAllEnvs();
}, 30000);

describe('qa1017r2 drafter A5 probe', () => {
  it('ident: bucket per key; raw key / stored hash in no log, Redis key, upstream request or response (planted controls found)', async () => {
    const names: string[] = [];
    const rnd = () => crypto.randomBytes(18).toString('hex');
    for (let i = 0; i < 60; i++) {
      const name = `sk_qa1017r2_${rnd()}`;
      const shape = i % 4 === 0 ? { tenantId: `t-r2-x${i}`, rateLimit: 5, rateLimitWindow: 60 }                                  // no connectorId, own tenant
        : i % 4 === 1 ? { connectorId: 'qa1017r2-shared-conn', tenantId: 't-r2-shared', rateLimit: 5, rateLimitWindow: 60 }      // one connectorId shared
        : i % 4 === 2 ? { tenantId: `t-r2-adm${i}`, rateLimit: 1000, rateLimitWindow: 3600 }                                    // admin-mint-shaped
        : { connectorId: `qa1017r2-own-${i}`, tenantId: `t-r2-own${i}`, rateLimit: 5, rateLimitWindow: 60 };                      // own connectorId
      KEYS.set(name, { scopes: ['anchors:read'], organizationId: 'org-r2', ...shape }); names.push(name);
    }
    const first: Res[] = []; const second: Res[] = [];
    for (let i = 0; i < names.length; i++) first.push(await send(gwUrl, 'GET', `/api/anchors/qar2-id-${i}-a`, { 'x-api-key': names[i] }));
    for (let i = 0; i < names.length; i++) second.push(await send(gwUrl, 'GET', `/api/anchors/qar2-id-${i}-b`, { 'x-api-key': names[i] }));
    // planted positive controls
    logger.warn(`qa1017r2 PLANT raw key ${names[0]}`);
    if (FAKE) await fakeRedis.incr(`ratelimit:qa-plant:${sha(names[1])}`); else console.warn(`qa1017r2 PLANT stored hash ${sha(names[1])}`);
    await send(gwUrl, 'GET', '/api/anchors/qar2-plant', { 'x-api-key': names[3], 'x-qa-plant': names[2] });
    const upstream = seen.filter((r) => r.url !== '/api/keys/validate' && r.url !== '/internal/connector-token').map((r) => r.method + ' ' + r.url + '\n' + JSON.stringify(r.headers) + '\n' + r.body);
    const inDesign = seen.filter((r) => r.url === '/api/keys/validate' || r.url === '/internal/connector-token').map((r) => JSON.stringify(r.headers) + '\n' + r.body);
    const corpora: Record<string, string[]> = { logs: logged, redisKeys: fakeRedis.keys, upstream, responses, inDesign_validate_exchange: inDesign };
    const count = (arr: string[], needle: string) => arr.reduce((n, s) => n + (s.split(needle).length - 1), 0);
    const hitsBy: Record<string, Record<string, Array<[number, number]>>> = {};
    for (const [cname, arr] of Object.entries(corpora)) {
      hitsBy[cname] = { raw: [], stored: [], domain: [] };
      names.forEach((n, i) => {
        const r = count(arr, n); const s = count(arr, sha(n)) + count(arr, sha(n).toUpperCase()); const d = count(arr, dom(n));
        if (r) hitsBy[cname].raw.push([i, r]); if (s) hitsBy[cname].stored.push([i, s]); if (d) hitsBy[cname].domain.push([i, d]);
      });
    }
    const redisBuckets = [...new Set(fakeRedis.keys.filter((k) => k.startsWith('ratelimit:api_key:')))];
    const expectedBuckets = names.map((n) => `ratelimit:api_key:${dom(n)}`);
    rows.ident = {
      keys: names.length,
      statusesFirst: first.reduce((a: any, r) => { a[r.status] = (a[r.status] || 0) + 1; return a; }, {}),
      remainingFirstByShape: [0, 1, 2, 3].map((m) => [...new Set(first.filter((_, i) => i % 4 === m).map((r) => `${r.limit}/${r.remaining}`))]),
      remainingSecondByShape: [0, 1, 2, 3].map((m) => [...new Set(second.filter((_, i) => i % 4 === m).map((r) => `${r.limit}/${r.remaining}`))]),
      hitsBy,
      redis: FAKE ? { distinctBucketKeys: redisBuckets.length, allExpectedPresent: expectedBuckets.every((k) => redisBuckets.includes(k)), anyEqualsStoredHashForm: names.some((n) => fakeRedis.keys.includes(`ratelimit:api_key:${sha(n)}`) || fakeRedis.keys.some((k) => k.endsWith(sha(n)) && !k.includes('qa-plant'))), sample: redisBuckets[0], nonApiKeyRatelimitKeys: [...new Set(fakeRedis.keys.filter((k) => !k.startsWith('ratelimit:api_key:')))] } : null,
      upstreamWhereRawKeyAppears: seen.filter((r) => r.url !== '/api/keys/validate' && r.url !== '/internal/connector-token').reduce((a: Record<string, number>, r) => {
        for (const [h, v] of Object.entries(r.headers)) if (names.some((n) => String(v).includes(n))) a['header:' + h] = (a['header:' + h] || 0) + 1;
        if (names.some((n) => r.body.includes(n))) a.body = (a.body || 0) + 1;
        if (names.some((n) => r.url.includes(n))) a.url = (a.url || 0) + 1;
        return a; }, {}),
      domainNeverEqualsStored: names.every((n) => dom(n) !== sha(n)),
      logLinesMentioningAnyDomainHash: logged.filter((l) => names.some((n) => l.includes(dom(n)))).map((l) => l.slice(0, 300)).slice(0, 3),
      expectedControls: { logs_raw: [[0, 1]], redisKeys_or_logs_stored: [[1, 1]], upstream_raw: [[2, 1]] },
    };
    expect(names.length).toBe(60);
  }, 120000);

  it('variants: whitespace around the key, a case-different key', async () => {
    const k = 'sk_qa1017r2_variant_Base01'; KEYS.set(k, { scopes: ['anchors:read'], tenantId: 't-r2-var', rateLimit: 3, rateLimitWindow: 60 });
    const kc = 'sk_qa1017r2_variant_base01'; KEYS.set(kc, { scopes: ['anchors:read'], tenantId: 't-r2-var', rateLimit: 3, rateLimitWindow: 60 });
    const steps: Array<[string, Record<string, string>]> = [['exact', { 'x-api-key': k }], ['trailing-space', { 'x-api-key': k + '  ' }], ['leading-space', { 'x-api-key': '  ' + k }], ['exact-again', { 'x-api-key': k }], ['case-variant-key (a DIFFERENT valid key)', { 'x-api-key': kc }]];
    for (const [label, h] of steps) { const r = await send(gwUrl, 'GET', `/api/anchors/qar2-var-${label.split(' ')[0]}`, h); rows.variants.push([label, r.status, r.limit, r.remaining]); }
    expect(rows.variants.length).toBe(5);
  }, 60000);

  it('claim: a rateLimitBucket claim on a JWT / test token', async () => {
    const victim = 'sk_qa1017r2_claim_victim'; KEYS.set(victim, { scopes: ['anchors:read'], tenantId: 't-r2-victim', rateLimit: 4, rateLimitWindow: 60 });
    const vb = `api_key:${dom(victim)}`;
    const v1 = await send(gwUrl, 'GET', '/api/anchors/qar2-claim-v1', { 'x-api-key': victim });
    const tokJ = sign({ userId: 'u-r2-claimer', tenantId: 't-r2-claimer', authMethod: 'api_key', rateLimit: 4, rateLimitWindow: 60, rateLimitBucket: vb });
    const j1 = await send(gwUrl, 'GET', '/api/anchors/qar2-claim-j1', { authorization: `Bearer ${tokJ}` });
    const tt = testToken({ userId: 'tt-r2-claimer', role: 'connector', email: 'tt@example.test', authMethod: 'api_key', verificationLevel: 'api_key', rateLimit: 4, rateLimitWindow: 60, rateLimitBucket: vb });
    const t1 = await send(gwUrl, 'GET', '/api/anchors/qar2-claim-t1', { authorization: `Bearer ${tt}` });
    const v2 = await send(gwUrl, 'GET', '/api/anchors/qar2-claim-v2', { 'x-api-key': victim });
    rows.claim.push({ victim_first: [v1.status, v1.remaining], jwt_with_victim_bucket_claim: [j1.status, j1.limit, j1.remaining], test_token_with_claim: [t1.status, t1.limit, t1.remaining], victim_second: [v2.status, v2.remaining],
      reading: 'victim Remaining 3 then 0 = both claims counted against the victim key; 3 then 2 = claims ignored' });
    expect(rows.claim.length).toBe(1);
  }, 60000);

  it('fallback: machine principals that did not come through x-api-key', async () => {
    const seq = async (label: string, toks: Array<[string, string]>) => {
      const out: any[] = []; let i = 0;
      for (const [tag, t] of toks) { const r = await send(gwUrl, 'GET', `/api/anchors/qar2-fb-${label}-${i++}`, { authorization: `Bearer ${t}` }); out.push([tag, r.status, r.limit, r.remaining]); }
      rows.fallback.push({ label, steps: out });
    };
    await seq('F1_jwt_api_key_no_connectorId_distinct_userIds', [['U1', sign({ userId: 'u-r2-f1-a', tenantId: 't-a', authMethod: 'api_key', rateLimit: 2, rateLimitWindow: 60 })], ['U1', sign({ userId: 'u-r2-f1-a', tenantId: 't-a', authMethod: 'api_key', rateLimit: 2, rateLimitWindow: 60 })], ['U2-first', sign({ userId: 'u-r2-f1-b', tenantId: 't-b', authMethod: 'api_key', rateLimit: 2, rateLimitWindow: 60 })]]);
    await seq('F2_jwt_api_key_same_connectorId_two_tenants', [['C-t1', sign({ userId: 'u-r2-f2-a', tenantId: 't-c1', connectorId: 'qa-r2-fb-conn', authMethod: 'api_key', rateLimit: 2, rateLimitWindow: 60 })], ['C-t1', sign({ userId: 'u-r2-f2-a', tenantId: 't-c1', connectorId: 'qa-r2-fb-conn', authMethod: 'api_key', rateLimit: 2, rateLimitWindow: 60 })], ['C-t2-first', sign({ userId: 'u-r2-f2-b', tenantId: 't-c2', connectorId: 'qa-r2-fb-conn', authMethod: 'api_key', rateLimit: 2, rateLimitWindow: 60 })]]);
    await seq('F3_jwt_api_key_userId_literal_connector_api-key_two_tenants', [['L-t1', sign({ userId: 'connector:api-key', tenantId: 't-l1', authMethod: 'api_key', rateLimit: 2, rateLimitWindow: 60 })], ['L-t1', sign({ userId: 'connector:api-key', tenantId: 't-l1', authMethod: 'api_key', rateLimit: 2, rateLimitWindow: 60 })], ['L-t2-first', sign({ userId: 'connector:api-key', tenantId: 't-l2', authMethod: 'api_key', rateLimit: 2, rateLimitWindow: 60 })]]);
    await seq('F4_connector_jwt_shape_as_minted_no_authMethod_control', [['M-t1', sign({ userId: 'connector:api-key', tenantId: 't-m1', type: 'connector' })], ['M-t1', sign({ userId: 'connector:api-key', tenantId: 't-m1', type: 'connector' })], ['M-t2', sign({ userId: 'connector:api-key', tenantId: 't-m2', type: 'connector' })]]);
    expect(rows.fallback.length).toBe(4);
  }, 60000);
});
