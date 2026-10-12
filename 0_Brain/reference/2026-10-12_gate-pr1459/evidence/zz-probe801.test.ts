// QA gate probe (scratch only, never committed): path-shape matrix over the REAL app.
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import net from 'net';
import { writeFileSync } from 'node:fs';
import type { AddressInfo } from 'net';

const SERVICE_URLS = ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM',
  'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET'].map((n) => `${n}_SERVICE_URL`);
const seen: Array<{ tag: string; url: string; type: string; len: number }> = [];
let seq = 0;
let recorder: http.Server; let recUrl = '';
async function listen(s: http.Server) { await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r())); return `http://127.0.0.1:${(s.address() as AddressInfo).port}`; }

async function boot(env: string) {
  for (const k of SERVICE_URLS) vi.stubEnv(k, recUrl);
  vi.stubEnv('NODE_ENV', env); vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  vi.resetModules();
  const app = (await import('../index')).default;
  const s = http.createServer(app as http.RequestListener);
  return { s, url: await listen(s) };
}

function raw(base: string, path: string, headers: Record<string, string>, body: string): Promise<string> {
  const u = new URL(base); const tag = `q${++seq}`;
  return new Promise((resolve) => {
    const sock = net.connect(Number(u.port), u.hostname, () => {
      const h = Object.entries({ ...headers, host: u.host, 'x-ks801-probe': tag, 'content-length': String(Buffer.byteLength(body)), connection: 'close' })
        .map(([k, v]) => `${k}: ${v}`).join('\r\n');
      sock.write(Buffer.concat([Buffer.from(`POST `, 'latin1'), Buffer.from(path, 'utf8'), Buffer.from(` HTTP/1.1\r\n${h}\r\n\r\n${body}`, 'latin1')]));
    });
    const ch: Buffer[] = [];
    sock.on('data', (c) => ch.push(c));
    sock.on('close', () => {
      const t = Buffer.concat(ch).toString();
      const status = t.slice(9, 12);
      let code = '';
      const m = t.match(/"code":"([A-Z_]+)"/); if (m) code = m[1];
      const hits = seen.filter((x) => x.tag === tag);
      resolve(`${status} ${code || '-'} hits=${hits.length}${hits.length ? ' up=' + hits.map((x) => `${x.url}[${x.type};${x.len}]`).join(',') : ''}`);
    });
    sock.on('error', (e) => resolve('ERR ' + e.message));
  });
}

beforeAll(async () => {
  recorder = http.createServer((req, res) => {
    const ch: Buffer[] = []; req.on('data', (c) => ch.push(c));
    req.on('end', () => { seen.push({ tag: String(req.headers['x-ks801-probe'] ?? ''), url: req.url ?? '', type: String(req.headers['content-type'] ?? ''), len: Buffer.concat(ch).length }); res.writeHead(200, { 'content-type': 'application/json' }); res.end('{}'); });
  });
  recUrl = await listen(recorder);
});
afterAll(() => { recorder?.closeAllConnections(); recorder?.close(); vi.unstubAllEnvs(); });

const TXT = { 'content-type': 'text/plain' };
const FORM = { 'content-type': 'application/x-www-form-urlencoded' };
const OCT = { 'content-type': 'application/octet-stream' };
const CK = { cookie: 'session=ambient', 'content-type': 'application/json' };

describe('probe', () => {
  it('guard + parse matrix (test env)', async () => {
    const g = await boot('test');
    const out: Record<string, string> = {};
    const rows: Array<[string, Record<string, string>, string]> = [
      ['/api/oauth/apps', TXT, 'x'], ['/API/OAUTH/APPS', TXT, 'x'], ['/api/oauth/apps/', TXT, 'x'], ['/API/oauth/apps/', TXT, 'x'],
      ['//API//oauth//apps', TXT, 'x'], ['/%61pi/oauth/apps', TXT, 'x'], ['/%41PI/oauth/apps', TXT, 'x'], ['/api/%6Fauth/apps', TXT, 'x'],
      ['/api/oauth%2Fapps', TXT, 'x'], ['/api/oauth/apps;x', TXT, 'x'], ['/api/oauth/apps?x=1', TXT, 'x'], ['/api/v1/oauth/apps', TXT, 'x'],
      ['/API/V1/oauth/apps', TXT, 'x'], ['/api/V1/oauth/apps', TXT, 'x'], ['/./api/oauth/apps', TXT, 'x'], ['/x/../api/oauth/apps', TXT, 'x'],
      ['/api\\oauth\\apps', TXT, 'x'], ['/api/oauth/token', FORM, 'grant_type=client_credentials'], ['/API/OAUTH/TOKEN', FORM, 'grant_type=client_credentials'],
      ['/api/oauth/token/', FORM, 'grant_type=client_credentials'], ['/api/v1/oauth/token', FORM, 'grant_type=client_credentials'],
      ['/api/oauth/toKen', FORM, 'grant_type=client_credentials'], ['/api/oauth/%74oken', FORM, 'grant_type=client_credentials'],
      ['/api/verification/verify-file', OCT, 'bytes'], ['/API/Verification/Verify-File', OCT, 'bytes'], ['/api/verification/verify-file/', OCT, 'bytes'],
      ['/api/v1/verification/verify-file', OCT, 'bytes'], ['/api/documents', TXT, 'x'], ['/API/DOCUMENTS', TXT, 'x'],
      ['/api/auth/login', { 'content-type': 'application/json' }, '{"email":"a@b.c","password":"x"}'],
      ['/API/AUTH/LOGIN', { 'content-type': 'application/json' }, '{"email":"a@b.c","password":"x"}'],
      ['/api/anchors', { 'content-type': 'application/json' }, '{"a":1}'], ['/API/ANCHORS', { 'content-type': 'application/json' }, '{"a":1}'],
      ['/api/webhooKs', TXT, 'x'], ['/Kpi/oauth/apps', TXT, 'x'],
    ];
    for (const [p, h, b] of rows) out[`${p} ${h['content-type']}`] = await raw(g.url, p, h, b);
    writeFileSync(process.env.PROBE_OUT + '.guard.json', JSON.stringify(out, null, 1));
    g.s.closeAllConnections(); g.s.close();
  }, 120000);

  it('csrf matrix (development env)', async () => {
    const g = await boot('development');
    const out: Record<string, string> = {};
    for (const p of ['/api/verification/verify', '/API/VERIFICATION/VERIFY', '/api/verification/verify/', '/api/v1/verification/verify',
      '/API/V1/verification/verify', '/api/%76erification/verify', '/api/verification/verifyX', '/api/auth/login', '/API/AUTH/LOGIN',
      '/api/auth/loginx', '/api/documents', '/API/DOCUMENTS', '/health', '/HEALTH', '/api/v2/verification/verify', '/API/V2/VERIFICATION/VERIFY']) {
      out[p] = await raw(g.url, p, CK, '{}');
    }
    writeFileSync(process.env.PROBE_OUT + '.csrf.json', JSON.stringify(out, null, 1));
    g.s.closeAllConnections(); g.s.close();
  }, 120000);
});
