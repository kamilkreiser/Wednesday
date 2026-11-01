// gate 92 probe: REAL express 4 over a real loopback socket; only api-client, hashing and package-generator replaced.
import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
import { writeFileSync } from 'node:fs';
const st = vi.hoisted(() => ({ val: undefined as unknown, mode: 'throw' }));
vi.mock('../api-client.js', () => {
  const f = () => Promise.reject(st.val);
  return { registerDocument: f, verifyDocument: f, listDocuments: f, getWorkflowInstance: f, getConnectorInfo: f, getVerificationPolicy: f };
});
vi.mock('../hashing.js', () => ({ hashFile: () => Promise.resolve('h'), extractFileName: (p: string) => p, hashBuffer: () => 'h' }));
vi.mock('../package-generator.js', () => ({ generatePackage: () => Promise.reject(st.val) }));
vi.mock('@secuura/shared', () => ({ enforceProductionConfig: () => undefined, rejectNulBytes: () => (_a: unknown, _b: unknown, n: () => void) => n() }));
const PORT = 17891;
process.env.MCP_HTTP_PORT = String(PORT);
const unhandled: string[] = [];
const logs: string[] = [];
const origErr = console.error;
process.on('unhandledRejection', (r) => { unhandled.push('UR'); });
const rows: unknown[] = [];
const routes: Array<[string, string, unknown]> = [
  ['POST', '/register', { title: 't', documentType: 'd', contentHash: 'h' }],
  ['POST', '/verify', { documentId: 'x', hash: 'h' }],
  ['GET', '/documents', undefined], ['GET', '/workflow/abc', undefined], ['GET', '/connector', undefined], ['GET', '/policy', undefined],
  ['POST', '/generate-package', { agentType: 'cursor', apiKey: 'k' }],
  ['POST', '/register-batch', { documents: [{ title: 't', documentType: 'd', contentHash: 'h' }] }],
  ['POST', '/verify-batch', { documents: [{ documentId: 'x', hash: 'h' }] }],
];
const vals: Array<[string, () => unknown]> = [
  ['ordinary Error', () => new Error('ordinary boom 10.0.0.7')],
  ['revoked Proxy', () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }],
  ['getter Error', () => Object.create(Error.prototype, { message: { get() { throw new Error('g'); } } })],
  ['string', () => 'S3CR3T-STR'],
  ['object', () => ({ secretField: 'S3CR3T-VAL', other: 1 })],
];
beforeAll(async () => {
  console.error = (...a: unknown[]) => { logs.push(a.map((x) => (typeof x === 'string' ? x : '<<' + typeof x + '>>')).join(' ')); };
  await import('../http-server.js');
  await new Promise((r) => setTimeout(r, 300));
});
afterAll(() => { console.error = origErr; writeFileSync(process.env.PROBE_OUT as string, JSON.stringify(rows, null, 1)); });
describe('real express', () => {
  for (const [m, p, body] of routes) for (const [vn, mk] of vals) {
    it(`${m} ${p} ${vn}`, async () => {
      st.val = mk(); logs.length = 0; const u0 = unhandled.length;
      let status: number | string = 'NO-RESPONSE'; let text = '';
      try {
        const r = await fetch(`http://127.0.0.1:${PORT}${p}`, { method: m, headers: { 'content-type': 'application/json' }, body: body ? JSON.stringify(body) : undefined, signal: AbortSignal.timeout(1500) });
        status = r.status; text = await r.text();
      } catch (e) { status = 'NO-RESPONSE'; }
      await new Promise((r) => setTimeout(r, 100));
      rows.push({ route: `${m} ${p}`, value: vn, status, body: text.slice(0, 160), logs: logs.slice(), unhandled: unhandled.length - u0 });
      expect(true).toBe(true);
    });
  }
});
