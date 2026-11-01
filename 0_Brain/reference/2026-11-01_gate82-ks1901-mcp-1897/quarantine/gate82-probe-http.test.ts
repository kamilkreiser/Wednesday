import { describe, it, expect, vi, beforeAll, beforeEach, afterEach } from 'vitest';
import type { MockInstance } from 'vitest';
import { hostile, SECRETVAL } from './hostile.js';
const h = vi.hoisted(() => ({ routes: {} as Record<string, (req: unknown, res: unknown) => Promise<void>>, toThrow: undefined as unknown, mode: 'throw' as string }));
vi.mock('express', () => {
  const app = { use: () => app, get: (p: string, f: any) => { h.routes['GET ' + p] = f; }, post: (p: string, f: any) => { h.routes['POST ' + p] = f; }, listen: () => ({}) };
  return { default: Object.assign(() => app, { json: () => () => undefined }) };
});
vi.mock('@secuura/shared', () => ({ enforceProductionConfig: () => undefined, rejectNulBytes: () => () => undefined }));
vi.mock('../api-client.js', () => {
  const next = () => (h.mode === 'throw' ? Promise.reject(h.toThrow) : Promise.resolve({ ok: true, status: 200, data: { id: 'ok' } }));
  return { registerDocument: next, verifyDocument: next, listDocuments: next, getWorkflowInstance: next, getConnectorInfo: next, getVerificationPolicy: next };
});
vi.mock('../hashing.js', () => ({ hashFile: () => Promise.reject(h.toThrow), extractFileName: (p: string) => p, hashBuffer: () => 'sha256:0' }));
vi.mock('../package-generator.js', () => ({ generatePackage: () => Promise.resolve() }));
let errSpy: MockInstance<typeof console.error>;
beforeAll(async () => { await import('../http-server.js'); });
beforeEach(() => { errSpy = vi.spyOn(console, 'error').mockImplementation(() => undefined); });
afterEach(() => errSpy.mockRestore());
for (const [route, item] of [['POST /register-batch', { title: 'T', documentType: 'c', contentHash: 'sha256:a' }], ['POST /verify-batch', { documentId: 'd' }]] as const) {
  describe('gate82 http probe ' + route, () => {
    for (const [label, f] of hostile()) {
      it(label, async () => {
        h.toThrow = f(); h.mode = 'throw';
        const res: any = { statusCode: 200, body: undefined, status(c: number) { res.statusCode = c; return res; }, json(b: unknown) { res.body = b; return res; }, setHeader() {} };
        let threw: unknown = null;
        try { await h.routes[route]({ body: { documents: [item, item] } }, res); } catch (e) { threw = e; }
        const log = errSpy.mock.calls.map((a) => a.map((x) => typeof x === 'string' ? x : '<<' + typeof x + '>>').join(' ')).join('\n');
        console.log('PROBE http', route, '|', label, '| status=', res.statusCode, '| body=', JSON.stringify(res.body), '| threw=', threw ? 'YES' : 'no', '| log=', JSON.stringify(log));
        expect(threw).toBeNull();
        expect(res.statusCode).toBe(200);
        expect(JSON.stringify(res.body)).not.toContain(SECRETVAL);
        expect(log).not.toContain('<<');
      });
    }
  });
}
