// QA GATE 85 probe (not part of the PR). Copied into the gate clone's src/__tests__ for the run only, then moved out.
// Measures what the GDPR erasure cascade (dbDeleteUserData) does, via BOTH callers: DELETE /api/kyc/user/:userId/data
// and the real user.erased subscriber handler (bus stubbed so the handler is captured), when the verification SELECT
// (and optionally the DELETEs) reject with an ordinary Error vs an unreadable thrown value.
import { describe, it, vi, beforeAll, afterAll } from 'vitest';
import http from 'http';
import { appendFileSync } from 'fs';

process.env.KYC_PROVIDER = 'mock';
process.env.NODE_ENV = 'test';
process.env.REDIS_URL = 'redis://gate85-stub:6379';

const OUT = process.env.PROBE_OUT as string;
const h = vi.hoisted(() => ({
  mode: 'none' as string,
  toThrow: undefined as unknown,
  sql: [] as string[],
  logged: [] as string[],
  console: [] as string[],
  unhandled: 0,
  handler: undefined as undefined | ((e: any) => Promise<void>),
}));

const ROW = {
  id: 'v1', user_id: 'U', requested_level: 'HIGH', current_level: 'NONE', status: 'in_progress', provider: 'mock',
  documents: JSON.stringify([{ id: 'd1', type: 'passport', frontImageId: 'img-front-legacy', backImageId: 'img-back-legacy' }]),
  liveness_completed: false, checks: '[]', consent_given: true, created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
};

vi.mock('../db', () => ({
  initDb: async () => undefined,
  isDbAvailable: () => true,
  query: (sql: string, params?: any[]) => {
    const s = String(sql).replace(/\s+/g, ' ').trim();
    const isSelectByUser = /FROM svc_kyc_verifications WHERE user_id/i.test(s) && /^SELECT/i.test(s);
    const isDelete = /^DELETE/i.test(s);
    if (isSelectByUser || isDelete) h.sql.push((isDelete ? s : 'SELECT verifications by user_id') + (params ? ' ' + JSON.stringify(params) : ''));
    if (isSelectByUser && (h.mode === 'selectFails' || h.mode === 'allFail')) return Promise.reject(h.toThrow);
    if (isDelete && h.mode === 'allFail') return Promise.reject(h.toThrow);
    if (isSelectByUser) return Promise.resolve({ rows: [ROW] });
    if (isDelete) return Promise.resolve({ rows: [], rowCount: /svc_kyc_verifications/.test(s) ? 1 : 0 });
    return Promise.resolve({ rows: [] });
  },
}));
vi.mock('../subjectDeks', () => ({
  subjectDeks: { getOrCreateDek: async () => Buffer.alloc(32, 7), getDek: async () => Buffer.alloc(32, 7), evict: () => { h.sql.push('evict DEK'); } },
}));
vi.mock('../utils/logger', () => {
  const push = (lvl: string) => (...a: unknown[]) => { try { h.logged.push(lvl + ':' + String(a[0]) + ':' + JSON.stringify(a[1])); } catch { h.logged.push(lvl + ':unserialisable'); } };
  const logger = { info: () => undefined, warn: push('warn'), debug: () => undefined, error: push('error') };
  return { logger, createLogger: () => logger, validateEnv: () => undefined };
});
vi.mock('@secuura/shared', async (importOriginal) => {
  const actual = await importOriginal<Record<string, unknown>>();
  return {
    ...actual,
    encryptFieldWithDek: (plain: string) => plain,
    isEncryptedPii: () => false,
    isSubjectDekCiphertext: () => false,
    authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
    initEventBus: () => undefined,
    getEventBus: () => ({ subscribe: (_t: unknown, _g: unknown, handler: any) => { h.handler = handler; return new Promise(() => undefined); } }),
  };
});
vi.mock('express', async (importOriginal) => {
  const actual: any = (await importOriginal<any>()).default ?? (await importOriginal<any>());
  const factory: any = (...args: any[]) => { const app = actual(...args); app.listen = () => ({ close: (cb?: () => void) => cb?.(), address: () => ({ port: 0 }), on() { return this; } }); return app; };
  Object.assign(factory, actual);
  return { ...actual, default: factory };
});

const SAVED = process.listeners('unhandledRejection');
const onUnhandled = () => { h.unhandled += 1; };
let server: http.Server; let origin: string;
const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('db down'),
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  throwingGetter: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
};
const safe = (v: unknown) => { try { return v instanceof Error ? 'Error:' + v.message : typeof v; } catch { return 'unreadable'; } };
const rec = (o: any) => appendFileSync(OUT, JSON.stringify(o) + '\n');
const reset = (mode: string, kind: string) => { h.mode = mode; h.toThrow = KINDS[kind](); h.sql = []; h.logged = []; h.console = []; h.unhandled = 0; };
const settle = () => new Promise((r) => setTimeout(r, 300));

beforeAll(async () => {
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
  vi.spyOn(console, 'log').mockImplementation((...a: unknown[]) => { h.console.push(String(a[0])); });
  const app = (await import('../index')).default as any;
  server = http.createServer(app);
  await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
  origin = 'http://127.0.0.1:' + String((server.address() as any).port);
  await settle();
}, 120_000);
afterAll(async () => {
  (server as any)?.closeAllConnections?.();
  await new Promise<void>((r) => server.close(() => r()));
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED) process.on('unhandledRejection', l as any);
});

const cascadeLog = () => h.console.filter((c) => c.includes('[cascade]') || c.includes('GDPR'));
const MODES = ['none', 'selectFails', 'allFail'];
describe('gate85 erasure probe', () => {
  it('subscriber handler was captured (positive control)', () => { rec({ probe: 'handler_captured', captured: typeof h.handler === 'function' }); });
  for (const mode of MODES) for (const kind of Object.keys(KINDS)) {
    if (mode === 'none' && kind !== 'ordinary') continue;
    it(`DELETE route [${mode}/${kind}]`, async () => {
      reset(mode, kind);
      const res = await fetch(origin + '/api/kyc/user/U/data', { method: 'DELETE', signal: AbortSignal.timeout(2500) }).catch(() => undefined);
      const body: any = res ? await res.json().catch(() => undefined) : undefined;
      await settle();
      rec({ probe: 'route', mode, kind, status: res ? res.status : 'UNANSWERED', body, unhandled: h.unhandled, sql: h.sql, logged: h.logged, cascadeLog: cascadeLog() });
    }, 20_000);
    it(`subscriber handler [${mode}/${kind}]`, async () => {
      reset(mode, kind);
      let outcome = 'resolved'; let thrown: any = null;
      try { await h.handler!({ payload: { userId: 'U', dsrId: 'dsr-1' } }); } catch (e) { outcome = 'rejected'; thrown = safe(e); }
      rec({ probe: 'subscriber', mode, kind, outcome, thrown, sql: h.sql, logged: h.logged, cascadeLog: cascadeLog() });
    }, 20_000);
  }
});
