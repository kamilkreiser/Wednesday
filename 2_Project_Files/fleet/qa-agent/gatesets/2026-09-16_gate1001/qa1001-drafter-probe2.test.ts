/**
 * DRAFTER FEASIBILITY PROBE for the #1001 (KS-1165) tier-1 gate set — NOT a product test, never enters the checkout.
 * Imports the REAL app exported by index.ts (the ks1041-edge-strip-wiring.test.ts pattern) with NODE_ENV stubbed to
 * 'development' BEFORE import, so index.ts:387-390 mounts csrfMiddleware.generateToken + protect (they are skipped
 * under NODE_ENV=test, which is vitest's default). originate is pointed at a local recorder. Each row sends ONE raw
 * http.request and records: status, error.code, whether the recorder saw it, and the upstream url.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import type { AddressInfo } from 'net';
import { writeFileSync } from 'fs';

let recorder: http.Server; let recorderUrl = ''; let gateway: http.Server; let gatewayUrl = '';
const seen: string[] = [];
async function listen(server: http.Server): Promise<string> {
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
  return `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}
function send(method: string, rawPath: string, headers: Record<string, string>, body: string): Promise<{ status: number; code: string | null }> {
  return new Promise((resolve, reject) => {
    const t = new URL(gatewayUrl);
    const req = http.request({ hostname: t.hostname, port: t.port, path: rawPath, method, headers: { ...headers, 'content-length': String(Buffer.byteLength(body)) }, agent: false }, (res) => {
      const chunks: Buffer[] = []; res.on('data', (c) => chunks.push(c));
      res.on('end', () => { let code: string | null = null; try { code = JSON.parse(Buffer.concat(chunks).toString())?.error?.code ?? null; } catch { code = null; } resolve({ status: res.statusCode ?? 0, code }); });
    });
    req.on('error', reject); req.end(body);
  });
}
const JSON_BODY = JSON.stringify({ hash: 'a'.repeat(64) });
const COOKIE = { cookie: 'session=ambient', 'content-type': 'application/json' };
const ROWS: Array<[string, string, Record<string, string>, string]> = [
  ['v2-verify', '/api/v2/verification/verify', COOKIE, JSON_BODY],
  ['v2-verify-file-octet', '/api/v2/verification/verify-file', { cookie: 'session=ambient', 'content-type': 'application/octet-stream' }, 'raw document bytes'],
  ['v1-verify', '/api/verification/verify', COOKIE, JSON_BODY],
  ['neighbour-documents', '/api/documents', COOKIE, JSON_BODY],
  ['neighbour-v1-hash', '/api/verification/hash', COOKIE, JSON_BODY],
  ['neighbour-v2-root', '/api/v2/verification', COOKIE, JSON_BODY],
  ['prefix-verifyX', '/api/v2/verification/verifyX', COOKIE, JSON_BODY],
  ['prefix-verify-slash-x', '/api/v2/verification/verify/x', COOKIE, JSON_BODY],
  ['trailing-slash', '/api/v2/verification/verify/', COOKIE, JSON_BODY],
  ['query', '/api/v2/verification/verify?x=1', COOKIE, JSON_BODY],
  ['case-API', '/API/v2/verification/verify', COOKIE, JSON_BODY],
  ['case-Verify', '/api/v2/verification/Verify', COOKIE, JSON_BODY],
  ['encoded-%76erify', '/api/v2/verification/%76erify', COOKIE, JSON_BODY],
  ['double-slash', '//api/v2/verification/verify', COOKIE, JSON_BODY],
  ['dot-segment-to-documents', '/api/v2/verification/verify/../../../documents', COOKIE, JSON_BODY],
  ['v1-alias', '/api/v1/verification/verify', COOKIE, JSON_BODY],
  ['v1-dot-segment-to-documents', '/api/verification/verify/../../documents', COOKIE, JSON_BODY],
  ['neighbour-documents-octet', '/api/documents', { cookie: 'session=ambient', 'content-type': 'application/octet-stream' }, 'raw document bytes'],
  ['v2-verify-evil-origin', '/api/v2/verification/verify', { ...COOKIE, origin: 'https://evil.example' }, JSON_BODY],
  ['neighbour-documents-evil-origin', '/api/documents', { ...COOKIE, origin: 'https://evil.example' }, JSON_BODY],
  ['v2-verify-no-cookie', '/api/v2/verification/verify', { 'content-type': 'application/json' }, JSON_BODY],
  ['neighbour-documents-no-cookie', '/api/documents', { 'content-type': 'application/json' }, JSON_BODY],
];

beforeAll(async () => {
  recorder = http.createServer((req, res) => { seen.push(req.url || ''); res.writeHead(200, { 'content-type': 'application/json' }); res.end('{"recorder":true}'); });
  recorderUrl = await listen(recorder);
  vi.resetModules();
  vi.stubEnv('NODE_ENV', 'development');
  vi.stubEnv('ORIGINATE_SERVICE_URL', recorderUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  const mod = await import('../index');
  gateway = http.createServer((mod as { default: http.RequestListener }).default);
  gatewayUrl = await listen(gateway);
}, 60000);
afterAll(async () => {
  if (gateway) await new Promise<void>((r) => gateway.close(() => r()));
  if (recorder) await new Promise<void>((r) => recorder.close(() => r()));
  vi.unstubAllEnvs();
});

describe('drafter probe — the real app, NODE_ENV=development', () => {
  it('the CSRF layers are mounted in the imported app (control: without them every row below is meaningless)', async () => {
    const mod: any = await import('../index');
    const names = (mod.default._router?.stack ?? []).map((l: any) => l.name);
    writeFileSync(process.env.QA_PROBE_OUT_STACK || '/dev/null', JSON.stringify(names, null, 1));
    expect(names.filter((n: string) => n === 'protectMiddleware' || n === 'generateTokenMiddleware').length).toBe(2);
  });
  it('matrix', async () => {
    const out: any[] = [];
    for (const [id, p, h, b] of ROWS) {
      const before = seen.length;
      const r = await send('POST', p, h, b);
      out.push({ id, path: p, status: r.status, code: r.code, reachedUpstream: seen.length > before, upstreamUrl: seen.length > before ? seen[seen.length - 1] : null });
    }
    writeFileSync(process.env.QA_PROBE_OUT || '/dev/null', JSON.stringify(out, null, 1));
    expect(out.length).toBe(ROWS.length);
  }, 60000);
});
