// gate 104 probe 2 (NOT part of the PR). The real retentionScheduler; R1 with enforceRetention replaced, R2 with the REAL gdprService.enforceRetention over a db stand-in.
import * as fs from 'fs';
const OUT = process.env.PROBE_OUT as string;
const emit = (o: unknown) => fs.appendFileSync(OUT, JSON.stringify(o) + '\n');
process.env.RETENTION_STARTUP_DELAY_MS = '5';
process.env.RETENTION_INTERVAL_MS = '60';

const logs: any[] = [];
const stmts: string[] = [];
let failOn: string | null = null; let failV: (() => unknown) | null = null;
const POLICIES = [
  { id: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1', data_type: 'user_sessions', retention_period_days: 30, deletion_method: 'delete', auto_delete: true },
  { id: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa2', data_type: 'verification_requests', retention_period_days: 30, deletion_method: 'delete', auto_delete: true },
  { id: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa3', data_type: 'share_records', retention_period_days: 30, deletion_method: 'delete', auto_delete: true },
];
function op(strings: TemplateStringsArray): string {
  const s = strings.join('?').replace(/\s+/g, ' ').trim();
  if (/FROM data_retention_policies/.test(s)) return 'SELECT policies';
  const m = /DELETE FROM (\w+)/.exec(s); if (m) return 'DELETE ' + m[1];
  if (/INSERT INTO data_deletion_log/.test(s)) return 'INSERT deletion_log';
  if (/UPDATE data_retention_policies/.test(s)) return 'UPDATE policy stamp';
  return 'other';
}
async function q(strings: TemplateStringsArray): Promise<any> {
  const o = op(strings); stmts.push(o);
  if (failOn && o === failOn && failV) throw failV();
  if (o === 'SELECT policies') return POLICIES;
  if (o.startsWith('DELETE')) return 2;
  if (o === 'INSERT deletion_log') return [{ id: 'x', data_type: 'd', records_affected: 2, deletion_method: 'delete', reason: 'r', performed_by: 'system', performed_at: new Date() }];
  return 1;
}
jest.mock('../db', () => ({ prisma: { $queryRaw: (s: any) => q(s), $executeRaw: (s: any) => q(s) } }));
jest.mock('../utils/logger', () => ({
  logger: { info: (...a: any[]) => logs.push(['info', ...a]), warn: (...a: any[]) => logs.push(['warn', ...a]), error: (...a: any[]) => logs.push(['error', ...a]), debug: () => {} },
}));
const mockEnforce = jest.fn();
let useReal = false;
jest.mock('../services/gdprService', () => {
  const real = jest.requireActual('../services/gdprService');
  return { ...real, enforceRetention: (...a: any[]) => (useReal ? real.enforceRetention(...a) : mockEnforce(...a)) };
});

function revokedProxy(): object { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
function throwingGetter(): Error { const e = new Error('hidden'); Object.defineProperty(e, 'message', { get() { throw new Error('getter'); } }); return e; }
const KINDS: Record<string, () => unknown> = { ordinaryError: () => new Error('db down'), string: () => 'plain string', revokedProxy, throwingGetter };

// eslint-disable-next-line @typescript-eslint/no-var-requires
const sched = require('../services/retentionScheduler');
const unhandled: string[] = [];
const onUR = (r: unknown) => { let t = 'unreadable'; try { t = String((r as any)?.message ?? r); } catch { /* */ } unhandled.push(t); };

async function twoRuns(): Promise<void> {
  sched.startRetentionScheduler();
  await new Promise((s) => setTimeout(s, 5 + 60 + 40));
  sched.stopRetentionScheduler();
  await new Promise((s) => setTimeout(s, 20));
}

describe('R1 runEnforcement with enforceRetention rejecting', () => {
  beforeAll(() => process.on('unhandledRejection', onUR));
  afterAll(() => process.off('unhandledRejection', onUR));
  for (const k of Object.keys(KINDS)) {
    it(`R1 ${k}`, async () => {
      logs.length = 0; unhandled.length = 0; useReal = false;
      mockEnforce.mockReset(); mockEnforce.mockRejectedValueOnce(KINDS[k]()); mockEnforce.mockResolvedValue([]);
      let thrownOut = 'none';
      try { await twoRuns(); } catch (e) { thrownOut = 'threw'; }
      emit({ probe: 'R1', kind: k, enforceCalls: mockEnforce.mock.calls.length, logs: JSON.parse(JSON.stringify(logs)), unhandled: [...unhandled], thrownOut });
    });
  }
});

describe('R2 REAL enforceRetention: one policy statement rejects', () => {
  beforeAll(() => process.on('unhandledRejection', onUR));
  afterAll(() => process.off('unhandledRejection', onUR));
  const cases: Array<[string, string]> = [['DELETE user_sessions', 'first policy DELETE'], ['DELETE verification_requests', 'second policy DELETE'], ['SELECT policies', 'policy SELECT']];
  for (const [target, label] of cases) {
    for (const k of ['none', ...Object.keys(KINDS)]) {
      it(`R2 ${label} ${k}`, async () => {
        logs.length = 0; stmts.length = 0; unhandled.length = 0; useReal = true;
        failOn = k === 'none' ? null : target; failV = k === 'none' ? null : KINDS[k];
        sched.startRetentionScheduler();
        await new Promise((s) => setTimeout(s, 40));
        sched.stopRetentionScheduler();
        failOn = null; failV = null;
        await new Promise((s) => setTimeout(s, 20));
        emit({ probe: 'R2', target: label, kind: k, stmts: [...stmts], logs: JSON.parse(JSON.stringify(logs)), unhandled: [...unhandled] });
      });
    }
  }
});
