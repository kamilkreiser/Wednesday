/**
 * qa1011-census — QA GATE instrument for #1011 (KS-871). NOT a product test; placed only in the QA clone's worktrees, quarantined by rename after.
 * REAL app (index.ts default export) + real audit middleware; ../db mocked (isDbAvailable/throw/hang switchable, query a recorder with a hit witness).
 * Requests come from QA1011_REQ (JSON); each is a RAW request line on a loopback socket with a unique User-Agent that the audit row carries,
 * so rows are matched to requests by UA, never by timing. 307s are followed once (production client). Output -> QA1011_OUT.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import net from 'net';
import fs from 'fs';
import jwt from 'jsonwebtoken';
import type { AddressInfo } from 'net';

const rec = vi.hoisted(() => ({ mockLoaded: false, calls: [] as { sql: string; params: unknown[]; t: number }[], dbAvailable: true, mode: 'ok' as 'ok' | 'throw' | 'hang' }));
vi.mock('../db', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  rec.mockLoaded = true;
  return {
    ...real,
    isDbAvailable: () => rec.dbAvailable,
    query: async (sql: string, params: unknown[] = []) => {
      rec.calls.push({ sql, params, t: Date.now() });
      if (/INSERT INTO audit_logs/.test(sql)) {
        if (rec.mode === 'throw') throw new Error('qa1011 sink threw');
        if (rec.mode === 'hang') return new Promise(() => {});
      }
      return { rows: [], rowCount: 0 };
    },
  };
});

type Req = { upstatus?: number; i: number; label: string; method: string; target: string; auth?: string; body?: string; env?: Record<string, string>; xff?: string; mode?: string; db?: boolean };
const REQS: Req[] = JSON.parse(fs.readFileSync(process.env.QA1011_REQ as string, 'utf8'));
const results: unknown[] = [];
let upstream: http.Server; const upSeen: { ua: string; line: string }[] = [];
let gw: http.Server; let port = 0;

function raw(method: string, target: string, headers: Record<string, string>, body: string): Promise<{ status: number; headers: [string, string][]; body: string; ms: number }> {
  return new Promise((resolve) => {
    const t0 = Date.now(); const s = net.connect(port, '127.0.0.1'); const chunks: Buffer[] = [];
    const done = (status: number) => {
      const buf = Buffer.concat(chunks).toString('latin1'); const idx = buf.indexOf('\r\n\r\n');
      const head = idx === -1 ? buf : buf.slice(0, idx); const lines = head.split('\r\n'); const m = (lines[0] || '').match(/^HTTP\/1\.1 (\d{3})/);
      resolve({ status: m ? Number(m[1]) : status, headers: lines.slice(1).map((l) => { const k = l.indexOf(':'); return [l.slice(0, k).toLowerCase(), l.slice(k + 1).trim()] as [string, string]; }), body: idx === -1 ? '' : buf.slice(idx + 4), ms: Date.now() - t0 });
    };
    s.setTimeout(5000, () => { s.destroy(); done(-3); });
    s.on('data', (d) => chunks.push(d)); s.on('end', () => done(-1)); s.on('error', () => done(-2));
    const h = { host: '127.0.0.1', connection: 'close', 'content-type': 'application/json', 'content-length': String(Buffer.byteLength(body)), ...headers };
    s.write(`${method} ${target} HTTP/1.1\r\n` + Object.entries(h).map(([k, v]) => `${k}: ${v}`).join('\r\n') + '\r\n\r\n' + body);
  });
}
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

beforeAll(async () => {
  upstream = http.createServer((req, res) => { req.resume(); req.on('end', () => { upSeen.push({ ua: String(req.headers['user-agent']), line: `${req.method} ${req.url}` }); const st = Number(req.headers['x-qa-upstatus'] || 200); res.writeHead(st, { 'content-type': 'application/json' }); res.end(st === 200 ? '{"up":true}' : '{"success":false,"error":{"code":"VALIDATION_ERROR"}}'); }); });
  await new Promise<void>((r) => upstream.listen(0, '127.0.0.1', () => r()));
  const upUrl = `http://127.0.0.1:${(upstream.address() as AddressInfo).port}`;
  for (const n of (process.env.QA1011_SVC_ENVS || '').split(',').filter(Boolean)) vi.stubEnv(n, upUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  const app = (await import('../index')).default;
  gw = http.createServer(app as http.RequestListener);
  await new Promise<void>((r) => gw.listen(0, '127.0.0.1', () => r()));
  port = (gw.address() as AddressInfo).port;
}, 60000);

afterAll(async () => {
  if (gw) { gw.closeAllConnections(); await new Promise<void>((r) => gw.close(() => r())); }
  if (upstream) { upstream.closeAllConnections(); await new Promise<void>((r) => upstream.close(() => r())); }
});

describe('qa1011 census', () => {
  it('drives every request through the real app and records the audit rows', async () => {
    const pem = process.env.__TEST_JWT_PRIVATE_PEM || '';
    const tok = (claims: object) => 'Bearer ' + jwt.sign({ tenantId: 'a0000000-0000-4000-8000-000000000001', email: 'qa@x.test', organizationId: 'd0000000-0000-4000-8000-00000000000d', verificationLevel: 'BASIC', ...claims }, pem, { algorithm: 'RS256', expiresIn: '10m' });
    const AUTH: Record<string, string> = {
      user: tok({ userId: 'b0000000-0000-4000-8000-00000000000b', role: 'user', authMethod: 'email' }),
      admin: tok({ userId: 'e0000000-0000-4000-8000-00000000000e', role: 'admin', authMethod: 'email' }),
      conn: tok({ userId: 'c0000000-0000-4000-8000-00000000000c', role: 'connector', authMethod: 'api_key', scopes: ['documents:read'] }),
      connscope: tok({ userId: 'c0000000-0000-4000-8000-00000000000c', role: 'connector', authMethod: 'api_key', scopes: ['documents:read', 'subjects:erase'] }),
      garbage: 'Bearer nope',
    };
    const nodeEnv = process.env.NODE_ENV;
    for (const r of REQS) {
      if (r.mode !== undefined || r.db !== undefined) { await sleep(400); rec.mode = (r.mode as 'ok') || 'ok'; rec.dbAvailable = r.db !== false; }
      const envPrev: [string, string | undefined][] = [];
      for (const [k, v] of Object.entries(r.env || {})) { envPrev.push([k, process.env[k]]); process.env[k] = v; }
      const ua = `qa1011-${r.i}`;
      const headers: Record<string, string> = { 'user-agent': ua, 'x-forwarded-for': r.xff || `10.11.${Math.floor(r.i / 250)}.${r.i % 250}` };
      if (r.auth) headers.authorization = AUTH[r.auth];
      if (r.upstatus) headers['x-qa-upstatus'] = String(r.upstatus);
      const body = r.body ?? '{}';
      const hops = [] as unknown[];
      let h = await raw(r.method, r.target, headers, body); hops.push({ target: r.target, ...h });
      if (h.status === 307) {
        const loc = (h.headers.find(([k]) => k === 'location') || [])[1];
        if (loc) { const h2 = await raw(r.method, loc, { ...headers, 'user-agent': ua + '~f' }, body); hops.push({ target: loc, ...h2 }); }
      }
      if (envPrev.length) { await sleep(60); for (const [k, v] of envPrev) { if (v === undefined) delete process.env[k]; else process.env[k] = v; } }
      results.push({ ...r, ua, hops });
    }
    await sleep(1500);
    const inserts = rec.calls.filter((c) => /INSERT INTO audit_logs/.test(c.sql)).map((c) => {
      const p = c.params as unknown[]; let details: unknown = p[8];
      try { details = JSON.parse(String(p[8])); if (details && typeof details === 'object') delete (details as Record<string, unknown>).durationMs; } catch { /* raw */ }
      return { tenant: p[0], user: p[1], org: p[2], action: p[3], resourceType: p[4], resourceId: p[5], ip: p[6], ua: p[7], details, success: p[9] };
    });
    fs.writeFileSync(process.env.QA1011_OUT as string, JSON.stringify({ meta: { nodeEnv, mockLoaded: rec.mockLoaded, queryCalls: rec.calls.length, inserts: inserts.length, requests: REQS.length }, results, inserts, upSeen }, null, 1));
    expect(rec.mockLoaded).toBe(true);
    expect(results.length).toBe(REQS.length);
  }, 900000);
});
