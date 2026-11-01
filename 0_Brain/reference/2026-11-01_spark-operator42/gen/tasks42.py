TASKS={}
AP='Blockchain/Dev/services/analytics/'
A_REF=AP+'src/__tests__/ks1868-export-service-load-unreadable-throw.test.ts'
E_OLD="""    } catch (err: any) {
      logger.info('DB save export failed', { error: err instanceof Error ? err.message : String(err) });
    }
"""
E_NEW="""    } catch (err: any) {
      let reason: string;
      try {
        reason = err instanceof Error ? err.message : String(err);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.info('DB save export failed', { error: reason });
    }
"""
FLAGS_HEAD="""import { describe, it, expect, vi, beforeEach } from 'vitest';
"""
E_TEST="""import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: ExportService.dbSaveExport must still log its INFO line (and resolve) when the thrown
// value itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message`
// getter throws, throws on `.message`).
// The db stand-in is a plain function, not a vi.fn(): a spy inspects what it rejects with and
// could itself fail on a revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  info: vi.fn(),
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: () => Promise.reject(h.toThrow),
}));

vi.mock('../utils/logger', () => ({
  logger: { info: h.info, warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
}));

import { ExportService } from '../services/exportService';

const EXPORT = {
  id: 'ks1868-export',
  status: 'pending' as const,
  type: 'overview',
  format: 'json',
  createdAt: '2026-11-01T00:00:00.000Z',
};
const SAVES = () => h.info.mock.calls.filter((c) => String(c[0]).includes('DB save export failed'));
const save = () =>
  (new ExportService() as unknown as { dbSaveExport(e: unknown): Promise<void> }).dbSaveExport(EXPORT);

describe('KS-1868 ExportService.dbSaveExport reads the thrown value safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.info.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message', async () => {
    h.toThrow = new Error('db down');
    await save();
    expect(SAVES()).toHaveLength(1);
    expect(SAVES()[0][1]).toEqual({ error: 'db down' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    await save().catch(() => undefined);
    expect(SAVES()).toHaveLength(1);
    expect(SAVES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    await save().catch(() => undefined);
    expect(SAVES()).toHaveLength(1);
    expect(SAVES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
"""
S_OLD="""  } catch (err: any) {
    logger.info('DB save alert rule failed', { error: err instanceof Error ? err.message : String(err) });
  }
"""
S_NEW="""  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.info('DB save alert rule failed', { error: reason });
  }
"""
S_TEST="""import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: dbSaveAlertRule (reached through ScheduledJobs.addAlertRule, which swallows its
// rejection) must still log its INFO line when the thrown value itself cannot be read (a revoked
// Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`).
// The db stand-in is a plain function, not a vi.fn(): a spy inspects what it rejects with and
// could itself fail on a revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  info: vi.fn(),
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: () => Promise.reject(h.toThrow),
}));

vi.mock('../utils/logger', () => ({
  logger: { info: h.info, warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
}));

import { ScheduledJobs } from '../services/scheduledJobs';
import { AlertSeverity } from '../types';
import type { AlertRule } from '../types';

const RULE: AlertRule = {
  id: 'ks1868-rule',
  name: 'KS-1868 rule',
  metric: 'ks1868.metric',
  condition: 'gt',
  threshold: 1,
  severity: AlertSeverity.INFO,
  enabled: true,
  cooldownMinutes: 1,
};
const SAVES = () => h.info.mock.calls.filter((c) => String(c[0]).includes('DB save alert rule failed'));
const flush = () => new Promise<void>((resolve) => setTimeout(resolve, 0));

/** Build ScheduledJobs, let the default-rule saves settle, then add ONE rule and let it settle. */
async function addOneRule(): Promise<void> {
  const jobs = new ScheduledJobs({} as never, {} as never);
  await flush();
  h.info.mockReset();
  jobs.addAlertRule(RULE);
  await flush();
}

describe('KS-1868 dbSaveAlertRule reads the thrown value safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.info.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message', async () => {
    h.toThrow = new Error('db down');
    await addOneRule();
    expect(SAVES()).toHaveLength(1);
    expect(SAVES()[0][1]).toEqual({ error: 'db down' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    await addOneRule();
    expect(SAVES()).toHaveLength(1);
    expect(SAVES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    await addOneRule();
    expect(SAVES()).toHaveLength(1);
    expect(SAVES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
"""
S9="This file is neither `tenant-context.ts` nor `tenant-pool-manager.ts` and is outside services/auth, services/originate, services/anchoring, services/tenant-provisioning and vc-issuer; the S9 brief itself was not re-read by the operator."
TASKS['p1']=dict(svc='analytics', runner_dir='Blockchain/Dev/services/analytics', ref=A_REF, s9note=S9,
 dir='ks_1868_o42_p1_analytics_exportservice_dbsaveexport_unreadable_throw',
 prod=AP+'src/services/exportService.ts', test=AP+'src/__tests__/ks1868-export-service-db-save-unreadable-throw.test.ts',
 old=E_OLD, new=E_NEW, tbody=E_TEST, where_line=56, fn='`ExportService.dbSaveExport`', file='exportService.ts',
 intro_site="the catch block of `ExportService.dbSaveExport` in `services/exportService.ts`",
 where_note="The catch block starts at line 55 (`} catch (err: any) {`); it logs the INFO line 'DB save export failed' with `{ error: <message> }`. The message is only logged: it is not stored on the export record and not returned (the method returns void). The other catch in this file that stores a message on the record (line 160, `exportResult.error`) is NOT in this brief.",
 whatwrong=("In `exportService.ts` the catch block of `dbSaveExport` (line 55) logs `logger.info('DB save export failed', { error: err instanceof Error ? err.message : String(err) })` (the read is on line 56). "
  "If the database call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
  "Either way the catch throws before the INFO line is logged: `dbSaveExport()` rejects, no log line is written, and every caller (`createExport`, `processExport`, in the failure path as well) is cut short instead of continuing with the in-memory copy it already set. "
  "The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }` and the log text is unchanged."),
 consequence="Today a hostile rejection from the database layer makes the catch block itself throw, so nothing is logged and `dbSaveExport` rejects instead of falling back to the in-memory copy.",
 red1="At the tip the call rejects (the test swallows that with `.catch`), so no INFO line is logged and the log-count assertion fails",
 dbnote="`../db` and `../utils/logger` are mocked; no database, no app boot and no network. `dbSaveExport` is private, so the test reaches it through a type cast on a fresh `ExportService`.",
 sibling="The other `instanceof Error` reads in `exportService.ts` (the loadFromDb catch, already fixed, and the `processExport` catch at line 160 that stores the message on the export record) are NOT in this brief")
TASKS['p2']=dict(svc='analytics', runner_dir='Blockchain/Dev/services/analytics', ref=A_REF, s9note=S9,
 dir='ks_1868_o42_p2_analytics_scheduledjobs_dbsavealertrule_unreadable_throw',
 prod=AP+'src/services/scheduledJobs.ts', test=AP+'src/__tests__/ks1868-scheduled-jobs-save-alert-rule-unreadable-throw.test.ts',
 old=S_OLD, new=S_NEW, tbody=S_TEST, where_line=59, fn='`dbSaveAlertRule`', file='scheduledJobs.ts',
 intro_site="the catch block of the module function `dbSaveAlertRule` in `services/scheduledJobs.ts`",
 where_note="The catch block starts at line 58 (`} catch (err: any) {`); it logs the INFO line 'DB save alert rule failed' with `{ error: <message> }`. The message is only logged (the function returns void; both callers, `initializeDefaultAlertRules` and `addAlertRule`, end in `.catch(() => {})`).",
 whatwrong=("In `scheduledJobs.ts` the catch block of `dbSaveAlertRule` (line 58) logs `logger.info('DB save alert rule failed', { error: err instanceof Error ? err.message : String(err) })` (the read is on line 59). "
  "If the database call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
  "Either way the catch throws before the INFO line is logged: the returned promise rejects, the callers' `.catch(() => {})` swallow it, and the operator sees no log line at all. "
  "The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }` and the log text is unchanged."),
 consequence="Today a hostile rejection from the database layer makes the catch block itself throw, the callers swallow the rejection, and nothing is logged.",
 red1="At the tip the helper rejects and the caller swallows it, so no INFO line is logged and the log-count assertion fails",
 dbnote="`../db` and `../utils/logger` are mocked; no database, no cron start and no network. `dbSaveAlertRule` is not exported, so the test reaches it through `new ScheduledJobs(...).addAlertRule(...)` (the collaborators are never called) and waits one macrotask; the constructor's default-rule saves are let settle and the logger mock is reset before the rule under test is added.",
 sibling="`dbSaveAlert` (line 85) has the same shape but is NOT in this brief")
