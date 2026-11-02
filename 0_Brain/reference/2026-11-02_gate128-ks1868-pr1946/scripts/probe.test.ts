// QA gate 128 probe: REAL retentionScheduler.ts; only gdprService.enforceRetention and the logger are replaced (logger optionally forwards to the REAL logger).
import * as fs from 'fs';
const mockEnforce = jest.fn();
const mockErr = jest.fn();
const mockInfo = jest.fn();
const mockWarn = jest.fn();
jest.mock('../services/gdprService', () => ({ enforceRetention: mockEnforce }));
jest.mock('../utils/logger', () => ({ logger: { info: mockInfo, warn: mockWarn, error: mockErr, debug: jest.fn() } }));
import { startRetentionScheduler, stopRetentionScheduler } from '../services/retentionScheduler';

function rp(): object { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
function getterErr(fn: () => unknown): Error { const e = new Error('hidden'); Object.defineProperty(e, 'message', { get: fn }); return e; }
const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('ordinary msg'),
  string: () => 'thrown string',
  revokedProxy: () => rp(),
  throwingGetter: () => getterErr(() => { throw new Error('getter threw'); }),
  getterRevokedProxy: () => getterErr(() => rp()),
  getterThrowingToJSON: () => getterErr(() => ({ toJSON() { throw new Error('tojson'); } })),
};
const out: any[] = [];
let unhandled = 0;
const onUnh = () => { unhandled++; };
beforeAll(() => { process.on('unhandledRejection', onUnh); });
afterAll(() => { process.removeListener('unhandledRejection', onUnh); fs.writeFileSync(process.env.PROBE_OUT as string, out.map((o) => JSON.stringify(o)).join('\n') + '\n'); });
beforeEach(() => { mockEnforce.mockReset(); mockErr.mockReset(); mockInfo.mockReset(); mockWarn.mockReset(); jest.useFakeTimers({ doNotFake: ['setImmediate', 'nextTick'] }); process.env.RETENTION_STARTUP_DELAY_MS = '10'; });
afterEach(() => { stopRetentionScheduler(); jest.clearAllTimers(); jest.useRealTimers(); });
const flush = async () => { for (let i = 0; i < 20; i++) await Promise.resolve(); await new Promise<void>((r) => setImmediate(r)); };
const safe = (v: unknown) => { try { return typeof v === 'string' ? v : 'typeof:' + typeof v; } catch { return 'unprintable'; } };

describe.each([['mockLogger'], ['realLogger']])('%s', (mode) => {
  it.each(Object.keys(KINDS))('%s', async (kind) => {
    let realThrew: string[] = [];
    let realCalls = 0;
    if (mode === 'realLogger') {
      const real = jest.requireActual('../utils/logger').logger;
      real.transports.forEach((t: any) => { t.log = (_i: unknown, n: () => void) => n(); });
      mockErr.mockImplementation((...a: unknown[]) => { realCalls++; try { return real.error(...a); } catch (e) { realThrew.push(safe((e as Error)?.message)); throw e; } });
    }
    const before = unhandled;
    // tick 1 (startup), tick 2 (first interval) reject with the value; tick 3 resolves -> sweep continues
    mockEnforce.mockRejectedValueOnce(KINDS[kind]()).mockRejectedValueOnce(KINDS[kind]()).mockResolvedValueOnce([{ recordsAffected: 3 }]);
    startRetentionScheduler();
    jest.advanceTimersByTime(10); await flush();
    const c1 = mockEnforce.mock.calls.length;
    jest.advanceTimersByTime(24 * 3600 * 1000); await flush();
    jest.advanceTimersByTime(24 * 3600 * 1000); await flush();
    out.push({ mode, kind, enforceCalls: [c1, mockEnforce.mock.calls.length],
      errCalls: mockErr.mock.calls.map((c) => [c[0], Object.keys(c[1] || {}), safe((c[1] || {}).error), typeof (c[1] || {}).error]),
      infoCalls: mockInfo.mock.calls.map((c) => c[0]), timers: jest.getTimerCount(), realCalls, realThrew,
      unhandled: unhandled - before });
  });
});
