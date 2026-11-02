// QA gate 102 probe (NOT part of the PR). Runs the REAL dbSaveAlert (exported via a copy of the product file) and the real
// acknowledgeAlert path, with only ../db and ../utils/logger replaced. Prints one JSON line per cell: PROBE {...}
import { describe, it, expect, vi } from 'vitest';

const h = vi.hoisted(() => ({ toThrow: undefined as unknown, info: [] as any[], queries: 0, unhandled: [] as any[] }));
vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: () => { h.queries += 1; return Promise.reject(h.toThrow); },
}));
vi.mock('../utils/logger', () => ({
  logger: {
    info: (...a: any[]) => { h.info.push(a); },
    warn: (...a: any[]) => { h.info.push(['WARN', ...a]); },
    error: (...a: any[]) => { h.info.push(['ERROR', ...a]); },
    debug: () => {},
  },
}));
process.on('unhandledRejection', (r) => { h.unhandled.push('x'); });

import * as mod from '../services/zz_probe_jobs';
import { AlertSeverity } from '../types';

const flush = () => new Promise<void>((r) => setTimeout(r, 5));
const kinds: Record<string, () => unknown> = {
  ordinaryError: () => new Error('db down'),
  zodLikeError: () => Object.assign(new Error('zod issue'), { name: 'ZodError', issues: [{ path: ['secretField'], message: 'bad' }] }),
  string: () => 'plain string failure',
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  messageGetter: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
};

describe('probe', () => {
  for (const [k, mk] of Object.entries(kinds)) {
    it('direct dbSaveAlert ' + k, async () => {
      h.info.length = 0; h.queries = 0; h.unhandled.length = 0; h.toThrow = mk();
      const alert: any = { id: 'a-' + k, ruleId: 'r', severity: AlertSeverity.INFO, message: 'm', value: 5, threshold: 1, triggeredAt: new Date() };
      let outcome = 'resolved';
      try { await (mod as any).dbSaveAlert(alert); } catch { outcome = 'REJECTED'; }
      await flush();
      require('fs').appendFileSync(process.env.PROBE_OUT as string, JSON.stringify({ cell: 'direct/' + k, outcome, queries: h.queries, logs: h.info.map((c) => [c[0], c[1]]), unhandled: h.unhandled.length }) + '\n');
      expect(true).toBe(true);
    });
    it('via acknowledgeAlert ' + k, async () => {
      h.toThrow = undefined;
      const jobs: any = new (mod as any).ScheduledJobs({ getCounter: () => 5 } as never, {} as never);
      jobs.addAlertRule({ id: 'rule-' + k, name: 'n', metric: 'm', condition: 'gt', threshold: 1, severity: AlertSeverity.INFO, enabled: true, cooldownMinutes: 1 });
      await flush();
      jobs.evaluateAlerts();
      const alert = jobs.getActiveAlerts().find((a: any) => a.ruleId === 'rule-' + k);
      h.info.length = 0; h.queries = 0; h.unhandled.length = 0; h.toThrow = mk();
      const ret = jobs.acknowledgeAlert(alert.id);
      await flush();
      require('fs').appendFileSync(process.env.PROBE_OUT as string, JSON.stringify({ cell: 'ack/' + k, returned: ret, ackSet: !!alert.acknowledgedAt, queries: h.queries, logs: h.info.map((c) => [c[0], c[1]]), unhandled: h.unhandled.length }) + '\n');
      expect(true).toBe(true);
    });
  }
});
