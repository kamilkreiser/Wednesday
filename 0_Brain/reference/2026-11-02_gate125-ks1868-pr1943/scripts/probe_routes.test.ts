// gate 125 probe (NOT part of the PR): real routes/certifications.ts + real certificationRepo.ts; only ../db, the logger, auth and chargeEvents are replaced.
import * as fs from 'fs';
const OUT = process.env.PROBE_OUT as string;
const mockLog = { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() };
const mockQuery = jest.fn();
const mockExec = jest.fn(async () => 1);
const mockCharge = jest.fn(async () => ({ id: 'charge-new', eventType: 'evidence_export' }));
jest.mock('../db', () => ({
  prisma: { $queryRaw: (...a: unknown[]) => (mockQuery as any)(...a), $executeRaw: (...a: unknown[]) => (mockExec as any)(...a), $executeRawUnsafe: jest.fn() },
  withTenant: jest.fn(),
}));
jest.mock('../services/chargeEvents', () => ({ createChargeEvent: (...a: unknown[]) => (mockCharge as any)(...a), getChargeEventsByCertification: jest.fn(async () => []) }));
jest.mock('../utils/notificationClient', () => ({ notifyDocumentCertified: jest.fn(), notifyDocumentRevoked: jest.fn(), notifyDocumentShared: jest.fn() }));
jest.mock('../events', () => ({ publishEvent: jest.fn(async () => undefined), EventTypes: { CERTIFICATION_ISSUED: 'certification.issued' } }));
jest.mock('../repositories/documentRepo', () => ({ getDocument: jest.fn(), saveDocument: jest.fn(), assertNoCycle: jest.fn(), generateContentHash: jest.fn(() => 'h') }));
jest.mock('../middleware/auth', () => ({ authenticate: () => (req: any, _r: unknown, next: () => void) => { req.user = { userId: 'u1', role: 'super_admin' }; next(); } }));
jest.mock('../utils/logger', () => ({ logger: mockLog }));
import express from 'express';
import { certificationsRouter } from '../routes/certifications';
const TENANT = 'a0000000-0000-4000-8000-0000000000aa';
const ID = 'aaaaaaaa-1111-4111-8111-111111111111';
const app = express();
app.use((req: any, _r: unknown, next: () => void) => { req.tenantId = TENANT; next(); });
app.use('/api/certifications', express.json(), certificationsRouter);
let base = ''; let server: any;
beforeAll(async () => { await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); }); base = `http://127.0.0.1:${server.address().port}`; });
afterAll(() => { server?.close(); });
const safe = (v: unknown): string => { try { return typeof v === 'string' ? v : '<non-string:' + (() => { try { return String(v); } catch { return 'unprintable'; } })() + '>'; } catch { return 'unprintable'; } };
const unhandled: string[] = [];
process.on('unhandledRejection', () => unhandled.push('unhandled'));
const proxy = () => { const { proxy: p, revoke } = Proxy.revocable({}, {}); revoke(); return p; };
const thrownKinds: Record<string, () => unknown> = {
  ordinaryError: () => new Error('probe ordinary'),
  thrownString: () => 'probe string',
  revokedProxy: proxy,
  throwingGetter: () => Object.defineProperty(new Error('h'), 'message', { get() { throw new Error('getter threw'); } }),
  getterReturnsProxy: () => Object.defineProperty(new Error('h'), 'message', { get() { return proxy(); } }),
};
const row = { id: ID, issuer_user_id: 'u1', owner_user_id: 'u2', status: 'certified', metadata: {}, certification_metadata: {}, created_at: new Date(), updated_at: new Date() };
const routes = [
  { name: 'list', path: '', rowFirst: false },
  { name: 'lineage', path: `/${ID}/lineage`, rowFirst: true },
  { name: 'evidence', path: `/${ID}/evidence-bundle`, rowFirst: true },
];
describe.each(routes)('probe $name', (r) => {
  it.each(Object.keys(thrownKinds))('%s', async (k) => {
    jest.clearAllMocks(); unhandled.length = 0;
    let n = 0;
    mockQuery.mockImplementation(async () => { n++; if (r.rowFirst && n === 1) return [row]; throw thrownKinds[k](); });
    const res = await fetch(`${base}/api/certifications${r.path}`, { signal: AbortSignal.timeout(3000) }).catch(() => null);
    const body = res ? await res.text() : 'NO ANSWER';
    const logs = (['info', 'warn', 'error'] as const).flatMap((lv) => (mockLog as any)[lv].mock.calls.map((c: any[]) => ({ lv, msg: c[0], error: safe(c[1] && (c[1] as any).error) })));
    fs.appendFileSync(OUT, JSON.stringify({ route: r.name, kind: k, status: res ? res.status : 'NO ANSWER', body, logs, queryCalls: n, execCalls: mockExec.mock.calls.length, chargeCalls: mockCharge.mock.calls.length, unhandled: unhandled.length }) + '\n');
  });
});
