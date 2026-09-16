/**
 * qa1012-drafter-probe — RECORDING harness (not pass/fail) for the #1012 (KS-745) drafter. Runs inside services/security so the REAL security
 * app (SECURITY_DISABLE_BOOT=1, static RS256 key, no DB) serves GET /api/audit on loopback behind a hit counter; the REAL gateway
 * audit-export router is imported by relative path from the same tree. req.user on the gateway side is the token's DECODED claims
 * (NOT the real authenticateToken — the gate must use the real one); the upstream verifies the same token for real.
 */
import { describe, it, expect, vi } from 'vitest';
import crypto from 'crypto';
import http from 'http';
import type { AddressInfo } from 'net';
import express from 'express';
import fs from 'fs';

process.env.SECURITY_DISABLE_BOOT = '1';
const OUT = process.env.PROBE_OUT || '/dev/null';
const rows: any[] = [];
const rec = (r: any) => { rows.push(r); fs.writeFileSync(OUT, JSON.stringify(rows, null, 1)); };
const TA = 'a0000000-0000-4000-8000-0000000000aa', TB = 'b0000000-0000-4000-8000-0000000000bb', TC = 'c0000000-0000-4000-8000-0000000000cc';
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIV = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const PUB = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64 = (b: Buffer) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function tok(claims: Record<string, unknown>, expOffset = 300): string {
  const h = b64(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' }))); const now = Math.floor(Date.now() / 1000);
  const p = b64(Buffer.from(JSON.stringify({ sub: 'probe', iat: now - 600, exp: now + expOffset, ...claims })));
  return `${h}.${p}.${b64(crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), PRIV))}`;
}
const decode = (t: string) => JSON.parse(Buffer.from(t.split('.')[1], 'base64url').toString());
const listen = (app: any) => new Promise<http.Server>((r) => { const s = app.listen(0, '127.0.0.1', () => r(s)); });
const portOf = (s: http.Server) => (s.address() as AddressInfo).port;
function get(port: number, path: string, headers: Record<string, string> = {}, waitMs = 3000): Promise<{ status: number | string; text: string; ms: number }> {
  const t0 = Date.now();
  return new Promise((resolve) => {
    const req = http.get({ hostname: '127.0.0.1', port, path, headers }, (res) => { let d = ''; res.on('data', (c) => (d += c)); res.on('end', () => resolve({ status: res.statusCode ?? 0, text: d, ms: Date.now() - t0 })); });
    req.on('error', (e) => resolve({ status: 'ERR ' + e.message, text: '', ms: Date.now() - t0 }));
    setTimeout(() => { req.destroy(); resolve({ status: 'NO RESPONSE', text: '', ms: Date.now() - t0 }); }, waitMs);
  });
}
async function loadRouter(url: string) {
  process.env.SECURITY_SERVICE_URL = url; vi.resetModules();
  return (await import('../../../api-gateway/src/routes/audit-export')).default;
}
function gwApp(router: any, inject: boolean) {
  const app = express();
  if (inject) app.use((req, _res, next) => { const a = req.headers.authorization; if (a) { try { (req as any).user = decode(a.slice(7)); } catch { /* */ } } next(); });
  app.use('/api/admin/audit', router); return app;
}
const summarise = (text: string) => { try { const j = JSON.parse(text); return { tenants: Array.isArray(j.data) ? [...new Set(j.data.map((e: any) => e.tenantId))].sort() : undefined, n: Array.isArray(j.data) ? j.data.length : undefined, dataIsArray: Array.isArray(j.data), meta: j.meta, error: j.error, keys0: Array.isArray(j.data) && j.data[0] ? Object.keys(j.data[0]).sort() : undefined }; } catch { return { raw: text.slice(0, 200) }; } };

describe('qa1012 drafter probe', () => {
  it('records', async () => {
    process.env.JWT_PUBLIC_KEY = Buffer.from(PUB, 'utf8').toString('base64'); delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;
    const sec = (await import('../index')).default;
    const hits: string[] = [];
    const outer = express(); outer.use((req, _res, next) => { hits.push(req.method + ' ' + req.url); next(); }); outer.use(sec);
    const ss = await listen(outer); const SP = portOf(ss); const SURL = `http://127.0.0.1:${SP}`;
    const post = async (t: string, action: string) => (await fetch(`${SURL}/api/audit`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${t}` }, body: JSON.stringify({ action, resourceType: 'probe', details: { note: 'secret-detail-' + action } }) })).status;
    const seed: any = {};
    seed.A = [await post(tok({ role: 'ISSUER_ADMIN', tenantId: TA }), 'a1'), await post(tok({ role: 'ISSUER_ADMIN', tenantId: TA }), 'a2')];
    seed.B = [await post(tok({ role: 'ISSUER_ADMIN', tenantId: TB }), 'b1'), await post(tok({ role: 'ISSUER_ADMIN', tenantId: TB }), 'b2')];
    seed.platform = [await post(tok({ role: 'SUPER_ADMIN' }), 'p1')];
    seed.C60 = 0; for (let i = 0; i < 60; i++) if ((await post(tok({ role: 'ISSUER_ADMIN', tenantId: TC }), 'c' + i)) === 201) seed.C60++;
    rec({ row: 'SEED', seed, hitsAfterSeed: hits.length });
    const today = new Date().toISOString().slice(0, 10); const tomorrow = new Date(Date.now() + 86400000).toISOString().slice(0, 10);
    const router = await loadRouter(SURL);
    const gw = await listen(gwApp(router, true)); const GP = portOf(gw);
    const gwIdx = await listen(gwApp(router, false)); const GIP = portOf(gwIdx);
    const Q = `/api/admin/audit/export?from=2026-01-01&to=${tomorrow}&format=json`;
    const callers: [string, string | undefined][] = [
      ['ORG_ADMIN tenant A', tok({ role: 'ORG_ADMIN', tenantId: TA })], ['ORG_ADMIN tenant B', tok({ role: 'ORG_ADMIN', tenantId: TB })],
      ['super_admin NO tenant', tok({ role: 'super_admin' })], ['SYSTEM_ADMIN NO tenant', tok({ role: 'SYSTEM_ADMIN' })],
      ['SYSTEM_ADMIN tenant A', tok({ role: 'SYSTEM_ADMIN', tenantId: TA })],
      ['platform_admin NO tenant (the seat cell role)', tok({ role: 'platform_admin' })], ['platform_admin tenant B', tok({ role: 'platform_admin', tenantId: TB })],
      ['ORG_ADMIN NO tenant', tok({ role: 'ORG_ADMIN' })], ['ISSUER_ADMIN tenant A (not a gateway admin role)', tok({ role: 'ISSUER_ADMIN', tenantId: TA })],
      ['USER tenant A', tok({ role: 'USER', tenantId: TA })], ['no token', undefined],
      ['ORG_ADMIN tenant A EXPIRED', tok({ role: 'ORG_ADMIN', tenantId: TA }, -60)],
    ];
    for (const [label, t] of callers) {
      const h: Record<string, string> = t ? { Authorization: `Bearer ${t}` } : {};
      const h0 = hits.length; const r = await get(GP, Q, h);
      rec({ row: 'EXPORT ' + label, mount: 'req.user = decoded claims', status: r.status, hits: hits.slice(h0), ...summarise(r.text) });
      const h1 = hits.length; const ri = await get(GIP, Q, h);
      rec({ row: 'EXPORT ' + label, mount: 'index.ts:801 shape (no auth middleware)', status: ri.status, hits: hits.slice(h1), ...summarise(ri.text) });
    }
    const orgA = { Authorization: `Bearer ${tok({ role: 'ORG_ADMIN', tenantId: TA })}` }; const orgC = { Authorization: `Bearer ${tok({ role: 'ORG_ADMIN', tenantId: TC })}` };
    for (const ty of ['auth', 'billing', 'all']) { const r = await get(GP, `/api/admin/audit/export?from=2026-01-01&to=${tomorrow}&format=json&type=${ty}`, orgA); rec({ row: 'RESIDUAL type=' + ty, status: r.status, ...summarise(r.text) }); }
    { const h0 = hits.length; const r = await get(GP, `/api/admin/audit/export?from=2026-01-01&to=${tomorrow}&format=json`, orgC); rec({ row: 'RESIDUAL limit: tenant C seeded 60', status: r.status, hits: hits.slice(h0), ...summarise(r.text) });
      const d = await fetch(`${SURL}/api/audit?from=2026-01-01&to=${tomorrow}`, { headers: orgC }); const j: any = await d.json(); rec({ row: 'RESIDUAL limit: direct list total', status: d.status, total: j.data?.total, returned: j.data?.logs?.length, limit: j.data?.limit }); }
    for (const [lbl, to] of [['to=today (UTC date, entries created today)', today], ['to=tomorrow', tomorrow]]) { const r = await get(GP, `/api/admin/audit/export?from=${today}&to=${to}&format=json`, orgA); rec({ row: 'RESIDUAL date ' + lbl, today, status: r.status, ...summarise(r.text) }); }
    { const r = await get(GP, `/api/admin/audit/export?from=2026-01-01&to=${tomorrow}&format=csv`, orgA); rec({ row: 'CSV shape ORG_ADMIN tenant A', status: r.status, csv: r.text.slice(0, 600) }); }
    // upstream failure shapes
    const fake = (fn: (req: http.IncomingMessage, res: http.ServerResponse) => void) => { const s = http.createServer(fn); return new Promise<http.Server>((r) => s.listen(0, '127.0.0.1', () => r(s))); };
    const FAIL: [string, ((req: any, res: any) => void) | 'closed'][] = [
      ['401 upstream', (_q, s) => { s.writeHead(401, { 'Content-Type': 'application/json' }); s.end(JSON.stringify({ success: false, error: { code: 'UNAUTHORIZED', message: 'UPSTREAM-MARKER-401 internal detail' } })); }],
      ['403 upstream', (_q, s) => { s.writeHead(403, { 'Content-Type': 'application/json' }); s.end(JSON.stringify({ success: false, error: 'UPSTREAM-MARKER-403 string error' })); }],
      ['404 upstream (base path shape)', (_q, s) => { s.writeHead(404, { 'Content-Type': 'application/json' }); s.end(JSON.stringify({ success: false, error: { code: 'NOT_FOUND', message: 'Audit log not found' } })); }],
      ['500 upstream html', (_q, s) => { s.writeHead(500, { 'Content-Type': 'text/html' }); s.end('<pre>UPSTREAM-MARKER-500 stack at /app/src/index.ts:77</pre>'); }],
      ['200 malformed body', (_q, s) => { s.writeHead(200, { 'Content-Type': 'application/json' }); s.end('{not json UPSTREAM-MARKER-MAL'); }],
      ['200 unexpected shape {data:[...]} (pre-fix read shape)', (_q, s) => { s.writeHead(200, { 'Content-Type': 'application/json' }); s.end(JSON.stringify({ success: true, data: [{ id: 'x' }] })); }],
      ['accepts, never answers', () => { /* hang */ }],
      ['closed port', 'closed'],
    ];
    for (const [lbl, fn] of FAIL) {
      let url = 'http://127.0.0.1:1'; let fsrv: http.Server | undefined;
      if (fn !== 'closed') { fsrv = await fake(fn); url = `http://127.0.0.1:${portOf(fsrv)}`; }
      const rtr = await loadRouter(url); const g = await listen(gwApp(rtr, true));
      const r = await get(portOf(g), Q, orgA, 4000);
      rec({ row: 'UPSTREAM ' + lbl, status: r.status, ms: r.ms, body: r.text.slice(0, 300), markerLeaks: /UPSTREAM-MARKER/.test(r.text) });
      (g as any).closeAllConnections?.(); g.close(); if (fsrv) { (fsrv as any).closeAllConnections?.(); fsrv.close(); }
    }
    for (const s of [gw, gwIdx, ss]) { (s as any).closeAllConnections?.(); s.close(); }
    expect(rows.length).toBeGreaterThan(0);
  }, 60_000);
});
