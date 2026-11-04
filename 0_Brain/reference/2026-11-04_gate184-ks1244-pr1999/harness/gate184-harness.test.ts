/**
 * QA gate 184 harness (KS-1244 / PR 1999). Written by the gate, never committed to the client repo.
 * Runs unchanged against base (develop 307d9b4c762a) and head (merge of defe782aaf61 onto it): it imports only the app.
 * Writes its measurements to $GATE_OUT/<label>.*.json; the gate compares them with a separate script.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import net from 'net';
import jwt from 'jsonwebtoken';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { AddressInfo } from 'node:net';
import { parse as parseYaml } from 'yaml';
import Transport from 'winston-transport';

vi.mock('../db', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
});
vi.mock('@secuura/shared', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  return { ...real, isSessionActive: async (s: string) => (s === 'g184-live' ? true : null) };
});

const OUT = process.env.GATE_OUT as string;
const LABEL = process.env.GATE_LABEL as string;
const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
const TENANT = 'a0000000-0000-4000-8000-000000000184';
const SPEC = resolve(__dirname, '../../../../docs/openapi/secuura-api.yaml');
const VALID_RE = /^sk_g184v_[a-z0-9]+$/;
let seq = 0;
// PLANT marks every key sent on a REPEATED request; CTL marks every key sent ALONE (controls: those may legitimately reach the security service).
const PLANT = 'qzplant184';
const CTL = 'qzctl184';
const vkey = (mark: string) => `sk_g184v_${mark}${(seq += 1).toString(36)}x${Date.now().toString(36)}`;
const jkey = (mark: string) => `sk_g184j_${mark}${(seq += 1).toString(36)}`;

type Up = { method: string; url: string; gid: string | null; rawHeaders: string[]; body: string };
const ups: Up[] = [];
const keyOwner = new Map<string, string>();

function sign(c: Record<string, unknown>): string {
  return jwt.sign({ userId: 'u-g184', email: 'u@g184.test', role: 'ISSUER', tenantId: TENANT, verificationLevel: 'BASIC', ...c }, PRIV, { algorithm: 'RS256', expiresIn: '10m' });
}
function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d: Buffer) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
}
async function listen(s: http.Server): Promise<string> {
  await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
  return `http://127.0.0.1:${(s.address() as AddressInfo).port}`;
}
async function closeServer(s?: http.Server) { if (!s) return; s.closeAllConnections(); await new Promise<void>((r) => s.close(() => r())); }

function createUpstream(): http.Server {
  return http.createServer(async (req, res) => {
    const body = await readBody(req);
    const url = req.url || '';
    ups.push({ method: req.method || '', url, gid: (req.headers['x-gate-id'] as string) ?? null, rawHeaders: [...req.rawHeaders], body });
    const json = (st: number, p: unknown) => { res.writeHead(st, { 'content-type': 'application/json' }); res.end(JSON.stringify(p)); };
    if (url === '/api/keys/validate') {
      const key = (JSON.parse(body || '{}') as { key?: unknown }).key;
      return json(200, typeof key === 'string' && VALID_RE.test(key)
        ? { data: { valid: true, connectorId: 'g184-conn', scopes: ['documents:read', 'documents:write', 'credentials:read', 'credentials:write'], organizationId: 'org-g184', tenantId: TENANT, rateLimit: 100000, rateLimitWindow: 60 } }
        : { data: { valid: false } });
    }
    if (url === '/internal/connector-token') {
      const k = (JSON.parse(body || '{}') as { apiKey?: unknown }).apiKey;
      if (typeof k !== 'string' || !VALID_RE.test(k)) return json(401, { success: false });
      return json(200, { success: true, data: { token: sign({ userId: 'connector:g184', role: 'connector', verificationLevel: 'api_key', type: 'connector' }), expiresIn: 600 } });
    }
    if (url.startsWith('/.well-known/')) return json(404, {});
    return json(200, { success: true, data: { recorder: true } });
  });
}

const SERVICES = ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM',
  'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET'];

// Everything any logger or console line carried, captured by a transport ADDED to the app's own logger instance plus console spies.
const logLines: string[] = [];
async function bootApp(upstreamUrl: string) {
  for (const n of SERVICES) vi.stubEnv(`${n}_SERVICE_URL`, upstreamUrl);
  vi.stubEnv('TENANT_PROVISIONING_URL', upstreamUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  delete process.env.JWT_JWKS_URL;
  vi.resetModules();
  const { logger } = await import('../utils/logger');
  class Cap extends Transport { log(info: unknown, cb: () => void) { logLines.push(JSON.stringify(info)); cb(); } }
  logger.add(new Cap({ level: 'silly' }));
  for (const m of ['log', 'info', 'warn', 'error', 'debug'] as const) {
    const orig = console[m].bind(console);
    vi.spyOn(console, m).mockImplementation((...a: unknown[]) => { logLines.push(a.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))).join(' ')); void orig; });
  }
  const app = (await import('../index')).default;
  const server = http.createServer(app as http.RequestListener);
  return { server, url: await listen(server) };
}

type Res = { status: number; head: string; body: string; location: string | null };
function dechunk(b: Buffer): Buffer {
  const out: Buffer[] = []; let i = 0;
  for (;;) { const nl = b.indexOf('\r\n', i); if (nl < 0) break; const size = parseInt(b.subarray(i, nl).toString('latin1'), 16); if (!size) break; out.push(b.subarray(nl + 2, nl + 2 + size)); i = nl + 2 + size + 2; }
  return Buffer.concat(out);
}
const responses: string[] = [];
function sendRaw(base: string, method: string, path: string, lines: string[]): Promise<Res> {
  const u = new URL(base);
  const withBody = ['POST', 'PUT', 'PATCH'].includes(method);
  const payload = withBody ? '{}' : '';
  const head = [`${method} ${path} HTTP/1.1`, `Host: ${u.host}`, 'Connection: close', ...(withBody ? ['Content-Type: application/json', `Content-Length: ${payload.length}`] : []), ...lines];
  return new Promise((ok, bad) => {
    const sock = net.connect(Number(u.port), u.hostname); const ch: Buffer[] = [];
    sock.setTimeout(20000, () => sock.destroy(new Error(`timeout ${method} ${path}`)));
    sock.on('data', (d: Buffer) => ch.push(d)); sock.on('error', bad);
    sock.on('close', () => {
      const buf = Buffer.concat(ch); const text = buf.toString('latin1'); const sep = text.indexOf('\r\n\r\n');
      if (sep < 0) { bad(new Error(`no response ${method} ${path}`)); return; }
      const hl = text.slice(0, sep).split('\r\n'); const h: Record<string, string> = {};
      for (const l of hl.slice(1)) { const c = l.indexOf(':'); if (c > 0) h[l.slice(0, c).trim().toLowerCase()] = l.slice(c + 1).trim(); }
      let raw: Buffer = buf.subarray(sep + 4); if ((h['transfer-encoding'] || '').toLowerCase() === 'chunked') raw = dechunk(raw);
      responses.push(text.slice(0, sep) + '\n\n' + raw.toString('utf8'));
      ok({ status: Number((hl[0].match(/^HTTP\/1\.1 (\d{3})/) || [])[1] || 0), head: text.slice(0, sep), body: raw.toString('utf8'), location: h.location ?? null });
    });
    sock.write(head.join('\r\n') + '\r\n\r\n' + payload);
  });
}
const settle = (ms = 80) => new Promise<void>((r) => setTimeout(r, ms));
let gidSeq = 0;
/** One request, tagged with x-gate-id; returns what the caller got and what reached the upstream for THIS request. */
async function probe(base: string, method: string, path: string, lines: string[], keys: string[]) {
  const gid = `g${(gidSeq += 1)}`;
  keys.forEach((k) => keyOwner.set(k, gid));
  const res = await sendRaw(base, method, path, [`x-gate-id: ${gid}`, ...lines]);
  await settle();
  const mine = ups.filter((u) => u.gid === gid || keys.some((k) => k && u.body.includes(k)));
  const validations = mine.filter((u) => u.url === '/api/keys/validate').length;
  const fwd = mine.filter((u) => u.url !== '/api/keys/validate' && u.url !== '/internal/connector-token');
  const auth = fwd.map((u) => { const i = u.rawHeaders.findIndex((x, j) => j % 2 === 0 && x.toLowerCase() === 'authorization'); return i < 0 ? 'none' : 'bearer'; });
  const fwdKeyLines = fwd.map((u) => u.rawHeaders.filter((x, j) => j % 2 === 0 && x.toLowerCase() === 'x-api-key').length);
  let code: string | null = null; try { code = (JSON.parse(res.body) as { error?: { code?: string } })?.error?.code ?? null; } catch { code = null; }
  return { status: res.status, code, location: res.location, hits: fwd.length, validations, auth: auth.join('|') || '-', fwdKeyLines: fwdKeyLines.join('|') || '-' };
}

type Op = { method: string; path: string };
function specOps(): Op[] {
  const spec = parseYaml(readFileSync(SPEC, 'utf8')) as { paths: Record<string, Record<string, unknown>> };
  const ops: Op[] = [];
  for (const [p, item] of Object.entries(spec.paths)) for (const m of Object.keys(item)) if (['get', 'post', 'put', 'patch', 'delete'].includes(m)) ops.push({ method: m.toUpperCase(), path: p.replace(/\{[^}]+\}/g, 'g184') });
  return ops;
}
const UNSPEC: Op[] = [
  { method: 'POST', path: '/originate/api/documents' }, { method: 'GET', path: '/originate/api/documents/g184' },
  { method: 'POST', path: '/webhooks/stripe' }, { method: 'GET', path: '/demo-api/g184' }, { method: 'POST', path: '/api/logs' },
  { method: 'GET', path: '/api/downloads/g184' }, { method: 'GET', path: '/health' }, { method: 'GET', path: '/developers' },
];
const SHAPES: Array<[string, () => { lines: string[]; keys: string[] }]> = [
  ['zero', () => ({ lines: [], keys: [] })],
  ['oneValid', () => { const k = vkey(CTL); return { lines: [`x-api-key: ${k}`], keys: [k] }; }],
  ['oneJunk', () => { const k = jkey(CTL); return { lines: [`x-api-key: ${k}`], keys: [k] }; }],
  ['oneNonSk', () => { const k = `nsk_${CTL}${(seq += 1)}`; return { lines: [`x-api-key: ${k}`], keys: [k] }; }],
  ['rep2valid', () => { const a = vkey(PLANT); const b = vkey(PLANT); return { lines: [`x-api-key: ${a}`, `X-Api-Key: ${b}`], keys: [a, b] }; }],
  ['repComma', () => { const a = vkey(PLANT); const b = vkey(PLANT); return { lines: [`x-api-key: ${a}, ${b}`], keys: [a, b] }; }],
  ['repEmptyFirst', () => { const b = vkey(PLANT); return { lines: ['x-api-key:', `x-api-key: ${b}`], keys: [b] }; }],
  ['repJunkValid', () => { const a = jkey(PLANT); const b = vkey(PLANT); return { lines: [`x-api-key: ${a}`, `x-api-key: ${b}`], keys: [a, b] }; }],
];
async function pool<T, R>(items: T[], size: number, fn: (t: T) => Promise<R>): Promise<R[]> {
  const out: R[] = new Array(items.length); let next = 0;
  await Promise.all(Array.from({ length: size }, async () => { for (;;) { const n = next++; if (n >= items.length) return; out[n] = await fn(items[n]); } }));
  return out;
}

let upstream: http.Server | undefined; let upstreamUrl = '';
const results: Record<string, unknown> = {};
beforeAll(async () => { upstream = createUpstream(); upstreamUrl = await listen(upstream); });
afterAll(async () => {
  await closeServer(upstream);
  writeFileSync(resolve(OUT, `${LABEL}.results.json`), JSON.stringify(results, null, 1));
  // Everything that left the process, for the gate's own grep: log lines, every raw response, every upstream request.
  writeFileSync(resolve(OUT, `${LABEL}.capture.logs.txt`), logLines.join('\n'));
  writeFileSync(resolve(OUT, `${LABEL}.capture.responses.txt`), responses.join('\n=====\n'));
  writeFileSync(resolve(OUT, `${LABEL}.capture.upstream.txt`), ups.map((u) => `${u.method} ${u.url} gid=${u.gid}\n${u.rawHeaders.join(': ')}\n${u.body}`).join('\n=====\n'));
  vi.restoreAllMocks(); vi.unstubAllEnvs();
});

async function matrix(base: string, prod: boolean) {
  const ops = [...specOps(), ...UNSPEC].map((o) => {
    if (!prod) return o;
    const f = o.path.toLowerCase();
    const v = f.startsWith('/api/') && !['/api/docs', '/api/health', '/api/v1/', '/api/v2/'].some((p) => f.startsWith(p));
    return v ? { method: o.method, path: o.path.replace(/^\/api\//, '/api/v1/') } : o;
  });
  const only = (process.env.GATE_SHAPES || '').split(',').filter(Boolean);
  const cells: Array<[Op, string]> = []; for (const op of ops) for (const [s] of SHAPES) if (!only.length || only.includes(s)) cells.push([op, s]);
  const shapeFn = Object.fromEntries(SHAPES);
  const rows = await pool(cells, 6, async ([op, s]) => { const { lines, keys } = shapeFn[s](); return { op: `${op.method} ${op.path}`, shape: s, ...(await probe(base, op.method, op.path, lines, keys)) }; });
  return rows;
}

describe('gate184 NODE_ENV=test', () => {
  let gw: { server: http.Server; url: string } | undefined;
  beforeAll(async () => { vi.stubEnv('NODE_ENV', 'test'); gw = await bootApp(upstreamUrl); }, 60000);
  afterAll(async () => { await closeServer(gw?.server); });
  it('matrix test-mode', async () => { results.matrixTest = await matrix(gw!.url, false); expect((results.matrixTest as unknown[]).length).toBeGreaterThan(process.env.GATE_SHAPES ? 1000 : 2800); }, 600000);
});

describe('gate184 NODE_ENV=production', () => {
  let gw: { server: http.Server; url: string } | undefined;
  beforeAll(async () => {
    vi.stubEnv('NODE_ENV', 'production');
    vi.stubEnv('CSRF_SECRET', 'g184-stub-csrf-not-a-real-secret');
    vi.stubEnv('DATABASE_URL', 'postgres://g184:g184@127.0.0.1:1/g184');
    vi.stubEnv('REDIS_URL', 'redis://127.0.0.1:1');
    vi.stubEnv('ENABLE_TEST_TOKENS', ''); vi.stubEnv('ENABLE_MOCK_ENDPOINTS', '');
    for (const k of ['RATE_LIMIT_MAX_REQUESTS', 'VERIFICATION_RATE_LIMIT_MAX', 'LOGIN_RATE_LIMIT', 'REGISTER_RATE_LIMIT', 'PASSWORD_RESET_RATE_LIMIT', 'REFRESH_RATE_LIMIT']) vi.stubEnv(k, '1000000');
    gw = await bootApp(upstreamUrl);
  }, 60000);
  afterAll(async () => { await closeServer(gw?.server); });

  it('P1 cookie, no CSRF token, POST', async () => {
    const path = '/api/v1/credentials/g184/revoke'; const cookie = 'Cookie: sid=g184-session';
    const noKey = await probe(gw!.url, 'POST', path, [cookie], []);
    const k1 = vkey(CTL); const oneValid = await probe(gw!.url, 'POST', path, [cookie, `x-api-key: ${k1}`], [k1]);
    const a = vkey(PLANT); const b = vkey(PLANT); const rep = await probe(gw!.url, 'POST', path, [cookie, `x-api-key: ${a}`, `x-api-key: ${b}`], [a, b]);
    const c = vkey(PLANT); const d = vkey(PLANT); const repC = await probe(gw!.url, 'POST', path, [cookie, `x-api-key: ${c},${d}`], [c, d]);
    results.P1 = { noKey, oneValid, rep, repC };
    expect([noKey.status, oneValid.status, rep.status, rep.hits, rep.validations, repC.status]).toBeDefined();
  });

  it('P2 bearerAuth GET, no Bearer', async () => {
    const path = '/api/v1/credentials';
    const none = await probe(gw!.url, 'GET', path, [], []);
    const k1 = vkey(CTL); const oneValid = await probe(gw!.url, 'GET', path, [`x-api-key: ${k1}`], [k1]);
    const j1 = jkey(CTL); const oneJunk = await probe(gw!.url, 'GET', path, [`x-api-key: ${j1}`], [j1]);
    const a = vkey(PLANT); const b = vkey(PLANT); const rep = await probe(gw!.url, 'GET', path, [`x-api-key: ${a}`, `x-api-key: ${b}`], [a, b]);
    results.P2 = { none, oneValid, oneJunk, rep };
  });

  it('V307 versioning above the refusal', async () => {
    const a = vkey(PLANT); const b = vkey(PLANT);
    const rep = await probe(gw!.url, 'POST', '/api/documents', [`x-api-key: ${a}`, `x-api-key: ${b}`], [a, b]);
    const c = vkey(PLANT); const d = vkey(PLANT);
    const follow = await probe(gw!.url, 'POST', rep.location || '/api/v1/documents', [`x-api-key: ${c}`, `x-api-key: ${d}`], [c, d]);
    const none = await probe(gw!.url, 'POST', '/api/documents', [], []);
    const k1 = vkey(CTL); const one = await probe(gw!.url, 'POST', '/api/documents', [`x-api-key: ${k1}`], [k1]);
    const e = vkey(PLANT); const f = vkey(PLANT);
    const repQs = await probe(gw!.url, 'POST', '/api/documents?x=1', [`x-api-key: ${e}, ${f}`], [e, f]);
    results.V307 = { rep, follow, none, one, repQs };
  });

  it('matrix production-mode', async () => { results.matrixProd = await matrix(gw!.url, true); expect((results.matrixProd as unknown[]).length).toBeGreaterThan(process.env.GATE_SHAPES ? 1000 : 2800); }, 600000);
});
