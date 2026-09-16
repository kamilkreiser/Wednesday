/** qa1012-drafter-realapp — RECORDING: the REAL gateway app (index.ts, as ks1165 imports it) with a recording upstream as SECURITY_SERVICE_URL.
 * Does a valid RS256 admin token (vitest.setup.ts throwaway key) reach the export's fetch through index.ts:801? Control: the same token on
 * a route that DOES run authenticateToken (GET /api/admin/audit-logs, admin.ts requireAdmin). */
import { describe, it, expect, vi } from 'vitest';
import http from 'http';
import crypto from 'crypto';
import fs from 'fs';
import type { AddressInfo } from 'net';
const OUT = process.env.PROBE_OUT || '/dev/null'; const rows: any[] = [];
const b64 = (b: Buffer) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function tok(claims: Record<string, unknown>) { const h = b64(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' }))); const now = Math.floor(Date.now() / 1000);
  const p = b64(Buffer.from(JSON.stringify({ sub: 'u-probe', userId: 'u-probe', email: 'p@example.invalid', iat: now, exp: now + 300, ...claims })));
  return `${h}.${p}.${b64(crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), process.env.__TEST_JWT_PRIVATE_PEM as string))}`; }
function get(port: number, path: string, headers: Record<string, string>): Promise<{ status: number | string; text: string }> {
  return new Promise((resolve) => { const r = http.get({ hostname: '127.0.0.1', port, path, headers, agent: false }, (res) => { let d = ''; res.on('data', (c) => (d += c)); res.on('end', () => resolve({ status: res.statusCode ?? 0, text: d.slice(0, 300) })); });
    r.on('error', (e) => resolve({ status: 'ERR ' + e.message, text: '' })); setTimeout(() => { r.destroy(); resolve({ status: 'NO RESPONSE', text: '' }); }, 5000); });
}
describe('qa1012 real app', () => {
  it('records', async () => {
    const seen: string[] = [];
    const rec = http.createServer((req, res) => { seen.push(req.method + ' ' + req.url + ' auth=' + (req.headers.authorization ? 'present' : 'absent')); res.writeHead(200, { 'content-type': 'application/json' }); res.end(JSON.stringify({ success: true, data: { logs: [{ id: 'rec-1', tenantId: 't' }], total: 1, limit: 50, offset: 0 } })); });
    await new Promise<void>((r) => rec.listen(0, '127.0.0.1', () => r())); const RU = `http://127.0.0.1:${(rec.address() as AddressInfo).port}`;
    vi.resetModules(); vi.stubEnv('SECURITY_SERVICE_URL', RU); vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
    const app = (await import('../index')).default; const gw = http.createServer(app as http.RequestListener);
    await new Promise<void>((r) => gw.listen(0, '127.0.0.1', () => r())); const GP = (gw.address() as AddressInfo).port;
    for (const [lbl, claims] of [['super_admin tenant A', { role: 'super_admin', tenantId: 'a0000000-0000-4000-8000-0000000000aa' }], ['SYSTEM_ADMIN no tenant', { role: 'SYSTEM_ADMIN' }], ['ORG_ADMIN tenant A', { role: 'ORG_ADMIN', tenantId: 'a0000000-0000-4000-8000-0000000000aa' }]] as [string, any][]) {
      const H = { Authorization: `Bearer ${tok(claims)}` };
      for (const path of ['/api/admin/audit/export?from=2026-01-01&to=2026-12-31&format=json', '/api/v1/admin/audit/export?from=2026-01-01&to=2026-12-31&format=json', '/api/admin/audit-logs']) {
        const s0 = seen.length; const r = await get(GP, path, H); rows.push({ caller: lbl, path, status: r.status, body: r.text, upstreamHits: seen.slice(s0) });
      }
    }
    { const s0 = seen.length; const r = await get(GP, '/api/admin/audit/export?from=2026-01-01&to=2026-12-31&format=json', {}); rows.push({ caller: 'no token', path: '/api/admin/audit/export', status: r.status, body: r.text, upstreamHits: seen.slice(s0) }); }
    fs.writeFileSync(OUT, JSON.stringify(rows, null, 1));
    (gw as any).closeAllConnections?.(); gw.close(); rec.close();
    expect(rows.length).toBeGreaterThan(0);
  }, 60_000);
});
