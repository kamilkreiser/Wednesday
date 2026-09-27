import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
process.env.SECURITY_DISABLE_BOOT = '1';
const out = (...a: unknown[]) => require('fs').appendFileSync('/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/ks888brief/probe.log', JSON.stringify(a) + '\n');
const TENANT_A = 'a0000000-0000-4000-8000-0000000000aa';
const ORG_A = '11111111-1111-4111-8111-111111111111';
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64url = (b: Buffer): string => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function token(claims: Record<string, unknown>): string {
  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const payload = b64url(Buffer.from(JSON.stringify({ sub: 'test-user', iat: now, exp: now + 300, ...claims })));
  const signature = b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM));
  return `${header}.${payload}.${signature}`;
}
const state = vi.hoisted(() => ({ fail: null as string | null, calls: [] as string[] }));
vi.mock('../db', () => ({
  isDbAvailable: () => true,
  initDb: async () => true,
  query: async (sql: string) => {
    state.calls.push(sql.slice(0, 40));
    if (/INSERT INTO svc_api_keys/.test(sql) && state.fail) throw Object.assign(new Error('boom'), { code: state.fail });
    return { rows: [], rowCount: 0 };
  },
}));
let server: Server; let base = '';
beforeAll(async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;
  const app = (await import('../index')).default;
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', r); });
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});
afterAll(async () => { await new Promise<void>((r) => server.close(() => r())); });
const mint = () => fetch(`${base}/api/keys`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token({ role: 'super_admin' })}` }, body: JSON.stringify({ name: 'p', organizationId: ORG_A, tenantId: TENANT_A, scopes: ['documents:read'] }) });
describe('probe', () => {
  it('mint', async () => {
    state.fail = '42703'; const r = await mint(); out('MINT42', r.status, await r.text()); state.fail = null;
    state.fail = '08006'; const r2 = await mint(); out('MINT08', r2.status); state.fail = null;
  });
  it('validate-active', async () => {
    const r = await mint(); const b: any = await r.json();
    state.fail = '42703';
    try { const v = await fetch(`${base}/api/keys/validate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key: b.data.key }), signal: AbortSignal.timeout(3000) }); out('VALACTIVE', v.status, await v.text()); } catch (e) { out('VALACTIVE-ERR', String(e)); }
    state.fail = null;
  });
  it('delete', async () => {
    const r = await mint(); const b: any = await r.json(); out('MINTOK', r.status, state.calls.filter(c=>/INSERT INTO svc_api/.test(c)).length);
    state.fail = '42703';
    const ac = new AbortController(); const t = setTimeout(() => ac.abort(), 3000);
    try { const d = await fetch(`${base}/api/keys/${b.data.id}`, { method: 'DELETE', headers: { Authorization: `Bearer ${token({ role: 'super_admin' })}` }, signal: ac.signal }); out('DEL', d.status, await d.text()); } catch (e) { out('DEL-ERR', String(e)); }
    clearTimeout(t);
    try { const v = await fetch(`${base}/api/keys/validate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key: b.data.key }), signal: AbortSignal.timeout(3000) }); out('VAL', v.status, await v.text()); } catch (e) { out('VAL-ERR', String(e)); }
    state.fail = null;
  });
});
