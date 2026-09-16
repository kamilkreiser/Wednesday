/**
 * qa1011-drafter-probe — DRAFTER pre-measurement for the #1011 (KS-871) tier-1 gate set. NOT a gate cell; copied into the
 * drafter's own clone worktrees (base d067725ff / head 0a1f8900c), never into the Secuura checkout.
 * The REAL app (index.ts default export, require.main guard) with ../db mocked: isDbAvailable true, query a recorder with a
 * hit witness. Every request is sent as a RAW request line on a loopback socket (so absolute-form, '#', '//' reach express
 * unaltered), then the audit INSERT params written for it are captured. Rows go to QA1011_PROBE_OUT as JSON.
 * Plus the nested-mount fixture (TE question) on a bare express app with the tree's createAuditMiddleware.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import net from 'net';
import fs from 'fs';
import express from 'express';
import jwt from 'jsonwebtoken';
import type { AddressInfo } from 'net';

const rec = vi.hoisted(() => ({ calls: [] as { sql: string; params: unknown[] }[], dbAvailable: true, throwOnInsert: false }));
vi.mock('../db', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  return {
    ...real,
    isDbAvailable: () => rec.dbAvailable,
    query: async (sql: string, params: unknown[] = []) => {
      rec.calls.push({ sql, params });
      if (rec.throwOnInsert && /INSERT INTO audit_logs/.test(sql)) throw new Error('qa1011 sink threw');
      return { rows: [], rowCount: 0 };
    },
  };
});

const rows: unknown[] = [];
let upstream: http.Server; let upUrl = ''; const upSeen: string[] = [];
let gw: http.Server; let port = 0;

function raw(requestLine: string, headers: Record<string, string>, body: string): Promise<{ status: number; body: string }> {
  return new Promise((resolve) => {
    const s = net.connect(port, '127.0.0.1');
    let buf = '';
    s.on('data', (d) => { buf += d.toString(); });
    s.on('end', () => {
      const m = buf.match(/^HTTP\/1\.1 (\d{3})/);
      resolve({ status: m ? Number(m[1]) : -1, body: buf.split('\r\n\r\n').slice(1).join('\r\n\r\n').slice(0, 160) });
    });
    s.on('error', () => resolve({ status: -2, body: '' }));
    const h = { host: '127.0.0.1', connection: 'close', 'content-type': 'application/json', 'content-length': String(Buffer.byteLength(body)), ...headers };
    s.write(requestLine + '\r\n' + Object.entries(h).map(([k, v]) => `${k}: ${v}`).join('\r\n') + '\r\n\r\n' + body);
  });
}

async function probe(label: string, method: string, target: string, headers: Record<string, string> = {}, body = '{}') {
  const before = rec.calls.length;
  const r = await raw(`${method} ${target} HTTP/1.1`, headers, body);
  await new Promise((res) => setTimeout(res, 250));
  const audits = rec.calls.slice(before).filter((c) => /INSERT INTO audit_logs/.test(c.sql)).map((c) => {
    const p = c.params as unknown[];
    let details: unknown = p[8];
    try { details = JSON.parse(String(p[8])); if (details && typeof details === 'object') delete (details as Record<string, unknown>).durationMs; } catch { /* keep raw */ }
    return { tenant: p[0], user: p[1], org: p[2], action: p[3], resourceType: p[4], resourceId: p[5], ip: p[6], ua: p[7], details, success: p[9] };
  });
  rows.push({ label, method, target, status: r.status, body: r.body, audits });
}

beforeAll(async () => {
  upstream = http.createServer((req, res) => { req.resume(); req.on('end', () => { upSeen.push(`${req.method} ${req.url}`); res.writeHead(200, { 'content-type': 'application/json' }); res.end('{"up":true}'); }); });
  await new Promise<void>((r) => upstream.listen(0, '127.0.0.1', () => r()));
  upUrl = `http://127.0.0.1:${(upstream.address() as AddressInfo).port}`;
  vi.stubEnv('ORIGINATE_SERVICE_URL', upUrl);
  vi.stubEnv('AUTH_SERVICE_URL', upUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  const app = (await import('../index')).default;
  gw = http.createServer(app as http.RequestListener);
  await new Promise<void>((r) => gw.listen(0, '127.0.0.1', () => r()));
  port = (gw.address() as AddressInfo).port;
}, 60000);

afterAll(async () => {
  if (gw) { gw.closeAllConnections(); await new Promise<void>((r) => gw.close(() => r())); }
  if (upstream) { upstream.closeAllConnections(); await new Promise<void>((r) => upstream.close(() => r())); }
  fs.writeFileSync(process.env.QA1011_PROBE_OUT || '/dev/null', JSON.stringify({ rows, upSeen }, null, 1));
});

describe('qa1011 drafter probe', () => {
  it('census through the real app', async () => {
    const pem = process.env.__TEST_JWT_PRIVATE_PEM || '';
    const tok = (claims: object) => jwt.sign({ tenantId: 'a0000000-0000-4000-8000-000000000001', email: 'qa@x.test', ...claims }, pem, { algorithm: 'RS256', expiresIn: '5m' });
    const conn = { authorization: 'Bearer ' + tok({ userId: 'c0000000-0000-4000-8000-00000000000c', role: 'connector', authMethod: 'api_key', scopes: ['documents:read'] }) };
    const user = { authorization: 'Bearer ' + tok({ userId: 'u0000000-0000-4000-8000-00000000000u', role: 'user', authMethod: 'email' }) };
    // gdpr erasure refusal classes
    await probe('gdpr POST no auth', 'POST', '/api/gdpr/erasures');
    await probe('gdpr POST garbage bearer', 'POST', '/api/gdpr/erasures', { authorization: 'Bearer nope' });
    vi.stubEnv('SUBJECTS_ERASE_SCOPE_ENFORCED', 'true');
    await probe('gdpr POST connector no scope ENFORCED', 'POST', '/api/gdpr/erasures', conn);
    await probe('gdpr POST user jwt ENFORCED', 'POST', '/api/gdpr/erasures', user);
    await probe('gdpr POST trailing slash connector ENFORCED', 'POST', '/api/gdpr/erasures/', conn);
    await probe('gdpr POST //erasures connector ENFORCED', 'POST', '/api/gdpr//erasures', conn);
    await probe('gdpr GET ref connector ENFORCED', 'GET', '/api/gdpr/erasures/abc', conn, '');
    vi.stubEnv('SUBJECTS_ERASE_SCOPE_ENFORCED', '');
    // other audited routes
    await probe('logs POST (app.post, admitted 204)', 'POST', '/api/logs');
    await probe('logs POST v1 (version strip before audit)', 'POST', '/api/v1/logs');
    await probe('logs POST v1 query', 'POST', '/api/v1/logs?x=1');
    await probe('logs POST //api//logs (normaliser)', 'POST', '//api//logs');
    await probe('logs POST #frag', 'POST', '/api/logs#frag');
    await probe('logs POST absolute-form', 'POST', 'http://127.0.0.1/api/logs');
    await probe('documents POST no auth', 'POST', '/api/documents');
    await probe('documents POST v1 no auth', 'POST', '/api/v1/documents');
    await probe('v3 POST unsupported version', 'POST', '/api/v3/logs');
    await probe('batch POST (app.use prefix mount)', 'POST', '/api/batch/verify', user);
    await probe('notifications POST (app.use prefix mount)', 'POST', '/api/notifications/read-all', user);
    await probe('system POST status (prefix mount)', 'POST', '/api/system/status');
    await probe('auth login proxied', 'POST', '/api/auth/login', {}, '{"email":"QA@X.test","password":"p"}');
    await probe('auth login v1 proxied', 'POST', '/api/v1/auth/login', {}, '{"email":"QA@X.test","password":"p"}');
    await probe('integrations POST no auth', 'POST', '/api/integrations');
    await probe('users admin PATCH user', 'PATCH', '/api/users/admin/c0000000-0000-4000-8000-00000000000c', user);
    await probe('workflow approve user', 'POST', '/api/workflow-instances/c0000000-0000-4000-8000-00000000000c/approve', user);
    await probe('nonexistent POST 404', 'POST', '/api/qa-nonexistent/thing');
    await probe('verification v2 verify', 'POST', '/api/v2/verification/verify', {}, '{"hash":"' + 'a'.repeat(64) + '"}');
    rec.dbAvailable = false;
    await probe('logs POST isDbAvailable=false', 'POST', '/api/logs');
    rec.dbAvailable = true; rec.throwOnInsert = true;
    await probe('logs POST sink throws', 'POST', '/api/logs');
    await probe('gdpr POST no auth sink throws', 'POST', '/api/gdpr/erasures');
    rec.throwOnInsert = false;
    expect(rows.length).toBeGreaterThan(0);
  }, 120000);

  it('nested-mount fixture (TE): audit middleware under app.use("/gw", ...) and a gate under router.use', async () => {
    const { createAuditMiddleware } = await import('../middleware/audit');
    const calls: unknown[][] = [];
    const a = express();
    const inner = express.Router();
    inner.use(createAuditMiddleware({ query: async (_s, p) => { calls.push(p); return { rows: [] }; }, isDbAvailable: () => true, log: () => {} }));
    inner.use('/api/gate', (_req, res) => { res.status(403).json({ refused: true }); });
    inner.post('/api/ok', (_req, res) => { res.status(201).json({ ok: true }); });
    a.use('/gw', inner);
    const s = http.createServer(a); await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
    const p = (s.address() as AddressInfo).port;
    const send = (path: string) => new Promise<number>((resolve) => { const rq = http.request({ host: '127.0.0.1', port: p, path, method: 'POST' }, (res) => { res.resume(); resolve(res.statusCode ?? 0); }); rq.end(); });
    const out: unknown[] = [];
    for (const path of ['/gw/api/gate/x', '/gw/api/ok']) {
      const n = calls.length; const st = await send(path); await new Promise((r) => setTimeout(r, 200));
      out.push({ path, st, audits: calls.slice(n).map((c) => ({ action: c[3], resourceType: c[4], details: JSON.parse(String(c[8])) })) });
    }
    s.closeAllConnections(); await new Promise<void>((r) => s.close(() => r()));
    rows.push({ label: 'NESTED fixture', out });
    expect(out.length).toBe(2);
  });
});
